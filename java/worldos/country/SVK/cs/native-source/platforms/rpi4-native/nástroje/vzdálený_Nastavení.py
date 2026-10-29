#!/usr/bin/env python3
"""장치별 Klíč_HODNOTA·kontakt_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

akce_kořen = Path(__file__).resolve().parents[1]


def Připravit(akce_kořen=akce_kořen):
    cesta_2 = akce_kořen / 'build/remote'
    cesta_2.mkdir(parents=True, exist_ok=True)
    Nastavení = cesta_2 / 'access.json'
    Klíč_HODNOTA = cesta_2 / 'host-key.der'
    if not Klíč_HODNOTA.exists():
        with Klíč_HODNOTA.open('xb') as název_souboru:
            os.chmod(str(Klíč_HODNOTA), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=název_souboru)
    if not Nastavení.exists():
        data = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Nastavení.open('x') as název_souboru:
            os.chmod(str(Nastavení), 0o600)
            json.dump(data, název_souboru, ensure_ascii=False, indent=2)
            název_souboru.write('\n')
    data = json.loads(Nastavení.read_text())
    if not isinstance(data, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if data.get('user') != 'user':
        raise SystemExit('access.json: user는 dobrá_zboží "user"만 지원합니다.')
    for Název in ('ssh_password', 'vnc_password'):
        if not isinstance(data.get(Název), str):
            raise SystemExit('access.json: ' + Název + '는 문자열이어야 합니다.')
    prostředí_heslo = data['ssh_password'].encode('utf-8')
    if len(prostředí_heslo) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = data['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. délka_HODNOTA 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def pole_HODNOTA(Název, HODNOTA):
        return 'static const unsigned char '+Název+'[] = {'+','.join(str(číslo) for číslo in HODNOTA)+'};\n'
    머리 = pole_HODNOTA('mobilní_Klíč', Klíč_HODNOTA.read_bytes())
    머리 += pole_HODNOTA('prostředí_heslo_souhrn', hashlib.sha256(prostředí_heslo).digest())
    머리 += pole_HODNOTA('화면암호', 화면열쇠)
    generovat = cesta_2 / 'Profil.h'
    generovat.write_text(머리)
    os.chmod(str(generovat), 0o600)
    return data


if __name__ == '__main__':
    analyzátor_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analyzátor_48ee4b1b.add_argument('Akce', choices=['show', 'prepare'], nargs='?', default='prepare')
    argumenty = analyzátor_48ee4b1b.parse_args()
    data = Připravit()
    if argumenty.Akce == 'show':
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print('장치별 vzdálený_HODNOTA kontakt_e05f319b Nastavení 준비됨. heslo_HODNOTA ověřit: python3 nástroje/vzdálený_Nastavení.py show')
