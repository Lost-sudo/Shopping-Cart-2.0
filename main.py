import datetime
import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import qrcode
from PIL import ImageTk


class MainApp:
    def __init__(self, master):
        self.master = master

        master.title("JUAN Shopping Cart")
        master.geometry("800x500")
        master.iconbitmap("mbrilogin_99599.ico")

        self.login = None
        self.register = None

        self.create_login_frame()

    def create_login_frame(self):
        self.login = LoginApp(self.master, self)
        self.login.pack(fill='both', expand=True)

    def open_register_frame(self):
        if self.login:
            self.login.pack_forget()
        self.register = Register(self.master, self)
        self.register.pack(fill='both', expand=True)

    def open_login_frame(self):
        if self.register:
            self.register.pack_forget()
        self.login = LoginApp(self.master, self)
        self.login.pack(fill='both', expand=True)


class LoginApp(tk.Frame):
    def __init__(self, master, main_app):
        super().__init__(master)

        self.main_app = main_app

        self.border_frame = tk.Frame(master=self.master, width=320, height=360, bd=5, relief=tk.RIDGE)
        self.border_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.login_label = tk.Label(master=self.border_frame, text="Login to your account",
                                    font=("times new roman", 20, "bold"))
        self.login_label.place(x=20, y=45)

        self.username_label = tk.Label(master=self.border_frame, text="Username", font=("times new roman", 15))
        self.username_label.place(x=20, y=100)

        self.username_entry = tk.Entry(master=self.border_frame, font=("times new roman", 15), bd=5)
        self.username_entry.place(x=20, y=125)

        self.password_label = tk.Label(master=self.border_frame, text="Password", font=("times new roman", 15))
        self.password_label.place(x=20, y=160)

        self.password_entry = tk.Entry(master=self.border_frame, font=("times new roman", 15), bd=5, show="*")
        self.password_entry.place(x=20, y=185)

        self.login_btn = tk.Button(master=self.border_frame, text="Login", border=4, bg="#4f90ff",
                                   command=self.user_login)
        self.login_btn.place(x=20, y=225)

        self.register_btn = tk.Label(master=self.border_frame, text="Don't have an account? Click here!", fg="gray")
        self.register_btn.place(x=20, y=265)
        self.register_btn.bind("<Button-1>", self.open_register_frame)

    def open_register_frame(self, event):
        self.main_app.open_register_frame()

    def user_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = sqlite3.connect("shoppingcart.db")

        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE username= ? AND password = ?", (username, password))

        user = c.fetchone()

        if user:
            self.master.withdraw()
            ShoppingCart(self.master, self)
        else:
            messagebox.showerror("ERROR", "Invalid username or password")


class Register(tk.Frame):
    def __init__(self, master, main_app):
        super().__init__(master)

        self.main_app = main_app
        self.border_frame = tk.Frame(master=self.master, width=320, height=360, relief=tk.RIDGE, bd=5)
        self.border_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.registration_label = tk.Label(master=self.border_frame, text="Registration",
                                           font=("times new roman", 20, "bold"))
        self.registration_label.place(x=40, y=45)

        self.username_label = tk.Label(master=self.border_frame, text="Username", font=("times new roman", 12))
        self.username_label.place(x=40, y=100)

        self.username_entry = tk.Entry(master=self.border_frame, font=("times new roman", 12))
        self.username_entry.place(x=40, y=125)

        self.password_label = tk.Label(master=self.border_frame, text="Password", font=("times new roman", 12))
        self.password_label.place(x=40, y=160)

        self.password_entry = tk.Entry(master=self.border_frame, font=("times new roman", 12))
        self.password_entry.place(x=40, y=185)

        self.password_label2 = tk.Label(master=self.border_frame, text="Confirm password", font=("times new roman", 12))
        self.password_label2.place(x=40, y=210)

        self.password_entry2 = tk.Entry(master=self.border_frame, font=("times new roman", 12))
        self.password_entry2.place(x=40, y=235)

        self.registration_btn = tk.Button(master=self.border_frame, text="Register", border=4,
                                          command=self.register_user)
        self.registration_btn.place(x=40, y=270)

        self.login_btn = tk.Label(master=self.border_frame, text="Already have an account? Login here!")
        self.login_btn.place(x=40, y=310)
        self.login_btn.bind("<Button-1>", self.open_login_frame)

    def open_login_frame(self, event):
        self.main_app.open_login_frame()

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        password2 = self.password_entry2.get()

        if password != password2:
            messagebox.showerror("ERROR", "Password do not match")
        else:
            if username and password:
                try:

                    conn = sqlite3.connect("shoppingcart.db")

                    c = conn.cursor()

                    shoppingcart = f"user_{username}"

                    c.execute("INSERT INTO users (username, password, shoppingcart) VALUES (?, ?, ?)",
                              (username, password, shoppingcart))

                    conn.commit()
                    conn.close()

                    messagebox.showinfo("SUCCESS", "Registered successfully")

                except sqlite3.Error as e:
                    messagebox.showerror("ERROR", f"Database error: {e}")
            else:
                messagebox.showerror("ERROR", "Please fill out the form")


class ShoppingCart(tk.Toplevel):
    def __init__(self, master, main_app):
        super().__init__(master)
        self.receipts = None
        self.cart = None
        self.main_app = main_app

        self.iconbitmap("shopping-cart_icon-icons.com_72552.ico")

        self.geometry("1000x1000")

        self.header_frame = tk.Frame(master=self, height=70, bd=10, bg="#000", relief=tk.RIDGE)
        self.header_frame.pack(fill='x', side='top')

        self.header_label = tk.Label(master=self.header_frame, text="JUAN SHOPPING CART",
                                     font=('times new roman', 20, 'bold'))
        self.header_label.pack(fill='x')

        self.bottom_frame = tk.Frame(master=self, height=200, bd=10, bg="#000", relief=tk.RIDGE)
        self.bottom_frame.pack(fill='x', side='bottom')

        self.place_order_btn = tk.Button(master=self.bottom_frame, text="Place order",
                                         font=("times new roman", 15, 'bold'), bd=10, command=self.place_order)
        self.place_order_btn.pack(fill='x', side='left', expand=True)

        self.add_to_cart_btn = tk.Button(master=self.bottom_frame, text="Add to cart",
                                         font=("times new roman", 15, 'bold'), bd=10, command=self.add_to_cart)
        self.add_to_cart_btn.pack(fill='x', side='left', expand=True)

        self.delete_btn = tk.Button(master=self.bottom_frame, text="Delete item", font=("times new roman", 15, 'bold'),
                                    bd=10, command=self.delete_item)
        self.delete_btn.pack(fill='x', side='left', expand=True)

        self.clear_btn = tk.Button(master=self.bottom_frame, text="Clear cart", font=('times new roman', 15, 'bold'),
                                   bd=10, command=self.clear_cart)
        self.clear_btn.pack(fill='x', side='left', expand=True)

        self.print_receipt_btn = tk.Button(master=self.bottom_frame, text="Print receipt",
                                           font=("times new roman", 15, 'bold'),
                                           bd=10, command=self.print_receipt)
        self.print_receipt_btn.pack(fill='x', side='left', expand=True)

        self.setting_btn = tk.Button(master=self.bottom_frame, text="Settings", font=("times new roman", 15, 'bold'),
                                     bd=10, command=self.setting_window)
        self.setting_btn.pack(fill='x', side='left', expand=True)

        self.products = Products(master=self, main_app=self.main_app, cart=self.cart)
        self.create_widgets()

    def clear_cart(self):
        self.cart.cart_treeview.delete(*self.cart.cart_treeview.get_children())
        self.cart.total_price = 0.0
        self.cart.update_total()

    def print_receipt(self):
        if self.receipts:
            self.receipts.print_receipt()
        else:
            messagebox.showerror("Error", "Receipts not available. Please add items to the cart.")

    def create_widgets(self):
        self.frame = tk.Frame(master=self, bd=10)
        self.frame.pack(fill='both', expand=True, side='left')
        self.cart = Cart(master=self.frame, main_app=self.main_app)
        self.receipts = Receipts(master=self.frame, main_app=self.main_app)

    def setting_window(self):
        settings_window = tk.Toplevel(self)
        settings_window.title("Settings")
        settings_window.geometry("300x200")
        settings_window.iconbitmap("1904675-configuration-edit-gear-options-preferences-setting-settings_122525.ico")

        history = tk.Button(settings_window, text="Purchase History", font=("times new roman", 15, 'bold'), bd=5,
                            relief=tk.RIDGE, command=self.purchase_history)
        history.pack(fill='x', pady=10, padx=10)

        exit_app = tk.Button(settings_window, text="Exit", font=("times new roman", 15, 'bold'), bd=5, relief=tk.RIDGE,
                             command=self.exit_application)
        exit_app.pack(fill='x', pady=10, padx=10)

    def exit_application(self):
        self.master.destroy()

    def purchase_history(self):
        purchase_history = tk.Toplevel(self)
        purchase_history.title("Purchase History")
        purchase_history.geometry("600x500")

        purchase_history.iconbitmap("-history_89998.ico")

        items_treeview = ttk.Treeview(master=purchase_history, columns=("Item", "Price", "Purchase Time"),
                                      show="headings")
        items_treeview.heading("Item", text="Item")
        items_treeview.heading("Price", text="Price")
        items_treeview.heading("Purchase Time", text="Purchase Time")
        items_treeview.pack(fill='both', expand=True)

        conn = sqlite3.connect("shoppingcart.db")
        c = conn.cursor()

        c.execute("SELECT item_name, item_price, sold_time FROM purchase_history")
        items = c.fetchall()

        for item in items:
            item_name = item[0]
            item_price = item[1].replace('₱', '')
            sold_time = item[2]

            items_treeview.insert("", tk.END, values=(item_name, f"₱{float(item_price):.2f}", sold_time))

        conn.close()

    def add_to_cart(self):
        selected_items = self.products.items_treeview.selection()
        if not selected_items:
            messagebox.showerror("Error", "Please select an item.")
            return

        for item_id in selected_items:
            item_details = self.products.items_treeview.item(item_id)
            item_name = item_details['values'][0]
            item_price = item_details['values'][1]
            self.cart.add_item(item_name, item_price)

    def delete_item(self):
        selected_item = self.cart.cart_treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an item to delete.")
            return

        for item_id in selected_item:
            item_details = self.cart.cart_treeview.item(item_id)
            item_price = item_details['values'][1]
            self.cart.cart_treeview.delete(item_id)
            self.cart.total_price -= float(item_price[1:])
            self.cart.update_total()

    def place_order(self):
        self.open_payment_window()

    def open_payment_window(self):
        payment_window = tk.Toplevel()
        payment_window.title("Payment mode")
        payment_window.geometry("300x200")

        selected_payment_method = tk.StringVar()

        def checkout():
            mode = selected_payment_method.get()

            if mode == "Gcash":
                self.open_gcash_payment_method()
                payment_window.destroy()
            if mode == "Cash":
                self.open_cash_payment_method()
                payment_window.destroy()

        payment_method = ["Gcash", "Cash"]

        for mode in payment_method:
            payment_mode = tk.Radiobutton(payment_window, text=mode, variable=selected_payment_method, value=mode,
                                          pady=15)
            payment_mode.pack()

        confirm_button = tk.Button(payment_window, text="Confirm", command=checkout)
        confirm_button.pack()

    def open_cash_payment_method(self):
        cash_window = tk.Toplevel(self)
        cash_window.title("Pay with cash")
        cash_window.geometry("300x200")

        total_label = tk.Label(cash_window, text=f"Total price: ₱{self.cart.total_price:.2f}",
                               font=("times new roman", 20, 'bold'))
        total_label.pack()

        amount_label = tk.Label(cash_window, text="Enter amount paid: ", font=("times new roman", 15))
        amount_label.pack()

        amount_entry = tk.Entry(cash_window, font=("times new roman", 15))
        amount_entry.pack()

        def process_cash_payment():
            amount_paid = float(amount_entry.get())
            if amount_paid < self.cart.total_price:
                messagebox.showerror("Error", "Amount paid is less than total price.")
            else:
                change = amount_paid - self.cart.total_price
                items_sold = []
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                for item_id in self.cart.cart_treeview.get_children():
                    item_details = self.cart.cart_treeview.item(item_id)
                    item_name = item_details['values'][0]
                    item_price = item_details['values'][1]
                    items_sold.append((item_name, item_price, current_time))

                if not items_sold:
                    messagebox.showerror("ERROR", "Your cart is empty. Please add items before you place order.")
                    return

                conn = sqlite3.connect("shoppingcart.db")
                c = conn.cursor()

                for item_name, item_price, sold_time in items_sold:
                    c.execute("INSERT INTO purchase_history (item_name, item_price, sold_time) VALUES (?, ?, ?)",
                              (item_name, item_price, sold_time))
                    self.receipts.add_item(item_name, item_price)

                conn.commit()
                conn.close()

                self.cart.cart_treeview.delete(*self.cart.cart_treeview.get_children())
                self.cart.total_price = 0.0
                self.cart.update_total()

                messagebox.showinfo("Success", f"Payment successful!\nChange: ₱{change:.2f}")
                cash_window.destroy()

        confirm_button = tk.Button(cash_window, text="Confirm Payment", command=process_cash_payment)
        confirm_button.pack()

    def open_gcash_payment_method(self):
        gcash_window = tk.Toplevel(self)
        gcash_window.title("Gcash payment")
        gcash_window.geometry("300x400")

        total_label = tk.Label(gcash_window, text=f"Total price: ₱{self.cart.total_price:.2f}",
                               font=("times new roman", 20, 'bold'))
        total_label.pack()

        phone_number = "09053897048"
        qr_code_img = self.generate_qr_code(phone_number)

        qr_code_label = tk.Label(gcash_window, image=qr_code_img)
        qr_code_label.image = qr_code_img
        qr_code_label.pack()

        def confirm_payment():
            items_sold = []
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for item_id in self.cart.cart_treeview.get_children():
                item_details = self.cart.cart_treeview.item(item_id)
                item_name = item_details['values'][0]
                item_price = item_details['values'][1]
                items_sold.append((item_name, item_price, current_time))

            if not items_sold:
                messagebox.showerror("ERROR", "Your cart is empty. Please add items before you place order.")
                return

            conn = sqlite3.connect("shoppingcart.db")
            c = conn.cursor()

            for item_name, item_price, sold_time in items_sold:
                c.execute("INSERT INTO purchase_history (item_name, item_price, sold_time) VALUES (?, ?, ?)",
                          (item_name, item_price, sold_time))
                self.receipts.add_item(item_name, item_price)

            conn.commit()
            conn.close()

            self.cart.cart_treeview.delete(*self.cart.cart_treeview.get_children())
            self.cart.total_price = 0.0
            self.cart.update_total()
            messagebox.showinfo("Success", f"Payment successful!")
            gcash_window.destroy()

        confirm_btn = tk.Button(gcash_window, text="Done payment", command=confirm_payment)
        confirm_btn.pack()

    def confirm_payment(self):
        items_sold = []
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for item_id in self.cart.cart_treeview.get_children():
            item_details = self.cart.cart_treeview.item(item_id)
            item_name = item_details['values'][0]
            item_price = item_details['values'][1]
            items_sold.append((item_name, item_price, current_time))

        if not items_sold:
            messagebox.showerror("ERROR", "Your cart is empty. Please add items before you place order.")
            return

        conn = sqlite3.connect("shoppingcart.db")
        c = conn.cursor()

        for item_name, item_price, sold_time in items_sold:
            c.execute("INSERT INTO purchase_history (item_name, item_price, sold_time) VALUES (?, ?, ?)",
                      (item_name, item_price, sold_time))
            self.receipts.add_item(item_name, item_price)

        conn.commit()
        conn.close()

        self.cart.cart_treeview.delete(*self.cart.cart_treeview.get_children())
        self.cart.total_price = 0.0
        self.cart.update_total()
        messagebox.showinfo("Success", f"Payment successful!")
        self.gcash_window.destroy()

    def generate_qr_code(self, data):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        return self.pil_to_photoimage(img)

    def pil_to_photoimage(self, pil_img):
        return ImageTk.PhotoImage(pil_img)


class Products(tk.Frame):
    def __init__(self, master, main_app, cart):
        super().__init__(master)

        self.main_app = main_app
        self.cart = cart

        self.products_frame = tk.Frame(master=self.master, height=700, bd=10, relief=tk.RIDGE)
        self.products_frame.pack(fill='both', expand=True, side='left')

        self.products_label = tk.Label(master=self.products_frame, text="PRODUCTS",
                                       font=('times new roman', 15, 'bold'))
        self.products_label.pack(fill='x')

        self.search_entry = tk.Entry(master=self.products_frame, bd=10, font=("times new roman", 15))
        self.search_entry.pack(side='top', fill='x')

        self.search_btn = tk.Button(master=self.products_frame, bd=5, text="Search", font=("times new roman", 15),
                                    command=self.search_items)
        self.search_btn.pack(side='top', fill='x', pady=10)

        self.items_treeview = ttk.Treeview(master=self.products_frame, columns=("Item", "Price"), show="headings")
        self.items_treeview.heading("Item", text="Item")
        self.items_treeview.heading("Price", text="Price")
        self.items_treeview.pack(fill='both', expand=True)

        self.populate_items_treeview()

    def populate_items_treeview(self):
        conn = sqlite3.connect("shoppingcart.db")
        c = conn.cursor()

        c.execute("SELECT item_name, item_price FROM items")
        items = c.fetchall()

        for item in items:
            item_name = item[0]
            item_price = f"₱{float(item[1]):.2f}"

            self.items_treeview.insert("", tk.END, values=(item_name, item_price))

        conn.close()

    def search_items(self):
        search_query = self.search_entry.get().strip().lower()
        conn = sqlite3.connect("shoppingcart.db")
        c = conn.cursor()

        c.execute("SELECT item_name, item_price FROM items WHERE lower(item_name) LIKE ?", ('%' + search_query + '%',))
        items = c.fetchall()

        for item in self.items_treeview.get_children():
            self.items_treeview.delete(item)

        for item in items:
            item_name = item[0]
            item_price = f"₱{float(item[1]):.2f}"
            self.items_treeview.insert("", tk.END, values=(item_name, item_price))

        conn.close()

    def get_selected_item(self):
        selected_items = []
        for item_id in self.items_treeview.selection():
            item_details = self.items_treeview.item(item_id)
            item_name = item_details['values'][0]
            item_price = item_details['values'][1]
            selected_items.append((item_name, item_price))
        return selected_items


class Cart(tk.Frame):
    def __init__(self, master, main_app):
        super().__init__(master)

        self.main_app = main_app

        self.cart_frame = tk.Frame(master=self.master, height=700, bd=10, relief=tk.RIDGE)
        self.cart_frame.pack(fill='both', expand=True, side='top')

        self.cart_label = tk.Label(master=self.cart_frame, text="CART", font=("times new roman", 15, 'bold'))
        self.cart_label.pack(fill='x')

        self.cart_treeview = ttk.Treeview(master=self.cart_frame, columns=("Item", "Price"), show="headings")
        self.cart_treeview.heading("Item", text="Item")
        self.cart_treeview.heading("Price", text="Price")
        self.cart_treeview.pack(fill='both', expand=True)

        self.total_label = tk.Label(master=self.cart_frame, text="", font=("times new roman", 15, 'bold'))
        self.total_label.pack(fill='x')

        self.total_price = 0.0

    def add_item(self, item_name, item_price):
        self.cart_treeview.insert("", tk.END, values=(item_name, item_price))
        self.total_price += float(item_price[1:])
        self.update_total()

    def update_total(self):
        self.total_label.configure(text=f"Total Price: ₱{self.total_price:.2f}")


class Receipts(tk.Frame):
    def __init__(self, master, main_app):
        super().__init__(master)

        self.main_app = main_app

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.receipt_frame = tk.Frame(master=self.master, height=700, bd=10, relief=tk.RIDGE)
        self.receipt_frame.pack(fill='both', expand=True, side='bottom')

        self.shop_name = tk.Label(master=self.receipt_frame, text="Juan Shopping Cart",
                                  font=('times new roman', 15, 'bold'))
        self.shop_name.pack(fill='x')

        self.shop_address = tk.Label(master=self.receipt_frame, text="P2 Magosilom, Cantilan, SDS",
                                     font=("times new roman", 10))
        self.shop_address.pack(fill='x')

        self.transaction_date = tk.Label(master=self.receipt_frame, text=f"{current_time}",
                                         font=('times new roman', 10))
        self.transaction_date.pack(fill='x')

        self.receipt_label = tk.Label(master=self.receipt_frame, text="RECEIPT", font=('times new roman', 15, 'bold'))
        self.receipt_label.pack(fill='x')

        self.receipt_treeview = ttk.Treeview(master=self.receipt_frame, columns=("Item", "Price"), show="headings")
        self.receipt_treeview.heading("Item", text="Item")
        self.receipt_treeview.heading("Price", text="Price")
        self.receipt_treeview.pack(fill='both', expand=True)

        self.total_label = tk.Label(master=self.receipt_frame, text="", font=("times new roman", 15, 'bold'))
        self.total_label.pack(fill='x')

        self.total_price = 0.0

    def add_item(self, item_name, item_price):
        self.receipt_treeview.insert("", tk.END, values=(item_name, item_price))
        self.total_price += float(item_price[1:])
        self.update_total()

    def update_total(self):
        self.total_label.configure(text=f'Total Price: {self.total_price:.2f}')

    def get_receipt_contents(self):
        receipt_content = f"Juan Shopping Cart\n"
        receipt_content += f"Transaction Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        receipt_content += "-------------------------\n"
        for item_id in self.receipt_treeview.get_children():
            item_details = self.receipt_treeview.item(item_id)
            item_name = item_details['values'][0]
            item_price = item_details['values'][1]
            receipt_content += f"{item_name}: {item_price}\n"
        receipt_content += "-------------------------\n"
        receipt_content += f"Total Price: ₱{self.total_price:.2f}\n"
        return receipt_content

    def print_receipt(self):
        receipt_contents = self.get_receipt_contents()
        print(receipt_contents)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
