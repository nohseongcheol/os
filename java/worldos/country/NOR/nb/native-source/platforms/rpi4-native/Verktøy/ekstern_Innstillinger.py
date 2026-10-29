#!/usr/bin/env python3
"""장치별 tast_VERDI·kontakt_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

speile_rot = Path(__file__).resolve().parents[1]


def Forbered(speile_rot=speile_rot):
    Sti = speile_rot / 'build/remote'
    Sti.mkdir(parents=True, exist_ok=True)
    Innstillinger = Sti / 'access.json'
    tast_VERDI = Sti / 'host-key.der'
    if not tast_VERDI.exists():
        with tast_VERDI.open('xb') as Fil:
            os.chmod(str(tast_VERDI), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Fil)
    if not Innstillinger.exists():
        data = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Innstillinger.open('x') as Fil:
            os.chmod(str(Innstillinger), 0o600)
            json.dump(data, Fil, ensure_ascii=False, indent=2)
            Fil.write('\n')
    data = json.loads(Innstillinger.read_text())
    if not isinstance(data, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if data.get('user') != 'user':
        raise SystemExit('access.json: user는 betalt_vare "user"만 지원합니다.')
    for Navn in ('ssh_password', 'vnc_password'):
        if not isinstance(data.get(Navn), str):
            raise SystemExit('access.json: ' + Navn + '는 문자열이어야 합니다.')
    Shell_passord = data['ssh_password'].encode('utf-8')
    if len(Shell_passord) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        skjermbilde_passord = data['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. lengde_VERDI 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    skjermbilde_tast = skjermbilde_passord[:8].ljust(8, b'\0')
    def MATRISE_VERDI(Navn, VERDI):
        return 'static const unsigned char '+Navn+'[] = {'+','.join(str(nummer) for nummer in VERDI)+'};\n'
    머리 = MATRISE_VERDI('enhet_tast', tast_VERDI.read_bytes())
    머리 += MATRISE_VERDI('Shell_passord_sammendrag', hashlib.sha256(Shell_passord).digest())
    머리 += MATRISE_VERDI('skjermbilde_passord', skjermbilde_tast)
    generere = Sti / 'Profil.h'
    generere.write_text(머리)
    os.chmod(str(generere), 0o600)
    return data


if __name__ == '__main__':
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('Handling', choices=['show', 'prepare'], nargs='?', default='prepare')
    Argumenter = parser_48ee4b1b.parse_args()
    data = Forbered()
    if Argumenter.Handling == 'show':
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print('장치별 ekstern_VERDI_28edcfa1 kontakt_e05f319b Innstillinger 준비됨. passord_VERDI bekrefte: python3 Verktøy/ekstern_Innstillinger.py show')
