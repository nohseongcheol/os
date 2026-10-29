#!/usr/bin/env python3
"""개인 ڪنيڪشن_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from بعيد_سيٽنگون import تياري_ڪريو
from COSL배포 import منزل_مقصود_نالو, لائبريري

기준 = Path(__file__).resolve().parents[1]


def هلائڻ():
    출력 = 기준 / 'build/verification/password-length'
    출력.mkdir(parents=True, exist_ok=True)
    ذاتي_سيٽنگس = 기준 / 'build/remote/access.json'
    원래설정 = ذاتي_سيٽنگس.read_bytes()
    رپورٽ_قدر = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            سيٽنگون_راههه = 시험터 / 'build/remote'
            سيٽنگون_راههه.mkdir(parents=True)
            سيٽنگون_فائل = سيٽنگون_راههه / 'access.json'
            def لکو_سيٽنگون(ڪوائف):
                سيٽنگون_فائل.write_text(json.dumps(ڪوائف, ensure_ascii=False) + '\n')
                سيٽنگون_فائل.chmod(0o600)
            def تصديق_ڪريو_سيٽنگون(شيل, 화면):
                لکو_سيٽنگون({'user': 'user', 'ssh_password': شيل, 'vnc_password': 화면})
                원본 = سيٽنگون_فائل.read_bytes()
                تياري_ڪريو(시험터)
                assert سيٽنگون_فائل.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (سيٽنگون_راههه / 'پروفائيل.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (سيٽنگون_راههه / 'پروفائيل.h').stat().st_mode & 0o777 == 0o600
            for شيل, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                تصديق_ڪريو_سيٽنگون(شيل, 화면)
            رپورٽ_قدر['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for تبديل_ڪريو_قدر, داخلا_قدر in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                ڪوائف = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                ڪوائف.update(تبديل_ڪريو_قدر)
                لکو_سيٽنگون(ڪوائف)
                try:
                    تياري_ڪريو(시험터)
                except SystemExit as نقص:
                    assert داخلا_قدر in str(نقص), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + داخلا_قدر)
            رپورٽ_قدر['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            سيٽنگون = json.loads((기준 / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            ڪنڪٽر = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            محفوظ_ٽول = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def تعميل_ڪرڻ_حڪم(인수, لاگ_صف):
                subprocess.run(list(map(str, 인수)), cwd=str(기준), stdout=لاگ_صف,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for نالو, شيل, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + نالو, flush=True)
                تصديق_ڪريو_سيٽنگون(شيل, 화면)
                결과 = 출력 / نالو
                결과.mkdir(exist_ok=True)
                with (결과 / 'build.log').open('wb') as لاگ_صف:
                    목적들 = []
                    for 원본 in sorted((기준 / 'بعيد_قدر').glob('*.c')):
                        منزل_مقصود_قدر = 시험터 / (원본.stem + '.o')
                        تعميل_ڪرڻ_حڪم([번역기] + سيٽنگون + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', سيٽنگون_راههه, '-I', 기준 / 'بعيد_قدر', '-I', 기준 / 'vendor/libassh/src',
                             '-I', 기준 / 'vendor/bearssl/inc', '-I', 기준 / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', منزل_مقصود_قدر], لاگ_صف)
                        목적들.append(منزل_مقصود_قدر)
                    بعيد_بنڊل = 시험터 / 'libremote.a'
                    تعميل_ڪرڻ_حڪم([محفوظ_ٽول, 'rcs', بعيد_بنڊل] + 목적들, لاگ_صف)
                    تعميل_ڪرڻ_حڪم([ڪنڪٽر, '--gc-sections', '-T', 기준 / '부팅/ڪڙي_لي_آئوٽ.ld', '-o', 시험터 / 'kernel.elf'] +
                         [기준 / 'build' / (نالو + '.o') for نالو in منزل_مقصود_نالو] + ['--start-group'] +
                         [بعيد_بنڊل if راههه == 'remote/libremote.a' else 기준 / 'build' / راههه for راههه in لائبريري] + ['--end-group'], لاگ_صف)
                    تعميل_ڪرڻ_حڪم([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], لاگ_صف)
                with (결과 / 'remote-test.log').open('wb') as لاگ_صف:
                    تعميل_ڪرڻ_حڪم(['python3', 기준 / 'اوزار/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', سيٽنگون_فائل, '--output', 결과], لاگ_صف)
                ڪارگر_ڪريو = json.loads((결과 / 'report.json').read_text())
                assert ڪارگر_ڪريو['passed']
                رپورٽ_قدر['checks'].append(نالو + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        رپورٽ_قدر['passed'] = True
    finally:
        رپورٽ_قدر['personal_settings_unchanged'] = ذاتي_سيٽنگس.read_bytes() == 원래설정
        if not رپورٽ_قدر['personal_settings_unchanged']:
            رپورٽ_قدر['passed'] = False
        رپورٽ_قدر['kernel_sha256'] = hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()
        (출력 / 'report.json').write_text(json.dumps(رپورٽ_قدر, ensure_ascii=False, indent=2) + '\n')
    assert رپورٽ_قدر['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(رپورٽ_قدر, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    هلائڻ()
