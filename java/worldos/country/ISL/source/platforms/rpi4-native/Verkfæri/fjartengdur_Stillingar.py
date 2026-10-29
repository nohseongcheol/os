#!/usr/bin/env python3
"""장치별 Lykill_VALUE·tenging_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

verk_rót = Path(__file__).resolve().parents[1]


def Undirbúa(verk_rót=verk_rót):
    SLÓÐ = verk_rót / 'build/remote'
    SLÓÐ.mkdir(parents=True, exist_ok=True)
    Stillingar = SLÓÐ / 'access.json'
    Lykill_VALUE = SLÓÐ / 'host-key.der'
    if not Lykill_VALUE.exists():
        with Lykill_VALUE.open('xb') as Skrá:
            os.chmod(str(Lykill_VALUE), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Skrá)
    if not Stillingar.exists():
        gögn = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Stillingar.open('x') as Skrá:
            os.chmod(str(Stillingar), 0o600)
            json.dump(gögn, Skrá, ensure_ascii=False, indent=2)
            Skrá.write('\n')
    gögn = json.loads(Stillingar.read_text())
    if not isinstance(gögn, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if gögn.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for Heiti in ('ssh_password', 'vnc_password'):
        if not isinstance(gögn.get(Heiti), str):
            raise SystemExit('access.json: ' + Heiti + '는 문자열이어야 합니다.')
    skel_aðgangsorð = gögn['ssh_password'].encode('utf-8')
    if len(skel_aðgangsorð) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = gögn['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. lengd_VALUE 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def ARRAY_VALUE(Heiti, VALUE):
        return 'static const unsigned char '+Heiti+'[] = {'+','.join(str(númer) for númer in VALUE)+'};\n'
    머리 = ARRAY_VALUE('tæki_Lykill', Lykill_VALUE.read_bytes())
    머리 += ARRAY_VALUE('skel_aðgangsorð_samantekt', hashlib.sha256(skel_aðgangsorð).digest())
    머리 += ARRAY_VALUE('화면암호', 화면열쇠)
    skapa = SLÓÐ / 'prófíll.h'
    skapa.write_text(머리)
    os.chmod(str(skapa), 0o600)
    return gögn


if __name__ == '__main__':
    þáttari_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    þáttari_48ee4b1b.add_argument('Aðgerð', choices=['show', 'prepare'], nargs='?', default='prepare')
    Viðföng = þáttari_48ee4b1b.parse_args()
    gögn = Undirbúa()
    if Viðföng.Aðgerð == 'show':
        print(json.dumps(gögn, ensure_ascii=False, indent=2))
    else:
        print('장치별 fjartengdur_VALUE tenging_e05f319b Stillingar 준비됨. aðgangsorð_VALUE sannprófa: python3 Verkfæri/fjartengdur_Stillingar.py show')
