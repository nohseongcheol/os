#!/usr/bin/env python3
"""장치별 Kitufe_thamani·muunganisho_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

기준 = Path(__file__).resolve().parents[1]


def Andaa(기준=기준):
    njia = 기준 / 'build/remote'
    njia.mkdir(parents=True, exist_ok=True)
    Mipangilio = njia / 'access.json'
    Kitufe_thamani = njia / 'host-key.der'
    if not Kitufe_thamani.exists():
        with Kitufe_thamani.open('xb') as faili:
            os.chmod(str(Kitufe_thamani), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=faili)
    if not Mipangilio.exists():
        data = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Mipangilio.open('x') as faili:
            os.chmod(str(Mipangilio), 0o600)
            json.dump(data, faili, ensure_ascii=False, indent=2)
            faili.write('\n')
    data = json.loads(Mipangilio.read_text())
    if not isinstance(data, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if data.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for Jina in ('ssh_password', 'vnc_password'):
        if not isinstance(data.get(Jina), str):
            raise SystemExit('access.json: ' + Jina + '는 문자열이어야 합니다.')
    sheli_nywila = data['ssh_password'].encode('utf-8')
    if len(sheli_nywila) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = data['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. urefu_thamani 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def ARRAY_thamani(Jina, thamani):
        return 'static const unsigned char '+Jina+'[] = {'+','.join(str(수) for 수 in thamani)+'};\n'
    머리 = ARRAY_thamani('kifaa_Kitufe', Kitufe_thamani.read_bytes())
    머리 += ARRAY_thamani('sheli_nywila_muhtasari', hashlib.sha256(sheli_nywila).digest())
    머리 += ARRAY_thamani('화면암호', 화면열쇠)
    생성 = njia / 'Maelezo_mafupi.h'
    생성.write_text(머리)
    os.chmod(str(생성), 0o600)
    return data


if __name__ == '__main__':
    kichanganuzi_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    kichanganuzi_48ee4b1b.add_argument('Kitendo', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = kichanganuzi_48ee4b1b.parse_args()
    data = Andaa()
    if 인수.Kitendo == 'show':
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print('장치별 kwa_mbali_thamani muunganisho_e05f319b Mipangilio 준비됨. nywila_thamani thibitisha: python3 Zana/kwa_mbali_Mipangilio.py show')
