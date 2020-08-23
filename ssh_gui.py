import os,sys,time
import tkinter as tk
from tkinter import messagebox
from tkinter import Label
from tkinter import Button
from tkinter import Entry
from tkinter import Text
from tkinter import Listbox
from netmiko import ConnectHandler
from netmiko import NetmikoAuthenticationException
from tkinter import *

__author__ = "cyro"
if __name__ == "__main__":

    ios_connect = {
        'device_type' : 'cisco_ios',
        'host' : 'ip',
        'username' : 'username',
        'password' : 'password',
        'port' : '22',
    }
    host_list = ['Core Router', 'Core Server', 'Core Switch']
    win = tk.Tk()
    win_width = win.winfo_reqwidth()
    win_height = win.winfo_reqheight()
    pos_right = int(win.winfo_screenwidth()/2 - win_width/2)
    pos_down = int(win.winfo_screenheight()/2 - win_height/2)

    win.title('Quick Task Terminal')
    win.configure(background = 'black')
    win.geometry('+{}+{}'.format(pos_right, pos_down))
    win.iconbitmap('space.ico') #add image.ico file
    
    lbl = Label(
        win,
        text = 'QT TRMNL',
        bg = 'black',
        fg = 'white',
        font = ('Arial Bold', 14))
    lbl.grid(column=0, row=0)

    lbl_usr = Label(
        win,
        text = 'Enter your name',
        bg = 'black',
        fg = 'white',
        font = ('Arial', 10))
    lbl_usr.grid(column=0, row=1)

    lbl_psw = Label(
        win,
        text = 'Enter your password',
        bg = 'black',
        fg = 'white',
        font = ('Arial', 10))
    lbl_psw.grid(column=0, row=3)

    def connect_terminal():
        global ssh_connect
        ios_connect['username'] = ent_usr.get()
        ios_connect['password'] = ent_psw.get()
        try:
            text_output.delete(1.0, END)
            ssh_connect = ConnectHandler(**ios_connect)
            output = ssh_connect.find_prompt()
            text_output.insert(INSERT, output)
            pass
        except NetmikoAuthenticationException:
            messagebox.showinfo('Sorry!', 'Authentication Failure!')
            pass
        ent_usr.delete(0, 'end')
        ent_psw.delete(0, 'end')
        
    def show_command():
        ssh_output = ssh_connect.send_command(ent_cmd.get())
        text_output.delete(1.0, END)
        text_output.insert(INSERT, ssh_output)
        ent_cmd.delete(0, 'end')

    def select():
        selection = lst_host.get(ANCHOR)
        if selection == 'Core Router':
            ios_connect['host'] = '192.168.1.7'
        elif selection == 'Core Server':
            ios_connect['host'] = '10.1.111.254'
            ios_connect['device_type'] = 'linux'
        elif selection == 'Core Switch':
            ios_connect['host'] = '10.1.111.2'
        else:
            pass
    
    def disconnect():
        text_output.delete(1.0, END)
        ssh_connect.disconnect()
        text_output.insert(INSERT, 'You have been disconnected')

    ent_usr = Entry(win, width=20)
    ent_usr.grid(column=0, row=2)
    ent_usr.focus()

    ent_psw = Entry(win, show='*', width=20)
    ent_psw.grid(column=0, row=4)

    ent_cmd = Entry(win, width=40)
    ent_cmd.grid(column=2, row=2)

    text_output = Text(win, width=75, height=25)
    text_output.grid(column=2, row=6)
    
    btn_sub = Button(
        win,
        text = 'Send',
        bg = 'blue',
        fg = 'white',
        command = show_command)
    btn_sub.grid(column=3, row=2)

    btn_usr = Button(
        win,
        text = 'Submit',
        bg = 'blue',
        fg = 'white',
        command = connect_terminal)
    btn_usr.grid(column=1, row=2)

    btn_choice = Button(
        win,
        text = 'Select',
        bg = 'blue',
        fg = 'white',
        command = select)
    btn_choice.grid(column=0, row=7)

    btn_disconnect = Button(
        win,
        text = 'Disconnect',
        bg = 'blue',
        fg = 'white',
        command = disconnect)
    btn_disconnect.grid(column=0, row=8)

    lst_host = Listbox(win, bg='blue', fg='white', selectmode=SINGLE)
    for i in host_list:
        lst_host.insert(END, i)
    lst_host.grid(column=0, row=6)
    
    win.wait_window()
    win.mainloop()
