#!/usr/bin/env python3
"""장치별 कुंजी_मान·कनेक्शन_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

प्रोजेक्ट_करें_मूल = Path(__file__).resolve().parents[1]


def 준비(प्रोजेक्ट_करें_मूल=प्रोजेक्ट_करें_मूल):
    पथ = प्रोजेक्ट_करें_मूल / 'build/remote'
    पथ.mkdir(parents=True, exist_ok=True)
    विन्यास = पथ / 'access.json'
    कुंजी_मान = पथ / 'host-key.der'
    if not कुंजी_मान.exists():
        with कुंजी_मान.open('xb') as संचिका:
            os.chmod(str(कुंजी_मान), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=संचिका)
    if not विन्यास.exists():
        आँकड़े = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with विन्यास.open('x') as संचिका:
            os.chmod(str(विन्यास), 0o600)
            json.dump(आँकड़े, संचिका, ensure_ascii=False, indent=2)
            संचिका.write('\n')
    आँकड़े = json.loads(विन्यास.read_text())
    if not isinstance(आँकड़े, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if आँकड़े.get('user') != 'user':
        raise SystemExit('access.json: user는 अद्यतित_आइटम "user"만 지원합니다.')
    for नाम in ('ssh_password', 'vnc_password'):
        if not isinstance(आँकड़े.get(नाम), str):
            raise SystemExit('access.json: ' + नाम + '는 문자열이어야 합니다.')
    शेल_पासवर्ड = आँकड़े['ssh_password'].encode('utf-8')
    if len(शेल_पासवर्ड) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = आँकड़े['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. 길이 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def सरणी_मान(नाम, मान):
        return 'static const unsigned char '+नाम+'[] = {'+','.join(str(수) for 수 in मान)+'};\n'
    머리 = सरणी_मान('उपकरण_कुंजी', कुंजी_मान.read_bytes())
    머리 += सरणी_मान('शेल_पासवर्ड_सारांश', hashlib.sha256(शेल_पासवर्ड).digest())
    머리 += सरणी_मान('화면암호', 화면열쇠)
    जनरेट_करें = पथ / 'प्रोफ़ाइल.h'
    जनरेट_करें.write_text(머리)
    os.chmod(str(जनरेट_करें), 0o600)
    return आँकड़े


if __name__ == '__main__':
    पार्सर_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    पार्सर_48ee4b1b.add_argument('क्रिया', choices=['show', 'prepare'], nargs='?', default='prepare')
    तर्क = पार्सर_48ee4b1b.parse_args()
    आँकड़े = 준비()
    if तर्क.क्रिया == 'show':
        print(json.dumps(आँकड़े, ensure_ascii=False, indent=2))
    else:
        print('장치별 दूरस्थ_मान कनेक्शन_e05f319b विन्यास 준비됨. पासवर्ड_मान सत्यापित_करें: python3 उपकरण/दूरस्थ_सेटिंग.py show')
