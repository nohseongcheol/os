#!/usr/bin/env python3
"""배포 묶음에서 libassh/TinyCC를 교체하고 بومی 커널을 다시 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

نمایش_دادن_جذر = Path(__file__).resolve().parent


def اجرا_فرمان(کلمات_متن):
    subprocess.check_call([str(ورودی_مقدار) for ورودی_مقدار in کلمات_متن], cwd=str(نمایش_دادن_جذر))


def اجرا_2():
    مفسر_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    مفسر_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 تأیید_صحت')
    مفسر_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    مفسر_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    مفسر_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    نشانوندها = مفسر_48ee4b1b.parse_args()
    명세 = json.loads((نمایش_دادن_جذر / 'relink.json').read_text())
    ساخت_سیستم = نمایش_دادن_جذر / 'build'
    새묶음 = ساخت_سیستم / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    رابط = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    آرشیو_ابزار = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    راه_دور_تنظیمات = json.loads((ساخت_سیستم / 'remote/libassh-build.json').read_text())
    تنظیمات = راه_دور_تنظیمات['flags']
    if نشانوندها.libassh_archive:
        امنیت_دسته_کردن = نشانوندها.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', نمایش_دادن_جذر / 'راه_دور_مقدار', '-I', نمایش_دادن_جذر / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for نام in راه_دور_تنظیمات['sources']:
            مقصد_مقدار = 새묶음 / (Path(نام).stem + '.o')
            اجرا_فرمان([번역기] + تنظیمات + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', نمایش_دادن_جذر / نام, '-o', مقصد_مقدار])
            목적들.append(مقصد_مقدار)
        امنیت_دسته_کردن = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            اجرا_فرمان([آرشیو_ابزار, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(امنیت_دسته_کردن)
    if نشانوندها.tinycc:
        if not نشانوندها.sdk:
            مفسر_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = نشانوندها.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            مفسر_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [مورد_انتخابی_مقدار for مورد_انتخابی_مقدار in تنظیمات if مورد_انتخابی_مقدار != '-mgeneral-regs-only']
        مقصد_مقدار = 새묶음 / '번역기.o'
        اجرا_فرمان([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', نمایش_دادن_جذر / '시언어번역기', '-I', نمایش_دادن_جذر / 'vendor/tinycc', '-I', نمایش_دادن_جذر / 'کاربر',
             '-I', ساخت_سیستم / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', نمایش_دادن_جذر / '시언어번역기/번역기.c', '-o', مقصد_مقدار])
        اجرا_فرمان([رابط, '--gc-sections', '-T', نمایش_دادن_جذر / 'کاربر/پیوند_پیمایش.ld', '-z', 'max-page-size=4096',
             '-o', ساخت_سیستم / 'user/cc.elf', ساخت_سیستم / 'user/start.o', ساخت_سیستم / 'user/runtime.o', مقصد_مقدار] +
             [ساخت_سیستم / 'ccompiler' / (نام + '.o') for نام in ('زمان_اجرای_زبان_مشترک_پشتیبان', 'اجرا_2', '미리번역', 'بازگرداندن_پل')] +
             [ساخت_سیستم / 'user' / (نام + '.o') for نام in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = ساخت_سیستم / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((ساخت_سیستم / 'user/cc.elf').stat().st_size), 머리.read_text()))
        اجرا_فرمان([번역기] + تنظیمات + ['-c', ساخت_سیستم / 'programs.S', '-o', نمایش_دادن_جذر / 'objects/programs.o'])
        اجرا_فرمان([번역기] + تنظیمات + ['-std=c11', '-I', نمایش_دادن_جذر / 'posix-kor/arm64-native/포함', '-I', ساخت_سیستم,
             '-c', نمایش_دادن_جذر / 'دستگاه/کاربر.c', '-o', نمایش_دادن_جذر / 'objects/user.o'])
    اجرا_فرمان([رابط, '--gc-sections', '-T', نمایش_دادن_جذر / '부팅/پیوند_پیمایش.ld', '-o', 새묶음 / 'kernel.elf'] +
         [نمایش_دادن_جذر / مسیر for مسیر in 명세['objects']] + ['--start-group'] +
         [امنیت_دسته_کردن if مسیر == 'objects/libassh.a' else نمایش_دادن_جذر / مسیر for مسیر in 명세['libraries']] + ['--end-group'])
    اجرا_فرمان([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    هاشور_فایل = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if نشانوندها.verify and هاشور_فایل != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + هاشور_فایل)
    print('RELINK PASS', هاشور_فایل, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    اجرا_2()
