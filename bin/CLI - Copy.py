from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import random
import string
import os
from datetime import datetime

# Function to generate random 8-digit bill number
def generate_bill_no():
    return ''.join(random.choices(string.digits, k=8))

# Function to copy EC/Roll No. as M.C. No. with "S" or "M" prepended randomly
def generate_mc_no(roll_no):
    prefix = random.choice(['S', 'M'])
    return f"{prefix}{roll_no}"

# Function to generate the PDF
def generate_pdf(patient_name, roll_no, mc_no, bill_no, date, medicines, prescribed_by, physician_name):
    # Create a new PDF
    pdf_file = f"{bill_no}.pdf"
    c = canvas.Canvas(pdf_file, pagesize=A4)
    width, height = A4
    left_margin, right_margin = 35, 35  # 1.25 cm margins
    top_margin, bottom_margin = 65, 65  # 2.25 cm margins

    # Draw the title
    c.setFont("Times-Bold", 12)
    c.drawCentredString(width / 2, height - top_margin, "HEALTH CENTRE")
    c.drawCentredString(width / 2, height - top_margin - 20, "NATIONAL INSTITUTE OF TECHNOLOGY, ROURKELA")
    c.setFont("Times-Roman", 12)
    c.drawCentredString(width / 2, height - top_margin - 40, "Online Billing")

    # Draw the subtitle
    c.setFont("Times-Bold", 10)
    c.drawCentredString(width / 2, height - top_margin - 60, "ORDER FOR PENDING MEDICINE")

    # Draw patient details
    c.setFont("Times-Bold", 10)
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
    table_width, table_height = table.wrapOn(c, width * 0.9, height)  # Measure the height of the table
    table.drawOn(c, left_margin, height - top_margin - 240)

    # Adjust position of the signature and following text based on the table's height
    y_position_after_table = height - top_margin - 240 - table_height - 20  # 20 is the spacing between table and signature

    # If prescribed_by is 3 letters, use the physician name as the signature
    signature = physician_name if len(prescribed_by) == 3 else prescribed_by

    # Signature section dynamically placed after the table
    c.setFont("Times-Bold", 10)
    c.drawString(400, y_position_after_table, signature)
    c.line(400, y_position_after_table - 5, 550, y_position_after_table - 5)  # Draw line under the name

    c.setFont("Times-Roman", 10)
    c.drawString(400, y_position_after_table - 20, "Signature of Physician")

    # Footer section with bold text
    c.setFont("Times-Bold", 10)
    footer_y_position = y_position_after_table - 40  # Adjust position dynamically after
    c.drawString(left_margin, footer_y_position, "* Marked medicines are not reimbursable")
    c.drawString(left_margin, footer_y_position - 20, "** Do not submit it to Account Section for Billing")
    c.drawString(left_margin, footer_y_position - 60, "To, ")
    c.drawString(left_margin, footer_y_position - 80, "Institute Dispensary, NIT Campus Rourkela-8")
    c.drawString(left_margin, footer_y_position - 100, "Intercom. 2114, Mob. 79929-10190")

    # Save the PDF
    c.showPage()
    file = c.save()
    
    # Define the output directory in the parent directory
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Files')

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Full path for the PDF file
    pdf_file_path = os.path.join(output_dir, file)


    print(f"PDF generated: {output_dir}{pdf_file}")

# Function to get checkbox input for dose and instruction
def get_checkbox_input(label):
    morning = input(f"Is this medicine taken in the morning? (y/n): ").lower() == 'y'
    noon = input(f"Is this medicine taken at noon? (y/n): ").lower() == 'y'
    night = input(f"Is this medicine taken at night? (y/n): ").lower() == 'y'
    dose = f"{'0' if morning else 'X'} | {'0' if noon else 'X'} | {'0' if night else 'X'}"

    before_food = input("Before food? (y/n): ").lower() == 'y'
    instruction = "B/F" if before_food else "A/F"

    return dose, instruction

# Function to get medicine input from the user
def get_medicine_input(medicines):
    name = input("Enter medicine name: ")
    quantity = input("Enter quantity: ")
    dose, instruction = get_checkbox_input('Dose')
    reimbursable = input("Is this medicine reimbursable? (y/n): ").lower()
    reimbursable_mark = "*" if reimbursable == 'n' else ""
    medicines.append({'name': name, 'quantity': quantity, 'instruction': instruction, 'dose': dose, 'reimbursable': reimbursable_mark})
    return medicines

# Function to display medicines
def display_medicines(medicines):
    print("\nCurrent Medicines List:")
    for idx, medicine in enumerate(medicines, start=1):
        print(f"{idx}. {medicine['name']} - {medicine['quantity']} - {medicine['instruction']} - {medicine['dose']} - {'Non-Reimbursable' if medicine['reimbursable'] else 'Reimbursable'}")
    print()

# Main function for interacting with the user
def main():
    medicines = []

    patient_name = input("Enter patient name: ")
    roll_no = input("Enter roll number: ")

    # Auto-generate M.C. No. by prepending "S" or "M" randomly to the roll number
    mc_no = generate_mc_no(roll_no)

    # Auto-generate 8-digit bill number
    bill_no = generate_bill_no()

    # Date defaults to today if not provided
    date = input("Enter date (Leave blank for today's date): ")
    if not date:
        date = datetime.today().strftime('%d-%m-%Y')

    prescribed_by = input("Enter prescribed by: ")
    physician_name = input("Enter physician name: ")

    while True:
        print("\nOptions: \n1. Add Medicine \n2. View Medicines \n3. Modify Medicine \n4. Validate and Finalize")
        choice = input("Choose an option: ")

        if choice == '1':
            # Add medicine
            medicines = get_medicine_input(medicines)

        elif choice == '2':
            # View medicines
            display_medicines(medicines)

        elif choice == '3':
            # Modify medicine
            display_medicines(medicines)
            to_delete = int(input("Enter the serial number of the medicine to delete: ")) - 1
            if 0 <= to_delete < len(medicines):
                del medicines[to_delete]
                print("Medicine deleted.")
            else:
                print("Invalid serial number.")

        elif choice == '4':
            # Validate and finalize
            display_medicines(medicines)
            finalize_choice = input("1. Generate PDF \n2. Modify Medicines\nChoose: ")
            if finalize_choice == '1':
                generate_pdf(patient_name, roll_no, mc_no, bill_no, date, medicines, prescribed_by, physician_name)
                break
            elif finalize_choice == '2':
                continue

if __name__ == "__main__":
    main()