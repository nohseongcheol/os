#!/usr/bin/env python3
"""장치별 kelal_njaru·ceŋondiral_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

기준 = Path(__file__).resolve().parents[1]


def Heblu(기준=기준):
    laawol = 기준 / 'build/remote'
    laawol.mkdir(parents=True, exist_ok=True)
    설정 = laawol / 'access.json'
    kelal_njaru = laawol / 'host-key.der'
    if not kelal_njaru.exists():
        with kelal_njaru.open('xb') as fiilde:
            os.chmod(str(kelal_njaru), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=fiilde)
    if not 설정.exists():
        keɓe = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with 설정.open('x') as fiilde:
            os.chmod(str(설정), 0o600)
            json.dump(keɓe, fiilde, ensure_ascii=False, indent=2)
            fiilde.write('\n')
    keɓe = json.loads(설정.read_text())
    if not isinstance(keɓe, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if keɓe.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for innde in ('ssh_password', 'vnc_password'):
        if not isinstance(keɓe.get(innde), str):
            raise SystemExit('access.json: ' + innde + '는 문자열이어야 합니다.')
    laalagal_finnde = keɓe['ssh_password'].encode('utf-8')
    if len(laalagal_finnde) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = keɓe['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. njuuteendi_njaru 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def 배열(innde, njaru):
        return 'static const unsigned char '+innde+'[] = {'+','.join(str(수) for 수 in njaru)+'};\n'
    머리 = 배열('kaɓirgal_kelal', kelal_njaru.read_bytes())
    머리 += 배열('셸암호요약', hashlib.sha256(laalagal_finnde).digest())
    머리 += 배열('화면암호', 화면열쇠)
    생성 = laawol / 'heftinirde_kuutoro.h'
    생성.write_text(머리)
    os.chmod(str(생성), 0o600)
    return keɓe


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('gollal', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = 해석기.parse_args()
    keɓe = Heblu()
    if 인수.gollal == 'show':
        print(json.dumps(keɓe, ensure_ascii=False, indent=2))
    else:
        print('장치별 원격 ceŋondiral_e05f319b 설정 준비됨. finnde_njaru ƴeewtaade: python3 도구/원격설정.py show')
