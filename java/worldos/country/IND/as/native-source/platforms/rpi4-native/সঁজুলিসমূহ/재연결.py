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


def নিষ্পাদন_আদেশ(말):
    subprocess.check_call([str(প্রবিষ্ট_মান) for প্রবিষ্ট_মান in 말], cwd=str(기준))


def সঞ্চালন():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 প্ৰমাণিত_কৰক')
    해석기.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    해석기.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    해석기.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = 해석기.parse_args()
    명세 = json.loads((기준 / 'relink.json').read_text())
    বিল্ড_ছিষ্টেম = 기준 / 'build'
    새묶음 = বিল্ড_ছিষ্টেম / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    সংযোজক = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    অভিলেখাগাৰ_সঁজুলি = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    দূৰবৰ্তী_ছেটিংছ = json.loads((বিল্ড_ছিষ্টেম / 'remote/libassh-build.json').read_text())
    বৈশিষ্ট্য = দূৰবৰ্তী_ছেটিংছ['flags']
    if 인수.libassh_archive:
        নিৰাপত্তা_বাণ্ডল = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', 기준 / 'দূৰবৰ্তী_মান', '-I', 기준 / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for নাম in দূৰবৰ্তী_ছেটিংছ['sources']:
            গন্তব্য_স্থান_মান = 새묶음 / (Path(নাম).stem + '.o')
            নিষ্পাদন_আদেশ([번역기] + বৈশিষ্ট্য + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', 기준 / নাম, '-o', গন্তব্য_স্থান_মান])
            목적들.append(গন্তব্য_স্থান_মান)
        নিৰাপত্তা_বাণ্ডল = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            নিষ্পাদন_আদেশ([অভিলেখাগাৰ_সঁজুলি, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(নিৰাপত্তা_বাণ্ডল)
    if 인수.tinycc:
        if not 인수.sdk:
            해석기.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            해석기.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [চয়ন_মান for চয়ন_মান in বৈশিষ্ট্য if চয়ন_মান != '-mgeneral-regs-only']
        গন্তব্য_স্থান_মান = 새묶음 / '번역기.o'
        নিষ্পাদন_আদেশ([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', 기준 / '시언어번역기', '-I', 기준 / 'vendor/tinycc', '-I', 기준 / 'ব্যৱহাৰকৰ্তা',
             '-I', বিল্ড_ছিষ্টেম / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', 기준 / '시언어번역기/번역기.c', '-o', গন্তব্য_স্থান_মান])
        নিষ্পাদন_আদেশ([সংযোজক, '--gc-sections', '-T', 기준 / 'ব্যৱহাৰকৰ্তা/লিংক_লেআউট.ld', '-z', 'max-page-size=4096',
             '-o', বিল্ড_ছিষ্টেম / 'user/cc.elf', বিল্ড_ছিষ্টেম / 'user/start.o', বিল্ড_ছিষ্টেম / 'user/runtime.o', গন্তব্য_স্থান_মান] +
             [বিল্ড_ছিষ্টেম / 'ccompiler' / (নাম + '.o') for নাম in ('উমৈহতীয়া_ভাষা_ৰানটাইম_সমর্থন', 'সঞ্চালন', '미리번역', '되돌림')] +
             [বিল্ড_ছিষ্টেম / 'user' / (নাম + '.o') for নাম in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = বিল্ড_ছিষ্টেম / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((বিল্ড_ছিষ্টেম / 'user/cc.elf').stat().st_size), 머리.read_text()))
        নিষ্পাদন_আদেশ([번역기] + বৈশিষ্ট্য + ['-c', বিল্ড_ছিষ্টেম / 'programs.S', '-o', 기준 / 'objects/programs.o'])
        নিষ্পাদন_আদেশ([번역기] + বৈশিষ্ট্য + ['-std=c11', '-I', 기준 / 'posix-kor/arm64-native/포함', '-I', বিল্ড_ছিষ্টেম,
             '-c', 기준 / 'মেচিন/ব্যৱহাৰকৰ্তা.c', '-o', 기준 / 'objects/user.o'])
    নিষ্পাদন_আদেশ([সংযোজক, '--gc-sections', '-T', 기준 / '부팅/লিংক_লেআউট.ld', '-o', 새묶음 / 'kernel.elf'] +
         [기준 / পথ for পথ in 명세['objects']] + ['--start-group'] +
         [নিৰাপত্তা_বাণ্ডল if পথ == 'objects/libassh.a' else 기준 / পথ for পথ in 명세['libraries']] + ['--end-group'])
    নিষ্পাদন_আদেশ([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    হেচ_ফাইল = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and হেচ_ফাইল != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + হেচ_ফাইল)
    print('RELINK PASS', হেচ_ফাইল, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    সঞ্চালন()
