本项目创建的初衷是为了方便使用者只通过前端页面来进行各种格式的文档浏览。

### 支持格式

现在系统支持的文档格式如下：

- text/plain: 如txt/log文件等;
- text/html: 如html/shtml文件等;
- text/csv: csv文件;
- application/json: json文件;
- application/pdf: pdf文件;
- text/python: Python文件;
- image/*: 各种图片文件，比如jpg, png等;
- markdown文件

### 启动方法

1. 切换至pdfjs文件夹，运行搭建文件服务器命令:

```
python -m http.server 8081
```

或者:

```
python -m SimpleHTTPServer 8081
```

2. 运行`tornado_file_receiver.py`文件；
3. 在浏览中输入网址: http://localhost:8888/file ，上传相关文件

### 效果demo

#### text/plain: 如txt/log文件等
#### text/html: 如html/shtml文件等
#### text/csv: csv文件
#### application/json: json文件
#### application/pdf: pdf文件
#### text/python: Python文件
#### image/*: 各种图片文件，比如jpg, png等
#### markdown文件

### 后续改进措施

### 维护者

Jclian91, 微信公众号：Python爬虫与算法


