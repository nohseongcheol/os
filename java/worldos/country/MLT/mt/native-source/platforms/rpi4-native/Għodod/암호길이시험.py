#!/usr/bin/env python3
"""개인 konnessjoni_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from mill_bogħod_Settings import Ħejji
from COSL배포 import destinazzjoni_isem, librerija

pprojetta_għerq = Path(__file__).resolve().parents[1]


def serje():
    출력 = pprojetta_għerq / 'build/verification/password-length'
    출력.mkdir(parents=True, exist_ok=True)
    konfigurazzjoni_personali = pprojetta_għerq / 'build/remote/access.json'
    원래설정 = konfigurazzjoni_personali.read_bytes()
    rapport_VALUE = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Settings_mogħdija = 시험터 / 'build/remote'
            Settings_mogħdija.mkdir(parents=True)
            Settings_fajl = Settings_mogħdija / 'access.json'
            def kiteb_Settings(data):
                Settings_fajl.write_text(json.dumps(data, ensure_ascii=False) + '\n')
                Settings_fajl.chmod(0o600)
            def vverifika_Settings(shell, 화면):
                kiteb_Settings({'user': 'user', 'ssh_password': shell, 'vnc_password': 화면})
                원본 = Settings_fajl.read_bytes()
                Ħejji(시험터)
                assert Settings_fajl.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Settings_mogħdija / 'Profil.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Settings_mogħdija / 'Profil.h').stat().st_mode & 0o777 == 0o600
            for shell, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                vverifika_Settings(shell, 화면)
            rapport_VALUE['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for bidel_VALUE, entrata_VALUE in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                data = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                data.update(bidel_VALUE)
                kiteb_Settings(data)
                try:
                    Ħejji(시험터)
                except SystemExit as żball:
                    assert entrata_VALUE in str(żball), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + entrata_VALUE)
            rapport_VALUE['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Settings = json.loads((pprojetta_għerq / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            konnettur = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Arkivju_għodda = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def eżegwixxa_kmand(인수, LOG_RECORD):
                subprocess.run(list(map(str, 인수)), cwd=str(pprojetta_għerq), stdout=LOG_RECORD,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for isem, shell, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + isem, flush=True)
                vverifika_Settings(shell, 화면)
                miżura = 출력 / isem
                miżura.mkdir(exist_ok=True)
                with (miżura / 'build.log').open('wb') as LOG_RECORD:
                    목적들 = []
                    for 원본 in sorted((pprojetta_għerq / 'mill_bogħod_VALUE').glob('*.c')):
                        destinazzjoni_VALUE = 시험터 / (원본.stem + '.o')
                        eżegwixxa_kmand([번역기] + Settings + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Settings_mogħdija, '-I', pprojetta_għerq / 'mill_bogħod_VALUE', '-I', pprojetta_għerq / 'vendor/libassh/src',
                             '-I', pprojetta_għerq / 'vendor/bearssl/inc', '-I', pprojetta_għerq / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', destinazzjoni_VALUE], LOG_RECORD)
                        목적들.append(destinazzjoni_VALUE)
                    mill_bogħod_lott = 시험터 / 'libremote.a'
                    eżegwixxa_kmand([Arkivju_għodda, 'rcs', mill_bogħod_lott] + 목적들, LOG_RECORD)
                    eżegwixxa_kmand([konnettur, '--gc-sections', '-T', pprojetta_għerq / '부팅/Link_Tqassim.ld', '-o', 시험터 / 'kernel.elf'] +
                         [pprojetta_għerq / 'build' / (isem + '.o') for isem in destinazzjoni_isem] + ['--start-group'] +
                         [mill_bogħod_lott if mogħdija == 'remote/libremote.a' else pprojetta_għerq / 'build' / mogħdija for mogħdija in librerija] + ['--end-group'], LOG_RECORD)
                    eżegwixxa_kmand([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], LOG_RECORD)
                with (miżura / 'remote-test.log').open('wb') as LOG_RECORD:
                    eżegwixxa_kmand(['python3', pprojetta_għerq / 'Għodod/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Settings_fajl, '--output', miżura], LOG_RECORD)
                vvalida = json.loads((miżura / 'report.json').read_text())
                assert vvalida['passed']
                rapport_VALUE['checks'].append(isem + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        rapport_VALUE['passed'] = True
    finally:
        rapport_VALUE['personal_settings_unchanged'] = konfigurazzjoni_personali.read_bytes() == 원래설정
        if not rapport_VALUE['personal_settings_unchanged']:
            rapport_VALUE['passed'] = False
        rapport_VALUE['kernel_sha256'] = hashlib.sha256((pprojetta_għerq / 'build/kernel8.img').read_bytes()).hexdigest()
        (출력 / 'report.json').write_text(json.dumps(rapport_VALUE, ensure_ascii=False, indent=2) + '\n')
    assert rapport_VALUE['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(rapport_VALUE, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    serje()
