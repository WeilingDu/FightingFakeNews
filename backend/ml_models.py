from settings import db
from models import Speaker, Party, News, Metrics
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn import metrics
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
import numpy as np
import scipy
from scipy import sparse
import pickle as pkl
from datetime import datetime
import utils

label_mapping = {
    "Pants on Fire!": 0,
    "False": 1,
    "Mostly False": 2,
    "Half-True": 3,
    "Mostly True": 4,
    "True": 5,
}
predict_mapping = {v: k for k, v in label_mapping.items()}


# feature : statement, speaker, party, state, speaker ch ,
def get_data():
    news = News.query.all()
    news = [n for n in news if n.label in label_mapping]
    return news


def tf_idf_model(news):
    statements = [n.statement for n in news]

    cv = CountVectorizer(stop_words="english", decode_error='ignore')

    d_count_vect = cv.fit_transform(statements)

    m = TfidfTransformer()
    tf_idf_feature = m.fit_transform(d_count_vect)

    # save model
    with open("saver/tf-idf/cv.pkl", "wb") as f:
        pkl.dump(cv, f)
    with open("saver/tf-idf/tf-idf.pkl", "wb") as f:
        pkl.dump(m, f)

    return tf_idf_feature


def prepare_training_data(mode):
    """
    mode -> int :
    1 : only statement
    2 : + speaker
    3 : + party
    4 : + speaker home state
    5 : + speaker credit history
    :param mode:
    :return: combination of features
    """
    if not 1 <= mode <= 5:
        raise ValueError("1 <= mode <= 5, plz check the doc")

    news = get_data()

    news = [n for n in news if n.label in label_mapping]

    labels = [label_mapping[n.label] for n in news]
    tf_idf_f = tf_idf_model(news).toarray()
    other_features = more_features(news)
    comb_features = tf_idf_f
    comb_features = feature_combinations(comb_features, other_features, mode)

    return comb_features, labels


def feature_combinations(comb_features, features, mode: int):
    # 不断累加特征
    if mode >= 2:
        comb_features = sparse.hstack((comb_features, features["speaker"]))
    if mode >= 3:
        comb_features = sparse.hstack((comb_features, features["party"]))
    if mode >= 4:
        comb_features = sparse.hstack((comb_features, features["state"]))
    if mode >= 5:
        comb_features = sparse.hstack((comb_features, features["ch"]))
    return comb_features


def one_hot_features(original_data, feature_name):
    le = preprocessing.LabelEncoder()
    label_encoder = le.fit_transform(original_data)
    ohe = preprocessing.OneHotEncoder(categories="auto")
    feature = ohe.fit_transform(label_encoder.reshape(-1, 1))
    with open(f"saver/encoder/{feature_name}_label_e.pkl", "wb") as f:
        pkl.dump(le, f)
    with open(f"saver/encoder/{feature_name}_onehot_e.pkl", "wb") as f:
        pkl.dump(ohe, f)
    return feature


# 所有特征都是稀疏矩阵存储, 后面计算速度快 类型:sparse.csr_matrix
def more_features(news):
    speaker_info = {}
    for n in news:
        s = Speaker.query.filter(Speaker.name == n.speaker).first()
        if not s:
            print("no such speaker", n.speaker)
            continue
        speaker_info[s.name] = s
    speaker_name = [n.speaker for n in news]

    speaker_onehot = one_hot_features(speaker_name, "speaker")

    ch = [[speaker_info[n.speaker].pants_fire_cnt, speaker_info[n.speaker].false_cnt,
           speaker_info[n.speaker].barely_true_cnt, speaker_info[n.speaker].half_true_cnt,
           speaker_info[n.speaker].mostly_true_cnt, speaker_info[n.speaker].true_cnt]
          for n in news]

    ch = np.array(ch)

    ch = preprocessing.normalize(ch)
    ch = scipy.sparse.csr_matrix(ch)

    party = [n.party for n in news]
    party_onehot = one_hot_features(party, "party")

    state = [speaker_info[n.speaker].state for n in news]
    state_onehot = one_hot_features(state, "state")
    return {"speaker": speaker_onehot, "party": party_onehot, "state": state_onehot, "ch": ch}


def model_factory(model_name):
    if model_name == "rf":
        return RandomForestClassifier()
    elif model_name == "lr":
        return LogisticRegression()
    elif model_name == "svm":
        return SVC()
    elif model_name == "adaboost":
        return AdaBoostClassifier()
    elif model_name == "bayes":
        return MultinomialNB()
    else:
        raise ValueError("not supported model", model_name)


def train_and_save_model(model_name: str, mode: int, test_size: float):
    """
    retrainging the model, save the related model and insert metrics to liar.metrics table
    :param model_name:
    :param mode: feature combinations mode
    :param test_size:
    :return:
    """
    x, y = prepare_training_data(mode)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size)

    clf = model_factory(model_name)
    clf.fit(x_train, y_train)
    save_path = f"saver/model/{model_name}_{mode}.pkl"
    with open(save_path, "wb") as f:
        pkl.dump(clf, f)
    pred = clf.predict(x_test)

    # first find the metrics by save_path, if not exist, insert to db otherwise update
    old_m = Metrics.query.filter(Metrics.save_path == save_path).first()
    if not old_m:
        metric = Metrics()
    else:
        metric = old_m

    metric.model_name = model_name
    metric.save_path = save_path
    metric.mode = mode
    metric.test_size = test_size
    metric.feature_dim = float(x.shape[1])
    metric.sample_nums = float(x.shape[0])
    metric.precision = float(metrics.precision_score(y_test, pred, average="macro"))
    metric.recall = float(metrics.recall_score(y_test, pred, average="macro"))
    metric.f1 = float(metrics.f1_score(y_test, pred, average="macro"))
    metric.accuracy = float(metrics.accuracy_score(y_test, pred))
    if metric.training_times:
        metric.training_times += 1
    else:
        metric.training_times = 1

    metric.last_training_date = datetime.now()

    db.session.add(metric)
    db.session.commit()


def predict(model_name: str, mode: int, news_id: int):
    """
    Predict the label by news_id(liar.news table).
    :param model_name:
    :param mode:
    :param news_id:
    :return:
    """
    news = News.query.get(news_id)
    speaker = news.speaker
    party = news.party
    statement = news.statement
    s = Speaker.query.filter(Speaker.name == news.speaker).first()
    state = s.state

    def text_prepare(t):
        with open("saver/tf-idf/cv.pkl", "rb") as f:
            cv = pkl.load(f)
        with open("saver/tf-idf/tf-idf.pkl", "rb") as f:
            tfidf = pkl.load(f)

        text_feature = tfidf.transform(cv.transform([t]))
        return text_feature

    def other_feature_prepare(feature_data, feature_name):
        with open(f"saver/encoder/{feature_name}_label_e.pkl", "rb") as f:
            le = pkl.load(f)
        with open(f"saver/encoder/{feature_name}_onehot_e.pkl", "rb") as f:
            ohe = pkl.load(f)

        led = le.transform(feature_data)
        return ohe.transform(led.reshape(-1, 1))

    text_f = text_prepare(statement)
    speaker = other_feature_prepare([speaker], "speaker")
    party = other_feature_prepare([party], "party")
    state = other_feature_prepare([state], "state")
    ch = [[s.pants_fire_cnt, s.false_cnt,
           s.barely_true_cnt, s.half_true_cnt,
           s.mostly_true_cnt, s.true_cnt]]

    ch = np.array(ch)

    ch = preprocessing.normalize(ch)
    ch = scipy.sparse.csr_matrix(ch)
    features = text_f
    other_features = {"speaker": speaker, "party": party, "state": state, "ch": ch}
    features = feature_combinations(features, other_features, mode)
    with open(f"saver/model/{model_name}_{mode}.pkl", "rb") as f:
        clf = pkl.load(f)
    return predict_mapping[clf.predict(features)[0]]


def train_save_send_email(model_name: str, mode: int, news_id: int, email: str):
    train_and_save_model(model_name, mode, news_id)
    utils.send_email(email)


def init_model():
    """
    Init model and db(For liar.metrics table).
    Currently model :
    1. RF
    2. LR
    3. SVM
    4. Bayes
    5. AdaBoost
    Currently mode:
    1, 2, 3, 4, 5

    Currently test_size: fixed at 0.3.
    :return:
    """
    for mode in range(1, 6):
        for model_name in ["rf", "lr", "adaboost", "bayes"]:
            train_and_save_model(model_name, mode, test_size=0.3)


def init_model_svm():
    for mode in range(1, 6):
        for model_name in ["svm"]:
            train_and_save_model(model_name, mode, test_size=0.3)


if __name__ == '__main__':
    # get_data()
    # train_and_save_model("rf",1,0.3)
    init_model_svm()
