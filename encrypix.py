from flask import Flask, request, render_template, send_file
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def xor_crypt(image_path, key):
    with open(image_path, 'rb') as fin:
        image = bytearray(fin.read())
    
    key_bytes = bytearray(key, 'utf-8')
    key_length = len(key_bytes)
    
    for index, value in enumerate(image):
        image[index] = value ^ key_bytes[index % key_length]
    
    with open(image_path, 'wb') as fin:
        fin.write(image)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    if 'image' not in request.files or request.form['key'] == '':
        return 'No image or key provided', 400
    
    file = request.files['image']
    key = request.form['key']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    
    xor_crypt(file_path, key)
    
    return send_file(file_path, as_attachment=True)

@app.route('/decrypt', methods=['POST'])
def decrypt():
    if 'image' not in request.files or request.form['key'] == '':
        return 'No image or key provided', 400
    
    file = request.files['image']
    key = request.form['key']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    
    xor_crypt(file_path, key)
    
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=False,host='0.0.0.0')
