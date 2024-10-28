from gunicorn import glogging


class CustomGunicornLogger(glogging.Logger):
    def access(self, resp, req, environ, request_time):
        # disable healthcheck logging
        if req.path in ["/api/v1.1/checkstatus/"]:
            return
        super().access(resp, req, environ, request_time)


logger_class = CustomGunicornLogger

pythonpath = '/usr/bin/python3'
chdir = '/opt/betack'
bind = 'iamIPaddr:5000'
workers = 2
backlog = 2048
worker_class = "gevent"
debug = True
reload = True
proc_name = 'gunicorn_ck_ops.proc'
pidfile = '/tmp/gunicorn_ck_ops.pid'
# accesslog = '/var/log/gunicorn/access.log'
# errorlog = '/var/log/gunicorn/error.log'
loglevel = 'debug'
