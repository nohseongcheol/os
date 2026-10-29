#!/usr/bin/env python3
"""장치별 Клуч_VALUE·врска_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

Project_корен = Path(__file__).resolve().parents[1]


def Подготви(Project_корен=Project_корен):
    ПАТЕКА = Project_корен / 'build/remote'
    ПАТЕКА.mkdir(parents=True, exist_ok=True)
    Подесувања = ПАТЕКА / 'access.json'
    Клуч_VALUE = ПАТЕКА / 'host-key.der'
    if not Клуч_VALUE.exists():
        with Клуч_VALUE.open('xb') as Датотека:
            os.chmod(str(Клуч_VALUE), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Датотека)
    if not Подесувања.exists():
        податоци = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Подесувања.open('x') as Датотека:
            os.chmod(str(Подесувања), 0o600)
            json.dump(податоци, Датотека, ensure_ascii=False, indent=2)
            Датотека.write('\n')
    податоци = json.loads(Подесувања.read_text())
    if not isinstance(податоци, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if податоци.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for Име in ('ssh_password', 'vnc_password'):
        if not isinstance(податоци.get(Име), str):
            raise SystemExit('access.json: ' + Име + '는 문자열이어야 합니다.')
    обвивка_лозинка = податоци['ssh_password'].encode('utf-8')
    if len(обвивка_лозинка) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = податоци['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. должина_VALUE 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def низа_VALUE(Име, VALUE):
        return 'static const unsigned char '+Име+'[] = {'+','.join(str(수) for 수 in VALUE)+'};\n'
    머리 = низа_VALUE('уред_Клуч', Клуч_VALUE.read_bytes())
    머리 += низа_VALUE('обвивка_лозинка_резиме', hashlib.sha256(обвивка_лозинка).digest())
    머리 += низа_VALUE('화면암호', 화면열쇠)
    генерира = ПАТЕКА / 'Профил.h'
    генерира.write_text(머리)
    os.chmod(str(генерира), 0o600)
    return податоци


if __name__ == '__main__':
    анализатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    анализатор_48ee4b1b.add_argument('Дејство', choices=['show', 'prepare'], nargs='?', default='prepare')
    Аргументи = анализатор_48ee4b1b.parse_args()
    податоци = Подготви()
    if Аргументи.Дејство == 'show':
        print(json.dumps(податоци, ensure_ascii=False, indent=2))
    else:
        print('장치별 далечинскo_VALUE врска_e05f319b Подесувања 준비됨. лозинка_VALUE провери: python3 Алатки/далечинскo_Параметри.py show')
