from tkinter import *
from tkinter import messagebox
import tkinter.font as tkFont

import os

from datetime import date, timedelta
from datetime import datetime
from fillpdf import fillpdfs


# Center a window on the screen
def center(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    try:
        win.update_idletasks()
        width = win.winfo_width()
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width
        height = win.winfo_height()
        titlebar_height = win.winfo_rooty() - win.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = win.winfo_screenwidth() // 2 - win_width // 2
        y = win.winfo_screenheight() // 2 - win_height // 2
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        win.deiconify()
    except AttributeError:
        pass

# Generate new invoice number
def get_invoice_number():
    # Create variable that will store new generated invoice number
    new_invoice_number = int
    current_year = datetime.now().year
    current_month = datetime.now().month

    # Go through the txt file and see what is the last invoice number
    with open('invoice_number.txt', encoding='utf-8') as f:
        invoice_number = f.readline().strip()

    if invoice_number[0:4] == str(current_year):
        if invoice_number[4:6] == str(f'0{current_month}'):
            new_invoice_number = int(invoice_number) + 1
        else:
            new_invoice_number = int(f'{current_year}0{current_month}001')
    else:
        new_invoice_number = int(f'{current_year}{current_month}001')

    with open('invoice_number.txt', 'w+', encoding='utf-8') as f:
        f.write(str(new_invoice_number))

    return str(invoice_number)

# Get current invoice number
def get_current_invoice_number():
    # Go through the txt file and see what is the last invoice number
    with open('invoice_number.txt', encoding='utf-8') as f:
        invoice_number = f.readline().strip()

    return invoice_number

# Change the invoice number
def change_invoice_number(new_number):
    with open('invoice_number.txt', 'w+', encoding='utf-8') as f:
        f.write(str(new_number))


class App:
    # Initilize the app
    def __init__(self):
        
        # Define data that needs to be filled
        self.data = fillpdfs.get_form_fields('template.pdf')

        # App variables
        self.product_list = []
        
        # Define the app
        self.app = Tk()

        # Custom configurations for the app
        self.app.title('Invoice Generator')
        self.app.geometry('600x300')
        self.app.configure(bg='white')
        self.app.resizable(False, False)

        # Setting up fonts
        self.headingFont = tkFont.Font(family='Arial', size=15, weight='bold')

        # Reset button
        self.resetButton = Button(self.app, text="Reset", height=1, command=self.reset_button)
        self.resetButton.configure(fg='#4B0082', activeforeground='#4B0082')
        self.resetButton.grid(row=4, column=0)
        self.resetButton.place(relx=0.033, rely=0.05, anchor=CENTER)

        # Reset button
        self.resetButton = Button(self.app, text="Invoice Number", height=1, command=self.invoice_number_page)
        self.resetButton.configure(fg='#4B0082', activeforeground='#4B0082')
        self.resetButton.grid(row=4, column=0)
        self.resetButton.place(relx=0.145, rely=0.05, anchor=CENTER)

        # Initiate the first page
        self.customer_page()

        # Start the app when called
        center(self.app)
        self.app.mainloop()

    # Page to fulfill information about the client
    # Should include following properties: Client Name, Client AddressLine 1, Postal Code + City
    def customer_page(self):
        # Delete fields
        self.delete_fields()

        # Heading of the page
        self.customerInfo = Label(self.app, text="Customer Information")
        self.customerInfo.configure(font=self.headingFont, bg='white')
        self.customerInfo.place(relx=0.49, rely=0.15, anchor=CENTER)

        # Label for customer name
        self.customerNameLabel = StringVar()
        self.customerNameLabel.set('Enter the name: ')

        self.customerName = Label(self.app, textvariable=self.customerNameLabel, width=40)
        self.customerName.configure(bg='white')
        self.customerName.place(relx=0.161, rely=0.30, anchor=CENTER)

        # Entry field for customer name
        self.customerNameEntry = StringVar(None)
        self.customerNameEntry = Entry(self.app, width=40)
        self.customerNameEntry.place(relx=0.67, rely=0.30, anchor=CENTER)

        # Label for addressLine 1
        self.customerAddressLabel = StringVar()
        self.customerAddressLabel.set('Enter the address: ')

        self.customerAddress = Label(self.app, textvariable=self.customerAddressLabel, width=40)
        self.customerAddress.configure(bg='white')
        self.customerAddress.place(relx=0.170, rely=0.45, anchor=CENTER)

        # Entry field for customer address
        self.customerAddressEntry = StringVar(None)
        self.customerAddressEntry = Entry(self.app, width=40)
        self.customerAddressEntry.place(relx=0.67, rely=0.45, anchor=CENTER)

        # Label for postal code and city
        self.customerPostalLabel = StringVar()
        self.customerPostalLabel.set('Enter the postal code and city: ')

        self.customerPostal = Label(self.app, textvariable=self.customerPostalLabel, width=40)
        self.customerPostal.configure(bg='white')
        self.customerPostal.place(relx=0.225, rely=0.60, anchor=CENTER)

        # Entry field for customer postal code and city
        self.customerPostalEntry = StringVar(None)
        self.customerPostalEntry = Entry(self.app, width=40)
        self.customerPostalEntry.place(relx=0.67, rely=0.60, anchor=CENTER)

        # Next button
        self.customerButtonStyles = LabelFrame(self.app, bd=2, bg='#4B0082', relief=FLAT)
        self.customerButtonStyles.grid(row=0, column=0)
        self.customerButtonStyles.place(relx=0.5, rely=0.78, anchor=CENTER)

        self.customerButton = Button(self.customerButtonStyles, text='Next', command=self.product_page, width=12, fg='#4B0082', bg='white', activebackground='white', activeforeground='#4B0082', relief=FLAT)
        self.customerButton.grid(row=0, column=0)

    # Should include number of products for the clients
    def product_page(self):
        # Check if window exists, if yes => save the data to the file
        if self.customerNameEntry.winfo_exists():
            if self.customerNameEntry.get() == '':
                return center(messagebox.showerror('Error', 'Please at least fulfill the name of the customer.'))
            self.data['client_name'] = self.customerNameEntry.get()
            self.data['client_addressLine_1'] = self.customerAddressEntry.get()
            self.data['postal_code'] = self.customerPostalEntry.get()
        else:
            pass

        # Delete fields
        self.delete_fields()

        # Heading of the page
        self.productInfo = Label(self.app, text="Product Information")
        self.productInfo.configure(font=self.headingFont, bg='white')
        self.productInfo.place(relx=0.49, rely=0.15, anchor=CENTER)

        # Label for product name
        self.productNameLabel = StringVar()
        self.productNameLabel.set('Enter the name: ')

        self.productName = Label(self.app, textvariable=self.productNameLabel, width=40)
        self.productName.configure(bg='white')
        self.productName.place(relx=0.158, rely=0.30, anchor=CENTER)

        # Entry field for product name
        self.productNameEntry = StringVar(None)
        self.productNameEntry = Entry(self.app, width=40)
        self.productNameEntry.place(relx=0.67, rely=0.30, anchor=CENTER)

        # Label for product quantity
        self.productQuantityLabel = StringVar()
        self.productQuantityLabel.set('Enter the quantity: ')

        self.productQuantity = Label(self.app, textvariable=self.productQuantityLabel, width=40)
        self.productQuantity.configure(bg='white')
        self.productQuantity.place(relx=0.170, rely=0.45, anchor=CENTER)

        # Entry field for product quantity
        self.productQuantityEntry = StringVar(None)
        self.productQuantityEntry = Entry(self.app, width=40)
        self.productQuantityEntry.place(relx=0.67, rely=0.45, anchor=CENTER)

        # Label for product price
        self.productPriceLabel = StringVar()
        self.productPriceLabel.set('Enter the price per product:                      €')

        self.productPrice = Label(self.app, textvariable=self.productPriceLabel, width=40)
        self.productPrice.configure(bg='white')
        self.productPrice.place(relx=0.267, rely=0.60, anchor=CENTER)

        # Entry field for product price
        self.productPriceEntry = StringVar(None)
        self.productPriceEntry = Entry(self.app, width=40)
        self.productPriceEntry.place(relx=0.67, rely=0.60, anchor=CENTER)

        # Button to add the product to the list
        self.addButtonBackStyles = LabelFrame(self.app, bd=2, bg='#4B0082', relief=FLAT)
        self.addButtonBackStyles.grid(row=0, column=0)
        self.addButtonBackStyles.place(relx=0.92, rely=0.445, anchor=CENTER)

        self.addButtonBack = Button(self.addButtonBackStyles, text='+', command=self.add_product, width=2, height=6,
                                    fg='#4B0082', bg='white', activebackground='white', activeforeground='#4B0082', relief=FLAT)
        self.addButtonBack.grid(row=0, column=0)

        # Back button
        self.productButtonBackStyles = LabelFrame(self.app, bd=2, bg='#4B0082', relief=FLAT)
        self.productButtonBackStyles.grid(row=1, column=0)
        self.productButtonBackStyles.place(relx=0.4, rely=0.78, anchor=CENTER)

        self.productButtonBack = Button(self.productButtonBackStyles, text='Back', command=self.customer_page, width=12, fg='#4B0082', bg='white', activebackground='white', activeforeground='#4B0082', relief=FLAT)
        self.productButtonBack.grid(row=1, column=0)

        # Next button
        self.productButtonStyles = LabelFrame(self.app, bd=2, bg='#4B0082', relief=FLAT)
        self.productButtonStyles.grid(row=2, column=0)
        self.productButtonStyles.place(relx=0.6, rely=0.78, anchor=CENTER)

        self.productButton = Button(self.productButtonStyles, text='Next', command=self.save_page, width=12, fg='#4B0082', bg='white', activebackground='white', activeforeground='#4B0082', relief=FLAT)
        self.productButton.grid(row=2, column=0)

    # Function to save the pdf
    def save_page(self):

        # Check whether fields we entered
        if len(self.product_list) < 1 and (self.productNameEntry.get() == '' or (self.productQuantityEntry.get() == '' or not self.productQuantityEntry.get().isdigit()) or (self.productPriceEntry.get() == '' or not self.productPriceEntry.get().isdigit())):
            return center(messagebox.showerror('Error', 'Please fulfill all the fields. Make sure that quantity and price is a number.'))

        # Delete fields
        self.delete_fields()

        # Header of the page
        self.saveInfo = Label(self.app, text="Generate and save the invoice")
        self.saveInfo.configure(font=self.headingFont, bg='white')
        self.saveInfo.place(relx=0.49, rely=0.15, anchor=CENTER)

        # Table with products


        # Back button
        self.saveButtonBackStyles = LabelFrame(self.app, bd=2, bg='#4B0082', relief=FLAT)
        self.saveButtonBackStyles.grid(row=1, column=0)
        self.saveButtonBackStyles.place(relx=0.4, rely=0.78, anchor=CENTER)

        self.saveButtonBack = Button(self.saveButtonBackStyles, text='Back', command=self.product_page, width=12, fg='#4B0082', bg='white', activebackground='white', activeforeground='#4B0082', relief=FLAT)
        self.saveButtonBack.grid(row=1, column=0)

        # Next button
        self.saveButtonStyles = LabelFrame(self.app, bd=2, bg='#4B0082', relief=FLAT)
        self.saveButtonStyles.grid(row=2, column=0)
        self.saveButtonStyles.place(relx=0.6, rely=0.78, anchor=CENTER)

        self.saveButton = Button(self.saveButtonStyles, text='Save', command=self.save_invoice, width=12, fg='#4B0082', bg='white', activebackground='white', activeforeground='#4B0082', relief=FLAT)
        self.saveButton.grid(row=2, column=0)

    # Change the invoice number pag
    def invoice_number_page(self):

        # Delete fields
        self.delete_fields()

        # Get current invoice number
        invoice_number = get_current_invoice_number()

        # Header of the page
        self.invoiceNumberInfo = Label(self.app, text="Change the invoice number")
        self.invoiceNumberInfo.configure(font=self.headingFont, bg='white')
        self.invoiceNumberInfo.place(relx=0.49, rely=0.30, anchor=CENTER)

        # Label for product name
        self.invoiceNumberLabel = StringVar()
        self.invoiceNumberLabel.set('Invoice number: ')
        
        self.invoiceNumber = Label(self.app, textvariable=self.invoiceNumberLabel, width=40)
        self.invoiceNumber.configure(bg='white')
        self.invoiceNumber.place(relx=0.158, rely=0.50, anchor=CENTER)

        # Entry field for invoiceNumbere
        self.invoiceNumberEntry = StringVar(None)
        self.invoiceNumberEntry = Entry(self.app, width=40, )
        self.invoiceNumberEntry.place(relx=0.67, rely=0.48, anchor=CENTER)

        self.invoiceNumberEntry.insert(END, str(invoice_number))

        # Next button
        self.invoiceNumberButtonStyles = LabelFrame(self.app, bd=2, bg='#4B0082', relief=FLAT)
        self.invoiceNumberButtonStyles.grid(row=0, column=0)
        self.invoiceNumberButtonStyles.place(relx=0.5, rely=0.70, anchor=CENTER)

        self.invoiceNumberButton = Button(self.invoiceNumberButtonStyles, text='Change', command=self.new_invoice_number, width=12, fg='#4B0082', bg='white', activebackground='white', activeforeground='#4B0082', relief=FLAT)
        self.invoiceNumberButton.grid(row=0, column=0)

    # Page to change the settings and personal information
    def setting(self):
        self.delete_fields()

    ### ------------------ NOT PAGES, !FUNCTIONS! ------------------ ###

    # Function to add product
    def add_product(self):
        # Check whether all fields are fulfilled before adding the product
        if self.productNameEntry.get() == '' or self.productQuantityEntry.get() == '' or self.productPriceEntry.get() == '':
            return center(messagebox.showerror('Fill all fields', 'Please fulfill all the fields before adding the product'))

        else:
            # If added product list isn't more than five, can add the product
            if len(self.product_list) < 5:
                # If product is delivery, put VAT to 1
                if self.productNameEntry.get() == 'Delivery':
                    self.product_list.append({
                        self.productNameEntry.get(): [int(self.productQuantityEntry.get()), int(self.productPriceEntry.get()), 1]
                    })

                else:    
                    self.product_list.append({
                        self.productNameEntry.get(): [int(self.productQuantityEntry.get()), int(self.productPriceEntry.get()), 9]
                    })
                    
                # Empty the fields for the next product
                self.productNameEntry.delete(0, END)
                self.productQuantityEntry.delete(0, END)
                self.productPriceEntry.delete(0, END)
                
                return center(messagebox.showinfo('Success', 'Product was successfully added!'))

            else:
               return center(messagebox.showerror('Too many products', 'Maximum amount of products is five. Please contact all mighty Sadi to fix this.'))

    # Function to clear all the added products
    def delete_products(self):
        self.product_list = []

        # Empty the fields for the next product
        self.productNameEntry.delete(0, END)
        self.productQuantityEntry.delete(0, END)
        self.productPriceEntry.delete(0, END)

        return center(messagebox.showinfo('Success', 'Delete all products from the list'))

    # Rest button
    def reset_button(self):
        # Define data that needs to be filled
        self.data = fillpdfs.get_form_fields('template.pdf')

        # App variables
        self.product_list = []

        # Initialize first page
        self.customer_page()

    # Delete fields
    def delete_fields(self):
        try:
            self.productInfo.destroy()
            self.productName.destroy()
            self.productNameEntry.destroy()
            self.productQuantity.destroy()
            self.productQuantityEntry.destroy()
            self.productPrice.destroy()
            self.productPriceEntry.destroy()
            self.addButtonBackStyles.destroy()
            self.addButtonBack.destroy()
            self.productButtonBackStyles.destroy()
            self.productButtonBack.destroy()
            self.productButtonStyles.destroy()
            self.productButton.destroy()
        except AttributeError: 
            pass

        # Delete the fields from the save page
        try:
            self.saveInfo.destroy()
            self.saveButtonStyles.destroy()
            self.saveButton.destroy()
            self.saveButtonBackStyles.destroy()
            self.saveButtonBack.destroy()
        except AttributeError:
            pass

        # Delete the pages from the customer page
        try:
            self.customerInfo.destroy()
            self.customerName.destroy()
            self.customerNameEntry.destroy()
            self.customerAddress.destroy()
            self.customerAddressEntry.destroy()
            self.customerPostal.destroy()
            self.customerPostalEntry.destroy()
            self.customerButtonStyles.destroy()
            self.customerButton.destroy()
        except AttributeError:
            pass

        # Delete the invoice number
        try:
            self.invoiceNumberInfo.destroy()
            self.invoiceNumber.destroy()
            self.invoiceNumberEntry.destroy()
            self.invoiceNumberButtonStyles.destroy()
            self.invoiceNumberButton.destroy()
        except AttributeError:
            pass

    # Function to save the product list to the data variable
    def save_to_data(self):
        # Variables needed for the total invoice amount
        total_price_excl_vat = 0
        total_vat = 0
        total_price_incl_vat = 0
        # Loop through the list and add the products
        for index, value in enumerate(self.product_list):
            for product in value:
                # Correct index for the product
                idx = str(index + 1)
                
                # Current product
                current_product = self.product_list[index]

                # If delivery is the product, do not make VAT calculations
                if product.lower() == 'delivery':
                    # Correct total price per product
                    total_product_price_float = round((int(current_product[product][0]) * int(current_product[product][1])), 2)

                    if total_product_price_float % 10 == 0:
                        total_product_price = int(total_product_price_float)
                    else:
                        total_product_price = total_product_price_float

                    self.data[f'product_{idx}'] = product
                    self.data[f'quantity_{idx}'] = current_product[product][0]
                    self.data[f'total_price_{idx}'] = f'€{current_product[product][1]}'

                else:
                    # Correct total price per product
                    total_product_price_float = round((int(current_product[product][0]) * int(current_product[product][1]) * 1.09), 2)
                    total_vat += round((int(current_product[product][0] * int(current_product[product][1])) * 0.09), 2)

                    if total_product_price_float % 10 == 0:
                        total_product_price = int(total_product_price_float)
                    else:
                        total_product_price = total_product_price_float

                    # Add all the data to the list
                    self.data[f'product_{idx}'] = product
                    self.data[f'quantity_{idx}'] = current_product[product][0]
                    self.data[f'price_{idx}'] = f'€{current_product[product][1]}'
                    self.data[f'vat_{idx}'] = f'{current_product[product][2]}%'
                    self.data[f'total_price_{idx}'] = f'€{str(total_product_price)}'

                # Add this for the final result
                total_price_incl_vat += total_product_price
                total_price_excl_vat += round((int(current_product[product][0]) * int(current_product[product][1])), 2)
        
        # Add the total amoun to the invoice
        self.data['total_excl_vat'] = total_price_excl_vat
        self.data['total_vat'] = total_vat
        self.data['total_incl_vat'] = total_price_incl_vat

    # Save the file
    def save_invoice(self):
        # Save everything to the data first
        self.save_to_data()

        # Current date needed for the path
        current_date = datetime.now()

        # Get the year and month for the path
        year = str(current_date.year)
        month = current_date.strftime('%B')

        # Get the invoice number
        invoice_number = get_invoice_number()

        # Get the start and end date
        start_date = date.today()
        end_date = start_date + timedelta(days=14)
        invoice_date = start_date.strftime("%d-%m-%Y")
        invoice_end_date = end_date.strftime("%d-%m-%Y")

        # Add final info to the data needed to generate invoice
        self.data['invoice_number'] = invoice_number
        self.data['invoice_date'] = invoice_date
        self.data['end_date'] = invoice_end_date

        try:
            path = f'{year}\\{month}'
            if os.path.exists(path):
                pass
            else:
                os.makedirs(path)
        
            fillpdfs.write_fillable_pdf('template.pdf', f'{path}\\{invoice_number}.pdf', self.data)
            return center(messagebox.showinfo('Success!', 'Invoice was successfully generated and saved.\nKEEP ON GOING ПУПС! <3'))
        except:
            return center(messagebox.showerror('Error', 'Something went wrong. Please contact allmighty Sadi to solve this issue'))

    # Change the invoice number
    def new_invoice_number(self):
        # Chech whether the field is empty
        if self.invoiceNumberEntry.get() == '':
            return center(messagebox.showerror('Fail', 'Please enter the invoice number')) 

        new_invoice_number = self.invoiceNumberEntry.get()

        change_invoice_number(new_invoice_number)

        return center(messagebox.showinfo('Success', 'Successfully changed the invoice number!'))

    # Functions to save the settings
    def save_settings(self):
        pass

if __name__ == '__main__':
    # Start the app
    App()