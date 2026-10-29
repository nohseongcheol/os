#!/usr/bin/env python3
"""장치별 ključ_VALUE·veza_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

projicirati_koijen = Path(__file__).resolve().parents[1]


def Pripremiti(projicirati_koijen=projicirati_koijen):
    Putanja = projicirati_koijen / 'build/remote'
    Putanja.mkdir(parents=True, exist_ok=True)
    Postavke = Putanja / 'access.json'
    ključ_VALUE = Putanja / 'host-key.der'
    if not ključ_VALUE.exists():
        with ključ_VALUE.open('xb') as Fajl:
            os.chmod(str(ključ_VALUE), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Fajl)
    if not Postavke.exists():
        podaci = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Postavke.open('x') as Fajl:
            os.chmod(str(Postavke), 0o600)
            json.dump(podaci, Fajl, ensure_ascii=False, indent=2)
            Fajl.write('\n')
    podaci = json.loads(Postavke.read_text())
    if not isinstance(podaci, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if podaci.get('user') != 'user':
        raise SystemExit('access.json: user는 trenutno_stavka "user"만 지원합니다.')
    for Naziv in ('ssh_password', 'vnc_password'):
        if not isinstance(podaci.get(Naziv), str):
            raise SystemExit('access.json: ' + Naziv + '는 문자열이어야 합니다.')
    ljuska_lozinka = podaci['ssh_password'].encode('utf-8')
    if len(ljuska_lozinka) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = podaci['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. dužina_VALUE 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def niz_VALUE(Naziv, VALUE):
        return 'static const unsigned char '+Naziv+'[] = {'+','.join(str(수) for 수 in VALUE)+'};\n'
    머리 = niz_VALUE('uređaj_ključ', ključ_VALUE.read_bytes())
    머리 += niz_VALUE('ljuska_lozinka_rezime', hashlib.sha256(ljuska_lozinka).digest())
    머리 += niz_VALUE('화면암호', 화면열쇠)
    generirati = Putanja / 'Profil.h'
    generirati.write_text(머리)
    os.chmod(str(generirati), 0o600)
    return podaci


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('radnja', choices=['show', 'prepare'], nargs='?', default='prepare')
    Argumenti = 해석기.parse_args()
    podaci = Pripremiti()
    if Argumenti.radnja == 'show':
        print(json.dumps(podaci, ensure_ascii=False, indent=2))
    else:
        print('장치별 udaljeno_VALUE veza_e05f319b Postavke 준비됨. lozinka_VALUE potvrditi: python3 Alati/udaljeno_Postavke.py show')
