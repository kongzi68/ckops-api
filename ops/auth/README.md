
## 初始管理员账号admin

初始创建admin的时候，可以如下

```python
@auth.route('/user/regist', methods=['POST'])
## 把下面这句注释掉，注册用户就不会要求登录授权，admin用户注册成功之后，再启用 login_required
# @multi_auth.login_required
def user_regist():
......
    return json_msg(200, '注册成功', {'user': username})
```

注册用户

```bash
http://iamIPaddr:8080/auth/user/regist?username=admin&password=123456

[root@localhost ckops]# curl -i -L -X POST 'http://iamIPaddr:8080/auth/user/regist?username=admin&password=123456' -u admin:123456
HTTP/iamIPaddr OK
Content-Type: application/json
Content-Length: 76
Server: Werkzeug/1.0.1 Python/3.9.9
Date: Tue, 07 Jun iamIPaddr:07 GMT

{
  "msg": "\u8be5\u7528\u6237\u5df2\u7ecf\u6ce8\u518c",  # 该用户已经注册
  "status": 200
}
```

## 接口说明

### 接口测试

```bash
## 接口
/auth/user/test

## 方法
GET

## 参数

## 示例
[root@localhost ckops]# curl -L -X GET 'http://iamIPaddr:8080/auth/user/test' -u admin:123456
{
  "data": "123"
}
```

### 管理用户注册

功能：用户注册

```bash
## 接口
/auth/user/regist

## 方法
POST

## 参数
username=admin
password=123456

## 示例
http://iamIPaddr:8080/auth/user/regist?username=admin&password=123456
curl -i -L -X POST 'http://iamIPaddr:8080/auth/user/regist?username=colin&password=123456' -u admin:123456

[root@localhost ckops]# curl -i -L -X POST 'http://iamIPaddr:8080/auth/user/regist?username=colin&password=123456' -u admin:123456
HTTP/iamIPaddr OK
Content-Type: application/json
Content-Length: 96
Server: Werkzeug/1.0.1 Python/3.9.9
Date: Tue, 07 Jun iamIPaddr:15 GMT

{
  "data": {
    "user": "colin"
  },
  "msg": "\u6ce8\u518c\u6210\u529f",
  "status": 200
}
```

### 设置管理用户状态

功能：修改用户状态

```bash
## 接口
/auth/user/change_user_status

## 方法
POST

## 参数
username=admin
is_valid=True

## 示例
#+ 禁用用户
[root@localhost ckops]# curl -X POST 'http://iamIPaddr:8080/auth/user/change_user_status?username=colin&is_valid=False' -u admin:123456
{
  "msg": "\u505c\u7528\u7528\u6237",
  "status": 200
}
```

### 修改管理用户密码

功能：修改密码

```bash
## 接口
/user/change_password

## 方法
POST

## 参数
username=admin
password=123456

## 示例
[root@localhost ckops]# curl -X POST 'http://iamIPaddr:8080/auth/user/change_password?username=colin&password=0HIqo2acvh' -u admin:123456
{
  "msg": "\u4fee\u6539\u5bc6\u7801\u6210\u529f",
  "status": 200
}
```

管理员用户表

```sql
mysql> select * from users;
+----+----------+------------------------------------------------------------------------------------------------+--------+----------+---------------------+---------------------+------------+
| id | username | password                                                                                       | status | is_valid | created_at          | updateed_at         | last_login |
+----+----------+------------------------------------------------------------------------------------------------+--------+----------+---------------------+---------------------+------------+
|  1 | admin    | pbkdf2:shaiamIPaddr$vFNSMvFv$482aaa322ea4a5cfeiamIPaddrciamIPaddrbiamIPaddrfbbiamIPaddrfeb | NULL   |        1 | iamIPaddr 12:16:57 | NULL                | NULL       |
|  2 | colin    | pbkdf2:shaiamIPaddr$iFPY5SBD$iamIPaddrcd5ceaaiamIPaddrc8b6eciamIPaddrbiamIPaddrbiamIPaddr | NULL   |        0 | iamIPaddr 12:48:16 | iamIPaddr 12:52:00 | NULL       |
+----+----------+------------------------------------------------------------------------------------------------+--------+----------+---------------------+---------------------+------------+
2 rows in set (0.00 sec)
```

