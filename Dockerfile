FROM python:3.10-slim-buster

WORKDIR /flask_app
COPY ./ /flask_app

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["flask", "--app", "main.py", "run"]