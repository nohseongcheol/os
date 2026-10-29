#!/usr/bin/env python3
"""장치별 კლავიში_მნიშვნელობა·კავშირი_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

პროეცირება_ფესვი = Path(__file__).resolve().parents[1]


def მომზადება(პროეცირება_ფესვი=პროეცირება_ფესვი):
    გეზი = პროეცირება_ფესვი / 'build/remote'
    გეზი.mkdir(parents=True, exist_ok=True)
    პარამეტრები = გეზი / 'access.json'
    კლავიში_მნიშვნელობა = გეზი / 'host-key.der'
    if not კლავიში_მნიშვნელობა.exists():
        with კლავიში_მნიშვნელობა.open('xb') as ფაილი:
            os.chmod(str(კლავიში_მნიშვნელობა), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=ფაილი)
    if not პარამეტრები.exists():
        მონაცემები = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with პარამეტრები.open('x') as ფაილი:
            os.chmod(str(პარამეტრები), 0o600)
            json.dump(მონაცემები, ფაილი, ensure_ascii=False, indent=2)
            ფაილი.write('\n')
    მონაცემები = json.loads(პარამეტრები.read_text())
    if not isinstance(მონაცემები, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if მონაცემები.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for სახელი in ('ssh_password', 'vnc_password'):
        if not isinstance(მონაცემები.get(სახელი), str):
            raise SystemExit('access.json: ' + სახელი + '는 문자열이어야 합니다.')
    გარემო_პაროლი = მონაცემები['ssh_password'].encode('utf-8')
    if len(გარემო_პაროლი) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = მონაცემები['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. სიგრძე_მნიშვნელობა 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def მასივი_მნიშვნელობა(სახელი, მნიშვნელობა):
        return 'static const unsigned char '+სახელი+'[] = {'+','.join(str(수) for 수 in მნიშვნელობა)+'};\n'
    머리 = მასივი_მნიშვნელობა('მობილური_კლავიში', კლავიში_მნიშვნელობა.read_bytes())
    머리 += მასივი_მნიშვნელობა('გარემო_პაროლი_რეზიუმე', hashlib.sha256(გარემო_პაროლი).digest())
    머리 += მასივი_მნიშვნელობა('화면암호', 화면열쇠)
    დაგენერირება = გეზი / 'პროფილი.h'
    დაგენერირება.write_text(머리)
    os.chmod(str(დაგენერირება), 0o600)
    return მონაცემები


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('ქმედება', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = 해석기.parse_args()
    მონაცემები = მომზადება()
    if 인수.ქმედება == 'show':
        print(json.dumps(მონაცემები, ensure_ascii=False, indent=2))
    else:
        print('장치별 დისტანციური_მნიშვნელობა კავშირი_e05f319b პარამეტრები 준비됨. პაროლი_მნიშვნელობა გადამოწმება: python3 ხელსაწყოები/დისტანციური_პარამეტრები.py show')
