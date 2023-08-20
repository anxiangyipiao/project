# 使用官方Python镜像作为基础
FROM python:3.8

# 设置工作目录
WORKDIR /app

# 将 Dockerfile 同级目录下的所有文件和文件夹复制到容器内的 /app 目录中。
COPY . /app/

# 安装项目依赖
RUN pip install  -r requirements.txt 

# 暴露Django应用的端口（根据你的Django设置来配置）
EXPOSE 8000

# 启动Django应用
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]



#docker exec -it webbacked-web-1 python manage.py migrate

#pip freeze > requirements.txt
#create database dbase default charset utf8 collate utf8_general_ci;

