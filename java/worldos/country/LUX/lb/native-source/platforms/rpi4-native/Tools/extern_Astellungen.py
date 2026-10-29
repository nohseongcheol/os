#!/usr/bin/env python3
"""장치별 Tast_VALUE·Verbindung_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

projezéieren_Racinn = Path(__file__).resolve().parents[1]


def Préparéieren(projezéieren_Racinn=projezéieren_Racinn):
    Wee = projezéieren_Racinn / 'build/remote'
    Wee.mkdir(parents=True, exist_ok=True)
    Astellungen = Wee / 'access.json'
    Tast_VALUE = Wee / 'host-key.der'
    if not Tast_VALUE.exists():
        with Tast_VALUE.open('xb') as Fichier:
            os.chmod(str(Tast_VALUE), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Fichier)
    if not Astellungen.exists():
        Daten = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Astellungen.open('x') as Fichier:
            os.chmod(str(Astellungen), 0o600)
            json.dump(Daten, Fichier, ensure_ascii=False, indent=2)
            Fichier.write('\n')
    Daten = json.loads(Astellungen.read_text())
    if not isinstance(Daten, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if Daten.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for Numm in ('ssh_password', 'vnc_password'):
        if not isinstance(Daten.get(Numm), str):
            raise SystemExit('access.json: ' + Numm + '는 문자열이어야 합니다.')
    Shell_Passwuert = Daten['ssh_password'].encode('utf-8')
    if len(Shell_Passwuert) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = Daten['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. Längt_VALUE 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def ARRAY_VALUE(Numm, VALUE):
        return 'static const unsigned char '+Numm+'[] = {'+','.join(str(수) for 수 in VALUE)+'};\n'
    머리 = ARRAY_VALUE('Mobil_Tast', Tast_VALUE.read_bytes())
    머리 += ARRAY_VALUE('Shell_Passwuert_Zesummefaassung', hashlib.sha256(Shell_Passwuert).digest())
    머리 += ARRAY_VALUE('화면암호', 화면열쇠)
    generéieren = Wee / 'Profil.h'
    generéieren.write_text(머리)
    os.chmod(str(generéieren), 0o600)
    return Daten


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('Aktioun', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = 해석기.parse_args()
    Daten = Préparéieren()
    if 인수.Aktioun == 'show':
        print(json.dumps(Daten, ensure_ascii=False, indent=2))
    else:
        print('장치별 extern_VALUE Verbindung_e05f319b Astellungen 준비됨. Passwuert_VALUE verifizéieren: python3 Tools/extern_Astellungen.py show')
