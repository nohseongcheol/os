#!/usr/bin/env python3
"""배포 묶음에서 libassh/TinyCC를 교체하고 নিজ 커널을 다시 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

প্রকল্প_মূল = Path(__file__).resolve().parent


def কার্যকর_করুন_আদেশ(শব্দ_পাঠ):
    subprocess.check_call([str(ভুক্তি_মান) for ভুক্তি_মান in শব্দ_পাঠ], cwd=str(প্রকল্প_মূল))


def চালনা():
    পার্সার_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    পার্সার_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 যাচাই_করা')
    পার্সার_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    পার্সার_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    পার্সার_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    আর্গুমেন্ট_তালিকা = পার্সার_48ee4b1b.parse_args()
    명세 = json.loads((প্রকল্প_মূল / 'relink.json').read_text())
    গঠন_সিস্টেম = প্রকল্প_মূল / 'build'
    새묶음 = গঠন_সিস্টেম / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    সংযোজক = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    সংগ্রহ_করা_টুল = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    দূরবর্তী_সেটিংস = json.loads((গঠন_সিস্টেম / 'remote/libassh-build.json').read_text())
    সেটিংস = দূরবর্তী_সেটিংস['flags']
    if আর্গুমেন্ট_তালিকা.libassh_archive:
        নিরাপত্তা_পাঁজা = আর্গুমেন্ট_তালিকা.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', প্রকল্প_মূল / 'দূরবর্তী_মান', '-I', প্রকল্প_মূল / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for নাম in দূরবর্তী_সেটিংস['sources']:
            গন্তব্য_মান = 새묶음 / (Path(নাম).stem + '.o')
            কার্যকর_করুন_আদেশ([번역기] + সেটিংস + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', প্রকল্প_মূল / নাম, '-o', গন্তব্য_মান])
            목적들.append(গন্তব্য_মান)
        নিরাপত্তা_পাঁজা = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            কার্যকর_করুন_আদেশ([সংগ্রহ_করা_টুল, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(নিরাপত্তা_পাঁজা)
    if আর্গুমেন্ট_তালিকা.tinycc:
        if not আর্গুমেন্ট_তালিকা.sdk:
            পার্সার_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = আর্গুমেন্ট_তালিকা.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            পার্সার_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [বাছাই_মান for বাছাই_মান in সেটিংস if বাছাই_মান != '-mgeneral-regs-only']
        গন্তব্য_মান = 새묶음 / '번역기.o'
        কার্যকর_করুন_আদেশ([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', প্রকল্প_মূল / '시언어번역기', '-I', প্রকল্প_মূল / 'vendor/tinycc', '-I', প্রকল্প_মূল / 'ব্যবহারকারী',
             '-I', গঠন_সিস্টেম / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', প্রকল্প_মূল / '시언어번역기/번역기.c', '-o', গন্তব্য_মান])
        কার্যকর_করুন_আদেশ([সংযোজক, '--gc-sections', '-T', প্রকল্প_মূল / 'ব্যবহারকারী/লিংক_লেআউট.ld', '-z', 'max-page-size=4096',
             '-o', গঠন_সিস্টেম / 'user/cc.elf', গঠন_সিস্টেম / 'user/start.o', গঠন_সিস্টেম / 'user/runtime.o', গন্তব্য_মান] +
             [গঠন_সিস্টেম / 'ccompiler' / (নাম + '.o') for নাম in ('সাধারণ_ভাষা_রানটাইম_সমর্থন', 'চালনা', '미리번역', '되돌림')] +
             [গঠন_সিস্টেম / 'user' / (নাম + '.o') for নাম in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = গঠন_সিস্টেম / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((গঠন_সিস্টেম / 'user/cc.elf').stat().st_size), 머리.read_text()))
        কার্যকর_করুন_আদেশ([번역기] + সেটিংস + ['-c', গঠন_সিস্টেম / 'programs.S', '-o', প্রকল্প_মূল / 'objects/programs.o'])
        কার্যকর_করুন_আদেশ([번역기] + সেটিংস + ['-std=c11', '-I', প্রকল্প_মূল / 'posix-kor/arm64-native/포함', '-I', গঠন_সিস্টেম,
             '-c', প্রকল্প_মূল / 'মেশিন/ব্যবহারকারী.c', '-o', প্রকল্প_মূল / 'objects/user.o'])
    কার্যকর_করুন_আদেশ([সংযোজক, '--gc-sections', '-T', প্রকল্প_মূল / '부팅/লিংক_লেআউট.ld', '-o', 새묶음 / 'kernel.elf'] +
         [প্রকল্প_মূল / পথ_2 for পথ_2 in 명세['objects']] + ['--start-group'] +
         [নিরাপত্তা_পাঁজা if পথ_2 == 'objects/libassh.a' else প্রকল্প_মূল / পথ_2 for পথ_2 in 명세['libraries']] + ['--end-group'])
    কার্যকর_করুন_আদেশ([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    হ্যাশ_ফাইল = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if আর্গুমেন্ট_তালিকা.verify and হ্যাশ_ফাইল != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + হ্যাশ_ফাইল)
    print('RELINK PASS', হ্যাশ_ফাইল, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    চালনা()
