FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

# Adjust the time
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

# Copy files to target file.
COPY ./ /app

# Install library
RUN pip3 install -r requirements.txt
