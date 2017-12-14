import os
import json
import random
from twisted.web.static import File
from twisted.internet import reactor, ssl
from twisted.web import server
from twisted.web.resource import Resource

sslContext = ssl.DefaultOpenSSLContextFactory(
    'severedsec.key',  # Private Key
    'severedsec.crt',  # Certificate
)


class VPNServerManager(Resource):

    def __init__(self):
        Resource.__init__(self)
        self.serverRoot = os.getcwd()
        self.pages = {b'/': self.root_get,
                      b'/servers': self.servers_json}

    def getChild(self, name, request):
        return self

    def render_GET(self, request):
        print(request.uri)
        try:
            return self.pages[request.uri](request)
        except KeyError:
            return self.page_not_found(request)

    def root_get(self, request):
        """
        notification page
        :param request:
        :return:
        """
        response = """
        <HTML>
        <div> this server is used for the SeveredSec VPN Connection Manager. It provides information on available </div>
        <div> SeveredSec VPN servers and provides the most up to date configs for the clients to use. Developers </div>
        <div> are welcome to use the endpoints on this server to develop their own applications or assist in </div>
        <div> developing the Connection Manager.</div>
        <p> If you discover any bugs please email Rod at roderick.a.daniels@gmail.com</p>
        <div> available endpoints: </div>
        <div> / : this page </div>
        <div> /servers : JSON list of servers </div>
        </HTML>
        """
        return bytes(response, encoding='utf8')

    def servers_json(self, request):
        """
        :param request:
        :return: a list of servers hosted by severedsec as a JSON
        """
        response = '[{"name": "dev.severedsec.com", "IP": "45.79.156.23", "status": "online", "config": "/configs/dev.ovpn"}]'
        return bytes(response, encoding='utf8')

    # 404 error
    def page_not_found(self, request):
        return bytes("the page you requested [{0}] does not exist".format(str(request.uri)), encoding="utf8")


site = server.Site(VPNServerManager())
reactor.listenSSL(8000, site, sslContext)
reactor.run()
