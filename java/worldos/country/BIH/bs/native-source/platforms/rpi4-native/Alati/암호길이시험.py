#!/usr/bin/env python3
"""개인 veza_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from udaljeno_Postavke import Pripremiti
from COSL배포 import odredište_naziv, biblioteka

projicirati_koijen = Path(__file__).resolve().parents[1]


def Pokreni():
    Ispis = projicirati_koijen / 'build/verification/password-length'
    Ispis.mkdir(parents=True, exist_ok=True)
    korisničko_podešavanje = projicirati_koijen / 'build/remote/access.json'
    원래설정 = korisničko_podešavanje.read_bytes()
    izvještaj_VALUE = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Postavke_put = 시험터 / 'build/remote'
            Postavke_put.mkdir(parents=True)
            Postavke_fajl = Postavke_put / 'access.json'
            def pisati_Postavke(podaci):
                Postavke_fajl.write_text(json.dumps(podaci, ensure_ascii=False) + '\n')
                Postavke_fajl.chmod(0o600)
            def potvrditi_Postavke(ljuska, 화면):
                pisati_Postavke({'user': 'user', 'ssh_password': ljuska, 'vnc_password': 화면})
                원본 = Postavke_fajl.read_bytes()
                Pripremiti(시험터)
                assert Postavke_fajl.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Postavke_put / 'Profil.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Postavke_put / 'Profil.h').stat().st_mode & 0o777 == 0o600
            for ljuska, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                potvrditi_Postavke(ljuska, 화면)
            izvještaj_VALUE['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for promijeniti_VALUE, unos_VALUE in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                podaci = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                podaci.update(promijeniti_VALUE)
                pisati_Postavke(podaci)
                try:
                    Pripremiti(시험터)
                except SystemExit as GRESKA:
                    assert unos_VALUE in str(GRESKA), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + unos_VALUE)
            izvještaj_VALUE['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Postavke = json.loads((projicirati_koijen / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            konektor = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Arhiva_alatka = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def Izvrši_komanda(Argumenti, LOG_red):
                subprocess.run(list(map(str, Argumenti)), cwd=str(projicirati_koijen), stdout=LOG_red,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Naziv, ljuska, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Naziv, flush=True)
                potvrditi_Postavke(ljuska, 화면)
                mjera = Ispis / Naziv
                mjera.mkdir(exist_ok=True)
                with (mjera / 'build.log').open('wb') as LOG_red:
                    목적들 = []
                    for 원본 in sorted((projicirati_koijen / 'udaljeno_VALUE').glob('*.c')):
                        odredište_VALUE = 시험터 / (원본.stem + '.o')
                        Izvrši_komanda([번역기] + Postavke + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Postavke_put, '-I', projicirati_koijen / 'udaljeno_VALUE', '-I', projicirati_koijen / 'vendor/libassh/src',
                             '-I', projicirati_koijen / 'vendor/bearssl/inc', '-I', projicirati_koijen / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', odredište_VALUE], LOG_red)
                        목적들.append(odredište_VALUE)
                    udaljeno_paket = 시험터 / 'libremote.a'
                    Izvrši_komanda([Arhiva_alatka, 'rcs', udaljeno_paket] + 목적들, LOG_red)
                    Izvrši_komanda([konektor, '--gc-sections', '-T', projicirati_koijen / '부팅/Veza_izgled.ld', '-o', 시험터 / 'kernel.elf'] +
                         [projicirati_koijen / 'build' / (Naziv + '.o') for Naziv in odredište_naziv] + ['--start-group'] +
                         [udaljeno_paket if Putanja == 'remote/libremote.a' else projicirati_koijen / 'build' / Putanja for Putanja in biblioteka] + ['--end-group'], LOG_red)
                    Izvrši_komanda([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], LOG_red)
                with (mjera / 'remote-test.log').open('wb') as LOG_red:
                    Izvrši_komanda(['python3', projicirati_koijen / 'Alati/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Postavke_fajl, '--output', mjera], LOG_red)
                ovjeriti = json.loads((mjera / 'report.json').read_text())
                assert ovjeriti['passed']
                izvještaj_VALUE['checks'].append(Naziv + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        izvještaj_VALUE['passed'] = True
    finally:
        izvještaj_VALUE['personal_settings_unchanged'] = korisničko_podešavanje.read_bytes() == 원래설정
        if not izvještaj_VALUE['personal_settings_unchanged']:
            izvještaj_VALUE['passed'] = False
        izvještaj_VALUE['kernel_sha256'] = hashlib.sha256((projicirati_koijen / 'build/kernel8.img').read_bytes()).hexdigest()
        (Ispis / 'report.json').write_text(json.dumps(izvještaj_VALUE, ensure_ascii=False, indent=2) + '\n')
    assert izvještaj_VALUE['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(izvještaj_VALUE, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Pokreni()
