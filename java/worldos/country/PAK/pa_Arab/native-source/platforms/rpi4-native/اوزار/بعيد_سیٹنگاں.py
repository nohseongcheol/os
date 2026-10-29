#!/usr/bin/env python3
"""장치별 کلید_قدر·کنکشن_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

기준 = Path(__file__).resolve().parents[1]


def تیاری_کرو(기준=기준):
    راہ = 기준 / 'build/remote'
    راہ.mkdir(parents=True, exist_ok=True)
    سیٹنگاں = راہ / 'access.json'
    کلید_قدر = راہ / 'host-key.der'
    if not کلید_قدر.exists():
        with کلید_قدر.open('xb') as فائل:
            os.chmod(str(کلید_قدر), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=فائل)
    if not سیٹنگاں.exists():
        کوائف = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with سیٹنگاں.open('x') as فائل:
            os.chmod(str(سیٹنگاں), 0o600)
            json.dump(کوائف, فائل, ensure_ascii=False, indent=2)
            فائل.write('\n')
    کوائف = json.loads(سیٹنگاں.read_text())
    if not isinstance(کوائف, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if کوائف.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for ناں in ('ssh_password', 'vnc_password'):
        if not isinstance(کوائف.get(ناں), str):
            raise SystemExit('access.json: ' + ناں + '는 문자열이어야 합니다.')
    شیل_لفظی_کنجی = کوائف['ssh_password'].encode('utf-8')
    if len(شیل_لفظی_کنجی) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = کوائف['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. لمبائی_قدر 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def ایرے_قدر(ناں, قدر):
        return 'static const unsigned char '+ناں+'[] = {'+','.join(str(수) for 수 in قدر)+'};\n'
    머리 = ایرے_قدر('آلہ_کلید', کلید_قدر.read_bytes())
    머리 += ایرے_قدر('셸암호요약', hashlib.sha256(شیل_لفظی_کنجی).digest())
    머리 += ایرے_قدر('화면암호', 화면열쇠)
    생성 = راہ / 'پروفائل.h'
    생성.write_text(머리)
    os.chmod(str(생성), 0o600)
    return کوائف


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('کم', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = 해석기.parse_args()
    کوائف = تیاری_کرو()
    if 인수.کم == 'show':
        print(json.dumps(کوائف, ensure_ascii=False, indent=2))
    else:
        print('장치별 بعيد_قدر کنکشن_e05f319b سیٹنگاں 준비됨. لفظی_کنجی_قدر تصدیق_کرو: python3 اوزار/بعيد_سیٹنگاں.py show')
