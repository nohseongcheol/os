#!/usr/bin/env python3
"""장치별 Chave_VALOR·conexión_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

Project_raíz = Path(__file__).resolve().parents[1]


def 준비(Project_raíz=Project_raíz):
    CAMIÑO = Project_raíz / 'build/remote'
    CAMIÑO.mkdir(parents=True, exist_ok=True)
    Configuración = CAMIÑO / 'access.json'
    Chave_VALOR = CAMIÑO / 'host-key.der'
    if not Chave_VALOR.exists():
        with Chave_VALOR.open('xb') as Ficheiro:
            os.chmod(str(Chave_VALOR), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Ficheiro)
    if not Configuración.exists():
        datos = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Configuración.open('x') as Ficheiro:
            os.chmod(str(Configuración), 0o600)
            json.dump(datos, Ficheiro, ensure_ascii=False, indent=2)
            Ficheiro.write('\n')
    datos = json.loads(Configuración.read_text())
    if not isinstance(datos, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if datos.get('user') != 'user':
        raise SystemExit('access.json: user는 ao_corrente_elemento "user"만 지원합니다.')
    for Nome in ('ssh_password', 'vnc_password'):
        if not isinstance(datos.get(Nome), str):
            raise SystemExit('access.json: ' + Nome + '는 문자열이어야 합니다.')
    shell_contrasinal = datos['ssh_password'].encode('utf-8')
    if len(shell_contrasinal) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        화면암호 = datos['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. duración_VALOR 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    화면열쇠 = 화면암호[:8].ljust(8, b'\0')
    def MATRIZ_VALOR(Nome, VALOR):
        return 'static const unsigned char '+Nome+'[] = {'+','.join(str(수) for 수 in VALOR)+'};\n'
    머리 = MATRIZ_VALOR('dispositivo_Chave', Chave_VALOR.read_bytes())
    머리 += MATRIZ_VALOR('shell_contrasinal_resumo', hashlib.sha256(shell_contrasinal).digest())
    머리 += MATRIZ_VALOR('화면암호', 화면열쇠)
    xerar = CAMIÑO / 'Perfil.h'
    xerar.write_text(머리)
    os.chmod(str(xerar), 0o600)
    return datos


if __name__ == '__main__':
    analizador_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizador_48ee4b1b.add_argument('Acción', choices=['show', 'prepare'], nargs='?', default='prepare')
    Argumentos = analizador_48ee4b1b.parse_args()
    datos = 준비()
    if Argumentos.Acción == 'show':
        print(json.dumps(datos, ensure_ascii=False, indent=2))
    else:
        print('장치별 remoto_VALOR conexión_e05f319b Configuración 준비됨. contrasinal_VALOR verificar: python3 Ferramentas/remoto_Configuración.py show')
