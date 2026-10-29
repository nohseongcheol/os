#!/usr/bin/env python3
"""장치별 keyValue·connection 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

projectRoot = Path(__file__).resolve().parents[1]


def prepare(projectRoot=projectRoot):
    path = projectRoot / 'build/remote'
    path.mkdir(parents=True, exist_ok=True)
    settings = path / 'access.json'
    keyValue = path / 'host-key.der'
    if not keyValue.exists():
        with keyValue.open('xb') as file:
            os.chmod(str(keyValue), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=file)
    if not settings.exists():
        data = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with settings.open('x') as file:
            os.chmod(str(settings), 0o600)
            json.dump(data, file, ensure_ascii=False, indent=2)
            file.write('\n')
    data = json.loads(settings.read_text())
    if not isinstance(data, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if data.get('user') != 'user':
        raise SystemExit('access.json: user는 currentItem "user"만 지원합니다.')
    for name in ('ssh_password', 'vnc_password'):
        if not isinstance(data.get(name), str):
            raise SystemExit('access.json: ' + name + '는 문자열이어야 합니다.')
    shellPassword = data['ssh_password'].encode('utf-8')
    if len(shellPassword) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        screenPassword = data['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. lengthValue 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    screenKey = screenPassword[:8].ljust(8, b'\0')
    def arrayValue(name, value):
        return 'static const unsigned char '+name+'[] = {'+','.join(str(number) for number in value)+'};\n'
    headValue = arrayValue('deviceKey', keyValue.read_bytes())
    headValue += arrayValue('shellPasswordSummary', hashlib.sha256(shellPassword).digest())
    headValue += arrayValue('screenPassword', screenKey)
    generate = path / 'profile.h'
    generate.write_text(headValue)
    os.chmod(str(generate), 0o600)
    return data


if __name__ == '__main__':
    Parser = argparse.ArgumentParser(description=__doc__)
    Parser.add_argument('action', choices=['show', 'prepare'], nargs='?', default='prepare')
    arguments = Parser.parse_args()
    data = prepare()
    if arguments.action == 'show':
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print('장치별 remoteValue connection settings isPrepared. passwordValue verify: python3 tools/remoteSettings.py show')
