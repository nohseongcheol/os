#!/usr/bin/env python3
"""개인 veza_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from udaljen_Postavke import Pripremi
from COSL배포 import odredište_ime, biblioteka

radnja_koren = Path(__file__).resolve().parents[1]


def koristiti():
    출력 = radnja_koren / 'build/verification/password-length'
    출력.mkdir(parents=True, exist_ok=True)
    Lična_Postavke = radnja_koren / 'build/remote/access.json'
    원래설정 = Lična_Postavke.read_bytes()
    izveštaj_VALUE = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Postavke_putanja = 시험터 / 'build/remote'
            Postavke_putanja.mkdir(parents=True)
            Postavke_Datoteka = Postavke_putanja / 'access.json'
            def 설정쓰기(podaci):
                Postavke_Datoteka.write_text(json.dumps(podaci, ensure_ascii=False) + '\n')
                Postavke_Datoteka.chmod(0o600)
            def verifikovati_Postavke(ljuska, 화면):
                설정쓰기({'user': 'user', 'ssh_password': ljuska, 'vnc_password': 화면})
                원본 = Postavke_Datoteka.read_bytes()
                Pripremi(시험터)
                assert Postavke_Datoteka.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Postavke_putanja / 'Profil.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Postavke_putanja / 'Profil.h').stat().st_mode & 0o777 == 0o600
            for ljuska, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                verifikovati_Postavke(ljuska, 화면)
            izveštaj_VALUE['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for promeniti_VALUE, stavka_VALUE in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                podaci = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                podaci.update(promeniti_VALUE)
                설정쓰기(podaci)
                try:
                    Pripremi(시험터)
                except SystemExit as greška:
                    assert stavka_VALUE in str(greška), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + stavka_VALUE)
            izveštaj_VALUE['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Postavke = json.loads((radnja_koren / 'build/remote/libassh-build.json').read_text())['flags']
            kompajler_alatka = os.environ.get('ARM64_CC', 'clang')
            Konektor = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Arhiva_alatka = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def Izvrši_komanda(인수, LOG_snimi):
                subprocess.run(list(map(str, 인수)), cwd=str(radnja_koren), stdout=LOG_snimi,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for ime, ljuska, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + ime, flush=True)
                verifikovati_Postavke(ljuska, 화면)
                KR = 출력 / ime
                KR.mkdir(exist_ok=True)
                with (KR / 'build.log').open('wb') as LOG_snimi:
                    목적들 = []
                    for 원본 in sorted((radnja_koren / 'udaljen_VALUE').glob('*.c')):
                        odredište_VALUE = 시험터 / (원본.stem + '.o')
                        Izvrši_komanda([kompajler_alatka] + Postavke + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Postavke_putanja, '-I', radnja_koren / 'udaljen_VALUE', '-I', radnja_koren / 'vendor/libassh/src',
                             '-I', radnja_koren / 'vendor/bearssl/inc', '-I', radnja_koren / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', odredište_VALUE], LOG_snimi)
                        목적들.append(odredište_VALUE)
                    udaljen_komplet = 시험터 / 'libremote.a'
                    Izvrši_komanda([Arhiva_alatka, 'rcs', udaljen_komplet] + 목적들, LOG_snimi)
                    Izvrši_komanda([Konektor, '--gc-sections', '-T', radnja_koren / '부팅/Veza_Raspored.ld', '-o', 시험터 / 'kernel.elf'] +
                         [radnja_koren / 'build' / (ime + '.o') for ime in odredište_ime] + ['--start-group'] +
                         [udaljen_komplet if putanja == 'remote/libremote.a' else radnja_koren / 'build' / putanja for putanja in biblioteka] + ['--end-group'], LOG_snimi)
                    Izvrši_komanda([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], LOG_snimi)
                with (KR / 'remote-test.log').open('wb') as LOG_snimi:
                    Izvrši_komanda(['python3', radnja_koren / 'Alatke/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Postavke_Datoteka, '--output', KR], LOG_snimi)
                potvrditi = json.loads((KR / 'report.json').read_text())
                assert potvrditi['passed']
                izveštaj_VALUE['checks'].append(ime + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        izveštaj_VALUE['passed'] = True
    finally:
        izveštaj_VALUE['personal_settings_unchanged'] = Lična_Postavke.read_bytes() == 원래설정
        if not izveštaj_VALUE['personal_settings_unchanged']:
            izveštaj_VALUE['passed'] = False
        izveštaj_VALUE['kernel_sha256'] = hashlib.sha256((radnja_koren / 'build/kernel8.img').read_bytes()).hexdigest()
        (출력 / 'report.json').write_text(json.dumps(izveštaj_VALUE, ensure_ascii=False, indent=2) + '\n')
    assert izveštaj_VALUE['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(izveštaj_VALUE, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    koristiti()
