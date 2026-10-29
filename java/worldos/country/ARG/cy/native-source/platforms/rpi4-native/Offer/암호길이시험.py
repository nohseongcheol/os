#!/usr/bin/env python3
"""개인 cyswllt_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from pell_Gosodiadau import Paratoi
from COSL배포 import cyrchfan_enw, llyfrgell

prosiect_gwraidd = Path(__file__).resolve().parents[1]


def Gweithredu_2():
    Allbwn = prosiect_gwraidd / 'build/verification/password-length'
    Allbwn.mkdir(parents=True, exist_ok=True)
    gosodiadau_personol = prosiect_gwraidd / 'build/remote/access.json'
    원래설정 = gosodiadau_personol.read_bytes()
    adrodd_VALUE = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Gosodiadau_llwybr = 시험터 / 'build/remote'
            Gosodiadau_llwybr.mkdir(parents=True)
            Gosodiadau_ffeil = Gosodiadau_llwybr / 'access.json'
            def ysgrifennu_Gosodiadau(data):
                Gosodiadau_ffeil.write_text(json.dumps(data, ensure_ascii=False) + '\n')
                Gosodiadau_ffeil.chmod(0o600)
            def dilysu_Gosodiadau(cragen, 화면):
                ysgrifennu_Gosodiadau({'user': 'user', 'ssh_password': cragen, 'vnc_password': 화면})
                원본 = Gosodiadau_ffeil.read_bytes()
                Paratoi(시험터)
                assert Gosodiadau_ffeil.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Gosodiadau_llwybr / 'Proffil.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Gosodiadau_llwybr / 'Proffil.h').stat().st_mode & 0o777 == 0o600
            for cragen, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                dilysu_Gosodiadau(cragen, 화면)
            adrodd_VALUE['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for newid_VALUE, cofnod_VALUE in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                data = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                data.update(newid_VALUE)
                ysgrifennu_Gosodiadau(data)
                try:
                    Paratoi(시험터)
                except SystemExit as Gwall:
                    assert cofnod_VALUE in str(Gwall), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + cofnod_VALUE)
            adrodd_VALUE['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Gosodiadau = json.loads((prosiect_gwraidd / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            cysylltydd = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Archif_offeryn = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def Gweithredu_gorchymyn(인수, LOG_rhes):
                subprocess.run(list(map(str, 인수)), cwd=str(prosiect_gwraidd), stdout=LOG_rhes,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Enw, cragen, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Enw, flush=True)
                dilysu_Gosodiadau(cragen, 화면)
                mesur = Allbwn / Enw
                mesur.mkdir(exist_ok=True)
                with (mesur / 'build.log').open('wb') as LOG_rhes:
                    목적들 = []
                    for 원본 in sorted((prosiect_gwraidd / 'pell_VALUE').glob('*.c')):
                        cyrchfan_VALUE = 시험터 / (원본.stem + '.o')
                        Gweithredu_gorchymyn([번역기] + Gosodiadau + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Gosodiadau_llwybr, '-I', prosiect_gwraidd / 'pell_VALUE', '-I', prosiect_gwraidd / 'vendor/libassh/src',
                             '-I', prosiect_gwraidd / 'vendor/bearssl/inc', '-I', prosiect_gwraidd / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', cyrchfan_VALUE], LOG_rhes)
                        목적들.append(cyrchfan_VALUE)
                    pell_bwndel = 시험터 / 'libremote.a'
                    Gweithredu_gorchymyn([Archif_offeryn, 'rcs', pell_bwndel] + 목적들, LOG_rhes)
                    Gweithredu_gorchymyn([cysylltydd, '--gc-sections', '-T', prosiect_gwraidd / '부팅/Dolen_Llywio.ld', '-o', 시험터 / 'kernel.elf'] +
                         [prosiect_gwraidd / 'build' / (Enw + '.o') for Enw in cyrchfan_enw] + ['--start-group'] +
                         [pell_bwndel if LLWYBR == 'remote/libremote.a' else prosiect_gwraidd / 'build' / LLWYBR for LLWYBR in llyfrgell] + ['--end-group'], LOG_rhes)
                    Gweithredu_gorchymyn([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], LOG_rhes)
                with (mesur / 'remote-test.log').open('wb') as LOG_rhes:
                    Gweithredu_gorchymyn(['python3', prosiect_gwraidd / 'Offer/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Gosodiadau_ffeil, '--output', mesur], LOG_rhes)
                dilysu_5fb2b747 = json.loads((mesur / 'report.json').read_text())
                assert dilysu_5fb2b747['passed']
                adrodd_VALUE['checks'].append(Enw + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        adrodd_VALUE['passed'] = True
    finally:
        adrodd_VALUE['personal_settings_unchanged'] = gosodiadau_personol.read_bytes() == 원래설정
        if not adrodd_VALUE['personal_settings_unchanged']:
            adrodd_VALUE['passed'] = False
        adrodd_VALUE['kernel_sha256'] = hashlib.sha256((prosiect_gwraidd / 'build/kernel8.img').read_bytes()).hexdigest()
        (Allbwn / 'report.json').write_text(json.dumps(adrodd_VALUE, ensure_ascii=False, indent=2) + '\n')
    assert adrodd_VALUE['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(adrodd_VALUE, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Gweithredu_2()
