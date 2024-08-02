import json
import streamlit as st
from main_app.convert import convert_to_dict, generate_config

st.title("Nekobox Custom Config Generator")
st.markdown("Aplikasi streamlit sederhana untuk membuat konfigurasi "
            "[NekoBox](https://github.com/MatsuriDayo/NekoBoxForAndroid), "
            "yang saat ini hanya mendukung protokol :blue-background[VMESS] dan :blue-background[VLESS]"
            "dengan transport :blue-background[WebSocket]."
            " Anda dapat membuat konfigurasi dengan "
            "mudah dengan menggunakan protokol yang di support.")
st.warning(
    "Pisahkan dengan enter/newline, contoh: vmess://... (enter)vmess://.../  (enter)vless://...")

config = st.text_area("V2Ray Config", height=100, key="config",
                      placeholder="masukan config v2ray disini")
if st.button("Generate", type="primary"):
    list_raw_config = config.strip().split("\n")
    list_outbond = []
    for i in list_raw_config:
        raw_config = i.strip()
        res = convert_to_dict(raw_config)
        list_outbond.append(res)

    res = generate_config(list_outbond)
    st.write("Hasil")
    st.code(json.dumps(res, indent=4))

st.markdown("""<a href="https://github.com/nixon42/nekobox_config_generator"><svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="50" height="50" viewBox="0,0,256,256">
<g fill="#ffffff" fill-rule="nonzero" stroke="none" stroke-width="1" stroke-linecap="butt" stroke-linejoin="miter" stroke-miterlimit="10" stroke-dasharray="" stroke-dashoffset="0" font-family="none" font-weight="none" font-size="none" text-anchor="none" style="mix-blend-mode: normal"><g transform="scale(8.53333,8.53333)"><path d="M15,3c-6.627,0 -12,5.373 -12,12c0,5.623 3.872,10.328 9.092,11.63c-0.056,-0.162 -0.092,-0.35 -0.092,-0.583v-2.051c-0.487,0 -1.303,0 -1.508,0c-0.821,0 -1.551,-0.353 -1.905,-1.009c-0.393,-0.729 -0.461,-1.844 -1.435,-2.526c-0.289,-0.227 -0.069,-0.486 0.264,-0.451c0.615,0.174 1.125,0.596 1.605,1.222c0.478,0.627 0.703,0.769 1.596,0.769c0.433,0 1.081,-0.025 1.691,-0.121c0.328,-0.833 0.895,-1.6 1.588,-1.962c-3.996,-0.411 -5.903,-2.399 -5.903,-5.098c0,-1.162 0.495,-2.286 1.336,-3.233c-0.276,-0.94 -0.623,-2.857 0.106,-3.587c1.798,0 2.885,1.166 3.146,1.481c0.896,-0.307 1.88,-0.481 2.914,-0.481c1.036,0 2.024,0.174 2.922,0.483c0.258,-0.313 1.346,-1.483 3.148,-1.483c0.732,0.731 0.381,2.656 0.102,3.594c0.836,0.945 1.328,2.066 1.328,3.226c0,2.697 -1.904,4.684 -5.894,5.097c1.098,0.573 1.899,2.183 1.899,3.396v2.734c0,0.104 -0.023,0.179 -0.035,0.268c4.676,-1.639 8.035,-6.079 8.035,-11.315c0,-6.627 -5.373,-12 -12,-12z"></path></g></g>
</svg> Source Code </a>

            
<a href="https://t.me/niponxd"><svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="45" height="45" viewBox="0,0,256,256">
<g fill="#ffffff" fill-rule="nonzero" stroke="none" stroke-width="1" stroke-linecap="butt" stroke-linejoin="miter" stroke-miterlimit="10" stroke-dasharray="" stroke-dashoffset="0" font-family="none" font-weight="none" font-size="none" text-anchor="none" style="mix-blend-mode: normal"><g transform="scale(5.12,5.12)"><path d="M25,2c12.703,0 23,10.297 23,23c0,12.703 -10.297,23 -23,23c-12.703,0 -23,-10.297 -23,-23c0,-12.703 10.297,-23 23,-23zM32.934,34.375c0.423,-1.298 2.405,-14.234 2.65,-16.783c0.074,-0.772 -0.17,-1.285 -0.648,-1.514c-0.578,-0.278 -1.434,-0.139 -2.427,0.219c-1.362,0.491 -18.774,7.884 -19.78,8.312c-0.954,0.405 -1.856,0.847 -1.856,1.487c0,0.45 0.267,0.703 1.003,0.966c0.766,0.273 2.695,0.858 3.834,1.172c1.097,0.303 2.346,0.04 3.046,-0.395c0.742,-0.461 9.305,-6.191 9.92,-6.693c0.614,-0.502 1.104,0.141 0.602,0.644c-0.502,0.502 -6.38,6.207 -7.155,6.997c-0.941,0.959 -0.273,1.953 0.358,2.351c0.721,0.454 5.906,3.932 6.687,4.49c0.781,0.558 1.573,0.811 2.298,0.811c0.725,0 1.107,-0.955 1.468,-2.064z"></path></g></g>
</svg> @niponxd on Telegram</a> 
""", unsafe_allow_html=True)

st.write("Credit: \n\n"
         "- [NekoBox](https://github.com/MatsuriDayo/NekoBoxForAndroid)\n\n"
         "- [V2Ray](https://github.com/v2fly/v2ray-core)\n\n"
         "- [v2ray2json](https://github.com/arminmokri/v2ray2json)"
         )
