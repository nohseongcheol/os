#!/usr/bin/env python3
"""개인 połączenie_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from zdalny_Ustawienia import Przygotuj
from COSL배포 import cel_nazwa, biblioteka

Project_korzeń = Path(__file__).resolve().parents[1]


def Uruchom_2():
    pozycja_wyjścia = Project_korzeń / 'build/verification/password-length'
    pozycja_wyjścia.mkdir(parents=True, exist_ok=True)
    ustawienia_osobiste = Project_korzeń / 'build/remote/access.json'
    원래설정 = ustawienia_osobiste.read_bytes()
    Raport_WARTOŚĆ = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            test_obszar_roboczy = Path(임시)
            Ustawienia_ścieżka = test_obszar_roboczy / 'build/remote'
            Ustawienia_ścieżka.mkdir(parents=True)
            Ustawienia_Plik = Ustawienia_ścieżka / 'access.json'
            def zapis_Ustawienia(dane):
                Ustawienia_Plik.write_text(json.dumps(dane, ensure_ascii=False) + '\n')
                Ustawienia_Plik.chmod(0o600)
            def 설정확인(powłoka, 화면):
                zapis_Ustawienia({'user': 'user', 'ssh_password': powłoka, 'vnc_password': 화면})
                원본 = Ustawienia_Plik.read_bytes()
                Przygotuj(test_obszar_roboczy)
                assert Ustawienia_Plik.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Ustawienia_ścieżka / 'Profil.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Ustawienia_ścieżka / 'Profil.h').stat().st_mode & 0o777 == 0o600
            for powłoka, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                설정확인(powłoka, 화면)
            Raport_WARTOŚĆ['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for zmienić_WARTOŚĆ, wpis_WARTOŚĆ in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                dane = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                dane.update(zmienić_WARTOŚĆ)
                zapis_Ustawienia(dane)
                try:
                    Przygotuj(test_obszar_roboczy)
                except SystemExit as błąd:
                    assert wpis_WARTOŚĆ in str(błąd), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + wpis_WARTOŚĆ)
            Raport_WARTOŚĆ['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Ustawienia = json.loads((Project_korzeń / 'build/remote/libassh-build.json').read_text())['flags']
            kompilator_narzędzie = os.environ.get('ARM64_CC', 'clang')
            Łącznik = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Archiwum_narzędzie = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def Wykonaj_polecenie(argumenty, LOG_zapis):
                subprocess.run(list(map(str, argumenty)), cwd=str(Project_korzeń), stdout=LOG_zapis,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Nazwa, powłoka, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Nazwa, flush=True)
                설정확인(powłoka, 화면)
                WYNIK = pozycja_wyjścia / Nazwa
                WYNIK.mkdir(exist_ok=True)
                with (WYNIK / 'build.log').open('wb') as LOG_zapis:
                    목적들 = []
                    for 원본 in sorted((Project_korzeń / 'zdalny_WARTOŚĆ').glob('*.c')):
                        cel_WARTOŚĆ = test_obszar_roboczy / (원본.stem + '.o')
                        Wykonaj_polecenie([kompilator_narzędzie] + Ustawienia + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Ustawienia_ścieżka, '-I', Project_korzeń / 'zdalny_WARTOŚĆ', '-I', Project_korzeń / 'vendor/libassh/src',
                             '-I', Project_korzeń / 'vendor/bearssl/inc', '-I', Project_korzeń / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', cel_WARTOŚĆ], LOG_zapis)
                        목적들.append(cel_WARTOŚĆ)
                    zdalny_pakiet = test_obszar_roboczy / 'libremote.a'
                    Wykonaj_polecenie([Archiwum_narzędzie, 'rcs', zdalny_pakiet] + 목적들, LOG_zapis)
                    Wykonaj_polecenie([Łącznik, '--gc-sections', '-T', Project_korzeń / 'rozruch_maszyny/układ_konsolidacji.ld', '-o', test_obszar_roboczy / 'kernel.elf'] +
                         [Project_korzeń / 'build' / (Nazwa + '.o') for Nazwa in cel_nazwa] + ['--start-group'] +
                         [zdalny_pakiet if ścieżka_2 == 'remote/libremote.a' else Project_korzeń / 'build' / ścieżka_2 for ścieżka_2 in biblioteka] + ['--end-group'], LOG_zapis)
                    Wykonaj_polecenie([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         test_obszar_roboczy / 'kernel.elf', test_obszar_roboczy / 'kernel8.img'], LOG_zapis)
                with (WYNIK / 'remote-test.log').open('wb') as LOG_zapis:
                    Wykonaj_polecenie(['python3', Project_korzeń / 'narzędzia/połączenie_zdalne_test.py', '--kernel', test_obszar_roboczy / 'kernel8.img',
                         '--access', Ustawienia_Plik, '--output', WYNIK], LOG_zapis)
                walidować = json.loads((WYNIK / 'report.json').read_text())
                assert walidować['passed']
                Raport_WARTOŚĆ['checks'].append(Nazwa + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        Raport_WARTOŚĆ['passed'] = True
    finally:
        Raport_WARTOŚĆ['personal_settings_unchanged'] = ustawienia_osobiste.read_bytes() == 원래설정
        if not Raport_WARTOŚĆ['personal_settings_unchanged']:
            Raport_WARTOŚĆ['passed'] = False
        Raport_WARTOŚĆ['kernel_sha256'] = hashlib.sha256((Project_korzeń / 'build/kernel8.img').read_bytes()).hexdigest()
        (pozycja_wyjścia / 'report.json').write_text(json.dumps(Raport_WARTOŚĆ, ensure_ascii=False, indent=2) + '\n')
    assert Raport_WARTOŚĆ['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(Raport_WARTOŚĆ, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Uruchom_2()
