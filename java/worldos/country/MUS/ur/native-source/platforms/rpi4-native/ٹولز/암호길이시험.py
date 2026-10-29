#!/usr/bin/env python3
"""개인 رابطہ_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from بعید_سیٹنگز import تیار_کریں
from COSL배포 import منزل_مقصود_نام, لائبریری

عکس_ڈالنا_روٹ = Path(__file__).resolve().parents[1]


def چلائیں():
    اخراج_کا_مقام = عکس_ڈالنا_روٹ / 'build/verification/password-length'
    اخراج_کا_مقام.mkdir(parents=True, exist_ok=True)
    ذاتی_سیٹنگیں = عکس_ڈالنا_روٹ / 'build/remote/access.json'
    원래설정 = ذاتی_سیٹنگیں.read_bytes()
    رپورٹ_قدر = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            سیٹنگز_راہ = 시험터 / 'build/remote'
            سیٹنگز_راہ.mkdir(parents=True)
            سیٹنگز_فائل = سیٹنگز_راہ / 'access.json'
            def لکھیں_سیٹنگز(کوائف):
                سیٹنگز_فائل.write_text(json.dumps(کوائف, ensure_ascii=False) + '\n')
                سیٹنگز_فائل.chmod(0o600)
            def تصدیق_کریں_سیٹنگز(شیل, 화면):
                لکھیں_سیٹنگز({'user': 'user', 'ssh_password': شیل, 'vnc_password': 화면})
                원본 = سیٹنگز_فائل.read_bytes()
                تیار_کریں(시험터)
                assert سیٹنگز_فائل.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (سیٹنگز_راہ / 'پروفائل.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (سیٹنگز_راہ / 'پروفائل.h').stat().st_mode & 0o777 == 0o600
            for شیل, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                تصدیق_کریں_سیٹنگز(شیل, 화면)
            رپورٹ_قدر['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for تبدیل_کریں_قدر, اندراج_قدر in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                کوائف = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                کوائف.update(تبدیل_کریں_قدر)
                لکھیں_سیٹنگز(کوائف)
                try:
                    تیار_کریں(시험터)
                except SystemExit as غلطی:
                    assert اندراج_قدر in str(غلطی), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + اندراج_قدر)
            رپورٹ_قدر['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            ترتیبات = json.loads((عکس_ڈالنا_روٹ / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            کنکٹر = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            محفوظ_ٹول = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def نفاذ_کریں_حکم(دلائل, لاگ_صف):
                subprocess.run(list(map(str, دلائل)), cwd=str(عکس_ڈالنا_روٹ), stdout=لاگ_صف,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for نام, شیل, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + نام, flush=True)
                تصدیق_کریں_سیٹنگز(شیل, 화면)
                پیمائش = اخراج_کا_مقام / نام
                پیمائش.mkdir(exist_ok=True)
                with (پیمائش / 'build.log').open('wb') as لاگ_صف:
                    목적들 = []
                    for 원본 in sorted((عکس_ڈالنا_روٹ / 'بعید_قدر').glob('*.c')):
                        منزل_مقصود_قدر = 시험터 / (원본.stem + '.o')
                        نفاذ_کریں_حکم([번역기] + ترتیبات + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', سیٹنگز_راہ, '-I', عکس_ڈالنا_روٹ / 'بعید_قدر', '-I', عکس_ڈالنا_روٹ / 'vendor/libassh/src',
                             '-I', عکس_ڈالنا_روٹ / 'vendor/bearssl/inc', '-I', عکس_ڈالنا_روٹ / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', منزل_مقصود_قدر], لاگ_صف)
                        목적들.append(منزل_مقصود_قدر)
                    بعید_بنڈل = 시험터 / 'libremote.a'
                    نفاذ_کریں_حکم([محفوظ_ٹول, 'rcs', بعید_بنڈل] + 목적들, لاگ_صف)
                    نفاذ_کریں_حکم([کنکٹر, '--gc-sections', '-T', عکس_ڈالنا_روٹ / '부팅/ربط_ترتیب.ld', '-o', 시험터 / 'kernel.elf'] +
                         [عکس_ڈالنا_روٹ / 'build' / (نام + '.o') for نام in منزل_مقصود_نام] + ['--start-group'] +
                         [بعید_بنڈل if راستہ_2 == 'remote/libremote.a' else عکس_ڈالنا_روٹ / 'build' / راستہ_2 for راستہ_2 in لائبریری] + ['--end-group'], لاگ_صف)
                    نفاذ_کریں_حکم([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], لاگ_صف)
                with (پیمائش / 'remote-test.log').open('wb') as لاگ_صف:
                    نفاذ_کریں_حکم(['python3', عکس_ڈالنا_روٹ / 'ٹولز/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', سیٹنگز_فائل, '--output', پیمائش], لاگ_صف)
                جواز_دہی_کریں = json.loads((پیمائش / 'report.json').read_text())
                assert جواز_دہی_کریں['passed']
                رپورٹ_قدر['checks'].append(نام + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        رپورٹ_قدر['passed'] = True
    finally:
        رپورٹ_قدر['personal_settings_unchanged'] = ذاتی_سیٹنگیں.read_bytes() == 원래설정
        if not رپورٹ_قدر['personal_settings_unchanged']:
            رپورٹ_قدر['passed'] = False
        رپورٹ_قدر['kernel_sha256'] = hashlib.sha256((عکس_ڈالنا_روٹ / 'build/kernel8.img').read_bytes()).hexdigest()
        (اخراج_کا_مقام / 'report.json').write_text(json.dumps(رپورٹ_قدر, ensure_ascii=False, indent=2) + '\n')
    assert رپورٹ_قدر['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(رپورٹ_قدر, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    چلائیں()
