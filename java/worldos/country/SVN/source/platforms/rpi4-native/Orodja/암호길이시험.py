#!/usr/bin/env python3
"""개인 povezava_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from oddaljen_Nastavitve import Pripravi
from COSL배포 import cilj_ime, knjižnica

pobuda_koren = Path(__file__).resolve().parents[1]


def Zaženi():
    Izpis = pobuda_koren / 'build/verification/password-length'
    Izpis.mkdir(parents=True, exist_ok=True)
    Oseben_Nastavitve = pobuda_koren / 'build/remote/access.json'
    원래설정 = Oseben_Nastavitve.read_bytes()
    prijavi_VALUE = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            preskusiti_delovni_prostor = Path(임시)
            Nastavitve_pot = preskusiti_delovni_prostor / 'build/remote'
            Nastavitve_pot.mkdir(parents=True)
            Nastavitve_Datoteka = Nastavitve_pot / 'access.json'
            def pisati_Nastavitve(podatki):
                Nastavitve_Datoteka.write_text(json.dumps(podatki, ensure_ascii=False) + '\n')
                Nastavitve_Datoteka.chmod(0o600)
            def 설정확인(lupina, 화면):
                pisati_Nastavitve({'user': 'user', 'ssh_password': lupina, 'vnc_password': 화면})
                원본 = Nastavitve_Datoteka.read_bytes()
                Pripravi(preskusiti_delovni_prostor)
                assert Nastavitve_Datoteka.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Nastavitve_pot / 'Profil.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Nastavitve_pot / 'Profil.h').stat().st_mode & 0o777 == 0o600
            for lupina, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                설정확인(lupina, 화면)
            prijavi_VALUE['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for spremeniti_VALUE, vnos_VALUE in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                podatki = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                podatki.update(spremeniti_VALUE)
                pisati_Nastavitve(podatki)
                try:
                    Pripravi(preskusiti_delovni_prostor)
                except SystemExit as NAPAKA:
                    assert vnos_VALUE in str(NAPAKA), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + vnos_VALUE)
            prijavi_VALUE['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Nastavitve = json.loads((pobuda_koren / 'build/remote/libassh-build.json').read_text())['flags']
            prevajalnik_orodje = os.environ.get('ARM64_CC', 'clang')
            priključek = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Arhiv_orodje = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def Izvedi_ukaz(Argumenti, LOG_zapis):
                subprocess.run(list(map(str, Argumenti)), cwd=str(pobuda_koren), stdout=LOG_zapis,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Ime, lupina, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Ime, flush=True)
                설정확인(lupina, 화면)
                REZULTAT = Izpis / Ime
                REZULTAT.mkdir(exist_ok=True)
                with (REZULTAT / 'build.log').open('wb') as LOG_zapis:
                    목적들 = []
                    for 원본 in sorted((pobuda_koren / 'oddaljen_VALUE').glob('*.c')):
                        cilj_VALUE = preskusiti_delovni_prostor / (원본.stem + '.o')
                        Izvedi_ukaz([prevajalnik_orodje] + Nastavitve + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Nastavitve_pot, '-I', pobuda_koren / 'oddaljen_VALUE', '-I', pobuda_koren / 'vendor/libassh/src',
                             '-I', pobuda_koren / 'vendor/bearssl/inc', '-I', pobuda_koren / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', cilj_VALUE], LOG_zapis)
                        목적들.append(cilj_VALUE)
                    oddaljen_sveženj = preskusiti_delovni_prostor / 'libremote.a'
                    Izvedi_ukaz([Arhiv_orodje, 'rcs', oddaljen_sveženj] + 목적들, LOG_zapis)
                    Izvedi_ukaz([priključek, '--gc-sections', '-T', pobuda_koren / '부팅/Povezava_Krmarjenje.ld', '-o', preskusiti_delovni_prostor / 'kernel.elf'] +
                         [pobuda_koren / 'build' / (Ime + '.o') for Ime in cilj_ime] + ['--start-group'] +
                         [oddaljen_sveženj if POT == 'remote/libremote.a' else pobuda_koren / 'build' / POT for POT in knjižnica] + ['--end-group'], LOG_zapis)
                    Izvedi_ukaz([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         preskusiti_delovni_prostor / 'kernel.elf', preskusiti_delovni_prostor / 'kernel8.img'], LOG_zapis)
                with (REZULTAT / 'remote-test.log').open('wb') as LOG_zapis:
                    Izvedi_ukaz(['python3', pobuda_koren / 'Orodja/oddaljena_povezava_preskusiti.py', '--kernel', preskusiti_delovni_prostor / 'kernel8.img',
                         '--access', Nastavitve_Datoteka, '--output', REZULTAT], LOG_zapis)
                preveriti_veljavnost = json.loads((REZULTAT / 'report.json').read_text())
                assert preveriti_veljavnost['passed']
                prijavi_VALUE['checks'].append(Ime + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        prijavi_VALUE['passed'] = True
    finally:
        prijavi_VALUE['personal_settings_unchanged'] = Oseben_Nastavitve.read_bytes() == 원래설정
        if not prijavi_VALUE['personal_settings_unchanged']:
            prijavi_VALUE['passed'] = False
        prijavi_VALUE['kernel_sha256'] = hashlib.sha256((pobuda_koren / 'build/kernel8.img').read_bytes()).hexdigest()
        (Izpis / 'report.json').write_text(json.dumps(prijavi_VALUE, ensure_ascii=False, indent=2) + '\n')
    assert prijavi_VALUE['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(prijavi_VALUE, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Zaženi()
