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

ಬಿಂಬಿಸು_ಮೂಲ = Path(__file__).resolve().parent


def ಪೂರೈಸು_ಆದೇಶ(ಪದ_ಪಠ್ಯ):
    subprocess.check_call([str(ನಮೂದು_ಮೌಲ್ಯ) for ನಮೂದು_ಮೌಲ್ಯ in ಪದ_ಪಠ್ಯ], cwd=str(ಬಿಂಬಿಸು_ಮೂಲ))


def ಚಲಾಯಿಸು_2():
    ಪಾರ್ಸರ್_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ಪಾರ್ಸರ್_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು')
    ಪಾರ್ಸರ್_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    ಪಾರ್ಸರ್_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    ಪಾರ್ಸರ್_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = ಪಾರ್ಸರ್_48ee4b1b.parse_args()
    명세 = json.loads((ಬಿಂಬಿಸು_ಮೂಲ / 'relink.json').read_text())
    ಬಿಲ್ಡ್_ಸಿಸ್ಟಂ = ಬಿಂಬಿಸು_ಮೂಲ / 'build'
    새묶음 = ಬಿಲ್ಡ್_ಸಿಸ್ಟಂ / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    ಜೋಡಿಸುವವ = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    ಅರ್ಖೀವ್_ಪರಿಕರ = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    ರಿಮೋಟ್_ಸೆಟ್ಟಿಂಗ್ಸ್ = json.loads((ಬಿಲ್ಡ್_ಸಿಸ್ಟಂ / 'remote/libassh-build.json').read_text())
    ಸಿದ್ಧತೆಗಳು = ರಿಮೋಟ್_ಸೆಟ್ಟಿಂಗ್ಸ್['flags']
    if 인수.libassh_archive:
        ಭದ್ರತೆ_ಬಂಡಲ್ = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', ಬಿಂಬಿಸು_ಮೂಲ / 'ರಿಮೋಟ್_ಮೌಲ್ಯ', '-I', ಬಿಂಬಿಸು_ಮೂಲ / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for ಹೆಸರು in ರಿಮೋಟ್_ಸೆಟ್ಟಿಂಗ್ಸ್['sources']:
            ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ = 새묶음 / (Path(ಹೆಸರು).stem + '.o')
            ಪೂರೈಸು_ಆದೇಶ([번역기] + ಸಿದ್ಧತೆಗಳು + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', ಬಿಂಬಿಸು_ಮೂಲ / ಹೆಸರು, '-o', ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ])
            목적들.append(ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ)
        ಭದ್ರತೆ_ಬಂಡಲ್ = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            ಪೂರೈಸು_ಆದೇಶ([ಅರ್ಖೀವ್_ಪರಿಕರ, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(ಭದ್ರತೆ_ಬಂಡಲ್)
    if 인수.tinycc:
        if not 인수.sdk:
            ಪಾರ್ಸರ್_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            ಪಾರ್ಸರ್_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [ಆಯ್ಕೆ_ಮೌಲ್ಯ for ಆಯ್ಕೆ_ಮೌಲ್ಯ in ಸಿದ್ಧತೆಗಳು if ಆಯ್ಕೆ_ಮೌಲ್ಯ != '-mgeneral-regs-only']
        ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ = 새묶음 / '번역기.o'
        ಪೂರೈಸು_ಆದೇಶ([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', ಬಿಂಬಿಸು_ಮೂಲ / '시언어번역기', '-I', ಬಿಂಬಿಸು_ಮೂಲ / 'vendor/tinycc', '-I', ಬಿಂಬಿಸು_ಮೂಲ / 'ಬಳಕೆದಾರ',
             '-I', ಬಿಲ್ಡ್_ಸಿಸ್ಟಂ / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', ಬಿಂಬಿಸು_ಮೂಲ / '시언어번역기/번역기.c', '-o', ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ])
        ಪೂರೈಸು_ಆದೇಶ([ಜೋಡಿಸುವವ, '--gc-sections', '-T', ಬಿಂಬಿಸು_ಮೂಲ / 'ಬಳಕೆದಾರ/ಜೋಡಣೆ_ಲೇಔಟ್.ld', '-z', 'max-page-size=4096',
             '-o', ಬಿಲ್ಡ್_ಸಿಸ್ಟಂ / 'user/cc.elf', ಬಿಲ್ಡ್_ಸಿಸ್ಟಂ / 'user/start.o', ಬಿಲ್ಡ್_ಸಿಸ್ಟಂ / 'user/runtime.o', ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ] +
             [ಬಿಲ್ಡ್_ಸಿಸ್ಟಂ / 'ccompiler' / (ಹೆಸರು + '.o') for ಹೆಸರು in ('ಸಾಮಾನ್ಯ_ಭಾಷೆಯ_ಚಾಲ್ತಿ_ಸಮಯ_ಬೆಂಬಲ', 'ಚಲಾಯಿಸು_2', '미리번역', '되돌림')] +
             [ಬಿಲ್ಡ್_ಸಿಸ್ಟಂ / 'user' / (ಹೆಸರು + '.o') for ಹೆಸರು in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = ಬಿಲ್ಡ್_ಸಿಸ್ಟಂ / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((ಬಿಲ್ಡ್_ಸಿಸ್ಟಂ / 'user/cc.elf').stat().st_size), 머리.read_text()))
        ಪೂರೈಸು_ಆದೇಶ([번역기] + ಸಿದ್ಧತೆಗಳು + ['-c', ಬಿಲ್ಡ್_ಸಿಸ್ಟಂ / 'programs.S', '-o', ಬಿಂಬಿಸು_ಮೂಲ / 'objects/programs.o'])
        ಪೂರೈಸು_ಆದೇಶ([번역기] + ಸಿದ್ಧತೆಗಳು + ['-std=c11', '-I', ಬಿಂಬಿಸು_ಮೂಲ / 'posix-kor/arm64-native/포함', '-I', ಬಿಲ್ಡ್_ಸಿಸ್ಟಂ,
             '-c', ಬಿಂಬಿಸು_ಮೂಲ / 'ಯಂತ್ರ/ಬಳಕೆದಾರ.c', '-o', ಬಿಂಬಿಸು_ಮೂಲ / 'objects/user.o'])
    ಪೂರೈಸು_ಆದೇಶ([ಜೋಡಿಸುವವ, '--gc-sections', '-T', ಬಿಂಬಿಸು_ಮೂಲ / '부팅/ಜೋಡಣೆ_ಲೇಔಟ್.ld', '-o', 새묶음 / 'kernel.elf'] +
         [ಬಿಂಬಿಸು_ಮೂಲ / ಮಾರ್ಗ for ಮಾರ್ಗ in 명세['objects']] + ['--start-group'] +
         [ಭದ್ರತೆ_ಬಂಡಲ್ if ಮಾರ್ಗ == 'objects/libassh.a' else ಬಿಂಬಿಸು_ಮೂಲ / ಮಾರ್ಗ for ಮಾರ್ಗ in 명세['libraries']] + ['--end-group'])
    ಪೂರೈಸು_ಆದೇಶ([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    ಹ್ಯಾಶ್_ಫೈಲ್ = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and ಹ್ಯಾಶ್_ಫೈಲ್ != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + ಹ್ಯಾಶ್_ಫೈಲ್)
    print('RELINK PASS', ಹ್ಯಾಶ್_ಫೈಲ್, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    ಚಲಾಯಿಸು_2()
