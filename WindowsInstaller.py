import logging
import ctypes
import urllib3
import os


class WindowsInstaller:
    """
    functions for installing python modules and openvpn on windows operating systems
    """
    def __init__(self, modules):
        self.modules = modules
        self.is_admin()
        self.install_python_modules()
        self.install_openvpn()

    def is_admin(self):
        try:
            rights = ctypes.windll.shell32.IsUserAnAdmin()
        except Exception as e:
            logging.error("unable to determine user rights: {0}".format(e))
            return False
        if rights == 1:
            logging.debug("user is admin")
            return True
        else:
            logging.error("user is not an admin")
            return False

    def install_python_modules(self):
        for module in self.modules:
            os.system("pip install {0}".format(module))

    def install_openvpn(self):
        http = urllib3.PoolManager()
        r = http.request('GET', "https://swupdate.openvpn.org/community/releases/openvpn-install-2.4.4-I601.exe")
        path = "{0}/openvpn.exe".format(os.path.dirname(os.path.abspath(__file__)))
        print(path)
        with open(path, 'wb') as out:
            while True:
                data = r.read(1024)
                if not data:
                    break
                out.write(data)
            r.release_conn()
