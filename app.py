import os
import sys
from flask import Flask, request, send_file, abort, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-this-in-production'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

HARDCODED_FILES = {
    'kanban.md': './TODO.md',
    'archive.md': './archive.md',
}

@app.route('/')
def index():
    return send_file("index.html", "text/html")

@app.route('/upload/<filename>', methods=['POST'])
def upload_file(filename):
    if filename not in HARDCODED_FILES:
        abort(404)
    data = dict(request.form)
    if 'file' not in data:
        return 'No file part', 400

    file = data['file']
    if file:
        filepath = HARDCODED_FILES[filename]
        with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
            f.write(file.replace('\r\n', '\n'))
        return jsonify({'message': f'File uploaded successfully: {filename}' }), 200
    return 'file not submitted', 400

@app.route('/download/<filename>')
def download_file(filename):
    # Security: Only allow downloading from the hardcoded list
    if filename not in HARDCODED_FILES:
        abort(404)
    file_path = HARDCODED_FILES[filename]
    if not os.path.isfile(file_path):
        abort(404)
    # Ensure the resolved path is what we expect (defense in depth)
    real_path = os.path.realpath(file_path)
    if not os.path.isfile(real_path):
        abort(404)

    return send_file(real_path, as_attachment=True, download_name=filename)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        HARDCODED_FILES['kanban.md'] = sys.argv[1]
    app.run(debug=False, host='0.0.0.0', port=5000)
