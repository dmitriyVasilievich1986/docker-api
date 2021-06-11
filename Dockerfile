FROM python:3.9

LABEL author="dmitriyvasil@gmail.com"

ENV HOST="0.0.0.0"
ENV PORT=8000

ENV KNOX_AUTH_HOST=http://auth:8000/auth/accounts/
ENV DB_PASSWORD=root
ENV DB_USER=postgres
ENV DB_DBNAME=astra
ENV DB_PORT=5432
ENV DEBUG=False
ENV DB_HOST=db

RUN mkdir /app
WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt

CMD python -u start_server.py