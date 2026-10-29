#!/usr/bin/env python3
"""개인 اتصال_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from راه_دور_تنظیمات import آماده_کردن
from COSL배포 import مقصد_نام, کتابخانه

نمایش_دادن_جذر = Path(__file__).resolve().parents[1]


def اجرا_2():
    خروجی = نمایش_دادن_جذر / 'build/verification/password-length'
    خروجی.mkdir(parents=True, exist_ok=True)
    تنظیمات_شخصی = نمایش_دادن_جذر / 'build/remote/access.json'
    원래설정 = تنظیمات_شخصی.read_bytes()
    گزارش_مقدار = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            시험터 = Path(임시)
            تنظیمات_مسیر = 시험터 / 'build/remote'
            تنظیمات_مسیر.mkdir(parents=True)
            تنظیمات_فایل = تنظیمات_مسیر / 'access.json'
            def نوشتن_تنظیمات(داده_ها):
                تنظیمات_فایل.write_text(json.dumps(داده_ها, ensure_ascii=False) + '\n')
                تنظیمات_فایل.chmod(0o600)
            def تأیید_صحت_تنظیمات(واسط, 화면):
                نوشتن_تنظیمات({'user': 'user', 'ssh_password': واسط, 'vnc_password': 화면})
                원본 = تنظیمات_فایل.read_bytes()
                آماده_کردن(시험터)
                assert تنظیمات_فایل.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (تنظیمات_مسیر / 'نمایه.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (تنظیمات_مسیر / 'نمایه.h').stat().st_mode & 0o777 == 0o600
            for واسط, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                تأیید_صحت_تنظیمات(واسط, 화면)
            گزارش_مقدار['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for تغییر_مقدار, ورودی_مقدار in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                داده_ها = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                داده_ها.update(تغییر_مقدار)
                نوشتن_تنظیمات(داده_ها)
                try:
                    آماده_کردن(시험터)
                except SystemExit as خطا:
                    assert ورودی_مقدار in str(خطا), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + ورودی_مقدار)
            گزارش_مقدار['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            تنظیمات = json.loads((نمایش_دادن_جذر / 'build/remote/libassh-build.json').read_text())['flags']
            번역기 = os.environ.get('ARM64_CC', 'clang')
            رابط = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            آرشیو_ابزار = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def اجرا_فرمان(نشانوندها, واقعه_نگار_ردیف):
                subprocess.run(list(map(str, نشانوندها)), cwd=str(نمایش_دادن_جذر), stdout=واقعه_نگار_ردیف,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for نام, واسط, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + نام, flush=True)
                تأیید_صحت_تنظیمات(واسط, 화면)
                سنجش = خروجی / نام
                سنجش.mkdir(exist_ok=True)
                with (سنجش / 'build.log').open('wb') as واقعه_نگار_ردیف:
                    목적들 = []
                    for 원본 in sorted((نمایش_دادن_جذر / 'راه_دور_مقدار').glob('*.c')):
                        مقصد_مقدار = 시험터 / (원본.stem + '.o')
                        اجرا_فرمان([번역기] + تنظیمات + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', تنظیمات_مسیر, '-I', نمایش_دادن_جذر / 'راه_دور_مقدار', '-I', نمایش_دادن_جذر / 'vendor/libassh/src',
                             '-I', نمایش_دادن_جذر / 'vendor/bearssl/inc', '-I', نمایش_دادن_جذر / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', مقصد_مقدار], واقعه_نگار_ردیف)
                        목적들.append(مقصد_مقدار)
                    راه_دور_دسته_کردن = 시험터 / 'libremote.a'
                    اجرا_فرمان([آرشیو_ابزار, 'rcs', راه_دور_دسته_کردن] + 목적들, واقعه_نگار_ردیف)
                    اجرا_فرمان([رابط, '--gc-sections', '-T', نمایش_دادن_جذر / '부팅/پیوند_پیمایش.ld', '-o', 시험터 / 'kernel.elf'] +
                         [نمایش_دادن_جذر / 'build' / (نام + '.o') for نام in مقصد_نام] + ['--start-group'] +
                         [راه_دور_دسته_کردن if مسیر == 'remote/libremote.a' else نمایش_دادن_جذر / 'build' / مسیر for مسیر in کتابخانه] + ['--end-group'], واقعه_نگار_ردیف)
                    اجرا_فرمان([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         시험터 / 'kernel.elf', 시험터 / 'kernel8.img'], واقعه_نگار_ردیف)
                with (سنجش / 'remote-test.log').open('wb') as واقعه_نگار_ردیف:
                    اجرا_فرمان(['python3', نمایش_دادن_جذر / 'ابزارها/원격접속시험.py', '--kernel', 시험터 / 'kernel8.img',
                         '--access', تنظیمات_فایل, '--output', سنجش], واقعه_نگار_ردیف)
                ارزیابی_کردن = json.loads((سنجش / 'report.json').read_text())
                assert ارزیابی_کردن['passed']
                گزارش_مقدار['checks'].append(نام + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        گزارش_مقدار['passed'] = True
    finally:
        گزارش_مقدار['personal_settings_unchanged'] = تنظیمات_شخصی.read_bytes() == 원래설정
        if not گزارش_مقدار['personal_settings_unchanged']:
            گزارش_مقدار['passed'] = False
        گزارش_مقدار['kernel_sha256'] = hashlib.sha256((نمایش_دادن_جذر / 'build/kernel8.img').read_bytes()).hexdigest()
        (خروجی / 'report.json').write_text(json.dumps(گزارش_مقدار, ensure_ascii=False, indent=2) + '\n')
    assert گزارش_مقدار['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(گزارش_مقدار, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    اجرا_2()
