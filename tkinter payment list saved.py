import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import os

def submit_form():
    answer = messagebox.askquestion('Confirm Submission', 'Do you want to submit the data?')

    if answer == 'yes':
        vessel = vessel_entry.get()
        vendor = vendor_entry.get()
        invoice_number = invoice_number_entry.get()
        price = price_entry.get()
        currency = currency_entry.get()
        buy_date = buy_date_entry.get_date()
        due_date = due_date_entry.get_date()
        remark = remark_entry.get()

        tree.insert('', 'end', values=("Unpaid", vessel, vendor, invoice_number, price, currency, buy_date, due_date, remark))
        vessel_entry.delete(0, 'end')
        vendor_entry.delete(0, 'end')
        invoice_number_entry.delete(0, 'end')
        price_entry.delete(0, 'end')
        currency_entry.delete(0, 'end')
        remark_entry.delete(0, 'end')

def load_data():
    if os.path.exists('PaymentCollect.txt'):
        with open('PaymentCollect.txt', 'r', encoding='utf-8') as f:
            for line in f:
                values = line.strip().split(',')
                tree.insert('', 'end', values=("Unpaid", *values))

def save_data():
    # clear file
    open('PaymentCollect.txt', 'w').close()

    # iterate through treeview and save all rows
    for row in tree.get_children():
        row_data = tree.item(row)['values']
        with open('PaymentCollect.txt', 'a', encoding='utf-8') as f:
            f.write(','.join(str(r) for r in row_data[1:]) + '\n')

def status_change(value):
    tree.set(cur_item, '#1', value)

def check_uncheck(event):
    global cur_item
    cur_item = tree.identify_row(event.y)
    cur_col = tree.identify_column(event.x)
    if cur_item and cur_col == '#1':
        toplevel = tk.Toplevel(root)
        toplevel.title("Choose status")
        ttk.Label(toplevel, text="Choose status:").pack(pady=10, padx=10)
        status_combobox = ttk.Combobox(toplevel, values=["Done", "Unpaid"])
        status_combobox.pack(pady=10, padx=10)
        status_combobox.bind("<<ComboboxSelected>>", lambda e: status_change(status_combobox.get()))
        toplevel.transient(root)
        toplevel.grab_set()
        root.wait_window(toplevel)

def ask_save():
    answer = messagebox.askquestion('Save data', 'Do you want to save data before closing?')

    if answer == 'yes':
        save_data()

    root.destroy()

root = tk.Tk()
root.title('Payment Lists')

labels = ['Vessel', 'Vendor', 'Invoice Number', 'Price', 'Currency', 'Buy Date', 'Due Date', 'Remark']
entries = []
frame = tk.Frame(root)  # A frame for your input boxes
frame.pack()

for i, label in enumerate(labels):
    lbl = tk.Label(frame, text=label)
    lbl.grid(row=i//2, column=(i%2)*2)  # Use grid instead of pack
    if label in ['Buy Date', 'Due Date']:  # DateEntry for dates
        entry = DateEntry(frame)
    else:  # normal Entry for other fields
        entry = tk.Entry(frame)
    entry.grid(row=i//2, column=(i%2)*2+1)  # Use grid instead of pack
    entries.append(entry)

vessel_entry, vendor_entry, invoice_number_entry, price_entry, currency_entry, buy_date_entry, due_date_entry, remark_entry = entries

submit_button = tk.Button(root, text="Submit", command=submit_form, bg='#d3d3d3', fg='#800080')
submit_button.pack()

columns = ('Paid', 'Vessel', 'Vendor', 'Invoice Number', 'Price', 'Currency', 'Buy Date', 'Due Date', 'Remark')
tree = ttk.Treeview(root, columns=columns, show='headings')

for column in columns:
    tree.heading(column, text=column)

tree.pack()

tree.bind("<Double-1>", check_uncheck)

load_data()

root.protocol('WM_DELETE_WINDOW', ask_save)

root.mainloop()
