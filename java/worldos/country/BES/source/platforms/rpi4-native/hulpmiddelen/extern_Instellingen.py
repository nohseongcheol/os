#!/usr/bin/env python3
"""장치별 toets_WAARDE·verbinding_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

Taken_wortel = Path(__file__).resolve().parents[1]


def Bereid_voor(Taken_wortel=Taken_wortel):
    pad = Taken_wortel / 'build/remote'
    pad.mkdir(parents=True, exist_ok=True)
    Instellingen = pad / 'access.json'
    toets_WAARDE = pad / 'host-key.der'
    if not toets_WAARDE.exists():
        with toets_WAARDE.open('xb') as bestand:
            os.chmod(str(toets_WAARDE), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=bestand)
    if not Instellingen.exists():
        gegevens = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Instellingen.open('x') as bestand:
            os.chmod(str(Instellingen), 0o600)
            json.dump(gegevens, bestand, ensure_ascii=False, indent=2)
            bestand.write('\n')
    gegevens = json.loads(Instellingen.read_text())
    if not isinstance(gegevens, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if gegevens.get('user') != 'user':
        raise SystemExit('access.json: user는 actueel_item "user"만 지원합니다.')
    for Naam in ('ssh_password', 'vnc_password'):
        if not isinstance(gegevens.get(Naam), str):
            raise SystemExit('access.json: ' + Naam + '는 문자열이어야 합니다.')
    Shell_wachtwoord = gegevens['ssh_password'].encode('utf-8')
    if len(Shell_wachtwoord) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        scherm_wachtwoord = gegevens['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. tijdsduur_WAARDE 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    scherm_toets = scherm_wachtwoord[:8].ljust(8, b'\0')
    def MATRIX_WAARDE(Naam, WAARDE):
        return 'static const unsigned char '+Naam+'[] = {'+','.join(str(nummer) for nummer in WAARDE)+'};\n'
    kop_WAARDE = MATRIX_WAARDE('mobiel_toets', toets_WAARDE.read_bytes())
    kop_WAARDE += MATRIX_WAARDE('Shell_wachtwoord_samenvatting', hashlib.sha256(Shell_wachtwoord).digest())
    kop_WAARDE += MATRIX_WAARDE('scherm_wachtwoord', scherm_toets)
    genereren = pad / 'Profiel.h'
    genereren.write_text(kop_WAARDE)
    os.chmod(str(genereren), 0o600)
    return gegevens


if __name__ == '__main__':
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('Actie', choices=['show', 'prepare'], nargs='?', default='prepare')
    argumenten = parser_48ee4b1b.parse_args()
    gegevens = Bereid_voor()
    if argumenten.Actie == 'show':
        print(json.dumps(gegevens, ensure_ascii=False, indent=2))
    else:
        print('장치별 extern_WAARDE_28edcfa1 verbinding_e05f319b Instellingen 준비됨. wachtwoord_WAARDE bevestigen: python3 hulpmiddelen/extern_Instellingen.py show')
