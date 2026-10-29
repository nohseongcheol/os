#!/usr/bin/env python3
"""장치별 key_VALUE·koneksyon_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

Project_root = Path(__file__).resolve().parents[1]


def Ihanda(Project_root=Project_root):
    path = Project_root / 'build/remote'
    path.mkdir(parents=True, exist_ok=True)
    Mga_Setting = path / 'access.json'
    key_VALUE = path / 'host-key.der'
    if not key_VALUE.exists():
        with key_VALUE.open('xb') as file:
            os.chmod(str(key_VALUE), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=file)
    if not Mga_Setting.exists():
        data = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Mga_Setting.open('x') as file:
            os.chmod(str(Mga_Setting), 0o600)
            json.dump(data, file, ensure_ascii=False, indent=2)
            file.write('\n')
    data = json.loads(Mga_Setting.read_text())
    if not isinstance(data, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if data.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for pangalan in ('ssh_password', 'vnc_password'):
        if not isinstance(data.get(pangalan), str):
            raise SystemExit('access.json: ' + pangalan + '는 문자열이어야 합니다.')
    shell_password = data['ssh_password'].encode('utf-8')
    if len(shell_password) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = data['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. haba_VALUE 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def ARRAY_VALUE(pangalan, VALUE):
        return 'static const unsigned char '+pangalan+'[] = {'+','.join(str(수) for 수 in VALUE)+'};\n'
    머리 = ARRAY_VALUE('device_key', key_VALUE.read_bytes())
    머리 += ARRAY_VALUE('shell_password_buod', hashlib.sha256(shell_password).digest())
    머리 += ARRAY_VALUE('화면암호', 화면열쇠)
    mag_generate = path / 'Profile.h'
    mag_generate.write_text(머리)
    os.chmod(str(mag_generate), 0o600)
    return data


if __name__ == '__main__':
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('aksyon', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = parser_48ee4b1b.parse_args()
    data = Ihanda()
    if 인수.aksyon == 'show':
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print('장치별 malayuan_VALUE koneksyon_e05f319b Mga_Setting 준비됨. password_VALUE tiyakin_kumpirmahin: python3 Mga_Tool/malayuan_Mga_Setting.py show')
