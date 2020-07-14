def when_ready(server):
    open('/tmp/app-initialized', 'w').close()


bind = '127.0.0.1:8000'
timeout = 90  # not necesssary