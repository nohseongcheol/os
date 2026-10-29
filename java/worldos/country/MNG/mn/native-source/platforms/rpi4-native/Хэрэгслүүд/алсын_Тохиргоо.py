#!/usr/bin/env python3
"""장치별 түлхүүр_утга·холболт_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

기준 = Path(__file__).resolve().parents[1]


def Бэлтгэх(기준=기준):
    ЗАМ = 기준 / 'build/remote'
    ЗАМ.mkdir(parents=True, exist_ok=True)
    Тохиргоо = ЗАМ / 'access.json'
    түлхүүр_утга = ЗАМ / 'host-key.der'
    if not түлхүүр_утга.exists():
        with түлхүүр_утга.open('xb') as Файл:
            os.chmod(str(түлхүүр_утга), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Файл)
    if not Тохиргоо.exists():
        өгөгдөл = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Тохиргоо.open('x') as Файл:
            os.chmod(str(Тохиргоо), 0o600)
            json.dump(өгөгдөл, Файл, ensure_ascii=False, indent=2)
            Файл.write('\n')
    өгөгдөл = json.loads(Тохиргоо.read_text())
    if not isinstance(өгөгдөл, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if өгөгдөл.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for Нэр in ('ssh_password', 'vnc_password'):
        if not isinstance(өгөгдөл.get(Нэр), str):
            raise SystemExit('access.json: ' + Нэр + '는 문자열이어야 합니다.')
    бүрхүүл_нууц_үг = өгөгдөл['ssh_password'].encode('utf-8')
    if len(бүрхүүл_нууц_үг) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = өгөгдөл['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. урт_утга 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def олонлог_утга(Нэр, утга):
        return 'static const unsigned char '+Нэр+'[] = {'+','.join(str(수) for 수 in утга)+'};\n'
    머리 = олонлог_утга('гар_утас_түлхүүр', түлхүүр_утга.read_bytes())
    머리 += олонлог_утга('бүрхүүл_нууц_үг_хураангуй', hashlib.sha256(бүрхүүл_нууц_үг).digest())
    머리 += олонлог_утга('화면암호', 화면열쇠)
    생성 = ЗАМ / 'Хувийн_тохиргоо.h'
    생성.write_text(머리)
    os.chmod(str(생성), 0o600)
    return өгөгдөл


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('Үйлдэл', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = 해석기.parse_args()
    өгөгдөл = Бэлтгэх()
    if 인수.Үйлдэл == 'show':
        print(json.dumps(өгөгдөл, ensure_ascii=False, indent=2))
    else:
        print('장치별 алсын_утга холболт_e05f319b Тохиргоо 준비됨. нууц_үг_утга шалгах: python3 Хэрэгслүүд/алсын_Тохиргоо.py show')
