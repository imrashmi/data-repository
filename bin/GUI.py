import os
import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import random
import string
from datetime import datetime

# Function to generate random 8-digit bill number
def generate_bill_no():
    return ''.join(random.choices(string.digits, k=8))

# Function to copy EC/Roll No. as M.C. No. with "S" or "M" prepended randomly
def generate_mc_no(roll_no):
    prefix = random.choice(['S', 'M'])
    return f"{prefix}{roll_no}"

# Function to generate the PDF
def generate_pdf(patient_name, roll_no, mc_no, bill_no, date, medicines, prescribed_by, physician_name, output_path):
    pdf_file = os.path.join(output_path, f"{bill_no}.pdf")
    c = canvas.Canvas(pdf_file, pagesize=A4)
    width, height = A4
    left_margin, right_margin = 35, 35  # 1.25 cm margins
    top_margin, bottom_margin = 65, 65  # 2.25 cm margins

    # Draw the title
    c.setFont("Times-Roman", 12)
    c.drawCentredString(width / 2, height - top_margin, "HEALTH CENTRE")
    c.drawCentredString(width / 2, height - top_margin - 20, "NATIONAL INSTITUTE OF TECHNOLOGY, ROURKELA")
    c.drawCentredString(width / 2, height - top_margin - 40, "Online Billing")

    # Draw the subtitle
    c.setFont("Times-Bold", 10)
    c.drawCentredString(width / 2, height - top_margin - 60, "ORDER FOR PENDING MEDICINE")

    # Draw patient details
    c.setFont("Times-Roman", 10)
    c.drawString(left_margin, height - top_margin - 100, f"Date: {date}")
    c.drawString(300, height - top_margin - 100, f"Bill No.: {bill_no}")
    c.drawString(left_margin, height - top_margin - 120, f"Patient Name: {patient_name}")
    c.drawString(300, height - top_margin - 120, f"Roll No.: {roll_no}")
    c.drawString(left_margin, height - top_margin - 140, f"M.C. No.: {mc_no}")
    c.drawString(300, height - top_margin - 140, f"Prescribed By: {prescribed_by}")

    # Draw the table with medicine details
    data = [["S.No", "*", "Medicine Name", "Quantity", "Instruction", "Dose"]]
    for idx, medicine in enumerate(medicines, start=1):
        data.append([str(idx), medicine['reimbursable'], medicine['name'], medicine['quantity'], medicine['instruction'], medicine['dose']])

    # Create the table
    table = Table(data, colWidths=[30, 30, 160, 80, 100, 120])
    style = TableStyle([
        ('FONT', (0, 0), (-1, 0), 'Times-Bold'),
        ('FONT', (0, 1), (-1, -1), 'Times-Roman'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER')
    ])
    table.setStyle(style)

    # Position and draw the table
    table_width, table_height = table.wrapOn(c, width * 0.9, height)
    table.drawOn(c, left_margin, height - top_margin - 240)

    # Adjust position of the signature and following text based on the table's height
    y_position_after_table = height - top_margin - 240 - table_height - 20

    # If prescribed_by is 3 letters, use the physician name as the signature
    signature = physician_name if len(prescribed_by) == 3 else prescribed_by

    # Signature section dynamically placed after the table
    c.setFont("Times-Bold", 10)
    c.drawString(400, y_position_after_table, signature)
    c.line(400, y_position_after_table - 5, 550, y_position_after_table - 5)

    c.setFont("Times-Roman", 10)
    c.drawString(400, y_position_after_table - 20, "Signature of Physician")

    # Footer section with bold text
    c.setFont("Times-Bold", 10)
    footer_y_position = y_position_after_table - 40
    c.drawString(left_margin, footer_y_position, "* Marked medicines are not reimbursable")
    c.drawString(left_margin, footer_y_position - 20, "Do not submit it to Account Section for Billing")
    c.drawString(left_margin, footer_y_position - 40, "To")
    c.drawString(left_margin, footer_y_position - 60, "Institute Dispensary, NIT Campus Rourkela-8")
    c.drawString(left_margin, footer_y_position - 80, "Intercom. 2114, Mob. 799*****90")

    # Save the PDF
    c.showPage()
    c.save()

    messagebox.showinfo("Success", f"PDF generated at: {pdf_file}")

# Function to handle button click
def on_generate_click():
    patient_name = entry_patient_name.get()
    roll_no = entry_roll_no.get()
    mc_no = generate_mc_no(roll_no)
    bill_no = generate_bill_no()
    date = entry_date.get()
    prescribed_by = entry_prescribed_by.get()
    physician_name = entry_physician_name.get()
    output_path = filedialog.askdirectory()

    if not date:
        date = datetime.today().strftime('%d-%m-%Y')

    medicines = [
        {"name": "Paracetamol", "quantity": "10", "instruction": "B/F", "dose": "0 | X | 0", "reimbursable": ""},
        # Add more sample medicine data as needed
    ]

    generate_pdf(patient_name, roll_no, mc_no, bill_no, date, medicines, prescribed_by, physician_name, output_path)

# Create the GUI window
root = tk.Tk()
root.title("PDF Generator")

# Create input fields
tk.Label(root, text="Patient Name:").grid(row=0, column=0, padx=10, pady=5)
entry_patient_name = tk.Entry(root)
entry_patient_name.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Roll No.:").grid(row=1, column=0, padx=10, pady=5)
entry_roll_no = tk.Entry(root)
entry_roll_no.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Date:").grid(row=2, column=0, padx=10, pady=5)
entry_date = tk.Entry(root)
entry_date.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Prescribed By:").grid(row=3, column=0, padx=10, pady=5)
entry_prescribed_by = tk.Entry(root)
entry_prescribed_by.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Physician Name:").grid(row=4, column=0, padx=10, pady=5)
entry_physician_name = tk.Entry(root)
entry_physician_name.grid(row=4, column=1, padx=10, pady=5)

# Create a button to generate PDF
button_generate = tk.Button(root, text="Generate PDF", command=on_generate_click)
button_generate.grid(row=5, columnspan=2, pady=20)

# Run the main loop
root.mainloop()
