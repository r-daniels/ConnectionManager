import logging
import os


class LinuxInstaller:
    """
    functions for installing python modules and openvpn on Linux operating systems

    """

    def __init__(self, modules):
        self.modules = modules
        self.is_admin()
        self.install_python_modules()
        self.install_openvpn()

    def is_admin(self):
        try:
            rights = os.getuid()
        except Exception as e:
            logging.error("unable to determine user rights: {0}".format(e))
            return False
        if rights == 0:
            logging.debug("user is admin")
            return True
        else:
            logging.error("user is not an admin.")
            return False

    def install_python_modules(self):
        for module in self.modules:
            os.system("pip install {0}".format(module))

    def install_openvpn(self):
        os.system("apt-get install openvpn")
