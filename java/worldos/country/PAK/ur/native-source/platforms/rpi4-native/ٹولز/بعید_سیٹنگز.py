#!/usr/bin/env python3
"""장치별 کلید_قدر·رابطہ_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

عکس_ڈالنا_روٹ = Path(__file__).resolve().parents[1]


def تیار_کریں(عکس_ڈالنا_روٹ=عکس_ڈالنا_روٹ):
    راستہ_2 = عکس_ڈالنا_روٹ / 'build/remote'
    راستہ_2.mkdir(parents=True, exist_ok=True)
    ترتیبات = راستہ_2 / 'access.json'
    کلید_قدر = راستہ_2 / 'host-key.der'
    if not کلید_قدر.exists():
        with کلید_قدر.open('xb') as فائل_کا_نام:
            os.chmod(str(کلید_قدر), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=فائل_کا_نام)
    if not ترتیبات.exists():
        کوائف = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with ترتیبات.open('x') as فائل_کا_نام:
            os.chmod(str(ترتیبات), 0o600)
            json.dump(کوائف, فائل_کا_نام, ensure_ascii=False, indent=2)
            فائل_کا_نام.write('\n')
    کوائف = json.loads(ترتیبات.read_text())
    if not isinstance(کوائف, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if کوائف.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for نام in ('ssh_password', 'vnc_password'):
        if not isinstance(کوائف.get(نام), str):
            raise SystemExit('access.json: ' + نام + '는 문자열이어야 합니다.')
    شیل_پاس_ورڈ = کوائف['ssh_password'].encode('utf-8')
    if len(شیل_پاس_ورڈ) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = کوائف['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. لمبا_ئی_قدر 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def لڑی_قدر(نام, قدر):
        return 'static const unsigned char '+نام+'[] = {'+','.join(str(수) for 수 in قدر)+'};\n'
    머리 = لڑی_قدر('آلہ_کلید', کلید_قدر.read_bytes())
    머리 += لڑی_قدر('شیل_پاس_ورڈ_خلاصہ', hashlib.sha256(شیل_پاس_ورڈ).digest())
    머리 += لڑی_قدر('화면암호', 화면열쇠)
    تخلیق_کرنا = راستہ_2 / 'پروفائل.h'
    تخلیق_کرنا.write_text(머리)
    os.chmod(str(تخلیق_کرنا), 0o600)
    return کوائف


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('عمل', choices=['show', 'prepare'], nargs='?', default='prepare')
    دلائل = 해석기.parse_args()
    کوائف = تیار_کریں()
    if دلائل.عمل == 'show':
        print(json.dumps(کوائف, ensure_ascii=False, indent=2))
    else:
        print('장치별 بعید_قدر رابطہ_e05f319b ترتیبات 준비됨. پاس_ورڈ_قدر تصدیق_کریں: python3 ٹولز/بعید_سیٹنگز.py show')
