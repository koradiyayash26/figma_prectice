import pandas as pd
import os
from win32com.client import Dispatch

def excel_to_pdf(excel_path):
    try:
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

# Example usage
if __name__ == "__main__":
    # Replace this with your Excel file path
    excel_file = r"C:\Users\yashk\Downloads\Standard_9_Sem3_Cards_20250313.xlsx"
    excel_to_pdf(excel_file)
