from Scraper.reviews import generate_data

from Model.sentiment import generate_sentiment

# data = generate_data('https://www.amazon.in/Bassbuds-Duo-Headphones-Water-Resistant-Assistance/dp/B09DD9SX9Z/ref=sr_1_1?_encoding=UTF8&_ref=dlx_gate_sd_dcl_tlt_04410e8d_dt&content-id=amzn1.sym.9e4ae409-2145-4395-aa6e-45d7f3e95c3e&pd_rd_r=81b7691e-3f71-41a4-bf8e-549b314a692e&pd_rd_w=D8FkQ&pd_rd_wg=5AAru&pf_rd_p=9e4ae409-2145-4395-aa6e-45d7f3e95c3e&pf_rd_r=KSHN3MBQKSQWTSEM51MT&qid=1684171691&sr=8-1')


import os
from flask import Flask, jsonify, request, send_file, send_from_directory

app = Flask(__name__)
app.use_x_sendfile = True
app.config['UPLOAD_FOLDER'] = "./"

@app.route('/images', methods=['GET'])
def get_images():
    images = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename.endswith('.png') and os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
            images.append(filename)
    return {'images': images}


@app.route('/uploads')
def download_file():
    filename = request.json['filename']
    return send_from_directory("../",filename)


@app.route('/sentiment', methods=['POST'])
def get_sentiment():
    url = request.json['url']

    generate_data(url)
    
    return jsonify(generate_sentiment())


if __name__ == '__main__':

    app.run(port=5010)
