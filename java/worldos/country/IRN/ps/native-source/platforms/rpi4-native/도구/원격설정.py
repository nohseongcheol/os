#!/usr/bin/env python3
"""장치별 کيلي_ارزښت·پيوستون_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

기준 = Path(__file__).resolve().parents[1]


def 준비(기준=기준):
    يونلور = 기준 / 'build/remote'
    يونلور.mkdir(parents=True, exist_ok=True)
    امستنې = يونلور / 'access.json'
    کيلي_ارزښت = يونلور / 'host-key.der'
    if not کيلي_ارزښت.exists():
        with کيلي_ارزښت.open('xb') as دوتنه:
            os.chmod(str(کيلي_ارزښت), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=دوتنه)
    if not امستنې.exists():
        اومتوک = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with امستنې.open('x') as دوتنه:
            os.chmod(str(امستنې), 0o600)
            json.dump(اومتوک, دوتنه, ensure_ascii=False, indent=2)
            دوتنه.write('\n')
    اومتوک = json.loads(امستنې.read_text())
    if not isinstance(اومتوک, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if اومتوک.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for نوم in ('ssh_password', 'vnc_password'):
        if not isinstance(اومتوک.get(نوم), str):
            raise SystemExit('access.json: ' + نوم + '는 문자열이어야 합니다.')
    سیپۍ_تېرنويى = اومتوک['ssh_password'].encode('utf-8')
    if len(سیپۍ_تېرنويى) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = اومتوک['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. اوږدوالى_ارزښت 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def لړوند_ارزښت(نوم, ارزښت):
        return 'static const unsigned char '+نوم+'[] = {'+','.join(str(수) for 수 in ارزښت)+'};\n'
    머리 = لړوند_ارزښت('وزله_کيلي', کيلي_ارزښت.read_bytes())
    머리 += لړوند_ارزښت('셸암호요약', hashlib.sha256(سیپۍ_تېرنويى).digest())
    머리 += لړوند_ارزښت('화면암호', 화면열쇠)
    생성 = يونلور / 'کارن_پېژنيال.h'
    생성.write_text(머리)
    os.chmod(str(생성), 0o600)
    return اومتوک


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('چار', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = 해석기.parse_args()
    اومتوک = 준비()
    if 인수.چار == 'show':
        print(json.dumps(اومتوک, ensure_ascii=False, indent=2))
    else:
        print('장치별 원격 پيوستون_e05f319b امستنې 준비됨. تېرنويى_ارزښت 확인: python3 도구/원격설정.py show')
