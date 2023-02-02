from flask import Flask, render_template, request, url_for, send_from_directory, redirect
from werkzeug.utils import secure_filename
from distutils.log import debug
import os
import zipfile
from time import time 

app = Flask(__name__, template_folder='templates', static_folder='uploads')  

# Flask application configuration to specify where to save uploaded files
app.config["UPLOAD_FOLDER"] = "uploads"

@app.route('/', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('index.html')

    elif request.method == 'POST':
        file = request.files['file']
        filename = generate_filename(secure_filename(file.filename))

        # if file is uploaded
        if file:
            
            # if the file is a zip file
            if filename.endswith('.zip'):
                file.save(os.path.join('uploads', filename))
                unzipped_files_folder = filename[:-4]

                with zipfile.ZipFile(os.path.join('uploads', filename), 'r') as zip_ref:
                    zip_ref.extractall(os.path.join('uploads', unzipped_files_folder))            

                # get all the images in the folder directory that are image files
                images = [img for img in os.listdir(os.path.join('uploads', unzipped_files_folder)) if valid_file(img)]

                urls = []
                for image in images:
                    file_url = url_for('static', filename = unzipped_files_folder + '/' + image)
                    urls.append(file_url)
                    
                return render_template('success.html', images=images, urls=urls)

            # if file is image
            elif valid_file(file.filename):
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                file_url = url_for('static', filename=filename)
                return render_template('success.html', single_file_url = file_url)

        # if no file was uploaded
        elif not file:
            return render_template('index.html', error_message = 'Please upload a valid image file or valid zip file.')
        
        # if invalid file was uploaded
        else:
            return render_template('index.html', error_message = 'Please upload a valid image file or valid zip file.')


# function to ensure that the filename is unique
def generate_filename(filename):
    return str(int(time())) + "_" + filename

# function to check that uploaded file is an image by its extension
def valid_file(filename):
    VALID_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # splits extension from filename, extracts it, converts to lowercase and and check if it is in the set of valid extensions
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in VALID_EXTENSIONS

# function to display the image to the browser when URL of file is requested
@app.route('/uploads/<filename>')
def serve_image(filename):
    return send_from_directory('uploads', filename)

if __name__ == '__main__':
   app.run(debug = True)