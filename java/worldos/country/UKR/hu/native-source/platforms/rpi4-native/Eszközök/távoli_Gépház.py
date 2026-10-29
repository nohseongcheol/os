#!/usr/bin/env python3
"""장치별 Kulcs_ÉRTÉK·ismerős_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

teendő_gyök = Path(__file__).resolve().parents[1]


def Előkészítés(teendő_gyök=teendő_gyök):
    ÚTVONAL = teendő_gyök / 'build/remote'
    ÚTVONAL.mkdir(parents=True, exist_ok=True)
    Beállítások = ÚTVONAL / 'access.json'
    Kulcs_ÉRTÉK = ÚTVONAL / 'host-key.der'
    if not Kulcs_ÉRTÉK.exists():
        with Kulcs_ÉRTÉK.open('xb') as Fájl:
            os.chmod(str(Kulcs_ÉRTÉK), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Fájl)
    if not Beállítások.exists():
        adat = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Beállítások.open('x') as Fájl:
            os.chmod(str(Beállítások), 0o600)
            json.dump(adat, Fájl, ensure_ascii=False, indent=2)
            Fájl.write('\n')
    adat = json.loads(Beállítások.read_text())
    if not isinstance(adat, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if adat.get('user') != 'user':
        raise SystemExit('access.json: user는 aktuális_cikk "user"만 지원합니다.')
    for Név in ('ssh_password', 'vnc_password'):
        if not isinstance(adat.get(Név), str):
            raise SystemExit('access.json: ' + Név + '는 문자열이어야 합니다.')
    felület_jelszó = adat['ssh_password'].encode('utf-8')
    if len(felület_jelszó) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = adat['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. hossz_ÉRTÉK 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def TÖMB_ÉRTÉK(Név, ÉRTÉK):
        return 'static const unsigned char '+Név+'[] = {'+','.join(str(szám) for szám in ÉRTÉK)+'};\n'
    머리 = TÖMB_ÉRTÉK('mobil_Kulcs', Kulcs_ÉRTÉK.read_bytes())
    머리 += TÖMB_ÉRTÉK('felület_jelszó_összegzés', hashlib.sha256(felület_jelszó).digest())
    머리 += TÖMB_ÉRTÉK('화면암호', 화면열쇠)
    generálás = ÚTVONAL / 'Profil.h'
    generálás.write_text(머리)
    os.chmod(str(generálás), 0o600)
    return adat


if __name__ == '__main__':
    elemző_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    elemző_48ee4b1b.add_argument('Művelet', choices=['show', 'prepare'], nargs='?', default='prepare')
    Argumentumok = elemző_48ee4b1b.parse_args()
    adat = Előkészítés()
    if Argumentumok.Művelet == 'show':
        print(json.dumps(adat, ensure_ascii=False, indent=2))
    else:
        print('장치별 távoli_ÉRTÉK ismerős_e05f319b Beállítások 준비됨. jelszó_ÉRTÉK igazol: python3 Eszközök/távoli_Gépház.py show')
