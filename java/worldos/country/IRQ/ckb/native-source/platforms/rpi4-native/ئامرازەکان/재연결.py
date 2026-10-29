#!/usr/bin/env python3
"""배포 묶음에서 libassh/TinyCC를 교체하고 자체 커널을 다시 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

기준 = Path(__file__).resolve().parent


def جێبەجێکردن_فەرمان(وشە_دەق):
    subprocess.check_call([str(تێنووسین_نرخ) for تێنووسین_نرخ in وشە_دەق], cwd=str(기준))


def ڕادان():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 سەلماندن')
    해석기.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    해석기.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    해석기.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = 해석기.parse_args()
    명세 = json.loads((기준 / 'relink.json').read_text())
    دروستکراو_سیستم = 기준 / 'build'
    새묶음 = دروستکراو_سیستم / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    لکێنەر = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    ئەرشیف_ئامراز = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    دوورەدەس_ڕێكبەندەكان = json.loads((دروستکراو_سیستم / 'remote/libassh-build.json').read_text())
    ڕێكبەندەكان = دوورەدەس_ڕێكبەندەكان['flags']
    if 인수.libassh_archive:
        ئاسایش_گورزە = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', 기준 / 'دوورەدەس_نرخ', '-I', 기준 / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for ناو in دوورەدەس_ڕێكبەندەكان['sources']:
            جێمەبەست_نرخ = 새묶음 / (Path(ناو).stem + '.o')
            جێبەجێکردن_فەرمان([번역기] + ڕێكبەندەكان + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', 기준 / ناو, '-o', جێمەبەست_نرخ])
            목적들.append(جێمەبەست_نرخ)
        ئاسایش_گورزە = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            جێبەجێکردن_فەرمان([ئەرشیف_ئامراز, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(ئاسایش_گورزە)
    if 인수.tinycc:
        if not 인수.sdk:
            해석기.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            해석기.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [بژاردە_نرخ for بژاردە_نرخ in ڕێكبەندەكان if بژاردە_نرخ != '-mgeneral-regs-only']
        جێمەبەست_نرخ = 새묶음 / '번역기.o'
        جێبەجێکردن_فەرمان([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', 기준 / '시언어번역기', '-I', 기준 / 'vendor/tinycc', '-I', 기준 / 'بەکارهێنەر',
             '-I', دروستکراو_سیستم / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', 기준 / '시언어번역기/번역기.c', '-o', جێمەبەست_نرخ])
        جێبەجێکردن_فەرمان([لکێنەر, '--gc-sections', '-T', 기준 / 'بەکارهێنەر/لینك_ڕیزبەست.ld', '-z', 'max-page-size=4096',
             '-o', دروستکراو_سیستم / 'user/cc.elf', دروستکراو_سیستم / 'user/start.o', دروستکراو_سیستم / 'user/runtime.o', جێمەبەست_نرخ] +
             [دروستکراو_سیستم / 'ccompiler' / (ناو + '.o') for ناو in ('ڕەنتایمی_زمانی_هاوبەش_پشتیوانی', 'ڕادان', '미리번역', '되돌림')] +
             [دروستکراو_سیستم / 'user' / (ناو + '.o') for ناو in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = دروستکراو_سیستم / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((دروستکراو_سیستم / 'user/cc.elf').stat().st_size), 머리.read_text()))
        جێبەجێکردن_فەرمان([번역기] + ڕێكبەندەكان + ['-c', دروستکراو_سیستم / 'programs.S', '-o', 기준 / 'objects/programs.o'])
        جێبەجێکردن_فەرمان([번역기] + ڕێكبەندەكان + ['-std=c11', '-I', 기준 / 'posix-kor/arm64-native/포함', '-I', دروستکراو_سیستم,
             '-c', 기준 / 'مەکینه/بەکارهێنەر.c', '-o', 기준 / 'objects/user.o'])
    جێبەجێکردن_فەرمان([لکێنەر, '--gc-sections', '-T', 기준 / '부팅/لینك_ڕیزبەست.ld', '-o', 새묶음 / 'kernel.elf'] +
         [기준 / گوزەر for گوزەر in 명세['objects']] + ['--start-group'] +
         [ئاسایش_گورزە if گوزەر == 'objects/libassh.a' else 기준 / گوزەر for گوزەر in 명세['libraries']] + ['--end-group'])
    جێبەجێکردن_فەرمان([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    دەرەنجام_فایل = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and دەرەنجام_فایل != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + دەرەنجام_فایل)
    print('RELINK PASS', دەرەنجام_فایل, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    ڕادان()
