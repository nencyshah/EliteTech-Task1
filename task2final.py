import pandas as pd
from fpdf import FPDF

# Load Data from CSV
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

# Analyze Data (Handles both numeric & text)
def analyze_data(df):
    summary = df.describe(include="all")  # Include all data types
    return summary.fillna("N/A")  # Replace NaN with "N/A"

# PDF Report Class
class PDFReport(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 16)
        self.cell(0, 10, "Data Analysis Report", new_x="LMARGIN", new_y="NEXT", align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 10)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

# Generate PDF from Analysis
def generate_pdf(summary, output_path):
    pdf = PDFReport()
    pdf.add_page()
    
    pdf.set_font("helvetica", size=12)

    # Add Table Headers
    pdf.cell(0, 10, "Summary Statistics", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)

    # Process Each Column
    for col in summary.columns:
        pdf.set_font("helvetica", "B", 12)
        pdf.cell(0, 10, f"Column: {col}", new_x="LMARGIN", new_y="NEXT", align="L")
        pdf.set_font("helvetica", size=11)

        # Process Each Statistic
        for stat in summary.index:
            value = summary[col][stat]
            
            # Format Numeric Values
            if isinstance(value, (int, float)):
                formatted_value = f"{value:.2f}"
            else:
                formatted_value = str(value)  # Convert text-based stats to string
            
            pdf.cell(0, 10, f"{stat}: {formatted_value}", new_x="LMARGIN", new_y="NEXT", align="L")

        pdf.ln(5)  # Space between columns
    
    # Save PDF
    pdf.output(output_path)
    print(f"✅ PDF Report saved as: {output_path}")

# Main Execution
if __name__ == "__main__":
    file_path = "data.csv"  # Change this to your CSV file name
    output_pdf = "Data_Report.pdf"

    df = load_data(file_path)
    if df is not None:
        summary = analyze_data(df)
        generate_pdf(summary, output_pdf)
