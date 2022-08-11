__author__ = "Christian Perla"

if __name__ == "__main__":

    import os,sys
    import tkinter as tk 
    from tkinter import Button
    from tkinter import messagebox
    import webbrowser

#Add functions below#
def wireshark_func():
    os.startfile("C:/Program Files/Wireshark/Wireshark.exe")

def putty_func():
    os.startfile("C:/Users/Owner/Downloads/putty.exe")

def winmerge_func():
    os.startfile("C:/Program Files/WinMerge/WinMergeU.exe")

def visual_func():
    os.startfile("C:/Users/Owner/AppData/Local/Programs/Microsoft VS Code/Code.exe")

def notepad_func():
    os.startfile("C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Notepad++.lnk")

def nmap_func():
    os.startfile("C:/Program Files (x86)/Nmap/zenmap.exe")

def keepass_func():
    os.startfile("C:/Program Files/KeePass Password Safe 2/KeePass.exe")

def cisco_func():
    cisco = "https://www.cisco.com/"
    webbrowser.open(cisco)

def google_func():
    google = "https://www.google.com/"
    webbrowser.open(google)

def motd_func():
    motd_file = open('test_file.txt', 'r')
    motd_line = motd_file.readline()
    messagebox.showinfo('MOTD', '%s' % (motd_line))
    # messagebox.showinfo('MOTD', 'test1')

def exit_func():
    winmain.destroy()
    sys.exit()
 
# Main Window Dimensions
winmain = tk.Tk()
winmain_width = winmain.winfo_reqwidth()
winmain_height = winmain.winfo_reqheight()
position_right = int(winmain.winfo_screenwidth()/2 - winmain_width/2)
position_down = int(winmain.winfo_screenheight()/2 - winmain_height/2)

# Main Window Parameters
winmain.title('QT Maint Terminal')
winmain.configure(background='gray16')
winmain.geometry('+{}+{}'.format(position_right, position_down))
winmain.wm_iconbitmap('qt.ico')

# Application Buttons
wireshark_app = Button(
    winmain,
    text='Wireshark',
    bg='sky blue',
    fg='gray16',
    command=wireshark_func)
wireshark_app.grid(column=0,row=0,ipadx=5,pady=5,padx=10)

putty_app = Button(
    winmain,
    text='Putty',
    bg='medium orchid',
    fg='white',
    command=putty_func)
putty_app.grid(column=1,row=0,ipadx=15,pady=5,padx=10)

winmerge_app = Button(
    text='WinMerge',
    bg='medium spring green',
    fg='gray16',
    command=winmerge_func)
winmerge_app.grid(column=2,row=0,ipadx=5,pady=5,padx=10)

visual_app = Button(
    text='Visual',
    bg='slate blue',
    fg='white',
    command=visual_func)
visual_app.grid(column=0,row=1,ipadx=15,pady=5,padx=10)

notepad_app = Button(
    text='Notepad +',
    bg='gold',
    fg='gray16',
    command=notepad_func)
notepad_app.grid(column=1,row=1,pady=5,padx=10)

nmap_app = Button(
    text='NMap',
    bg='sky blue',
    fg='gray16',
    command=nmap_func)
nmap_app.grid(column=2,row=1,ipadx=15,pady=5,padx=10)

keepass_app = Button(
    text='KeePass',
    bg='medium orchid',
    fg='white',
    command=keepass_func)
keepass_app.grid(column=0,row=2,ipadx=10,pady=5,padx=10)

cisco_app = Button(
    text='Cisco',
    bg='medium spring green',
    fg='gray16',
    command=cisco_func)
cisco_app.grid(column=1,row=2,ipadx=15,pady=5,padx=10)

google_app = Button(
    text='Google',
    bg='slate blue',
    fg='white',
    command=google_func)
google_app.grid(column=2,row=2,ipadx=12,pady=5,padx=10)

exit_app = Button(
    text='Exit',
    bg='red',
    fg='white',
    command=exit_func)
exit_app.grid(column=0,row=3,ipadx=15,pady=5,padx=10,sticky='e')

motd_app = Button(
    text='MOTD',
    bg='gold',
    fg='gray16',
    command=motd_func)
motd_app.grid(column=2,row=3,ipadx=15,pady=5,padx=10,sticky='w')

winmain.mainloop()