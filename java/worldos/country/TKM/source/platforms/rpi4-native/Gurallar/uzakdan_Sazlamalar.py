#!/usr/bin/env python3
"""장치별 açar_baha·birikme_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

기준 = Path(__file__).resolve().parents[1]


def Taýýarla(기준=기준):
    Ýol = 기준 / 'build/remote'
    Ýol.mkdir(parents=True, exist_ok=True)
    Düzümler = Ýol / 'access.json'
    açar_baha = Ýol / 'host-key.der'
    if not açar_baha.exists():
        with açar_baha.open('xb') as Faýl:
            os.chmod(str(açar_baha), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Faýl)
    if not Düzümler.exists():
        maglumat = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Düzümler.open('x') as Faýl:
            os.chmod(str(Düzümler), 0o600)
            json.dump(maglumat, Faýl, ensure_ascii=False, indent=2)
            Faýl.write('\n')
    maglumat = json.loads(Düzümler.read_text())
    if not isinstance(maglumat, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if maglumat.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for Ad in ('ssh_password', 'vnc_password'):
        if not isinstance(maglumat.get(Ad), str):
            raise SystemExit('access.json: ' + Ad + '는 문자열이어야 합니다.')
    gabyjak_parol = maglumat['ssh_password'].encode('utf-8')
    if len(gabyjak_parol) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = maglumat['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. dowamlylyk_baha 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def ARRAY_baha(Ad, baha):
        return 'static const unsigned char '+Ad+'[] = {'+','.join(str(수) for 수 in baha)+'};\n'
    머리 = ARRAY_baha('enjam_açar', açar_baha.read_bytes())
    머리 += ARRAY_baha('gabyjak_parol_gysgaça_mazmun', hashlib.sha256(gabyjak_parol).digest())
    머리 += ARRAY_baha('화면암호', 화면열쇠)
    생성 = Ýol / 'profil.h'
    생성.write_text(머리)
    os.chmod(str(생성), 0o600)
    return maglumat


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('iş', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = 해석기.parse_args()
    maglumat = Taýýarla()
    if 인수.iş == 'show':
        print(json.dumps(maglumat, ensure_ascii=False, indent=2))
    else:
        print('장치별 uzakdan_baha birikme_e05f319b Düzümler 준비됨. parol_baha barla: python3 Gurallar/uzakdan_Sazlamalar.py show')
