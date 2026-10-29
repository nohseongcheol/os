#!/usr/bin/env python3
"""개인 접속 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from 원격설정 import 준비
from COSL배포 import 목적이름, 라이브러리

기준 = Path(__file__).resolve().parents[1]


def 시작():
    출력 = 기준 / 'build/verification/password-length'
    출력.mkdir(parents=True, exist_ok=True)
    개인설정 = 기준 / 'build/remote/access.json'
    원래설정 = 개인설정.read_bytes()
    보고 = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            설정경로 = 시험터 / 'build/remote'
            설정경로.mkdir(parents=True)
            설정파일 = 설정경로 / 'access.json'
            def 설정쓰기(자료):
                설정파일.write_text(json.dumps(자료, ensure_ascii=False) + '\n')
                설정파일.chmod(0o600)
            def 설정확인(셸, 화면):
                설정쓰기({'user': 'user', 'ssh_password': 셸, 'vnc_password': 화면})
                원본 = 설정파일.read_bytes()
                준비(시험터)
                assert 설정파일.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (설정경로 / '접속설정.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (설정경로 / '접속설정.h').stat().st_mode & 0o777 == 0o600
            for 셸, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                설정확인(셸, 화면)
            보고['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for 변경, 항목 in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                자료 = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                자료.update(변경)
                설정쓰기(자료)
                try:
                    준비(시험터)
                except SystemExit as טעות:
                    assert 항목 in str(טעות), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + 항목)
            보고['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            설정 = json.loads((기준 / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            연결기 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            묶음도구 = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def 실행(인수, 기록):
                subprocess.run(list(map(str, 인수)), cwd=str(기준), stdout=기록,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for נאָמען, 셸, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + נאָמען, flush=True)
                설정확인(셸, 화면)
                결과 = 출력 / נאָמען
                결과.mkdir(exist_ok=True)
                with (결과 / 'build.log').open('wb') as 기록:
                    목적들 = []
                    for 원본 in sorted((기준 / '원격').glob('*.c')):
                        목적 = 시험터 / (원본.stem + '.o')
                        실행([번역기] + 설정 + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', 설정경로, '-I', 기준 / '원격', '-I', 기준 / 'vendor/libassh/src',
                             '-I', 기준 / 'vendor/bearssl/inc', '-I', 기준 / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', 목적], 기록)
                        목적들.append(목적)
                    원격묶음 = 시험터 / 'libremote.a'
                    실행([묶음도구, 'rcs', 원격묶음] + 목적들, 기록)
                    실행([연결기, '--gc-sections', '-T', 기준 / '부팅/배치.ld', '-o', 시험터 / 'kernel.elf'] +
                         [기준 / 'build' / (נאָמען + '.o') for נאָמען in 목적이름] + ['--start-group'] +
                         [원격묶음 if 경로 == 'remote/libremote.a' else 기준 / 'build' / 경로 for 경로 in 라이브러리] + ['--end-group'], 기록)
                    실행([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], 기록)
                with (결과 / 'remote-test.log').open('wb') as 기록:
                    실행(['python3', 기준 / '도구/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', 설정파일, '--output', 결과], 기록)
                검증 = json.loads((결과 / 'report.json').read_text())
                assert 검증['passed']
                보고['checks'].append(נאָמען + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        보고['passed'] = True
    finally:
        보고['personal_settings_unchanged'] = 개인설정.read_bytes() == 원래설정
        if not 보고['personal_settings_unchanged']:
            보고['passed'] = False
        보고['kernel_sha256'] = hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()
        (출력 / 'report.json').write_text(json.dumps(보고, ensure_ascii=False, indent=2) + '\n')
    assert 보고['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(보고, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    시작()
