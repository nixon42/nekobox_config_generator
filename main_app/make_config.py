#!/bin/python
import json

SELECTOR_BASE = {
    "type": "selector",
    "tag": 'Internet',
    "interrupt_exist_connections": False,
    "outbounds": [
        "Best Latency",
    ]
}

URLTEST_BASE = {
    "type": "urltest",
    "tag": "Best Latency",
    "outbounds": [
    ],
    "url": "https://detectportal.firefox.com/success.txt",
    "interval": "1m0s",
    "interrupt_exist_connections": False
}

OUTBOND = [
    {}
]

with open('raw.json') as handle:
    raw = json.load(handle)
    raw_outbond = raw['outbounds']

    for r in raw_outbond:
        if r['type'] in ('selector', 'urltest', 'direct', 'dns', 'block'):
            continue

        SELECTOR_BASE['outbounds'].append(r['tag'])
        URLTEST_BASE['outbounds'].append(r['tag'])
        OUTBOND.append(r)


with open('nekobox_base.json') as handle:
    data = json.load(handle)
    data['outbounds'] = [
        SELECTOR_BASE,
        URLTEST_BASE,
        *OUTBOND
    ]

    text = json.dumps(data, separators=(',', ':'))
    print(text)
