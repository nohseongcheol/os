#!/usr/bin/env python3
"""توزيع_قيمة 묶음에서 libassh/TinyCC를 교체하고 ذاتي 커널을 إعادة_محاولة_قيمة 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

يعرض_جذر = Path(__file__).resolve().parent


def ينفذ_أمر(الكلمات_نص):
    subprocess.check_call([str(إدخال_قيمة_962f286b) for إدخال_قيمة_962f286b in الكلمات_نص], cwd=str(يعرض_جذر))


def تشغيل():
    المحلل_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    المحلل_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 يتحقق')
    المحلل_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a يستخدم_قيمة')
    المحلل_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 إعادة_محاولة_قيمة 컴파일하고 커널에 탑재')
    المحلل_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    وسائط = المحلل_48ee4b1b.parse_args()
    المواصفات = json.loads((يعرض_جذر / 'relink.json').read_text())
    بنية_نظام = يعرض_جذر / 'build'
    새묶음 = بنية_نظام / 'relinked'
    새묶음.mkdir(exist_ok=True)
    محول_برمجي_أداة = os.environ.get('ARM64_CC', 'clang')
    موصل = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    أرشيف_أداة = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    بعيد_إعدادات = json.loads((بنية_نظام / 'remote/libassh-build.json').read_text())
    إعدادات = بعيد_إعدادات['flags']
    if وسائط.libassh_archive:
        أمان_يُجمع = وسائط.libassh_archive.resolve()
    else:
        목적들 = []
        تصريحات = ['-I', يعرض_جذر / 'بعيد_قيمة', '-I', يعرض_جذر / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for اسم in بعيد_إعدادات['sources']:
            وجهة_قيمة = 새묶음 / (Path(اسم).stem + '.o')
            ينفذ_أمر([محول_برمجي_أداة] + إعدادات + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + تصريحات +
                 ['-c', يعرض_جذر / اسم, '-o', وجهة_قيمة])
            목적들.append(وجهة_قيمة)
        أمان_يُجمع = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            ينفذ_أمر([أرشيف_أداة, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(أمان_يُجمع)
    if وسائط.tinycc:
        if not وسائط.sdk:
            المحلل_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = وسائط.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            المحلل_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [تحديد_قيمة for تحديد_قيمة in إعدادات if تحديد_قيمة != '-mgeneral-regs-only']
        وجهة_قيمة = 새묶음 / 'محول_برمجي_أداة.o'
        ينفذ_أمر([محول_برمجي_أداة] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', يعرض_جذر / 'الرمز_البريدي_محول_برمجي', '-I', يعرض_جذر / 'vendor/tinycc', '-I', يعرض_جذر / 'فضاء_المستخدم',
             '-I', بنية_نظام / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', يعرض_جذر / 'الرمز_البريدي_محول_برمجي/محول_برمجي_أداة.c', '-o', وجهة_قيمة])
        ينفذ_أمر([موصل, '--gc-sections', '-T', يعرض_جذر / 'فضاء_المستخدم/تخطيط_الربط.ld', '-z', 'max-page-size=4096',
             '-o', بنية_نظام / 'user/cc.elf', بنية_نظام / 'user/start.o', بنية_نظام / 'user/runtime.o', وجهة_قيمة] +
             [بنية_نظام / 'ccompiler' / (اسم + '.o') for اسم in ('دعمتشغيل', 'تشغيل', '미리번역', 'إرجاع_جسر')] +
             [بنية_نظام / 'user' / (اسم + '.o') for اسم in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        رأس_قيمة = بنية_نظام / 'programs.h'
        رأس_قيمة.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((بنية_نظام / 'user/cc.elf').stat().st_size), رأس_قيمة.read_text()))
        ينفذ_أمر([محول_برمجي_أداة] + إعدادات + ['-c', بنية_نظام / 'programs.S', '-o', يعرض_جذر / 'objects/programs.o'])
        ينفذ_أمر([محول_برمجي_أداة] + إعدادات + ['-std=c11', '-I', يعرض_جذر / 'posix-kor/arm64-native/تصريحات', '-I', بنية_نظام,
             '-c', يعرض_جذر / 'جهاز/فضاء_المستخدم.c', '-o', يعرض_جذر / 'objects/user.o'])
    ينفذ_أمر([موصل, '--gc-sections', '-T', يعرض_جذر / 'إقلاع_الآلة/تخطيط_الربط.ld', '-o', 새묶음 / 'kernel.elf'] +
         [يعرض_جذر / مسار for مسار in المواصفات['objects']] + ['--start-group'] +
         [أمان_يُجمع if مسار == 'objects/libassh.a' else يعرض_جذر / مسار for مسار in المواصفات['libraries']] + ['--end-group'])
    ينفذ_أمر([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    تجزئة_ملف = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if وسائط.verify and تجزئة_ملف != المواصفات['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + تجزئة_ملف)
    print('RELINK PASS', تجزئة_ملف, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    تشغيل()
