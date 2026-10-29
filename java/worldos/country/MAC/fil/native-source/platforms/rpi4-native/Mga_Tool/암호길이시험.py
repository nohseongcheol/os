#!/usr/bin/env python3
"""개인 koneksyon_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from malayuan_Mga_Setting import Ihanda
from COSL배포 import patutunguhan_pangalan, library

Project_root = Path(__file__).resolve().parents[1]


def run():
    출력 = Project_root / 'build/verification/password-length'
    출력.mkdir(parents=True, exist_ok=True)
    mga_seting_na_personal = Project_root / 'build/remote/access.json'
    원래설정 = mga_seting_na_personal.read_bytes()
    ulat_VALUE = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Mga_Setting_path = 시험터 / 'build/remote'
            Mga_Setting_path.mkdir(parents=True)
            Mga_Setting_file = Mga_Setting_path / 'access.json'
            def sumulat_Mga_Setting(data):
                Mga_Setting_file.write_text(json.dumps(data, ensure_ascii=False) + '\n')
                Mga_Setting_file.chmod(0o600)
            def tiyakin_kumpirmahin_Mga_Setting(shell, 화면):
                sumulat_Mga_Setting({'user': 'user', 'ssh_password': shell, 'vnc_password': 화면})
                원본 = Mga_Setting_file.read_bytes()
                Ihanda(시험터)
                assert Mga_Setting_file.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Mga_Setting_path / 'Profile.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Mga_Setting_path / 'Profile.h').stat().st_mode & 0o777 == 0o600
            for shell, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                tiyakin_kumpirmahin_Mga_Setting(shell, 화면)
            ulat_VALUE['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for baguhin_VALUE, pagpasok_VALUE in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                data = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                data.update(baguhin_VALUE)
                sumulat_Mga_Setting(data)
                try:
                    Ihanda(시험터)
                except SystemExit as error:
                    assert pagpasok_VALUE in str(error), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + pagpasok_VALUE)
            ulat_VALUE['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Mga_Setting = json.loads((Project_root / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            tagapagkabit = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Archive_tool = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def Mag_execute_utos(인수, LOG_hanay):
                subprocess.run(list(map(str, 인수)), cwd=str(Project_root), stdout=LOG_hanay,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for pangalan, shell, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + pangalan, flush=True)
                tiyakin_kumpirmahin_Mga_Setting(shell, 화면)
                sukat = 출력 / pangalan
                sukat.mkdir(exist_ok=True)
                with (sukat / 'build.log').open('wb') as LOG_hanay:
                    목적들 = []
                    for 원본 in sorted((Project_root / 'malayuan_VALUE').glob('*.c')):
                        patutunguhan_VALUE = 시험터 / (원본.stem + '.o')
                        Mag_execute_utos([번역기] + Mga_Setting + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Mga_Setting_path, '-I', Project_root / 'malayuan_VALUE', '-I', Project_root / 'vendor/libassh/src',
                             '-I', Project_root / 'vendor/bearssl/inc', '-I', Project_root / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', patutunguhan_VALUE], LOG_hanay)
                        목적들.append(patutunguhan_VALUE)
                    malayuan_bundle = 시험터 / 'libremote.a'
                    Mag_execute_utos([Archive_tool, 'rcs', malayuan_bundle] + 목적들, LOG_hanay)
                    Mag_execute_utos([tagapagkabit, '--gc-sections', '-T', Project_root / '부팅/Link_Layout.ld', '-o', 시험터 / 'kernel.elf'] +
                         [Project_root / 'build' / (pangalan + '.o') for pangalan in patutunguhan_pangalan] + ['--start-group'] +
                         [malayuan_bundle if path == 'remote/libremote.a' else Project_root / 'build' / path for path in library] + ['--end-group'], LOG_hanay)
                    Mag_execute_utos([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], LOG_hanay)
                with (sukat / 'remote-test.log').open('wb') as LOG_hanay:
                    Mag_execute_utos(['python3', Project_root / 'Mga_Tool/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Mga_Setting_file, '--output', sukat], LOG_hanay)
                patunayan = json.loads((sukat / 'report.json').read_text())
                assert patunayan['passed']
                ulat_VALUE['checks'].append(pangalan + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        ulat_VALUE['passed'] = True
    finally:
        ulat_VALUE['personal_settings_unchanged'] = mga_seting_na_personal.read_bytes() == 원래설정
        if not ulat_VALUE['personal_settings_unchanged']:
            ulat_VALUE['passed'] = False
        ulat_VALUE['kernel_sha256'] = hashlib.sha256((Project_root / 'build/kernel8.img').read_bytes()).hexdigest()
        (출력 / 'report.json').write_text(json.dumps(ulat_VALUE, ensure_ascii=False, indent=2) + '\n')
    assert ulat_VALUE['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(ulat_VALUE, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    run()
