import requests
import time


class MfiDevice:
    """Base class for all mFi devices"""
    def __init__(self,  url, user, passwd):

        """Provide a url to the mpower device, a username, and a password"""
        self.url = url
        self.user = user
        self.passwd = passwd
        self.session = requests.Session()
        self.data_retrieved = 0
        #This get is necessary to set a cookie in the session prior to trying
        #to login might be better to stick it in the login method itself
        self.session.get(url)
        self.login()

    def login(self):
        post_data = {"uri": "/", "username": self.user,
                     "password": self.passwd}
        headers = {"Expect": ""}
        self.session.post((self.url + "/login.cgi"),
                          headers=headers, data=post_data,
                          allow_redirects=True)

    def get_data(self):
        if (time.time() - self.data_retrieved) > 2000:
            r = self.session.get((self.url + "/mfi/sensors.cgi"))
            self.data_retrieved = time.time()
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

    def get_temperature(self, port_no, temp_format='c'):
        self.get_data()
        try:
            sensor = self.data['sensors'][port_no - 1]
            if "model" in sensor and sensor['model'] == 'Ubiquiti mFi-THS':
                if temp_format == "c":
                    return sensor['analog'] * 30 - 10
                elif temp_format == "f":
                    return (sensor['analog'] * 30 - 10) * 1.8 + 32
            else:
                raise IndexError
        except(IndexError):
            print("Sorry port #" + str(port_no) +
                    " either does not exist or is not a Temperature Sensor")
