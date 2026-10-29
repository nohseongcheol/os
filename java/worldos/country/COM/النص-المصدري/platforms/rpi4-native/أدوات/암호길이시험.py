#!/usr/bin/env python3
"""개인 صديق_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from بعيد_إعدادات import إعداد
from COSL배포 import وجهة_اسم, مكتبة

يعرض_جذر = Path(__file__).resolve().parents[1]


def تشغيل():
    مخرجات = يعرض_جذر / 'build/verification/password-length'
    مخرجات.mkdir(parents=True, exist_ok=True)
    شخصي_إعدادات = يعرض_جذر / 'build/remote/access.json'
    원래설정 = شخصي_إعدادات.read_bytes()
    إبلاغ_قيمة = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            يختبر_مساحة_عمل = Path(임시)
            إعدادات_مسار = يختبر_مساحة_عمل / 'build/remote'
            إعدادات_مسار.mkdir(parents=True)
            إعدادات_ملف = إعدادات_مسار / 'access.json'
            def كتابة_إعدادات(بيانات):
                إعدادات_ملف.write_text(json.dumps(بيانات, ensure_ascii=False) + '\n')
                إعدادات_ملف.chmod(0o600)
            def يتحقق_إعدادات(셸, 화면):
                كتابة_إعدادات({'user': 'user', 'ssh_password': 셸, 'vnc_password': 화면})
                원본 = إعدادات_ملف.read_bytes()
                إعداد(يختبر_مساحة_عمل)
                assert إعدادات_ملف.read_bytes() == 원본, 'Settings were rewritten'
                رأس_قيمة = (إعدادات_مسار / 'يحلل.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', رأس_قيمة)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (إعدادات_مسار / 'يحلل.h').stat().st_mode & 0o777 == 0o600
            for 셸, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                يتحقق_إعدادات(셸, 화면)
            إبلاغ_قيمة['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for يغيّر_قيمة, إدخال_قيمة_962f286b in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                بيانات = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                بيانات.update(يغيّر_قيمة)
                كتابة_إعدادات(بيانات)
                try:
                    إعداد(يختبر_مساحة_عمل)
                except SystemExit as خطأ:
                    assert إدخال_قيمة_962f286b in str(خطأ), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + إدخال_قيمة_962f286b)
            إبلاغ_قيمة['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            إعدادات = json.loads((يعرض_جذر / 'build/remote/libassh-build.json').read_text())['flags']
            محول_برمجي_أداة = os.environ.get('ARM64_CC', 'clang')
            موصل = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            أرشيف_أداة = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def ينفذ_أمر(وسائط, سجل_سجل):
                subprocess.run(list(map(str, وسائط)), cwd=str(يعرض_جذر), stdout=سجل_سجل,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for اسم, 셸, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + اسم, flush=True)
                يتحقق_إعدادات(셸, 화면)
                نتيجة = مخرجات / اسم
                نتيجة.mkdir(exist_ok=True)
                with (نتيجة / 'build.log').open('wb') as سجل_سجل:
                    목적들 = []
                    for 원본 in sorted((يعرض_جذر / 'بعيد_قيمة').glob('*.c')):
                        وجهة_قيمة = يختبر_مساحة_عمل / (원본.stem + '.o')
                        ينفذ_أمر([محول_برمجي_أداة] + إعدادات + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', إعدادات_مسار, '-I', يعرض_جذر / 'بعيد_قيمة', '-I', يعرض_جذر / 'vendor/libassh/src',
                             '-I', يعرض_جذر / 'vendor/bearssl/inc', '-I', يعرض_جذر / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', وجهة_قيمة], سجل_سجل)
                        목적들.append(وجهة_قيمة)
                    بعيد_يُجمع = يختبر_مساحة_عمل / 'libremote.a'
                    ينفذ_أمر([أرشيف_أداة, 'rcs', بعيد_يُجمع] + 목적들, سجل_سجل)
                    ينفذ_أمر([موصل, '--gc-sections', '-T', يعرض_جذر / 'إقلاع_الآلة/تخطيط_الربط.ld', '-o', يختبر_مساحة_عمل / 'kernel.elf'] +
                         [يعرض_جذر / 'build' / (اسم + '.o') for اسم in وجهة_اسم] + ['--start-group'] +
                         [بعيد_يُجمع if مسار == 'remote/libremote.a' else يعرض_جذر / 'build' / مسار for مسار in مكتبة] + ['--end-group'], سجل_سجل)
                    ينفذ_أمر([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         يختبر_مساحة_عمل / 'kernel.elf', يختبر_مساحة_عمل / 'kernel8.img'], سجل_سجل)
                with (نتيجة / 'remote-test.log').open('wb') as سجل_سجل:
                    ينفذ_أمر(['python3', يعرض_جذر / 'أدوات/اتصال_بعيد_يختبر.py', '--kernel', يختبر_مساحة_عمل / 'kernel8.img',
                         '--access', إعدادات_ملف, '--output', نتيجة], سجل_سجل)
                التحقق_من_صحة = json.loads((نتيجة / 'report.json').read_text())
                assert التحقق_من_صحة['passed']
                إبلاغ_قيمة['checks'].append(اسم + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        إبلاغ_قيمة['passed'] = True
    finally:
        إبلاغ_قيمة['personal_settings_unchanged'] = شخصي_إعدادات.read_bytes() == 원래설정
        if not إبلاغ_قيمة['personal_settings_unchanged']:
            إبلاغ_قيمة['passed'] = False
        إبلاغ_قيمة['kernel_sha256'] = hashlib.sha256((يعرض_جذر / 'build/kernel8.img').read_bytes()).hexdigest()
        (مخرجات / 'report.json').write_text(json.dumps(إبلاغ_قيمة, ensure_ascii=False, indent=2) + '\n')
    assert إبلاغ_قيمة['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(إبلاغ_قيمة, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    تشغيل()
