#!/usr/bin/env python3
"""개인 verbinding_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from afstands_Instellings import Maak_gereed
from COSL배포 import bestemming_naam, biblioteek

Project_wortel = Path(__file__).resolve().parents[1]


def Loop():
    Afvoer = Project_wortel / 'build/verification/password-length'
    Afvoer.mkdir(parents=True, exist_ok=True)
    persoonlike_instellings = Project_wortel / 'build/remote/access.json'
    원래설정 = persoonlike_instellings.read_bytes()
    verslag_VALUE = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Instellings_pad = 시험터 / 'build/remote'
            Instellings_pad.mkdir(parents=True)
            Instellings_lêer = Instellings_pad / 'access.json'
            def skryf_Instellings(data):
                Instellings_lêer.write_text(json.dumps(data, ensure_ascii=False) + '\n')
                Instellings_lêer.chmod(0o600)
            def verifieer_Instellings(dop, 화면):
                skryf_Instellings({'user': 'user', 'ssh_password': dop, 'vnc_password': 화면})
                원본 = Instellings_lêer.read_bytes()
                Maak_gereed(시험터)
                assert Instellings_lêer.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Instellings_pad / 'Profiel.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Instellings_pad / 'Profiel.h').stat().st_mode & 0o777 == 0o600
            for dop, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                verifieer_Instellings(dop, 화면)
            verslag_VALUE['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for verander_VALUE, inskrywing_VALUE in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                data = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                data.update(verander_VALUE)
                skryf_Instellings(data)
                try:
                    Maak_gereed(시험터)
                except SystemExit as Fout:
                    assert inskrywing_VALUE in str(Fout), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + inskrywing_VALUE)
            verslag_VALUE['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Instellings = json.loads((Project_wortel / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            Verbinder = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Argief_nutsmiddel = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def uitvoer_bevel(인수, LOG_ry):
                subprocess.run(list(map(str, 인수)), cwd=str(Project_wortel), stdout=LOG_ry,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Naam, dop, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Naam, flush=True)
                verifieer_Instellings(dop, 화면)
                maatreël = Afvoer / Naam
                maatreël.mkdir(exist_ok=True)
                with (maatreël / 'build.log').open('wb') as LOG_ry:
                    목적들 = []
                    for 원본 in sorted((Project_wortel / 'afstands_VALUE').glob('*.c')):
                        bestemming_VALUE = 시험터 / (원본.stem + '.o')
                        uitvoer_bevel([번역기] + Instellings + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Instellings_pad, '-I', Project_wortel / 'afstands_VALUE', '-I', Project_wortel / 'vendor/libassh/src',
                             '-I', Project_wortel / 'vendor/bearssl/inc', '-I', Project_wortel / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', bestemming_VALUE], LOG_ry)
                        목적들.append(bestemming_VALUE)
                    afstands_bondel = 시험터 / 'libremote.a'
                    uitvoer_bevel([Argief_nutsmiddel, 'rcs', afstands_bondel] + 목적들, LOG_ry)
                    uitvoer_bevel([Verbinder, '--gc-sections', '-T', Project_wortel / '부팅/Skakel_Uitleg.ld', '-o', 시험터 / 'kernel.elf'] +
                         [Project_wortel / 'build' / (Naam + '.o') for Naam in bestemming_naam] + ['--start-group'] +
                         [afstands_bondel if Pad == 'remote/libremote.a' else Project_wortel / 'build' / Pad for Pad in biblioteek] + ['--end-group'], LOG_ry)
                    uitvoer_bevel([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], LOG_ry)
                with (maatreël / 'remote-test.log').open('wb') as LOG_ry:
                    uitvoer_bevel(['python3', Project_wortel / 'Nutsmiddels/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Instellings_lêer, '--output', maatreël], LOG_ry)
                valideer = json.loads((maatreël / 'report.json').read_text())
                assert valideer['passed']
                verslag_VALUE['checks'].append(Naam + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        verslag_VALUE['passed'] = True
    finally:
        verslag_VALUE['personal_settings_unchanged'] = persoonlike_instellings.read_bytes() == 원래설정
        if not verslag_VALUE['personal_settings_unchanged']:
            verslag_VALUE['passed'] = False
        verslag_VALUE['kernel_sha256'] = hashlib.sha256((Project_wortel / 'build/kernel8.img').read_bytes()).hexdigest()
        (Afvoer / 'report.json').write_text(json.dumps(verslag_VALUE, ensure_ascii=False, indent=2) + '\n')
    assert verslag_VALUE['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(verslag_VALUE, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Loop()
