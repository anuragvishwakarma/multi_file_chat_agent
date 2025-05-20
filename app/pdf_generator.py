from fpdf import FPDF
import matplotlib.pyplot as plt
import os
from datetime import datetime
import json


class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_page()
        font_path = os.path.join("app", "fonts", "DejaVuSans.ttf")  # Update if different
        self.add_font("DejaVu", "", font_path, uni=True)
        self.set_font("DejaVu", "", 12)

    def chapter_title(self, title):
        self.set_font("DejaVu", "", 14)
        self.cell(0, 10, title, ln=True)

    def chapter_body(self, body):
        self.set_font("DejaVu", "", 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_dataframe(self, df, title="Data Snapshot"):
        self.chapter_title(title)
        self.set_font("Courier", "", 9)
        table_str = df.to_string(index=False)
        self.multi_cell(0, 5, table_str)
        self.ln()

    def add_chart(self, fig_path, title="Chart"):
        self.chapter_title(title)
        self.image(fig_path, w=180)
        self.ln()

def create_pdf_report(query, answer, dfs, chart_paths=None, output_path="report.pdf"):
    pdf = PDF()
    pdf.add_page()
    pdf.chapter_title("User Query")
    pdf.chapter_body(query)
    pdf.chapter_title("AI-Generated Answer")
    pdf.chapter_body(str(answer))

    for sheet, df in dfs.items():
        pdf.add_dataframe(df.head(10), title=f"Sheet: {sheet} (Top 10 rows)")

    if chart_paths:
        for chart_path in chart_paths:
            pdf.add_chart(chart_path)

    pdf.output(output_path)
    return output_path


def generate_chart(df, filename):
    plt.figure(figsize=(6,4))
    df.select_dtypes(include='number').head(10).plot(kind='bar')
    plt.title("Sample Bar Chart")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
