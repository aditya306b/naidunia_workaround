FROM python

WORKDIR /app
COPY . .

RUN pip install -r ./requirements.txt

EXPOSE 5000

CMD ["gunicorn", "run:app", '--bind', "0.0.0.0:5000", '--timeout 900']
