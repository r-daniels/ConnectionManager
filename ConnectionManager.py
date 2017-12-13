import platform
import logging
import


class Main:
    """
    the SeveredSec connection Manager
    must be run as administrator.
    """
    def __init__(self):
        self.installer = None
        self.admin_rights = False
        self.operating_system = platform.system()
        self.supported_os = {"Linux": self.linux_installer,
                             "Windows": self.windows_installer}
        self.required_modules = ["twisted"]
        try:
            self.supported_os[self.operating_system]()
        except KeyError as bad_os:
            print("this Platform may not be supported: {0}".format(bad_os))

    def linux_installer(self):
        logging.debug("OS is linux")
        from LinuxInstaller import LinuxInstaller as Installer
        self.installer = Installer(self.required_modules)

    def windows_installer(self):
        logging.debug("os is windows")
        from WindowsInstaller import WindowsInstaller as Installer
        self.installer = Installer(self.required_modules)

Main()
