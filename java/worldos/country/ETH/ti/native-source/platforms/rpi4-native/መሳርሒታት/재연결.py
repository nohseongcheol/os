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


def ተግብር_ትእዛዝ(ናይ_ቃል_ጸወታ_ጽሑፍ):
    subprocess.check_call([str(ምእታው_ዋጋ) for ምእታው_ዋጋ in ናይ_ቃል_ጸወታ_ጽሑፍ], cwd=str(기준))


def ኣኺድ():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 ኣረጋግጽ')
    해석기.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    해석기.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    해석기.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = 해석기.parse_args()
    명세 = json.loads((기준 / 'relink.json').read_text())
    ህነጽ_ስርዓት = 기준 / 'build'
    새묶음 = ህነጽ_ስርዓት / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    መላገቢ = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    ሰንድ_መሳርሒ = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    ርሑቕ_ኣቀማምጣታት = json.loads((ህነጽ_ስርዓት / 'remote/libassh-build.json').read_text())
    ኣቀማምጣታት = ርሑቕ_ኣቀማምጣታት['flags']
    if 인수.libassh_archive:
        ሓለዋ_ጥማር = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', 기준 / 'ርሑቕ_ዋጋ', '-I', 기준 / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for ሽም in ርሑቕ_ኣቀማምጣታት['sources']:
            መዓልቦ_ዋጋ = 새묶음 / (Path(ሽም).stem + '.o')
            ተግብር_ትእዛዝ([번역기] + ኣቀማምጣታት + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', 기준 / ሽም, '-o', መዓልቦ_ዋጋ])
            목적들.append(መዓልቦ_ዋጋ)
        ሓለዋ_ጥማር = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            ተግብር_ትእዛዝ([ሰንድ_መሳርሒ, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(ሓለዋ_ጥማር)
    if 인수.tinycc:
        if not 인수.sdk:
            해석기.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            해석기.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [ምሩጽ_ዋጋ for ምሩጽ_ዋጋ in ኣቀማምጣታት if ምሩጽ_ዋጋ != '-mgeneral-regs-only']
        መዓልቦ_ዋጋ = 새묶음 / '번역기.o'
        ተግብር_ትእዛዝ([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', 기준 / '시언어번역기', '-I', 기준 / 'vendor/tinycc', '-I', 기준 / 'ተጠቃሚ',
             '-I', ህነጽ_ስርዓት / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', 기준 / '시언어번역기/번역기.c', '-o', መዓልቦ_ዋጋ])
        ተግብር_ትእዛዝ([መላገቢ, '--gc-sections', '-T', 기준 / 'ተጠቃሚ/መጋጠሚ_ኣቀማምጣ.ld', '-z', 'max-page-size=4096',
             '-o', ህነጽ_ስርዓት / 'user/cc.elf', ህነጽ_ስርዓት / 'user/start.o', ህነጽ_ስርዓት / 'user/runtime.o', መዓልቦ_ዋጋ] +
             [ህነጽ_ስርዓት / 'ccompiler' / (ሽም + '.o') for ሽም in ('ግዜ_ስራሕ_ናይ_ሓባር_ቛንቛ_ሓገዝ', 'ኣኺድ', '미리번역', '되돌림')] +
             [ህነጽ_ስርዓት / 'user' / (ሽም + '.o') for ሽም in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = ህነጽ_ስርዓት / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((ህነጽ_ስርዓት / 'user/cc.elf').stat().st_size), 머리.read_text()))
        ተግብር_ትእዛዝ([번역기] + ኣቀማምጣታት + ['-c', ህነጽ_ስርዓት / 'programs.S', '-o', 기준 / 'objects/programs.o'])
        ተግብር_ትእዛዝ([번역기] + ኣቀማምጣታት + ['-std=c11', '-I', 기준 / 'posix-kor/arm64-native/포함', '-I', ህነጽ_ስርዓት,
             '-c', 기준 / 'ማሽን/ተጠቃሚ.c', '-o', 기준 / 'objects/user.o'])
    ተግብር_ትእዛዝ([መላገቢ, '--gc-sections', '-T', 기준 / '부팅/መጋጠሚ_ኣቀማምጣ.ld', '-o', 새묶음 / 'kernel.elf'] +
         [기준 / መገዲ for መገዲ in 명세['objects']] + ['--start-group'] +
         [ሓለዋ_ጥማር if መገዲ == 'objects/libassh.a' else 기준 / መገዲ for መገዲ in 명세['libraries']] + ['--end-group'])
    ተግብር_ትእዛዝ([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    해시 = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and 해시 != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + 해시)
    print('RELINK PASS', 해시, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    ኣኺድ()
