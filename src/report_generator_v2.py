# def flatten_record(record, sep='.'):
#     """
#     Iteratively flattens nested dictionaries for better performance.
#     """
#     stack = [((), record)]
#     flat_dict = {}

#     while stack:
#         path, current = stack.pop()
#         if isinstance(current, dict):
#             for k, v in current.items():
#                 stack.append((path + (k,), v))
#         else:
#             flat_key = sep.join(path)
#             flat_dict[flat_key] = current

#     return flat_dict

from reportlab.lib import colors
from reportlab.lib.pagesizes import A3
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from io import BytesIO
import json

def flatten_record(record, parent_key='', sep='.'):
    """
    Recursively flattens nested dictionaries.
    """
    items = []
    for k, v in record.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_record(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def generate_pdf_report(graphql_query: str, json_result: dict):
    """
    Generates a PDF report from a GraphQL query and its JSON result.
    :param graphql_query: The GraphQL query used to fetch data
    :param json_result: The JSON response from the GraphQL API
    """
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=A3)
    elements = []
    styles = getSampleStyleSheet()
    
    # Add GraphQL Query to the PDF
    # elements.append(Paragraph("GraphQL Query:", styles['Heading2']))
    # elements.append(Paragraph(f"<pre>{graphql_query}</pre>", styles['Normal']))
    
    # Extracting table data dynamically
    data_key = list(json_result.keys())[0]  
    
    # Assuming first key contains relevant data
    records = json_result.get(data_key, {}).get("nodes", [])
    
    if not records or not isinstance(records, list):
        elements.append(Paragraph("No data available.", styles['Normal']))
    else:
        # Flatten records and extract headers
        flattened_records = [flatten_record(record) for record in records]
        headers = list(flattened_records[0].keys()) if flattened_records else []
        
        table_data = [headers]  # Table header row
        
        # Extract row values
        for record in flattened_records:
            table_data.append([str(record.get(col, '')) for col in headers])
                
        # Create table with styling
        table = Table(table_data, colWidths=None)
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        table.setStyle(style)
        elements.append(table)
    
    # Build PDF
    doc.build(elements)
    pdf_buffer.seek(0)  # Reset buffer position
    
    print(f"PDF report generated")
    return pdf_buffer