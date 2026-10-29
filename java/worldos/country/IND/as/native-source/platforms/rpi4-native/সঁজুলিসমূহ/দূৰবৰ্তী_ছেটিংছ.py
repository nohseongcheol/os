#!/usr/bin/env python3
"""장치별 কী_মান·সংযোগ_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

기준 = Path(__file__).resolve().parents[1]


def প্ৰস্তুত_কৰক(기준=기준):
    পথ = 기준 / 'build/remote'
    পথ.mkdir(parents=True, exist_ok=True)
    বৈশিষ্ট্য = পথ / 'access.json'
    কী_মান = পথ / 'host-key.der'
    if not কী_মান.exists():
        with কী_মান.open('xb') as নথিপত্ৰ:
            os.chmod(str(কী_মান), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=নথিপত্ৰ)
    if not বৈশিষ্ট্য.exists():
        ডাটা = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with বৈশিষ্ট্য.open('x') as নথিপত্ৰ:
            os.chmod(str(বৈশিষ্ট্য), 0o600)
            json.dump(ডাটা, নথিপত্ৰ, ensure_ascii=False, indent=2)
            নথিপত্ৰ.write('\n')
    ডাটা = json.loads(বৈশিষ্ট্য.read_text())
    if not isinstance(ডাটা, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if ডাটা.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for নাম in ('ssh_password', 'vnc_password'):
        if not isinstance(ডাটা.get(নাম), str):
            raise SystemExit('access.json: ' + নাম + '는 문자열이어야 합니다.')
    শ্বেল_পাছৱৰ্ড = ডাটা['ssh_password'].encode('utf-8')
    if len(শ্বেল_পাছৱৰ্ড) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = ডাটা['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. দৈর্ঘ্য_মান 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def শৃঙ্খলা_মান(নাম, মান):
        return 'static const unsigned char '+নাম+'[] = {'+','.join(str(수) for 수 in মান)+'};\n'
    머리 = শৃঙ্খলা_মান('চেলফোন_কী', কী_মান.read_bytes())
    머리 += শৃঙ্খলা_মান('শ্বেল_পাছৱৰ্ড_সাৰাংশ', hashlib.sha256(শ্বেল_পাছৱৰ্ড).digest())
    머리 += শৃঙ্খলা_মান('화면암호', 화면열쇠)
    সৃষ্টি_কৰক = পথ / 'প্ৰ_ফাইল.h'
    সৃষ্টি_কৰক.write_text(머리)
    os.chmod(str(সৃষ্টি_কৰক), 0o600)
    return ডাটা


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('কাৰ্য্য', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = 해석기.parse_args()
    ডাটা = প্ৰস্তুত_কৰক()
    if 인수.কাৰ্য্য == 'show':
        print(json.dumps(ডাটা, ensure_ascii=False, indent=2))
    else:
        print('장치별 দূৰবৰ্তী_মান সংযোগ_e05f319b বৈশিষ্ট্য 준비됨. পাছৱৰ্ড_মান প্ৰমাণিত_কৰক: python3 সঁজুলিসমূহ/দূৰবৰ্তী_ছেটিংছ.py show')
