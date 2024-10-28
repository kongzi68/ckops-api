# 非 Bearer Token 方式
## 用账号与密码访问API接口
```shell script
[centos@centos7-shell-scripts ~]$ curl -u admin:123456 -i -X GET http://iamIPaddr:8080/api/v1.0/token
HTTP/iamIPaddr OK
Content-Type: application/json
Content-Length: 205
Server: Werkzeug/1.0.1 Python/3.6.10
Date: Fri, 12 Jun iamIPaddr:09 GMT

{
  "expiration": 600, 
  "token": "eyJhbGciOiJIUzUxMiIsImlhdCI6MTU5MTk3MDEwOSwiZXhwIjoxNTkxOTcwNzA5fQ.eyJpZCI6MX0.j85FexG1qvKaZ3MwfEThiAXUpRr4taE3LGNOgusgdKw2V7JoP3fohUf6-77NWU_GlkjaZ1YH9C_67ov0dTqRFA"
}
[centos@centos7-shell-scripts ~]$ curl -u admin:123456 -i -X GET http://iamIPaddr:8080/api/v1.0/contact_list
HTTP/iamIPaddr OK
Content-Type: application/json
Content-Length: 350
Server: Werkzeug/1.0.1 Python/3.6.10
Date: Fri, 12 Jun iamIPaddr:16 GMT

[
  {
    "email": "email@betack.com", 
    "en_name": "colin", 
    "name": "\u5b54\u5c0f\u6797", 
    "phone": iamIPaddr
  }, 
  {
    "email": "test123@qq.com", 
    "en_name": "zhangsan", 
    "name": "\u5f20\u4e09", 
    "phone": iamIPaddr
  }, 
  {
    "email": "", 
    "en_name": "lisi", 
    "name": "\u674e\u56db", 
    "phone": 0
  }
]

```
## 用token访问接口
```shell script
# 先用账号与密码获取token
[centos@centos7-shell-scripts ~]$ curl -u admin:123456 -i -X GET http://iamIPaddr:8080/api/v1.0/token
HTTP/iamIPaddr OK
Content-Type: application/json
Content-Length: 205
Server: Werkzeug/1.0.1 Python/3.6.10
Date: Fri, 12 Jun iamIPaddr:16 GMT

{
  "expiration": 600, 
  "token": "eyJhbGciOiJIUzUxMiIsImlhdCI6MTU5MTk3MDE3NiwiZXhwIjoxNTkxOTcwNzc2fQ.eyJpZCI6MX0.HjSZJ1BCdW_uYO6hk3XxspaW3mcaZ8HcFSZ07DD88SyVKAAqFIlJa_HkZ1W7hSybTNUVwB9o8frLF3mJUfRIJQ"
}
# 用token调用其它接口
[centos@centos7-shell-scripts ~]$ curl -u eyJhbGciOiJIUzUxMiIsImlhdCI6MTU5MTk3MDE3NiwiZXhwIjoxNTkxOTcwNzc2fQ.eyJpZCI6MX0.HjSZJ1BCdW_uYO6hk3XxspaW3mcaZ8HcFSZ07DD88SyVKAAqFIlJa_HkZ1W7hSybTNUVwB9o8frLF3mJUfRIJQ:admin -i -X GET http://iamIPaddr:8080/api/v1.0/contact_list
HTTP/iamIPaddr OK
Content-Type: application/json
Content-Length: 350
Server: Werkzeug/1.0.1 Python/3.6.10
Date: Fri, 12 Jun iamIPaddr:47 GMT

[
  {
    "email": "email@betack.com", 
    "en_name": "colin", 
    "name": "\u5b54\u5c0f\u6797", 
    "phone": iamIPaddr
  }, 
  {
    "email": "test123@qq.com", 
    "en_name": "zhangsan", 
    "name": "\u5f20\u4e09", 
    "phone": iamIPaddr
  }, 
  {
    "email": "", 
    "en_name": "lisi", 
    "name": "\u674e\u56db", 
    "phone": 0
  }
]
```
