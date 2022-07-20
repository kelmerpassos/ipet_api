FROM python:3.10.5-slim 

WORKDIR /ipet

COPY requirements.txt requirements-dev.txt ./

RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt

COPY . .

EXPOSE 5000

CMD ["flask", "run", "--port=5000", "--host=0.0.0.0"]