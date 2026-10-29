#!/usr/bin/env python3
"""장치별 ئاچقۇچ_قىممىتى·ئۇلىنىش_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

كۆرسىتىش_يىلتىز = Path(__file__).resolve().parents[1]


def تەييارلىماق(كۆرسىتىش_يىلتىز=كۆرسىتىش_يىلتىز):
    يول = كۆرسىتىش_يىلتىز / 'build/remote'
    يول.mkdir(parents=True, exist_ok=True)
    تەڭشەكلەر = يول / 'access.json'
    ئاچقۇچ_قىممىتى = يول / 'host-key.der'
    if not ئاچقۇچ_قىممىتى.exists():
        with ئاچقۇچ_قىممىتى.open('xb') as ھۆججەت:
            os.chmod(str(ئاچقۇچ_قىممىتى), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=ھۆججەت)
    if not تەڭشەكلەر.exists():
        مەلۇمات = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with تەڭشەكلەر.open('x') as ھۆججەت:
            os.chmod(str(تەڭشەكلەر), 0o600)
            json.dump(مەلۇمات, ھۆججەت, ensure_ascii=False, indent=2)
            ھۆججەت.write('\n')
    مەلۇمات = json.loads(تەڭشەكلەر.read_text())
    if not isinstance(مەلۇمات, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if مەلۇمات.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for ئاتى in ('ssh_password', 'vnc_password'):
        if not isinstance(مەلۇمات.get(ئاتى), str):
            raise SystemExit('access.json: ' + ئاتى + '는 문자열이어야 합니다.')
    قاپ_پارول = مەلۇمات['ssh_password'].encode('utf-8')
    if len(قاپ_پارول) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = مەلۇمات['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. ئۇزۇنلۇق_قىممىتى 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def رەت_قىممىتى(ئاتى, قىممىتى):
        return 'static const unsigned char '+ئاتى+'[] = {'+','.join(str(수) for 수 in قىممىتى)+'};\n'
    머리 = رەت_قىممىتى('كۆچمە_ئاچقۇچ', ئاچقۇچ_قىممىتى.read_bytes())
    머리 += رەت_قىممىتى('셸암호요약', hashlib.sha256(قاپ_پارول).digest())
    머리 += رەت_قىممىتى('화면암호', 화면열쇠)
    ھاسىل_قىلىش = يول / 'ئارخىپ_1c9b560a.h'
    ھاسىل_قىلىش.write_text(머리)
    os.chmod(str(ھاسىل_قىلىش), 0o600)
    return مەلۇمات


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('مەشغۇلات', choices=['show', 'prepare'], nargs='?', default='prepare')
    ئۆزگەرگۈچىلەر = 해석기.parse_args()
    مەلۇمات = تەييارلىماق()
    if ئۆزگەرگۈچىلەر.مەشغۇلات == 'show':
        print(json.dumps(مەلۇمات, ensure_ascii=False, indent=2))
    else:
        print('장치별 يىراق_قىممىتى ئۇلىنىش_e05f319b تەڭشەكلەر 준비됨. پارول_قىممىتى دەلىللىمەك: python3 قوراللار/يىراق_تەڭشەك.py show')
