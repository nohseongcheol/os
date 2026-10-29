#!/usr/bin/env python3
"""အိမ်ရှင် 루프백 주소에만 바인딩하는 UDP စမ်းသပ်မှု ဝန်ဆောင်စက်တန်ဖိုး. Ctrl+C로 종료한다."""
import argparse
import socket

def စက်မောင်း():
    တန်ဖိုးသဒ္ဒါခွဲခြမ်း = argparse.ArgumentParser(description='jkoros သုံးစွဲသူ UDP 예제의 로컬 ပြန်ပေးတံတား ဝန်ဆောင်စက်တန်ဖိုး')
    တန်ဖိုးသဒ္ဒါခွဲခြမ်း.add_argument('--port', type=int, default=9000)
    သတ်မှတ်အချက်ပေးအချက် = တန်ဖိုးသဒ္ဒါခွဲခြမ်း.parse_args()
    if not 1 <= သတ်မှတ်အချက်ပေးအချက်.port <= 65535: တန်ဖိုးသဒ္ဒါခွဲခြမ်း.error('ဆက်သွယ်ပေါက်တန်ဖိုး 번호는 1..65535')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as ဝန်ဆောင်စက်တန်ဖိုး:
        ဝန်ဆောင်စက်တန်ဖိုး.bind(('127.0.0.1', သတ်မှတ်အချက်ပေးအချက်.port))
        print('UDP 127.0.0.1:{} ပြင်ဆင်. Ctrl+C로 ထွက်ပရိုဂရမ်.'.format(သတ်မှတ်အချက်ပေးအချက်.port), flush=True)
        while True:
            ဒေတာ, တစ်ဖက်တန်ဖိုး = ဝန်ဆောင်စက်တန်ဖိုး.recvfrom(65535)
            ဝန်ဆောင်စက်တန်ဖိုး.sendto(ဒေတာ, တစ်ဖက်တန်ဖိုး)

if __name__ == '__main__':
    try: စက်မောင်း()
    except KeyboardInterrupt: pass
