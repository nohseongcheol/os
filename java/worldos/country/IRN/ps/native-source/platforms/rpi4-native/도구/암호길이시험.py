#!/usr/bin/env python3
"""개인 پيوستون_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from 원격설정 import 준비
from COSL배포 import 목적이름, کتابتون

기준 = Path(__file__).resolve().parents[1]


def ځغلول():
    출력 = 기준 / 'build/verification/password-length'
    출력.mkdir(parents=True, exist_ok=True)
    ځاني_امستنې = 기준 / 'build/remote/access.json'
    원래설정 = ځاني_امستنې.read_bytes()
    راپور_ارزښت = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            설정경로 = 시험터 / 'build/remote'
            설정경로.mkdir(parents=True)
            설정파일 = 설정경로 / 'access.json'
            def 설정쓰기(اومتوک):
                설정파일.write_text(json.dumps(اومتوک, ensure_ascii=False) + '\n')
                설정파일.chmod(0o600)
            def 설정확인(سیپۍ, 화면):
                설정쓰기({'user': 'user', 'ssh_password': سیپۍ, 'vnc_password': 화면})
                원본 = 설정파일.read_bytes()
                준비(시험터)
                assert 설정파일.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (설정경로 / 'کارن_پېژنيال.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (설정경로 / 'کارن_پېژنيال.h').stat().st_mode & 0o777 == 0o600
            for سیپۍ, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                설정확인(سیپۍ, 화면)
            راپور_ارزښت['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for 변경, ننوت_ارزښت in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                اومتوک = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                اومتوک.update(변경)
                설정쓰기(اومتوک)
                try:
                    준비(시험터)
                except SystemExit as تېروتنه:
                    assert ننوت_ارزښت in str(تېروتنه), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + ننوت_ارزښت)
            راپور_ارزښت['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            امستنې = json.loads((기준 / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            연결기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            ارشیف_توکى = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def 실행(인수, خبرال_کیل):
                subprocess.run(list(map(str, 인수)), cwd=str(기준), stdout=خبرال_کیل,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for نوم, سیپۍ, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + نوم, flush=True)
                설정확인(سیپۍ, 화면)
                결과 = 출력 / نوم
                결과.mkdir(exist_ok=True)
                with (결과 / 'build.log').open('wb') as خبرال_کیل:
                    목적들 = []
                    for 원본 in sorted((기준 / '원격').glob('*.c')):
                        موخه_ارزښت = 시험터 / (원본.stem + '.o')
                        실행([번역기] + امستنې + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', 설정경로, '-I', 기준 / '원격', '-I', 기준 / 'vendor/libassh/src',
                             '-I', 기준 / 'vendor/bearssl/inc', '-I', 기준 / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', موخه_ارزښت], خبرال_کیل)
                        목적들.append(موخه_ارزښت)
                    원격묶음 = 시험터 / 'libremote.a'
                    실행([ارشیف_توکى, 'rcs', 원격묶음] + 목적들, خبرال_کیل)
                    실행([연결기, '--gc-sections', '-T', 기준 / '부팅/پيوند_هډوانه.ld', '-o', 시험터 / 'kernel.elf'] +
                         [기준 / 'build' / (نوم + '.o') for نوم in 목적이름] + ['--start-group'] +
                         [원격묶음 if يونلور == 'remote/libremote.a' else 기준 / 'build' / يونلور for يونلور in کتابتون] + ['--end-group'], خبرال_کیل)
                    실행([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], خبرال_کیل)
                with (결과 / 'remote-test.log').open('wb') as خبرال_کیل:
                    실행(['python3', 기준 / '도구/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', 설정파일, '--output', 결과], خبرال_کیل)
                검증 = json.loads((결과 / 'report.json').read_text())
                assert 검증['passed']
                راپور_ارزښت['checks'].append(نوم + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        راپور_ارزښت['passed'] = True
    finally:
        راپور_ارزښت['personal_settings_unchanged'] = ځاني_امستنې.read_bytes() == 원래설정
        if not راپور_ارزښت['personal_settings_unchanged']:
            راپور_ارزښت['passed'] = False
        راپور_ارزښت['kernel_sha256'] = hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()
        (출력 / 'report.json').write_text(json.dumps(راپور_ارزښت, ensure_ascii=False, indent=2) + '\n')
    assert راپور_ارزښت['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(راپور_ارزښت, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    ځغلول()
