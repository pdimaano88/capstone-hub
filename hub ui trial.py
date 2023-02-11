from tkinter import *
from tkinter import ttk
import tkinter.font as font
import time
#import sv_ttk

##mainscreen 
mainscreen = Tk()
mainscreen.title("Hub App 1.0")
##mainscreen.geometry("1024x600")
mainscreen.config(bg = "gray69")
#mainscreen.attributes('-type', 'dock') #turn on when in raspberry pi

Hubtextfont = font.Font(family="Helvetica", size = 10, weight = "bold")

##login func
def login():
    username = "admin"
    password = "admin"
    if username_entry.get() == username and password_entry.get() == password:
        username_label.destroy()
        username_entry.destroy()
        password_label.destroy()
        password_entry.destroy()
        login_button.destroy()

        ##home button
        home_button = Button(mainscreen, text = "Home", fg = "black", bg = "gray85", font=buttonfont)
        home_button.grid(row = 2, column = 0, padx = 15)

        #reminder button
        reminder_button = Button(mainscreen, text = "Reminders", fg = "black", bg = "gray85", font=buttonfont, command=reminder)
        reminder_button.grid(row = 2, column = 1, padx = 15)

        ##calendar button
        calendar_button = Button(mainscreen, text = "Calendar", fg = "black", bg = "gray85", font=buttonfont)
        #calendar_button.grid(row = 1, column = 2)
        calendar_button.grid(row = 2, column = 2, padx = 15)

        ##weather button
        weather_button = Button(mainscreen, text = "Weather", fg = "black", bg = "gray85", font=buttonfont)
        #weather_button.grid(row = 1, column = 3)
        weather_button.grid(row = 2, column = 3, padx = 15)

        ##office button
        office_button = Button(mainscreen, text = "Office Controls", fg = "black", bg = "gray85", font=buttonfont)
        #weather_button.grid(row = 1, column = 3)
        office_button.grid(row = 2, column = 4, padx = 15)

        ##team button
        team_button = Button(mainscreen, text = "Team", fg = "black", bg = "gray85", font=buttonfont)
        #weather_button.grid(row = 1, column = 3)
        team_button.grid(row = 2, column = 5, padx = 15)
    else:
        loginfailed_label = Label(mainscreen, text = "Login Failed",font = Hubtextfont, fg = "black", bg= "gray69")
        loginfailed_label.grid(row = 6, column = 4)


def reminder():

    def sendreminder():
        reminder_file = open("reminders.txt", "w")
        reminder_file.write(reminder_text_textbox.get(1.0, END))
        reminder_file.close()

    reminder_person_label = Label(mainscreen, text = "Recepient",font = Hubtextfont, fg = "black", bg= "gray69")
    reminder_person_label.grid(row = 3, column = 0)
    recipientoption = [
        "Anthony",
        "Paolo",
        "Cavin",
        "Aisha",
    ]
    selectrecipient = StringVar()
    selectrecipient.set(recipientoption[0])
    recepient_combobox = ttk.Combobox(mainscreen, value = recipientoption)
    recepient_combobox.grid(row = 3, column = 1,columnspan = 3)

    reminder_text_label = Label(mainscreen, text = "Message",font = Hubtextfont, fg = "black", bg= "gray69")
    reminder_text_label.grid(row = 4, column = 0)
    reminder_text_textbox = Text(mainscreen, font = Hubtextfont, width = 40, height = 10)
    reminder_text_textbox.grid(row = 4, column = 1, columnspan= 3)

    reminder_text_button = Button(mainscreen, text = "Send", fg = "black", bg = "gray85", font=buttonfont, command = sendreminder)
    reminder_text_button.grid(row = 4, column = 4)

    





##Clock func
def clock():
    hour = time.strftime("%I")
    minute = time.strftime("%M")
    second = time.strftime("%S")
    am_pm = time.strftime("%p")
    day = time.strftime("%a")
    month = time.strftime("%b")
    monthday = time.strftime("%e")
    time_widget.config(text=hour + ":" + minute + ":" + second + " " + am_pm + " " + day + ", " + month + " " + monthday)
    time_widget.after(1000, clock)

time_widget = Label(mainscreen, text=" ", font = Hubtextfont, fg = "black", bg= "gray69")
time_widget.grid(row = 0, column = 6, sticky = "E")
clock()


Hubapp = Label(mainscreen, text = "Hub App 1.0", font = Hubtextfont, bg = "gray69")
Hubapp.grid(row = 0, column=0, sticky = "W")

##buttons func
buttonfont = font.Font(family="Helvetica", size = 15, weight = "bold")

##username field
username_label = Label(mainscreen, text = "Username",font = Hubtextfont, fg = "black", bg= "gray69")
username_entry = Entry(mainscreen)
username_label.grid(row = 2, column = 3)
username_entry.grid(row = 2, column = 4)

##password field
password_label = Label(mainscreen, text = "Password",font = Hubtextfont, fg = "black", bg= "gray69")
password_entry = Entry(mainscreen)
password_label.grid(row = 4, column = 3)
password_entry.grid(row = 4, column = 4)

##login button
#login_label = Label(mainscreen, text = "Login",font = Hubtextfont, fg = "black", bg= "gray69")
login_button = Button(mainscreen, text = "Login", fg = "black", bg = "gray85", font=buttonfont, command = login)
#login_label.pack(side= TOP, anchor= N)
login_button.grid(row = 5, column = 4)



#sv_ttk.set_theme("dark")
mainscreen.mainloop()