from urllib.parse import unquote
from urllib.parse import parse_qs
from urllib.parse import urlparse
import base64

DEFAULT_PORT = 443
DEFAULT_SECURITY = "auto"
DEFAULT_LEVEL = 8
DEFAULT_NETWORK = "tcp"

TLS = "tls"
REALITY = "reality"
HTTP = "http"



class EConfigType:
    class VMESS:
        protocolScheme = "vmess://"
        protocolName = "vmess"

    class CUSTOM:
        protocolScheme = ""
        protocolName = ""

    class SHADOWSOCKS:
        protocolScheme = "ss://"
        protocolName = "ss"

    class SOCKS:
        protocolScheme = "socks://"
        protocolName = "socks"

    class VLESS:
        protocolScheme = "vless://"
        protocolName = "vless"

    class TROJAN:
        protocolScheme = "trojan://"
        protocolName = "trojan"

    class WIREGUARD:
        protocolScheme = "wireguard://"
        protocolName = "wireguard"

    class FREEDOM:
        protocolScheme = "freedom://"
        protocolName = "freedom"

    class BLACKHOLE:
        protocolScheme = "blackhole://"
        protocolName = "blackhole"


class OutboundBean:
    class OutSettingsBean:
        class VnextBean:
            class UsersBean:
                id: str = ""
                alterId: int = None
                security: str = DEFAULT_SECURITY
                level: int = DEFAULT_LEVEL
                encryption: str = ""
                flow: str = ""

                def __init__(
                    self,
                    id: str = "",
                    alterId: int = None,
                    security: str = DEFAULT_SECURITY,
                    level: int = DEFAULT_LEVEL,
                    encryption: str = "",
                    flow: str = "",
                ) -> None:
                    self.id = id
                    self.alterId = alterId
                    self.security = security
                    self.level = level
                    self.encryption = encryption
                    self.flow = flow

            address: str = ""
            port: int = DEFAULT_PORT
            users: list[UsersBean]  # UsersBean

            def __init__(
                self,
                address: str = "",
                port: int = DEFAULT_PORT,
                users: list[UsersBean] = [],
            ) -> None:
                self.address = address
                self.port = port
                self.users = users

        class ServersBean:
            class SocksUsersBean:
                user: str = ""
                # @SerializedName("pass")
                _pass: str = ""
                level: int = DEFAULT_LEVEL

                def __init__(
                    self, user: str = "", _pass: str = "", level: int = DEFAULT_LEVEL
                ) -> None:
                    self.user = user
                    self._pass = _pass
                    self.level = level

            address: str = ""
            method: str = "chacha20-poly1305"
            ota: bool = False
            password: str = ""
            port: int = DEFAULT_PORT
            level: int = DEFAULT_LEVEL
            email: str = None
            flow: str = None
            ivCheck: bool = None
            users: list[SocksUsersBean] = None  # SocksUsersBean

            def __init__(
                self,
                address: str = "",
                method: str = "chacha20-poly1305",
                ota: bool = False,
                password: str = "",
                port: int = DEFAULT_PORT,
                level: int = DEFAULT_LEVEL,
                email: str = None,
                flow: str = None,
                ivCheck: bool = None,
                users: list[SocksUsersBean] = None,
            ) -> None:
                self.address = address
                self.method = method
                self.ota = ota
                self.password = password
                self.port = port
                self.level = level
                self.email = email
                self.flow = flow
                self.ivCheck = ivCheck
                self.users = users

        class Response:
            type: str

            def __init__(self, type: str) -> None:
                self.type = type

        class WireGuardBean:
            publicKey: str = ""
            endpoint: str = ""

            def __init__(self, publicKey: str = "", endpoint: str = "") -> None:
                self.publicKey = publicKey
                self.endpoint = endpoint

        vnext: list[VnextBean] = None  # VnextBean
        servers: list[ServersBean] = None  # ServersBean
        response: Response = None
        network: str = None
        address: str = None
        port: int = None
        domainStrategy: str = None
        redirect: str = None
        userLevel: int = None
        inboundTag: str = None
        secretKey: str = None
        peers: list[WireGuardBean] = None  # WireGuardBean

        def __init__(
            self,
            vnext: list[VnextBean] = None,
            servers: list[ServersBean] = None,
            response: Response = None,
            network: str = None,
            address: str = None,
            port: int = None,
            domainStrategy: str = None,
            redirect: str = None,
            userLevel: int = None,
            inboundTag: str = None,
            secretKey: str = None,
            peers: list[WireGuardBean] = None,
        ) -> None:
            self.vnext = vnext
            self.servers = servers
            self.response = response
            self.network = network
            self.address = address
            self.port = port
            self.domainStrategy = domainStrategy
            self.redirect = redirect
            self.userLevel = userLevel
            self.inboundTag = inboundTag
            self.secretKey = secretKey
            self.peers = peers

    class StreamSettingsBean:
        class TcpSettingsBean:
            class HeaderBean:
                class RequestBean:
                    class HeadersBean:
                        Host: list[str] = []  # str
                        # @SerializedName("User-Agent")
                        userAgent: list[str] = None  # str
                        # @SerializedName("Accept-Encoding")
                        acceptEncoding: list[str] = None  # str
                        Connection: list[str] = None  # str
                        Pragma: str = None

                        def __init__(
                            self,
                            Host: list[str] = [],
                            userAgent: list[str] = None,
                            acceptEncoding: list[str] = None,
                            Connection: list[str] = None,
                            Pragma: str = None,
                        ) -> None:
                            self.Host = Host
                            self.userAgent = userAgent
                            self.acceptEncoding = acceptEncoding
                            self.Connection = Connection
                            self.Pragma = Pragma

                    path: list[str] = []  # str
                    headers: HeadersBean = HeadersBean()
                    version: str = None
                    method: str = None

                    def __init__(
                        self,
                        path: list[str] = [],
                        headers: HeadersBean = HeadersBean(),
                        version: str = None,
                        method: str = None,
                    ) -> None:
                        self.path = path
                        self.headers = headers
                        self.version = version
                        self.method = method

                type: str = "none"
                request: RequestBean = None

                def __init__(
                    self, type: str = "none", request: RequestBean = None
                ) -> None:
                    self.type = type
                    self.request = request

            header: HeaderBean = HeaderBean()
            acceptProxyProtocol: bool = None

            def __init__(
                self,
                header: HeaderBean = HeaderBean(),
                acceptProxyProtocol: bool = None,
            ) -> None:
                self.header = header
                self.acceptProxyProtocol = acceptProxyProtocol

        class KcpSettingsBean:
            class HeaderBean:
                type: str = "none"

                def __init__(self, type: str = "none") -> None:
                    self.type = type

            mtu: int = 1350
            tti: int = 50
            uplinkCapacity: int = 12
            downlinkCapacity: int = 100
            congestion: bool = False
            readBufferSize: int = 1
            writeBufferSize: int = 1
            header: HeaderBean = HeaderBean()
            seed: str = None

            def __init__(
                self,
                mtu: int = 1350,
                tti: int = 50,
                uplinkCapacity: int = 12,
                downlinkCapacity: int = 100,
                congestion: bool = False,
                readBufferSize: int = 1,
                writeBufferSize: int = 1,
                header: HeaderBean = HeaderBean(),
                seed: str = None,
            ) -> None:
                self.mtu = mtu
                self.tti = tti
                self.uplinkCapacity = uplinkCapacity
                self.downlinkCapacity = downlinkCapacity
                self.congestion = congestion
                self.readBufferSize = readBufferSize
                self.writeBufferSize = writeBufferSize
                self.header = header
                self.seed = seed

        class WsSettingsBean:
            class HeadersBean:
                Host: str = ""

                def __init__(self, Host: str = "") -> None:
                    self.Host = Host

            path: str = ""
            headers: HeadersBean = HeadersBean()
            maxEarlyData: int = None
            useBrowserForwarding: bool = None
            acceptProxyProtocol: bool = None

            def __init__(
                self,
                path: str = "",
                headers: HeadersBean = HeadersBean(),
                maxEarlyData: int = None,
                useBrowserForwarding: bool = None,
                acceptProxyProtocol: bool = None,
            ) -> None:
                self.path = path
                self.headers = headers
                self.maxEarlyData = maxEarlyData
                self.useBrowserForwarding = useBrowserForwarding
                self.acceptProxyProtocol = acceptProxyProtocol

        class HttpSettingsBean:
            host: list[str] = []  # str
            path: str = ""

            def __init__(self, host: list[str] = [], path: str = "") -> None:
                self.host = host
                self.path = path

        class TlsSettingsBean:
            allowInsecure: bool = False
            serverName: str = ""
            alpn: list[str] = None  # str
            minVersion: str = None
            maxVersion: str = None
            preferServerCipherSuites: bool = None
            cipherSuites: str = None
            fingerprint: str = None
            certificates: list[any] = None  # any
            disableSystemRoot: bool = None
            enableSessionResumption: bool = None
            show: bool = False
            publicKey: str = None
            shortId: str = None
            spiderX: str = None

            def __init__(
                self,
                allowInsecure: bool = False,
                serverName: str = "",
                alpn: list[str] = None,
                minVersion: str = None,
                maxVersion: str = None,
                preferServerCipherSuites: bool = None,
                cipherSuites: str = None,
                fingerprint: str = None,
                certificates: list[any] = None,
                disableSystemRoot: bool = None,
                enableSessionResumption: bool = None,
                show: bool = False,
                publicKey: str = None,
                shortId: str = None,
                spiderX: str = None,
            ) -> None:
                self.allowInsecure = allowInsecure
                self.serverName = serverName
                self.alpn = alpn
                self.minVersion = minVersion
                self.maxVersion = maxVersion
                self.preferServerCipherSuites = preferServerCipherSuites
                self.cipherSuites = cipherSuites
                self.fingerprint = fingerprint
                self.certificates = certificates
                self.disableSystemRoot = disableSystemRoot
                self.enableSessionResumption = enableSessionResumption
                self.show = show
                self.publicKey = publicKey
                self.shortId = shortId
                self.spiderX = spiderX

        class QuicSettingBean:
            class HeaderBean:
                type: str = "none"

                def __init__(self, type: str = "none") -> None:
                    self.type = type

            security: str = "none"
            key: str = ""
            header: HeaderBean = HeaderBean()

            def __init__(
                self,
                security: str = "none",
                key: str = "",
                header: HeaderBean = HeaderBean(),
            ) -> None:
                self.security = security
                self.key = key
                self.header = header

        class GrpcSettingsBean:
            serviceName: str = ""
            multiMode: bool = None

            def __init__(self, serviceName: str = "", multiMode: bool = None) -> None:
                self.serviceName = serviceName
                self.multiMode = multiMode

        network: str = DEFAULT_NETWORK
        security: str = ""
        tcpSettings: TcpSettingsBean = None
        kcpSettings: KcpSettingsBean = None
        wsSettings: WsSettingsBean = None
        httpSettings: HttpSettingsBean = None
        tlsSettings: TlsSettingsBean = None
        quicSettings: QuicSettingBean = None
        realitySettings: TlsSettingsBean = None
        grpcSettings: GrpcSettingsBean = None
        dsSettings: any = None
        sockopt: any = None

        def __init__(
            self,
            network: str = DEFAULT_NETWORK,
            security: str = "",
            tcpSettings: TcpSettingsBean = None,
            kcpSettings: KcpSettingsBean = None,
            wsSettings: WsSettingsBean = None,
            httpSettings: HttpSettingsBean = None,
            tlsSettings: TlsSettingsBean = None,
            quicSettings: QuicSettingBean = None,
            realitySettings: TlsSettingsBean = None,
            grpcSettings: GrpcSettingsBean = None,
            dsSettings: any = None,
            sockopt: any = None,
        ) -> None:
            self.network = network
            self.security = security
            self.tcpSettings = tcpSettings
            self.kcpSettings = kcpSettings
            self.wsSettings = wsSettings
            self.httpSettings = httpSettings
            self.tlsSettings = tlsSettings
            self.quicSettings = quicSettings
            self.realitySettings = realitySettings
            self.grpcSettings = grpcSettings
            self.dsSettings = dsSettings
            self.sockopt = sockopt

        def populateTransportSettings(
            self,
            transport: str,
            headerType: str,
            host: str,
            path: str,
            seed: str,
            quicSecurity: str,
            key: str,
            mode: str,
            serviceName: str,
        ) -> str:
            sni = ""
            self.network = transport
            if self.network == "tcp":
                tcpSetting = self.TcpSettingsBean()
                if headerType == HTTP:
                    tcpSetting.header.type = HTTP
                    if host != "" or path != "":
                        requestObj = self.TcpSettingsBean.HeaderBean.RequestBean()
                        requestObj.headers.Host = (
                            "" if host == None else host.split(",")
                        )
                        requestObj.path = "" if path == None else path.split(
                            ",")
                        tcpSetting.header.request = requestObj
                        sni = (
                            requestObj.headers.Host[0]
                            if len(requestObj.headers.Host) > 0
                            else sni
                        )
                else:
                    tcpSetting.header.type = "none"
                    sni = host if host != "" else ""
                self.tcpSetting = tcpSetting

            elif self.network == "kcp":
                kcpsetting = self.KcpSettingsBean()
                kcpsetting.header.type = headerType if headerType != None else "none"
                if seed == None or seed == "":
                    kcpsetting.seed = None
                else:
                    kcpsetting.seed = seed
                self.kcpSettings = kcpsetting

            elif self.network == "ws":
                wssetting = self.WsSettingsBean()
                wssetting.headers.Host = host if host != None else ""
                sni = wssetting.headers.Host
                wssetting.path = path if path != None else "/"
                self.wsSettings = wssetting

            elif self.network == "h2" or self.network == "http":
                network = "h2"
                h2Setting = self.HttpSettingsBean()
                h2Setting.host = "" if host == None else host.split(",")
                sni = h2Setting.host[0] if len(h2Setting.host) > 0 else sni
                h2Setting.path = path if path != None else "/"
                self.httpSettings = h2Setting

            elif self.network == "quic":
                quicsetting = self.QuicSettingBean()
                quicsetting.security = quicSecurity if quicSecurity != None else "none"
                quicsetting.key = key if key != None else ""
                quicsetting.header.type = headerType if headerType != None else "none"
                self.quicSettings = quicsetting

            elif self.network == "grpc":
                grpcSetting = self.GrpcSettingsBean()
                grpcSetting.multiMode = mode == "multi"
                grpcSetting.serviceName = serviceName if serviceName != None else ""
                sni = host if host != None else ""
                self.grpcSettings = grpcSetting

            return sni

        def populateTlsSettings(
            self,
            streamSecurity: str,
            allowInsecure: bool,
            sni: str,
            fingerprint: str,
            alpns: str,
            publicKey: str,
            shortId: str,
            spiderX: str
        ):
            self.security = streamSecurity
            tlsSetting = self.TlsSettingsBean(
                allowInsecure=allowInsecure,
                serverName=sni,
                fingerprint=fingerprint,
                alpn=None if alpns == None or alpns == "" else alpns.split(
                    ","),
                publicKey=publicKey,
                shortId=shortId,
                spiderX=spiderX
            )

            if self.security == TLS:
                self.tlsSettings = tlsSetting
                self.realitySettings = None
            elif self.security == REALITY:
                self.tlsSettings = None
                self.realitySettings = tlsSetting

    class MuxBean:
        enabled: bool
        concurrency: int

        def __init__(self, enabled: bool, concurrency: int = 8):
            self.enabled = enabled
            self.concurrency = concurrency

    tag: str = "proxy"
    protocol: str
    settings: OutSettingsBean = None
    streamSettings: StreamSettingsBean = None
    proxySettings: any = None
    sendThrough: str = None
    mux: MuxBean = MuxBean(False)

    def __init__(
        self,
        tag: str = "proxy",
        protocol: str = None,
        settings: OutSettingsBean = None,
        streamSettings: StreamSettingsBean = None,
        proxySettings: any = None,
        sendThrough: str = None,
        mux: MuxBean = MuxBean(enabled=False),
    ):
        self.tag = tag
        self.protocol = protocol
        self.settings = settings
        self.streamSettings = streamSettings
        self.proxySettings = proxySettings
        self.sendThrough = sendThrough
        self.mux = mux


def get_outbound_vmess():
    outbound = OutboundBean(
        protocol=EConfigType.VMESS.protocolName,
        settings=OutboundBean.OutSettingsBean(
            vnext=[
                OutboundBean.OutSettingsBean.VnextBean(
                    users=[OutboundBean.OutSettingsBean.VnextBean.UsersBean()],
                ),
            ]
        ),
        streamSettings=OutboundBean.StreamSettingsBean(),
    )
    return outbound


def get_outbound_vless():
    outbound = OutboundBean(
        protocol=EConfigType.VLESS.protocolName,
        settings=OutboundBean.OutSettingsBean(
            vnext=[
                OutboundBean.OutSettingsBean.VnextBean(
                    users=[OutboundBean.OutSettingsBean.VnextBean.UsersBean()],
                ),
            ]
        ),
        streamSettings=OutboundBean.StreamSettingsBean(),
    )
    return outbound


def get_outbound_trojan():
    outbound = OutboundBean(
        protocol=EConfigType.TROJAN.protocolName,
        settings=OutboundBean.OutSettingsBean(
            servers=[OutboundBean.OutSettingsBean.ServersBean()]
        ),
        streamSettings=OutboundBean.StreamSettingsBean(),
    )
    return outbound


def get_outbound_ss():
    outbound = OutboundBean(
        protocol="shadowsocks",
        settings=OutboundBean.OutSettingsBean(
            servers=[OutboundBean.OutSettingsBean.ServersBean()]
        ),
        streamSettings=OutboundBean.StreamSettingsBean(),
    )
    return outbound


class VmessQRCode:
    v: str = ""
    ps: str = ""
    add: str = ""
    port: str = ""
    id: str = ""
    aid: str = "0"
    scy: str = ""
    net: str = ""
    type: str = ""
    host: str = ""
    path: str = ""
    tls: str = ""
    sni: str = ""
    alpn: str = ""
    allowInsecure: str = ""

    def __init__(
        self,
        v: str = "",
        ps: str = "",
        add: str = "",
        port: str = "",
        id: str = "",
        aid: str = "0",
        scy: str = "",
        net: str = "",
        type: str = "",
        host: str = "",
        path: str = "",
        tls: str = "",
        sni: str = "",
        alpn: str = "",
        allowInsecure: str = "",
        fp: str = "",
    ):
        self.v = v
        self.ps = ps
        self.add = add
        self.port = port
        self.id = id
        self.aid = aid
        self.scy = scy
        self.net = net
        self.type = type
        self.host = host
        self.path = path
        self.tls = tls
        self.sni = sni
        self.alpn = alpn
        self.allowInsecure = allowInsecure
        self.fp = fp


def remove_nulls(d):
    if isinstance(d, dict):
        for k, v in list(d.items()):
            if v is None:
                del d[k]
            else:
                remove_nulls(v)
    if isinstance(d, list):
        for v in d:
            remove_nulls(v)
    return d


class Fingerprint:
    randomized = "randomized"
    randomizedalpn = "randomizedalpn"
    randomizednoalpn = "randomizednoalpn"
    firefox_auto = "firefox_auto"
    chrome_auto = "chrome_auto"
    ios_auto = "ios_auto"
    android_11_okhttp = "android_11_okhttp"
    edge_auto = "edge_auto"
    safari_auto = "safari_auto"
    _360_auto = "360_auto"
    qq_auto = "qq_auto"


def try_resolve_resolve_sip002(str: str, config: OutboundBean):
    try:
        uri = urlparse(str)
        config.remarks = unquote(uri.fragment or "")

        if ":" in uri.username:
            arr_user_info = list(map(str.strip, uri.username.split(":")))
            if len(arr_user_info) != 2:
                return False
            method = arr_user_info[0]
            password = unquote(arr_user_info[1])
        else:
            base64_decode = base64.b64decode(uri.username).decode(
                encoding="utf-8", errors="ignore")
            arr_user_info = list(map(str.strip, base64_decode.split(":")))
            if len(arr_user_info) < 2:
                return False
            method = arr_user_info[0]
            password = base64_decode.split(":", 1)[1]

        server = config.outbound_bean.settings.servers[0]
        server.address = uri.hostname
        server.port = uri.port
        server.password = password
        server.method = method

        return True
    except Exception as e:
        return False
