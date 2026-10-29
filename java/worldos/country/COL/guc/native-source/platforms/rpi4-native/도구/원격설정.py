#!/usr/bin/env python3
"""장치별 ajüttia_ajutuu·epe_ipajia_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

기준 = Path(__file__).resolve().parents[1]


def 준비(기준=기준):
    wopu_a_ttaaleemüin = 기준 / 'build/remote'
    wopu_a_ttaaleemüin.mkdir(parents=True, exist_ok=True)
    설정 = wopu_a_ttaaleemüin / 'access.json'
    ajüttia_ajutuu = wopu_a_ttaaleemüin / 'host-key.der'
    if not ajüttia_ajutuu.exists():
        with ajüttia_ajutuu.open('xb') as anaajaalaa:
            os.chmod(str(ajüttia_ajutuu), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=anaajaalaa)
    if not 설정.exists():
        atijaaya = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with 설정.open('x') as anaajaalaa:
            os.chmod(str(설정), 0o600)
            json.dump(atijaaya, anaajaalaa, ensure_ascii=False, indent=2)
            anaajaalaa.write('\n')
    atijaaya = json.loads(설정.read_text())
    if not isinstance(atijaaya, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if atijaaya.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for 이름 in ('ssh_password', 'vnc_password'):
        if not isinstance(atijaaya.get(이름), str):
            raise SystemExit('access.json: ' + 이름 + '는 문자열이어야 합니다.')
    aluwataalapu_u_amoutia = atijaaya['ssh_password'].encode('utf-8')
    if len(aluwataalapu_u_amoutia) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = atijaaya['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. akaliaa_ajutuu 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def matüriisü_ajutuu(이름, ajutuu):
        return 'static const unsigned char '+이름+'[] = {'+','.join(str(수) for 수 in ajutuu)+'};\n'
    머리 = matüriisü_ajutuu('serulaalü_ajüttia', ajüttia_ajutuu.read_bytes())
    머리 += matüriisü_ajutuu('셸암호요약', hashlib.sha256(aluwataalapu_u_amoutia).digest())
    머리 += matüriisü_ajutuu('화면암호', 화면열쇠)
    생성 = wopu_a_ttaaleemüin / 'ka_yataayakua_ipakalü.h'
    생성.write_text(머리)
    os.chmod(str(생성), 0o600)
    return atijaaya


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('aa_inra_awai', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = 해석기.parse_args()
    atijaaya = 준비()
    if 인수.aa_inra_awai == 'show':
        print(json.dumps(atijaaya, ensure_ascii=False, indent=2))
    else:
        print('장치별 원격 epe_ipajia_e05f319b 설정 준비됨. amoutia_ajutuu 확인: python3 도구/원격설정.py show')
