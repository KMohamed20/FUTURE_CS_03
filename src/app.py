"""
app.py
Serveur Flask pour le partage sécurisé de fichiers
"""

from flask import Flask, request, send_file, render_template_string
import os
from encrypt_decrypt import encrypt_file, decrypt_file

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML = '''
<h2>🔐 Secure File Sharing</h2>
<form method="POST" enctype="multipart/form-data">
  <input type="file" name="file" required><br><br>
  <input type="password" name="password" placeholder="Encryption Password" required><br><br>
  <input type="submit" value="Upload & Encrypt">
</form>
<hr>
<a href="/download">📁 Download File</a>
'''

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        password = request.form['password']
        data = file.read()
        encrypted = encrypt_file(data, password)
        path = os.path.join(UPLOAD_FOLDER, "encrypted.bin")
        with open(path, 'wb') as f:
            f.write(encrypted)
        return "<h2>✅ File uploaded and encrypted!</h2><br><a href='/'>🔙 Upload another</a>"
    return HTML

@app.route('/download')
def download():
    path = os.path.join(UPLOAD_FOLDER, "encrypted.bin")
    if not os.path.exists(path):
        return "No file available", 404
    return '''
    <h2>🔓 Download File</h2>
    <form method="POST">
      <input type="password" name="password" placeholder="Enter password" required><br><br>
      <input type="submit" value="Decrypt & Download">
    </form>
    <br><a href="/">🔙 Upload another</a>
    '''

@app.route('/download', methods=['POST'])
def decrypt_and_send():
    path = os.path.join(UPLOAD_FOLDER, "encrypted.bin")
    password = request.form['password']
    try:
        with open(path, 'rb') as f:
            data = f.read()
        decrypted = decrypt_file(data, password)
        temp_path = "/tmp/decrypted_file"
        with open(temp_path, 'wb') as f:
            f.write(decrypted)
        os.remove(path)  # Supprimer après téléchargement
        return send_file(temp_path, as_attachment=True, download_name="secure_file.dat")
    except Exception as e:
        return f"❌ Decryption failed: {str(e)}", 400

if __name__ == '__main__':
    app.run(port=5000)
