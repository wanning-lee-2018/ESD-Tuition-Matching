FROM python:3-slim
WORKDIR /usr/src/app
COPY amqp.reqs.txt http.reqs.txt ./
RUN pip install --no-cache-dir -r amqp.reqs.txt -r http.reqs.txt
COPY ./notification.py  ./amqp_setup.py ./
CMD [ "python", "./notification.py" ]