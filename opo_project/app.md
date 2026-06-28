from flask import Flask, request, send_file, jsonify
from exports.exporter import ExportEngine
import os

app = Flask(__name__)

@app.route('/')
def index():
    return app.send_static_file('index.html')  # ваша HTML-форма

@app.route('/export/docx', methods=['POST'])
def export_docx():
    data = request.get_json(force=True)
    context = ExportEngine.build_context(data)
    path = ExportEngine.export_docx('opo_template.docx', context)
    return send_file(path, as_attachment=True, download_name='Сведения_об_ОПО.docx')

@app.route('/export/pdf', methods=['POST'])
def export_pdf():
    data = request.get_json(force=True)
    context = ExportEngine.build_context(data)
    path = ExportEngine.export_pdf('opo_template.docx', context)
    return send_file(path, as_attachment=True, download_name='Сведения_об_ОПО.pdf')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

