#!/usr/bin/env python3
"""개인 connexió_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from remot_Configuració import Prepara
from COSL배포 import destinació_nom, biblioteca

Project_rel = Path(__file__).resolve().parents[1]


def Executa_2():
    Sortida = Project_rel / 'build/verification/password-length'
    Sortida.mkdir(parents=True, exist_ok=True)
    configuració_personal = Project_rel / 'build/remote/access.json'
    원래설정 = configuració_personal.read_bytes()
    informe_VALOR = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Configuració_camí = 시험터 / 'build/remote'
            Configuració_camí.mkdir(parents=True)
            Configuració_arxiu = Configuració_camí / 'access.json'
            def escriure_Configuració(dades):
                Configuració_arxiu.write_text(json.dumps(dades, ensure_ascii=False) + '\n')
                Configuració_arxiu.chmod(0o600)
            def verificar_Configuració(shell, 화면):
                escriure_Configuració({'user': 'user', 'ssh_password': shell, 'vnc_password': 화면})
                원본 = Configuració_arxiu.read_bytes()
                Prepara(시험터)
                assert Configuració_arxiu.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Configuració_camí / 'Perfil.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Configuració_camí / 'Perfil.h').stat().st_mode & 0o777 == 0o600
            for shell, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                verificar_Configuració(shell, 화면)
            informe_VALOR['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for canviar_VALOR, introducció_VALOR in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                dades = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                dades.update(canviar_VALOR)
                escriure_Configuració(dades)
                try:
                    Prepara(시험터)
                except SystemExit as s_ha_produït_un_error:
                    assert introducció_VALOR in str(s_ha_produït_un_error), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + introducció_VALOR)
            informe_VALOR['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Ajusts = json.loads((Project_rel / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            Connector = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Arxiu_eina = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def Executa_ordre(인수, LOG_fila):
                subprocess.run(list(map(str, 인수)), cwd=str(Project_rel), stdout=LOG_fila,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Nom, shell, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Nom, flush=True)
                verificar_Configuració(shell, 화면)
                RESULTAT = Sortida / Nom
                RESULTAT.mkdir(exist_ok=True)
                with (RESULTAT / 'build.log').open('wb') as LOG_fila:
                    목적들 = []
                    for 원본 in sorted((Project_rel / 'remot_VALOR').glob('*.c')):
                        destinació_VALOR = 시험터 / (원본.stem + '.o')
                        Executa_ordre([번역기] + Ajusts + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Configuració_camí, '-I', Project_rel / 'remot_VALOR', '-I', Project_rel / 'vendor/libassh/src',
                             '-I', Project_rel / 'vendor/bearssl/inc', '-I', Project_rel / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', destinació_VALOR], LOG_fila)
                        목적들.append(destinació_VALOR)
                    remot_paquet = 시험터 / 'libremote.a'
                    Executa_ordre([Arxiu_eina, 'rcs', remot_paquet] + 목적들, LOG_fila)
                    Executa_ordre([Connector, '--gc-sections', '-T', Project_rel / '부팅/enllaç_disseny.ld', '-o', 시험터 / 'kernel.elf'] +
                         [Project_rel / 'build' / (Nom + '.o') for Nom in destinació_nom] + ['--start-group'] +
                         [remot_paquet if Camí == 'remote/libremote.a' else Project_rel / 'build' / Camí for Camí in biblioteca] + ['--end-group'], LOG_fila)
                    Executa_ordre([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], LOG_fila)
                with (RESULTAT / 'remote-test.log').open('wb') as LOG_fila:
                    Executa_ordre(['python3', Project_rel / 'Eines/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Configuració_arxiu, '--output', RESULTAT], LOG_fila)
                validar = json.loads((RESULTAT / 'report.json').read_text())
                assert validar['passed']
                informe_VALOR['checks'].append(Nom + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        informe_VALOR['passed'] = True
    finally:
        informe_VALOR['personal_settings_unchanged'] = configuració_personal.read_bytes() == 원래설정
        if not informe_VALOR['personal_settings_unchanged']:
            informe_VALOR['passed'] = False
        informe_VALOR['kernel_sha256'] = hashlib.sha256((Project_rel / 'build/kernel8.img').read_bytes()).hexdigest()
        (Sortida / 'report.json').write_text(json.dumps(informe_VALOR, ensure_ascii=False, indent=2) + '\n')
    assert informe_VALOR['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(informe_VALOR, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Executa_2()
