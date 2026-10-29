#!/usr/bin/env python3
"""개인 ᎫᏓᎸᎢ_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from 원격설정 import ᎭᏛᏅᎢᏍᏓ
from COSL배포 import ᏮᎦᏛᎢ_ᏚᏙᎥᎢ, ᏧᏂᎪᎵᏰᏗᎢ

기준 = Path(__file__).resolve().parents[1]


def ᎠᎢᏎᏍᏗ():
    출력 = 기준 / 'build/verification/password-length'
    출력.mkdir(parents=True, exist_ok=True)
    ᎠᏏᏴᏫ_ᏕᎦᎧᎲᎢ = 기준 / 'build/remote/access.json'
    원래설정 = ᎠᏏᏴᏫ_ᏕᎦᎧᎲᎢ.read_bytes()
    ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            ᎠᏓᎪᎵᏰᏍᎩ_ᏗᎦᎸᏫᏍᏓᏁᎢ_ᎢᎬᎾᏕ = Path(임시)
            ᏕᎦᎧᎲᎢ_ᎠᏍᏓᏩᏛᏍᏗ = ᎠᏓᎪᎵᏰᏍᎩ_ᏗᎦᎸᏫᏍᏓᏁᎢ_ᎢᎬᎾᏕ / 'build/remote'
            ᏕᎦᎧᎲᎢ_ᎠᏍᏓᏩᏛᏍᏗ.mkdir(parents=True)
            ᏕᎦᎧᎲᎢ_ᎠᏍᏆᏂᎪᏙᏗ = ᏕᎦᎧᎲᎢ_ᎠᏍᏓᏩᏛᏍᏗ / 'access.json'
            def ᎪᏪᎶᏗ_ᏕᎦᎧᎲᎢ(ᎦᏟᏌᏅᎯ):
                ᏕᎦᎧᎲᎢ_ᎠᏍᏆᏂᎪᏙᏗ.write_text(json.dumps(ᎦᏟᏌᏅᎯ, ensure_ascii=False) + '\n')
                ᏕᎦᎧᎲᎢ_ᎠᏍᏆᏂᎪᏙᏗ.chmod(0o600)
            def ᎰᎯᏳᏓ_ᏕᎦᎧᎲᎢ(ᎤᏯᏍᎦ, 화면):
                ᎪᏪᎶᏗ_ᏕᎦᎧᎲᎢ({'user': 'user', 'ssh_password': ᎤᏯᏍᎦ, 'vnc_password': 화면})
                원본 = ᏕᎦᎧᎲᎢ_ᎠᏍᏆᏂᎪᏙᏗ.read_bytes()
                ᎭᏛᏅᎢᏍᏓ(ᎠᏓᎪᎵᏰᏍᎩ_ᏗᎦᎸᏫᏍᏓᏁᎢ_ᎢᎬᎾᏕ)
                assert ᏕᎦᎧᎲᎢ_ᎠᏍᏆᏂᎪᏙᏗ.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (ᏕᎦᎧᎲᎢ_ᎠᏍᏓᏩᏛᏍᏗ / 'ᎬᏗᏍᎩ_ᏄᏍᏗᏓᏅᎢ.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (ᏕᎦᎧᎲᎢ_ᎠᏍᏓᏩᏛᏍᏗ / 'ᎬᏗᏍᎩ_ᏄᏍᏗᏓᏅᎢ.h').stat().st_mode & 0o777 == 0o600
            for ᎤᏯᏍᎦ, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                ᎰᎯᏳᏓ_ᏕᎦᎧᎲᎢ(ᎤᏯᏍᎦ, 화면)
            ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for ᎯᏁᏟᏴᎾ_ᏧᎬᏩᎶᏗᏯ, Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                ᎦᏟᏌᏅᎯ = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                ᎦᏟᏌᏅᎯ.update(ᎯᏁᏟᏴᎾ_ᏧᎬᏩᎶᏗᏯ)
                ᎪᏪᎶᏗ_ᏕᎦᎧᎲᎢ(ᎦᏟᏌᏅᎯ)
                try:
                    ᎭᏛᏅᎢᏍᏓ(ᎠᏓᎪᎵᏰᏍᎩ_ᏗᎦᎸᏫᏍᏓᏁᎢ_ᎢᎬᎾᏕ)
                except SystemExit as ᎦᎵᏓᏍᏔᏅ:
                    assert Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ in str(ᎦᎵᏓᏍᏔᏅ), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ)
            ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            ᏕᎦᎧᎲᎢ = json.loads((기준 / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            ᎫᏓᎸᏙᏗ = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            ᎠᏍᏆᏂᎪᏛᎢ_ᎬᏔᏂᏓᏍᏗ = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(인수, ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ):
                subprocess.run(list(map(str, 인수)), cwd=str(기준), stdout=ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for ᏚᏙᎥᎢ, ᎤᏯᏍᎦ, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + ᏚᏙᎥᎢ, flush=True)
                ᎰᎯᏳᏓ_ᏕᎦᎧᎲᎢ(ᎤᏯᏍᎦ, 화면)
                결과 = 출력 / ᏚᏙᎥᎢ
                결과.mkdir(exist_ok=True)
                with (결과 / 'build.log').open('wb') as ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ:
                    목적들 = []
                    for 원본 in sorted((기준 / '원격').glob('*.c')):
                        ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ = ᎠᏓᎪᎵᏰᏍᎩ_ᏗᎦᎸᏫᏍᏓᏁᎢ_ᎢᎬᎾᏕ / (원본.stem + '.o')
                        ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ([번역기] + ᏕᎦᎧᎲᎢ + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', ᏕᎦᎧᎲᎢ_ᎠᏍᏓᏩᏛᏍᏗ, '-I', 기준 / '원격', '-I', 기준 / 'vendor/libassh/src',
                             '-I', 기준 / 'vendor/bearssl/inc', '-I', 기준 / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ], ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ)
                        목적들.append(ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ)
                    원격묶음 = ᎠᏓᎪᎵᏰᏍᎩ_ᏗᎦᎸᏫᏍᏓᏁᎢ_ᎢᎬᎾᏕ / 'libremote.a'
                    ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ([ᎠᏍᏆᏂᎪᏛᎢ_ᎬᏔᏂᏓᏍᏗ, 'rcs', 원격묶음] + 목적들, ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ)
                    ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ([ᎫᏓᎸᏙᏗ, '--gc-sections', '-T', 기준 / '부팅/ᎫᏓᎸᎢ_ᏱᎬᏂ.ld', '-o', ᎠᏓᎪᎵᏰᏍᎩ_ᏗᎦᎸᏫᏍᏓᏁᎢ_ᎢᎬᎾᏕ / 'kernel.elf'] +
                         [기준 / 'build' / (ᏚᏙᎥᎢ + '.o') for ᏚᏙᎥᎢ in ᏮᎦᏛᎢ_ᏚᏙᎥᎢ] + ['--start-group'] +
                         [원격묶음 if ᎠᏍᏓᏩᏛᏍᏗ == 'remote/libremote.a' else 기준 / 'build' / ᎠᏍᏓᏩᏛᏍᏗ for ᎠᏍᏓᏩᏛᏍᏗ in ᏧᏂᎪᎵᏰᏗᎢ] + ['--end-group'], ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ)
                    ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         ᎠᏓᎪᎵᏰᏍᎩ_ᏗᎦᎸᏫᏍᏓᏁᎢ_ᎢᎬᎾᏕ / 'kernel.elf', ᎠᏓᎪᎵᏰᏍᎩ_ᏗᎦᎸᏫᏍᏓᏁᎢ_ᎢᎬᎾᏕ / 'kernel8.img'], ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ)
                with (결과 / 'remote-test.log').open('wb') as ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ:
                    ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(['python3', 기준 / '도구/원격접속시험.py', '--kernel', ᎠᏓᎪᎵᏰᏍᎩ_ᏗᎦᎸᏫᏍᏓᏁᎢ_ᎢᎬᎾᏕ / 'kernel8.img',
                         '--access', ᏕᎦᎧᎲᎢ_ᎠᏍᏆᏂᎪᏙᏗ, '--output', 결과], ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ)
                ᎪᎯᏳᏙᏗ = json.loads((결과 / 'report.json').read_text())
                assert ᎪᎯᏳᏙᏗ['passed']
                ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['checks'].append(ᏚᏙᎥᎢ + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['passed'] = True
    finally:
        ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['personal_settings_unchanged'] = ᎠᏏᏴᏫ_ᏕᎦᎧᎲᎢ.read_bytes() == 원래설정
        if not ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['personal_settings_unchanged']:
            ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['passed'] = False
        ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['kernel_sha256'] = hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()
        (출력 / 'report.json').write_text(json.dumps(ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ, ensure_ascii=False, indent=2) + '\n')
    assert ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(ᎬᏂᎨᏒᎢᎬᏁᏗ_ᏧᎬᏩᎶᏗᏯ, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    ᎠᎢᏎᏍᏗ()
