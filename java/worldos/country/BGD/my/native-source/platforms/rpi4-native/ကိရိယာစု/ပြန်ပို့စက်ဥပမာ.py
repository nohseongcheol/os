#!/usr/bin/env python3
"""မြန်မာ ကွန်ရက်ဆက် 예제용 အိမ်ရှင် TCP/UDP 응답기 (localhost)."""
import argparse
import socketserver
import threading
import time


class 되돌림서버:
    def __init__(자신,TCPဆက်သွယ်ပေါက်=0,UDPဆက်သွယ်ပေါက်=0):
        자신.수신됨=[];자신.အလုပ်ကြိုးများ=[]
        수신됨=자신.수신됨
        class ကိုင်တွယ်ရာချိတ်ဆက်မှုတောင်းဆိုချက်(socketserver.BaseRequestHandler):
            def handle(자신):
                자신.request.settimeout(5);ဒေတာ=bytearray()
                while b'\n' not in ဒေတာ and len(ဒေတာ)<=512:
                    အစိတ်အပိုင်း=자신.request.recv(512)
                    if not အစိတ်အပိုင်း:return
                    ဒေတာ.extend(အစိတ်အပိုင်း)
                수신됨.append(('tcp',bytes(ဒေတာ)));자신.request.sendall(ဒေတာ)
        class ဒေတာစာကိုင်တွယ်ရာတောင်းဆိုချက်(socketserver.BaseRequestHandler):
            def handle(자신):
                ဒေတာ,ကွန်ရက်ပေါက်တန်ဖိုး=자신.request;수신됨.append(('udp',ဒေတာ));ကွန်ရက်ပေါက်တန်ဖိုး.sendto(ဒေတာ,자신.client_address)
        자신.ချိတ်ဆက်မှုထိန်းချုပ်=socketserver.ThreadingTCPServer(('127.0.0.1',TCPဆက်သွယ်ပေါက်),ကိုင်တွယ်ရာချိတ်ဆက်မှုတောင်းဆိုချက်)
        try:자신.ဒေတာစာထိန်းချုပ်=socketserver.ThreadingUDPServer(('127.0.0.1',UDPဆက်သွယ်ပေါက်),ဒေတာစာကိုင်တွယ်ရာတောင်းဆိုချက်)
        except Exception:자신.ချိတ်ဆက်မှုထိန်းချုပ်.server_close();raise
        자신.ချိတ်ဆက်မှုထိန်းချုပ်.daemon_threads=자신.ဒေတာစာထိန်းချုပ်.daemon_threads=True
        자신.TCPဆက်သွယ်ပေါက်=자신.ချိတ်ဆက်မှုထိန်းချုပ်.server_address[1];자신.UDPဆက်သွယ်ပေါက်=자신.ဒေတာစာထိန်းချုပ်.server_address[1]

    def __enter__(자신):
        for ဝန်ဆောင်စက်တန်ဖိုး in (자신.ချိတ်ဆက်မှုထိန်းချုပ်,자신.ဒေတာစာထိန်းချုပ်):
            အလုပ်သမား=threading.Thread(target=ဝန်ဆောင်စက်တန်ဖိုး.serve_forever,kwargs={'poll_interval':.1},daemon=True)
            အလုပ်သမား.start();자신.အလုပ်ကြိုးများ.append(အလုပ်သမား)
        return 자신

    def __exit__(자신,*ပေးအချက်အခင်းအကျင်း):
        for ဝန်ဆောင်စက်တန်ဖိုး in (자신.ချိတ်ဆက်မှုထိန်းချုပ်,자신.ဒေတာစာထိန်းချုပ်):ဝန်ဆောင်စက်တန်ဖိုး.shutdown();ဝန်ဆောင်စက်တန်ဖိုး.server_close()
        for အလုပ်သမား in 자신.အလုပ်ကြိုးများ:အလုပ်သမား.join(timeout=1)


if __name__=='__main__':
    인수해석기=argparse.ArgumentParser(description=__doc__)
    인수해석기.add_argument('--tcp-port',type=int,default=9000);인수해석기.add_argument('--udp-port',type=int,default=9001)
    ပေးအချက်အခင်းအကျင်း=인수해석기.parse_args()
    with 되돌림서버(ပေးအချက်အခင်းအကျင်း.tcp_port,ပေးအချက်အခင်းအကျင်း.udp_port) as ပြန်ပို့ဝန်ဆောင်စက်အချက်:
        print('အိမ်ရှင် TCP {}, UDP {} ပြင်ဆင်. 게스트 လိပ်စာ: 10.0.2.2. ထွက်ပရိုဂရမ်: Ctrl+C'.format(ပြန်ပို့ဝန်ဆောင်စက်အချက်.TCPဆက်သွယ်ပေါက်,ပြန်ပို့ဝန်ဆောင်စက်အချက်.UDPဆက်သွယ်ပေါက်),flush=True)
        try:
            while True:time.sleep(.2)
        except KeyboardInterrupt:pass
