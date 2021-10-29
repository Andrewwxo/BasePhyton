FROM python:3.9-buster

WORKDIR /var/app

COPY /requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY shop .

EXPOSE 8000
# hint to forward the port

CMD uvicorn app:app --host=0.0.0.0


