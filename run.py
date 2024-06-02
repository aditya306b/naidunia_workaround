from flask import Flask, render_template, request, jsonify, send_file, abort
import requests
from bs4 import BeautifulSoup
import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import time
from gevent.pywsgi import WSGIServer
import logging as log


app = Flask(__name__)


def download_image(url, filename):
  """Downloads an image from the specified URL and saves it with the given filename."""
  try:
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
            
        log.debug(f"Image downloaded: {filename}")
    else:
      log.error(f"Failed to download image: {url} - Status code: {response.status_code}")
  except Exception as e:
    log.error(f"Error downloading image: {url} - {e}")

def scrape_images(output_dir, date, day, city_id):
    all_file = []
    response = ""
    images = []
    no = 2
    try: 
        # URL = f"https://epaper.naidunia.com/epaper/{date}-{day}-2024-74-indore-edition-indore-page-{no}.html"
        INDORE_URL = f"https://epaper.naidunia.com/epaper/{date}-{day}-2024-74-indore-edition-indore-page-{no}.html"
        KHANDWA_URL = f"https://epaper.naidunia.com/epaper/{date}-{day}-2024-8-khandwa-edition-khandwa-page-{no}.html"
        response = requests.get( INDORE_URL if city_id == "74" else KHANDWA_URL if city_id=="8" else False)
        if response:
            soup = BeautifulSoup(response.content, 'html.parser')
            images = soup.find_all('img', attrs={'data-src': True})
            os.makedirs(output_dir, exist_ok=True)
            log.debug(f"Image downloaded: {images}")

        else:
            raise Exception("Unable to generate presentation!")
        
    except Exception as err:
        log.error(f"PAGE NO - {no} | NOT FOUND")
        log.error(err)

    for image in images:
        image_url = image.get('data-src')
        filename = os.path.join(output_dir, os.path.basename(image_url))
        if re.match(r"^(?!.*ss\.png)(?=.*m-).*\.png$", filename):            
            download_image(image_url, filename)
            all_file.append(filename)
    return all_file


def convert_images_to_pdf(image_paths, pdf_path):
    print(image_paths)
    try:
        c = canvas.Canvas(pdf_path, pagesize=letter)
        for image_path in image_paths:
            img_width, img_height = 1671 , 2730
            c.setPageSize((img_width, img_height))
            c.drawImage(image_path, 0, 0, img_width, img_height)
            c.showPage()
            os.remove(image_path)

        c.save()
        return True
    except Exception as err:
        raise err



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    date = data.get('date')
    month = data.get('month')
    city = data.get('city')
    city_id = data.get('cityId') 
    
    response = {
        'date': date,
        'month': month,
        'city': city,
        'cityId': city_id,
        'message': f'You have selected: {date} {month}, {city} (ID: {city_id})'
    }

 
    try:
        output_dir = 'scraped_images'
        all_path = scrape_images(output_dir, date, month.lower(), city_id)
        res = convert_images_to_pdf(all_path, "output/output.pdf") if all_path else False
        if res :
            return jsonify(response) 
        else:
            raise Exception("Unable to extract")
        
    except FileNotFoundError:
        abort(404)


@app.route('/download-pdf', methods=['GET'])
def download_pdf():
    try:
        # Replace 'static/example.pdf' with the path to your PDF file
        return send_file('output/output.pdf', 
                         download_name='output.pdf', 
                         as_attachment=True)
    except FileNotFoundError:
        abort(404)

if __name__ == '__main__':
    from gunicorn.app.base import Application

    def run():
        config = {  # Optional configuration from gunicorn_config.py (if used)
            'bind': "0.0.0.0:5000",
            'workers': 1,
            'timeout': 180,
        }

        app = Application(**config)
        app.wsgi_app = app.app.wsgi_app  # Set WSGI app for Gunicorn
        app.run()

    run()