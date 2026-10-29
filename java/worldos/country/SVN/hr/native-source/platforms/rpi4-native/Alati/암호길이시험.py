#!/usr/bin/env python3
"""개인 veza_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from udaljeno_Postavke import Pripremi
from COSL배포 import odredište_naziv, biblioteka

akcija_korijen = Path(__file__).resolve().parents[1]


def Pokreni():
    Izlaz = akcija_korijen / 'build/verification/password-length'
    Izlaz.mkdir(parents=True, exist_ok=True)
    Osobno_Postavke = akcija_korijen / 'build/remote/access.json'
    원래설정 = Osobno_Postavke.read_bytes()
    izvješće_VALUE = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Postavke_put = 시험터 / 'build/remote'
            Postavke_put.mkdir(parents=True)
            Postavke_Datoteka = Postavke_put / 'access.json'
            def zapisivanje_Postavke(podaci):
                Postavke_Datoteka.write_text(json.dumps(podaci, ensure_ascii=False) + '\n')
                Postavke_Datoteka.chmod(0o600)
            def provjeriti_Postavke(ljuska, 화면):
                zapisivanje_Postavke({'user': 'user', 'ssh_password': ljuska, 'vnc_password': 화면})
                원본 = Postavke_Datoteka.read_bytes()
                Pripremi(시험터)
                assert Postavke_Datoteka.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Postavke_put / 'Profil.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Postavke_put / 'Profil.h').stat().st_mode & 0o777 == 0o600
            for ljuska, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                provjeriti_Postavke(ljuska, 화면)
            izvješće_VALUE['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for promijeniti_VALUE, unos_VALUE in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                podaci = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                podaci.update(promijeniti_VALUE)
                zapisivanje_Postavke(podaci)
                try:
                    Pripremi(시험터)
                except SystemExit as GREŠKA:
                    assert unos_VALUE in str(GREŠKA), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + unos_VALUE)
            izvješće_VALUE['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Postavke = json.loads((akcija_korijen / 'build/remote/libassh-build.json').read_text())['flags']
            kompilator_alat = os.environ.get('ARM64_CC', 'clang')
            Poveznik = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Arhiva_alat = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def Izvrši_naredba(Argumenti, LOG_zapis):
                subprocess.run(list(map(str, Argumenti)), cwd=str(akcija_korijen), stdout=LOG_zapis,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Ime, ljuska, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Ime, flush=True)
                provjeriti_Postavke(ljuska, 화면)
                REZULTAT = Izlaz / Ime
                REZULTAT.mkdir(exist_ok=True)
                with (REZULTAT / 'build.log').open('wb') as LOG_zapis:
                    목적들 = []
                    for 원본 in sorted((akcija_korijen / 'udaljeno_VALUE').glob('*.c')):
                        odredište_VALUE = 시험터 / (원본.stem + '.o')
                        Izvrši_naredba([kompilator_alat] + Postavke + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Postavke_put, '-I', akcija_korijen / 'udaljeno_VALUE', '-I', akcija_korijen / 'vendor/libassh/src',
                             '-I', akcija_korijen / 'vendor/bearssl/inc', '-I', akcija_korijen / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', odredište_VALUE], LOG_zapis)
                        목적들.append(odredište_VALUE)
                    udaljeno_komplet = 시험터 / 'libremote.a'
                    Izvrši_naredba([Arhiva_alat, 'rcs', udaljeno_komplet] + 목적들, LOG_zapis)
                    Izvrši_naredba([Poveznik, '--gc-sections', '-T', akcija_korijen / '부팅/veza_Raspored.ld', '-o', 시험터 / 'kernel.elf'] +
                         [akcija_korijen / 'build' / (Ime + '.o') for Ime in odredište_naziv] + ['--start-group'] +
                         [udaljeno_komplet if PUTANJA == 'remote/libremote.a' else akcija_korijen / 'build' / PUTANJA for PUTANJA in biblioteka] + ['--end-group'], LOG_zapis)
                    Izvrši_naredba([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], LOG_zapis)
                with (REZULTAT / 'remote-test.log').open('wb') as LOG_zapis:
                    Izvrši_naredba(['python3', akcija_korijen / 'Alati/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Postavke_Datoteka, '--output', REZULTAT], LOG_zapis)
                potvrditi = json.loads((REZULTAT / 'report.json').read_text())
                assert potvrditi['passed']
                izvješće_VALUE['checks'].append(Ime + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        izvješće_VALUE['passed'] = True
    finally:
        izvješće_VALUE['personal_settings_unchanged'] = Osobno_Postavke.read_bytes() == 원래설정
        if not izvješće_VALUE['personal_settings_unchanged']:
            izvješće_VALUE['passed'] = False
        izvješće_VALUE['kernel_sha256'] = hashlib.sha256((akcija_korijen / 'build/kernel8.img').read_bytes()).hexdigest()
        (Izlaz / 'report.json').write_text(json.dumps(izvješće_VALUE, ensure_ascii=False, indent=2) + '\n')
    assert izvješće_VALUE['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(izvješće_VALUE, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Pokreni()
