# 使用官方Python镜像作为基础
FROM python:3.8

# 设置工作目录
WORKDIR /app

# 复制项目代码到容器内的工作目录
COPY . /app/

# 安装项目依赖
RUN pip install -r requirements.txt

# 暴露Django应用的端口（根据你的Django设置来配置）
EXPOSE 8000

# 启动Django应用
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

