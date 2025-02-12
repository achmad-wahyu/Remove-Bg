from flask import Flask, request, render_template, send_file
from rembg import remove
from PIL import Image
import io
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Pastikan folder upload ada
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['image']
        if file:
            # Simpan file yang diunggah
            input_image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(input_image_path)

            # Hapus latar belakang
            input_image = Image.open(input_image_path)
            output_image = remove(input_image)

            # Simpan gambar yang telah diproses dalam format PNG
            output_image_path = os.path.join(app.config['UPLOAD_FOLDER'], f'remo_{file.filename}.png')
            output_image.save(output_image_path, format='PNG')  # Pastikan formatnya PNG

            return render_template('index.html', original_image=file.filename, modified_image=f'remo_{file.filename}.png')
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)