from models import News
from models import Speaker
from models import Party
from settings import db


def clean_speaker():
    speakers = Speaker.query.all()
    for s in speakers:
        s.name = s.name.replace("\n", "")
        # if s.party == "none" or not s.party or s.party == "None" or s.party == "independent":
        #     s.party = "Independent"
    db.session.commit()


def add_party_to_news():
    news = News.query.all()
    ss = set()
    cnt = 0
    for n in news:
        speaker = Speaker.query.filter(Speaker.name == n.speaker).first()
        if not speaker:
            print(n.speaker)
            ss.add(n.speaker)
            cnt += 1
            continue
        n.party = speaker.party
    print(cnt, len(ss))
    db.session.commit()


def init_party_table():
    speakers = Speaker.query.all()
    party = set([s.party for s in speakers])
    for p in party:
        _p = Party()
        _p.name = p
        db.session.add(_p)
    db.session.commit()


def strip_speaker():
    news = News.query.all()
    for n in news:
        n.speaker = n.speaker.strip()
    speakers = Speaker.query.all()
    for s in speakers:
        s.name = s.name.strip()
    db.session.commit()


def clean_state():
    speakers = Speaker.query.all()
    for s in speakers:
        if not s.state or s.state.lower() == "none":
            s.state = "unknown"
    db.session.commit()


if __name__ == '__main__':
    # add_party_to_news()
    # init_party_table()
    clean_state()
