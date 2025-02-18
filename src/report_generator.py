from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def create_pdf_report(entity: str, fields: str, result: dict, filename: str = "report.pdf"):

    try:
        # Prepare document and table data
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []
        
        # Extracting table headers and rows from the JSON data
        headers = fields.split(',')
        rows = []

        # Assuming the data comes in the form of 'accounts' > 'nodes'
        for account in result.get(entity, {}).get("nodes", []):
            row =[]
            for field in headers:
                row.append(account.get(field.strip(), ""))
            rows.append(row)

        # Create the table with headers and rows
        data = [headers] + rows
        table = Table(data)

        # Style the table
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header row background color
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Align text to center
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),  # Font style
            ('FONTSIZE', (0, 0), (-1, -1), 10),  # Font size
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Padding for header row
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Grid for table
        ])

        table.setStyle(style)
        elements.append(table)

        # Build the document (PDF generation)
        doc.build(elements)
        print(f"PDF report generated: {filename}")
        return filename
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None
