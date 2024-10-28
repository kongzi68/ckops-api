FROM harbor.betack.com/libs-hwcloud/python:3.9
LABEL maintainer="colin" version="1.0" datetime="iamIPaddr"
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone && \
    pip install --no-cache-dir --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
WORKDIR /opt/betack
COPY requirements.txt ./
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
COPY ops ./ops
COPY *.py ./
## 正式环境通过挂载，替换该文件？
#COPY .env ./
EXPOSE 5000
## 不能用[]这种形式，会报错 /bin/sh: 1: [/usr/local/bin/gunicorn,: not found
#CMD ['/usr/local/bin/gunicorn', '-c', '/opt/betack/gunicorn_cnf.py', 'manage:app']
#+ 正确如下：
CMD /usr/local/bin/gunicorn -c /opt/betack/gunicorn_cnf.py manage:app
