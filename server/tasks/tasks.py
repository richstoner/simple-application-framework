from celery import Celery

c = Celery('tasks', backend='amqp', broker='amqp://')

@c.task
def add(x, y):
    print 'hello task'
    return x + y