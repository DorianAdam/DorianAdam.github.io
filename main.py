from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
from deepface import DeepFace
import praw
import cv2
import requests
import urllib.request
import numpy as np
 
app = Flask(__name__)
 
UPLOAD_FOLDER = 'static/files/'
 
app.secret_key = "TheDecoder" #Don't Show
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     

@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(filename)
        image = cv2.imread('static/files/' + filename)

        similarity = 0
        post = None

        client_id = 'Jo3aKCn4HbZUHufXZeDr0Q' # Don't show
        client_secret = 'yARx6A3x4SULO82EPzD4PY2QxnWBwQ' #Don't show
        user_agent = 'RoastApi' #Don't show
        username = "IhaveNoClue232" #Don't show
        password = "doriandorian27" #Don't show

        reddit = praw.Reddit(client_id = client_id, client_secret = client_secret, user_agent = user_agent, username = username, password = password)
        subred = reddit.subreddit("RoastMe").new(limit = 10)

        loops = 0

        for i in subred:
            if(i.thumbnail != 'nsfw'):
                req = urllib.request.urlopen(i.thumbnail)
                arr = np.array(bytearray(req.read()), dtype=np.uint8)
                curr_img = cv2.imdecode(arr, -1)

                curr_sim = DeepFace.verify(image, curr_img, enforce_detection = False)['distance']

                if curr_sim > similarity :
                    similarity = curr_sim
                    post = i

        one = None
        two = None
        three = None

        if post.comments[0].ups > post.comments[1].ups:
            one = post.comments[0].body
            two = post.comments[1].body
            three = post.comments[2].body
        else:
            one = post.comments[1].body
            two = post.comments[2].body
            three = post.comments[3].body
        flash(one)
        flash(two)
        flash(three)
        return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png and jpg')
        return redirect(request.url)
 
@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='files/' + filename), code=301)
 
if __name__ == "__main__":
    app.run()