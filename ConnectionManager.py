import tkinter as tk
from tkinter import ttk
from twisted.internet import tksupport, reactor, task
import platform
import logging
import pickle
import os


class Main(tk.Tk):
    """
    the SeveredSec connection Manager
    must be run as administrator.
    """
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("VPN Manager")
        self.geometry("512x256")
        self.resizable(width=True, height=True)
        self.attributes('-alpha', 1)
        tksupport.install(self)

        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)
        sub_menu = ttk.Menubutton(menu_bar)
        menu_bar.add_cascade(label="File", menu=sub_menu)

        self.installer = None
        self.admin_rights = False
        self.config = None
        self.operating_system = platform.system()
        self.supported_os = {"Linux": self.linux_installer,
                             "Windows": self.windows_installer}
        self.required_modules = ["twisted"]
        try:
            self.supported_os[self.operating_system]()
        except KeyError as bad_os:
            logging.critical("this Platform may not be supported: {0}".format(bad_os))

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        if os.path.isfile("config.p"):
            with open('config.p', 'r') as config:
                self.config = pickle.load(config)

        for F in [HomeGUI, InstallScreen]:
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[page_name] = frame

        reactor.run()

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    @staticmethod
    def on_closing():
        # todo add clean shutdown which closes the opened VPN connection
        reactor.stop()

    def linux_installer(self):
        logging.debug("OS is linux")
        #from LinuxInstaller import LinuxInstaller as Installer
        #self.installer = Installer(self.required_modules)

    def windows_installer(self):
        logging.debug("os is windows")
        #from WindowsInstaller import WindowsInstaller as Installer
        #self.installer = Installer(self.required_modules)


class HomeGUI(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


class InstallScreen(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller



Main()
