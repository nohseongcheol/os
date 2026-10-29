#!/usr/bin/env python3
"""장치별 Nyckel_värde·kontakt_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

åtgärd_rot = Path(__file__).resolve().parents[1]


def Förbereda(åtgärd_rot=åtgärd_rot):
    sökväg_2 = åtgärd_rot / 'build/remote'
    sökväg_2.mkdir(parents=True, exist_ok=True)
    Inställningar = sökväg_2 / 'access.json'
    Nyckel_värde = sökväg_2 / 'host-key.der'
    if not Nyckel_värde.exists():
        with Nyckel_värde.open('xb') as filnamn:
            os.chmod(str(Nyckel_värde), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=filnamn)
    if not Inställningar.exists():
        data = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Inställningar.open('x') as filnamn:
            os.chmod(str(Inställningar), 0o600)
            json.dump(data, filnamn, ensure_ascii=False, indent=2)
            filnamn.write('\n')
    data = json.loads(Inställningar.read_text())
    if not isinstance(data, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if data.get('user') != 'user':
        raise SystemExit('access.json: user는 aktuellt_objekt "user"만 지원합니다.')
    for Namn in ('ssh_password', 'vnc_password'):
        if not isinstance(data.get(Namn), str):
            raise SystemExit('access.json: ' + Namn + '는 문자열이어야 합니다.')
    Shell_lösenord = data['ssh_password'].encode('utf-8')
    if len(Shell_lösenord) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        skärmbild_lösenord = data['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. längd_värde 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    skärmbild_Nyckel = skärmbild_lösenord[:8].ljust(8, b'\0')
    def MATRIS_värde(Namn, värde):
        return 'static const unsigned char '+Namn+'[] = {'+','.join(str(nummer) for nummer in värde)+'};\n'
    머리 = MATRIS_värde('enhet_Nyckel', Nyckel_värde.read_bytes())
    머리 += MATRIS_värde('Shell_lösenord_sammanfattning', hashlib.sha256(Shell_lösenord).digest())
    머리 += MATRIS_värde('skärmbild_lösenord', skärmbild_Nyckel)
    generera = sökväg_2 / 'Profil.h'
    generera.write_text(머리)
    os.chmod(str(generera), 0o600)
    return data


if __name__ == '__main__':
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('Åtgärd', choices=['show', 'prepare'], nargs='?', default='prepare')
    argument = parser_48ee4b1b.parse_args()
    data = Förbereda()
    if argument.Åtgärd == 'show':
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print('장치별 fjärr_värde kontakt_e05f319b Inställningar 준비됨. lösenord_värde verifiera: python3 verktyg/fjärr_Inställningar.py show')
