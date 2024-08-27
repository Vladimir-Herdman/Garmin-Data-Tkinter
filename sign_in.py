from tkinter import *
from tkinter import ttk
from tkmacosx import Button

from garminconnect import Garmin, GarminConnectTooManyRequestsError
from garth.http import GarthHTTPError

from datetime import date

from show_data import ShowData


class SignIn():
    def __init__(self, root):
        # variable for later frame usage
        self.root = root
        # initial set up
        root.title('Garmin Sign In')

        self.sign_in_frame = ttk.Frame(root, padding='12 12 12 12')
        self.sign_in_frame.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

            # variables
        self.username = StringVar()
        self.password = StringVar()
        self.show_password = BooleanVar()
            # entrys
        self.user_entry = ttk.Entry(self.sign_in_frame, width=21, textvariable=self.username)
        self.user_entry.grid(column=1, row=1, sticky=(W, E))

        self.pass_entry = ttk.Entry(self.sign_in_frame, width=21, textvariable=self.password, show='\u2022') # \u2022 for bullet character in password entry
        self.pass_entry.grid(column=1, row=2, sticky=(W, E))
            # labels
        ttk.Label(self.sign_in_frame, text='Username:').grid(column=0, row=1, sticky=E)
        ttk.Label(self.sign_in_frame, text='Password:').grid(column=0, row=2, sticky=E)
            # button
        self.sign_in_button = Button(self.sign_in_frame, text='Sign In', command=self.sign_in_func, bg='lightblue')
        self.sign_in_button.grid(column=0, row=3, columnspan=2, sticky=(W, E))

        self.show_password_button = Button(self.sign_in_frame, text='Show', command=self.show_password_func, bg='lightgray')
        self.show_password_button.grid(column=2, row=2, sticky=W)
            # clean up
        root.after(100, self.user_entry.focus)  # cursor starts in this field, so users don't need to click to before starting to type
        root.bind('<Return>', self.sign_in_func)

    def sign_in_func(self, *args):
        '''
        Button function command that is the logic for the username and password that works for Garmin sign in
        '''
        try:
            # check sign in to Garmin API wrapper
            client = Garmin(self.username.get(), self.password.get())
            client.login()
                # provide feedback that signin worked so not just staring at button after
            self.destroy_all_frame_widgets(self.sign_in_frame)
            ttk.Label(self.sign_in_frame, text='Account Found, Currently Loading...', padding='0 0 0 10').grid(column=0, row=0, sticky=W)
            progress_bar = ttk.Progressbar(self.sign_in_frame, maximum=100)
            progress_bar.grid(column=0, row=2, columnspan=2, sticky=(W, E))
            
            self.root.after(1000) # update bar
            progress_bar.step(40)
            self.sign_in_frame.update_idletasks()
                
                # get the whole list of activities for data section
            self.all_activities = client.get_activities_by_date('2003-08-14', str(date.today()))
            
            self.root.after(1000) # update bar
            progress_bar.step(50)
            self.sign_in_frame.update_idletasks()
            
            client.logout()
            
            self.root.after(1000) # update bar
            progress_bar.step(10)
            self.sign_in_frame.update_idletasks()
                
                # destroy for next frame
            self.sign_in_frame.destroy()
            ShowData(self.root, self.all_activities, str(date.today()))
        except GarthHTTPError:
            # label error in signing in, move button
            self.sign_in_button.destroy()
            ttk.Label(self.sign_in_frame, text='No Account Found', foreground='red').grid(column=1, row=3, sticky=W)
            self.sign_in_button = Button(self.sign_in_frame, text='Sign In', command=self.sign_in_func, bg='lightblue')
            self.sign_in_button.grid(column=0, row=4, columnspan=2, sticky=(W, E))
                # remove wrong entries and refocus
            self.user_entry.delete(0, 'end')
            self.pass_entry.delete(0, 'end')
            self.user_entry.focus()
        except GarminConnectTooManyRequestsError:
            self.destroy_all_frame_widgets(self.sign_in_frame)
            ttk.Label(self.sign_in_frame, text="Sorry, you've tried to sign in too many times, and so too many requests have been made to Garmin.  Take a break, and try again later!", foreground='red', wraplength=300).grid(column=0, row=0, sticky=(N, E, S, W))

    def show_password_func(self, *args):
        if self.show_password.get() is False:
            # show text
            self.show_password.set(True)
            self.pass_entry.config(show='')
            self.show_password_button.configure(text='Hide')
        elif self.show_password.get() is True:
            # hide text
            self.show_password.set(False)
            self.pass_entry.config(show='\u2022')
            self.show_password_button.configure(text='Show')
    
    def destroy_all_frame_widgets(self, frame):
        for widget in frame.winfo_children():
                widget.destroy()