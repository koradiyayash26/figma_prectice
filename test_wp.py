import win32com.client

def excel_to_pdf(input_path, output_path):
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = False  # Run Excel in the background
    workbook = excel.Workbooks.Open(input_path)
    
    # Save as PDF
    workbook.ExportAsFixedFormat(0, output_path)
    
    workbook.Close()
    excel.Quit()

# Convert Excel to PDF
excel_to_pdf('demo.xlsx', 'demo.pdf')
