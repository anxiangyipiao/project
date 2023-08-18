import os
from celery import Celery

'''Beat：定时地将任务发往消息队列；
Worke：实时监视消息队列获取队列中的任务执行(可以一个或多个)；
Broker：消息代理，又称消息中间件。就是生产者和消费者存放/拿取产品的地方(消费队列)。Celery目前支持RabbitMQ、Redis、MongoDB、Beanstalk、SQLAlchemy、Zookeeper等作为消息代理，官方推荐 RabbitMQ。
Result Backend：任务处理完后保存状态信息和结果，以供查询。

'''
# 专属于myproject项目的任务


 # 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WebBacked.settings')
 
 # 实例化
app = Celery('app')
 
 # namespace='CELERY'作用是允许你在Django配置文件中对Celery进行配置
 # 但所有Celery配置项必须以CELERY开头，防止冲突
app.config_from_object('django.conf:settings', namespace='CELERY')
 
 # 自动从Django的已注册app中发现任务
app.autodiscover_tasks()
 
 # 一个测试任务
@app.task(bind=True)
def debug_task(self):
     print(f'Request: {self.request!r}')