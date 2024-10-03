FROM python:latest

COPY server.py server.py

COPY 1.json 1.json

COPY 2.json 2.json

EXPOSE 67/udp

ENTRYPOINT ["python", "server.py"]
