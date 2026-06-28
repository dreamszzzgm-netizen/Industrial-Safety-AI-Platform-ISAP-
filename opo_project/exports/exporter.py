import os
import subprocess
import uuid
from docxtpl import DocxTemplate

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'word_templates')
DOCX_OUT = os.path.join(BASE_DIR, 'generated', 'docx')
PDF_OUT = os.path.join(BASE_DIR, 'generated', 'pdf')


class ExportEngine:

    @staticmethod
    def build_context(data: dict) -> dict:
        """
        Превращает JSON из формы в контекст для docxtpl.
        data — это то, что отправляет HTML-форма.
        """
        # --- Раздел 1 ---
        ctx = {
            'opo_name':           data.get('f1_1', ''),
            'object_type':        data.get('f1_2', ''),
            'industry_code':      data.get('f1_3', ''),
            'address':            data.get('f1_4', ''),
            'oktmo':              data.get('f1_5', ''),
            'commissioning_date': data.get('f1_6', ''),
            'owner_name':         data.get('f1_7_1', ''),
            'owner_inn':          data.get('f1_7_2', ''),

            # --- Разделы 2–5 (собираются на клиенте как текст) ---
            'processes_text':      data.get('processes_text', ''),
            'danger_class':        data.get('danger_class', ''),
            'classification_text': data.get('classification_text', ''),
            'licenses_text':       data.get('licenses_text', ''),

            # --- Раздел 6 — таблица ---
            # Ожидается список: [{ number, name, danger, substance, characteristics, processes }]
            'composition': data.get('composition', []),
            'total_amount': data.get('totalAmount', '0'),

            # --- Раздел 7 ---
            'nearby_substances': data.get('f7', ''),

            # --- Раздел 8 ---
            'applicant_full':      data.get('f8_1_1', ''),
            'applicant_short':     data.get('f8_1_2', ''),
            'applicant_inn':       data.get('f8_1_3', ''),
            'applicant_ogrn':      data.get('f8_1_4', ''),
            'applicant_post':      data.get('f8_1_5', ''),
            'applicant_fio':       data.get('f8_1_6', ''),
            'applicant_address':   data.get('f8_1_7', ''),
            'applicant_sign_date': data.get('f8_1_9', ''),

            # --- Раздел 9 ---
            'reg_number':    data.get('f9_1', ''),
            'temp_number':   data.get('f9_2', ''),
            'reg_date':      data.get('f9_3', ''),
            'change_date':   data.get('f9_4', ''),
            'reg_org':       data.get('f9_5', ''),
            'auth_post':     data.get('f9_6', ''),
            'auth_fio':      data.get('f9_7', ''),
            'auth_sign_date': data.get('f9_10', ''),

            # --- Подпись ---
            'sign_dolj': data.get('signDolj', ''),
            'sign_date': data.get('signDate', ''),
            'sign_mp':   data.get('signMp', ''),
        }
        return ctx

    @staticmethod
    def export_docx(template_name: str, context: dict) -> str:
        tpl_path = os.path.join(TEMPLATES_DIR, template_name)
        doc = DocxTemplate(tpl_path)
        doc.render(context)
        out_name = f"opo_{uuid.uuid4().hex[:8]}.docx"
        out_path = os.path.join(DOCX_OUT, out_name)
        os.makedirs(DOCX_OUT, exist_ok=True)
        doc.save(out_path)
        return out_path

    @staticmethod
    def export_pdf(template_name: str, context: dict) -> str:
        # Сначала генерируем DOCX, потом конвертируем через LibreOffice
        docx_path = ExportEngine.export_docx(template_name, context)
        os.makedirs(PDF_OUT, exist_ok=True)
        subprocess.run([
            'libreoffice', '--headless', '--convert-to', 'pdf',
            '--outdir', PDF_OUT, docx_path
        ], check=True)
        pdf_name = os.path.splitext(os.path.basename(docx_path))[0] + '.pdf'
        return os.path.join(PDF_OUT, pdf_name)
