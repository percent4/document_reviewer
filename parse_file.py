# -*- coding: utf-8 -*-
# author: Jclian91
# place: Pudong Shanghai
# time: 2020/6/5 1:05 下午
# filename: parse_file.py
# 用于解析各种文件类型的数据
import json
import base64
import logging
import traceback
from json import JSONDecodeError


# 解析text/plain或者text/csv文件格式
def parse_text_plain(text):
    return "<html><head></head><body>%s</body></html>" % text.replace("\n", "<br>")


# 解析application/json文件格式
def parse_application_json(text):
    try:
        data_dict = json.loads(text)
        return json.dumps(data_dict, ensure_ascii=False, indent=2).replace("\n", "<br>").replace(" ", "&nbsp;")
    except JSONDecodeError:
        try:
            data_list = [json.loads(_) for _ in text.split("\n") if _]
            return json.dumps(data_list, ensure_ascii=False, indent=2).replace("\n", "<br>").replace(" ", "&nbsp;")
        except JSONDecodeError:
            logging.error(traceback.format_exc())
            return "JSON文件格式解析错误"
        except Exception as err:
            logging.error(traceback.format_exc())
            return "未知错误: %s" % err


# 解析image/*文件格式
def parse_image(mtype, text):
    return '<html><head></head><body><img src="data:%s;base64,%s"></body></html>' % \
           (mtype, str(base64.b64encode(text), "utf-8"))


# 解析Python文件
def parse_python(text):
    # indent和换行
    text = text.replace("\n", "<br>").replace(" ", "&nbsp;").replace("\t", "&nbsp;" * 4)

    # 关键字配色
    color_list = ["gray", "red", "green", "blue", "orange", "purple", "pink", "brown", "wheat", "seagreen", "orchid", "olive"]
    key_words = ["self", "from", "import", "def", ":", "return", "open", "class", "try", "except", '"', "print"]
    for word, color in zip(key_words, color_list):
        text = text.replace(word, '<font color=%s>%s</font>' % (color, word))

    colors = ["peru"] * 7
    punctuations = list("[](){}#")
    for punctuation, color in zip(punctuations, colors):
        text = text.replace(punctuation, '<font color=%s>%s</font>' % (color, punctuation))

    html = "<html><head></head><body>%s</body></html>" % text

    return html