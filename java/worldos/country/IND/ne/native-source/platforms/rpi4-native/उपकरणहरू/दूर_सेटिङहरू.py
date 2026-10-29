#!/usr/bin/env python3
"""장치별 कुञ्जी_मान·जडान_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

परियोजना_रूट = Path(__file__).resolve().parents[1]


def तयार_गर्नुहोस्(परियोजना_रूट=परियोजना_रूट):
    मार्ग = परियोजना_रूट / 'build/remote'
    मार्ग.mkdir(parents=True, exist_ok=True)
    सेटिङ = मार्ग / 'access.json'
    कुञ्जी_मान = मार्ग / 'host-key.der'
    if not कुञ्जी_मान.exists():
        with कुञ्जी_मान.open('xb') as फाइल:
            os.chmod(str(कुञ्जी_मान), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=फाइल)
    if not सेटिङ.exists():
        लगत = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with सेटिङ.open('x') as फाइल:
            os.chmod(str(सेटिङ), 0o600)
            json.dump(लगत, फाइल, ensure_ascii=False, indent=2)
            फाइल.write('\n')
    लगत = json.loads(सेटिङ.read_text())
    if not isinstance(लगत, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if लगत.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for नाम in ('ssh_password', 'vnc_password'):
        if not isinstance(लगत.get(नाम), str):
            raise SystemExit('access.json: ' + नाम + '는 문자열이어야 합니다.')
    शेल_पासवर्ड = लगत['ssh_password'].encode('utf-8')
    if len(शेल_पासवर्ड) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = लगत['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. लम्बाइ_मान 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def विन्यास_मान(नाम, मान):
        return 'static const unsigned char '+नाम+'[] = {'+','.join(str(수) for 수 in मान)+'};\n'
    머리 = विन्यास_मान('मोबाइल_कुञ्जी', कुञ्जी_मान.read_bytes())
    머리 += विन्यास_मान('शेल_पासवर्ड_सारांश', hashlib.sha256(शेल_पासवर्ड).digest())
    머리 += विन्यास_मान('화면암호', 화면열쇠)
    सिर्जना_गर्नुहोस् = मार्ग / 'प्रोफाइल.h'
    सिर्जना_गर्नुहोस्.write_text(머리)
    os.chmod(str(सिर्जना_गर्नुहोस्), 0o600)
    return लगत


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('कार्य', choices=['show', 'prepare'], nargs='?', default='prepare')
    तर्क = 해석기.parse_args()
    लगत = तयार_गर्नुहोस्()
    if तर्क.कार्य == 'show':
        print(json.dumps(लगत, ensure_ascii=False, indent=2))
    else:
        print('장치별 दूर_मान जडान_e05f319b सेटिङ 준비됨. पासवर्ड_मान रुजू_गर्नुहोस्: python3 उपकरणहरू/दूर_सेटिङहरू.py show')
