from flask import jsonify

import yagmail


def check_year(year: str) -> bool:
    try:
        year = int(year)
    except Exception:
        return False
    if 2000 <= year <= 2999 or year == 0:
        return True
    return False


def generate_result(code, data):
    return jsonify({"code": code, "data": data})


db2front = {
    "Mostly True": "mostlyTrueCounts",
    "Pants on Fire!": "onFireCounts",
    "True": "TrueCounts",
    "Half-True": "halfTrueCounts",
    "False": "FalseCounts",
    "Mostly False": "mostlyFalseCounts"
}


def trans_label(label):
    pass


def send_email(address):
    yag = yagmail.SMTP(user='hanhao0125@163.com', password='haon130518', host='smtp.163.com')
    yag.send(to=address, subject='[FakeNewsVis]训练完成提醒',
             contents='您提交的训练任务已完成')


if __name__ == '__main__':
    send_email("")
