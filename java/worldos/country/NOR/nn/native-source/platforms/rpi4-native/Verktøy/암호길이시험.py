#!/usr/bin/env python3
"""개인 kontakt_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from fjern_Innstillingar import Klargjer
from COSL배포 import mål_namn, bibliotek

spegle_rot = Path(__file__).resolve().parents[1]


def Køyr_2():
    Utdata = spegle_rot / 'build/verification/password-length'
    Utdata.mkdir(parents=True, exist_ok=True)
    personlege_innstillingar = spegle_rot / 'build/remote/access.json'
    원래설정 = personlege_innstillingar.read_bytes()
    rapport_VALUE = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Innstillingar_bane = 시험터 / 'build/remote'
            Innstillingar_bane.mkdir(parents=True)
            Innstillingar_fil = Innstillingar_bane / 'access.json'
            def skrive_Innstillingar(data):
                Innstillingar_fil.write_text(json.dumps(data, ensure_ascii=False) + '\n')
                Innstillingar_fil.chmod(0o600)
            def stadfeste_Innstillingar(grensesnitt, 화면):
                skrive_Innstillingar({'user': 'user', 'ssh_password': grensesnitt, 'vnc_password': 화면})
                원본 = Innstillingar_fil.read_bytes()
                Klargjer(시험터)
                assert Innstillingar_fil.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Innstillingar_bane / 'Profil.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Innstillingar_bane / 'Profil.h').stat().st_mode & 0o777 == 0o600
            for grensesnitt, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                stadfeste_Innstillingar(grensesnitt, 화면)
            rapport_VALUE['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for endre_VALUE, oppføring_VALUE in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                data = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                data.update(endre_VALUE)
                skrive_Innstillingar(data)
                try:
                    Klargjer(시험터)
                except SystemExit as FEIL:
                    assert oppføring_VALUE in str(FEIL), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + oppføring_VALUE)
            rapport_VALUE['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Innstillingar = json.loads((spegle_rot / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            Kopling = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Arkiv_verktøy = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def Utfør_kommando(Argument, LOG_rad):
                subprocess.run(list(map(str, Argument)), cwd=str(spegle_rot), stdout=LOG_rad,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Namn, grensesnitt, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Namn, flush=True)
                stadfeste_Innstillingar(grensesnitt, 화면)
                forretningsmål = Utdata / Namn
                forretningsmål.mkdir(exist_ok=True)
                with (forretningsmål / 'build.log').open('wb') as LOG_rad:
                    목적들 = []
                    for 원본 in sorted((spegle_rot / 'fjern_VALUE').glob('*.c')):
                        mål_VALUE = 시험터 / (원본.stem + '.o')
                        Utfør_kommando([번역기] + Innstillingar + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Innstillingar_bane, '-I', spegle_rot / 'fjern_VALUE', '-I', spegle_rot / 'vendor/libassh/src',
                             '-I', spegle_rot / 'vendor/bearssl/inc', '-I', spegle_rot / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', mål_VALUE], LOG_rad)
                        목적들.append(mål_VALUE)
                    fjern_bunt = 시험터 / 'libremote.a'
                    Utfør_kommando([Arkiv_verktøy, 'rcs', fjern_bunt] + 목적들, LOG_rad)
                    Utfør_kommando([Kopling, '--gc-sections', '-T', spegle_rot / '부팅/kople_Oppsett.ld', '-o', 시험터 / 'kernel.elf'] +
                         [spegle_rot / 'build' / (Namn + '.o') for Namn in mål_namn] + ['--start-group'] +
                         [fjern_bunt if STIGE == 'remote/libremote.a' else spegle_rot / 'build' / STIGE for STIGE in bibliotek] + ['--end-group'], LOG_rad)
                    Utfør_kommando([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], LOG_rad)
                with (forretningsmål / 'remote-test.log').open('wb') as LOG_rad:
                    Utfør_kommando(['python3', spegle_rot / 'Verktøy/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Innstillingar_fil, '--output', forretningsmål], LOG_rad)
                bekrefte = json.loads((forretningsmål / 'report.json').read_text())
                assert bekrefte['passed']
                rapport_VALUE['checks'].append(Namn + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        rapport_VALUE['passed'] = True
    finally:
        rapport_VALUE['personal_settings_unchanged'] = personlege_innstillingar.read_bytes() == 원래설정
        if not rapport_VALUE['personal_settings_unchanged']:
            rapport_VALUE['passed'] = False
        rapport_VALUE['kernel_sha256'] = hashlib.sha256((spegle_rot / 'build/kernel8.img').read_bytes()).hexdigest()
        (Utdata / 'report.json').write_text(json.dumps(rapport_VALUE, ensure_ascii=False, indent=2) + '\n')
    assert rapport_VALUE['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(rapport_VALUE, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Køyr_2()
