#!/usr/bin/env python3
"""장치별 iqhosha_ixabiso·uqhagamshelo_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

기준 = Path(__file__).resolve().parents[1]


def lungisa(기준=기준):
    INDLELA = 기준 / 'build/remote'
    INDLELA.mkdir(parents=True, exist_ok=True)
    Imimiselo = INDLELA / 'access.json'
    iqhosha_ixabiso = INDLELA / 'host-key.der'
    if not iqhosha_ixabiso.exists():
        with iqhosha_ixabiso.open('xb') as iFayili:
            os.chmod(str(iqhosha_ixabiso), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=iFayili)
    if not Imimiselo.exists():
        iingcombolo = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Imimiselo.open('x') as iFayili:
            os.chmod(str(Imimiselo), 0o600)
            json.dump(iingcombolo, iFayili, ensure_ascii=False, indent=2)
            iFayili.write('\n')
    iingcombolo = json.loads(Imimiselo.read_text())
    if not isinstance(iingcombolo, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if iingcombolo.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for Igama in ('ssh_password', 'vnc_password'):
        if not isinstance(iingcombolo.get(Igama), str):
            raise SystemExit('access.json: ' + Igama + '는 문자열이어야 합니다.')
    isiniki_myalelo_iphaswedi = iingcombolo['ssh_password'].encode('utf-8')
    if len(isiniki_myalelo_iphaswedi) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = iingcombolo['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. ubude_ixabiso 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def ULUHLU_ixabiso(Igama, ixabiso):
        return 'static const unsigned char '+Igama+'[] = {'+','.join(str(수) for 수 in ixabiso)+'};\n'
    머리 = ULUHLU_ixabiso('isixhobo_iqhosha', iqhosha_ixabiso.read_bytes())
    머리 += ULUHLU_ixabiso('isiniki_myalelo_iphaswedi_ushwankathelo', hashlib.sha256(isiniki_myalelo_iphaswedi).digest())
    머리 += ULUHLU_ixabiso('화면암호', 화면열쇠)
    생성 = INDLELA / 'Iprofayile.h'
    생성.write_text(머리)
    os.chmod(str(생성), 0o600)
    return iingcombolo


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('Intshukumo', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = 해석기.parse_args()
    iingcombolo = lungisa()
    if 인수.Intshukumo == 'show':
        print(json.dumps(iingcombolo, ensure_ascii=False, indent=2))
    else:
        print('장치별 kude_ixabiso uqhagamshelo_e05f319b Imimiselo 준비됨. iphaswedi_ixabiso ngqinisisa: python3 Izixhobo/kude_Iisetingi.py show')
