#!/usr/bin/env python3
"""개인 ceangal_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from cian_roghainnean import Ullaich
from COSL배포 import ceann_uidhe_ainm, leabhar_lann

tilg_freumh = Path(__file__).resolve().parents[1]


def ruith():
    출력 = tilg_freumh / 'build/verification/password-length'
    출력.mkdir(parents=True, exist_ok=True)
    roghainnean_pearsanta = tilg_freumh / 'build/remote/access.json'
    원래설정 = roghainnean_pearsanta.read_bytes()
    aithisg_VALUE = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            roghainnean_slighe = 시험터 / 'build/remote'
            roghainnean_slighe.mkdir(parents=True)
            roghainnean_faidhle = roghainnean_slighe / 'access.json'
            def sgrìobh_roghainnean(dàta):
                roghainnean_faidhle.write_text(json.dumps(dàta, ensure_ascii=False) + '\n')
                roghainnean_faidhle.chmod(0o600)
            def dearbh_roghainnean(slige, 화면):
                sgrìobh_roghainnean({'user': 'user', 'ssh_password': slige, 'vnc_password': 화면})
                원본 = roghainnean_faidhle.read_bytes()
                Ullaich(시험터)
                assert roghainnean_faidhle.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (roghainnean_slighe / 'Pròifil.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (roghainnean_slighe / 'Pròifil.h').stat().st_mode & 0o777 == 0o600
            for slige, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                dearbh_roghainnean(slige, 화면)
            aithisg_VALUE['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for atharraich_VALUE, cur_a_steach_VALUE in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                dàta = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                dàta.update(atharraich_VALUE)
                sgrìobh_roghainnean(dàta)
                try:
                    Ullaich(시험터)
                except SystemExit as Mearachd:
                    assert cur_a_steach_VALUE in str(Mearachd), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + cur_a_steach_VALUE)
            aithisg_VALUE['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            roghainnean = json.loads((tilg_freumh / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            ceanglaiche = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            taisg_inneal = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def gnìomhaich_àithne(인수, LOG_ràgh):
                subprocess.run(list(map(str, 인수)), cwd=str(tilg_freumh), stdout=LOG_ràgh,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Ainm, slige, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Ainm, flush=True)
                dearbh_roghainnean(slige, 화면)
                tomhas = 출력 / Ainm
                tomhas.mkdir(exist_ok=True)
                with (tomhas / 'build.log').open('wb') as LOG_ràgh:
                    목적들 = []
                    for 원본 in sorted((tilg_freumh / 'cian_VALUE').glob('*.c')):
                        ceann_uidhe_VALUE = 시험터 / (원본.stem + '.o')
                        gnìomhaich_àithne([번역기] + roghainnean + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', roghainnean_slighe, '-I', tilg_freumh / 'cian_VALUE', '-I', tilg_freumh / 'vendor/libassh/src',
                             '-I', tilg_freumh / 'vendor/bearssl/inc', '-I', tilg_freumh / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', ceann_uidhe_VALUE], LOG_ràgh)
                        목적들.append(ceann_uidhe_VALUE)
                    cian_trusgan = 시험터 / 'libremote.a'
                    gnìomhaich_àithne([taisg_inneal, 'rcs', cian_trusgan] + 목적들, LOG_ràgh)
                    gnìomhaich_àithne([ceanglaiche, '--gc-sections', '-T', tilg_freumh / '부팅/ceangal_co_dhealbhachd.ld', '-o', 시험터 / 'kernel.elf'] +
                         [tilg_freumh / 'build' / (Ainm + '.o') for Ainm in ceann_uidhe_ainm] + ['--start-group'] +
                         [cian_trusgan if Slighe == 'remote/libremote.a' else tilg_freumh / 'build' / Slighe for Slighe in leabhar_lann] + ['--end-group'], LOG_ràgh)
                    gnìomhaich_àithne([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], LOG_ràgh)
                with (tomhas / 'remote-test.log').open('wb') as LOG_ràgh:
                    gnìomhaich_àithne(['python3', tilg_freumh / 'innealan/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', roghainnean_faidhle, '--output', tomhas], LOG_ràgh)
                dearbh_5fb2b747 = json.loads((tomhas / 'report.json').read_text())
                assert dearbh_5fb2b747['passed']
                aithisg_VALUE['checks'].append(Ainm + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        aithisg_VALUE['passed'] = True
    finally:
        aithisg_VALUE['personal_settings_unchanged'] = roghainnean_pearsanta.read_bytes() == 원래설정
        if not aithisg_VALUE['personal_settings_unchanged']:
            aithisg_VALUE['passed'] = False
        aithisg_VALUE['kernel_sha256'] = hashlib.sha256((tilg_freumh / 'build/kernel8.img').read_bytes()).hexdigest()
        (출력 / 'report.json').write_text(json.dumps(aithisg_VALUE, ensure_ascii=False, indent=2) + '\n')
    assert aithisg_VALUE['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(aithisg_VALUE, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    ruith()
