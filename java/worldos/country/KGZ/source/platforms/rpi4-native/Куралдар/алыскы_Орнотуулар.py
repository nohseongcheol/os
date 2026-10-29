#!/usr/bin/env python3
"""장치별 ачкыч_маани·туташуу_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

기준 = Path(__file__).resolve().parents[1]


def Даярдоо(기준=기준):
    ЖОЛ = 기준 / 'build/remote'
    ЖОЛ.mkdir(parents=True, exist_ok=True)
    Орнотуулар = ЖОЛ / 'access.json'
    ачкыч_маани = ЖОЛ / 'host-key.der'
    if not ачкыч_маани.exists():
        with ачкыч_маани.open('xb') as Файл:
            os.chmod(str(ачкыч_маани), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Файл)
    if not Орнотуулар.exists():
        берилмелер = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Орнотуулар.open('x') as Файл:
            os.chmod(str(Орнотуулар), 0o600)
            json.dump(берилмелер, Файл, ensure_ascii=False, indent=2)
            Файл.write('\n')
    берилмелер = json.loads(Орнотуулар.read_text())
    if not isinstance(берилмелер, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if берилмелер.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for Аты in ('ssh_password', 'vnc_password'):
        if not isinstance(берилмелер.get(Аты), str):
            raise SystemExit('access.json: ' + Аты + '는 문자열이어야 합니다.')
    сырты_жашыруун_сөз = берилмелер['ssh_password'].encode('utf-8')
    if len(сырты_жашыруун_сөз) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = берилмелер['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. узундук_маани 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def МАССИВ_маани(Аты, маани):
        return 'static const unsigned char '+Аты+'[] = {'+','.join(str(수) for 수 in маани)+'};\n'
    머리 = МАССИВ_маани('түзмөк_ачкыч', ачкыч_маани.read_bytes())
    머리 += МАССИВ_маани('сырты_жашыруун_сөз_жыйынтык', hashlib.sha256(сырты_жашыруун_сөз).digest())
    머리 += МАССИВ_маани('화면암호', 화면열쇠)
    생성 = ЖОЛ / 'Профиль.h'
    생성.write_text(머리)
    os.chmod(str(생성), 0o600)
    return берилмелер


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('Аракети', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = 해석기.parse_args()
    берилмелер = Даярдоо()
    if 인수.Аракети == 'show':
        print(json.dumps(берилмелер, ensure_ascii=False, indent=2))
    else:
        print('장치별 алыскы_маани туташуу_e05f319b Орнотуулар 준비됨. жашыруун_сөз_маани тууралыгын_аныктоо: python3 Куралдар/алыскы_Орнотуулар.py show')
