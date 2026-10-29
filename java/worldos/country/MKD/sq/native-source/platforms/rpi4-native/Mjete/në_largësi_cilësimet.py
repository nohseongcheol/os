#!/usr/bin/env python3
"""장치별 tast_VALUE·lidhje_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

Project_rrënjë = Path(__file__).resolve().parents[1]


def Përgatit(Project_rrënjë=Project_rrënjë):
    POZICIONI = Project_rrënjë / 'build/remote'
    POZICIONI.mkdir(parents=True, exist_ok=True)
    Rregullime = POZICIONI / 'access.json'
    tast_VALUE = POZICIONI / 'host-key.der'
    if not tast_VALUE.exists():
        with tast_VALUE.open('xb') as Kartelë:
            os.chmod(str(tast_VALUE), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Kartelë)
    if not Rregullime.exists():
        të_dhëna = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Rregullime.open('x') as Kartelë:
            os.chmod(str(Rregullime), 0o600)
            json.dump(të_dhëna, Kartelë, ensure_ascii=False, indent=2)
            Kartelë.write('\n')
    të_dhëna = json.loads(Rregullime.read_text())
    if not isinstance(të_dhëna, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if të_dhëna.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for Emër in ('ssh_password', 'vnc_password'):
        if not isinstance(të_dhëna.get(Emër), str):
            raise SystemExit('access.json: ' + Emër + '는 문자열이어야 합니다.')
    pasues_fjalëkalim = të_dhëna['ssh_password'].encode('utf-8')
    if len(pasues_fjalëkalim) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = të_dhëna['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. gjatësi_VALUE 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def ARRAY_VALUE(Emër, VALUE):
        return 'static const unsigned char '+Emër+'[] = {'+','.join(str(수) for 수 in VALUE)+'};\n'
    머리 = ARRAY_VALUE('pajisje_tast', tast_VALUE.read_bytes())
    머리 += ARRAY_VALUE('pasues_fjalëkalim_përmbledhje', hashlib.sha256(pasues_fjalëkalim).digest())
    머리 += ARRAY_VALUE('화면암호', 화면열쇠)
    gjeneroj = POZICIONI / 'profil.h'
    gjeneroj.write_text(머리)
    os.chmod(str(gjeneroj), 0o600)
    return të_dhëna


if __name__ == '__main__':
    analizues_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizues_48ee4b1b.add_argument('Veprim', choices=['show', 'prepare'], nargs='?', default='prepare')
    Argumente = analizues_48ee4b1b.parse_args()
    të_dhëna = Përgatit()
    if Argumente.Veprim == 'show':
        print(json.dumps(të_dhëna, ensure_ascii=False, indent=2))
    else:
        print('장치별 në_largësi_VALUE lidhje_e05f319b Rregullime 준비됨. fjalëkalim_VALUE verifikoj: python3 Mjete/në_largësi_cilësimet.py show')
