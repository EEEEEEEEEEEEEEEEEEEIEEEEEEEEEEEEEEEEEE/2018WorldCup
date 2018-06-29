### 在Linux上部署
#### 首先需要Python3.X，以Ubuntu为例，系统已经自带Python所以无需安装。
#### 然后把项目上传到服务器，在Windows上需要下载XFTP.
#### Linux下上传用scp
```
 $ scp -r username@host:服务器目录 本机项目目录
```
#### 接下来创建虚拟环境。
```
 $ pip install virtualenv
```
```
 $ virtualenv venv
```
```
 $ source venv/bin/activate
```
```
 $ pip install -r requirements.txt
```
```
# $ pip install gunicorn
```
```
 $ gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

#### 打开绑定的域名:8000即可访问。
