FROM python:latest

COPY *.py ./

EXPOSE 67/udp

ENTRYPOINT ["python", "main.py"]
