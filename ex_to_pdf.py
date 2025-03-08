import win32com.client
import os

def excel_to_pdf(excel_path, pdf_path=None):
    """
    Convert Excel file to PDF
    
    Args:
        excel_path (str): Path to the Excel file
        pdf_path (str): Optional path for the PDF output. If not provided,
                       will use the same name as Excel file with .pdf extension
    """
    # If pdf_path not provided, create one from excel_path
    if pdf_path is None:
        pdf_path = os.path.splitext(excel_path)[0] + '.pdf'
    
    # Create absolute paths
    excel_path = os.path.abspath(excel_path)
    pdf_path = os.path.abspath(pdf_path)
    
    # Initialize Excel application
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = False
    
    try:
        # Open the Excel file
        wb = excel.Workbooks.Open(excel_path)
        
        # Specify PDF format
        xlTypePDF = 0
        
        # Set print area and formatting if needed
        ws = wb.Worksheets[0]  # First worksheet
        ws.PageSetup.Zoom = False  # Don't zoom
        ws.PageSetup.FitToPagesTall = 1  # Fit to 1 page tall
        ws.PageSetup.FitToPagesWide = 1  # Fit to 1 page wide
        
        # Export as PDF
        wb.ExportAsFixedFormat(xlTypePDF, pdf_path)
        
    except Exception as e:
        print(f"Error converting Excel to PDF: {str(e)}")
        
    finally:
        # Close and clean up
        wb.Close(False)
        excel.Quit()

if __name__ == "__main__":
    # Example usage
    excel_file = "demo.xlsx"
    pdf_file = "c:\\Downloads\demoPdf.pdf"  # Optional
    
    excel_to_pdf(excel_file, pdf_file)