import requests


class MfiDevice:
    """Base class for all mFi devices"""
    def __init__(self,  url, user, passwd):

        """Provide a url to the mpower device, a username, and a password"""
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
        self.data = r.json()
        return self.data


class MPower(MfiDevice):
    """Provides an interface to a single mPower Device"""

    def get_power(self, port_no):
        self.get_data()
        try:
            return self.data["sensors"][port_no - 1]["power"]
        except(KeyError, IndexError):
            print("Port #" + str(port_no) + " does not exist on this device")


class MPort(MfiDevice):
    """Provides an API to a single mPort Device"""

    def get_temperature(self, format='c'):
        self.get_data()
