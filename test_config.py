import mfi
import os
import json
from collections import defaultdict


def save_config():
    test_mpower = mfi.MPower(os.environ['TESTMPOWER'], os.environ['TESTUSER'],
                             os.environ['TESTPASS'])
    test_config = test_mpower.get_cfg()
    with open('mpower.cfg', 'r+') as f:
        f.write(test_config)


def load_config():
    with open('mpower.cfg', 'r+') as f:
        test_config = f.read()
    return test_config

config_text = load_config()


def parse_config(conf):
    def Tree():
        return defaultdict(Tree)

    data = Tree()

    for line in conf.splitlines():
        if not line:
            continue
        path, val = line.split('=')
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

config = mfi.UbntConfig()
print(json.dumps(config.parse_config(config_text), indent=2))


