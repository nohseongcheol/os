#!/usr/bin/env python3
"""장치별 کلیل_نرخ·گرێدان_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

기준 = Path(__file__).resolve().parents[1]


def ئامادە_کردن_9ce364fc(기준=기준):
    گوزەر = 기준 / 'build/remote'
    گوزەر.mkdir(parents=True, exist_ok=True)
    ڕێكبەندەكان = گوزەر / 'access.json'
    کلیل_نرخ = گوزەر / 'host-key.der'
    if not کلیل_نرخ.exists():
        with کلیل_نرخ.open('xb') as فایل:
            os.chmod(str(کلیل_نرخ), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=فایل)
    if not ڕێكبەندەكان.exists():
        دەیتا = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with ڕێكبەندەكان.open('x') as فایل:
            os.chmod(str(ڕێكبەندەكان), 0o600)
            json.dump(دەیتا, فایل, ensure_ascii=False, indent=2)
            فایل.write('\n')
    دەیتا = json.loads(ڕێكبەندەكان.read_text())
    if not isinstance(دەیتا, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if دەیتا.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for ناو in ('ssh_password', 'vnc_password'):
        if not isinstance(دەیتا.get(ناو), str):
            raise SystemExit('access.json: ' + ناو + '는 문자열이어야 합니다.')
    توێکڵ_نهێنوشە = دەیتا['ssh_password'].encode('utf-8')
    if len(توێکڵ_نهێنوشە) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = دەیتا['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. درێژی_نرخ 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def ڕیزی_داتا_نرخ(ناو, نرخ):
        return 'static const unsigned char '+ناو+'[] = {'+','.join(str(수) for 수 in نرخ)+'};\n'
    머리 = ڕیزی_داتا_نرخ('ئامێر_کلیل', کلیل_نرخ.read_bytes())
    머리 += ڕیزی_داتا_نرخ('셸암호요약', hashlib.sha256(توێکڵ_نهێنوشە).digest())
    머리 += ڕیزی_داتا_نرخ('화면암호', 화면열쇠)
    생성 = گوزەر / 'پرۆفایل.h'
    생성.write_text(머리)
    os.chmod(str(생성), 0o600)
    return دەیتا


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('ئاکشن', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = 해석기.parse_args()
    دەیتا = ئامادە_کردن_9ce364fc()
    if 인수.ئاکشن == 'show':
        print(json.dumps(دەیتا, ensure_ascii=False, indent=2))
    else:
        print('장치별 دوورەدەس_نرخ گرێدان_e05f319b ڕێكبەندەكان 준비됨. نهێنوشە_نرخ سەلماندن: python3 ئامرازەکان/دوورەدەس_ڕێكبەندەكان.py show')
