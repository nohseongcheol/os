#!/usr/bin/env python3
"""개인 کنکشن_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from بعيد_سیٹنگاں import تیاری_کرو
from COSL배포 import منزل_مقصود_ناں, لائبریری

기준 = Path(__file__).resolve().parents[1]


def چلاؤ():
    출력 = 기준 / 'build/verification/password-length'
    출력.mkdir(parents=True, exist_ok=True)
    ذاتی_سیٹنگیں = 기준 / 'build/remote/access.json'
    원래설정 = ذاتی_سیٹنگیں.read_bytes()
    رپورٹ_قدر = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            سیٹنگاں_راہ = 시험터 / 'build/remote'
            سیٹنگاں_راہ.mkdir(parents=True)
            سیٹنگاں_فائل = سیٹنگاں_راہ / 'access.json'
            def لکھو_سیٹنگاں(کوائف):
                سیٹنگاں_فائل.write_text(json.dumps(کوائف, ensure_ascii=False) + '\n')
                سیٹنگاں_فائل.chmod(0o600)
            def تصدیق_کرو_سیٹنگاں(شیل, 화면):
                لکھو_سیٹنگاں({'user': 'user', 'ssh_password': شیل, 'vnc_password': 화면})
                원본 = سیٹنگاں_فائل.read_bytes()
                تیاری_کرو(시험터)
                assert سیٹنگاں_فائل.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (سیٹنگاں_راہ / 'پروفائل.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (سیٹنگاں_راہ / 'پروفائل.h').stat().st_mode & 0o777 == 0o600
            for شیل, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                تصدیق_کرو_سیٹنگاں(شیل, 화면)
            رپورٹ_قدر['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for تبدیل_کرو_قدر, داخلہ_قدر in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                کوائف = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                کوائف.update(تبدیل_کرو_قدر)
                لکھو_سیٹنگاں(کوائف)
                try:
                    تیاری_کرو(시험터)
                except SystemExit as نقص:
                    assert داخلہ_قدر in str(نقص), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + داخلہ_قدر)
            رپورٹ_قدر['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            سیٹنگاں = json.loads((기준 / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            کنکٹر = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            محفوظہ_ٹول = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def نفاذ_کرو_حکم(인수, لاگ_صف):
                subprocess.run(list(map(str, 인수)), cwd=str(기준), stdout=لاگ_صف,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for ناں, شیل, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + ناں, flush=True)
                تصدیق_کرو_سیٹنگاں(شیل, 화면)
                결과 = 출력 / ناں
                결과.mkdir(exist_ok=True)
                with (결과 / 'build.log').open('wb') as لاگ_صف:
                    목적들 = []
                    for 원본 in sorted((기준 / 'بعيد_قدر').glob('*.c')):
                        منزل_مقصود_قدر = 시험터 / (원본.stem + '.o')
                        نفاذ_کرو_حکم([번역기] + سیٹنگاں + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', سیٹنگاں_راہ, '-I', 기준 / 'بعيد_قدر', '-I', 기준 / 'vendor/libassh/src',
                             '-I', 기준 / 'vendor/bearssl/inc', '-I', 기준 / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', منزل_مقصود_قدر], لاگ_صف)
                        목적들.append(منزل_مقصود_قدر)
                    بعيد_گٹھ = 시험터 / 'libremote.a'
                    نفاذ_کرو_حکم([محفوظہ_ٹول, 'rcs', بعيد_گٹھ] + 목적들, لاگ_صف)
                    نفاذ_کرو_حکم([کنکٹر, '--gc-sections', '-T', 기준 / '부팅/ربط_لے_آؤٹ.ld', '-o', 시험터 / 'kernel.elf'] +
                         [기준 / 'build' / (ناں + '.o') for ناں in منزل_مقصود_ناں] + ['--start-group'] +
                         [بعيد_گٹھ if راہ == 'remote/libremote.a' else 기준 / 'build' / راہ for راہ in لائبریری] + ['--end-group'], لاگ_صف)
                    نفاذ_کرو_حکم([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], لاگ_صف)
                with (결과 / 'remote-test.log').open('wb') as لاگ_صف:
                    نفاذ_کرو_حکم(['python3', 기준 / 'اوزار/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', سیٹنگاں_فائل, '--output', 결과], لاگ_صف)
                تریخ_دے_مطابق_کرو = json.loads((결과 / 'report.json').read_text())
                assert تریخ_دے_مطابق_کرو['passed']
                رپورٹ_قدر['checks'].append(ناں + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        رپورٹ_قدر['passed'] = True
    finally:
        رپورٹ_قدر['personal_settings_unchanged'] = ذاتی_سیٹنگیں.read_bytes() == 원래설정
        if not رپورٹ_قدر['personal_settings_unchanged']:
            رپورٹ_قدر['passed'] = False
        رپورٹ_قدر['kernel_sha256'] = hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()
        (출력 / 'report.json').write_text(json.dumps(رپورٹ_قدر, ensure_ascii=False, indent=2) + '\n')
    assert رپورٹ_قدر['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(رپورٹ_قدر, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    چلاؤ()
