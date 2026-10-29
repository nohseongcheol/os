#!/usr/bin/env python3
"""개인 Verbindung_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from extern_Astellungen import Préparéieren
from COSL배포 import Zil_Numm, Bibliothéik

projezéieren_Racinn = Path(__file__).resolve().parents[1]


def Laf():
    출력 = projezéieren_Racinn / 'build/verification/password-length'
    출력.mkdir(parents=True, exist_ok=True)
    perséinlech_Parameteren = projezéieren_Racinn / 'build/remote/access.json'
    원래설정 = perséinlech_Parameteren.read_bytes()
    mellen_VALUE = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Astellungen_Wee = 시험터 / 'build/remote'
            Astellungen_Wee.mkdir(parents=True)
            Astellungen_Fichier = Astellungen_Wee / 'access.json'
            def schreiwen_Astellungen(Daten):
                Astellungen_Fichier.write_text(json.dumps(Daten, ensure_ascii=False) + '\n')
                Astellungen_Fichier.chmod(0o600)
            def verifizéieren_Astellungen(Shell, 화면):
                schreiwen_Astellungen({'user': 'user', 'ssh_password': Shell, 'vnc_password': 화면})
                원본 = Astellungen_Fichier.read_bytes()
                Préparéieren(시험터)
                assert Astellungen_Fichier.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Astellungen_Wee / 'Profil.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Astellungen_Wee / 'Profil.h').stat().st_mode & 0o777 == 0o600
            for Shell, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                verifizéieren_Astellungen(Shell, 화면)
            mellen_VALUE['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for änneren_VALUE, Agab_VALUE in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                Daten = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                Daten.update(änneren_VALUE)
                schreiwen_Astellungen(Daten)
                try:
                    Préparéieren(시험터)
                except SystemExit as Feeler:
                    assert Agab_VALUE in str(Feeler), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + Agab_VALUE)
            mellen_VALUE['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Astellungen = json.loads((projezéieren_Racinn / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            Konnektor = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Archiv_Tool = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def ausféieren_Befeel(인수, LOG_Rei):
                subprocess.run(list(map(str, 인수)), cwd=str(projezéieren_Racinn), stdout=LOG_Rei,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Numm, Shell, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Numm, flush=True)
                verifizéieren_Astellungen(Shell, 화면)
                Mooss = 출력 / Numm
                Mooss.mkdir(exist_ok=True)
                with (Mooss / 'build.log').open('wb') as LOG_Rei:
                    목적들 = []
                    for 원본 in sorted((projezéieren_Racinn / 'extern_VALUE').glob('*.c')):
                        Zil_VALUE = 시험터 / (원본.stem + '.o')
                        ausféieren_Befeel([번역기] + Astellungen + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Astellungen_Wee, '-I', projezéieren_Racinn / 'extern_VALUE', '-I', projezéieren_Racinn / 'vendor/libassh/src',
                             '-I', projezéieren_Racinn / 'vendor/bearssl/inc', '-I', projezéieren_Racinn / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', Zil_VALUE], LOG_Rei)
                        목적들.append(Zil_VALUE)
                    extern_Bëndel = 시험터 / 'libremote.a'
                    ausféieren_Befeel([Archiv_Tool, 'rcs', extern_Bëndel] + 목적들, LOG_Rei)
                    ausféieren_Befeel([Konnektor, '--gc-sections', '-T', projezéieren_Racinn / '부팅/Link_Layout.ld', '-o', 시험터 / 'kernel.elf'] +
                         [projezéieren_Racinn / 'build' / (Numm + '.o') for Numm in Zil_Numm] + ['--start-group'] +
                         [extern_Bëndel if Wee == 'remote/libremote.a' else projezéieren_Racinn / 'build' / Wee for Wee in Bibliothéik] + ['--end-group'], LOG_Rei)
                    ausféieren_Befeel([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], LOG_Rei)
                with (Mooss / 'remote-test.log').open('wb') as LOG_Rei:
                    ausféieren_Befeel(['python3', projezéieren_Racinn / 'Tools/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Astellungen_Fichier, '--output', Mooss], LOG_Rei)
                validéieren = json.loads((Mooss / 'report.json').read_text())
                assert validéieren['passed']
                mellen_VALUE['checks'].append(Numm + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        mellen_VALUE['passed'] = True
    finally:
        mellen_VALUE['personal_settings_unchanged'] = perséinlech_Parameteren.read_bytes() == 원래설정
        if not mellen_VALUE['personal_settings_unchanged']:
            mellen_VALUE['passed'] = False
        mellen_VALUE['kernel_sha256'] = hashlib.sha256((projezéieren_Racinn / 'build/kernel8.img').read_bytes()).hexdigest()
        (출력 / 'report.json').write_text(json.dumps(mellen_VALUE, ensure_ascii=False, indent=2) + '\n')
    assert mellen_VALUE['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(mellen_VALUE, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Laf()
