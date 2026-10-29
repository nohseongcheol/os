#!/usr/bin/env python3
"""개인 kontakt_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from fjärr_Inställningar import Förbereda
from COSL배포 import mål_namn, bibliotek

åtgärd_rot = Path(__file__).resolve().parents[1]


def Kör():
    utmatningsposition = åtgärd_rot / 'build/verification/password-length'
    utmatningsposition.mkdir(parents=True, exist_ok=True)
    Personliga_inställningar = åtgärd_rot / 'build/remote/access.json'
    원래설정 = Personliga_inställningar.read_bytes()
    Rapport_värde = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            test_arbetsyta = Path(임시)
            Inställningar_väg = test_arbetsyta / 'build/remote'
            Inställningar_väg.mkdir(parents=True)
            Inställningar_fil = Inställningar_väg / 'access.json'
            def skriva_Inställningar(data):
                Inställningar_fil.write_text(json.dumps(data, ensure_ascii=False) + '\n')
                Inställningar_fil.chmod(0o600)
            def verifiera_Inställningar(Shell, skärmbild):
                skriva_Inställningar({'user': 'user', 'ssh_password': Shell, 'vnc_password': skärmbild})
                원본 = Inställningar_fil.read_bytes()
                Förbereda(test_arbetsyta)
                assert Inställningar_fil.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Inställningar_väg / 'Profil.h').read_text()
                일치 = re.search(r'skärmbild_lösenord\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Inställningar_väg / 'Profil.h').stat().st_mode & 0o777 == 0o600
            for Shell, skärmbild in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                verifiera_Inställningar(Shell, skärmbild)
            Rapport_värde['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for ändra_värde, post_värde in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                data = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                data.update(ändra_värde)
                skriva_Inställningar(data)
                try:
                    Förbereda(test_arbetsyta)
                except SystemExit as fel:
                    assert post_värde in str(fel), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + post_värde)
            Rapport_värde['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Inställningar = json.loads((åtgärd_rot / 'build/remote/libassh-build.json').read_text())['flags']
            kompilerare_verktyg = os.environ.get('ARM64_CC', 'clang')
            Koppling = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Arkiv_verktyg = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def köra_kommando(argument, LOG_POST):
                subprocess.run(list(map(str, argument)), cwd=str(åtgärd_rot), stdout=LOG_POST,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Namn, Shell, skärmbild in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Namn, flush=True)
                verifiera_Inställningar(Shell, skärmbild)
                RESULTAT = utmatningsposition / Namn
                RESULTAT.mkdir(exist_ok=True)
                with (RESULTAT / 'build.log').open('wb') as LOG_POST:
                    목적들 = []
                    for 원본 in sorted((åtgärd_rot / 'fjärr_värde').glob('*.c')):
                        mål_värde = test_arbetsyta / (원본.stem + '.o')
                        köra_kommando([kompilerare_verktyg] + Inställningar + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Inställningar_väg, '-I', åtgärd_rot / 'fjärr_värde', '-I', åtgärd_rot / 'vendor/libassh/src',
                             '-I', åtgärd_rot / 'vendor/bearssl/inc', '-I', åtgärd_rot / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', mål_värde], LOG_POST)
                        목적들.append(mål_värde)
                    fjärr_bunt = test_arbetsyta / 'libremote.a'
                    köra_kommando([Arkiv_verktyg, 'rcs', fjärr_bunt] + 목적들, LOG_POST)
                    köra_kommando([Koppling, '--gc-sections', '-T', åtgärd_rot / 'maskinstart/länkningslayout.ld', '-o', test_arbetsyta / 'kernel.elf'] +
                         [åtgärd_rot / 'build' / (Namn + '.o') for Namn in mål_namn] + ['--start-group'] +
                         [fjärr_bunt if sökväg_2 == 'remote/libremote.a' else åtgärd_rot / 'build' / sökväg_2 for sökväg_2 in bibliotek] + ['--end-group'], LOG_POST)
                    köra_kommando([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         test_arbetsyta / 'kernel.elf', test_arbetsyta / 'kernel8.img'], LOG_POST)
                with (RESULTAT / 'remote-test.log').open('wb') as LOG_POST:
                    köra_kommando(['python3', åtgärd_rot / 'verktyg/fjärranslutning_test.py', '--kernel', test_arbetsyta / 'kernel8.img',
                         '--access', Inställningar_fil, '--output', RESULTAT], LOG_POST)
                validera = json.loads((RESULTAT / 'report.json').read_text())
                assert validera['passed']
                Rapport_värde['checks'].append(Namn + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        Rapport_värde['passed'] = True
    finally:
        Rapport_värde['personal_settings_unchanged'] = Personliga_inställningar.read_bytes() == 원래설정
        if not Rapport_värde['personal_settings_unchanged']:
            Rapport_värde['passed'] = False
        Rapport_värde['kernel_sha256'] = hashlib.sha256((åtgärd_rot / 'build/kernel8.img').read_bytes()).hexdigest()
        (utmatningsposition / 'report.json').write_text(json.dumps(Rapport_värde, ensure_ascii=False, indent=2) + '\n')
    assert Rapport_värde['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(Rapport_värde, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Kör()
