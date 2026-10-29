#!/usr/bin/env python3
"""개인 kgokaganya_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from ya_kgole_Dipeakanyo import Lokišetša
from COSL배포 import boyo_leina, Bokgobadata

기준 = Path(__file__).resolve().parents[1]


def Diriša():
    출력 = 기준 / 'build/verification/password-length'
    출력.mkdir(parents=True, exist_ok=True)
    boitšhupo_bja_moswananoši_bja_khomphutha = 기준 / 'build/remote/access.json'
    원래설정 = boitšhupo_bja_moswananoši_bja_khomphutha.read_bytes()
    pego_boleng = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            Dipeakanyo_tsela = 시험터 / 'build/remote'
            Dipeakanyo_tsela.mkdir(parents=True)
            Dipeakanyo_faele = Dipeakanyo_tsela / 'access.json'
            def ngwala_Dipeakanyo(data):
                Dipeakanyo_faele.write_text(json.dumps(data, ensure_ascii=False) + '\n')
                Dipeakanyo_faele.chmod(0o600)
            def kgonthiša_Dipeakanyo(šele, 화면):
                ngwala_Dipeakanyo({'user': 'user', 'ssh_password': šele, 'vnc_password': 화면})
                원본 = Dipeakanyo_faele.read_bytes()
                Lokišetša(시험터)
                assert Dipeakanyo_faele.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (Dipeakanyo_tsela / 'Profaele.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (Dipeakanyo_tsela / 'Profaele.h').stat().st_mode & 0o777 == 0o600
            for šele, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                kgonthiša_Dipeakanyo(šele, 화면)
            pego_boleng['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for fetoša_boleng, go_tsenya_tshedimošo_boleng in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                data = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                data.update(fetoša_boleng)
                ngwala_Dipeakanyo(data)
                try:
                    Lokišetša(시험터)
                except SystemExit as Phošo:
                    assert go_tsenya_tshedimošo_boleng in str(Phošo), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + go_tsenya_tshedimošo_boleng)
            pego_boleng['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            Dipeakanyo = json.loads((기준 / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            sekgokaganyi = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            Akhaebe_tholosi = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def phethagatša_taelo(인수, pego_rei):
                subprocess.run(list(map(str, 인수)), cwd=str(기준), stdout=pego_rei,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for Leina, šele, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + Leina, flush=True)
                kgonthiša_Dipeakanyo(šele, 화면)
                결과 = 출력 / Leina
                결과.mkdir(exist_ok=True)
                with (결과 / 'build.log').open('wb') as pego_rei:
                    목적들 = []
                    for 원본 in sorted((기준 / 'ya_kgole_boleng').glob('*.c')):
                        boyo_boleng = 시험터 / (원본.stem + '.o')
                        phethagatša_taelo([번역기] + Dipeakanyo + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', Dipeakanyo_tsela, '-I', 기준 / 'ya_kgole_boleng', '-I', 기준 / 'vendor/libassh/src',
                             '-I', 기준 / 'vendor/bearssl/inc', '-I', 기준 / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', boyo_boleng], pego_rei)
                        목적들.append(boyo_boleng)
                    ya_kgole_sehlopha = 시험터 / 'libremote.a'
                    phethagatša_taelo([Akhaebe_tholosi, 'rcs', ya_kgole_sehlopha] + 목적들, pego_rei)
                    phethagatša_taelo([sekgokaganyi, '--gc-sections', '-T', 기준 / '부팅/linke_Sebopego.ld', '-o', 시험터 / 'kernel.elf'] +
                         [기준 / 'build' / (Leina + '.o') for Leina in boyo_leina] + ['--start-group'] +
                         [ya_kgole_sehlopha if Tsejana == 'remote/libremote.a' else 기준 / 'build' / Tsejana for Tsejana in Bokgobadata] + ['--end-group'], pego_rei)
                    phethagatša_taelo([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], pego_rei)
                with (결과 / 'remote-test.log').open('wb') as pego_rei:
                    phethagatša_taelo(['python3', 기준 / 'Ditholosi/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', Dipeakanyo_faele, '--output', 결과], pego_rei)
                kgonthiša_5fb2b747 = json.loads((결과 / 'report.json').read_text())
                assert kgonthiša_5fb2b747['passed']
                pego_boleng['checks'].append(Leina + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        pego_boleng['passed'] = True
    finally:
        pego_boleng['personal_settings_unchanged'] = boitšhupo_bja_moswananoši_bja_khomphutha.read_bytes() == 원래설정
        if not pego_boleng['personal_settings_unchanged']:
            pego_boleng['passed'] = False
        pego_boleng['kernel_sha256'] = hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()
        (출력 / 'report.json').write_text(json.dumps(pego_boleng, ensure_ascii=False, indent=2) + '\n')
    assert pego_boleng['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(pego_boleng, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Diriša()
