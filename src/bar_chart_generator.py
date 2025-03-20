from io import BytesIO
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

def plot_bar_chart(json_data : dict, x_label, y_label, title):
    # Extracting table data dynamically
    data_key = list(json_data.keys())[0]

    # Assuming first key contains relevant data
    records = json_data.get(data_key, {}).get("nodes", [])
    
    # Extract x-axis and y-axis values
    x_axis_values = [record[x_label] for record in records]
    y_axis_values = [record[y_label] for record in records]
    
    # Create bar chart
    plt.figure(figsize=(8, 5))
    plt.bar(x_axis_values, y_axis_values, color='skyblue')
    
    # Labels and title
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    
    # Rotate x-axis labels for better visibility
    plt.xticks(rotation=45)
    
    # Save to PDF buffer
    pdf_buffer = BytesIO()
    with PdfPages(pdf_buffer) as pdf:
        pdf.savefig()  # Save the current figure
        plt.close()  # Close the figure to free memory
    
    pdf_buffer.seek(0)
    return pdf_buffer
