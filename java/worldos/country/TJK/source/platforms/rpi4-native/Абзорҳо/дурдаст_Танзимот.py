#!/usr/bin/env python3
"""장치별 калид_қимат·пайваст_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

기준 = Path(__file__).resolve().parents[1]


def Омода_кардан(기준=기준):
    масир = 기준 / 'build/remote'
    масир.mkdir(parents=True, exist_ok=True)
    Танзимот = масир / 'access.json'
    калид_қимат = масир / 'host-key.der'
    if not калид_қимат.exists():
        with калид_қимат.open('xb') as Файл:
            os.chmod(str(калид_қимат), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Файл)
    if not Танзимот.exists():
        иттилоот = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Танзимот.open('x') as Файл:
            os.chmod(str(Танзимот), 0o600)
            json.dump(иттилоот, Файл, ensure_ascii=False, indent=2)
            Файл.write('\n')
    иттилоот = json.loads(Танзимот.read_text())
    if not isinstance(иттилоот, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if иттилоот.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for Ном in ('ssh_password', 'vnc_password'):
        if not isinstance(иттилоот.get(Ном), str):
            raise SystemExit('access.json: ' + Ном + '는 문자열이어야 합니다.')
    восит_парол = иттилоот['ssh_password'].encode('utf-8')
    if len(восит_парол) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = иттилоот['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. дарозӣ_қимат 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def қатор_қимат(Ном, қимат):
        return 'static const unsigned char '+Ном+'[] = {'+','.join(str(수) for 수 in қимат)+'};\n'
    머리 = қатор_қимат('мобилӣ_калид', калид_қимат.read_bytes())
    머리 += қатор_қимат('셸암호요약', hashlib.sha256(восит_парол).digest())
    머리 += қатор_қимат('화면암호', 화면열쇠)
    생성 = масир / 'Профил.h'
    생성.write_text(머리)
    os.chmod(str(생성), 0o600)
    return иттилоот


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('Амал', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = 해석기.parse_args()
    иттилоот = Омода_кардан()
    if 인수.Амал == 'show':
        print(json.dumps(иттилоот, ensure_ascii=False, indent=2))
    else:
        print('장치별 дурдаст_қимат пайваст_e05f319b Танзимот 준비됨. парол_қимат тасдиқ_кардан: python3 Абзорҳо/дурдаст_Танзимот.py show')
