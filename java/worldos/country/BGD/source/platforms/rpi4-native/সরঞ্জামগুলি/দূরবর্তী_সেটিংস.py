#!/usr/bin/env python3
"""장치별 কী_মান·সংযোগ_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

প্রকল্প_মূল = Path(__file__).resolve().parents[1]


def প্রস্তুত_করুন(প্রকল্প_মূল=প্রকল্প_মূল):
    পথ_2 = প্রকল্প_মূল / 'build/remote'
    পথ_2.mkdir(parents=True, exist_ok=True)
    সেটিংস = পথ_2 / 'access.json'
    কী_মান = পথ_2 / 'host-key.der'
    if not কী_মান.exists():
        with কী_মান.open('xb') as নথির_নাম:
            os.chmod(str(কী_মান), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=নথির_নাম)
    if not সেটিংস.exists():
        ডাটা = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with সেটিংস.open('x') as নথির_নাম:
            os.chmod(str(সেটিংস), 0o600)
            json.dump(ডাটা, নথির_নাম, ensure_ascii=False, indent=2)
            নথির_নাম.write('\n')
    ডাটা = json.loads(সেটিংস.read_text())
    if not isinstance(ডাটা, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if ডাটা.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for নাম in ('ssh_password', 'vnc_password'):
        if not isinstance(ডাটা.get(নাম), str):
            raise SystemExit('access.json: ' + নাম + '는 문자열이어야 합니다.')
    শেল_পাসওয়ার্ড = ডাটা['ssh_password'].encode('utf-8')
    if len(শেল_পাসওয়ার্ড) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = ডাটা['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. দৈর্ঘ্য_মান 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def অ্যারে_মান(নাম, মান):
        return 'static const unsigned char '+নাম+'[] = {'+','.join(str(수) for 수 in মান)+'};\n'
    머리 = অ্যারে_মান('ডিভাইস_কী', কী_মান.read_bytes())
    머리 += অ্যারে_মান('শেল_পাসওয়ার্ড_সামারি', hashlib.sha256(শেল_পাসওয়ার্ড).digest())
    머리 += অ্যারে_মান('화면암호', 화면열쇠)
    সৃষ্টি_করুন = পথ_2 / 'বিবরণী.h'
    সৃষ্টি_করুন.write_text(머리)
    os.chmod(str(সৃষ্টি_করুন), 0o600)
    return ডাটা


if __name__ == '__main__':
    পার্সার_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    পার্সার_48ee4b1b.add_argument('কাজ', choices=['show', 'prepare'], nargs='?', default='prepare')
    আর্গুমেন্ট_তালিকা = পার্সার_48ee4b1b.parse_args()
    ডাটা = প্রস্তুত_করুন()
    if আর্গুমেন্ট_তালিকা.কাজ == 'show':
        print(json.dumps(ডাটা, ensure_ascii=False, indent=2))
    else:
        print('장치별 দূরবর্তী_মান সংযোগ_e05f319b সেটিংস 준비됨. পাসওয়ার্ড_মান যাচাই_করা: python3 সরঞ্জামগুলি/দূরবর্তী_সেটিংস.py show')
