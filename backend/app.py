from functools import wraps

import config
from flask import request, abort, g
from settings import app, db, data, data_s, datas
from models import User, Speaker, News, Party, Metrics
from flask_httpauth import HTTPTokenAuth
import re
from config import SEARCH_NEWS_LIMITED, SEARCH_PARTY_LIMITED, SEARCH_SPEAKER_LIMITED
from utils import *
from sqlalchemy import func
from sqlalchemy import and_
from similar import get_similarities
from ml_models import predict, train_save_send_email
import threading

model_name_mapping = {"rf": "RandomForest", "lr": "Logistic Regression",
                      "adaboost": "AdaBoost", "bayes": "Bayes", "svm": "SVM"}
reverse_model_name_mapping = {v: k for k, v in model_name_mapping.items()}

auth = HTTPTokenAuth(scheme='Bearer')


# 定义一个检查权限的装饰器
def admin_required():
    def decorator(func):
        @wraps(func)
        def mywrap(*args, **kwargs):
            if not g.user.admin():
                return generate_result(3, "Insufficient permissions")
            return func(*args, **kwargs)

        return mywrap

    return decorator


@app.route('/user/register', methods=['GET'])
def new_user():
    username = request.args.get('username')
    password = request.args.get('password')
    email = request.args.get('email')
    username = str(username)
    password = str(password)
    if username is None or password is None:
        return generate_result(2, [])
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'code': 0})

    user = User(username=username)
    user.hash_password(password)
    user.email = email
    db.session.add(user)
    db.session.commit()
    return jsonify({'username': user.username, 'code': 1})


@app.route("/user/logout", methods=["GET"])
def logout():
    pass


@auth.verify_token
def verify_token(token):
    user = User.verify_auth_token(token)
    if user:
        g.user = user
        return True
    else:
        return False


@app.route('/user/token', methods=['get'])
def get_auth_token():
    username = request.args.get('username')
    password = request.args.get('password')

    if username is None or password is None:
        abort(400)
    u = User.query.filter_by(username=username).first()
    if u is None:
        print('no such user')
        abort(400)
    u.verify_password(password)
    token = u.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


def count_word(s):
    punc = ['"', '(', ')', ',', '.', '$', ':', '?', '!', '%', '‘']
    cnt = {}
    # i为每个statement
    for i in s:
        # 删除statement中的标点符号
        i = i.replace('’', "'")
        for p in punc:
            i = i.replace(p, '')
        # _i为每个单词
        for _i in i.lower().split(' '):
            _i = _i.strip()
            if not _i.isdigit():
                cnt[_i] = cnt.get(_i, 0) + 1
    d = [{"name": k, "value": v} for k, v in cnt.items() if k not in stop_words]
    return d


def count_ch(fd):
    items = ['True', 'Mostly True', 'Half-True', 'Mostly False', 'False', 'Pants on Fire!']
    credit = []
    for item in items:
        credit.append(fd.count(item))
    ch = {"TrueCounts": credit[0], "mostlyTrueCounts": credit[1], "halfTrueCounts": credit[2],
          "mostlyFalseCounts": credit[3], "FalseCounts": credit[4], "onFireCounts": credit[5]}
    return ch


def count_ch_binary(fd):
    items = ['True', 'Mostly True', 'Half-True', 'Mostly False', 'False', 'Pants on Fire!']
    credit = []
    for item in items:
        credit.append(fd.count(item))
    ch = {"True": credit[0] + credit[1], "False": credit[2] + credit[3] + credit[4] + credit[5]}
    return ch


def eliminate():
    datas['partyAffiliation'] = datas['partyAffiliation'].replace('none', 'independent')
    # 将数据中的标点符号去掉
    data["statement"] = data["statement"].apply(
        lambda x: re.sub('[0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+', "", str(x)))


eliminate()
# 去掉数据中的回车符和空格
data['speaker'] = data['speaker'].apply(lambda x: x.replace("\n", ""))
data_s['speaker'] = data_s['speaker'].apply(lambda x: x.lstrip())
data['statement'] = data['statement'].apply(lambda x: x.rstrip())

# 读取停止词表
with open('liar_dataset/liar_dataset/stopword.txt', 'r') as f:
    stop_words = f.read().splitlines()
    f.close()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/speaker/statements')
@auth.login_required
def speaker_statement():
    # 接受参数sname，返回该speaker所有statement
    sname = request.args.get('sname')
    cnt = request.args.get('cnt')
    d = []
    if sname is None:
        # 没有传入sname,返回状态值2
        status = 2
    elif cnt is not None and not cnt.isdigit():
        status = 2
    else:
        sname = '\n' + sname + '\n'  # 修改数据后删除此行代码
        s = News.query.filter(News.speaker == sname).all()
        if len(s) == 0:
            # 没有speaker的数据，返回状态值1
            status = 1
        else:
            status = 0
            if cnt is None:
                fd = [i.statement for i in s][0:5]
            else:
                fd = [i.statement for i in s][0:int(cnt)]
            for statement in fd:
                y = News.query.filter(News.statement == statement).all()
                year = [i.pub_year for i in y].pop()
                month = [i.pub_month for i in y].pop()
                st = {'statement': statement, "time": month + ' ' + str(year)}
                d.append(st)
    r = {'code': status, 'data': d}
    return jsonify(r)


@app.route('/speaker/info')
@auth.login_required
def speaker_info():
    s_name = request.args.get('sname')
    d = []
    if s_name is None:
        status = 2
    else:
        fd = Speaker.query.filter(Speaker.name == s_name).all()
        if len(fd) == 0:
            status = 1
        else:
            status = 0
            party = [i.party for i in fd].pop()
            state = [i.state for i in fd].pop()
            d = {"party": party, "stateInfo": state}
    r = {'code': status, 'data': d}
    return jsonify(r)


@app.route('/wordcnt/speaker')
@auth.login_required
def word_cnt_by_speaker():
    # 接受参数sname,year
    # 若year为空，返回speaker的所有statements中词的统计
    # 若year不空，返回speaker这一年的statements中词的统计
    sname = request.args.get('sname')
    year = request.args.get('year')
    if sname is None:
        return generate_result(2, [])
    if year is None:
        news = News.query.filter(News.speaker == sname).all()
    else:
        try:
            year = int(year)
        except:
            return generate_result(2, [])
        if year == 0:
            news = News.query.filter(News.speaker == sname).all()
        else:
            news = News.query.filter(News.speaker == sname, News.pub_year == str(year)).all()

    statements = [n.statement for n in news]
    d = count_word(statements)
    return generate_result(0, d)


@app.route('/wordcnt/time')
@auth.login_required
def word_cnt_by_year():
    # 接受参数year,month
    # 若month为空，返回年份year所有statements中词的统计
    # 若month不空，返回年份year月份month所有statements中词的统计
    year = request.args.get('year')
    month = request.args.get('month')
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December', '0']
    d = []
    if year is None:
        # 没有传入year,返回状态值2
        status = 2
    elif not year.isdigit():
        status = 2
    elif month not in months:
        status = 2
    else:
        # 判断month是否为空
        if month is None or (month.isdigit() and int(month) == 0):
            fd = News.query.filter(News.pub_year == year).all()
        else:
            fd = News.query.filter(News.pub_year == year, News.pub_month == month).all()
        # 判断数据是否为空
        if len(fd) == 0:
            # 没有找到数据，返回状态值1
            status = 1
        else:
            # 正常，返回状态值0
            status = 0
            s = [i.statement for i in fd]
            d = count_word(s)
    r = {'code': status, 'data': d}
    return jsonify(r)


@app.route("/wordcnt/party")
@auth.login_required
def wordcnt_by_party():
    party = request.args.get('party')
    year = request.args.get('year')
    if party is None or year is None or not check_year(year):
        return generate_result(2, [])
    if int(year) == 0:
        news = News.query.filter(func.lower(News.party) == party.lower()).all()
    else:
        news = News.query.filter(func.lower(News.party) == party.lower(), News.pub_year == year).all()
    statements = [n.statement for n in news]
    d = count_word(statements)
    return generate_result(0, d)


@app.route('/ch/year')
@auth.login_required
def credit_history_by_year():
    year1 = request.args.get('year1')
    year2 = request.args.get('year2')
    d = []
    if year1 is None:
        status = 2
    elif not year1.isdigit():
        status = 2
    elif year2 is None:
        fd = data[data['year'] == int(year1)]
        if fd.shape[0] == 0:
            status = 1
        else:
            status = 0
            ch = fd['label'].values.tolist()
            d = {year1: count_ch(ch)}
    elif not year2.isdigit():
        status = 2
    elif year1 > year2:
        status = 2
    else:
        status = 0
        for year in range(int(year1), int(year2) + 1):
            fd = data[data['year'] == year]
            if fd.shape[0] != 0:
                ch = fd['label'].values.tolist()
                c = {year: count_ch(ch)}
                d.append(c)
            else:
                ch = {"TrueCounts": 0, "mostlyTrueCounts": 0, "halfTrueCounts": 0,
                      "mostlyFalseCounts": 0, "FalseCounts": 0, "onFireCounts": 0}
                d.append({year: ch})
        if len(d) == 0:
            status = 1
    r = {'code': status, 'data': d}
    return jsonify(r)


@app.route('/ch/speaker')
@auth.login_required
def credit_history_by_speaker():
    sname = request.args.get('sname')
    year1 = request.args.get('year1')
    year2 = request.args.get('year2')
    d = []
    if sname is None:
        status = 2
    elif year1 is not None and not year1.isdigit():
        status = 2
    elif year2 is not None and not year2.isdigit():
        status = 2
    elif year1 is not None and year2 is not None and year1 > year2:
        status = 2
    elif year2 is None or (year2.isdigit() and int(year2) == 0):
        if year1 is None or (year1.isdigit and int(year1) == 0):
            fd = data[data['speaker'] == sname]
        else:
            fd = data[(data['speaker'] == sname) & (data['year'] == int(year1))]
        if fd.shape[0] == 0:
            status = 1
        else:
            status = 0
            ch = fd['label'].values.tolist()
            d = count_ch(ch)
    else:
        status = 0
        for year in range(int(year1), int(year2) + 1):
            fd = data[(data['speaker'] == sname) & (data['year'] == int(year))]
            if fd.shape[0] != 0:
                ch = fd['label'].values.tolist()
                c = {year: count_ch(ch)}
                d.append(c)
        if len(d) == 0:
            status = 1
    r = {'code': status, 'data': d}
    return jsonify(r)


@app.route("/h/ch/speaker")
@auth.login_required
def h_ch_by_speaker():
    speaker = request.args.get('speaker')
    year1 = request.args.get('year1')
    year2 = request.args.get('year2')
    if speaker is None or not check_year(year1) or not check_year(year2):
        return generate_result(2, [])
    speaker = speaker.lower()
    s = Speaker.query.filter(func.lower(Speaker.name) == speaker).first()

    if not s:
        return generate_result(1, [])
    # if year1 == 0 and year2 == 0, then return the all data
    if int(year1) == 0 and int(year2) == 0:
        year1 = "2000"
        year2 = "2999"

    if year1 > year2:
        return generate_result(2, [])
    news = News.query.filter(
        and_(func.lower(News.speaker) == speaker, year1 <= News.pub_year, News.pub_year <= year2)).all()
    if len(news) == 0:
        return generate_result(1, [])
    d = {
        "TrueCounts": 0,
        "mostlyTrueCounts": 0,
        "halfTrueCounts": 0,
        "mostlyFalseCounts": 0,
        "FalseCounts": 0,
        "onFireCounts": 0
    }
    for n in news:
        if n.label not in db2front:
            continue
        d[db2front[n.label]] += 1

    return generate_result(0, d)


# TODO: refactor this shit
@app.route("/h/wordcnt/speaker")
@auth.login_required
def h_wordcnt_by_speaker():
    speaker = request.args.get('speaker')
    year1 = request.args.get('year1')
    year2 = request.args.get('year2')
    if speaker is None or not check_year(year1) or not check_year(year2):
        return generate_result(2, [])
    speaker = speaker.lower()
    s = Speaker.query.filter(func.lower(Speaker.name) == speaker).first()

    if not s:
        return generate_result(1, [])
    # if year1 == 0 and year2 == 0, then return the all data
    if int(year1) == 0 and int(year2) == 0:
        year1 = "2000"
        year2 = "2999"

    if year1 > year2:
        return generate_result(2, [])
    news = News.query.filter(
        and_(func.lower(News.speaker) == speaker, year1 <= News.pub_year, News.pub_year <= year2)).all()
    if len(news) == 0:
        return generate_result(1, [])
    d = count_word([n.statement for n in news])

    return generate_result(0, d)


@app.route("/ch/party")
@auth.login_required
def ch_by_party():
    party = request.args.get('party').lower()
    year1 = request.args.get('year1')
    year2 = request.args.get('year2')
    if party is None or not check_year(year1) or not check_year(year2):
        return generate_result(2, [])

    s_party = Party.query.filter(func.lower(Party.name) == party).first()

    if not s_party:
        return generate_result(1, [])
    # if year1 == 0 and year2 == 0, then return the all data
    if year1 == 0 and year2 == 0:
        year1 = "2000"
        year2 = "2999"

    if year1 > year2:
        return generate_result(2, [])
    news = News.query.filter(
        and_(func.lower(News.party) == party, year1 <= News.pub_year, News.pub_year <= year2)).all()
    year1, year2 = int(year1), int(year2)

    d = {str(y): {"TrueCounts": 0,
                  "mostlyTrueCounts": 0,
                  "halfTrueCounts": 0,
                  "mostlyFalseCounts": 0,
                  "FalseCounts": 0,
                  "onFireCounts": 0}
         for y in range(year1, year2 + 1)}

    for n in news:
        if n.label not in db2front:
            continue
        d[n.pub_year][db2front[n.label]] += 1
    d = [{k: v} for k, v in d.items()]
    return generate_result(0, d)


@app.route('/ch/time')
@auth.login_required
def credit_history_by_time():
    from collections import defaultdict
    binary = request.args.get('binary')
    months = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7,
              'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
    t = []
    counts = ["TrueCounts", "mostlyTrueCounts", "halfTrueCounts",
              "mostlyFalseCounts", "FalseCounts", "onFireCounts"]
    c = defaultdict(list)
    years = data['year'].values.tolist()
    years = list(set(years))
    for year in range(min(years), max(years) + 1):
        for month in months.keys():
            fd = data[(data['year'] == year) & (data['month'] == month)]
            if fd.shape[0] != 0:
                t.append(str(year) + '/' + str(months[month]))
                ch = fd['label'].values.tolist()
                if binary == 'true':
                    ch = count_ch_binary(ch)
                    c['True'].append(ch['True'])
                    c['False'].append(ch['False'])
                else:
                    ch = count_ch(ch)
                    for label in counts:
                        c[label].append(ch[label])
    r = {'time': t, 'count': c}
    return jsonify(r)


@app.route('/speakers')
@auth.login_required
def all_speakers():
    from collections import defaultdict
    fd = Speaker.query.all()
    names = [i.name.strip() for i in fd]
    name_dict = defaultdict(list)
    for n in names:
        name_dict[n[0].upper()].append(n)
    sorted_names = sorted(name_dict.items(), key=lambda x: x[0])
    return jsonify(sorted_names)


@app.route('/party')
@auth.login_required
def all_party():
    from collections import defaultdict
    fd = Speaker.query.all()
    parties = [i.party for i in fd]
    parties = list(set(parties))
    party_dict = defaultdict(list)
    for p in parties:
        party_dict[p[0].upper()].append(p)
    sorted_party = sorted(party_dict.items(), key=lambda x: x[0])
    return jsonify(sorted_party)


@app.route("/all_parties")
@auth.login_required
def all_parties():
    parities = Party.query.all()
    parities = [i.name for i in parities]
    parities.sort()
    return generate_result(0, parities)


@app.route("/all_speakers")
@auth.login_required
def all_speakers_():
    s = Speaker.query.all()
    s = [i.name for i in s]
    s.sort()
    return generate_result(0, s)


@app.route('/ss')
def ss():
    all = Speaker.query.all()
    s = [i.name for i in all]
    return jsonify(s)


@app.route('/statement')
@auth.login_required
def statement():
    res = []
    a = News.query.all()
    for i in a:
        d = {'statement': i.statement, 'speaker': i.speaker, 'torf': i.label,
             'year': i.pub_year, 'month': i.pub_month}
        res.append(d)
    return jsonify(res)


@app.route('/news')
@auth.login_required
def s_news():
    mode = request.args.get('mode')
    wd = request.args.get('wd')
    page = request.args.get('page')
    number = request.args.get('num')
    if mode is None or not mode.isdigit():
        mode = 0
    if page is None or not page.isdigit():
        page = 1
    if number is None or not number.isdigit():
        number = 10
    count = News.query.all()
    start = 1 + (int(page) - 1) * int(number)
    end = int(number) + start
    if int(mode) == 0:
        a = News.query.filter(News.id.in_(range(start, end))).all()
    elif int(mode) == 1:
        a = News.query.filter(News.speaker.like(wd + '%') if wd is not None else "").all()
        a = a[start:end]
    elif int(mode) == 2:
        s = []
        sp = Speaker.query.filter(Speaker.party.like(wd + '%') if wd is not None else "").all()
        for i in sp:
            s.append(i.name)
        a = News.query.filter(News.speaker.in_(s)).order_by(News.id.asc()).all()
        a = a[start:end]
    else:
        a = News.query.filter(News.statement.like('%' + wd + '%') if wd is not None else "").all()
        a = a[start:end]
    if a is None:
        return jsonify({'code': 1, 'data': []})
    res = []
    for i in a:
        s = Speaker.query.filter(Speaker.name == i.speaker).first()
        if s is not None:
            p = s.party
        else:
            p = 'none'
        d = {'id': i.id, 'statement': i.statement, 'speaker': i.speaker, 'torf': i.label, 'party': p,
             'subject': i.subjects, 'year': i.pub_year, 'month': i.pub_month}
        res.append(d)
    r = {'code': 0, 'data': {'length': len(count), 'res': res}}
    return jsonify(r)


@app.route('/s')
@auth.login_required
def search():
    wd = request.args.get('wd')
    res = []
    n = News.query.filter(News.statement.like('%' + wd + '%') if wd is not None else "").order_by(News.id.asc()).limit(
        10).all()
    for i in n:
        res.append(i.statement)
        print(i.id)
    r = {'code': 0, 'data': res}
    return jsonify(r)


@app.route("/pred")
@auth.login_required
def get_prediction():
    try:
        news_id = int(request.args.get("id"))
    except Exception:
        return generate_result(2, [])
    news = News.query.get(news_id)
    if not news:
        return generate_result(2, [])
    res = []
    for m in ["rf", "lr", "adaboost", "bayes", "svm"]:
        pred = predict(m, config.DEFAULT_MODEL_MODE, news_id)
        res.append({"model": model_name_mapping[m], "pred": pred})
    return generate_result(0, res)


@app.route('/sim')
@auth.login_required
def similar_news():
    news_id = request.args.get("id")
    news_id = int(news_id)
    if not news_id:
        return generate_result(2, [])
    news = News.query.get(news_id)
    if not news:
        return generate_result(2, [])

    top_similar = get_similarities(news_id)
    res = []
    for sid, sc in top_similar:
        sn = News.query.get(sid)
        res.append({"id": sid, "sc": sc, "statement": sn.statement})
    return generate_result(0, res)


@app.route('/new')
@auth.login_required
def search_new():
    id = request.args.get('id')
    if id is None or not id.isdigit():
        return jsonify({'code': 2, 'data': []})
    i = News.query.filter(News.id == int(id)).first()
    if i is None:
        return jsonify({'code': 1, 'data': []})
    s = Speaker.query.filter(Speaker.name == i.speaker).first()
    if s is None:
        return jsonify({'code': 1, 'data': []})
    s.party = s.party.replace('none', 'independent')
    res = {'label': i.label, 'statement': i.statement, 'speaker': i.speaker,
           'partyAffiliation': s.party, 'barelyTrue': s.barely_true_cnt, 'false': s.false_cnt,
           'halfTrue': s.half_true_cnt, 'mostlyTrue': s.mostly_true_cnt, 'pantsOnFire': s.pants_fire_cnt}
    return jsonify({'code': 0, 'data': res})


# 分三个部分搜索, 分别返回 speaker,  party 和 statement 的搜索结果,限定返回结果为 20 条
@app.route("/search")
@auth.login_required
def full_search():
    keyword = request.args.get("keyword")
    fuzzy_keyword = "%" + keyword + "%"

    speakers = Speaker.query.filter(Speaker.name.like(fuzzy_keyword)).limit(SEARCH_SPEAKER_LIMITED)

    party = Party.query.filter(Party.name.like(fuzzy_keyword)).limit(SEARCH_PARTY_LIMITED)

    news = News.query.filter(News.statement.like(fuzzy_keyword)).limit(SEARCH_NEWS_LIMITED)

    speakers = [{"id": s.id, "name": s.name} for s in speakers]

    party = [{"id": p.id, "name": p.name} for p in party]

    news = [{"id": s.id, "statement": s.statement, "label": s.label, "speaker": s.speaker, "party": s.party} for s in
            news]
    return jsonify({"code": 0, "data": {"speaker": speakers, "party": party, "news": news}})


@app.route("/search/speaker")
@auth.login_required
def search_speakers():
    query = request.args.get("query")
    if query is None:
        return generate_result(2, [])
    fuzzy_query = "%" + query + "%"
    speakers = Speaker.query.filter(Speaker.name.like(fuzzy_query))
    speakers = [{"id": s.id, "name": s.name} for s in speakers]
    return generate_result(0, speakers)


@app.route("/speaker/cnt")
@auth.login_required
def speaker_cnt():
    cnt = Speaker.query.count()
    return generate_result(0, {"cnt": cnt})


@app.route("/party/cnt")
@auth.login_required
def party_cnt():
    cnt = Party.query.count()
    return generate_result(0, {"cnt": cnt})


@app.route("/model/supportedModel")
@auth.login_required
def supported_model():
    return generate_result(0, list(model_name_mapping.values()))


@app.route("/model/metrics")
@auth.login_required
def model_metrics():
    mode = int(request.args.get("mode"))
    if not 1 <= mode <= 5:
        return generate_result(2, [])
    met = Metrics.query.filter(Metrics.mode == mode).all()
    models = {k: [] for k in model_name_mapping.keys()}
    for m in met:
        models[m.model_name] = [m.accuracy, m.precision, m.recall, m.f1]
    res = {model_name_mapping[k]: v for k, v in models.items()}
    return generate_result(0, res)


@app.route("/model/train")
@auth.login_required
@admin_required()
def train_model():
    model_name = request.args.get("model_name")
    mode = request.args.get("mode")
    test_size = request.args.get("test_size")
    email = request.args.get("email")
    try:
        mode = int(mode)
        test_size = float(test_size)
    except Exception:
        return generate_result(2, [])

    if not 1 <= mode <= 5 or not 0 < test_size < 1:
        return generate_result(2, [])
    # 异步执行训练过程, 完成后邮件通知
    training_thread = threading.Thread(target=train_save_send_email, name="training thread",
                                       args=(reverse_model_name_mapping[model_name], mode, test_size, email))
    training_thread.start()
    return generate_result(0, {"status": "success"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
