#!/usr/bin/env python3
"""حديث_عنصر ذاتي ARM64 산출물을 검사하고 LGPL مصدر_شجرة·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

يعرض_جذر = Path(__file__).resolve().parents[1]
مستودع_جذر = يعرض_جذر.parents[1]
وجهة_اسم = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
مكتبة = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def تجزئة_ملف(مسار):
    return hashlib.sha256(Path(مسار).read_bytes()).hexdigest()


def 점검():
    for اسم in ('vendor/wolfssh', 'vendor/wolfssl', 'بعيد_قيمة/user_settings.h'):
        if (يعرض_جذر / اسم).exists():
            raise SystemExit('COSL توزيع_قيمة إيقاف: 이전 GPL بعيد_قيمة 구현이 مصدر_شجرة 트리에 남아 있습니다: ' + اسم)
    سلكي_قيمة = (يعرض_جذر / 'شبكة_رمز/سلكي_شبكة.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in سلكي_قيمة or 'SPDX-License-Identifier: GPL' in سلكي_قيمة:
        raise SystemExit('COSL توزيع_قيمة إيقاف: BSD GENET 구현·고지 يتحقق 필요')
    for اسم in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (مستودع_جذر / اسم).is_file():
            raise SystemExit('COSL توزيع_قيمة 고지 없음: ' + اسم)
    رمز_قيمة = subprocess.check_output(['aarch64-linux-gnu-nm', str(يعرض_جذر / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', رمز_قيمة):
        raise SystemExit('COSL توزيع_قيمة إيقاف: 커널에 이전 GPL رمز_الوصول_قيمة/SSH 심볼이 남아 있습니다. إعادة_محاولة_قيمة 빌드하세요.')
    for اسم in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + اسم + r'$', رمز_قيمة, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + اسم)
    with tempfile.TemporaryDirectory(dir=str(يعرض_جذر / 'build')) as 임시:
        صورة_قيمة = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(يعرض_جذر / 'build/kernel.elf'), str(صورة_قيمة)])
        if تجزئة_ملف(صورة_قيمة) != تجزئة_ملف(يعرض_جذر / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    إبلاغ_قيمة = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': تجزئة_ملف(يعرض_جذر / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {اسم: تجزئة_ملف(يعرض_جذر / 'build' / اسم) for اسم in مكتبة}}
    (يعرض_جذر / 'build/cosl-distribution-check.json').write_text(json.dumps(إبلاغ_قيمة, ensure_ascii=False, indent=2) + '\n')
    return إبلاغ_قيمة


def يربط_المشارك():
    إبلاغ_قيمة = 점검()
    توزيع_قيمة = يعرض_جذر / 'dist'
    توزيع_قيمة.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(يعرض_جذر / 'build')) as 임시:
        يجمع_قيمة = Path(임시) / 'jkoros-native-relink'
        يجمع_قيمة.mkdir()
        def مثيل_قيمة(원본, نظير_قيمة):
            وجهة_قيمة = يجمع_قيمة / نظير_قيمة
            وجهة_قيمة.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(وجهة_قيمة), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(وجهة_قيمة))
        for اسم in وجهة_اسم:
            مثيل_قيمة(يعرض_جذر / 'build' / (اسم + '.o'), 'objects/' + اسم + '.o')
        for اسم in مكتبة:
            مثيل_قيمة(يعرض_جذر / 'build' / اسم, 'objects/' + Path(اسم).name)
        for اسم in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     'الرمز_البريدي_محول_برمجي', 'فضاء_المستخدم', '명명', 'جهاز', 'شبكة_رمز/شبكة_رمز.h', 'إقلاع_الآلة/تخطيط_الربط.ld',
                     'بعيد_قيمة/assh_config.h', 'بعيد_قيمة/config.h', 'بعيد_قيمة/ctype.h', 'بعيد_قيمة/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            مثيل_قيمة(يعرض_جذر / اسم, اسم)
        for اسم in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            مثيل_قيمة(مستودع_جذر / اسم, اسم)
        for مسار in sorted((يعرض_جذر / 'vendor').glob('LICENSE*')):
            مثيل_قيمة(مسار, 'vendor/' + مسار.name)
        مثيل_قيمة(يعرض_جذر / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        مثيل_قيمة(يعرض_جذر / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        مثيل_قيمة(مستودع_جذر / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        مثيل_قيمة(يعرض_جذر / 'أدوات/재연결.py', 'relink.py')
        for مسار in sorted((يعرض_جذر / 'build/user').glob('*.elf')):
            مثيل_قيمة(مسار, 'build/user/' + مسار.name)
        for اسم in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            مثيل_قيمة(يعرض_جذر / 'build/user' / (اسم + '.o'), 'build/user/' + اسم + '.o')
        for اسم in ('crt', 'aot-runtime', 'دعمتشغيل', 'تشغيل', '미리번역', 'إرجاع_جسر'):
            مثيل_قيمة(يعرض_جذر / 'build/ccompiler' / (اسم + '.o'), 'build/ccompiler/' + اسم + '.o')
        المواصفات = dict(إبلاغ_قيمة, objects=['objects/' + اسم + '.o' for اسم in وجهة_اسم],
                    libraries=['objects/' + Path(مسار).name for مسار in مكتبة])
        (يجمع_قيمة / 'relink.json').write_text(json.dumps(المواصفات, ensure_ascii=False, indent=2) + '\n')
        (يجمع_قيمة / 'README.md').write_text('''# jkoros native LGPL source and relink kit

This kit accompanies the matching kernel image. Retain it with binary distributions.
Application terms: LICENSE. Library terms: vendor/libassh/COPYING and vendor/tinycc/COPYING.
Other notices: THIRD_PARTY_NOTICES.md. COSL does not override the LGPL permissions.
This product includes software developed by Bill Paul.

Host dependencies: Python 3, Clang supporting aarch64-none-elf, libnewlib-dev headers,
and aarch64-linux-gnu binutils. No Linux kernel is linked into the guest.

From this extracted directory:

    python3 relink.py --verify

This recompiles libassh from the included source/configuration and relinks the kernel.
The original unmodified library must produce the recorded kernel SHA256.
To change libassh, edit vendor/libassh/src, then run without --verify.
Alternatively: python3 relink.py --libassh-archive /path/to/modified/libassh.a

TinyCC source is included in vendor/tinycc; the native port is in الرمز_البريدي_محول_برمجي.
To rebuild a modified TinyCC and replace its embedded executable:

    python3 relink.py --tinycc --sdk /path/to/alpine-arm64-rootfs

Use the same Alpine 3.24.2 ARM64 SDK headers and GCC 15.2.0 libgcc runtime as the
original build (jkoros/platforms/rpi4: make prepare-runtime; see that platform's docs).
The SDK is a host build prerequisite and is not included here. Its libgcc exception
and GPL text are in vendor/LICENSE.libgcc-runtime and vendor/LICENSE.gcc-gpl3.
GCC sources: https://gcc.gnu.org/pub/gcc/releases/gcc-15.2.0/
Both the cc ELF size table and user/program objects are regenerated when --tinycc is used.
Output: build/relinked/kernel8.img. Boot it using the same Pi4 firmware/config or QEMU
runner as the original image. There is no signature lock against modified libraries.

This is a relink kit for one device image. Objects contain the same embedded device
key as that image. Keep personal development images and build/remote credentials
out of public source uploads; provision appropriate images for recipients.
''')
        الهدف = توزيع_قيمة / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / الهدف.name
        with tarfile.open(str(임시압축), 'w:gz') as أرشيف_قيمة:
            أرشيف_قيمة.add(str(يجمع_قيمة), arcname=يجمع_قيمة.name)
        임시압축.replace(الهدف)
    إبلاغ_قيمة['relink_archive_sha256'] = تجزئة_ملف(الهدف)
    (توزيع_قيمة / 'cosl-distribution.json').write_text(json.dumps(إبلاغ_قيمة, ensure_ascii=False, indent=2) + '\n')
    return الهدف


if __name__ == '__main__':
    المحلل_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    المحلل_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    قيمة = المحلل_48ee4b1b.parse_args()
    if قيمة.command == 'bundle':
        print('COSL source/relink kit:', يربط_المشارك())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
