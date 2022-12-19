from fpdf import FPDF
import os

class PdfReport():
    """
    object that represents the PDF that it's going to be generated
    to show a brief of the bill and the executed operations
    """

    def __init__(self, filename):
        self.filename = filename

    def generate(self, bill, flatmates):
        description = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."""

        # create a pdf instance
        pdf = FPDF(orientation="P", unit="pt", format="A4")
        pdf.add_page()   

        # meta data
        pdf.set_author(author="Balyverse")
        pdf.set_creator(creator="Balyverse")
        pdf.set_title(title="Bill")

        # logo
        pdf.image(name="./assets/balydev_logo.png", w=80)

        # title
        pdf.set_font(family="Helvetica", style="B", size=24)
        pdf.cell(w=0, h=60, txt="Bill - " + str(bill.period), border=0, align="L", ln=2)
        
        # description
        pdf.set_font(family="Helvetica", style="", size=14)
        pdf.multi_cell(w=0, h=20, txt=description, border=0, align="L")

        # flatmates
        pdf.set_font(family="Helvetica", style="B", size=18)
        pdf.cell(w=0, h=50, txt="Flatmates:", border=0, align="L", ln=2)

        for i in range(2):
            pdf.set_font(family="Helvetica", style="B", size=14)
            pdf.cell(w=0, h=25, txt=flatmates[i].name + " -", border=0, align="L", ln=1)
            pdf.set_font(family="Helvetica", style="", size=14)
            
            if i == 0:
                pdf.cell(w=0, h=20, txt=str(flatmates[i].pays(bill, flatmates[1])) + "$", border=0, align="L", ln=1)
            else:
                pdf.cell(w=0, h=20, txt=str(flatmates[i].pays(bill, flatmates[0])) + "$", border=0, align="L", ln=1)

            pdf.cell(w=0, h=20, txt="", border=0, align="L", ln=1)

        # output
        os.chdir("./reports")
        pdf.output(self.filename + '.pdf')