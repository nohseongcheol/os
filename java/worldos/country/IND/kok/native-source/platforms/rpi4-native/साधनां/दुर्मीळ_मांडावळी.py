#!/usr/bin/env python3
"""장치별 की_मोल·कनॅक्शन_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

प्रॉजॅक्ट_रूट = Path(__file__).resolve().parents[1]


def तयार_करचें_9ce364fc(प्रॉजॅक्ट_रूट=प्रॉजॅक्ट_रूट):
    पाथ = प्रॉजॅक्ट_रूट / 'build/remote'
    पाथ.mkdir(parents=True, exist_ok=True)
    मांडावळी = पाथ / 'access.json'
    की_मोल = पाथ / 'host-key.der'
    if not की_मोल.exists():
        with की_मोल.open('xb') as फायल:
            os.chmod(str(की_मोल), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=फायल)
    if not मांडावळी.exists():
        डेटा = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with मांडावळी.open('x') as फायल:
            os.chmod(str(मांडावळी), 0o600)
            json.dump(डेटा, फायल, ensure_ascii=False, indent=2)
            फायल.write('\n')
    डेटा = json.loads(मांडावळी.read_text())
    if not isinstance(डेटा, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if डेटा.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for नांव in ('ssh_password', 'vnc_password'):
        if not isinstance(डेटा.get(नांव), str):
            raise SystemExit('access.json: ' + नांव + '는 문자열이어야 합니다.')
    शॅल_पासवर्ड = डेटा['ssh_password'].encode('utf-8')
    if len(शॅल_पासवर्ड) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = डेटा['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. लांबाय_मोल 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def क्रम_मोल_ed437109(नांव, मोल):
        return 'static const unsigned char '+नांव+'[] = {'+','.join(str(수) for 수 in मोल)+'};\n'
    머리 = क्रम_मोल_ed437109('मोबायल_की', की_मोल.read_bytes())
    머리 += क्रम_मोल_ed437109('शॅल_पासवर्ड_सारांश', hashlib.sha256(शॅल_पासवर्ड).digest())
    머리 += क्रम_मोल_ed437109('화면암호', 화면열쇠)
    तयार_करचें = पाथ / 'प्रोफायल.h'
    तयार_करचें.write_text(머리)
    os.chmod(str(तयार_करचें), 0o600)
    return डेटा


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('कृती', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = 해석기.parse_args()
    डेटा = तयार_करचें_9ce364fc()
    if 인수.कृती == 'show':
        print(json.dumps(डेटा, ensure_ascii=False, indent=2))
    else:
        print('장치별 दुर्मीळ_मोल कनॅक्शन_e05f319b मांडावळी 준비됨. पासवर्ड_मोल पुनर्तपासणी_करची: python3 साधनां/दुर्मीळ_मांडावळी.py show')
