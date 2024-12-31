import tkinter as tk
import sqlite3
from tkinter import messagebox
import random as r
from homepage import Homepage

class Database:
    def __init__(self):
        self.db = sqlite3.connect('ewallet_database.db')
        self.cursor = self.db.cursor()


class Login:
    def __init__(self, login_window):


        def sign_up(e, parent_window, max_length):

            def finish():
                try:
                    try:
                        int(self.otpentry.get())
                    except Exception:
                        messagebox.showerror('Error', 'OTP Invalid')
                        return False
                    if int(self.otpentry.get()) != self.fixedotp:
                        messagebox.showwarning('Warning', 'OTP does not match')
                        return False
                    elif len(self.pwentry.get()) < 6 or len(self.pwentry.get()) > 15:
                        messagebox.showwarning('Warning', 'Please input a password with at least 6 characters and not more than 15 characters.')
                            
                    name = self.valid_name
                    age = self.valid_age
                    contact = self.valid_number
                    password = self.pwentry.get().replace(' ', '_')

                    self.cursor.execute('INSERT INTO users (name, age, contact_num, password) VALUES (?, ?, ?, ?)', (name, age, contact, password,))
                    self.db.commit()
                            
                    self.cursor.execute('INSERT INTO user_balance (user, balance) VALUES (?, ?)', (contact, 100))
                    self.db.commit()

                    messagebox.showinfo('Signup', 'Account Successfully Registered!')
                    self.login = login(self.login_window, 10)
                except Exception as e:
                    messagebox.showerror('Error', e)

            def finish_signup(parent_win, max_length, otp):

                def hover_in(e):
                    self.finishbtn.config(bg='#2cc71e')
                def hover_out(e):
                    self.finishbtn.config(bg='#46f536')

                for widget in self.inputfields.winfo_children():
                    widget.destroy()
                    
                comm = (parent_win.register(limit_character(max_length)), '%P')
                self.fixedotp = otp

                self.label = tk.Label(self.inputfields, text='Sign Up', font=('Consolas', 18), bg='#61fc56')
                self.label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

                self.otplabel = tk.Label(self.inputfields, text='Enter 4-Digit OTP:', font=('Consolas', 11), bg='#61fc56')
                self.otplabel.grid(row=1, column=0, padx=10, sticky=tk.W, pady=(35, 0))
                self.otpentry = tk.Entry(self.inputfields, font=('Consolas', 11), bd=0, bg='#61fc56', justify=tk.CENTER, validate='key', validatecommand=comm)
                self.otpentry.grid(row=1, column=1, padx=10, pady=(42, 10))
                self.otpline = tk.Frame(self.inputfields, height=1, bg='black')
                self.otpline.grid(row=1, column=1, sticky=tk.EW, pady=(50, 0), padx=10)

                self.pwlabel = tk.Label(self.inputfields, text='Enter password:', font=('Consolas', 11), bg='#61fc56')
                self.pwlabel.grid(row=2, column=0, padx=10, sticky=tk.W, pady=(19, 20))
                self.pwentry = tk.Entry(self.inputfields, font=('Consolas', 11), bd=0, bg='#61fc56', justify=tk.CENTER)
                self.pwentry.grid(row=2, column=1, padx=10)
                self.pwline = tk.Frame(self.inputfields, height=1, bg='black')
                self.pwline.grid(row=2, column=1, sticky=tk.EW, pady=(17, 0), padx=10)

                self.finishbtn = tk.Button(self.inputfields, text='Finish Signing Up', font=('Calibri', 13),
                                    bg='#46f536', bd=1, relief=tk.RIDGE, padx=13, activebackground='#61fc56', command=finish)
                self.finishbtn.grid(row=3, column=0, columnspan=2, pady=10)
                self.finishbtn.bind('<Enter>', hover_in)
                self.finishbtn.bind('<Leave>', hover_out)

            def verify_entries():
                try:
                    user = self.contactentry.get()
                    self.cursor.execute('SELECT contact_num FROM users WHERE contact_num = ?', (user,))
                    result = self.cursor.fetchone()
                    if len(user) == 0:
                        messagebox.showerror('Sign Up', 'Please input your contact number.')
                        return False
                    
                    if result == None:
                        try:
                            int(self.ageentry.get())
                        except Exception:
                            messagebox.showerror('Age Error', 'Age must be a 2 digit number not less than 18.')
                            return False
                        try:
                            int(self.contactentry.get())
                        except Exception:
                            messagebox.showerror('Contact number error', 'Contact number must be number characters only.')
                            return False

                        if self.name_entry.get().isdigit():
                            messagebox.showerror('Name Error', 'Name can\'t contain numbers.')
                            return False
                        elif len(self.name_entry.get()) <= 4:
                            messagebox.showerror('Name Error', 'Name is invalid.')
                            return False
                        elif len(self.ageentry.get()) > 2 or len(self.ageentry.get()) <= 1:
                            messagebox.showerror('Age Error', 'Age is invalid.')
                            return False
                        elif int(self.ageentry.get()) < 18:
                            messagebox.showerror('Age not eligible', 'Sorry, you\'re too young my nigga.')
                            return False

                        self.valid_name = self.name_entry.get()
                        self.valid_age = int(self.ageentry.get())
                        self.valid_number = str(self.contactentry.get())
                        regotp = r.randint(1000, 9999)
                        current_otp = regotp
                        messagebox.showinfo('One-Time PIN', f'Your new OTP is {current_otp}')
                        self.last_page = finish_signup(self.login_window, 4, current_otp)
                    else:
                        messagebox.showerror('Sign Up', 'Contact number is already registered.')
                        return False
                        
                except Exception as e:
                    messagebox.showerror('Error', e)


            def verifyhover_in(e):
                self.verifybtn.config(bg='#2cc71e')
            def verifyhover_out(e):
                self.verifybtn.config(bg='#46f536')
            
            def back_to_login(e):
                answer = messagebox.askyesno('Back to Login', 'Are you sure you want to cancel your registration?')
                if answer:
                    self.loginframe = login(self.login_window, max_length)

            for widget in self.inputfields.winfo_children():
                widget.destroy()
            
            vcmd = (parent_window.register(limit_character(max_length)), '%P')
            self.label = tk.Label(self.inputfields, text='Sign Up', font=('Consolas', 18), bg='#61fc56')
            self.label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

            self.namelabel = tk.Label(self.inputfields, text='Name:', font=('Consolas', 13), bg='#61fc56')
            self.namelabel.grid(row=1, column=0, padx=10, pady=15, sticky=tk.W)
            self.name_entry = tk.Entry(self.inputfields, font=('Consolas', 13), bd=0, bg='#61fc56', width=20, justify=tk.CENTER)
            self.name_entry.grid(row=1, column=1, padx=10, pady=15)
            self.nameline = tk.Frame(self.inputfields, height=1, bg='black')
            self.nameline.grid(row=1, column=1, sticky=tk.EW, pady=(20, 0), padx=10)

            self.agelabel = tk.Label(self.inputfields, text='Age:', font=('Consolas', 13), bg='#61fc56')
            self.agelabel.grid(row=2, column=0, padx=10, sticky=tk.W)
            self.ageentry = tk.Entry(self.inputfields, font=('Consolas', 13), bd=0, bg='#61fc56', justify=tk.CENTER)
            self.ageentry.grid(row=2, column=1, padx=10)
            self.ageline = tk.Frame(self.inputfields, height=1, bg='black')
            self.ageline.grid(row=2, column=1, sticky=tk.EW, pady=(20, 0), padx=10)

            self.contactlabel = tk.Label(self.inputfields, text='Contact:', font=('Consolas', 13), bg='#61fc56')
            self.contactlabel.grid(row=3, column=0, padx=10, sticky=tk.W)
            self.contactentry = tk.Entry(self.inputfields, font=('Consolas', 13), bd=0, bg='#61fc56', justify=tk.CENTER, validate='key', validatecommand=vcmd)
            self.contactentry.grid(row=3, column=1, padx=10, pady=15)
            self.contactline = tk.Frame(self.inputfields, height=1, bg='black')
            self.contactline.grid(row=3, column=1, sticky=tk.EW, pady=(20, 0), padx=10)

            self.verifybtn = tk.Button(self.inputfields, text='Confirm Details', font=('Calibri', 13),
                                       bg='#46f536', bd=1, relief=tk.RIDGE, padx=13, activebackground='#61fc56', command=verify_entries)
            self.verifybtn.grid(row=4, column=0, columnspan=2, pady=10)
            self.verifybtn.bind('<Enter>', verifyhover_in)
            self.verifybtn.bind('<Leave>', verifyhover_out)

            self.back = tk.Label(self.inputfields, text='Back to login', font=('Poppins', 10), bg='#61fc56', cursor='hand2')
            self.back.grid(row=5, column=0, columnspan=2)
            self.back.bind('<Button-1>', back_to_login)

        def generate_otp(parent_win, max_length, user_contact):
            try:
                self.cursor.execute('SELECT contact_num FROM users WHERE contact_num = ?', (user_contact,))
                user = self.cursor.fetchone()

                if user != None:
                    self.otp = r.randint(1000, 9999)
                    self.current_otp = self.otp
                    messagebox.showinfo('One-Time PIN', f'Your OTP is {self.current_otp}')

                    def login_win():
                        def homepage():
                            self.login_window.destroy()
                            self.home_page = Homepage(user_contact)

                        try:
                            self.cursor.execute('SELECT password FROM users WHERE contact_num = ?', user)
                            result = self.cursor.fetchone()
                            user_password = result[0]
                            if self.pwentry.get() == user_password:
                                try:
                                    int(self.otpentry.get())
                                except Exception:
                                    messagebox.showwarning('Login', 'OTP is Invalid.')
                                    return False
                                if int(self.otpentry.get()) != self.current_otp:
                                    messagebox.showwarning('Login', 'Incorrect OTP. Please try again.')
                                    print(type(self.otpentry.get()))
                                    return False
                                else:
                                    messagebox.showinfo('Login', 'Login Successful.')
                                    self.homepage = homepage()
                            else:
                                messagebox.showwarning('Login', 'Incorrect password.')
                                return False
                        except Exception as e:
                            print(e)
                            return False

                    def hover_in(e):
                        self.loginbtn.config(bg='#2cc71e')
                    def hover_out(e):
                        self.loginbtn.config(bg='#46f536')

                    def back_to_login(parent, max_length):
                        self.back = login(parent, max_length)
                    
                    comm = (parent_win.register(limit_character(max_length)), '%P')

                    for widget in self.inputfields.winfo_children():
                        widget.destroy()
                    
                    self.label = tk.Label(self.inputfields, text='Login', font=('Consolas', 18), bg='#61fc56')
                    self.label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

                    self.otplabel = tk.Label(self.inputfields, text='Enter 4-Digit OTP:', font=('Consolas', 11), bg='#61fc56')
                    self.otplabel.grid(row=1, column=0, padx=10, sticky=tk.W, pady=(35, 0))
                    self.otpentry = tk.Entry(self.inputfields, font=('Consolas', 11), bd=0, bg='#61fc56', justify=tk.CENTER, validate='key', validatecommand=comm)
                    self.otpentry.grid(row=1, column=1, padx=10, pady=(42, 10))
                    self.otpline = tk.Frame(self.inputfields, height=1, bg='black')
                    self.otpline.grid(row=1, column=1, sticky=tk.EW, pady=(50, 0), padx=10)

                    self.pwlabel = tk.Label(self.inputfields, text='Enter password:', font=('Consolas', 11), bg='#61fc56')
                    self.pwlabel.grid(row=2, column=0, padx=10, sticky=tk.W, pady=(19, 20))
                    self.pwentry = tk.Entry(self.inputfields, font=('Consolas', 11), bd=0, bg='#61fc56', justify=tk.CENTER)
                    self.pwentry.grid(row=2, column=1, padx=10)
                    self.pwline = tk.Frame(self.inputfields, height=1, bg='black')
                    self.pwline.grid(row=2, column=1, sticky=tk.EW, pady=(17, 0), padx=10)

                    self.loginbtn = tk.Button(self.inputfields, text='Log in', font=('Calibri', 13),
                                            bg='#46f536', bd=1, relief=tk.RIDGE, padx=13, activebackground='#61fc56', command=login_win)
                    self.loginbtn.grid(row=3, column=0, pady=10)
                    self.loginbtn.bind('<Enter>', hover_in)
                    self.loginbtn.bind('<Leave>', hover_out)

                    self.regenbtn = tk.Button(self.inputfields, text='Resend OTP', font=('Calibri', 13),
                                            bg='#46f536', bd=1, relief=tk.RIDGE, padx=13, activebackground='#61fc56', command=lambda :generate_otp(self.login_window, 10, user_contact))
                    self.regenbtn.grid(row=3, column=1, pady=10)
                    self.backbtn = tk.Button(self.inputfields, text='Back to login', font=('Calibri', 13),
                                            bg='#46f536', bd=1, relief=tk.RIDGE, padx=13, activebackground='#61fc56', command=lambda :back_to_login(self.login_window, 10))
                    self.backbtn.grid(row=4, column=0, columnspan=2, pady=10)
                else:
                    messagebox.showerror('Login', 'Account number doesn\'t exist.')
                    return False
            except Exception as e:
                messagebox.showerror('Error', e)
            

        def login(parent, max_length):
            vcmd = (parent.register(limit_character(max_length)), '%P')

            def hover_in(e):
                self.signup_label.config(fg='#FFFFFF')
            def hover_out(e):
                self.signup_label.config(fg='black')

            def otphover_in(e):
                self.otpbtn.config(bg='#2cc71e')
            def otphover_out(e):
                self.otpbtn.config(bg='#46f536')

            for widget in self.inputfields.winfo_children():
                widget.destroy()

            self.numLabel = tk.Label(self.inputfields, text='Enter your number below for verification',
                                    font=('Poppins', 13), bg='#61fc56')
            self.numLabel.grid(row=0, column=0, padx=25, pady=(20, 0))
            
            self.entry = tk.Frame(self.inputfields, width=300, height=75, bg='#61fc56')
            self.entry.grid(row=1, column=0, pady=(30, 0))

            self.label = tk.Label(self.entry, text='+63', font=('Consolas', 13, 'underline'), bg='#61fc56')
            self.label.grid(row=0, column=0, sticky=tk.E, pady=(15, 0))
            self.numEntry = tk.Entry(self.entry, font=('Consolas', 13), bg='#61fc56', bd=0, validate='key', validatecommand=vcmd, justify=tk.CENTER)
            self.numEntry.grid(row=0, column=1, sticky=tk.W, padx=10, pady=(16,0))
            self.hline = tk.Frame(self.entry, height=1, bg='black')
            self.hline.grid(row=0, column=1, sticky=tk.EW, pady=(34, 0), padx=10)

            self.otpbtn = tk.Button(self.entry, text='Get OTP', font=('Poppins', 13),
                                    padx=5, bd=1, relief=tk.RIDGE, bg='#46f536',
                                    activebackground='#61fc56', command=lambda: generate_otp(self.login_window, 4, self.numEntry.get()))
            self.otpbtn.grid(row=1, column=0, columnspan=2, pady=(25, 5))
            self.otpbtn.bind('<Enter>', otphover_in)
            self.otpbtn.bind('<Leave>', otphover_out)

            self.signup_label = tk.Label(self.entry, text='Don\'t have an account? Click here!', font=('Poppins', 10), bg='#61fc56', cursor='hand2')
            self.signup_label.grid(row=2, column=0, columnspan=2)
            self.signup_label.bind('<Button-1>', lambda event, win = self.login_window: sign_up(event, win, 10))
            self.signup_label.bind('<Enter>', hover_in)
            self.signup_label.bind('<Leave>', hover_out)

        def limit_character(max_length):
            def checklen(new_value):
                return len(new_value) <= max_length
            return checklen


        self.login_window = login_window
        self.login_window.title('My E-Wallet App -- Login')
        self.login_window.geometry('450x620+550+80')
        self.login_window.resizable(0, 0)
        self.login_window.config(bg='#61fc56')
        self.database = Database()
        self.db = self.database.db
        self.cursor = self.database.cursor
        self.icon_path = tk.PhotoImage(file='wallet.png')
        self.icon = self.icon_path
        self.login_window.iconphoto(True, self.icon)

        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS users (
                            name TEXT NOT NULL,
                            age INTEGER NOT NULL,
                            contact_num TEXT PRIMARY KEY,
                            password TEXT NOT NULL)
                            """)
        self.db.commit()

        self.logo_path = tk.PhotoImage(file='wallet.png')
        self.logo = self.logo_path

        self.upper_logo = tk.Label(self.login_window, text='My E-Wallet App',
                                   image=self.logo, bg='#61fc56', font=('Times New Roman', 20),
                                   compound=tk.TOP)
        self.upper_logo.pack(anchor=tk.CENTER, pady=(75, 10))
        self.inputfields = tk.Frame(self.login_window, width=400, height=275, bg='#61fc56', pady=10)
        self.inputfields.pack_propagate(False)
        self.inputfields.pack(anchor=tk.CENTER, pady=10)
        self.loginframe = login(self.login_window, 10)


if __name__ == '__main__':
    win = tk.Tk()
    app = Login(win)
    win.mainloop()