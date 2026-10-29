#!/usr/bin/env python3
"""장치별 Clau_VALOR·connexió_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

Project_rel = Path(__file__).resolve().parents[1]


def Prepara(Project_rel=Project_rel):
    Camí = Project_rel / 'build/remote'
    Camí.mkdir(parents=True, exist_ok=True)
    Ajusts = Camí / 'access.json'
    Clau_VALOR = Camí / 'host-key.der'
    if not Clau_VALOR.exists():
        with Clau_VALOR.open('xb') as Fitxer:
            os.chmod(str(Clau_VALOR), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Fitxer)
    if not Ajusts.exists():
        dades = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Ajusts.open('x') as Fitxer:
            os.chmod(str(Ajusts), 0o600)
            json.dump(dades, Fitxer, ensure_ascii=False, indent=2)
            Fitxer.write('\n')
    dades = json.loads(Ajusts.read_text())
    if not isinstance(dades, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if dades.get('user') != 'user':
        raise SystemExit('access.json: user는 현재 "user"만 지원합니다.')
    for Nom in ('ssh_password', 'vnc_password'):
        if not isinstance(dades.get(Nom), str):
            raise SystemExit('access.json: ' + Nom + '는 문자열이어야 합니다.')
    shell_contrasenya = dades['ssh_password'].encode('utf-8')
    if len(shell_contrasenya) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = dades['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. durada_VALOR 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def MATRIU_VALOR(Nom, VALOR):
        return 'static const unsigned char '+Nom+'[] = {'+','.join(str(수) for 수 in VALOR)+'};\n'
    머리 = MATRIU_VALOR('dispositiu_Clau', Clau_VALOR.read_bytes())
    머리 += MATRIU_VALOR('shell_contrasenya_resum', hashlib.sha256(shell_contrasenya).digest())
    머리 += MATRIU_VALOR('화면암호', 화면열쇠)
    generar = Camí / 'Perfil.h'
    generar.write_text(머리)
    os.chmod(str(generar), 0o600)
    return dades


if __name__ == '__main__':
    analitzador_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analitzador_48ee4b1b.add_argument('Acció', choices=['show', 'prepare'], nargs='?', default='prepare')
    인수 = analitzador_48ee4b1b.parse_args()
    dades = Prepara()
    if 인수.Acció == 'show':
        print(json.dumps(dades, ensure_ascii=False, indent=2))
    else:
        print('장치별 remot_VALOR connexió_e05f319b Ajusts 준비됨. contrasenya_VALOR verificar: python3 Eines/remot_Configuració.py show')
