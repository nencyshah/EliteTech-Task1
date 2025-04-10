from fpdf import FPDF

# Create PDF object
pdf = FPDF()
pdf.add_page()
class MyPDF(FPDF):
    def header(self):
        #logo
        try:
            self.image('nency.png', 10, 8, 33)
        except FileNotFoundError:
            print("Warning: 'nency.png' not found. Skipping logo.")
        # Arial bold 15
        self.set_font('helvetica', 'B', 20)
        # Title
        self.cell(0, 10, 'My PDF Header', 0, 1, 'C', border=0)
        # Line break
        self.ln(10)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'C')
# Set font
pdf.set_font("Arial", size=12)

# Add text
pdf.cell(120, 10, 'HELLO WORLD', new_x="LMARGIN", new_y="NEXT", border=1)
pdf.cell(300, 10, 'good bye world!', new_x="LMARGIN", new_y="NEXT")
for i in range(41):
    pdf.cell(0, 10, 'This is line %d' % (i + 1), new_x="LMARGIN", new_y="NEXT")
#set auto page break
pdf.set_auto_page_break(auto=True, margin=15)
#set pafe add
pdf.add_page()
pdf.set_fill_color(255, 255, 255)
# Add an image (optional, uncomment if you have an image)
# pdf.image("path_to_image.jpg", x=10, y=20, w=100)

# Set the position for the next cell
# Save PDF
pdf.output("hello_world.pdf")

print("PDF generated successfully! Open 'hello_world.pdf' to see the output.")

