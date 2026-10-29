#!/usr/bin/env python3
"""개인 kontakt_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from vzdálený_Nastavení import Připravit
from COSL배포 import cíl_název, knihovna

akce_kořen = Path(__file__).resolve().parents[1]


def Spustit_2():
    výstupní_pozice = akce_kořen / 'build/verification/password-length'
    výstupní_pozice.mkdir(parents=True, exist_ok=True)
    Osobní_Nastavení = akce_kořen / 'build/remote/access.json'
    원래설정 = Osobní_Nastavení.read_bytes()
    Zpráva_HODNOTA = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            test_pracovní_prostor = Path(임시)
            Nastavení_cesta = test_pracovní_prostor / 'build/remote'
            Nastavení_cesta.mkdir(parents=True)
            Nastavení_Soubor = Nastavení_cesta / 'access.json'
            def zápis_Nastavení(data):
                Nastavení_Soubor.write_text(json.dumps(data, ensure_ascii=False) + '\n')
                Nastavení_Soubor.chmod(0o600)
            def ověřit_Nastavení(prostředí, 화면):
                zápis_Nastavení({'user': 'user', 'ssh_password': prostředí, 'vnc_password': 화면})
                원본 = Nastavení_Soubor.read_bytes()
                Připravit(test_pracovní_prostor)
                assert Nastavení_Soubor.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Nastavení_cesta / 'Profil.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Nastavení_cesta / 'Profil.h').stat().st_mode & 0o777 == 0o600
            for prostředí, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                ověřit_Nastavení(prostředí, 화면)
            Zpráva_HODNOTA['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for změnit_HODNOTA, položka_HODNOTA in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                data = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                data.update(změnit_HODNOTA)
                zápis_Nastavení(data)
                try:
                    Připravit(test_pracovní_prostor)
                except SystemExit as chyba:
                    assert položka_HODNOTA in str(chyba), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + položka_HODNOTA)
            Zpráva_HODNOTA['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Nastavení = json.loads((akce_kořen / 'build/remote/libassh-build.json').read_text())['flags']
            kompilátor_nástroj = os.environ.get('ARM64_CC', 'clang')
            Spojnice = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Archiv_nástroj = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def Provést_příkaz(argumenty, LOGZ_ZÁZNAM):
                subprocess.run(list(map(str, argumenty)), cwd=str(akce_kořen), stdout=LOGZ_ZÁZNAM,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Název, prostředí, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Název, flush=True)
                ověřit_Nastavení(prostředí, 화면)
                VÝSLEDEK = výstupní_pozice / Název
                VÝSLEDEK.mkdir(exist_ok=True)
                with (VÝSLEDEK / 'build.log').open('wb') as LOGZ_ZÁZNAM:
                    목적들 = []
                    for 원본 in sorted((akce_kořen / 'vzdálený_HODNOTA').glob('*.c')):
                        cíl_HODNOTA = test_pracovní_prostor / (원본.stem + '.o')
                        Provést_příkaz([kompilátor_nástroj] + Nastavení + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Nastavení_cesta, '-I', akce_kořen / 'vzdálený_HODNOTA', '-I', akce_kořen / 'vendor/libassh/src',
                             '-I', akce_kořen / 'vendor/bearssl/inc', '-I', akce_kořen / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', cíl_HODNOTA], LOGZ_ZÁZNAM)
                        목적들.append(cíl_HODNOTA)
                    vzdálený_sada = test_pracovní_prostor / 'libremote.a'
                    Provést_příkaz([Archiv_nástroj, 'rcs', vzdálený_sada] + 목적들, LOGZ_ZÁZNAM)
                    Provést_příkaz([Spojnice, '--gc-sections', '-T', akce_kořen / 'spuštění_stroje/rozvržení_spojování.ld', '-o', test_pracovní_prostor / 'kernel.elf'] +
                         [akce_kořen / 'build' / (Název + '.o') for Název in cíl_název] + ['--start-group'] +
                         [vzdálený_sada if cesta_2 == 'remote/libremote.a' else akce_kořen / 'build' / cesta_2 for cesta_2 in knihovna] + ['--end-group'], LOGZ_ZÁZNAM)
                    Provést_příkaz([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         test_pracovní_prostor / 'kernel.elf', test_pracovní_prostor / 'kernel8.img'], LOGZ_ZÁZNAM)
                with (VÝSLEDEK / 'remote-test.log').open('wb') as LOGZ_ZÁZNAM:
                    Provést_příkaz(['python3', akce_kořen / 'nástroje/vzdálené_připojení_test.py', '--kernel', test_pracovní_prostor / 'kernel8.img',
                         '--access', Nastavení_Soubor, '--output', VÝSLEDEK], LOGZ_ZÁZNAM)
                ověřit_5fb2b747 = json.loads((VÝSLEDEK / 'report.json').read_text())
                assert ověřit_5fb2b747['passed']
                Zpráva_HODNOTA['checks'].append(Název + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        Zpráva_HODNOTA['passed'] = True
    finally:
        Zpráva_HODNOTA['personal_settings_unchanged'] = Osobní_Nastavení.read_bytes() == 원래설정
        if not Zpráva_HODNOTA['personal_settings_unchanged']:
            Zpráva_HODNOTA['passed'] = False
        Zpráva_HODNOTA['kernel_sha256'] = hashlib.sha256((akce_kořen / 'build/kernel8.img').read_bytes()).hexdigest()
        (výstupní_pozice / 'report.json').write_text(json.dumps(Zpráva_HODNOTA, ensure_ascii=False, indent=2) + '\n')
    assert Zpráva_HODNOTA['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(Zpráva_HODNOTA, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Spustit_2()
