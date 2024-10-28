# ckops

运维平台，提供API接口？

## .env 文件

```bash
[root@localhost ckops]# cat .env
SECRET_KEY="248eaiamIPaddrce6e423ef6d7345fc"
FLASK_CONFIG="testing"
TOKEN_EXPIRATION=600
```

## 开发时，直接启动调试

```bash
(ckops-Zf7rOhxa) [root@localhost ckops]# python manage.py runserver -h iamIPaddr -p 8080
iamIPaddr iamIPaddriamIPaddr INFO manage-23::Running.
iamIPaddr iamIPaddriamIPaddr INFO manage-26::配置文件： testing
 * Serving Flask app "ops" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
iamIPaddr iamIPaddriamIPaddr INFO _internal-113:: * Running on http://iamIPaddr:8080/ (Press CTRL+C to quit)
```

## 创建镜像

```bash
[root@localhost ckops]# docker image pull python:3.9
[root@localhost ckops]# docker image tag python:3.9 harbor.betack.com/libs-hwcloud/python:3.9
[root@localhost ckops]# docker image push harbor.betack.com/libs-hwcloud/python:3.9

[root@localhost ckops]# cat Dockerfile
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
COPY .env ./
EXPOSE 5000
CMD /usr/local/bin/gunicorn -c /opt/betack/gunicorn_cnf.py manage:app

[root@localhost ckops]# docker image build -t harbor.betack.com/devops-tools/ck_ops:v1 .
[root@localhost ckops]# docker image push harbor.betack.com/devops-tools/ck_ops:v1
```

## 测试镜像

```bash
[root@localhost ckops]# docker run --name ck_ops -itd --restart=unless-stopped -p iamIPaddr:iamIPaddr harbor.betack.com/devops-tools/ck_ops:v1
75183eciamIPaddreaiamIPaddrba17bc0d5ae7cbiamIPaddrdaiamIPaddr
```

## 部署

> 注意，部署到正式环境的，记得修改.env文件的 FLASK_CONFIG="production"
> 然后重新打镜像？还是是挂载.env?

```bash
[root@localhost ckops]# cat deploy_script.sh
#!/usr/bin/env bash
# deploy_script.sh
# by colin on iamIPaddr
# revision on iamIPaddr
##################################
##脚本功能：
# 部署**运维API接口服务
#
##脚本说明：
#+ 用docker启动ck-ops API 接口服务

REGISTRY='harbor.betack.com'
IMG_TAG='v1'
CONTAINER_NAME='ck_ops'

# 删除旧有的部署
docker container rm -f $(docker container ls -q -f "name=${CONTAINER_NAME}")
# 新启动服务
docker run --name ${CONTAINER_NAME} -itd --restart=unless-stopped \
    -p iamIPaddr:iamIPaddr ${REGISTRY}/devops-tools/ck_ops:${IMG_TAG}
# 检查容器运行情况
sleep 10
docker container ls -q -f "name=${CONTAINER_NAME}"
docker container logs ${CONTAINER_NAME}

[root@localhost ckops]# sh deploy_script.sh
4cka68e52ece
73f4292beciamIPaddraiamIPaddrdcckiamIPaddrebc81ce87bbbiamIPaddr
73f4292bec63
[iamIPaddr 17:40:38 +0800] [7] [DEBUG] Current configuration:
  config: /opt/betack/gunicorn_cnf.py
  bind: ['iamIPaddr:5000']
......略
  strip_header_spaces: False
[iamIPaddr 17:40:38 +0800] [7] [INFO] Starting gunicorn 20.0.4
[iamIPaddr 17:40:38 +0800] [7] [DEBUG] Arbiter booted
[iamIPaddr 17:40:38 +0800] [7] [INFO] Listening at: http://iamIPaddr:5000 (7)
[iamIPaddr 17:40:38 +0800] [7] [INFO] Using worker: gevent
[iamIPaddr 17:40:38 +0800] [8] [INFO] Booting worker with pid: 8
[iamIPaddr 17:40:38 +0800] [9] [INFO] Booting worker with pid: 9
[iamIPaddr 17:40:38 +0800] [7] [DEBUG] 2 workers
iamIPaddr iamIPaddriamIPaddr INFO manage-23::Running.
iamIPaddr iamIPaddriamIPaddr INFO manage-23::Running.
iamIPaddr iamIPaddriamIPaddr INFO manage-26::配置文件： testing
iamIPaddr iamIPaddriamIPaddr INFO manage-26::配置文件： testing
```

## 验证 ck-ops API服务

admin: 123456

```bash
curl -L -X GET 'http://iamIPaddr:8080/auth/user/test' -u admin:123456
curl --location --request GET 'http://iamIPaddr:5000/api/v1.1/contact_list' -u admin:123456
curl --location --request GET 'http://iamIPaddr:5000/api/v1.1/contact_list' --header 'Authorization: Basic YWRtaW46MTIzNDU2'
curl --location --request GET 'http://iamIPaddr:5000/api/v1.1/token' -u admin:123456
curl --location --request GET 'http://iamIPaddr:5000/api/v1.1/token' --header 'Authorization: Basic YWRtaW46MTIzNDU2'

betack@ecs-diamIPaddr-1-171:ck_ops$ curl --location --request GET 'http://iamIPaddr:5000/api/v1.1/token' -u admin:123456
{"expiration":600,"token":"eyJhbGciOiJIUzUxMiIsImlhdCI6MTY1NDU5Njk1MywiZXhwIjoxNjU0NTk3NTUzfQ.eyJ1c2VybmFtZSI6ImFkbWluIn0.eLH0_Q9KbNcR-5d7-10AoAfmDLYRmGP9C5-Is8OKrgrEO_4sr1Z5dmQmcOqRoYaQpYu_fb0l4h7RMWDPkenPZQ"}

betack@ecs-diamIPaddr-1-171:ck_ops$ curl -L -X GET 'http://iamIPaddr:5000/auth/user/test'
{"error":"Unauthorized"}
betack@ecs-diamIPaddr-1-171:ck_ops$ curl -L -X GET 'http://iamIPaddr:5000/auth/user/test' -H 'Authorization: Bearer eyJhbGciOiJIUzUxMiIsImlhdCI6MTY1NDU5Njk1MywiZXhwIjoxNjU0NTk3NTUzfQ.eyJ1c2VybmFtZSI6ImFkbWluIn0.eLH0_Q9KbNcR-5d7-10AoAfmDLYRmGP9C5-Is8OKrgrEO_4sr1Z5dmQmcOqRoYaQpYu_fb0l4h7RMWDPkenPZQ'
{"data":"123"}

(ckops-Zf7rOhxa) [root@localhost alarm]# curl -i -X GET 'http://iamIPaddr:5000/auth/user/test' -u admin:iampassword
HTTP/iamIPaddr OK
Server: gunicorn/20.0.4
Date: Tue, 07 Jun iamIPaddr:17 GMT
Connection: keep-alive
Content-Type: application/json
Content-Length: 15

{"data":"123"}

```
