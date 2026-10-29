#!/usr/bin/env python3
"""장치별 Raktas_VALUE·ryšys_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

Project_šaknis = Path(__file__).resolve().parents[1]


def Parengti(Project_šaknis=Project_šaknis):
    KELIAS = Project_šaknis / 'build/remote'
    KELIAS.mkdir(parents=True, exist_ok=True)
    Nustatymai = KELIAS / 'access.json'
    Raktas_VALUE = KELIAS / 'host-key.der'
    if not Raktas_VALUE.exists():
        with Raktas_VALUE.open('xb') as Failas:
            os.chmod(str(Raktas_VALUE), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Failas)
    if not Nustatymai.exists():
        duomenys = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Nustatymai.open('x') as Failas:
            os.chmod(str(Nustatymai), 0o600)
            json.dump(duomenys, Failas, ensure_ascii=False, indent=2)
            Failas.write('\n')
    duomenys = json.loads(Nustatymai.read_text())
    if not isinstance(duomenys, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if duomenys.get('user') != 'user':
        raise SystemExit('access.json: user는 dabartinis_prekė "user"만 지원합니다.')
    for Pavadinimas_2 in ('ssh_password', 'vnc_password'):
        if not isinstance(duomenys.get(Pavadinimas_2), str):
            raise SystemExit('access.json: ' + Pavadinimas_2 + '는 문자열이어야 합니다.')
    apvalkalas_slaptažodis = duomenys['ssh_password'].encode('utf-8')
    if len(apvalkalas_slaptažodis) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = duomenys['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. 길이 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def ARRAY_VALUE(Pavadinimas_2, VALUE):
        return 'static const unsigned char '+Pavadinimas_2+'[] = {'+','.join(str(numeris) for numeris in VALUE)+'};\n'
    머리 = ARRAY_VALUE('įrenginys_Raktas', Raktas_VALUE.read_bytes())
    머리 += ARRAY_VALUE('apvalkalas_slaptažodis_suvestinė', hashlib.sha256(apvalkalas_slaptažodis).digest())
    머리 += ARRAY_VALUE('화면암호', 화면열쇠)
    generuoti = KELIAS / 'Profilis.h'
    generuoti.write_text(머리)
    os.chmod(str(generuoti), 0o600)
    return duomenys


if __name__ == '__main__':
    analizatorius_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizatorius_48ee4b1b.add_argument('Veiksmas', choices=['show', 'prepare'], nargs='?', default='prepare')
    Argumentai = analizatorius_48ee4b1b.parse_args()
    duomenys = Parengti()
    if Argumentai.Veiksmas == 'show':
        print(json.dumps(duomenys, ensure_ascii=False, indent=2))
    else:
        print('장치별 nuotolinis_VALUE ryšys_e05f319b Nustatymai 준비됨. slaptažodis_VALUE patvirtinti: python3 Įrankiai/nuotolinis_Parametrai.py show')
