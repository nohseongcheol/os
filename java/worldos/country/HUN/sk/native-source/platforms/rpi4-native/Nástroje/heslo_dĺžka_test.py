#!/usr/bin/env python3
"""개인 kontakt_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from vzdialený_Nastavenia import Pripraviť
from COSL배포 import cieľ_názov, knižnica

akcia_koreň = Path(__file__).resolve().parents[1]


def Spustiť_2():
    Výstup = akcia_koreň / 'build/verification/password-length'
    Výstup.mkdir(parents=True, exist_ok=True)
    Osobné_Nastavenia = akcia_koreň / 'build/remote/access.json'
    원래설정 = Osobné_Nastavenia.read_bytes()
    správa_VALUE = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            test_pracovný_priestor = Path(임시)
            Nastavenia_cesta = test_pracovný_priestor / 'build/remote'
            Nastavenia_cesta.mkdir(parents=True)
            Nastavenia_Súbor = Nastavenia_cesta / 'access.json'
            def zapísať_Nastavenia(údaje):
                Nastavenia_Súbor.write_text(json.dumps(údaje, ensure_ascii=False) + '\n')
                Nastavenia_Súbor.chmod(0o600)
            def overiť_Nastavenia(셸, 화면):
                zapísať_Nastavenia({'user': 'user', 'ssh_password': 셸, 'vnc_password': 화면})
                원본 = Nastavenia_Súbor.read_bytes()
                Pripraviť(test_pracovný_priestor)
                assert Nastavenia_Súbor.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Nastavenia_cesta / 'Profil.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Nastavenia_cesta / 'Profil.h').stat().st_mode & 0o777 == 0o600
            for 셸, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                overiť_Nastavenia(셸, 화면)
            správa_VALUE['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for zmeniť_VALUE, položka_VALUE in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                údaje = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                údaje.update(zmeniť_VALUE)
                zapísať_Nastavenia(údaje)
                try:
                    Pripraviť(test_pracovný_priestor)
                except SystemExit as chyba:
                    assert položka_VALUE in str(chyba), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + položka_VALUE)
            správa_VALUE['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Nastavenia = json.loads((akcia_koreň / 'build/remote/libassh-build.json').read_text())['flags']
            kompilátor_nástroj = os.environ.get('ARM64_CC', 'clang')
            Spojnica = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Archív_nástroj = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def Vykonať_príkaz(Argumenty, LOG_RECORD):
                subprocess.run(list(map(str, Argumenty)), cwd=str(akcia_koreň), stdout=LOG_RECORD,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Názov, 셸, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Názov, flush=True)
                overiť_Nastavenia(셸, 화면)
                KR = Výstup / Názov
                KR.mkdir(exist_ok=True)
                with (KR / 'build.log').open('wb') as LOG_RECORD:
                    목적들 = []
                    for 원본 in sorted((akcia_koreň / 'vzdialený_VALUE').glob('*.c')):
                        cieľ_VALUE = test_pracovný_priestor / (원본.stem + '.o')
                        Vykonať_príkaz([kompilátor_nástroj] + Nastavenia + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Nastavenia_cesta, '-I', akcia_koreň / 'vzdialený_VALUE', '-I', akcia_koreň / 'vendor/libassh/src',
                             '-I', akcia_koreň / 'vendor/bearssl/inc', '-I', akcia_koreň / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', cieľ_VALUE], LOG_RECORD)
                        목적들.append(cieľ_VALUE)
                    vzdialený_zväzok = test_pracovný_priestor / 'libremote.a'
                    Vykonať_príkaz([Archív_nástroj, 'rcs', vzdialený_zväzok] + 목적들, LOG_RECORD)
                    Vykonať_príkaz([Spojnica, '--gc-sections', '-T', akcia_koreň / '부팅/odkaz_Navigácia.ld', '-o', test_pracovný_priestor / 'kernel.elf'] +
                         [akcia_koreň / 'build' / (Názov + '.o') for Názov in cieľ_názov] + ['--start-group'] +
                         [vzdialený_zväzok if Cesta == 'remote/libremote.a' else akcia_koreň / 'build' / Cesta for Cesta in knižnica] + ['--end-group'], LOG_RECORD)
                    Vykonať_príkaz([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         test_pracovný_priestor / 'kernel.elf', test_pracovný_priestor / 'kernel8.img'], LOG_RECORD)
                with (KR / 'remote-test.log').open('wb') as LOG_RECORD:
                    Vykonať_príkaz(['python3', akcia_koreň / 'Nástroje/vzdialené_pripojenie_test.py', '--kernel', test_pracovný_priestor / 'kernel8.img',
                         '--access', Nastavenia_Súbor, '--output', KR], LOG_RECORD)
                overiť_5fb2b747 = json.loads((KR / 'report.json').read_text())
                assert overiť_5fb2b747['passed']
                správa_VALUE['checks'].append(Názov + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        správa_VALUE['passed'] = True
    finally:
        správa_VALUE['personal_settings_unchanged'] = Osobné_Nastavenia.read_bytes() == 원래설정
        if not správa_VALUE['personal_settings_unchanged']:
            správa_VALUE['passed'] = False
        správa_VALUE['kernel_sha256'] = hashlib.sha256((akcia_koreň / 'build/kernel8.img').read_bytes()).hexdigest()
        (Výstup / 'report.json').write_text(json.dumps(správa_VALUE, ensure_ascii=False, indent=2) + '\n')
    assert správa_VALUE['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(správa_VALUE, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Spustiť_2()
