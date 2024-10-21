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
    # Define the output directory in the parent directory
    output_dir = os.path.join(os.path.dirname(os.getcwd()), 'Prescriptions')
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    # Create a new PDF
    pdf_file = f"{bill_no}.pdf"
    pdf_file_path = os.path.join(output_dir, pdf_file)
    c = canvas.Canvas(pdf_file_path, pagesize=A4)
    width, height = A4
    left_margin, right_margin = 35, 35  # 1.25 cm margins
    top_margin, bottom_margin = 65, 65  # 2.25 cm margins

    # Draw the title
    c.setFont("Times-Bold", 12)
    c.drawCentredString(width / 2, height - top_margin, "HEALTH CENTRE")
    c.drawCentredString(width / 2, height - top_margin - 20, institute)  # Corrected this line
    c.setFont("Times-Roman", 12)
    c.drawCentredString(width / 2, height - top_margin - 40, "Online Billing")

    # Draw the subtitle
    c.setFont("Times-Bold", 10)
    c.drawCentredString(width / 2, height - top_margin - 60, "Prescription")

    # Draw patient details
    c.setFont("Times-Bold", 10)
    c.drawString(left_margin, height - top_margin - 100, f"Date: {date}")
    c.drawString(300, height - top_margin - 100, f"Bill No.: {bill_no}")
    c.drawString(left_margin, height - top_margin - 120, f"Patient Name: {patient_name}")
    c.drawString(300, height - top_margin - 120, f"Roll No.: {roll_no}")
    c.drawString(left_margin, height - top_margin - 140, f"M.C. No.: {mc_no}")
    c.drawString(300, height - top_margin - 140, f"Prescribed By: {prescribed_by}")

    # Draw the table with medicine details
    data = [["S.No", "*", "Medicine Name", "Quantity", "Instruction", "Dose (#)"]]
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
    y_position_after_table = height - top_margin - 240 - table_height - 20  # 20 is the spacing between table and signature

    # Physician name as the signature
    signature = physician_name

    # Signature section dynamically placed after the table
    c.setFont("Times-Bold", 10)
    c.drawString(400, y_position_after_table, signature)
    c.line(400, y_position_after_table - 5, 550, y_position_after_table - 5)  # Draw line under the name

    c.setFont("Times-Roman", 10)
    c.drawString(400, y_position_after_table - 20, "Signature of Physician")

    # Footer section with bold text
    c.setFont("Times-Roman", 10)
    footer_y_position = y_position_after_table - 40
    c.drawString(left_margin, footer_y_position, "# Dose: 0 (Take) | X (Don't Take)")
    c.drawString(left_margin, footer_y_position - 20, "* Marked medicines are not reimbursable")
    c.drawString(left_margin, footer_y_position - 40, "** Do not submit it to Account Section for Billing")
    c.setFont("Times-Bold", 10)
    c.drawString(left_margin, footer_y_position - 80, "To, ")
    c.drawString(left_margin, footer_y_position - 100, end_note)
    c.drawString(left_margin, footer_y_position - 120, end_note_contact)

    # Save the PDF
    c.showPage()
    c.save()  # Save the PDF here

    print(f"PDF generated: {pdf_file_path}")

# Function to get checkbox input for dose and instruction
def get_checkbox_input(label):
    # Helper function to handle input with default 'n'
    def get_input_with_default(prompt):
        response = input(prompt).lower()
        return response if response in ['y', 'n'] else 'n'

    # Get dose information with default to 'n'
    morning = get_input_with_default(f"Is this medicine taken in the morning? (y/n): ") == 'y'
    noon = get_input_with_default(f"Is this medicine taken at noon? (y/n): ") == 'y'
    night = get_input_with_default(f"Is this medicine taken at night? (y/n): ") == 'y'
    
    # If all options are 'n', leave dose empty, otherwise format the dose
    if not (morning or noon or night):
        dose = ""  # No dose if all are 'n'
    else:
        dose = f"{'0' if morning else 'X'} | {'0' if noon else 'X'} | {'0' if night else 'X'}"

    # Get food instruction with default to 'n'
    before_food = get_input_with_default("Before food? (y/n): ") == 'y'

    if before_food:
        instruction = "B/F"
    else:
        # Only ask for After Food if Before Food is not chosen
        after_food = get_input_with_default("After food? (y/n): ") == 'y'
        if after_food:
            instruction = "A/F"
        else:
            instruction = "-"  # If neither is chosen, set instruction to "-"

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

# Function to generate a random 6-digit number formatted with dashes
def generate_random_contact():
    random_number = ''.join(random.choices(string.digits, k=6))
    return f"0671-{random_number[:3]}-{random_number[3:]}"

# Main function for interacting with the user
def main():
    medicines = []

    patient_name = input("Enter patient name: ")
    roll_no = input("Enter Patient Code (e.g. Employee ID/Regd. No): ")
    institute = input("Enter Organisation: ")

    # Auto-generate M.C. No. by prepending "S" or "M" randomly to the roll number
    mc_no = generate_mc_no(roll_no)

    # Auto-generate 8-digit bill number
    bill_no = generate_bill_no()

    # Date defaults to today if not provided
    date = input("Enter date (Leave blank for today's date): ")
    if not date:
        date = datetime.today().strftime('%d-%m-%Y')

    # Prescribed by input with default value
    prescribed_by_input = input("Enter prescribed by <INT/EXT: for internal/outside prescription> <Leave blank for Internal Prescription>: ").strip().upper()
    if prescribed_by_input == "EXT":
        prescribed_by = "External Prescription"
    else:
        prescribed_by = "Internal Prescription"

    # Default end note and contact if not provided by user
    end_note = input("Provide any institutional entity to which the bill will be submitted to: (e.g. Institute Dispensary, Organisation Name, Address): ").strip()
    if not end_note:
        end_note = "Financial Unit, Dispensary Division, \nRRSMEDIA Inc., Odisha 751010"

    end_note_contact = input("Institutional entity contact details if any (e.g. Intercom. 06xx-2xx4, Mob. 7xxxx-1xxx0): ").strip()
    if not end_note_contact:
        end_note_contact = f"Intercom {generate_random_contact()}"

    physician_name = input("Enter physician name: (Leave Blank for Internal Assigned Doctors): ") 
    if not physician_name:
        physician_name = "Dr. Ashutosh Jena"

   
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
                # Now pass `institute`, `end_note`, and `end_note_contact` when calling `generate_pdf`
                generate_pdf(patient_name, roll_no, mc_no, bill_no, date, medicines, prescribed_by, physician_name, institute, end_note, end_note_contact)
                break
            elif finalize_choice == '2':
                continue

if __name__ == "__main__":
    main()
