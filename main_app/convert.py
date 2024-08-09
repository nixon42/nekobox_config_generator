from .utils import get_outbound_ss, get_outbound_trojan, get_outbound_vless, get_outbound_vmess, remove_nulls, try_resolve_resolve_sip002
from .utils import EConfigType, OutboundBean, Fingerprint, VmessQRCode
import base64
import json
import copy

import re
from urllib.parse import urlparse
from urllib.parse import parse_qs
from urllib.parse import unquote


DEFAULT_PORT = 443
DEFAULT_SECURITY = "auto"
DEFAULT_LEVEL = 8
DEFAULT_NETWORK = "tcp"

TLS = "tls"
REALITY = "reality"
HTTP = "http"

SELECTOR_BASE = {
    "type": "selector",
    "tag": 'Internet',
    "interrupt_exist_connections": False,
    "outbounds": [
        "Best Latency",
        "block",
        "direct"
    ]
}

URLTEST_BASE = {
    "type": "urltest",
    "tag": "Best Latency",
    "outbounds": [
    ],
    "url": "https://detectportal.firefox.com/success.txt",
    "interval": "120m",
    "interrupt_exist_connections": False
}

OUTBOND = [
    {
        "tag": "direct",
        "type": "direct"
    },
    {
        "tag": "block",
        "type": "block"
    },
    {
        "tag": "dns-out",
        "type": "dns"
    }
]


def convert_to_dict(config: str) -> dict:
    temp = config.split("://")
    protocol = temp[0]
    raw_config = temp[1]

    if protocol == EConfigType.VMESS.protocolName:
        allowInsecure = True
        _len = len(raw_config)
        if _len % 4 > 0:
            raw_config += "=" * (4 - _len % 4)

        b64decode = base64.b64decode(raw_config).decode(
            encoding="utf-8", errors="ignore")
        _json = json.loads(b64decode, strict=False)

        vmessQRCode_attributes = list(
            VmessQRCode.__dict__["__annotations__"].keys())
        for key in list(_json.keys()):
            if key not in vmessQRCode_attributes:
                del _json[key]

        vmessQRCode = VmessQRCode(**_json)

        outbound = get_outbound_vmess()

        vnext = outbound.settings.vnext[0]
        vnext.address = vmessQRCode.add
        vnext.port = int(
            vmessQRCode.port) if vmessQRCode.port.isdigit() else DEFAULT_PORT

        user = vnext.users[0]
        user.id = vmessQRCode.id
        user.security = vmessQRCode.scy if vmessQRCode.scy != "" else DEFAULT_SECURITY
        user.alterId = int(
            vmessQRCode.aid) if vmessQRCode.aid.isdigit() else None

        streamSetting = outbound.streamSettings

        sni = streamSetting.populateTransportSettings(
            transport=vmessQRCode.net,
            headerType=vmessQRCode.type,
            host=vmessQRCode.host,
            path=vmessQRCode.path,
            seed=vmessQRCode.path,
            quicSecurity=vmessQRCode.host,
            key=vmessQRCode.path,
            mode=vmessQRCode.type,
            serviceName=vmessQRCode.path,
        )

        fingerprint = vmessQRCode.fp if vmessQRCode.fp else streamSetting.tlsSettings.fingerprint if streamSetting.tlsSettings else None

        streamSetting.populateTlsSettings(
            streamSecurity=vmessQRCode.tls,
            allowInsecure=allowInsecure,
            sni=sni if vmessQRCode.sni == "" else vmessQRCode.sni,
            fingerprint=fingerprint,
            alpns=vmessQRCode.alpn,
            publicKey=None,
            shortId=None,
            spiderX=None
        )
        outbound.tag = vmessQRCode.ps
        v2rayConfig_str_json = json.dumps(
            outbound, default=vars)
        res = json.loads(v2rayConfig_str_json)
        res = remove_nulls(res)

        return res

    elif protocol == EConfigType.VLESS.protocolName:
        allowInsecure = True
        parsed_url = urlparse(config)
        _netloc = parsed_url.netloc.split("@")

        name = parsed_url.fragment
        uid = _netloc[0]
        hostname = _netloc[1].rsplit(":", 1)[0]
        port = int(_netloc[1].rsplit(":", 1)[1])

        netquery = dict(
            (k, v if len(v) > 1 else v[0])
            for k, v in parse_qs(parsed_url.query).items()
        )

        outbound = get_outbound_vless()
        outbound.tag = name

        streamSetting = outbound.streamSettings
        fingerprint = (
            streamSetting.tlsSettings.fingerprint
            if streamSetting.tlsSettings != None
            else None
        )

        vnext = outbound.settings.vnext[0]
        vnext.address = hostname
        vnext.port = port

        user = vnext.users[0]
        user.id = uid
        user.encryption = netquery.get("encryption", "none")
        user.flow = netquery.get("flow", "")

        sni = streamSetting.populateTransportSettings(
            transport=netquery.get("type", "tcp"),
            headerType=netquery.get("headerType", None),
            host=netquery.get("host", None),
            path=netquery.get("path", None),
            seed=netquery.get("seed", None),
            quicSecurity=netquery.get("quicSecurity", None),
            key=netquery.get("key", None),
            mode=netquery.get("mode", None),
            serviceName=netquery.get("serviceName", None),
        )
        streamSetting.populateTlsSettings(
            streamSecurity=netquery.get("security", ""),
            allowInsecure=allowInsecure,
            sni=sni if netquery.get(
                "sni", None) == None else netquery.get("sni", None),
            fingerprint=fingerprint,
            alpns=netquery.get("alpn", None),
            publicKey=netquery.get("pbk", ""),
            shortId=netquery.get("sid", ""),
            spiderX=netquery.get("spx", ""),
        )

        # v2rayConfig = V2rayConfig(
        #     _comment=Comment(remark=name),
        #     log=get_log(),
        #     inbounds=[get_inbound()],
        #     outbounds=[outbound, get_outbound1(), get_outbound2()],
        #     dns=get_dns(dns_list=dns_list),
        #     routing=get_routing(),
        # )

        v2rayConfig_str_json = json.dumps(outbound, default=vars)

        res = json.loads(v2rayConfig_str_json)
        res = remove_nulls(res)

        return res

    elif protocol == EConfigType.TROJAN.protocolName:

        parsed_url = urlparse(config)
        _netloc = parsed_url.netloc.split("@")

        name = parsed_url.fragment
        uid = _netloc[0]
        hostname = _netloc[1].rsplit(":", 1)[0]
        port = int(_netloc[1].rsplit(":", 1)[1])

        netquery = dict(
            (k, v if len(v) > 1 else v[0])
            for k, v in parse_qs(parsed_url.query).items()
        )

        outbound = get_outbound_trojan()

        streamSetting = outbound.streamSettings

        flow = ""
        fingerprint = (
            streamSetting.tlsSettings.fingerprint
            if streamSetting.tlsSettings != None
            else Fingerprint.randomized
        )

        if len(netquery) > 0:
            sni = streamSetting.populateTransportSettings(
                transport=netquery.get("type", "tcp"),
                headerType=netquery.get("headerType", None),
                host=netquery.get("host", None),
                path=netquery.get("path", None),
                seed=netquery.get("seed", None),
                quicSecurity=netquery.get("quicSecurity", None),
                key=netquery.get("key", None),
                mode=netquery.get("mode", None),
                serviceName=netquery.get("serviceName", None),
            )

            streamSetting.populateTlsSettings(
                streamSecurity=netquery.get("security", TLS),
                allowInsecure=allowInsecure,
                sni=sni if netquery.get(
                    "sni", None) == None else netquery.get("sni", None),
                fingerprint=fingerprint,
                alpns=netquery.get("alpn", None),
                publicKey=None,
                shortId=None,
                spiderX=None,
            )

            flow = netquery.get("flow", "")

        else:
            streamSetting.populateTlsSettings(
                streamSecurity=TLS,
                allowInsecure=allowInsecure,
                sni="",
                fingerprint=fingerprint,
                alpns=None,
                publicKey=None,
                shortId=None,
                spiderX=None,
            )

        server = outbound.settings.servers[0]
        server.address = hostname
        server.port = port
        server.password = uid
        server.flow = flow

        # v2rayConfig = V2rayConfig(
        #     _comment=Comment(remark=name),
        #     log=get_log(),
        #     inbounds=[get_inbound()],
        #     outbounds=[outbound, get_outbound1(), get_outbound2()],
        #     dns=get_dns(dns_list=dns_list),
        #     routing=get_routing(),
        # )

        v2rayConfig_str_json = json.dumps(outbound, default=vars)

        res = json.loads(v2rayConfig_str_json)
        res = remove_nulls(res)

        return res

    elif protocol == EConfigType.SHADOWSOCKS.protocolName:
        outbound = get_outbound_ss()
        if not try_resolve_resolve_sip002(raw_config, outbound):
            result = raw_config.replace(
                EConfigType.SHADOWSOCKS.protocolScheme, "")
            index_split = result.find("#")
            if index_split > 0:
                try:
                    outbound.remarks = unquote(result[index_split + 1:])
                except Exception as e:
                    None  # print(e)

                result = result[:index_split]

            # part decode
            index_s = result.find("@")
            result = base64.b64decode(result[:index_s]).decode(encoding="utf-8", errors="ignore") + \
                result[index_s:] if index_s > 0 else base64.b64decode(
                    result).decode(encoding="utf-8", errors="ignore")

            legacy_pattern = re.compile(r'^(.+?):(.*)@(.+):(\d+)\/?.*$')
            match = legacy_pattern.match(result)

            if not match:
                raise Exception("Incorrect protocol")

            server = outbound.settings.servers[0]
            server.address = match.group(3).strip("[]")
            server.port = int(match.group(4))
            server.password = match.group(2)
            server.method = match.group(1).lower()

        #     v2rayConfig = V2rayConfig(
        #         _comment=Comment(remark=outbound.remarks),
        #         log=get_log(),
        #         inbounds=[get_inbound()],
        #         outbounds=[outbound, get_outbound1(), get_outbound2()],
        #         dns=get_dns(dns_list=dns_list),
        #         routing=get_routing(),
        #     )

            v2rayConfig_str_json = json.dumps(outbound, default=vars)

        res = json.loads(v2rayConfig_str_json)
        res = remove_nulls(res)

        return res


def gen_settings(protocol: str, mux: dict, server: dict, user: dict) -> dict:
    base = {
        "server": server['address'],
        "server_port": server['port'],
        "uuid": user['id'],
        "multiplex": {
            "enabled": mux['enabled'],
            "max_streams": mux['concurrency'],
            "protocol": "smux"
        },
        "domain_strategy": "ipv4_only"
    }

    if protocol == "vmess":
        pass
    elif protocol == "vless":
        pass
    return base


def gen_transport(stream_settings: dict) -> dict:
    transport = stream_settings['network']
    if transport == "ws":
        return {
            "type": "ws",
            "path": stream_settings['wsSettings']['path'],
            "headers": {
                    "Host": stream_settings['wsSettings']['headers']['Host']
            },
            "max_early_data": 0,
            "early_data_header_name": "Sec-WebSocket-Protocol"
        }


def generate_config(outbond: list[dict]) -> str:
    domain_suffix = []
    sing_box_outbond = []
    selector = copy.deepcopy(SELECTOR_BASE)
    urltest = copy.deepcopy(URLTEST_BASE)

    with open("main_app/nekobox_base.json") as f:
        data = json.load(f)

    for out in outbond:
        server = out["settings"]['vnext'][0]
        user = server['users'][0]
        stream_settings = out["streamSettings"]
        mux = out["mux"]

        protocol = out["protocol"]

        settings = gen_settings(protocol, mux, server, user)

        settings["transport"] = gen_transport(stream_settings)

        sing_box_outbond.append(
            {"tag": out["tag"], "type": protocol, **settings})

        domain_suffix.append(server["address"])
        selector["outbounds"].append(out["tag"])
        urltest["outbounds"].append(out["tag"])

    domain_suffix = list(set(domain_suffix))
    data['dns']['rules'][0]['domain_suffix'] = domain_suffix
    data['outbounds'] = [
        selector,
        urltest,
        *OUTBOND,
        *sing_box_outbond
    ]
    return data
