#!/usr/bin/env python3
"""장치별 gako_balio·konexio_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

Project_erro = Path(__file__).resolve().parents[1]


def 준비(Project_erro=Project_erro):
    Bide_izena = Project_erro / 'build/remote'
    Bide_izena.mkdir(parents=True, exist_ok=True)
    Ezarpenak = Bide_izena / 'access.json'
    gako_balio = Bide_izena / 'host-key.der'
    if not gako_balio.exists():
        with gako_balio.open('xb') as Fitxategia:
            os.chmod(str(gako_balio), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Fitxategia)
    if not Ezarpenak.exists():
        datuak = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Ezarpenak.open('x') as Fitxategia:
            os.chmod(str(Ezarpenak), 0o600)
            json.dump(datuak, Fitxategia, ensure_ascii=False, indent=2)
            Fitxategia.write('\n')
    datuak = json.loads(Ezarpenak.read_text())
    if not isinstance(datuak, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if datuak.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for Izena in ('ssh_password', 'vnc_password'):
        if not isinstance(datuak.get(Izena), str):
            raise SystemExit('access.json: ' + Izena + '는 문자열이어야 합니다.')
    shell_pasahitz = datuak['ssh_password'].encode('utf-8')
    if len(shell_pasahitz) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = datuak['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. luzera_balio 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def matrize_balio(Izena, balio):
        return 'static const unsigned char '+Izena+'[] = {'+','.join(str(수) for 수 in balio)+'};\n'
    머리 = matrize_balio('gailu_gako', gako_balio.read_bytes())
    머리 += matrize_balio('셸암호요약', hashlib.sha256(shell_pasahitz).digest())
    머리 += matrize_balio('화면암호', 화면열쇠)
    sortu = Bide_izena / 'profil.h'
    sortu.write_text(머리)
    os.chmod(str(sortu), 0o600)
    return datuak


if __name__ == '__main__':
    analizatzaile_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizatzaile_48ee4b1b.add_argument('Ekintza', choices=['show', 'prepare'], nargs='?', default='prepare')
    Argumentuak = analizatzaile_48ee4b1b.parse_args()
    datuak = 준비()
    if Argumentuak.Ekintza == 'show':
        print(json.dumps(datuak, ensure_ascii=False, indent=2))
    else:
        print('장치별 urruneko_balio konexio_e05f319b Ezarpenak 준비됨. pasahitz_balio egiaztatu: python3 Tresnak/urruneko_Ezarpenak.py show')
