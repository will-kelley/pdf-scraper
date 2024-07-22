from fpdf import FPDF
from datetime import datetime

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Sample PDF Document', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(10)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

#Baseball Scores
pdf = PDF()
pdf.add_page()
pdf.chapter_title('Baseball Scores')
pdf.chapter_body(
    "2023-04-01\n"
    "Yankees vs Red Sox\n"
    "Score: 5-3.\n\n"
    "2023-04-02\n"
    "Dodgers vs Giants\n"
    "Score: 4-4.\n\n"
    "2023-04-03\n"
    "Cubs vs Cardinals\n"
    "Score: 2-1.\n"
)
pdf.output('pdfs/baseball_scores.pdf')

#Vaccine Records
pdf = PDF()
pdf.add_page()
pdf.chapter_title('Vaccination Records')
pdf.chapter_body(
    "2022-01-15\n"
    "Patient: John Doe\n"
    "Vaccine: COVID-19\n"
    "Dose: 1st.\n\n"
    "2022-02-15\n"
    "Patient: John Doe\n"
    "Vaccine: COVID-19\n"
    "Dose: 2nd.\n\n"
    "2023-03-20\n"
    "Patient: Jane Smith\n"
    "Vaccine: Influenza\n"
    "Dose: 1st.\n"
)
pdf.output('pdfs/vaccination_records.pdf')

#Combined
pdf = PDF()
pdf.add_page()
pdf.chapter_title('Random Information')
pdf.chapter_body(
    "This document contains various pieces of random information. "
    "It includes data about different subjects, not limited to sports, health, and daily facts.\n\n"
    "Interesting Fact: The Eiffel Tower can be 15 cm taller during the summer due to the expansion of iron.\n\n"
    "Health Tip: Drinking water helps to maintain the balance of body fluids.\n\n"
    "Random Quote: 'To be yourself in a world that is constantly trying to make you something else is the greatest accomplishment.' - Ralph Waldo Emerson\n"
)
pdf.output('pdfs/random_information.pdf')

