import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import os
import csv

def submit_form():
    answer = messagebox.askquestion('Confirm Submission', 'Do you want to submit the data?')

    if answer == 'yes':
        vessel = vessel_entry.get()
        vendor = vendor_entry.get()
        invoice_number = invoice_number_entry.get()
        price = price_entry.get()
        currency = currency_entry.get()
        remark = remark_entry.get()
        buy_date = buy_date_entry.get_date()
        due_date = due_date_entry.get_date()

        tree.insert('', 'end', values=("Unpaid", vessel, vendor, invoice_number, price, currency, remark, buy_date, due_date))
        vessel_entry.delete(0, 'end')
        vendor_entry.delete(0, 'end')
        invoice_number_entry.delete(0, 'end')
        price_entry.delete(0, 'end')
        currency_entry.delete(0, 'end')
        remark_entry.delete(0, 'end')

def load_data():
    if os.path.exists('PaymentCollect.csv'):
        with open('PaymentCollect.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for values in reader:
                tree.insert('', 'end', values=values)

def save_data():
    with open('PaymentCollect.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for row in tree.get_children():
            row_data = tree.item(row)['values']
            writer.writerow(row_data)  # Save the whole row, including 'Paid' column

def delete_row():
    selected_item = tree.selection()  # get selected item
    if selected_item:  # if item selected
        answer = messagebox.askquestion('Delete', 'Are you sure you want to delete?')
        if answer == 'yes':
            tree.delete(selected_item)

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
        status_combobox = ttk.Combobox(toplevel, values=["Paid", "Unpaid"])
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


labels = ['Vessel', 'Vendor', 'Invoice Number', 'Price', 'Currency', 'Remark', 'Buy Date', 'Due Date']
entries = []
frame = tk.Frame(root)
frame.pack()

for i, label in enumerate(labels):
    lbl = tk.Label(frame, text=label, font=("Arial", 14, 'bold'))  # Increase font size here
    lbl.grid(row=i//2, column=(i%2)*2)
    if label in ['Buy Date', 'Due Date']:
        entry = DateEntry(frame)
    else:
        entry = tk.Entry(frame)
    entry.grid(row=i//2, column=(i%2)*2+1)
    entries.append(entry)

vessel_entry, vendor_entry, invoice_number_entry, price_entry, currency_entry, remark_entry, buy_date_entry, due_date_entry = entries

submit_button = tk.Button(root, text="Submit", command=submit_form, bg='#d3d3d3', fg='#800080')
submit_button.pack()

columns = ('Status', 'Vessel', 'Vendor', 'Invoice Number', 'Price', 'Currency', 'Remark', 'Buy Date', 'Due Date')
tree = ttk.Treeview(root, columns=columns, show='headings')

# Set column fonts to bold and set background color to a color other than white.
style = ttk.Style(root)
style.configure("Treeview.Heading", font=(None, 10, 'bold'))
style.configure("Treeview", background="lightgray")  # Change 'lightgray' to color of your choice.

for column in columns:
    tree.heading(column, text=column)

tree.pack(fill='both', expand=True)  # Pack treeview widget to fill the entire root window.

tree.bind("<Double-1>", check_uncheck)

# Create a right-click menu using a Menu widget
popup = tk.Menu(root, tearoff=0)
popup.add_command(label="Delete", command=delete_row)  # Add delete option to the menu

def do_popup(event):
    # display the popup menu
    try:
        popup.tk_popup(event.x_root, event.y_root, 0)
    finally:
        # make sure to release the grab (Tk 8.0a1 only)
        popup.grab_release()

tree.bind("<Button-3>", do_popup)  # Bind right click to do_popup

load_data()

root.protocol('WM_DELETE_WINDOW', ask_save)

root.mainloop()
