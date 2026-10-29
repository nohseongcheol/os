#!/usr/bin/env python3
"""장치별 Cheie_VALUE·conexiune_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

Project_rădăcină = Path(__file__).resolve().parents[1]


def Pregătiți(Project_rădăcină=Project_rădăcină):
    Cale = Project_rădăcină / 'build/remote'
    Cale.mkdir(parents=True, exist_ok=True)
    Setări = Cale / 'access.json'
    Cheie_VALUE = Cale / 'host-key.der'
    if not Cheie_VALUE.exists():
        with Cheie_VALUE.open('xb') as Fișier:
            os.chmod(str(Cheie_VALUE), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Fișier)
    if not Setări.exists():
        date = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Setări.open('x') as Fișier:
            os.chmod(str(Setări), 0o600)
            json.dump(date, Fișier, ensure_ascii=False, indent=2)
            Fișier.write('\n')
    date = json.loads(Setări.read_text())
    if not isinstance(date, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if date.get('user') != 'user':
        raise SystemExit('access.json: user는 curent_element "user"만 지원합니다.')
    for Nume in ('ssh_password', 'vnc_password'):
        if not isinstance(date.get(Nume), str):
            raise SystemExit('access.json: ' + Nume + '는 문자열이어야 합니다.')
    shell_parolă = date['ssh_password'].encode('utf-8')
    if len(shell_parolă) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = date['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. lungime_VALUE 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def ARRAY_VALUE(Nume, VALUE):
        return 'static const unsigned char '+Nume+'[] = {'+','.join(str(수) for 수 in VALUE)+'};\n'
    머리 = ARRAY_VALUE('mobil_Cheie', Cheie_VALUE.read_bytes())
    머리 += ARRAY_VALUE('shell_parolă_rezumat', hashlib.sha256(shell_parolă).digest())
    머리 += ARRAY_VALUE('화면암호', 화면열쇠)
    genera = Cale / 'Profil.h'
    genera.write_text(머리)
    os.chmod(str(genera), 0o600)
    return date


if __name__ == '__main__':
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('Acțiuni', choices=['show', 'prepare'], nargs='?', default='prepare')
    Argumente = parser_48ee4b1b.parse_args()
    date = Pregătiți()
    if Argumente.Acțiuni == 'show':
        print(json.dumps(date, ensure_ascii=False, indent=2))
    else:
        print('장치별 la_distanță_VALUE conexiune_e05f319b Setări 준비됨. parolă_VALUE verifica: python3 Instrumente/la_distanță_Setări.py show')
