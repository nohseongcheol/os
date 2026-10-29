#!/usr/bin/env python3
"""장치별 Chave_VALOR·conexão_e05f319b 암호를 생성한다. build/remote의 비밀 자료는 공유하지 않는다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess

ação_raiz = Path(__file__).resolve().parents[1]


def Preparar(ação_raiz=ação_raiz):
    caminho = ação_raiz / 'build/remote'
    caminho.mkdir(parents=True, exist_ok=True)
    Definições = caminho / 'access.json'
    Chave_VALOR = caminho / 'host-key.der'
    if not Chave_VALOR.exists():
        with Chave_VALOR.open('xb') as ficheiro:
            os.chmod(str(Chave_VALOR), 0o600)
            subprocess.check_call(['openssl', 'ecparam', '-name', 'prime256v1', '-genkey',
                                   '-noout', '-outform', 'DER'], stdout=ficheiro)
    if not Definições.exists():
        dados = {'user': 'user', 'ssh_password': secrets.token_urlsafe(24),
                'vnc_password': ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789') for _ in range(8))}
        with Definições.open('x') as ficheiro:
            os.chmod(str(Definições), 0o600)
            json.dump(dados, ficheiro, ensure_ascii=False, indent=2)
            ficheiro.write('\n')
    dados = json.loads(Definições.read_text())
    if not isinstance(dados, dict):
        raise SystemExit('access.json: JSON 객체가 필요합니다.')
    if dados.get('user') != 'user':
        raise SystemExit('access.json: user는 em_dia_item "user"만 지원합니다.')
    for Nome in ('ssh_password', 'vnc_password'):
        if not isinstance(dados.get(Nome), str):
            raise SystemExit('access.json: ' + Nome + '는 문자열이어야 합니다.')
    shell_senha = dados['ssh_password'].encode('utf-8')
    if len(shell_senha) > 256:
        raise SystemExit('access.json: ssh_password가 SSH 서버의 UTF-8 256바이트 상한을 넘습니다.')
    try:
        tela_senha = dados['vnc_password'].encode('ascii')
    except UnicodeEncodeError:
        raise SystemExit('access.json: vnc_password는 VNC 클라이언트 호환을 위해 ASCII 문자로 작성하세요. duração_VALOR 제한은 없습니다.')
    # RFB 3.8 VNC Authentication (RFC 6143, 7.2.2): truncate or zero-pad.
    # The native DES code must always receive exactly eight bytes, even for "".
    tela_Chave = tela_senha[:8].ljust(8, b'\0')
    def MATRIZ_VALOR(Nome, VALOR):
        return 'static const unsigned char '+Nome+'[] = {'+','.join(str(número) for número in VALOR)+'};\n'
    HEAD_VALOR = MATRIZ_VALOR('celular_Chave', Chave_VALOR.read_bytes())
    HEAD_VALOR += MATRIZ_VALOR('shell_senha_resumo', hashlib.sha256(shell_senha).digest())
    HEAD_VALOR += MATRIZ_VALOR('tela_senha', tela_Chave)
    gerar = caminho / 'Perfil.h'
    gerar.write_text(HEAD_VALOR)
    os.chmod(str(gerar), 0o600)
    return dados


if __name__ == '__main__':
    analisador_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analisador_48ee4b1b.add_argument('Acção', choices=['show', 'prepare'], nargs='?', default='prepare')
    argumentos = analisador_48ee4b1b.parse_args()
    dados = Preparar()
    if argumentos.Acção == 'show':
        print(json.dumps(dados, ensure_ascii=False, indent=2))
    else:
        print('장치별 remoto_VALOR conexão_e05f319b Definições 준비됨. senha_VALOR verificar: python3 ferramentas/remoto_Configurações.py show')
