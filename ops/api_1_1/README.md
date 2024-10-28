# Bearer Token

## 接口

认证方式支持：账号与密码，Bearer Token两种方式。

```shell script
## 用 POSTMAN，获取 Authorization: Basic 代码如下：
#+ Authorization Type类型选择为 Basic Auth
#+ Username 设置用户名；Password 设置密码；点击 send
#+ 然后点击右侧 code，可以查看到本次调试请求的源代码
#+ 获得的源代码如下：
curl --location --request GET 'http://iamIPaddr:5000/auth/user/test' \
--header 'Authorization: Basic YWRtaW46MTIzNDU2'

## 用这种方式获取到token
curl --location --request GET 'http://iamIPaddr:5000/api/v1.1/token' \
--header 'Authorization: Basic YWRtaW46MTIzNDU2'
#+ 返回结果如下：
{
    "expiration": 600,
    "token": "eyJhbGciOiJIUzUxMiIsImlhdCI6MTY1NDU5MTg3NywiZXhwIjoxNjU0NTkyNDc3fQ.eyJ1c2VybmFtZSI6ImFkbWluIn0._jRWDwd6PJ3cIjDJo1LD_l2BZbIg8igZrmDTxvNeZEZxaL8F8H3sobia7iYc2efrR5WLbUSvPBeizWNzT6IF3w"
}

## 然后就可以用token获取其它信息了
curl --location --request GET 'http://iamIPaddr:5000/api/v1.1/contact_list' \
--header 'Authorization: Bearer eyJhbGciOiJIUzUxMiIsImlhdCI6MTY1NDU5MTg3NywiZXhwIjoxNjU0NTkyNDc3fQ.eyJ1c2VybmFtZSI6ImFkbWluIn0._jRWDwd6PJ3cIjDJo1LD_l2BZbIg8igZrmDTxvNeZEZxaL8F8H3sobia7iYc2efrR5WLbUSvPBeizWNzT6IF3w'
#+ 返回结果如下：
[
    {
        "email": "colin@betack.com",
        "en_name": "colin",
        "name": "孔小林",
        "phone": iamIPaddr
    }
]

################################
# 获取token
[root@centos7-shell-scripts hxkj_ops]# curl -L -X GET 'http://iamIPaddr:8080/api/v1.1/token' -H 'Authorization: Basic YWRtaW46MTIzNDU2'
{
  "expiration": 600, 
  "token": "eyJhbGciOiJIUzUxMiIsImlhdCI6MTU5MjE4OTc0OSwiZXhwIjoxNTkyMTkwMzQ5fQ.eyJ1c2VybmFtZSI6ImFkbWluIn0.D2wSgerOvvV00yIpA1XHiRrLMForgt_UUarZwufiA2kG2MwBijw-UzolpA4qzefLmfhVFT3Jfb5Ehh68ALgyAQ"
}
[root@centos7-shell-scripts hxkj_ops]# curl -L -X GET 'http://iamIPaddr:8080/api/v1.1/token' -u admin:123456
{
  "expiration": 600, 
  "token": "eyJhbGciOiJIUzUxMiIsImlhdCI6MTU5MjE4OTc2OSwiZXhwIjoxNTkyMTkwMzY5fQ.eyJ1c2VybmFtZSI6ImFkbWluIn0.7ND_jQZWC5Qp2-lsgJ4CXakntgk8EDB9h_02YALIQM4ulM7p-Y0nZtO6tAZ6oJl73EruCOSMEVmsY9jYpluboQ"
}
# 获取通讯录
[root@centos7-shell-scripts hxkj_ops]# curl -L -X GET 'http://iamIPaddr:8080/api/v1.1/contact_list' -H 'Authorization: Bearer eyJhbGciOiJIUzUxMiIsImlhdCI6MTU5MjE4OTc2OSwiZXhwIjoxNTkyMTkwMzY5fQ.eyJ1c2VybmFtZSI6ImFkbWluIn0.7ND_jQZWC5Qp2-lsgJ4CXakntgk8EDB9h_02YALIQM4ulM7p-Y0nZtO6tAZ6oJl73EruCOSMEVmsY9jYpluboQ'
[
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

### 获取token

```bash
curl --location --request GET 'http://iamIPaddr:8080/api/v1.1/token' \
--header 'Authorization: Basic YWRtaW46MTIzNDU2'
```

### 拨打电话

```bash
curl --location --request POST 'http://iamIPaddr:8080/api/v1.1/call_phone?callee_nbr=iamIPaddr&send_txt=拨打电话测试数据' \
--header 'Authorization: Basic YWRtaW46MTIzNDU2'

curl --location --request POST 'http://iamIPaddr:8080/api/v1.1/call_phone' \
--header 'Authorization: Basic YWRtaW46MTIzNDU2' \
--form 'callee_nbr="iamIPaddr"' \
--form 'send_txt="电话通知告警信息"'
```



















| 接口| 方法|参数 | 说明 |
|------------|-----------|-----------|------------|
|`/api/v1.1/checkstatus/`|get|无|负载均衡健康检查|
|`/api/v1.1/token`|get|无|获取token|
|`/api/v1.1/contact_list`|get|无|用于发短信或邮件的通讯录|






