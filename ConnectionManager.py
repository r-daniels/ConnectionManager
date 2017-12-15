import tkinter as tk
from tkinter import ttk
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
        self.resizable(width=False, height=False)
        self.attributes('-alpha', 1)

        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        sub_menu = ttk.Menubutton(menu_bar)
        menu_bar.add_cascade(label="File", menu=sub_menu)

        self.installer = None  # which installer to use
        self.admin_rights = False  # if not run as admin prompt user to rerun as admin
        self.config = dict()  # loaded from config.p
        self.directory_servers = ['127.0.0.1']  # list of directory servers to pull configs from
        logging.basicConfig(level=logging.DEBUG)
        self.operating_system = platform.system()
        self.supported_os = {"Linux": self.linux_installer,
                             "Windows": self.windows_installer}
        self.required_modules = []

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.frames = dict()
        for F in [HomeGUI, InstallScreen]:
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            frame.grid(row=0, column=0, sticky=tk.NSEW)
            self.frames[page_name] = frame

        # config.p can be used to store user settings and preferences across reboots
        if os.path.isfile("config.p"):
            with open('config.p', 'rb') as config:
                self.config = pickle.load(config)
            self.show_frame('HomeGUI')
        else:
            self.show_frame('InstallScreen')

        self.mainloop()

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        if page_name == 'HomeGUI':  # todo start directory server query to populate listbox
            pass
        frame.tkraise()

    @staticmethod
    def on_closing():
        # todo add clean shutdown which closes the opened VPN connection
        exit(1)

    def linux_installer(self):
        logging.debug("OS is linux")
        from LinuxInstaller import LinuxInstaller as Installer
        self.installer = Installer(self.required_modules)

    def windows_installer(self):
        logging.debug("os is windows")
        from WindowsInstaller import WindowsInstaller as Installer
        self.installer = Installer(self.required_modules)

    def check_for_updates(self):
        """
        checks directory server for updated versions of SeveredSec Connect and dependencies. if a new version is found
        download the new version, and restart.
        :return:
        """
        pass


class HomeGUI(ttk.Frame):
    """
    this frame contains the main portion of the user interface allowing users to select which server to connect to
    and to select additional options such as selecting to use plugable transports like obfsproxy or tor over VPN
    """
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        ttk.Treeview(self, columns=None, show="headings")

    def display_server_info(self):
        pass


class InstallScreen(ttk.Frame):
    """
    frame contains a label notifying the user that the Connection Manager is not installed
    """
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.install_label = ttk.Label(self,
                                       text="""SeveredSec Connect has detected that this is the first time it's been run on this
system. if you would like to use the Connection Manager please click install to
allow SeveredSec Connect to create the required directories and install:
OpenVPN,
TOR,
and obfsproxy""",
                                       wraplength=750)
        self.install_label.grid(row=0, padx=3, pady=3, sticky="n")

        self.install_button = ttk.Button(self,
                                         text="Install",
                                         command=self.install)
        self.install_button.grid(row=1, padx=3, pady=3, sticky="n")

        self.installing_label = ttk.Label(self,
                                          text="SeveredSec Connect is installing this may take a few minutes")

    def install(self):
        self.install_label.destroy()
        self.install_button.destroy()
        self.installing_label.grid(row=0, padx=3, pady=3, sticky="n")
        try:
            self.controller.supported_os[self.controller.operating_system]()
        except KeyError as bad_os:
            logging.critical("this Platform may not be supported: {0}".format(bad_os))
            exit(1)

Main()
