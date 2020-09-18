from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config.from_object('config')
db = SQLAlchemy(app)


def read_statement():
    # 读取新闻的数据
    csv = pd.read_csv('liar_dataset/liar_dataset/statement.csv', sep=',', header=None, index_col=False,
                      names=['label', 'statement', 'speaker', 'year', 'month', 'url'])
    return csv


def read_speakerinfo():
    # 读取人物的数据
    csv = pd.read_csv('liar_dataset/liar_dataset/speaker.csv', sep=',', header=None, index_col=False,
                      names=['speaker', 'party', 'stateInfo'])
    return csv

def read_news():
    # 读取人物的数据
    csv = pd.read_csv('liar_dataset/liar_dataset/news.csv', sep=',', header=None, index_col=False,
                      names=['label', 'statement', 'speaker','partyAffiliation', 'barelyTrue',
                             'false' ,'halfTrue', 'mostlyTrue','pantsOnFire'])
    return csv

data = read_statement()
data_s = read_speakerinfo()
datas = read_news()
