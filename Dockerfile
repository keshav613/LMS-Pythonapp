# FROM alpine:latest

# RUN apk add --no-cache python3-dev
# RUN apk add py3-pip
# RUN pip3 install --upgrade pip

# WORKDIR /LMSapp
# COPY . /LMSapp/

# RUN pip3 --no-cache-dir install -r requirements.txt

# EXPOSE 80

# ENTRYPOINT [ "python3" ]
# CMD [ "app.py" ]


FROM python:3.8-alpine
RUN pip install --upgrade pip
WORKDIR /LMSapp
COPY . /LMSapp/

RUN pip --no-cache-dir install -r requirements.txt

EXPOSE 80

ENTRYPOINT [ "python" ]
CMD [ "app.py" ]