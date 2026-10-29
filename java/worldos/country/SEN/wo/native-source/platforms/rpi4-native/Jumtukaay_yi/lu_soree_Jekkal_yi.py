#!/usr/bin/env python3
"""장치별 kër_xëyma·jokkalóo_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

기준 = Path(__file__).resolve().parents[1]


def jël_matuwaay(기준=기준):
    Yoonu_jëmale = 기준 / 'build/remote'
    Yoonu_jëmale.mkdir(parents=True, exist_ok=True)
    Jekkal_yi = Yoonu_jëmale / 'access.json'
    kër_xëyma = Yoonu_jëmale / 'host-key.der'
    if not kër_xëyma.exists():
        with kër_xëyma.open('xb') as bara_denc:
            os.chmod(str(kër_xëyma), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=bara_denc)
    if not Jekkal_yi.exists():
        mbir = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Jekkal_yi.open('x') as bara_denc:
            os.chmod(str(Jekkal_yi), 0o600)
            json.dump(mbir, bara_denc, ensure_ascii=False, indent=2)
            bara_denc.write('\n')
    mbir = json.loads(Jekkal_yi.read_text())
    if not isinstance(mbir, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if mbir.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for tur_253d1510 in ('ssh_password', 'vnc_password'):
        if not isinstance(mbir.get(tur_253d1510), str):
            raise SystemExit('access.json: ' + tur_253d1510 + '는 문자열이어야 합니다.')
    Wëreef_pasu_dugg = mbir['ssh_password'].encode('utf-8')
    if len(Wëreef_pasu_dugg) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = mbir['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. diir_xëyma 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def TABLO_xëyma(tur_253d1510, xëyma):
        return 'static const unsigned char '+tur_253d1510+'[] = {'+','.join(str(수) for 수 in xëyma)+'};\n'
    머리 = TABLO_xëyma('toftal_kër', kër_xëyma.read_bytes())
    머리 += TABLO_xëyma('셸암호요약', hashlib.sha256(Wëreef_pasu_dugg).digest())
    머리 += TABLO_xëyma('화면암호', 화면열쇠)
    생성 = Yoonu_jëmale / 'profil.h'
    생성.write_text(머리)
    os.chmod(str(생성), 0o600)
    return mbir


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('jëf', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = 해석기.parse_args()
    mbir = jël_matuwaay()
    if 인수.jëf == 'show':
        print(json.dumps(mbir, ensure_ascii=False, indent=2))
    else:
        print('장치별 lu_soree_xëyma jokkalóo_e05f319b Jekkal_yi 준비됨. pasu_dugg_xëyma luñutu: python3 Jumtukaay_yi/lu_soree_Jekkal_yi.py show')
