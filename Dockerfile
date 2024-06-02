FROM python

WORKDIR /app
COPY . .

RUN pip install -r ./requirements.txt

EXPOSE 5000

CMD ["gunicorn", "run:app"]
