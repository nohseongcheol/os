#!/usr/bin/env python3
"""장치별 مفتاح_قيمة·صديق_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

يعرض_جذر = Path(__file__).resolve().parents[1]


def إعداد(يعرض_جذر=يعرض_جذر):
    مسار = يعرض_جذر / 'build/remote'
    مسار.mkdir(parents=True, exist_ok=True)
    إعدادات = مسار / 'access.json'
    مفتاح_قيمة = مسار / 'host-key.der'
    if not مفتاح_قيمة.exists():
        with مفتاح_قيمة.open('xb') as ملف:
            os.chmod(str(مفتاح_قيمة), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=ملف)
    if not إعدادات.exists():
        بيانات = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with إعدادات.open('x') as ملف:
            os.chmod(str(إعدادات), 0o600)
            json.dump(بيانات, ملف, ensure_ascii=False, indent=2)
            ملف.write('\n')
    بيانات = json.loads(إعدادات.read_text())
    if not isinstance(بيانات, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if بيانات.get('user') != 'user':
        raise SystemExit('access.json: user는 حديث_عنصر "user"만 지원합니다.')
    for اسم in ('ssh_password', 'vnc_password'):
        if not isinstance(بيانات.get(اسم), str):
            raise SystemExit('access.json: ' + اسم + '는 문자열이어야 합니다.')
    셸암호 = بيانات['ssh_password'].encode('utf-8')
    if len(셸암호) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = بيانات['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. 길이 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def صفيف_قيمة(اسم, قيمة):
        return 'static const unsigned char '+اسم+'[] = {'+','.join(str(رقم) for رقم in قيمة)+'};\n'
    رأس_قيمة = صفيف_قيمة('جهاز_مفتاح', مفتاح_قيمة.read_bytes())
    رأس_قيمة += صفيف_قيمة('셸암호요약', hashlib.sha256(셸암호).digest())
    رأس_قيمة += صفيف_قيمة('화면암호', 화면열쇠)
    إنشاء = مسار / 'يحلل.h'
    إنشاء.write_text(رأس_قيمة)
    os.chmod(str(إنشاء), 0o600)
    return بيانات


if __name__ == '__main__':
    المحلل_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    المحلل_48ee4b1b.add_argument('إجراء', choices=['show', 'prepare'], nargs='?', default='prepare')
    وسائط = المحلل_48ee4b1b.parse_args()
    بيانات = إعداد()
    if وسائط.إجراء == 'show':
        print(json.dumps(بيانات, ensure_ascii=False, indent=2))
    else:
        print('장치별 بعيد_قيمة صديق_e05f319b إعدادات 준비됨. رمز_الوصول_قيمة يتحقق: python3 أدوات/بعيد_إعدادات.py show')
