import requests


class MPower:
    """Provides an interface to a single mPower Device"""

    def __init__(self,  url=None, user=None, passwd=None):
        if user is not None and passwd is not None and url is not None:
            self.url = url
            self.user = user
            self.passwd = passwd
            self.session = requests.Session()
            self.session.get(url)
            self.login()

    def login(self):
        post_data = {"uri": "mfi/sensors.cgi", "username": self.user,
                     "password": self.passwd}
        headers = {"Expect": ""}
        self.session.post((self.url + "/login.cgi"),
                          headers=headers, data=post_data,
                          allow_redirects=True)

    def get_data(self):
        r = self.session.get((self.url + "/mfi/sensors.cgi"))
        return r.json()
