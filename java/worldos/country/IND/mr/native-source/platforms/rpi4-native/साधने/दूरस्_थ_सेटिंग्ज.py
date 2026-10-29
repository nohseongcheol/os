#!/usr/bin/env python3
"""장치별 कळ_मूल्य·कनेक्शन_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

प्रोजेक्ट_मूळ = Path(__file__).resolve().parents[1]


def तयार_करणे(प्रोजेक्ट_मूळ=प्रोजेक्ट_मूळ):
    मार्ग = प्रोजेक्ट_मूळ / 'build/remote'
    मार्ग.mkdir(parents=True, exist_ok=True)
    संयोजना = मार्ग / 'access.json'
    कळ_मूल्य = मार्ग / 'host-key.der'
    if not कळ_मूल्य.exists():
        with कळ_मूल्य.open('xb') as फाइल:
            os.chmod(str(कळ_मूल्य), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=फाइल)
    if not संयोजना.exists():
        डेटा = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with संयोजना.open('x') as फाइल:
            os.chmod(str(संयोजना), 0o600)
            json.dump(डेटा, फाइल, ensure_ascii=False, indent=2)
            फाइल.write('\n')
    डेटा = json.loads(संयोजना.read_text())
    if not isinstance(डेटा, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if डेटा.get('user') != 'user':
        raise SystemExit('access.json: user는 सध्याचे_आयटम "user"만 지원합니다.')
    for नाव in ('ssh_password', 'vnc_password'):
        if not isinstance(डेटा.get(नाव), str):
            raise SystemExit('access.json: ' + नाव + '는 문자열이어야 합니다.')
    शेल_पासवर्ड = डेटा['ssh_password'].encode('utf-8')
    if len(शेल_पासवर्ड) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        पडदा_पासवर्ड = डेटा['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. लांबी_मूल्य 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    पडदा_कळ = पडदा_पासवर्ड[:8].ljust(8, b'\0')
    def ऍरे_मूल्य(नाव, मूल्य):
        return 'static const unsigned char '+नाव+'[] = {'+','.join(str(संख्या) for संख्या in मूल्य)+'};\n'
    शीर्ष_मूल्य = ऍरे_मूल्य('मोबाइल_कळ', कळ_मूल्य.read_bytes())
    शीर्ष_मूल्य += ऍरे_मूल्य('शेल_पासवर्ड_सारांश', hashlib.sha256(शेल_पासवर्ड).digest())
    शीर्ष_मूल्य += ऍरे_मूल्य('पडदा_पासवर्ड', पडदा_कळ)
    तयार_करा = मार्ग / 'प्रोफाइल.h'
    तयार_करा.write_text(शीर्ष_मूल्य)
    os.chmod(str(तयार_करा), 0o600)
    return डेटा


if __name__ == '__main__':
    व्याकरणविश्लेषक_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    व्याकरणविश्लेषक_48ee4b1b.add_argument('कृती', choices=['show', 'prepare'], nargs='?', default='prepare')
    बाबी = व्याकरणविश्लेषक_48ee4b1b.parse_args()
    डेटा = तयार_करणे()
    if बाबी.कृती == 'show':
        print(json.dumps(डेटा, ensure_ascii=False, indent=2))
    else:
        print('장치별 दूरस्_थ_मूल्य कनेक्शन_e05f319b संयोजना आहे_तयारकेलेले. पासवर्ड_मूल्य पडताळा: python3 साधने/दूरस्_थ_सेटिंग्ज.py show')
