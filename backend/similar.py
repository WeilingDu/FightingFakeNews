from sklearn.metrics.pairwise import cosine_similarity
import pickle as pkl
from ml_models import get_data
import numpy as np
from config import SIM_LIMITED


def get_tfidf_matrix():
    news = get_data()
    db_id2matrix_id = {n.id: i for i, n in enumerate(news)}
    statement = [n.statement for n in news]
    with open("saver/tf-idf/cv.pkl", "rb") as f:
        cv = pkl.load(f)
    with open("saver/tf-idf/tf-idf.pkl", "rb") as f:
        tfidf = pkl.load(f)

    tfidf_matrix = tfidf.transform(cv.transform(statement))
    return tfidf_matrix, db_id2matrix_id


def get_row_similarities(matrix):
    sim = cosine_similarity(matrix)
    return sim


tfidf_matrix, db_id2matrix_id = get_tfidf_matrix()
matrix_id2db_id = {v: k for k, v in db_id2matrix_id.items()}
sim_matrix = get_row_similarities(tfidf_matrix)


def get_similarities(news_id):
    """
    :param news_id: news id in liar.news table
    :return: top k similar news id (sort by cosine_similarity of tf-idf matrix).
    """

    matrix_id = db_id2matrix_id.get(news_id)
    row_sim = sim_matrix[matrix_id]
    # 获取前 SIM_LIMITED个最大值的索引,也即最相似的新闻
    top_sim_idx = np.argpartition(row_sim, -SIM_LIMITED)[-SIM_LIMITED:]
    top_sim_news_id = [matrix_id2db_id[tsi] for tsi in top_sim_idx]
    top_sim = [round(row_sim[tsi], 3) for tsi in top_sim_idx]
    top = [(nid, c) for nid, c in zip(top_sim_news_id, top_sim)]
    top.sort(key=lambda x: x[1], reverse=True)
    # exclude itself
    return top[1:]


if __name__ == '__main__':
    get_similarities(1)
