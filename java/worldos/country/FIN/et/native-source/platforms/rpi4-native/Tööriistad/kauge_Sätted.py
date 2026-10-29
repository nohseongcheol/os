#!/usr/bin/env python3
"""장치별 Võti_VALUE·ühendus_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

Project_juur = Path(__file__).resolve().parents[1]


def Ettevalmistamine(Project_juur=Project_juur):
    RADA = Project_juur / 'build/remote'
    RADA.mkdir(parents=True, exist_ok=True)
    Seaded = RADA / 'access.json'
    Võti_VALUE = RADA / 'host-key.der'
    if not Võti_VALUE.exists():
        with Võti_VALUE.open('xb') as Fail:
            os.chmod(str(Võti_VALUE), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Fail)
    if not Seaded.exists():
        andmed = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Seaded.open('x') as Fail:
            os.chmod(str(Seaded), 0o600)
            json.dump(andmed, Fail, ensure_ascii=False, indent=2)
            Fail.write('\n')
    andmed = json.loads(Seaded.read_text())
    if not isinstance(andmed, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if andmed.get('user') != 'user':
        raise SystemExit('access.json: user는 tähtaja_piires_kaup "user"만 지원합니다.')
    for Nimi_2 in ('ssh_password', 'vnc_password'):
        if not isinstance(andmed.get(Nimi_2), str):
            raise SystemExit('access.json: ' + Nimi_2 + '는 문자열이어야 합니다.')
    kest_parool = andmed['ssh_password'].encode('utf-8')
    if len(kest_parool) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = andmed['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. 길이 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def ARRAY_VALUE(Nimi_2, VALUE):
        return 'static const unsigned char '+Nimi_2+'[] = {'+','.join(str(number) for number in VALUE)+'};\n'
    머리 = ARRAY_VALUE('seade_Võti', Võti_VALUE.read_bytes())
    머리 += ARRAY_VALUE('kest_parool_kokkuvõte', hashlib.sha256(kest_parool).digest())
    머리 += ARRAY_VALUE('화면암호', 화면열쇠)
    genereerima = RADA / 'Profiil.h'
    genereerima.write_text(머리)
    os.chmod(str(genereerima), 0o600)
    return andmed


if __name__ == '__main__':
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('Nimi', choices=['show', 'prepare'], nargs='?', default='prepare')
    Argumendid = parser_48ee4b1b.parse_args()
    andmed = Ettevalmistamine()
    if Argumendid.Nimi == 'show':
        print(json.dumps(andmed, ensure_ascii=False, indent=2))
    else:
        print('장치별 kauge_VALUE ühendus_e05f319b Seaded 준비됨. parool_VALUE kinnitama: python3 Tööriistad/kauge_Sätted.py show')
