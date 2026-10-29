#!/usr/bin/env python3
"""개인 conexión_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from remoto_Configuración import 준비
from COSL배포 import destino_nome, biblioteca

Project_raíz = Path(__file__).resolve().parents[1]


def Executar_2():
    Saída = Project_raíz / 'build/verification/password-length'
    Saída.mkdir(parents=True, exist_ok=True)
    configuración_persoal = Project_raíz / 'build/remote/access.json'
    원래설정 = configuración_persoal.read_bytes()
    informe_VALOR = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Configuración_camiño = 시험터 / 'build/remote'
            Configuración_camiño.mkdir(parents=True)
            Configuración_Ficheiro = Configuración_camiño / 'access.json'
            def escribir_Configuración(datos):
                Configuración_Ficheiro.write_text(json.dumps(datos, ensure_ascii=False) + '\n')
                Configuración_Ficheiro.chmod(0o600)
            def verificar_Configuración(shell, 화면):
                escribir_Configuración({'user': 'user', 'ssh_password': shell, 'vnc_password': 화면})
                원본 = Configuración_Ficheiro.read_bytes()
                준비(시험터)
                assert Configuración_Ficheiro.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Configuración_camiño / 'Perfil.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Configuración_camiño / 'Perfil.h').stat().st_mode & 0o777 == 0o600
            for shell, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                verificar_Configuración(shell, 화면)
            informe_VALOR['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for modificar_VALOR, introdución_VALOR in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                datos = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                datos.update(modificar_VALOR)
                escribir_Configuración(datos)
                try:
                    준비(시험터)
                except SystemExit as ERRO:
                    assert introdución_VALOR in str(ERRO), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + introdución_VALOR)
            informe_VALOR['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Configuración = json.loads((Project_raíz / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            Conector = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Arquivo_ferramenta = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def executar_comando(Argumentos, LOG_fila):
                subprocess.run(list(map(str, Argumentos)), cwd=str(Project_raíz), stdout=LOG_fila,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Nome, shell, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Nome, flush=True)
                verificar_Configuración(shell, 화면)
                RESULTANTE = Saída / Nome
                RESULTANTE.mkdir(exist_ok=True)
                with (RESULTANTE / 'build.log').open('wb') as LOG_fila:
                    목적들 = []
                    for 원본 in sorted((Project_raíz / 'remoto_VALOR').glob('*.c')):
                        destino_VALOR = 시험터 / (원본.stem + '.o')
                        executar_comando([번역기] + Configuración + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Configuración_camiño, '-I', Project_raíz / 'remoto_VALOR', '-I', Project_raíz / 'vendor/libassh/src',
                             '-I', Project_raíz / 'vendor/bearssl/inc', '-I', Project_raíz / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', destino_VALOR], LOG_fila)
                        목적들.append(destino_VALOR)
                    remoto_paquete = 시험터 / 'libremote.a'
                    executar_comando([Arquivo_ferramenta, 'rcs', remoto_paquete] + 목적들, LOG_fila)
                    executar_comando([Conector, '--gc-sections', '-T', Project_raíz / '부팅/Ligar_deseño.ld', '-o', 시험터 / 'kernel.elf'] +
                         [Project_raíz / 'build' / (Nome + '.o') for Nome in destino_nome] + ['--start-group'] +
                         [remoto_paquete if CAMIÑO == 'remote/libremote.a' else Project_raíz / 'build' / CAMIÑO for CAMIÑO in biblioteca] + ['--end-group'], LOG_fila)
                    executar_comando([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], LOG_fila)
                with (RESULTANTE / 'remote-test.log').open('wb') as LOG_fila:
                    executar_comando(['python3', Project_raíz / 'Ferramentas/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Configuración_Ficheiro, '--output', RESULTANTE], LOG_fila)
                validar = json.loads((RESULTANTE / 'report.json').read_text())
                assert validar['passed']
                informe_VALOR['checks'].append(Nome + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        informe_VALOR['passed'] = True
    finally:
        informe_VALOR['personal_settings_unchanged'] = configuración_persoal.read_bytes() == 원래설정
        if not informe_VALOR['personal_settings_unchanged']:
            informe_VALOR['passed'] = False
        informe_VALOR['kernel_sha256'] = hashlib.sha256((Project_raíz / 'build/kernel8.img').read_bytes()).hexdigest()
        (Saída / 'report.json').write_text(json.dumps(informe_VALOR, ensure_ascii=False, indent=2) + '\n')
    assert informe_VALOR['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(informe_VALOR, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Executar_2()
