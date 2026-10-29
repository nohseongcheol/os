#!/usr/bin/env python3
"""장치별 ստեղն_արժեք·կապ_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

արձակել_արմատ = Path(__file__).resolve().parents[1]


def Պատրաստել(արձակել_արմատ=արձակել_արմատ):
    Ճանապարհ = արձակել_արմատ / 'build/remote'
    Ճանապարհ.mkdir(parents=True, exist_ok=True)
    Նախընտրանքներ = Ճանապարհ / 'access.json'
    ստեղն_արժեք = Ճանապարհ / 'host-key.der'
    if not ստեղն_արժեք.exists():
        with ստեղն_արժեք.open('xb') as Ֆայլ:
            os.chmod(str(ստեղն_արժեք), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Ֆայլ)
    if not Նախընտրանքներ.exists():
        տվյալ = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Նախընտրանքներ.open('x') as Ֆայլ:
            os.chmod(str(Նախընտրանքներ), 0o600)
            json.dump(տվյալ, Ֆայլ, ensure_ascii=False, indent=2)
            Ֆայլ.write('\n')
    տվյալ = json.loads(Նախընտրանքներ.read_text())
    if not isinstance(տվյալ, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if տվյալ.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for Անուն in ('ssh_password', 'vnc_password'):
        if not isinstance(տվյալ.get(Անուն), str):
            raise SystemExit('access.json: ' + Անուն + '는 문자열이어야 합니다.')
    խեցի_գաղտնաբառ = տվյալ['ssh_password'].encode('utf-8')
    if len(խեցի_գաղտնաբառ) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = տվյալ['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. տեւողություն_արժեք 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def ԶԱՆԳՎԱԾ_արժեք(Անուն, արժեք):
        return 'static const unsigned char '+Անուն+'[] = {'+','.join(str(수) for 수 in արժեք)+'};\n'
    머리 = ԶԱՆԳՎԱԾ_արժեք('սարք_ստեղն', ստեղն_արժեք.read_bytes())
    머리 += ԶԱՆԳՎԱԾ_արժեք('խեցի_գաղտնաբառ_ամփոփագիր', hashlib.sha256(խեցի_գաղտնաբառ).digest())
    머리 += ԶԱՆԳՎԱԾ_արժեք('화면암호', 화면열쇠)
    արտադրել = Ճանապարհ / 'Հատկագիր.h'
    արտադրել.write_text(머리)
    os.chmod(str(արտադրել), 0o600)
    return տվյալ


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('Գործողություն', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = 해석기.parse_args()
    տվյալ = Պատրաստել()
    if 인수.Գործողություն == 'show':
        print(json.dumps(տվյալ, ensure_ascii=False, indent=2))
    else:
        print('장치별 հեռակա_արժեք կապ_e05f319b Նախընտրանքներ 준비됨. գաղտնաբառ_արժեք հաստատել: python3 Գործիքներ/հեռակա_Կարգավորումներ.py show')
