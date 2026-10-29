#!/usr/bin/env python3
"""장치별 valorTecla·conexión 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

raízProyecto = Path(__file__).resolve().parents[1]


def preparar(raízProyecto=raízProyecto):
    ruta = raízProyecto / 'build/remote'
    ruta.mkdir(parents=True, exist_ok=True)
    ajustes = ruta / 'access.json'
    valorTecla = ruta / 'host-key.der'
    if not valorTecla.exists():
        with valorTecla.open('xb') as Archivo:
            os.chmod(str(valorTecla), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=Archivo)
    if not ajustes.exists():
        Datos = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with ajustes.open('x') as Archivo:
            os.chmod(str(ajustes), 0o600)
            json.dump(Datos, Archivo, ensure_ascii=False, indent=2)
            Archivo.write('\n')
    Datos = json.loads(ajustes.read_text())
    if not isinstance(Datos, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if Datos.get('user') != 'user':
        raise SystemExit('access.json: user는 elementoListaActual "user"만 지원합니다.')
    for nombre in ('ssh_password', 'vnc_password'):
        if not isinstance(Datos.get(nombre), str):
            raise SystemExit('access.json: ' + nombre + '는 문자열이어야 합니다.')
    contraseñaIntérpreteComandos = Datos['ssh_password'].encode('utf-8')
    if len(contraseñaIntérpreteComandos) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        contraseñaPantalla = Datos['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. longitud 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    teclaPantalla = contraseñaPantalla[:8].ljust(8, b'\0')
    def valorArreglo(nombre, valor):
        return 'static const unsigned char '+nombre+'[] = {'+','.join(str(númeroValor) for númeroValor in valor)+'};\n'
    valorCabecera = valorArreglo('teclaDispositivo', valorTecla.read_bytes())
    valorCabecera += valorArreglo('resumenContraseñaIntérpreteComandos', hashlib.sha256(contraseñaIntérpreteComandos).digest())
    valorCabecera += valorArreglo('contraseñaPantalla', teclaPantalla)
    generar = ruta / 'perfil.h'
    generar.write_text(valorCabecera)
    os.chmod(str(generar), 0o600)
    return Datos


if __name__ == '__main__':
    Analizador = argparse.ArgumentParser(description=__doc__)
    Analizador.add_argument('acción', choices=['show', 'prepare'], nargs='?', default='prepare')
    argumentos = Analizador.parse_args()
    Datos = preparar()
    if argumentos.acción == 'show':
        print(json.dumps(Datos, ensure_ascii=False, indent=2))
    else:
        print('장치별 valorRemoto conexión ajustes esPreparado. valorContraseña verificar: python3 Herramientas/ajustesRemoto.py show')
