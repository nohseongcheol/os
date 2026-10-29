#!/usr/bin/env python3
"""장치별 Açar_VALUE·qoşulma_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

Project_kök = Path(__file__).resolve().parents[1]


def Hazırla(Project_kök=Project_kök):
    Cığır = Project_kök / 'build/remote'
    Cığır.mkdir(parents=True, exist_ok=True)
    Sazlama = Cığır / 'access.json'
    Açar_VALUE = Cığır / 'host-key.der'
    if not Açar_VALUE.exists():
        with Açar_VALUE.open('xb') as FAYL:
            os.chmod(str(Açar_VALUE), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=FAYL)
    if not Sazlama.exists():
        verilənlər = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Sazlama.open('x') as FAYL:
            os.chmod(str(Sazlama), 0o600)
            json.dump(verilənlər, FAYL, ensure_ascii=False, indent=2)
            FAYL.write('\n')
    verilənlər = json.loads(Sazlama.read_text())
    if not isinstance(verilənlər, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if verilənlər.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for Ad in ('ssh_password', 'vnc_password'):
        if not isinstance(verilənlər.get(Ad), str):
            raise SystemExit('access.json: ' + Ad + '는 문자열이어야 합니다.')
    örtük_parol = verilənlər['ssh_password'].encode('utf-8')
    if len(örtük_parol) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = verilənlər['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. uzunluq_VALUE 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def ARRAY_VALUE(Ad, VALUE):
        return 'static const unsigned char '+Ad+'[] = {'+','.join(str(수) for 수 in VALUE)+'};\n'
    머리 = ARRAY_VALUE('cihaz_Açar', Açar_VALUE.read_bytes())
    머리 += ARRAY_VALUE('örtük_parol_xülasə', hashlib.sha256(örtük_parol).digest())
    머리 += ARRAY_VALUE('화면암호', 화면열쇠)
    yarat = Cığır / 'Profil.h'
    yarat.write_text(머리)
    os.chmod(str(yarat), 0o600)
    return verilənlər


if __name__ == '__main__':
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('Gedişat', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = parser_48ee4b1b.parse_args()
    verilənlər = Hazırla()
    if 인수.Gedişat == 'show':
        print(json.dumps(verilənlər, ensure_ascii=False, indent=2))
    else:
        print('장치별 uzaq_VALUE qoşulma_e05f319b Sazlama 준비됨. parol_VALUE yoxlamaq: python3 Alətlər/uzaq_Parametrlər.py show')
