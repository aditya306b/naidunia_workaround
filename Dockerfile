FROM python

WORKDIR /app
COPY . .

RUN pip install -r ./requirements.txt

EXPOSE 4700

CMD ["python", "run.py"]
