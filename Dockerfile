FROM python:3.10.4

WORKDIR /remoter

COPY . .

RUN pip3 install -r req.txt
RUN python3 manage.py collectstatic
# RUN python3 manage.py makemigrations app api
# RUN python3 manage.py migrate

EXPOSE 8080

CMD ["uvicorn", "websocket.asgi:application", "--port", "8080", "--host", "0.0.0.0", "--workers", "4"]