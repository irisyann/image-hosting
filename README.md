# Flask File Upload
This is a Flask application for image upload. The application provides a simple web interface to upload images and generates a permanent link for the images. It also accepts images in a zip file for bulk upload.

## Requirements
- Flask
- Werkzeug

## Installation
`pip install Flask`

## Usage
1. Clone the repository.
`git clone https://github.com/irisyann/image-hosting.git`

2. Run the Flask development server.
`python app.py`

3. Open your web browser and go to http://localhost:5000.

## Endpoints
- `/`: This is the home page that displays a file upload form.
- `/result`: This is the endpoint for file upload. The endpoint accepts file uploads and returns the contents of the uploaded file.

## Tests
The application comes with a set of tests to verify its functionality. To run the tests, execute the following command in the project directory:
`python -m unittest test_app`
