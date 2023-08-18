
# app/tasks.py, 可以复用的task
from celery import shared_task
import time

'''用celery定义任务时，避免在一个任务中调用另一个异步任务，容易造成阻塞。
当我们使用@app.task装饰器定义我们的异步任务时，那么这个任务依赖于根据项目名myproject生成的Celery实例。
然而我们在进行Django开发时为了保证每个app的可重用性，我们经常会在每个app文件夹下编写异步任务，这些任务并不依赖于具体的Django项目名。
使用@shared_task装饰器能让我们避免对某个项目名对应Celery实例的依赖，使app的可移植性更强。'''

# 异步调用任务
# Celery提供了2种以异步方式调用任务的方法，delay和apply_async方法
'''# 方法一：delay方法
 task_name.delay(args1, args2, kwargs=value_1, kwargs2=value_2)
 ​
 # 方法二： apply_async方法，与delay类似，但支持更多参数
 task.apply_async(args=[arg1, arg2], kwargs={key:value, key:value})'''


@shared_task
def add(x, y):
     time.sleep(5)
     return x + y