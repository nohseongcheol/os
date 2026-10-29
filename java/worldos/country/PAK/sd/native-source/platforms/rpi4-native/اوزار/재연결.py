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


def تعميل_ڪرڻ_حڪم(ورڊ_متن):
    subprocess.check_call([str(داخلا_قدر) for داخلا_قدر in ورڊ_متن], cwd=str(기준))


def هلائڻ():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 تصديق_ڪريو')
    해석기.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    해석기.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    해석기.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = 해석기.parse_args()
    명세 = json.loads((기준 / 'relink.json').read_text())
    گڏ_ڪريو_سسٽم = 기준 / 'build'
    새묶음 = گڏ_ڪريو_سسٽم / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    ڪنڪٽر = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    محفوظ_ٽول = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    بعيد_سيٽنگون = json.loads((گڏ_ڪريو_سسٽم / 'remote/libassh-build.json').read_text())
    سيٽنگون = بعيد_سيٽنگون['flags']
    if 인수.libassh_archive:
        سلامتي_بنڊل = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', 기준 / 'بعيد_قدر', '-I', 기준 / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for نالو in بعيد_سيٽنگون['sources']:
            منزل_مقصود_قدر = 새묶음 / (Path(نالو).stem + '.o')
            تعميل_ڪرڻ_حڪم([번역기] + سيٽنگون + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', 기준 / نالو, '-o', منزل_مقصود_قدر])
            목적들.append(منزل_مقصود_قدر)
        سلامتي_بنڊل = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            تعميل_ڪرڻ_حڪم([محفوظ_ٽول, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(سلامتي_بنڊل)
    if 인수.tinycc:
        if not 인수.sdk:
            해석기.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            해석기.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [چونڊ_قدر for چونڊ_قدر in سيٽنگون if چونڊ_قدر != '-mgeneral-regs-only']
        منزل_مقصود_قدر = 새묶음 / '번역기.o'
        تعميل_ڪرڻ_حڪم([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', 기준 / '시언어번역기', '-I', 기준 / 'vendor/tinycc', '-I', 기준 / 'صارف',
             '-I', گڏ_ڪريو_سسٽم / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', 기준 / '시언어번역기/번역기.c', '-o', منزل_مقصود_قدر])
        تعميل_ڪرڻ_حڪم([ڪنڪٽر, '--gc-sections', '-T', 기준 / 'صارف/ڪڙي_لي_آئوٽ.ld', '-z', 'max-page-size=4096',
             '-o', گڏ_ڪريو_سسٽم / 'user/cc.elf', گڏ_ڪريو_سسٽم / 'user/start.o', گڏ_ڪريو_سسٽم / 'user/runtime.o', منزل_مقصود_قدر] +
             [گڏ_ڪريو_سسٽم / 'ccompiler' / (نالو + '.o') for نالو in ('عام_ٻولي_جو_رن_ٽائيم_معاونت', 'هلائڻ', '미리번역', '되돌림')] +
             [گڏ_ڪريو_سسٽم / 'user' / (نالو + '.o') for نالو in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = گڏ_ڪريو_سسٽم / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((گڏ_ڪريو_سسٽم / 'user/cc.elf').stat().st_size), 머리.read_text()))
        تعميل_ڪرڻ_حڪم([번역기] + سيٽنگون + ['-c', گڏ_ڪريو_سسٽم / 'programs.S', '-o', 기준 / 'objects/programs.o'])
        تعميل_ڪرڻ_حڪم([번역기] + سيٽنگون + ['-std=c11', '-I', 기준 / 'posix-kor/arm64-native/포함', '-I', گڏ_ڪريو_سسٽم,
             '-c', 기준 / 'مشين/صارف.c', '-o', 기준 / 'objects/user.o'])
    تعميل_ڪرڻ_حڪم([ڪنڪٽر, '--gc-sections', '-T', 기준 / '부팅/ڪڙي_لي_آئوٽ.ld', '-o', 새묶음 / 'kernel.elf'] +
         [기준 / راههه for راههه in 명세['objects']] + ['--start-group'] +
         [سلامتي_بنڊل if راههه == 'objects/libassh.a' else 기준 / راههه for راههه in 명세['libraries']] + ['--end-group'])
    تعميل_ڪرڻ_حڪم([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    هيش_فائل = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and هيش_فائل != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + هيش_فائل)
    print('RELINK PASS', هيش_فائل, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    هلائڻ()
