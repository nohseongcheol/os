#!/usr/bin/env python3
"""장치별 bọ́tìnnì_iye·Ìsomọ́_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

기준 = Path(__file__).resolve().parents[1]


def gbaradì(기준=기준):
    ọ̀nà = 기준 / 'build/remote'
    ọ̀nà.mkdir(parents=True, exist_ok=True)
    Àwọn_ààtò = ọ̀nà / 'access.json'
    bọ́tìnnì_iye = ọ̀nà / 'host-key.der'
    if not bọ́tìnnì_iye.exists():
        with bọ́tìnnì_iye.open('xb') as Fáìlì:
            os.chmod(str(bọ́tìnnì_iye), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Fáìlì)
    if not Àwọn_ààtò.exists():
        détà = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Àwọn_ààtò.open('x') as Fáìlì:
            os.chmod(str(Àwọn_ààtò), 0o600)
            json.dump(détà, Fáìlì, ensure_ascii=False, indent=2)
            Fáìlì.write('\n')
    détà = json.loads(Àwọn_ààtò.read_text())
    if not isinstance(détà, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if détà.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for Orúkọ in ('ssh_password', 'vnc_password'):
        if not isinstance(détà.get(Orúkọ), str):
            raise SystemExit('access.json: ' + Orúkọ + '는 문자열이어야 합니다.')
    ṣẹ́ẹ̀lì_ọ̀rọ̀_aṣínà = détà['ssh_password'].encode('utf-8')
    if len(ṣẹ́ẹ̀lì_ọ̀rọ̀_aṣínà) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = détà['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. gígùn_iye 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def ÀRÉÈ_iye(Orúkọ, iye):
        return 'static const unsigned char '+Orúkọ+'[] = {'+','.join(str(수) for 수 in iye)+'};\n'
    머리 = ÀRÉÈ_iye('ohun_èlò_bọ́tìnnì', bọ́tìnnì_iye.read_bytes())
    머리 += ÀRÉÈ_iye('ṣẹ́ẹ̀lì_ọ̀rọ̀_aṣínà_ìṣoníṣókí', hashlib.sha256(ṣẹ́ẹ̀lì_ọ̀rọ̀_aṣínà).digest())
    머리 += ÀRÉÈ_iye('화면암호', 화면열쇠)
    생성 = ọ̀nà / 'Ìrísí_Olùlò.h'
    생성.write_text(머리)
    os.chmod(str(생성), 0o600)
    return détà


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('ìṣe', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = 해석기.parse_args()
    détà = gbaradì()
    if 인수.ìṣe == 'show':
        print(json.dumps(détà, ensure_ascii=False, indent=2))
    else:
        print('장치별 Ìjìnnà_iye Ìsomọ́_e05f319b Àwọn_ààtò 준비됨. ọ̀rọ̀_aṣínà_iye ridájú: python3 Àwọn_irinṣẹ́/Ìjìnnà_Àwọn_ààtò.py show')
