#!/usr/bin/env python3
"""개인 kontakt_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from ekstern_Innstillinger import Forbered
from COSL배포 import mål_navn, bibliotek

speile_rot = Path(__file__).resolve().parents[1]


def Kjør_2():
    Utgang = speile_rot / 'build/verification/password-length'
    Utgang.mkdir(parents=True, exist_ok=True)
    personlige_innstillinger = speile_rot / 'build/remote/access.json'
    원래설정 = personlige_innstillinger.read_bytes()
    rapport_VERDI = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            test_arbeidsområde = Path(임시)
            Innstillinger_bane = test_arbeidsområde / 'build/remote'
            Innstillinger_bane.mkdir(parents=True)
            Innstillinger_Fil = Innstillinger_bane / 'access.json'
            def skrive_Innstillinger(data):
                Innstillinger_Fil.write_text(json.dumps(data, ensure_ascii=False) + '\n')
                Innstillinger_Fil.chmod(0o600)
            def bekrefte_Innstillinger(Shell, skjermbilde):
                skrive_Innstillinger({'user': 'user', 'ssh_password': Shell, 'vnc_password': skjermbilde})
                원본 = Innstillinger_Fil.read_bytes()
                Forbered(test_arbeidsområde)
                assert Innstillinger_Fil.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Innstillinger_bane / 'Profil.h').read_text()
                일치 = re.search(r'skjermbilde_passord\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Innstillinger_bane / 'Profil.h').stat().st_mode & 0o777 == 0o600
            for Shell, skjermbilde in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                bekrefte_Innstillinger(Shell, skjermbilde)
            rapport_VERDI['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for endre_VERDI, oppføring_VERDI in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                data = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                data.update(endre_VERDI)
                skrive_Innstillinger(data)
                try:
                    Forbered(test_arbeidsområde)
                except SystemExit as feil:
                    assert oppføring_VERDI in str(feil), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + oppføring_VERDI)
            rapport_VERDI['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Innstillinger = json.loads((speile_rot / 'build/remote/libassh-build.json').read_text())['flags']
            kompilator_verktøy = os.environ.get('ARM64_CC', 'clang')
            Kobling = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Arkiv_verktøy = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def Utfør_kommando(Argumenter, LOG_POST):
                subprocess.run(list(map(str, Argumenter)), cwd=str(speile_rot), stdout=LOG_POST,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Navn, Shell, skjermbilde in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Navn, flush=True)
                bekrefte_Innstillinger(Shell, skjermbilde)
                KR = Utgang / Navn
                KR.mkdir(exist_ok=True)
                with (KR / 'build.log').open('wb') as LOG_POST:
                    목적들 = []
                    for 원본 in sorted((speile_rot / 'ekstern_VERDI_28edcfa1').glob('*.c')):
                        mål_VERDI = test_arbeidsområde / (원본.stem + '.o')
                        Utfør_kommando([kompilator_verktøy] + Innstillinger + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Innstillinger_bane, '-I', speile_rot / 'ekstern_VERDI_28edcfa1', '-I', speile_rot / 'vendor/libassh/src',
                             '-I', speile_rot / 'vendor/bearssl/inc', '-I', speile_rot / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', mål_VERDI], LOG_POST)
                        목적들.append(mål_VERDI)
                    ekstern_bunt = test_arbeidsområde / 'libremote.a'
                    Utfør_kommando([Arkiv_verktøy, 'rcs', ekstern_bunt] + 목적들, LOG_POST)
                    Utfør_kommando([Kobling, '--gc-sections', '-T', speile_rot / '부팅/koble_Oppsett.ld', '-o', test_arbeidsområde / 'kernel.elf'] +
                         [speile_rot / 'build' / (Navn + '.o') for Navn in mål_navn] + ['--start-group'] +
                         [ekstern_bunt if Sti == 'remote/libremote.a' else speile_rot / 'build' / Sti for Sti in bibliotek] + ['--end-group'], LOG_POST)
                    Utfør_kommando([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         test_arbeidsområde / 'kernel.elf', test_arbeidsområde / 'kernel8.img'], LOG_POST)
                with (KR / 'remote-test.log').open('wb') as LOG_POST:
                    Utfør_kommando(['python3', speile_rot / 'Verktøy/ekstern_tilkobling_test.py', '--kernel', test_arbeidsområde / 'kernel8.img',
                         '--access', Innstillinger_Fil, '--output', KR], LOG_POST)
                bekrefte_5fb2b747 = json.loads((KR / 'report.json').read_text())
                assert bekrefte_5fb2b747['passed']
                rapport_VERDI['checks'].append(Navn + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        rapport_VERDI['passed'] = True
    finally:
        rapport_VERDI['personal_settings_unchanged'] = personlige_innstillinger.read_bytes() == 원래설정
        if not rapport_VERDI['personal_settings_unchanged']:
            rapport_VERDI['passed'] = False
        rapport_VERDI['kernel_sha256'] = hashlib.sha256((speile_rot / 'build/kernel8.img').read_bytes()).hexdigest()
        (Utgang / 'report.json').write_text(json.dumps(rapport_VERDI, ensure_ascii=False, indent=2) + '\n')
    assert rapport_VERDI['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(rapport_VERDI, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Kjør_2()
