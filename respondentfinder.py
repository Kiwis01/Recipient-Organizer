import fitz  # PyMuPDF
import re
from collections import defaultdict

def process_pdf(pdf_path):
    names_list = []  # To store names
    money_list = []
    is_void = False
    
    with fitz.open(pdf_path) as pdf_document:
        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            text = page.get_text()

            # Use regex to find names and amounts after 'Virtual Incentives' and 'Focus Group Wallet'
            matches_vi = re.finditer(r'Virtual Incentives\s+([A-Za-z\s]+)', text)
            matches_fg = re.finditer(r'Focus Group Wallet\s+([A-Za-z\s]+)', text)
            matches_paid = re.finditer(r'(Paid|Void)\s+\$([\d,]+\.\d{2})', text)

            for match in matches_paid:
                action = match.group(1).strip()
                mon = float(match.group(2).replace(',', ''))
                
                if action == 'Paid' and mon != 0:
                    money_list.append(mon)
                    is_void = False
                elif action == 'Void' and not is_void:
                    money_list.append(-mon)  
                    is_void = True

            for match in matches_vi:
                name = match.group(1).strip()
                names_list.append(name)

            for match in matches_fg:
                name = match.group(1).strip()
                names_list.append(name)

    return names_list, money_list

def simplify_list(names, amounts):
    simplified_dict = defaultdict(float)
    for name, amount in zip(names, amounts):
        simplified_dict[name] += amount

    simplified_list = [(name, total_amount) for name, total_amount in zip(names, amounts) if total_amount != 0]
    return simplified_list

def main():
    pdf_path = "data.pdf"  
    names, amounts = process_pdf(pdf_path)
    
    simplified_list = simplify_list(names, amounts)

    for name, total_amount in simplified_list:
        print(f"Recipient: {name}, Amount paid: ${total_amount:.2f}")

if __name__ == "__main__":
    main()
