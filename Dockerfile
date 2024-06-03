FROM python

WORKDIR /app
COPY . .


EXPOSE 5000
RUN python -m venv /opt/venv

# Install dependencies:
COPY requirements.txt .
RUN /opt/venv/bin/pip install -r requirements.txt

# Run the application:
COPY run.py .
CMD ["gunicorn", "run:app", '--bind', "0.0.0.0:5000", '--timeout',  '900']
