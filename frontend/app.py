import sys
import os
from flask import Flask, render_template, request, redirect, url_for
from PIL import Image

# Add the eval directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../eval')))

import eval_AesA1
import eval_AesA2
import eval_AesA3

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            return redirect(request.url)
        
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            return render_template('assess.html', filename=file.filename)
    
    return render_template('index.html')

@app.route('/assess', methods=['POST'])
def assess_image():
    filename = request.form.get('filename')
    method = request.form.get('method')
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Load the image for assessment (if needed)
    image = Image.open(filepath)

    # Perform the selected assessment
    if method == 'AesA1':
        result = eval_AesA1.assess(image)
    elif method == 'AesA2':
        result = eval_AesA2.assess(image)
    elif method == 'AesA3':
        result = eval_AesA3.assess(image)
    else:
        result = "Invalid method selected."

    return render_template('result.html', filename=filename, result=result)

if __name__ == '__main__':
    app.run(debug=True)