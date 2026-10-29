#!/usr/bin/env python3
"""장치별 naqigaq_atuutilik·kasuqsimaniq_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

기준 = Path(__file__).resolve().parents[1]


def Parnalli(기준=기준):
    aqqut = 기준 / 'build/remote'
    aqqut.mkdir(parents=True, exist_ok=True)
    설정 = aqqut / 'access.json'
    naqigaq_atuutilik = aqqut / 'host-key.der'
    if not naqigaq_atuutilik.exists():
        with naqigaq_atuutilik.open('xb') as ini:
            os.chmod(str(naqigaq_atuutilik), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=ini)
    if not 설정.exists():
        titiqqat = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with 설정.open('x') as ini:
            os.chmod(str(설정), 0o600)
            json.dump(titiqqat, ini, ensure_ascii=False, indent=2)
            ini.write('\n')
    titiqqat = json.loads(설정.read_text())
    if not isinstance(titiqqat, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if titiqqat.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for atiq in ('ssh_password', 'vnc_password'):
        if not isinstance(titiqqat.get(atiq), str):
            raise SystemExit('access.json: ' + atiq + '는 문자열이어야 합니다.')
    piqujijjutiliriji_isirut = titiqqat['ssh_password'].encode('utf-8')
    if len(piqujijjutiliriji_isirut) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = titiqqat['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. takininga_atuutilik 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def array_atuutilik(atiq, atuutilik):
        return 'static const unsigned char '+atiq+'[] = {'+','.join(str(수) for 수 in atuutilik)+'};\n'
    머리 = array_atuutilik('sunakkutaaq_naqigaq', naqigaq_atuutilik.read_bytes())
    머리 += array_atuutilik('piqujijjutiliriji_isirut_naiglitiqsimajuq', hashlib.sha256(piqujijjutiliriji_isirut).digest())
    머리 += array_atuutilik('화면암호', 화면열쇠)
    생성 = aqqut / 'Miksaanuungajuq.h'
    생성.write_text(머리)
    os.chmod(str(생성), 0o600)
    return titiqqat


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('sugiarut', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = 해석기.parse_args()
    titiqqat = Parnalli()
    if 인수.sugiarut == 'show':
        print(json.dumps(titiqqat, ensure_ascii=False, indent=2))
    else:
        print('장치별 ungasittuq_atuutilik kasuqsimaniq_e05f319b 설정 준비됨. isirut_atuutilik nalunairli_1aacb54c: python3 도구/원격설정.py show')
