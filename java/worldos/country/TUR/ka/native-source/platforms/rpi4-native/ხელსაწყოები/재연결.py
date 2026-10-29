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

პროეცირება_ფესვი = Path(__file__).resolve().parent


def შესრულება_ბრძანება(სიტყვები_ტექსტი):
    subprocess.check_call([str(შენატანი_მნიშვნელობა) for შენატანი_მნიშვნელობა in სიტყვები_ტექსტი], cwd=str(პროეცირება_ფესვი))


def გაშვება():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 გადამოწმება')
    해석기.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    해석기.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    해석기.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = 해석기.parse_args()
    명세 = json.loads((პროეცირება_ფესვი / 'relink.json').read_text())
    აწყობა_სისტემა = პროეცირება_ფესვი / 'build'
    새묶음 = აწყობა_სისტემა / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    მაერთებელი = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    არქივი_ხელსაწყო = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    დისტანციური_პარამეტრები = json.loads((აწყობა_სისტემა / 'remote/libassh-build.json').read_text())
    პარამეტრები = დისტანციური_პარამეტრები['flags']
    if 인수.libassh_archive:
        უსაფრთხოება_შეკვრა = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', პროეცირება_ფესვი / 'დისტანციური_მნიშვნელობა', '-I', პროეცირება_ფესვი / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for სახელი in დისტანციური_პარამეტრები['sources']:
            მიმართულება_მნიშვნელობა = 새묶음 / (Path(სახელი).stem + '.o')
            შესრულება_ბრძანება([번역기] + პარამეტრები + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', პროეცირება_ფესვი / სახელი, '-o', მიმართულება_მნიშვნელობა])
            목적들.append(მიმართულება_მნიშვნელობა)
        უსაფრთხოება_შეკვრა = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            შესრულება_ბრძანება([არქივი_ხელსაწყო, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(უსაფრთხოება_შეკვრა)
    if 인수.tinycc:
        if not 인수.sdk:
            해석기.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            해석기.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [მონიშნული_ობიექტი_მნიშვნელობა for მონიშნული_ობიექტი_მნიშვნელობა in პარამეტრები if მონიშნული_ობიექტი_მნიშვნელობა != '-mgeneral-regs-only']
        მიმართულება_მნიშვნელობა = 새묶음 / '번역기.o'
        შესრულება_ბრძანება([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', პროეცირება_ფესვი / '시언어번역기', '-I', პროეცირება_ფესვი / 'vendor/tinycc', '-I', პროეცირება_ფესვი / 'მომხმარებელი',
             '-I', აწყობა_სისტემა / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', პროეცირება_ფესვი / '시언어번역기/번역기.c', '-o', მიმართულება_მნიშვნელობა])
        შესრულება_ბრძანება([მაერთებელი, '--gc-sections', '-T', პროეცირება_ფესვი / 'მომხმარებელი/ბმული_განლაგება.ld', '-z', 'max-page-size=4096',
             '-o', აწყობა_სისტემა / 'user/cc.elf', აწყობა_სისტემა / 'user/start.o', აწყობა_სისტემა / 'user/runtime.o', მიმართულება_მნიშვნელობა] +
             [აწყობა_სისტემა / 'ccompiler' / (სახელი + '.o') for სახელი in ('საერთო_ენობრივი_გარემო_მხარდაჭერა', 'გაშვება', '미리번역', 'დაბრუნება_ხიდი')] +
             [აწყობა_სისტემა / 'user' / (სახელი + '.o') for სახელი in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = აწყობა_სისტემა / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((აწყობა_სისტემა / 'user/cc.elf').stat().st_size), 머리.read_text()))
        შესრულება_ბრძანება([번역기] + პარამეტრები + ['-c', აწყობა_სისტემა / 'programs.S', '-o', პროეცირება_ფესვი / 'objects/programs.o'])
        შესრულება_ბრძანება([번역기] + პარამეტრები + ['-std=c11', '-I', პროეცირება_ფესვი / 'posix-kor/arm64-native/포함', '-I', აწყობა_სისტემა,
             '-c', პროეცირება_ფესვი / 'კომპიუტერი/მომხმარებელი.c', '-o', პროეცირება_ფესვი / 'objects/user.o'])
    შესრულება_ბრძანება([მაერთებელი, '--gc-sections', '-T', პროეცირება_ფესვი / '부팅/ბმული_განლაგება.ld', '-o', 새묶음 / 'kernel.elf'] +
         [პროეცირება_ფესვი / გეზი for გეზი in 명세['objects']] + ['--start-group'] +
         [უსაფრთხოება_შეკვრა if გეზი == 'objects/libassh.a' else პროეცირება_ფესვი / გეზი for გეზი in 명세['libraries']] + ['--end-group'])
    შესრულება_ბრძანება([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    ჰეში_ფაილი = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and ჰეში_ფაილი != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + ჰეში_ფაილი)
    print('RELINK PASS', ჰეში_ფაილი, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    გაშვება()
