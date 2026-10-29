#!/usr/bin/env python3
"""개인 conexão_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from remoto_Configurações import Preparar
from COSL배포 import destino_nome, biblioteca

ação_raiz = Path(__file__).resolve().parents[1]


def iniciar():
    saídaTexto = ação_raiz / 'build/verification/password-length'
    saídaTexto.mkdir(parents=True, exist_ok=True)
    Configurações_pessoais = ação_raiz / 'build/remote/access.json'
    원래설정 = Configurações_pessoais.read_bytes()
    relatar_VALOR = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            teste_workspace = Path(임시)
            Configurações_caminho = teste_workspace / 'build/remote'
            Configurações_caminho.mkdir(parents=True)
            Configurações_Arquivo = Configurações_caminho / 'access.json'
            def gravar_Configurações(dados):
                Configurações_Arquivo.write_text(json.dumps(dados, ensure_ascii=False) + '\n')
                Configurações_Arquivo.chmod(0o600)
            def verificar_Configurações(shell, tela):
                gravar_Configurações({'user': 'user', 'ssh_password': shell, 'vnc_password': tela})
                원본 = Configurações_Arquivo.read_bytes()
                Preparar(teste_workspace)
                assert Configurações_Arquivo.read_bytes() == 원본, 'Settings were rewritten'
                HEAD_VALOR = (Configurações_caminho / 'Perfil.h').read_text()
                일치 = re.search(r'tela_senha\[\] = \{([^}]+)\}', HEAD_VALOR)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Configurações_caminho / 'Perfil.h').stat().st_mode & 0o777 == 0o600
            for shell, tela in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                verificar_Configurações(shell, tela)
            relatar_VALOR['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for alterar_VALOR, entrada_VALOR_962f286b in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                dados = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                dados.update(alterar_VALOR)
                gravar_Configurações(dados)
                try:
                    Preparar(teste_workspace)
                except SystemExit as erro:
                    assert entrada_VALOR_962f286b in str(erro), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + entrada_VALOR_962f286b)
            relatar_VALOR['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Definições = json.loads((ação_raiz / 'build/remote/libassh-build.json').read_text())['flags']
            compilador_ferramenta = os.environ.get('ARM64_CC', 'clang')
            Conector = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            arquivo_ferramenta = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def Executar_comando(argumentos, LOG_linha):
                subprocess.run(list(map(str, argumentos)), cwd=str(ação_raiz), stdout=LOG_linha,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Nome, shell, tela in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Nome, flush=True)
                verificar_Configurações(shell, tela)
                resultado = saídaTexto / Nome
                resultado.mkdir(exist_ok=True)
                with (resultado / 'build.log').open('wb') as LOG_linha:
                    목적들 = []
                    for 원본 in sorted((ação_raiz / 'remoto_VALOR').glob('*.c')):
                        destino_VALOR = teste_workspace / (원본.stem + '.o')
                        Executar_comando([compilador_ferramenta] + Definições + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Configurações_caminho, '-I', ação_raiz / 'remoto_VALOR', '-I', ação_raiz / 'vendor/libassh/src',
                             '-I', ação_raiz / 'vendor/bearssl/inc', '-I', ação_raiz / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', destino_VALOR], LOG_linha)
                        목적들.append(destino_VALOR)
                    remoto_grupo = teste_workspace / 'libremote.a'
                    Executar_comando([arquivo_ferramenta, 'rcs', remoto_grupo] + 목적들, LOG_linha)
                    Executar_comando([Conector, '--gc-sections', '-T', ação_raiz / 'arranque_da_máquina/disposição_de_ligação.ld', '-o', teste_workspace / 'kernel.elf'] +
                         [ação_raiz / 'build' / (Nome + '.o') for Nome in destino_nome] + ['--start-group'] +
                         [remoto_grupo if caminho == 'remote/libremote.a' else ação_raiz / 'build' / caminho for caminho in biblioteca] + ['--end-group'], LOG_linha)
                    Executar_comando([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         teste_workspace / 'kernel.elf', teste_workspace / 'kernel8.img'], LOG_linha)
                with (resultado / 'remote-test.log').open('wb') as LOG_linha:
                    Executar_comando(['python3', ação_raiz / 'ferramentas/conexão_remota_teste.py', '--kernel', teste_workspace / 'kernel8.img',
                         '--access', Configurações_Arquivo, '--output', resultado], LOG_linha)
                validar = json.loads((resultado / 'report.json').read_text())
                assert validar['passed']
                relatar_VALOR['checks'].append(Nome + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        relatar_VALOR['passed'] = True
    finally:
        relatar_VALOR['personal_settings_unchanged'] = Configurações_pessoais.read_bytes() == 원래설정
        if not relatar_VALOR['personal_settings_unchanged']:
            relatar_VALOR['passed'] = False
        relatar_VALOR['kernel_sha256'] = hashlib.sha256((ação_raiz / 'build/kernel8.img').read_bytes()).hexdigest()
        (saídaTexto / 'report.json').write_text(json.dumps(relatar_VALOR, ensure_ascii=False, indent=2) + '\n')
    assert relatar_VALOR['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(relatar_VALOR, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    iniciar()
