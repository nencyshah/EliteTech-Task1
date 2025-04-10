from fpdf import FPDF

class MyPDF(FPDF):
    def header(self):
        try:
            self.image('nency.png', 10, 15, 33)
        except FileNotFoundError:
            print("Warning: 'nency.png' not found. Skipping logo.")
        self.cell(80)
        self.set_font('helvetica', 'B', 20)
        self.cell(30, 50, 'My PDF Header', border=1, ln=1, align='C')
        self.ln(50)


# Instantiate MyPDF (not FPDF)
pdf = MyPDF()
pdf.add_page()

# Set font
pdf.set_font("helvetica", size=12)





# Generate multiple lines
for i in range(41):
    pdf.cell(0, 10, 'This is line %d' % (i + 1), new_x="LMARGIN", new_y="NEXT")

# Enable auto page break
pdf.set_auto_page_break(auto=True, margin=15)

# Add another page
pdf.add_page()
pdf.set_fill_color(255, 255, 255)

# Save PDF
pdf.output("hello_world.pdf")

print("PDF generated successfully! Open 'hello_world.pdf' to see the output.")
