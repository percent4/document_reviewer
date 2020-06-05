# -*- coding: utf-8 -*-
import os
import logging
import traceback
import tornado.ioloop
import tornado.web
from tornado import options

from parse_file import *


# 文档上传与解析
class UploadFileHandler(tornado.web.RequestHandler):
    # get函数
    def get(self):
        self.render('upload.html')

    def post(self):
        # 文件的存放路径
        upload_path = os.path.join(os.path.dirname(__file__), 'pdfjs/web/files')
        # 提取表单中‘name’为‘file’的文件元数据
        # 暂时只支持单文档的上传
        file_meta = self.request.files['file'][0]
        filename = file_meta['filename']
        # 保存文件
        with open(os.path.join(upload_path, filename), 'wb') as up:
            up.write(file_meta['body'])

        text = file_meta["body"]

        # 解析文件的内容
        mtype = file_meta["content_type"]
        logging.info('POST "%s" "%s" %d bytes', filename, mtype, len(text))
        if mtype in ["text/x-python", "text/x-python-script"]:
            self.write(parse_python(str(text, encoding="utf-8")))
        elif mtype in ["text/plain", "text/csv"]:
            self.write(parse_text_plain(str(text, encoding="utf-8")))
        elif mtype == "text/html":
            self.write(str(text, encoding="utf-8"))
        elif mtype.startswith("image"):
            self.write(parse_image(mtype, text))
        elif mtype == "application/json":
            self.write(parse_application_json(str(text, encoding="utf-8")))
        elif mtype == "application/pdf":
            self.redirect("http://127.0.0.1:8081/web/viewer.html?file=files/%s" % filename)
        elif mtype == "application/octet-stream" and filename.endswith(".md"):
            self.render("markdown.html", md_content=r"%s" % str(text, encoding="utf-8").replace("\n", "newline"))
        else:   # 其余文件格式
            try:
                self.write(str(text, encoding="utf-8").replace("\n", "<br>"))
            except Exception:
                logging.error(traceback.format_exc())
                self.write('<font color=red>系统不支持的文件解析格式！</font>')


def make_app():
    return tornado.web.Application([(r"/file", UploadFileHandler)],
                                    template_path=os.path.join(os.path.dirname(__file__), "templates"))  # 模板路径


if __name__ == "__main__":
    # Tornado configures logging.
    options.parse_command_line()
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()