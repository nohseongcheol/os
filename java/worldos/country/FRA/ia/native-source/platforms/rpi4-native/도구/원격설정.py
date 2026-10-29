#!/usr/bin/env python3
"""장치별 키·접속 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

기준 = Path(__file__).resolve().parents[1]


def 준비(기준=기준):
    Percurso = 기준 / 'build/remote'
    Percurso.mkdir(parents=True, exist_ok=True)
    설정 = Percurso / 'access.json'
    키 = Percurso / 'host-key.der'
    if not 키.exists():
        with 키.open('xb') as 파일:
            os.chmod(str(키), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=파일)
    if not 설정.exists():
        자료 = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with 설정.open('x') as 파일:
            os.chmod(str(설정), 0o600)
            json.dump(자료, 파일, ensure_ascii=False, indent=2)
            파일.write('\n')
    자료 = json.loads(설정.read_text())
    if not isinstance(자료, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if 자료.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for Nomine in ('ssh_password', 'vnc_password'):
        if not isinstance(자료.get(Nomine), str):
            raise SystemExit('access.json: ' + Nomine + '는 문자열이어야 합니다.')
    셸암호 = 자료['ssh_password'].encode('utf-8')
    if len(셸암호) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = 자료['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. 길이 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def 배열(Nomine, 값):
        return 'static const unsigned char '+Nomine+'[] = {'+','.join(str(수) for 수 in 값)+'};\n'
    머리 = 배열('장치열쇠', 키.read_bytes())
    머리 += 배열('셸암호요약', hashlib.sha256(셸암호).digest())
    머리 += 배열('화면암호', 화면열쇠)
    생성 = Percurso / '접속설정.h'
    생성.write_text(머리)
    os.chmod(str(생성), 0o600)
    return 자료


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('동작', choices=['show', 'prepare'], nargs='?', default='prepare')
    Argumentos = 해석기.parse_args()
    자료 = 준비()
    if Argumentos.동작 == 'show':
        print(json.dumps(자료, ensure_ascii=False, indent=2))
    else:
        print('장치별 원격 접속 설정 준비됨. 암호 확인: python3 도구/원격설정.py show')
