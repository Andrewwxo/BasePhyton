FROM python:3.9-buster

WORKDIR /var/app

COPY homework/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY homework .

EXPOSE 5000   #hint to forward the port

CMD uvicorn app:app --host=0.0.0.0