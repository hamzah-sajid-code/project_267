import os
import cv2
import numpy as np
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from PIL import Image, ImageOps

app = Flask(__name__)

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join('static/', filename))

        image = Image.open(file).convert("RGB")
        image_flip = ImageOps.mirror(image)
        flip_filename = 'flip.jpg'
        flip_filepath = os.path.join('static/', flip_filename)
        image_flip.save(flip_filepath)
        
        return render_template('upload.html', filename=flip_filename)
@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename=filename))

if __name__ == "__main__":
    app.run()
