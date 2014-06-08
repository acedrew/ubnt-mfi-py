import requests
import time
from collections import defaultdict


class UbntConfig:

    def parse_line(self, line_string, data):
        Tree = lambda: defaultdict(Tree)
        path, val = line_string.split('=')
        fields = path.split('.')
        prop = fields.pop()
        obj = data
        for f in fields:
            if f.isdigit():
                items = obj.setdefault('items', [])
                idx = int(f) - 1
                while len(items) < idx + 1:
                    items.append(Tree())
                obj = items[idx]
            else:
                obj = obj[f]

        obj[prop] = val
        return data

    def parse_config(self, conf):
        Tree = lambda: defaultdict(Tree)

        data = Tree()

        for line in conf.splitlines():
            if not line:
                continue
            data = self.parse_line(line, data)

        self.config = data
        return data


class MfiDevice:
    """Base class for all mFi devices"""
    def __init__(self,  url, user, passwd, cache_timeout=2000):

        """Provide a url to the mpower device, a username, and a password"""
        self.url = url
        self.user = user
        self.passwd = passwd
        self.cache_timeout = cache_timeout
        self.data_retrieved = 0
        self.session = requests.Session()
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
        if (time.time() - self.data_retrieved) > self.cache_timeout:
            r = self.session.get((self.url + "/mfi/sensors.cgi"))
            self.data_retrieved = time.time()
            self.data = r.json()
        return self.data

    def get_cfg(self):
        r = self.session.get(self.url + "/cfg.cgi")
        return r.text

    def set_cfg(self, config):
        files = {'file': ('config.cfg', config)}
        p = self.session.post((self.url + "/system.cgi"), files=files)
        return p.text


class MPower(MfiDevice):
    """Provides an interface to a single mPower Device"""

    def get_param(self, port_no, param):
        self.get_data()
        try:
            return self.data["sensors"][port_no - 1][param]
        except(KeyError, IndexError):
            print("Port #" + str(port_no) + " does not exist on this device")

    def get_power(self, port_no):
        return self.get_param(port_no, 'power')

    def switch(self, port_no, state="toggle"):
        if state == "toggle":
            current_state = self.get_param(port_no, 'output')
            if current_state:
                next_state = 0
            else:
                next_state = 1
        else:
            if int(state) == 0 or int(state) == 1:
                next_state = int(state)
        data = {"output": str(next_state)}
        self.session.put((self.url + "/sensors/" + str(port_no) + "/"),
                         data=data)


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
