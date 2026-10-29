#!/usr/bin/env python3
"""개인 ryšys_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from nuotolinis_Parametrai import Parengti
from COSL배포 import vieta_pavadinimas, biblioteka

Project_šaknis = Path(__file__).resolve().parents[1]


def Paleisti():
    Išvestis = Project_šaknis / 'build/verification/password-length'
    Išvestis.mkdir(parents=True, exist_ok=True)
    Asmeninis_Parametrai = Project_šaknis / 'build/remote/access.json'
    원래설정 = Asmeninis_Parametrai.read_bytes()
    pranešti_VALUE = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Parametrai_kelias = 시험터 / 'build/remote'
            Parametrai_kelias.mkdir(parents=True)
            Parametrai_Failas = Parametrai_kelias / 'access.json'
            def rašymas_Parametrai(duomenys):
                Parametrai_Failas.write_text(json.dumps(duomenys, ensure_ascii=False) + '\n')
                Parametrai_Failas.chmod(0o600)
            def patvirtinti_Parametrai(apvalkalas, 화면):
                rašymas_Parametrai({'user': 'user', 'ssh_password': apvalkalas, 'vnc_password': 화면})
                원본 = Parametrai_Failas.read_bytes()
                Parengti(시험터)
                assert Parametrai_Failas.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Parametrai_kelias / 'Profilis.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Parametrai_kelias / 'Profilis.h').stat().st_mode & 0o777 == 0o600
            for apvalkalas, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                patvirtinti_Parametrai(apvalkalas, 화면)
            pranešti_VALUE['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for keisti_VALUE, įrašas_VALUE in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                duomenys = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                duomenys.update(keisti_VALUE)
                rašymas_Parametrai(duomenys)
                try:
                    Parengti(시험터)
                except SystemExit as KLAIDA:
                    assert įrašas_VALUE in str(KLAIDA), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + įrašas_VALUE)
            pranešti_VALUE['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Nustatymai = json.loads((Project_šaknis / 'build/remote/libassh-build.json').read_text())['flags']
            kompiliatorius_įrankis = os.environ.get('ARM64_CC', 'clang')
            Jungtis = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Archyvas_įrankis = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def Vykdyti_komanda(Argumentai, LOG_RECORD):
                subprocess.run(list(map(str, Argumentai)), cwd=str(Project_šaknis), stdout=LOG_RECORD,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Pavadinimas_2, apvalkalas, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Pavadinimas_2, flush=True)
                patvirtinti_Parametrai(apvalkalas, 화면)
                REZULTATAS = Išvestis / Pavadinimas_2
                REZULTATAS.mkdir(exist_ok=True)
                with (REZULTATAS / 'build.log').open('wb') as LOG_RECORD:
                    목적들 = []
                    for 원본 in sorted((Project_šaknis / 'nuotolinis_VALUE').glob('*.c')):
                        vieta_VALUE = 시험터 / (원본.stem + '.o')
                        Vykdyti_komanda([kompiliatorius_įrankis] + Nustatymai + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Parametrai_kelias, '-I', Project_šaknis / 'nuotolinis_VALUE', '-I', Project_šaknis / 'vendor/libassh/src',
                             '-I', Project_šaknis / 'vendor/bearssl/inc', '-I', Project_šaknis / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', vieta_VALUE], LOG_RECORD)
                        목적들.append(vieta_VALUE)
                    nuotolinis_paketas = 시험터 / 'libremote.a'
                    Vykdyti_komanda([Archyvas_įrankis, 'rcs', nuotolinis_paketas] + 목적들, LOG_RECORD)
                    Vykdyti_komanda([Jungtis, '--gc-sections', '-T', Project_šaknis / '부팅/sieti_schema.ld', '-o', 시험터 / 'kernel.elf'] +
                         [Project_šaknis / 'build' / (Pavadinimas_2 + '.o') for Pavadinimas_2 in vieta_pavadinimas] + ['--start-group'] +
                         [nuotolinis_paketas if KELIAS == 'remote/libremote.a' else Project_šaknis / 'build' / KELIAS for KELIAS in biblioteka] + ['--end-group'], LOG_RECORD)
                    Vykdyti_komanda([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], LOG_RECORD)
                with (REZULTATAS / 'remote-test.log').open('wb') as LOG_RECORD:
                    Vykdyti_komanda(['python3', Project_šaknis / 'Įrankiai/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Parametrai_Failas, '--output', REZULTATAS], LOG_RECORD)
                tikrinti = json.loads((REZULTATAS / 'report.json').read_text())
                assert tikrinti['passed']
                pranešti_VALUE['checks'].append(Pavadinimas_2 + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        pranešti_VALUE['passed'] = True
    finally:
        pranešti_VALUE['personal_settings_unchanged'] = Asmeninis_Parametrai.read_bytes() == 원래설정
        if not pranešti_VALUE['personal_settings_unchanged']:
            pranešti_VALUE['passed'] = False
        pranešti_VALUE['kernel_sha256'] = hashlib.sha256((Project_šaknis / 'build/kernel8.img').read_bytes()).hexdigest()
        (Išvestis / 'report.json').write_text(json.dumps(pranešti_VALUE, ensure_ascii=False, indent=2) + '\n')
    assert pranešti_VALUE['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(pranešti_VALUE, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Paleisti()
