#!/usr/bin/env python3
"""장치별 bysell_VALUE·cyswllt_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

prosiect_gwraidd = Path(__file__).resolve().parents[1]


def Paratoi(prosiect_gwraidd=prosiect_gwraidd):
    LLWYBR = prosiect_gwraidd / 'build/remote'
    LLWYBR.mkdir(parents=True, exist_ok=True)
    Gosodiadau = LLWYBR / 'access.json'
    bysell_VALUE = LLWYBR / 'host-key.der'
    if not bysell_VALUE.exists():
        with bysell_VALUE.open('xb') as Ffeil:
            os.chmod(str(bysell_VALUE), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Ffeil)
    if not Gosodiadau.exists():
        data = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Gosodiadau.open('x') as Ffeil:
            os.chmod(str(Gosodiadau), 0o600)
            json.dump(data, Ffeil, ensure_ascii=False, indent=2)
            Ffeil.write('\n')
    data = json.loads(Gosodiadau.read_text())
    if not isinstance(data, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if data.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for Enw in ('ssh_password', 'vnc_password'):
        if not isinstance(data.get(Enw), str):
            raise SystemExit('access.json: ' + Enw + '는 문자열이어야 합니다.')
    cragen_cyfrinair = data['ssh_password'].encode('utf-8')
    if len(cragen_cyfrinair) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = data['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. hyd_VALUE 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def ARAE_VALUE(Enw, VALUE):
        return 'static const unsigned char '+Enw+'[] = {'+','.join(str(수) for 수 in VALUE)+'};\n'
    머리 = ARAE_VALUE('dyfais_bysell', bysell_VALUE.read_bytes())
    머리 += ARAE_VALUE('cragen_cyfrinair_crynodeb', hashlib.sha256(cragen_cyfrinair).digest())
    머리 += ARAE_VALUE('화면암호', 화면열쇠)
    cynhyrchu = LLWYBR / 'Proffil.h'
    cynhyrchu.write_text(머리)
    os.chmod(str(cynhyrchu), 0o600)
    return data


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('Gweithrediad', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = 해석기.parse_args()
    data = Paratoi()
    if 인수.Gweithrediad == 'show':
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print('장치별 pell_VALUE cyswllt_e05f319b Gosodiadau 준비됨. cyfrinair_VALUE dilysu: python3 Offer/pell_Gosodiadau.py show')
