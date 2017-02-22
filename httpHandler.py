import urllib.request
import urllib.parse

class HTTPRequest:
    def __init__(self, root):
        self.root = root

    def POST(self, address, data):
        data = urllib.parse.urlencode(data)
        data = data.encode('utf8')
        req = urllib.request.Request(self.root+address, data)

        return urllib.request.urlopen(req).read().decode('utf-8')

    def GET(self, address, data):
        data = urllib.parse.urlencode(data)
        req = urllib.request.Request(self.root+address+'?'+data)

        return urllib.request.urlopen(req).read().decode('utf-8')
