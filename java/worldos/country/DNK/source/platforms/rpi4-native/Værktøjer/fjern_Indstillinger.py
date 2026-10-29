#!/usr/bin/env python3
"""장치별 tast_VÆRDI·forbindelse_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

To_do_rod = Path(__file__).resolve().parents[1]


def Tilrettelæg(To_do_rod=To_do_rod):
    Sti = To_do_rod / 'build/remote'
    Sti.mkdir(parents=True, exist_ok=True)
    Indstillinger = Sti / 'access.json'
    tast_VÆRDI = Sti / 'host-key.der'
    if not tast_VÆRDI.exists():
        with tast_VÆRDI.open('xb') as Fil:
            os.chmod(str(tast_VÆRDI), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Fil)
    if not Indstillinger.exists():
        data = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Indstillinger.open('x') as Fil:
            os.chmod(str(Indstillinger), 0o600)
            json.dump(data, Fil, ensure_ascii=False, indent=2)
            Fil.write('\n')
    data = json.loads(Indstillinger.read_text())
    if not isinstance(data, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if data.get('user') != 'user':
        raise SystemExit('access.json: user는 aktuel_vare "user"만 지원합니다.')
    for Navn in ('ssh_password', 'vnc_password'):
        if not isinstance(data.get(Navn), str):
            raise SystemExit('access.json: ' + Navn + '는 문자열이어야 합니다.')
    Shell_adgangskode = data['ssh_password'].encode('utf-8')
    if len(Shell_adgangskode) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        skærmbillede_adgangskode = data['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. varighed_VÆRDI 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    skærmbillede_tast = skærmbillede_adgangskode[:8].ljust(8, b'\0')
    def MATRIX_VÆRDI(Navn, VÆRDI):
        return 'static const unsigned char '+Navn+'[] = {'+','.join(str(tal) for tal in VÆRDI)+'};\n'
    머리 = MATRIX_VÆRDI('enhed_tast', tast_VÆRDI.read_bytes())
    머리 += MATRIX_VÆRDI('Shell_adgangskode_resume', hashlib.sha256(Shell_adgangskode).digest())
    머리 += MATRIX_VÆRDI('skærmbillede_adgangskode', skærmbillede_tast)
    generere = Sti / 'Profil.h'
    generere.write_text(머리)
    os.chmod(str(generere), 0o600)
    return data


if __name__ == '__main__':
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('Handling', choices=['show', 'prepare'], nargs='?', default='prepare')
    Argumenter = parser_48ee4b1b.parse_args()
    data = Tilrettelæg()
    if Argumenter.Handling == 'show':
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print('장치별 fjern_VÆRDI forbindelse_e05f319b Indstillinger 준비됨. adgangskode_VÆRDI bekræfte: python3 Værktøjer/fjern_Indstillinger.py show')
