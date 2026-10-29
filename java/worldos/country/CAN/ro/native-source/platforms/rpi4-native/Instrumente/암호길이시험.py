#!/usr/bin/env python3
"""개인 conexiune_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from la_distanță_Setări import Pregătiți
from COSL배포 import destinație_nume, bibliotecă

Project_rădăcină = Path(__file__).resolve().parents[1]


def Pornește():
    Rezultat = Project_rădăcină / 'build/verification/password-length'
    Rezultat.mkdir(parents=True, exist_ok=True)
    Personal_Setări = Project_rădăcină / 'build/remote/access.json'
    원래설정 = Personal_Setări.read_bytes()
    raport_VALUE = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Setări_cale = 시험터 / 'build/remote'
            Setări_cale.mkdir(parents=True)
            Setări_Fișier = Setări_cale / 'access.json'
            def scriere_Setări(date):
                Setări_Fișier.write_text(json.dumps(date, ensure_ascii=False) + '\n')
                Setări_Fișier.chmod(0o600)
            def verifica_Setări(shell, 화면):
                scriere_Setări({'user': 'user', 'ssh_password': shell, 'vnc_password': 화면})
                원본 = Setări_Fișier.read_bytes()
                Pregătiți(시험터)
                assert Setări_Fișier.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Setări_cale / 'Profil.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Setări_cale / 'Profil.h').stat().st_mode & 0o777 == 0o600
            for shell, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                verifica_Setări(shell, 화면)
            raport_VALUE['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for schimba_VALUE, intrare_VALUE in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                date = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                date.update(schimba_VALUE)
                scriere_Setări(date)
                try:
                    Pregătiți(시험터)
                except SystemExit as eroare:
                    assert intrare_VALUE in str(eroare), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + intrare_VALUE)
            raport_VALUE['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Setări = json.loads((Project_rădăcină / 'build/remote/libassh-build.json').read_text())['flags']
            compilator_instrument = os.environ.get('ARM64_CC', 'clang')
            Conector = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Arhivă_instrument = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def executa_comandă(Argumente, LOG_RECORD):
                subprocess.run(list(map(str, Argumente)), cwd=str(Project_rădăcină), stdout=LOG_RECORD,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Nume, shell, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Nume, flush=True)
                verifica_Setări(shell, 화면)
                KR = Rezultat / Nume
                KR.mkdir(exist_ok=True)
                with (KR / 'build.log').open('wb') as LOG_RECORD:
                    목적들 = []
                    for 원본 in sorted((Project_rădăcină / 'la_distanță_VALUE').glob('*.c')):
                        destinație_VALUE = 시험터 / (원본.stem + '.o')
                        executa_comandă([compilator_instrument] + Setări + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Setări_cale, '-I', Project_rădăcină / 'la_distanță_VALUE', '-I', Project_rădăcină / 'vendor/libassh/src',
                             '-I', Project_rădăcină / 'vendor/bearssl/inc', '-I', Project_rădăcină / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', destinație_VALUE], LOG_RECORD)
                        목적들.append(destinație_VALUE)
                    la_distanță_set = 시험터 / 'libremote.a'
                    executa_comandă([Arhivă_instrument, 'rcs', la_distanță_set] + 목적들, LOG_RECORD)
                    executa_comandă([Conector, '--gc-sections', '-T', Project_rădăcină / '부팅/Link_Aspect.ld', '-o', 시험터 / 'kernel.elf'] +
                         [Project_rădăcină / 'build' / (Nume + '.o') for Nume in destinație_nume] + ['--start-group'] +
                         [la_distanță_set if Cale == 'remote/libremote.a' else Project_rădăcină / 'build' / Cale for Cale in bibliotecă] + ['--end-group'], LOG_RECORD)
                    executa_comandă([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], LOG_RECORD)
                with (KR / 'remote-test.log').open('wb') as LOG_RECORD:
                    executa_comandă(['python3', Project_rădăcină / 'Instrumente/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Setări_Fișier, '--output', KR], LOG_RECORD)
                valida = json.loads((KR / 'report.json').read_text())
                assert valida['passed']
                raport_VALUE['checks'].append(Nume + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        raport_VALUE['passed'] = True
    finally:
        raport_VALUE['personal_settings_unchanged'] = Personal_Setări.read_bytes() == 원래설정
        if not raport_VALUE['personal_settings_unchanged']:
            raport_VALUE['passed'] = False
        raport_VALUE['kernel_sha256'] = hashlib.sha256((Project_rădăcină / 'build/kernel8.img').read_bytes()).hexdigest()
        (Rezultat / 'report.json').write_text(json.dumps(raport_VALUE, ensure_ascii=False, indent=2) + '\n')
    assert raport_VALUE['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(raport_VALUE, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Pornește()
