#!/usr/bin/env python3
"""장치별 מקש_ערך·קשר_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

לשקף_בסיס = Path(__file__).resolve().parents[1]


def להכין(לשקף_בסיס=לשקף_בסיס):
    נתיב = לשקף_בסיס / 'build/remote'
    נתיב.mkdir(parents=True, exist_ok=True)
    הגדרות = נתיב / 'access.json'
    מקש_ערך = נתיב / 'host-key.der'
    if not מקש_ערך.exists():
        with מקש_ערך.open('xb') as קובץ:
            os.chmod(str(מקש_ערך), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=קובץ)
    if not הגדרות.exists():
        נתונים = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with הגדרות.open('x') as קובץ:
            os.chmod(str(הגדרות), 0o600)
            json.dump(נתונים, קובץ, ensure_ascii=False, indent=2)
            קובץ.write('\n')
    נתונים = json.loads(הגדרות.read_text())
    if not isinstance(נתונים, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if נתונים.get('user') != 'user':
        raise SystemExit('access.json: user는 נוכחי_פריט "user"만 지원합니다.')
    for שם in ('ssh_password', 'vnc_password'):
        if not isinstance(נתונים.get(שם), str):
            raise SystemExit('access.json: ' + שם + '는 문자열이어야 합니다.')
    מעטפת_סיסמה = נתונים['ssh_password'].encode('utf-8')
    if len(מעטפת_סיסמה) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = נתונים['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. 길이 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def מערך_ערך(שם, ערך):
        return 'static const unsigned char '+שם+'[] = {'+','.join(str(수) for 수 in ערך)+'};\n'
    ראש_ערך = מערך_ערך('התקן_מקש', מקש_ערך.read_bytes())
    ראש_ערך += מערך_ערך('מעטפת_סיסמה_סיכום', hashlib.sha256(מעטפת_סיסמה).digest())
    ראש_ערך += מערך_ערך('화면암호', 화면열쇠)
    יצר = נתיב / 'פרופיל.h'
    יצר.write_text(ראש_ערך)
    os.chmod(str(יצר), 0o600)
    return נתונים


if __name__ == '__main__':
    מנתח_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    מנתח_48ee4b1b.add_argument('פעולה', choices=['show', 'prepare'], nargs='?', default='prepare')
    ארגומנטים = מנתח_48ee4b1b.parse_args()
    נתונים = להכין()
    if ארגומנטים.פעולה == 'show':
        print(json.dumps(נתונים, ensure_ascii=False, indent=2))
    else:
        print('장치별 מרוחק_ערך קשר_e05f319b הגדרות 준비됨. סיסמה_ערך ודא_אמת: python3 כלים/מרוחק_הגדרות.py show')
