#!/usr/bin/env python3
"""장치별 buto_agaciro·kwihuza_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

기준 = Path(__file__).resolve().parents[1]


def Gutegura(기준=기준):
    Inzira = 기준 / 'build/remote'
    Inzira.mkdir(parents=True, exist_ok=True)
    Amagenamiterere = Inzira / 'access.json'
    buto_agaciro = Inzira / 'host-key.der'
    if not buto_agaciro.exists():
        with buto_agaciro.open('xb') as Idosiye:
            os.chmod(str(buto_agaciro), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Idosiye)
    if not Amagenamiterere.exists():
        amakurushingiro = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Amagenamiterere.open('x') as Idosiye:
            os.chmod(str(Amagenamiterere), 0o600)
            json.dump(amakurushingiro, Idosiye, ensure_ascii=False, indent=2)
            Idosiye.write('\n')
    amakurushingiro = json.loads(Amagenamiterere.read_text())
    if not isinstance(amakurushingiro, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if amakurushingiro.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for Izina in ('ssh_password', 'vnc_password'):
        if not isinstance(amakurushingiro.get(Izina), str):
            raise SystemExit('access.json: ' + Izina + '는 문자열이어야 합니다.')
    insomamabwiriza_ijambobanga = amakurushingiro['ssh_password'].encode('utf-8')
    if len(insomamabwiriza_ijambobanga) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = amakurushingiro['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. uburebure_agaciro 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def ARRAY_agaciro(Izina, agaciro):
        return 'static const unsigned char '+Izina+'[] = {'+','.join(str(수) for 수 in agaciro)+'};\n'
    머리 = ARRAY_agaciro('igendanwa_buto', buto_agaciro.read_bytes())
    머리 += ARRAY_agaciro('셸암호요약', hashlib.sha256(insomamabwiriza_ijambobanga).digest())
    머리 += ARRAY_agaciro('화면암호', 화면열쇠)
    생성 = Inzira / 'Umwirondoro.h'
    생성.write_text(머리)
    os.chmod(str(생성), 0o600)
    return amakurushingiro


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('Igikorwa', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = 해석기.parse_args()
    amakurushingiro = Gutegura()
    if 인수.Igikorwa == 'show':
        print(json.dumps(amakurushingiro, ensure_ascii=False, indent=2))
    else:
        print('장치별 kure_agaciro kwihuza_e05f319b Amagenamiterere 준비됨. ijambobanga_agaciro gusuzuma: python3 Ibikoresho/kure_Amagenamiterere.py show')
