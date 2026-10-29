#!/usr/bin/env python3
"""장치별 သော့တန်ဖိုး·ချိတ်ဆက်မှု 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

စီမံကိန်းအမြစ် = Path(__file__).resolve().parents[1]


def ပြင်ဆင်(စီမံကိန်းအမြစ်=စီမံကိန်းအမြစ်):
    လမ်း = စီမံကိန်းအမြစ် / 'build/remote'
    လမ်း.mkdir(parents=True, exist_ok=True)
    သတ်မှတ်ချက် = လမ်း / 'access.json'
    သော့တန်ဖိုး = လမ်း / 'host-key.der'
    if not သော့တန်ဖိုး.exists():
        with သော့တန်ဖိုး.open('xb') as ဖိုင်:
            os.chmod(str(သော့တန်ဖိုး), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=ဖိုင်)
    if not သတ်မှတ်ချက်.exists():
        ဒေတာ = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with သတ်မှတ်ချက်.open('x') as ဖိုင်:
            os.chmod(str(သတ်မှတ်ချက်), 0o600)
            json.dump(ဒေတာ, ဖိုင်, ensure_ascii=False, indent=2)
            ဖိုင်.write('\n')
    ဒေတာ = json.loads(သတ်မှတ်ချက်.read_text())
    if not isinstance(ဒေတာ, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if ဒေတာ.get('user') != 'user':
        raise SystemExit('access.json: user는 လက်ရှိအချက်အလက်တစ်ခု "user"만 지원합니다.')
    for အမည် in ('ssh_password', 'vnc_password'):
        if not isinstance(ဒေတာ.get(အမည်), str):
            raise SystemExit('access.json: ' + အမည် + '는 문자열이어야 합니다.')
    အမိန့်ဝင်းစကားဝှက် = ဒေတာ['ssh_password'].encode('utf-8')
    if len(အမိန့်ဝင်းစကားဝှက်) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        မျက်နှာပြင်စကားဝှက် = ဒေတာ['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. အလျား 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    မျက်နှာပြင်သော့ = မျက်နှာပြင်စကားဝှက်[:8].ljust(8, b'\0')
    def အခင်းအကျင်းတန်ဖိုး(အမည်, တန်ဖိုး):
        return 'static const unsigned char '+အမည်+'[] = {'+','.join(str(ကိန်းတန်ဖိုး) for ကိန်းတန်ဖိုး in တန်ဖိုး)+'};\n'
    ဦးခေါင်းတန်ဖိုး = အခင်းအကျင်းတန်ဖိုး('ကိရိယာသော့', သော့တန်ဖိုး.read_bytes())
    ဦးခေါင်းတန်ဖိုး += အခင်းအကျင်းတန်ဖိုး('အမိန့်ဝင်းစကားဝှက်အကျဉ်းချုပ်', hashlib.sha256(အမိန့်ဝင်းစကားဝှက်).digest())
    ဦးခေါင်းတန်ဖိုး += အခင်းအကျင်းတန်ဖိုး('မျက်နှာပြင်စကားဝှက်', မျက်နှာပြင်သော့)
    ထုတ်လုပ် = လမ်း / 'ချိတ်ဆက်ပုံစံ.h'
    ထုတ်လုပ်.write_text(ဦးခေါင်းတန်ဖိုး)
    os.chmod(str(ထုတ်လုပ်), 0o600)
    return ဒေတာ


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('လှုပ်ရှားမှု', choices=['show', 'prepare'], nargs='?', default='prepare')
    အချက်များ = 해석기.parse_args()
    ဒေတာ = ပြင်ဆင်()
    if အချက်များ.လှုပ်ရှားမှု == 'show':
        print(json.dumps(ဒေတာ, ensure_ascii=False, indent=2))
    else:
        print('장치별 အဝေးတန်ဖိုး ချိတ်ဆက်မှု သတ်မှတ်ချက် 준비됨. စကားဝှက်တန်ဖိုး အတည်ပြု: python3 ကိရိယာစု/အဝေးသတ်မှတ်ချက်.py show')
