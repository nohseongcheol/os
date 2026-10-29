#!/usr/bin/env python3
"""장치별 tast_VALUE·kontakt_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

spegle_rot = Path(__file__).resolve().parents[1]


def Klargjer(spegle_rot=spegle_rot):
    STIGE = spegle_rot / 'build/remote'
    STIGE.mkdir(parents=True, exist_ok=True)
    Innstillingar = STIGE / 'access.json'
    tast_VALUE = STIGE / 'host-key.der'
    if not tast_VALUE.exists():
        with tast_VALUE.open('xb') as Fil:
            os.chmod(str(tast_VALUE), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Fil)
    if not Innstillingar.exists():
        data = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Innstillingar.open('x') as Fil:
            os.chmod(str(Innstillingar), 0o600)
            json.dump(data, Fil, ensure_ascii=False, indent=2)
            Fil.write('\n')
    data = json.loads(Innstillingar.read_text())
    if not isinstance(data, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if data.get('user') != 'user':
        raise SystemExit('access.json: user는 betalt_vare "user"만 지원합니다.')
    for Namn in ('ssh_password', 'vnc_password'):
        if not isinstance(data.get(Namn), str):
            raise SystemExit('access.json: ' + Namn + '는 문자열이어야 합니다.')
    grensesnitt_passord = data['ssh_password'].encode('utf-8')
    if len(grensesnitt_passord) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = data['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. lengd_VALUE 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def ARRAY_VALUE(Namn, VALUE):
        return 'static const unsigned char '+Namn+'[] = {'+','.join(str(수) for 수 in VALUE)+'};\n'
    머리 = ARRAY_VALUE('mobil_tast', tast_VALUE.read_bytes())
    머리 += ARRAY_VALUE('grensesnitt_passord_samandrag', hashlib.sha256(grensesnitt_passord).digest())
    머리 += ARRAY_VALUE('화면암호', 화면열쇠)
    generere = STIGE / 'Profil.h'
    generere.write_text(머리)
    os.chmod(str(generere), 0o600)
    return data


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('Handling', choices=['show', 'prepare'], nargs='?', default='prepare')
    Argument = 해석기.parse_args()
    data = Klargjer()
    if Argument.Handling == 'show':
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print('장치별 fjern_VALUE kontakt_e05f319b Innstillingar 준비됨. passord_VALUE stadfeste: python3 Verktøy/fjern_Innstillingar.py show')
