from flask import Flask, request, jsonify
from pyresparser import ResumeParser
import tempfile
import os

app = Flask(__name__)

@app.route('/parse', methods=['POST'])
def parse_resume():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    
    # Save file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        file.save(tmp.name)
        try:
            data = ResumeParser(tmp.name).get_extracted_data()
        except Exception as e:
            return jsonify({'error': str(e)})
        finally:
            os.unlink(tmp.name)

    return jsonify(data or {})
