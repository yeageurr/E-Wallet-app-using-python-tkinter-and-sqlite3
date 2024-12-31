import tkinter as tk
from tkinter import messagebox
import sqlite3


class Connection:
    def __init__(self):
        self.db = sqlite3.connect('ewallet_database.db')
        self.cursor = self.db.cursor()


class Homepage:
    def __init__(self, user_num):
        self.user = user_num
        self.database = Connection()
        self.db = self.database.db
        self.cursor = self.database.cursor

        def home_page():
            self.send_path = tk.PhotoImage(file='send.png')
            self.empty_path = tk.PhotoImage(file='checklist.png')
            self.empty_icon = self.empty_path
            self.send_icon = self.send_path

            def send_balance(bal):

                def sendto(userbalance):
                    
                    number = self.recipiententry.get()
                    userbalance = int(userbalance)
                    if len(number) != 10:
                        self.warninglabel.config(text='Invalid recipient number.')
                        return False
                    if len(self.amountentry.get()) == 0:
                        self.warninglabel.config(text='Invalid amount.')
                        return False
                    else:
                        try:
                            amount = int(self.amountentry.get())
                        except Exception as e:
                            self.warninglabel.config(text='Invalid amount.')
                            return False
                    try:
                        if number == self.user:
                            self.warninglabel.config(text='You cannot send to your self.')
                            return False
                    except Exception as e:
                        print(e)
                    
                    try:
                        self.cursor.execute('SELECT * FROM users WHERE contact_num = ?', (number,))
                        result = self.cursor.fetchall()
                        if result[0] == self.user:
                            self.warninglabel.config(text='Invalid amount.')
                            return False
                        else:
                            if result != None:
                                try:
                                    self.cursor.execute('SELECT balance FROM user_balance WHERE user = ?', (number,))
                                    user = self.cursor.fetchone()
                                    balance = user[0]
                                    try:
                                        if userbalance >= amount:
                                            balance += amount
                                            self.cursor.execute('''UPDATE user_balance
                                                                SET balance = ?
                                                                WHERE user = ?''', (balance, number, ))
                                            self.db.commit()

                                            self.cursor.execute('SELECT balance FROM user_balance WHERE user = ?', (self.user,))
                                            currbal = self.cursor.fetchone()
                                            mybal = currbal[0]

                                            mybal -= amount
                                            self.cursor.execute('''UPDATE user_balance
                                                                SET balance = ?
                                                                WHERE user = ?''', (mybal, self.user, ))
                                            self.db.commit()

                                            self.cursor.execute('''INSERT INTO transactions (user, transaction_type, amount, recipient)
                                                               VALUES (?, ?, ?, ?)''', (self.user, 'Payment', amount, number,))
                                            self.db.commit()

                                            self.cursor.execute('''INSERT INTO transactions (user, transaction_type, amount, recipient)
                                                               VALUES (?, ?, ?, ?)''', (number, 'Money Recieved', amount, self.user,))
                                            self.db.commit()

                                            messagebox.showinfo('Send Money', 'Sent Successfuly! Thank you for using My E-Wallet App!')
                                            self.refresh = home_page()
                                        else:
                                            self.warninglabel.config(text='Insufficient Balance')
                                    except Exception as e:
                                        print(e)
                                        return False
                                except Exception as e:
                                    print(e)
                                    return False
                            else:
                                self.warninglabel.config(text='User not found.')
                                return False
                    except Exception as e:
                        print(e)
                        return False

                self.curr_bal = bal
                self.send_window = tk.Toplevel()
                self.send_window.title('Send Money')
                self.send_window.geometry('450x375+550+200')
                self.send_window.resizable(0, 0)
                self.send_window.config(bg='#e3e6e3')

                self.balance = tk.Frame(self.send_window, width=400, height=85, pady=8, padx=13, bg='#e3e6e3')
                self.balance.pack_propagate(False)
                self.balance.pack(anchor=tk.CENTER, pady=(25, 0))

                self.mybalance = tk.Label(self.balance, text=f'$ {bal:.2f}', font=('Arial Black', 20), bg='#e3e6e3')
                self.mybalance.pack(pady=(10, 0))
                self.balancelabel = tk.Label(self.balance, text='Your Balance', font=('Calibri Light', 8, 'bold'), bg='#e3e6e3')
                self.balancelabel.pack()

                self.sendframe = tk.Frame(self.send_window, width=300, height=215, bg='#e3e6e3')
                self.sendframe.pack(pady=45)

                self.recipientlabel = tk.Label(self.sendframe, text='Send to:', font=('Calibri Light', 13), justify=tk.LEFT, bg='#e3e6e3')
                self.recipientlabel.grid(row=0, column=0, sticky=tk.W, padx=(0, 15))
                self.recipiententry = tk.Entry(self.sendframe, font=('Calibri Light', 13), justify=tk.LEFT,
                                               bd=1, relief=tk.RIDGE, bg='#FFFFFF', width=15)
                self.recipiententry.grid(row=0, column=1, sticky=tk.W)
                self.amountlabel = tk.Label(self.sendframe, text='Enter amount:', font=('Calibri Light', 13), justify=tk.LEFT, bg='#e3e6e3')
                self.amountlabel.grid(row=1, column=0, sticky=tk.W, padx=(0, 15))
                self.amountentry = tk.Entry(self.sendframe, font=('Calibri Light', 13), justify=tk.LEFT,
                                               bd=1, relief=tk.RIDGE, bg='#FFFFFF',
                                               width=15)
                self.amountentry.grid(row=1, column=1, sticky=tk.W)

                self.send_btn = tk.Button(self.sendframe, text='Send',
                                          image=self.send_icon, compound=tk.LEFT, font=('Poppins', 8), padx=10, pady=3,
                                          bd=0, bg='#04063d', fg='#FFFFFF', activebackground='#FFFFFF', activeforeground='#04063d',
                                          command=lambda: sendto(self.curr_bal))
                self.send_btn.grid(row=2, column=0, columnspan=2, pady=(15, 10))
                self.warninglabel = tk.Label(self.sendframe, text='', fg='red', font=('Calibri Light', 13), bg='#e3e6e3')
                self.warninglabel.grid(row=3, column=0, columnspan=2)
                
            try:
                self.cursor.execute('SELECT balance FROM user_balance WHERE user = ?', (self.user,))
                result = self.cursor.fetchone()
                self.current_balance = result[0]
            except Exception as e:
                messagebox.showerror('fetch balance', e)

            for widget in self.main_frame.winfo_children():
                widget.destroy()

            self.homepage.title('My E-Wallet App -- Home')
            self.balance = tk.Frame(self.main_frame, width=375, height=85, pady=8, padx=13)
            self.balance.pack_propagate(False)
            self.balance.pack(anchor=tk.CENTER, pady=(25, 0))

            self.mybalance = tk.Label(self.balance, text=f'$ {self.current_balance:.2f}', font=('Arial Black', 20))
            self.mybalance.pack(pady=(10, 0))
            self.balancelabel = tk.Label(self.balance, text='Your Balance', font=('Calibri Light', 8, 'bold'))
            self.balancelabel.pack()
            self.hline1 = tk.Frame(self.main_frame, height=1, bg='#000000', width=375)
            self.hline1.pack(pady=25)

            self.actionsframe = tk.Frame(self.main_frame, width=375, bg='#f7f7fa')
            self.actionsframe.pack()
            self.sendbtn = tk.Button(self.actionsframe, text='Send Money',
                                     image=self.send_icon, compound=tk.LEFT, font=('Poppins', 8), padx=10, pady=3,
                                     bd=0, bg='#04063d', fg='#FFFFFF', activebackground='#FFFFFF', activeforeground='#04063d',
                                     command=lambda: send_balance(self.current_balance))
            self.sendbtn.pack(anchor=tk.NW)
            self.hline2 = tk.Frame(self.main_frame, height=1, bg='#000000', width=375)
            self.hline2.pack(pady=25)

            try:
                self.cursor.execute('''SELECT transaction_type, amount, recipient FROM transactions
                                    WHERE user = ? ORDER BY receipt_id DESC
                                    LIMIT 3''', (self.user,))
                results = self.cursor.fetchall()
            except Exception as e:
                print(e)
            
            self.recordsframe = tk.Frame(self.main_frame, width=375, height=350, bg='#f7f7fa')
            self.recordsframe.pack(pady=(5, 0))
            self.toplabel = tk.Label(self.recordsframe, text='Recent', font=13, bg='#f7f7fa')
            self.toplabel.pack(pady=(20, 0))
            self.history = tk.Frame(self.recordsframe, width=350, height=200, bg='#f7f7fa')
            self.history.pack(expand=1, anchor=tk.N)
            try:
                if len(results) != 0:
                    self.transactlabel = tk.Label(self.history, text='Transaction', fg='#04063d', bg='#f7f7fa', font=('Arial', 15, 'bold')
                                            ).grid(row=0, column=0, padx=(15, 0), pady=(15, 0))
                    self.recipientlabel = tk.Label(self.history, text='Recipient', fg='#04063d', bg='#f7f7fa', font=('Arial', 15, 'bold')
                                            ).grid(row=0, column=1, padx=(15, 0), pady=(15, 0))
                    self.amountlabel = tk.Label(self.history, text='Amount', fg='#04063d', bg='#f7f7fa', font=('Arial', 15, 'bold')
                                            ).grid(row=0, column=2, padx=(15, 0), pady=(15, 0))
                    
                    for i, (transaction_type, amount, recipient) in enumerate(results, start=1):

                        if transaction_type == 'Money Recieved':
                            tk.Label(self.history, text=f"+${amount:.2f}", fg='#0aba07', bg='#f7f7fa', font=('Arial', 13, 'bold')
                                                ).grid(row=i, column=2, padx=(15, 0), pady=(15, 0))
                            tk.Label(self.history, text=transaction_type, fg='#04063d', bg='#f7f7fa', font=('Arial', 13)
                                                        ).grid(row=i, column=0, padx=(15, 0), pady=(15, 0))
                            tk.Label(self.history, text=recipient, fg='#04063d', bg='#f7f7fa', font=('Arial', 11)
                                                    ).grid(row=i, column=1, padx=(15, 0), pady=(15, 0))
                            tk.Frame(self.history, height=1, bg='#000000', width=375).grid(row=i, column=0, columnspan=3, pady=(38, 0))
                        
                        elif transaction_type == 'Payment':
                            tk.Label(self.history, text=f"-${amount:.2f}", fg='#f20a11', bg='#f7f7fa', font=('Arial', 13, 'bold')
                                                ).grid(row=i, column=2, padx=(15, 0), pady=(15, 0))
                            tk.Label(self.history, text=transaction_type, fg='#04063d', bg='#f7f7fa', font=('Arial', 13)
                                                        ).grid(row=i, column=0, padx=(15, 0), pady=(15, 0))
                            tk.Label(self.history, text=recipient, fg='#04063d', bg='#f7f7fa', font=('Arial', 11)
                                                    ).grid(row=i, column=1, padx=(15, 0), pady=(15, 0))
                            tk.Frame(self.history, height=1, bg='#000000', width=375).grid(row=i, column=0, columnspan=3, pady=(38, 0))
                else:
                    self.iconlabel = tk.Label(self.history, image=self.empty_icon, height=225,
                                              text='Recent transactions will appear here.', fg='#04063d',
                                              font=('Consolas', 10), compound=tk.TOP, width=350)
                    self.iconlabel.grid(row=0, column=0, columnspan=3, sticky=tk.N)
            except Exception as e:
                print(e)


        def activity():
            self.homepage.title('My E-Wallet App -- Activity')

            def clear_history(results):
                
                if len(results) == 0:
                    messagebox.showinfo('Clear History', 'Nothing to clear here.')
                    return False
                answer = messagebox.askyesno('Clear History', 'Are you sure your want to clear your transactions history?')
                if answer == 1:
                    try:
                        self.cursor.execute('''
                                            DELETE FROM transactions 
                                            WHERE user = ?''', (self.user,))
                        self.db.commit()

                        self.refreshtab = activity()
                    except Exception as e:
                        print(e)
                else:
                    return False
            
            for widget in self.main_frame.winfo_children():
                widget.destroy()
            
            try:
                self.cursor.execute('''SELECT transaction_type, amount, recipient, receipt_id FROM transactions
                                    WHERE user = ? ORDER BY receipt_id DESC
                                    ''', (self.user,))
                results = self.cursor.fetchall()
            except Exception as e:
                print(e)
            
            self.records = tk.Frame(self.main_frame, width=375, height=500, bg='#f7f7fa')
            self.records.pack_propagate(False)
            self.records.pack(pady=(5, 0))
            self.toplabel = tk.Label(self.records, text='Activity History', font=13, bg='#f7f7fa')
            self.toplabel.pack(pady=(20, 0))
            self.clearbtn = tk.Button(self.records, text='Clear', font=('Poppins', 8), padx=10, pady=3,
                                      bd=0, bg='#04063d', fg='#FFFFFF', activebackground='#FFFFFF', activeforeground='#04063d',
                                      command=lambda: clear_history(results))
            self.clearbtn.pack(anchor=tk.CENTER, side=tk.BOTTOM)
            self.historytab = tk.Frame(self.records, width=350, bg='#f7f7fa')
            self.historytab.pack_propagate(False)
            self.historytab.pack(expand=True, anchor=tk.N)
            
            try:
                if len(results) != 0:
                    self.transactlabel = tk.Label(self.historytab, text='Transaction', fg='#04063d', bg='#f7f7fa', font=('Arial', 13, 'bold')
                                            ).grid(row=0, column=0, padx=(10, 0), pady=(15, 0))
                    self.recipientlabel = tk.Label(self.historytab, text='Recipient', fg='#04063d', bg='#f7f7fa', font=('Arial', 13, 'bold')
                                            ).grid(row=0, column=1, padx=(10, 0), pady=(15, 0))
                    self.amountlabel = tk.Label(self.historytab, text='Amount', fg='#04063d', bg='#f7f7fa', font=('Arial', 13, 'bold')
                                            ).grid(row=0, column=2, padx=(10, 0), pady=(15, 0))
                    self.invoicelabel = tk.Label(self.historytab, text='Invoice ID', fg='#04063d', bg='#f7f7fa', font=('Arial', 13, 'bold')
                                            ).grid(row=0, column=3, padx=(10, 0), pady=(15, 0))
                    
                    for i, (transaction_type, amount, recipient, receipt_id) in enumerate(results, start=1):

                        if transaction_type == 'Money Recieved':
                            tk.Label(self.historytab, text=f"+${amount:.2f}", fg='#0aba07', bg='#f7f7fa', font=('Arial', 11, 'bold')
                                                ).grid(row=i, column=2, padx=(10, 0), pady=(15, 0))
                            tk.Label(self.historytab, text=transaction_type, fg='#04063d', bg='#f7f7fa', font=('Arial', 11)
                                                        ).grid(row=i, column=0, padx=(10, 0), pady=(15, 0))
                            tk.Label(self.historytab, text=recipient, fg='#04063d', bg='#f7f7fa', font=('Arial', 11)
                                                    ).grid(row=i, column=1, padx=(10, 0), pady=(15, 0))
                            tk.Label(self.historytab, text=receipt_id, fg='#04063d', bg='#f7f7fa', font=('Arial', 11, 'bold')
                                                ).grid(row=i, column=3, padx=(10, 0), pady=(15, 0))
                            tk.Frame(self.historytab, height=1, bg='#000000', width=375).grid(row=i, column=0, columnspan=3, pady=(38, 0))
                        
                        elif transaction_type == 'Payment':
                            tk.Label(self.historytab, text=f"-${amount:.2f}", fg='#f20a11', bg='#f7f7fa', font=('Arial', 11, 'bold')
                                                ).grid(row=i, column=2, padx=(15, 0), pady=(15, 0))
                            tk.Label(self.historytab, text=transaction_type, fg='#04063d', bg='#f7f7fa', font=('Arial', 11)
                                                        ).grid(row=i, column=0, padx=(15, 0), pady=(15, 0))
                            tk.Label(self.historytab, text=recipient, fg='#04063d', bg='#f7f7fa', font=('Arial', 11)
                                                    ).grid(row=i, column=1, padx=(15, 0), pady=(15, 0))
                            tk.Label(self.historytab, text=receipt_id, fg='#04063d', bg='#f7f7fa', font=('Arial', 11, 'bold')
                                                ).grid(row=i, column=3, padx=(10, 0), pady=(15, 0))
                            tk.Frame(self.historytab, height=1, bg='#000000', width=375).grid(row=i, column=0, columnspan=3, pady=(38, 0))
                else:
                    self.iconlabel = tk.Label(self.historytab, image=self.empty_icon,
                                              text='Recent transactions will appear here.', fg='#04063d',
                                              font=('Consolas', 10), compound=tk.TOP, width=350, height=475)
                    self.iconlabel.grid(row=0, column=0, columnspan=3, sticky=tk.N)
            except Exception as e:
                print(e)


        def profile():
            self.homepage.title('My E-Wallet App -- Profile')
            self.prof_path = tk.PhotoImage(file='account.png')
            self.edit_path = tk.PhotoImage(file='edit.png')
            self.out_path = tk.PhotoImage(file='logout.png')
            self.profile_pic = self.prof_path
            self.edit_icon = self.edit_path
            self.logout_icon = self.out_path

            def editprof():

                def verify_entries():
                    nameinput = self.edit_user_name.get()
                    ageinput = self.edit_user_age.get()
                    self.validnewname = None
                    self.validnewage = None
                    try:
                        if any(i.isdigit() for i in nameinput):
                            self.warninglabel.config(text='Oops! You cannot put a number in your name, please try again.')
                            return False
                        elif len(nameinput) <= 7:
                            self.warninglabel.config(text='Oops! Your name might be invalid, please try again.')
                            return False
                        elif len(nameinput) == 0:
                            self.warninglabel.config(text='Please input your name.')
                            return False
                        else:
                            self.validnewname = nameinput
                        
                        if len(ageinput) != 2:
                            self.warninglabel.config(text='Oops! Your age is invalid. Please try again.')
                            return False
                        else:
                            try:
                                int(self.edit_user_age.get())
                                self.validnewage = int(self.edit_user_age.get())
                            except Exception as e:
                                self.warninglabel.config(text='Oops! Your age might be invalid, please double check.')
                                return False

                        self.cursor.execute('''UPDATE users
                                            SET name = ?, 
                                                age = ?
                                            WHERE contact_num = ?''', (self.validnewname, self.validnewage, self.user,))
                        self.db.commit()
                        self.refreshprof = profile()
                        self.editwin.destroy()
                    except Exception as e:
                        print(e)

                self.editwin = tk.Toplevel()
                self.editwin.geometry('450x335+550+230')
                self.editwin.title('Edit Profile')
                self.editwin.resizable(0, 0)

                self.toplabel = tk.Label(self.editwin, text='Edit Profile', font=('Ink free', 17))
                self.toplabel.pack(pady=(25, 15))

                self.editframe = tk.Frame(self.editwin, height=225, width=400, bg='#ededed')
                self.editframe.pack()

                self.edit_namelabel = tk.Label(self.editframe, text='Name:', font=('Consolas', 13), bg='#ededed')
                self.edit_namelabel.grid(row=0, column=0, pady=8, sticky=tk.W, padx=(10, 5))
                self.edit_user_name = tk.Entry(self.editframe, bd=0, font=('Consolas', 13), bg='#FFFFFF')
                self.edit_user_name.grid(row=0, column=1, padx=10, pady=8)

                self.edit_agelabel = tk.Label(self.editframe, text='Age:', font=('Consolas', 13), bg='#ededed')
                self.edit_agelabel.grid(row=1, column=0, pady=8, sticky=tk.W, padx=(10, 5))
                self.edit_user_age = tk.Entry(self.editframe, bd=0, font=('Consolas', 13), bg='#FFFFFF')
                self.edit_user_age.grid(row=1, column=1, padx=10, pady=8)

                self.savebtn = tk.Button(self.editframe, text='Save Changes',
                                        image=self.edit_icon, compound=tk.LEFT, font=('Poppins', 10), padx=15, pady=5,
                                        bd=0, bg='#22e325', fg='#FFFFFF', activebackground='#FFFFFF', activeforeground='#04063d', command=verify_entries)
                self.savebtn.grid(row=2, column=0, pady=15)
                self.cancelbtn = tk.Button(self.editframe, text='Cancel',
                                        image=self.logout_icon, compound=tk.LEFT, font=('Poppins', 10), padx=15, pady=5,
                                        bd=0, bg='#d1021a', fg='#FFFFFF', activebackground='#FFFFFF', activeforeground='#04063d', command=lambda: self.editwin.destroy())
                self.cancelbtn.grid(row=2, column=1)
                self.warninglabel = tk.Label(self.editframe, text='', fg='red', font=('Calibri Light', 9), bg='#ededed')
                self.warninglabel.grid(row=3, column=0, columnspan=2)



            def logout():
                answer = messagebox.askyesno('Logout', 'Are you sure you want to logout?')
                if answer == 1:
                    messagebox.showinfo('Logout', 'Thank you for using My E-Wallet App!')
                    self.homepage.destroy()
                else:
                    return False
            
            for widget in self.main_frame.winfo_children():
                widget.destroy()
            
            self.cursor.execute('SELECT name, age, contact_num FROM users WHERE contact_num = ?', (self.user,))
            curr_user = self.cursor.fetchone()

            if curr_user != None:
                self.name, self.age, self.contact = curr_user

            self.deets = tk.Frame(self.main_frame, width=385, height=450, bg='#ededed', padx=10, pady=10)
            self.deets.pack(anchor=tk.CENTER, pady=(35, 0))

            self.pic = tk.Label(self.deets, image=self.profile_pic)
            self.pic.grid(row=0, column=0, columnspan=2, pady=(35, 45))

            self.namelabel = tk.Label(self.deets, text='Name:', font=('Consolas', 13), bg='#ededed')
            self.namelabel.grid(row=1, column=0, pady=8, sticky=tk.W, padx=(10, 5))
            self.user_name = tk.Label(self.deets, text=self.name, font=('Consolas', 13), bg='#ededed')
            self.user_name.grid(row=1, column=1, padx=10, pady=8)
            self.agelabel = tk.Label(self.deets, text='Age:', font=('Consolas', 13), bg='#ededed')
            self.agelabel.grid(row=2, column=0, pady=8, sticky=tk.W, padx=(10, 5))
            self.user_age = tk.Label(self.deets, text=self.age, font=('Consolas', 13), bg='#ededed')
            self.user_age.grid(row=2, column=1, padx=10, pady=8)
            self.contactlabel = tk.Label(self.deets, text='Contact Number:', font=('Consolas', 13), bg='#ededed')
            self.contactlabel.grid(row=3, column=0, pady=8, sticky=tk.W, padx=(10, 5))
            self.user_contact = tk.Label(self.deets, text=f"+63{self.contact}", font=('Consolas', 13), bg='#ededed')
            self.user_contact.grid(row=3, column=1, padx=10, pady=8)

            self.editbtn = tk.Button(self.deets, text='Edit Profile',
                                     image=self.edit_icon, compound=tk.LEFT, font=('Poppins', 10), padx=15, pady=5,
                                     bd=0, bg='#22e325', fg='#FFFFFF', activebackground='#FFFFFF', activeforeground='#04063d', command=editprof)
            self.editbtn.grid(row=4, column=0, columnspan=2, pady=15)
            self.logoutbtn = tk.Button(self.deets, text='Logout',
                                     image=self.logout_icon, compound=tk.LEFT, font=('Poppins', 10), padx=15, pady=5,
                                     bd=0, bg='#d1021a', fg='#FFFFFF', activebackground='#FFFFFF', activeforeground='#04063d', command=logout)
            self.logoutbtn.grid(row=5, column=0, columnspan=2)






        self.homepage = tk.Tk()
        self.homepage.geometry('450x620+550+80')
        self.homepage.resizable(False, False)
        self.homepage.title('My E-Wallet App')
        self.homepage.config(bg='#FFFFFF')
        try:
            self.cursor.execute("""
                                CREATE TABLE IF NOT EXISTS transactions (
                                user TEXT NULL,
                                transaction_type TEXT NOT NULL,
                                amount INTEGER NOT NULL,
                                recipient TEXT NOT NULL,
                                receipt_id INTEGER PRIMARY KEY AUTOINCREMENT)
                                """)
            self.db.commit()
        except Exception as e:
            messagebox.showerror('table transactions create', e)

        self.home_path = tk.PhotoImage(file='home.png')
        self.acts_path = tk.PhotoImage(file='activity.png')
        self.prof_path = tk.PhotoImage(file='user.png')
        self.home_icon = self.home_path
        self.acts_icon = self.acts_path
        self.prof_icon = self.prof_path

        self.nav_buttons = tk.Frame(self.homepage, bg='#04063d', height=85)
        self.nav_buttons.grid_propagate(False)
        self.nav_buttons.pack(anchor=tk.S, side=tk.BOTTOM, fill=tk.X, expand=1)

        self.homebtn = tk.Button(self.nav_buttons, text='Home',
                                 bd=0, image=self.home_icon,
                                 compound=tk.TOP, bg='#04063d', padx=55,
                                 fg='#ebebed', height=85, activebackground='#04063d',
                                 activeforeground='#04063d', command=home_page)
        self.homebtn.grid(row=0, column=0)
        self.homebtn.image = self.home_icon
        
        self.actsbtn = tk.Button(self.nav_buttons, text='Activity',
                                 bd=0, image=self.acts_icon,
                                 compound=tk.TOP, bg='#04063d', padx=55,
                                 fg='#ebebed', height=85, activebackground='#04063d',
                                 activeforeground='#04063d', command=activity)
        self.actsbtn.grid(row=0, column=1)
        self.actsbtn.image = self.acts_icon

        self.profilebtn = tk.Button(self.nav_buttons, text='Profile',
                                 bd=0, image=self.prof_icon,
                                 compound=tk.TOP, bg='#04063d', padx=55,
                                 fg='#ebebed', height=85, activebackground='#04063d',
                                 activeforeground='#04063d', command=profile)
        self.profilebtn.grid(row=0, column=2)
        self.profilebtn.image = self.prof_icon
            
        self.main_frame = tk.Frame(self.homepage, height=535, bg='#f7f7fa')
        self.main_frame.pack_propagate(False)
        self.main_frame.pack(anchor=tk.N, side=tk.TOP, ipadx=10, ipady=10, fill=tk.X, expand=1)
        self.default_page = home_page()

