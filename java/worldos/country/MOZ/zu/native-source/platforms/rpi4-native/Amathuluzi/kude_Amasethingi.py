#!/usr/bin/env python3
"""장치별 inkomba_inani·uxhumano_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

기준 = Path(__file__).resolve().parents[1]


def Hlela(기준=기준):
    Indlela_2 = 기준 / 'build/remote'
    Indlela_2.mkdir(parents=True, exist_ok=True)
    Izinhlelo = Indlela_2 / 'access.json'
    inkomba_inani = Indlela_2 / 'host-key.der'
    if not inkomba_inani.exists():
        with inkomba_inani.open('xb') as Ihele:
            os.chmod(str(inkomba_inani), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Ihele)
    if not Izinhlelo.exists():
        imininingwane = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Izinhlelo.open('x') as Ihele:
            os.chmod(str(Izinhlelo), 0o600)
            json.dump(imininingwane, Ihele, ensure_ascii=False, indent=2)
            Ihele.write('\n')
    imininingwane = json.loads(Izinhlelo.read_text())
    if not isinstance(imininingwane, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if imininingwane.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for Igama in ('ssh_password', 'vnc_password'):
        if not isinstance(imininingwane.get(Igama), str):
            raise SystemExit('access.json: ' + Igama + '는 문자열이어야 합니다.')
    isihumushi_miyalelo_iphasiwedi = imininingwane['ssh_password'].encode('utf-8')
    if len(isihumushi_miyalelo_iphasiwedi) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = imininingwane['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. ubude_inani 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def AMALUNGU_AFANAYO_inani(Igama, inani):
        return 'static const unsigned char '+Igama+'[] = {'+','.join(str(수) for 수 in inani)+'};\n'
    머리 = AMALUNGU_AFANAYO_inani('idivayisi_inkomba', inkomba_inani.read_bytes())
    머리 += AMALUNGU_AFANAYO_inani('isihumushi_miyalelo_iphasiwedi_isifinyezo', hashlib.sha256(isihumushi_miyalelo_iphasiwedi).digest())
    머리 += AMALUNGU_AFANAYO_inani('화면암호', 화면열쇠)
    생성 = Indlela_2 / 'Iphrofayili.h'
    생성.write_text(머리)
    os.chmod(str(생성), 0o600)
    return imininingwane


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('Isenzo', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = 해석기.parse_args()
    imininingwane = Hlela()
    if 인수.Isenzo == 'show':
        print(json.dumps(imininingwane, ensure_ascii=False, indent=2))
    else:
        print('장치별 kude_inani uxhumano_e05f319b Izinhlelo 준비됨. iphasiwedi_inani qiniseka: python3 Amathuluzi/kude_Amasethingi.py show')
