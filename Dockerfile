FROM tiangolo/uvicorn-gunicorn:python3.11

WORKDIR /

COPY ./iserv.py /iserv.py
COPY ./server.py /server.py

EXPOSE 80

RUN pip install fastapi
RUN pip install requests

CMD [ "uvicorn", "server:app", "--reload", "--port", "80", "--host", "0.0.0.0", "--log-level", "critical" ]