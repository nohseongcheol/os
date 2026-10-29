#!/usr/bin/env python3
"""장치별 eochair_VALUE·nasc_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

teilgean_fréamh = Path(__file__).resolve().parents[1]


def Ullmhaigh(teilgean_fréamh=teilgean_fréamh):
    CONAIR = teilgean_fréamh / 'build/remote'
    CONAIR.mkdir(parents=True, exist_ok=True)
    Socruithe = CONAIR / 'access.json'
    eochair_VALUE = CONAIR / 'host-key.der'
    if not eochair_VALUE.exists():
        with eochair_VALUE.open('xb') as Comhad:
            os.chmod(str(eochair_VALUE), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Comhad)
    if not Socruithe.exists():
        sonraí = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Socruithe.open('x') as Comhad:
            os.chmod(str(Socruithe), 0o600)
            json.dump(sonraí, Comhad, ensure_ascii=False, indent=2)
            Comhad.write('\n')
    sonraí = json.loads(Socruithe.read_text())
    if not isinstance(sonraí, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if sonraí.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for Ainm in ('ssh_password', 'vnc_password'):
        if not isinstance(sonraí.get(Ainm), str):
            raise SystemExit('access.json: ' + Ainm + '는 문자열이어야 합니다.')
    blaosc_pasfhocal = sonraí['ssh_password'].encode('utf-8')
    if len(blaosc_pasfhocal) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = sonraí['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. fad_VALUE 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def ARRAY_VALUE(Ainm, VALUE):
        return 'static const unsigned char '+Ainm+'[] = {'+','.join(str(수) for 수 in VALUE)+'};\n'
    머리 = ARRAY_VALUE('gléas_eochair', eochair_VALUE.read_bytes())
    머리 += ARRAY_VALUE('blaosc_pasfhocal_achoimre', hashlib.sha256(blaosc_pasfhocal).digest())
    머리 += ARRAY_VALUE('화면암호', 화면열쇠)
    giniúint = CONAIR / 'Próifíl.h'
    giniúint.write_text(머리)
    os.chmod(str(giniúint), 0o600)
    return sonraí


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('Gníomh', choices=['show', 'prepare'], nargs='?', default='prepare')
    Argóintí = 해석기.parse_args()
    sonraí = Ullmhaigh()
    if Argóintí.Gníomh == 'show':
        print(json.dumps(sonraí, ensure_ascii=False, indent=2))
    else:
        print('장치별 cianda_VALUE nasc_e05f319b Socruithe 준비됨. pasfhocal_VALUE fíoraigh: python3 Uirlisí/cianda_Socruithe.py show')
