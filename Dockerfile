FROM python:3.10.4

WORKDIR /moonsuit

COPY . .


RUN pip3 install -r req.txt
RUN python3 manage.py collectstatic

EXPOSE 8080

CMD ["uvicorn", "moonsuit.asgi:application", "--port", "8080", "--host", "0.0.0.0", "--workers", "4"]