#!/usr/bin/env python3
"""장치별 Kľúč_VALUE·kontakt_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

akcia_koreň = Path(__file__).resolve().parents[1]


def Pripraviť(akcia_koreň=akcia_koreň):
    Cesta = akcia_koreň / 'build/remote'
    Cesta.mkdir(parents=True, exist_ok=True)
    Nastavenia = Cesta / 'access.json'
    Kľúč_VALUE = Cesta / 'host-key.der'
    if not Kľúč_VALUE.exists():
        with Kľúč_VALUE.open('xb') as Súbor:
            os.chmod(str(Kľúč_VALUE), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Súbor)
    if not Nastavenia.exists():
        údaje = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Nastavenia.open('x') as Súbor:
            os.chmod(str(Nastavenia), 0o600)
            json.dump(údaje, Súbor, ensure_ascii=False, indent=2)
            Súbor.write('\n')
    údaje = json.loads(Nastavenia.read_text())
    if not isinstance(údaje, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if údaje.get('user') != 'user':
        raise SystemExit('access.json: user는 v_termíne_splatnosti_položka "user"만 지원합니다.')
    for Názov in ('ssh_password', 'vnc_password'):
        if not isinstance(údaje.get(Názov), str):
            raise SystemExit('access.json: ' + Názov + '는 문자열이어야 합니다.')
    셸암호 = údaje['ssh_password'].encode('utf-8')
    if len(셸암호) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = údaje['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. dĺžka_VALUE 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def pole_VALUE(Názov, VALUE):
        return 'static const unsigned char '+Názov+'[] = {'+','.join(str(수) for 수 in VALUE)+'};\n'
    머리 = pole_VALUE('telefón_Kľúč', Kľúč_VALUE.read_bytes())
    머리 += pole_VALUE('셸암호요약', hashlib.sha256(셸암호).digest())
    머리 += pole_VALUE('화면암호', 화면열쇠)
    generovať = Cesta / 'Profil.h'
    generovať.write_text(머리)
    os.chmod(str(generovať), 0o600)
    return údaje


if __name__ == '__main__':
    analyzátor_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analyzátor_48ee4b1b.add_argument('Akcia', choices=['show', 'prepare'], nargs='?', default='prepare')
    Argumenty = analyzátor_48ee4b1b.parse_args()
    údaje = Pripraviť()
    if Argumenty.Akcia == 'show':
        print(json.dumps(údaje, ensure_ascii=False, indent=2))
    else:
        print('장치별 vzdialený_VALUE kontakt_e05f319b Nastavenia 준비됨. heslo_VALUE overiť: python3 Nástroje/vzdialený_Nastavenia.py show')
