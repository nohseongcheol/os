#!/usr/bin/env python3
"""장치별 ڪليد_قدر·ڪنيڪشن_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

기준 = Path(__file__).resolve().parents[1]


def تياري_ڪريو(기준=기준):
    راههه = 기준 / 'build/remote'
    راههه.mkdir(parents=True, exist_ok=True)
    سيٽنگون = راههه / 'access.json'
    ڪليد_قدر = راههه / 'host-key.der'
    if not ڪليد_قدر.exists():
        with ڪليد_قدر.open('xb') as فائل:
            os.chmod(str(ڪليد_قدر), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=فائل)
    if not سيٽنگون.exists():
        ڪوائف = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with سيٽنگون.open('x') as فائل:
            os.chmod(str(سيٽنگون), 0o600)
            json.dump(ڪوائف, فائل, ensure_ascii=False, indent=2)
            فائل.write('\n')
    ڪوائف = json.loads(سيٽنگون.read_text())
    if not isinstance(ڪوائف, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if ڪوائف.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for نالو in ('ssh_password', 'vnc_password'):
        if not isinstance(ڪوائف.get(نالو), str):
            raise SystemExit('access.json: ' + نالو + '는 문자열이어야 합니다.')
    شيل_پاس_ورڊ = ڪوائف['ssh_password'].encode('utf-8')
    if len(شيل_پاس_ورڊ) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = ڪوائف['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. لمبائي_قدر 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def ترتيب_قدر_ed437109(نالو, قدر):
        return 'static const unsigned char '+نالو+'[] = {'+','.join(str(수) for 수 in قدر)+'};\n'
    머리 = ترتيب_قدر_ed437109('آلو_ڪليد', ڪليد_قدر.read_bytes())
    머리 += ترتيب_قدر_ed437109('셸암호요약', hashlib.sha256(شيل_پاس_ورڊ).digest())
    머리 += ترتيب_قدر_ed437109('화면암호', 화면열쇠)
    생성 = راههه / 'پروفائيل.h'
    생성.write_text(머리)
    os.chmod(str(생성), 0o600)
    return ڪوائف


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('عمل', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = 해석기.parse_args()
    ڪوائف = تياري_ڪريو()
    if 인수.عمل == 'show':
        print(json.dumps(ڪوائف, ensure_ascii=False, indent=2))
    else:
        print('장치별 بعيد_قدر ڪنيڪشن_e05f319b سيٽنگون 준비됨. پاس_ورڊ_قدر تصديق_ڪريو: python3 اوزار/بعيد_سيٽنگون.py show')
