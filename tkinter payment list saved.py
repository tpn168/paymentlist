import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import os

def submit_form():
    vessel = vessel_entry.get()
    vendor = vendor_entry.get()
    invoice_number = invoice_number_entry.get()
    price = price_entry.get()
    currency = currency_entry.get()
    buy_date = buy_date_entry.get_date()
    due_date = due_date_entry.get_date()
    remark = remark_entry.get()

    tree.insert('', 'end', values=("", vessel, vendor, invoice_number, price, currency, buy_date, due_date, remark))
    
    with open('PaymentCollect.txt', 'a', encoding='utf-8') as f:
        f.write(f'{vessel},{vendor},{invoice_number},{price},{currency},{buy_date},{due_date},{remark}\n')

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
                tree.insert('', 'end', values=("", *values))

def check_uncheck(event):
    item = tree.identify_row(event.y)
    if item:
        value = tree.item(item, "values")[0]
        if value == "✓":
            tree.set(item, '#1', "")
        else:
            tree.set(item, '#1', "✓")

root = tk.Tk()
root.title('Payment Lists')

labels = ['Vessel', 'Vendor', 'Invoice Number', 'Price', 'Currency', 'Remark']
entries = []

for label in labels:
    lbl = tk.Label(root, text=label)
    lbl.pack()
    entry = tk.Entry(root)
    entry.pack()
    entries.append(entry)

buy_date_label = tk.Label(root, text='Buy Date')
buy_date_label.pack()
buy_date_entry = DateEntry(root)
buy_date_entry.pack()

due_date_label = tk.Label(root, text='Due Date')
due_date_label.pack()
due_date_entry = DateEntry(root)
due_date_entry.pack()

vessel_entry, vendor_entry, invoice_number_entry, price_entry, currency_entry, remark_entry = entries

submit_button = tk.Button(root, text="Submit", command=submit_form, bg='#d3d3d3', fg='#800080')
submit_button.pack()

columns = ('Paid', 'Vessel', 'Vendor', 'Invoice Number', 'Price', 'Currency', 'Buy Date', 'Due Date', 'Remark')
tree = ttk.Treeview(root, columns=columns, show='headings')

for column in columns:
    tree.heading(column, text=column)

tree.pack()

tree.bind("<Button-1>", check_uncheck)

load_data()

root.mainloop()
