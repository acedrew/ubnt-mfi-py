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


def output_conf(item, items=None, lines=None):
    if items is None:
        items = []
    if lines is None:
        lines = []
    if isinstance(item, defaultdict):
        for key, value in item.items():
            items.append(key)
            return output_conf(value, items, lines)
    elif isinstance(item, list):
        for value in item:
            items.append(1)
            return output_conf(value, items, lines)
    else:
        items.append('=')
        items.append(item)
        lines.append(items)
        print(lines)
        return output_conf(item, items, lines)


config = mfi.UbntConfig(config_text)
print(config.get_config_dump())
