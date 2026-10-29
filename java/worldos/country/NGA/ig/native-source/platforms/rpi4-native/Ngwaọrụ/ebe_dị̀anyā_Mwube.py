#!/usr/bin/env python3
"""장치별 ọtụgwo_valuu·njikọ_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

기준 = Path(__file__).resolve().parents[1]


def Kwado(기준=기준):
    ụzọ_ozi = 기준 / 'build/remote'
    ụzọ_ozi.mkdir(parents=True, exist_ok=True)
    Mwube = ụzọ_ozi / 'access.json'
    ọtụgwo_valuu = ụzọ_ozi / 'host-key.der'
    if not ọtụgwo_valuu.exists():
        with ọtụgwo_valuu.open('xb') as Faịlụ:
            os.chmod(str(ọtụgwo_valuu), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Faịlụ)
    if not Mwube.exists():
        datà = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Mwube.open('x') as Faịlụ:
            os.chmod(str(Mwube), 0o600)
            json.dump(datà, Faịlụ, ensure_ascii=False, indent=2)
            Faịlụ.write('\n')
    datà = json.loads(Mwube.read_text())
    if not isinstance(datà, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if datà.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for Aha in ('ssh_password', 'vnc_password'):
        if not isinstance(datà.get(Aha), str):
            raise SystemExit('access.json: ' + Aha + '는 문자열이어야 합니다.')
    nkọwannyemiwu_okwuntughe = datà['ssh_password'].encode('utf-8')
    if len(nkọwannyemiwu_okwuntughe) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = datà['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. ogologo_valuu 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def MKPOKỌTA_valuu(Aha, valuu):
        return 'static const unsigned char '+Aha+'[] = {'+','.join(str(수) for 수 in valuu)+'};\n'
    머리 = MKPOKỌTA_valuu('njìarụ_ọtụgwo', ọtụgwo_valuu.read_bytes())
    머리 += MKPOKỌTA_valuu('nkọwannyemiwu_okwuntughe_nchịkọta', hashlib.sha256(nkọwannyemiwu_okwuntughe).digest())
    머리 += MKPOKỌTA_valuu('화면암호', 화면열쇠)
    생성 = ụzọ_ozi / 'Profaịl.h'
    생성.write_text(머리)
    os.chmod(str(생성), 0o600)
    return datà


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('mmèm', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = 해석기.parse_args()
    datà = Kwado()
    if 인수.mmèm == 'show':
        print(json.dumps(datà, ensure_ascii=False, indent=2))
    else:
        print('장치별 ebe_dị̀anyā_valuu njikọ_e05f319b Mwube 준비됨. okwuntughe_valuu nkwàdo_eziokwū: python3 Ngwaọrụ/ebe_dị̀anyā_Mwube.py show')
