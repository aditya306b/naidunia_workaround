FROM python

WORKDIR /app
COPY . .


EXPOSE 5000
RUN python -m venv news_venv
RUN source news_venv/bin/activate
RUN pip install -r ./requirements.txt
CMD ["gunicorn", "run:app", '--bind', "0.0.0.0:5000", '--timeout',  '900']
