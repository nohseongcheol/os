#!/usr/bin/env python3
"""장치별 Atslēga_VALUE·paziņa_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

Project_sakne = Path(__file__).resolve().parents[1]


def Sagatavot(Project_sakne=Project_sakne):
    CEĻŠ = Project_sakne / 'build/remote'
    CEĻŠ.mkdir(parents=True, exist_ok=True)
    Uzstādījumi = CEĻŠ / 'access.json'
    Atslēga_VALUE = CEĻŠ / 'host-key.der'
    if not Atslēga_VALUE.exists():
        with Atslēga_VALUE.open('xb') as Fails:
            os.chmod(str(Atslēga_VALUE), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Fails)
    if not Uzstādījumi.exists():
        dati = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Uzstādījumi.open('x') as Fails:
            os.chmod(str(Uzstādījumi), 0o600)
            json.dump(dati, Fails, ensure_ascii=False, indent=2)
            Fails.write('\n')
    dati = json.loads(Uzstādījumi.read_text())
    if not isinstance(dati, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if dati.get('user') != 'user':
        raise SystemExit('access.json: user는 pašreizējais_krājums "user"만 지원합니다.')
    for Nosaukums in ('ssh_password', 'vnc_password'):
        if not isinstance(dati.get(Nosaukums), str):
            raise SystemExit('access.json: ' + Nosaukums + '는 문자열이어야 합니다.')
    čaula_parole = dati['ssh_password'].encode('utf-8')
    if len(čaula_parole) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = dati['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. 길이 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def ARRAY_VALUE(Nosaukums, VALUE):
        return 'static const unsigned char '+Nosaukums+'[] = {'+','.join(str(numurs) for numurs in VALUE)+'};\n'
    머리 = ARRAY_VALUE('ierīce_Atslēga', Atslēga_VALUE.read_bytes())
    머리 += ARRAY_VALUE('čaula_parole_kopsavilkums', hashlib.sha256(čaula_parole).digest())
    머리 += ARRAY_VALUE('화면암호', 화면열쇠)
    ģenerēt = CEĻŠ / 'Profils.h'
    ģenerēt.write_text(머리)
    os.chmod(str(ģenerēt), 0o600)
    return dati


if __name__ == '__main__':
    parsētājs_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parsētājs_48ee4b1b.add_argument('Darbība', choices=['show', 'prepare'], nargs='?', default='prepare')
    Parametri = parsētājs_48ee4b1b.parse_args()
    dati = Sagatavot()
    if Parametri.Darbība == 'show':
        print(json.dumps(dati, ensure_ascii=False, indent=2))
    else:
        print('장치별 attāls_VALUE paziņa_e05f319b Uzstādījumi 준비됨. parole_VALUE verificēt: python3 Rīki/attāls_Iestatījumi.py show')
