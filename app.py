import os
from urllib.parse import urlparse

from dotenv import load_dotenv
from flask import Flask
from flask import render_template, request

from create_cloud import create_cloud

app = Flask(__name__, static_folder='static')


@app.route('/', methods=['POST', 'GET'])
def get_link():
    if request.method == 'POST':
        link = request.form['link']
        disassembled_url = urlparse(link)
        group_id = os.path.basename(disassembled_url.path)
        create_cloud(group_id)
        return render_template('template.html', image_name=f'images/{group_id}.png')

    return render_template('template.html')


if __name__ == '__main__':
    load_dotenv()
    app.run(debug=True)
