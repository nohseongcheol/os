#!/usr/bin/env python3
"""장치별 Iuchair_VALUE·ceangal_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

tilg_freumh = Path(__file__).resolve().parents[1]


def Ullaich(tilg_freumh=tilg_freumh):
    Slighe = tilg_freumh / 'build/remote'
    Slighe.mkdir(parents=True, exist_ok=True)
    roghainnean = Slighe / 'access.json'
    Iuchair_VALUE = Slighe / 'host-key.der'
    if not Iuchair_VALUE.exists():
        with Iuchair_VALUE.open('xb') as faidhle:
            os.chmod(str(Iuchair_VALUE), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=faidhle)
    if not roghainnean.exists():
        dàta = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with roghainnean.open('x') as faidhle:
            os.chmod(str(roghainnean), 0o600)
            json.dump(dàta, faidhle, ensure_ascii=False, indent=2)
            faidhle.write('\n')
    dàta = json.loads(roghainnean.read_text())
    if not isinstance(dàta, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if dàta.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for Ainm in ('ssh_password', 'vnc_password'):
        if not isinstance(dàta.get(Ainm), str):
            raise SystemExit('access.json: ' + Ainm + '는 문자열이어야 합니다.')
    slige_facal_faire = dàta['ssh_password'].encode('utf-8')
    if len(slige_facal_faire) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = dàta['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. faid_VALUE 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def ARRAY_VALUE(Ainm, VALUE):
        return 'static const unsigned char '+Ainm+'[] = {'+','.join(str(수) for 수 in VALUE)+'};\n'
    머리 = ARRAY_VALUE('uidheam_Iuchair', Iuchair_VALUE.read_bytes())
    머리 += ARRAY_VALUE('셸암호요약', hashlib.sha256(slige_facal_faire).digest())
    머리 += ARRAY_VALUE('화면암호', 화면열쇠)
    gin = Slighe / 'Pròifil.h'
    gin.write_text(머리)
    os.chmod(str(gin), 0o600)
    return dàta


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('Gnìomh', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = 해석기.parse_args()
    dàta = Ullaich()
    if 인수.Gnìomh == 'show':
        print(json.dumps(dàta, ensure_ascii=False, indent=2))
    else:
        print('장치별 cian_VALUE ceangal_e05f319b roghainnean 준비됨. facal_faire_VALUE dearbh: python3 innealan/cian_roghainnean.py show')
