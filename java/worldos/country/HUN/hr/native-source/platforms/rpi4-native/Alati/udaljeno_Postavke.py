#!/usr/bin/env python3
"""장치별 Ključ_VALUE·veza_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

akcija_korijen = Path(__file__).resolve().parents[1]


def Pripremi(akcija_korijen=akcija_korijen):
    PUTANJA = akcija_korijen / 'build/remote'
    PUTANJA.mkdir(parents=True, exist_ok=True)
    Postavke = PUTANJA / 'access.json'
    Ključ_VALUE = PUTANJA / 'host-key.der'
    if not Ključ_VALUE.exists():
        with Ključ_VALUE.open('xb') as Datoteka:
            os.chmod(str(Ključ_VALUE), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Datoteka)
    if not Postavke.exists():
        podaci = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Postavke.open('x') as Datoteka:
            os.chmod(str(Postavke), 0o600)
            json.dump(podaci, Datoteka, ensure_ascii=False, indent=2)
            Datoteka.write('\n')
    podaci = json.loads(Postavke.read_text())
    if not isinstance(podaci, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if podaci.get('user') != 'user':
        raise SystemExit('access.json: user는 redovno_artikl "user"만 지원합니다.')
    for Ime in ('ssh_password', 'vnc_password'):
        if not isinstance(podaci.get(Ime), str):
            raise SystemExit('access.json: ' + Ime + '는 문자열이어야 합니다.')
    ljuska_lozinka = podaci['ssh_password'].encode('utf-8')
    if len(ljuska_lozinka) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = podaci['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. 길이 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def ARRAY_VALUE(Ime, VALUE):
        return 'static const unsigned char '+Ime+'[] = {'+','.join(str(수) for 수 in VALUE)+'};\n'
    머리 = ARRAY_VALUE('uređaj_Ključ', Ključ_VALUE.read_bytes())
    머리 += ARRAY_VALUE('ljuska_lozinka_sažetak', hashlib.sha256(ljuska_lozinka).digest())
    머리 += ARRAY_VALUE('화면암호', 화면열쇠)
    generirati = PUTANJA / 'Profil.h'
    generirati.write_text(머리)
    os.chmod(str(generirati), 0o600)
    return podaci


if __name__ == '__main__':
    analizator_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizator_48ee4b1b.add_argument('Aktivnost', choices=['show', 'prepare'], nargs='?', default='prepare')
    Argumenti = analizator_48ee4b1b.parse_args()
    podaci = Pripremi()
    if Argumenti.Aktivnost == 'show':
        print(json.dumps(podaci, ensure_ascii=False, indent=2))
    else:
        print('장치별 udaljeno_VALUE veza_e05f319b Postavke 준비됨. lozinka_VALUE provjeriti: python3 Alati/udaljeno_Postavke.py show')
