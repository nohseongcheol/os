#!/usr/bin/env python3
"""개인 nasc_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from cianda_Socruithe import Ullmhaigh
from COSL배포 import sprioc_ainm, leabharlann

teilgean_fréamh = Path(__file__).resolve().parents[1]


def Rith_2():
    Aschur = teilgean_fréamh / 'build/verification/password-length'
    Aschur.mkdir(parents=True, exist_ok=True)
    socruithe_pearsanta = teilgean_fréamh / 'build/remote/access.json'
    원래설정 = socruithe_pearsanta.read_bytes()
    tuairisc_VALUE = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Socruithe_cosán = 시험터 / 'build/remote'
            Socruithe_cosán.mkdir(parents=True)
            Socruithe_comhad = Socruithe_cosán / 'access.json'
            def scríobh_Socruithe(sonraí):
                Socruithe_comhad.write_text(json.dumps(sonraí, ensure_ascii=False) + '\n')
                Socruithe_comhad.chmod(0o600)
            def fíoraigh_Socruithe(blaosc, 화면):
                scríobh_Socruithe({'user': 'user', 'ssh_password': blaosc, 'vnc_password': 화면})
                원본 = Socruithe_comhad.read_bytes()
                Ullmhaigh(시험터)
                assert Socruithe_comhad.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Socruithe_cosán / 'Próifíl.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Socruithe_cosán / 'Próifíl.h').stat().st_mode & 0o777 == 0o600
            for blaosc, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                fíoraigh_Socruithe(blaosc, 화면)
            tuairisc_VALUE['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for athraigh_VALUE, iontráil_VALUE in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                sonraí = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                sonraí.update(athraigh_VALUE)
                scríobh_Socruithe(sonraí)
                try:
                    Ullmhaigh(시험터)
                except SystemExit as ERREÁID:
                    assert iontráil_VALUE in str(ERREÁID), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + iontráil_VALUE)
            tuairisc_VALUE['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Socruithe = json.loads((teilgean_fréamh / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            nascóir = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Cartlann_uirlis = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def Rith_ordú(Argóintí, LOG_ró):
                subprocess.run(list(map(str, Argóintí)), cwd=str(teilgean_fréamh), stdout=LOG_ró,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Ainm, blaosc, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Ainm, flush=True)
                fíoraigh_Socruithe(blaosc, 화면)
                tomhas = Aschur / Ainm
                tomhas.mkdir(exist_ok=True)
                with (tomhas / 'build.log').open('wb') as LOG_ró:
                    목적들 = []
                    for 원본 in sorted((teilgean_fréamh / 'cianda_VALUE').glob('*.c')):
                        sprioc_VALUE = 시험터 / (원본.stem + '.o')
                        Rith_ordú([번역기] + Socruithe + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Socruithe_cosán, '-I', teilgean_fréamh / 'cianda_VALUE', '-I', teilgean_fréamh / 'vendor/libassh/src',
                             '-I', teilgean_fréamh / 'vendor/bearssl/inc', '-I', teilgean_fréamh / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', sprioc_VALUE], LOG_ró)
                        목적들.append(sprioc_VALUE)
                    cianda_beart = 시험터 / 'libremote.a'
                    Rith_ordú([Cartlann_uirlis, 'rcs', cianda_beart] + 목적들, LOG_ró)
                    Rith_ordú([nascóir, '--gc-sections', '-T', teilgean_fréamh / '부팅/Nasc_dáileadh.ld', '-o', 시험터 / 'kernel.elf'] +
                         [teilgean_fréamh / 'build' / (Ainm + '.o') for Ainm in sprioc_ainm] + ['--start-group'] +
                         [cianda_beart if CONAIR == 'remote/libremote.a' else teilgean_fréamh / 'build' / CONAIR for CONAIR in leabharlann] + ['--end-group'], LOG_ró)
                    Rith_ordú([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], LOG_ró)
                with (tomhas / 'remote-test.log').open('wb') as LOG_ró:
                    Rith_ordú(['python3', teilgean_fréamh / 'Uirlisí/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Socruithe_comhad, '--output', tomhas], LOG_ró)
                bailíochtaigh = json.loads((tomhas / 'report.json').read_text())
                assert bailíochtaigh['passed']
                tuairisc_VALUE['checks'].append(Ainm + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        tuairisc_VALUE['passed'] = True
    finally:
        tuairisc_VALUE['personal_settings_unchanged'] = socruithe_pearsanta.read_bytes() == 원래설정
        if not tuairisc_VALUE['personal_settings_unchanged']:
            tuairisc_VALUE['passed'] = False
        tuairisc_VALUE['kernel_sha256'] = hashlib.sha256((teilgean_fréamh / 'build/kernel8.img').read_bytes()).hexdigest()
        (Aschur / 'report.json').write_text(json.dumps(tuairisc_VALUE, ensure_ascii=False, indent=2) + '\n')
    assert tuairisc_VALUE['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(tuairisc_VALUE, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Rith_2()
