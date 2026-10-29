#!/usr/bin/env python3
"""장치별 کلید_مقدار·اتصال_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

نمایش_دادن_جذر = Path(__file__).resolve().parents[1]


def آماده_کردن(نمایش_دادن_جذر=نمایش_دادن_جذر):
    مسیر = نمایش_دادن_جذر / 'build/remote'
    مسیر.mkdir(parents=True, exist_ok=True)
    تنظیمات = مسیر / 'access.json'
    کلید_مقدار = مسیر / 'host-key.der'
    if not کلید_مقدار.exists():
        with کلید_مقدار.open('xb') as پرونده:
            os.chmod(str(کلید_مقدار), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=پرونده)
    if not تنظیمات.exists():
        داده_ها = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with تنظیمات.open('x') as پرونده:
            os.chmod(str(تنظیمات), 0o600)
            json.dump(داده_ها, پرونده, ensure_ascii=False, indent=2)
            پرونده.write('\n')
    داده_ها = json.loads(تنظیمات.read_text())
    if not isinstance(داده_ها, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if داده_ها.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for نام in ('ssh_password', 'vnc_password'):
        if not isinstance(داده_ها.get(نام), str):
            raise SystemExit('access.json: ' + نام + '는 문자열이어야 합니다.')
    واسط_رمز_عبور = داده_ها['ssh_password'].encode('utf-8')
    if len(واسط_رمز_عبور) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = داده_ها['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. طول_مقدار 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def آرايه_مقدار(نام, مقدار):
        return 'static const unsigned char '+نام+'[] = {'+','.join(str(수) for 수 in مقدار)+'};\n'
    머리 = آرايه_مقدار('دستگاه_کلید', کلید_مقدار.read_bytes())
    머리 += آرايه_مقدار('واسط_رمز_عبور_خلاصه', hashlib.sha256(واسط_رمز_عبور).digest())
    머리 += آرايه_مقدار('화면암호', 화면열쇠)
    ایجاد = مسیر / 'نمایه.h'
    ایجاد.write_text(머리)
    os.chmod(str(ایجاد), 0o600)
    return داده_ها


if __name__ == '__main__':
    مفسر_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    مفسر_48ee4b1b.add_argument('کنش', choices=['show', 'prepare'], nargs='?', default='prepare')
    نشانوندها = مفسر_48ee4b1b.parse_args()
    داده_ها = آماده_کردن()
    if نشانوندها.کنش == 'show':
        print(json.dumps(داده_ها, ensure_ascii=False, indent=2))
    else:
        print('장치별 راه_دور_مقدار اتصال_e05f319b تنظیمات 준비됨. رمز_عبور_مقدار تأیید_صحت: python3 ابزارها/راه_دور_تنظیمات.py show')
