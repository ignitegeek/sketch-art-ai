from flask import Flask, render_template, request, redirect, url_for
from utils.sketch_converter import convert_to_sketch
import os
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['RESULT_FOLDER'] = 'static/results/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

# Admin switch: Toggle paid/free mode
IS_PAID_MODE = False

@app.route('/')
def index():
    return render_template('index.html', is_paid=IS_PAID_MODE)

@app.route('/upload', methods=['POST'])
def upload():
    global IS_PAID_MODE
    if 'photo' not in request.files:
        return "No file uploaded"
    file = request.files['photo']
    if file.filename == '':
        return "No selected file"

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"img_{timestamp}.jpg"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    result_path = convert_to_sketch(filepath, app.config['RESULT_FOLDER'])

    return render_template('result.html', 
                           original=url_for('static', filename='uploads/' + filename),
                           result=url_for('static', filename='results/' + os.path.basename(result_path)),
                           is_paid=IS_PAID_MODE)

@app.route('/admin/toggle')
def toggle_mode():
    global IS_PAID_MODE
    IS_PAID_MODE = not IS_PAID_MODE
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
