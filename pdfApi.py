import pandas as pd
import os
from win32com.client import Dispatch
import pythoncom
from flask import Flask, request, render_template, send_file
import tempfile
from werkzeug.utils import secure_filename

def excel_to_pdf(excel_path):
    try:
        # Initialize COM for this thread
        pythoncom.CoInitialize()
        
        # Get the directory and filename from the Excel path
        directory = os.path.dirname(excel_path)
        filename = os.path.splitext(os.path.basename(excel_path))[0]
        pdf_path = os.path.join(directory, f"{filename}.pdf")

        # Create Excel application object
        excel = Dispatch("Excel.Application")
        excel.Visible = False

        # Open the Excel file
        workbook = excel.Workbooks.Open(excel_path)
        
        # Save as PDF
        workbook.ExportAsFixedFormat(0, pdf_path)
        
        # Close workbook and Excel application
        workbook.Close()
        excel.Quit()
        
        print(f"Successfully converted {filename}.xlsx to PDF!")
        print(f"PDF saved at: {pdf_path}")
        return True
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False
    finally:
        # Clean up COM resources
        pythoncom.CoUninitialize()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return "No file part", 400
    
    file = request.files['file']
    
    if file.filename == '':
        return "No file selected", 400
    
    if not file.filename.endswith('.xlsx') and not file.filename.endswith('.xls'):
        return "Please upload an Excel file (.xlsx or .xls)", 400
    
    # Save the uploaded file to a temporary location
    filename = secure_filename(file.filename)
    excel_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(excel_path)
    
    # Get the PDF path (same directory but with .pdf extension)
    pdf_filename = os.path.splitext(filename)[0] + '.pdf'
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
    
    # Convert Excel to PDF
    success = excel_to_pdf(excel_path)
    
    if success:
        # Return the PDF file for download - using attachment_filename instead of download_name
        return send_file(pdf_path, 
                        as_attachment=True, 
                        attachment_filename=pdf_filename,
                        mimetype='application/pdf')
    else:
        return "Error converting to PDF", 500

if __name__ == '__main__':
    app.run(debug=True)
