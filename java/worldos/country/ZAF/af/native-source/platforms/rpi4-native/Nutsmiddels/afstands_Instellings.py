#!/usr/bin/env python3
"""장치별 Sleutel_VALUE·verbinding_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

Project_wortel = Path(__file__).resolve().parents[1]


def Maak_gereed(Project_wortel=Project_wortel):
    Pad = Project_wortel / 'build/remote'
    Pad.mkdir(parents=True, exist_ok=True)
    Instellings = Pad / 'access.json'
    Sleutel_VALUE = Pad / 'host-key.der'
    if not Sleutel_VALUE.exists():
        with Sleutel_VALUE.open('xb') as Lêer:
            os.chmod(str(Sleutel_VALUE), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Lêer)
    if not Instellings.exists():
        data = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Instellings.open('x') as Lêer:
            os.chmod(str(Instellings), 0o600)
            json.dump(data, Lêer, ensure_ascii=False, indent=2)
            Lêer.write('\n')
    data = json.loads(Instellings.read_text())
    if not isinstance(data, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if data.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for Naam in ('ssh_password', 'vnc_password'):
        if not isinstance(data.get(Naam), str):
            raise SystemExit('access.json: ' + Naam + '는 문자열이어야 합니다.')
    dop_wagwoord = data['ssh_password'].encode('utf-8')
    if len(dop_wagwoord) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = data['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. lengte_VALUE 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def ARRAY_VALUE(Naam, VALUE):
        return 'static const unsigned char '+Naam+'[] = {'+','.join(str(수) for 수 in VALUE)+'};\n'
    머리 = ARRAY_VALUE('mobiel_Sleutel', Sleutel_VALUE.read_bytes())
    머리 += ARRAY_VALUE('셸암호요약', hashlib.sha256(dop_wagwoord).digest())
    머리 += ARRAY_VALUE('화면암호', 화면열쇠)
    genereer = Pad / 'Profiel.h'
    genereer.write_text(머리)
    os.chmod(str(genereer), 0o600)
    return data


if __name__ == '__main__':
    ontleder_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ontleder_48ee4b1b.add_argument('Aksie', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = ontleder_48ee4b1b.parse_args()
    data = Maak_gereed()
    if 인수.Aksie == 'show':
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print('장치별 afstands_VALUE verbinding_e05f319b Instellings 준비됨. wagwoord_VALUE verifieer: python3 Nutsmiddels/afstands_Instellings.py show')
