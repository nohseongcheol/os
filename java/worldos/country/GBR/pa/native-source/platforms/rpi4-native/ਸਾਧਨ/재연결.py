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

ਪ੍ਰੋਜੈਕਟ_ਰੂਟ = Path(__file__).resolve().parent


def ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(ਸ਼ਬਦ_ਪਾਠ):
    subprocess.check_call([str(ਦਾਖਲਾ_ਕੀਮਤ) for ਦਾਖਲਾ_ਕੀਮਤ in ਸ਼ਬਦ_ਪਾਠ], cwd=str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ))


def ਚਲਾਓ_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 ਤਸਦੀਕ')
    해석기.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    해석기.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    해석기.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    ਆਰਗੂਮੈਂਟ = 해석기.parse_args()
    명세 = json.loads((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'relink.json').read_text())
    ਬਿਲਡ_ਪਰਬੰਧ = ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build'
    새묶음 = ਬਿਲਡ_ਪਰਬੰਧ / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    ਕਨੈਕਟਰ = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    ਸੰਗ੍ਰਹਿ_ਸਾਧਨ = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    ਰਿਮੋਟ_ਸੈਟਿੰਗਾਂ = json.loads((ਬਿਲਡ_ਪਰਬੰਧ / 'remote/libassh-build.json').read_text())
    ਸੈਟਿੰਗ = ਰਿਮੋਟ_ਸੈਟਿੰਗਾਂ['flags']
    if ਆਰਗੂਮੈਂਟ.libassh_archive:
        ਸੁਰੱਖਿਆ_ਬੰਡਲ = ਆਰਗੂਮੈਂਟ.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'ਰਿਮੋਟ_ਕੀਮਤ', '-I', ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for ਨਾਂ in ਰਿਮੋਟ_ਸੈਟਿੰਗਾਂ['sources']:
            ਮੰਜਿਲ_ਕੀਮਤ = 새묶음 / (Path(ਨਾਂ).stem + '.o')
            ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼([번역기] + ਸੈਟਿੰਗ + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / ਨਾਂ, '-o', ਮੰਜਿਲ_ਕੀਮਤ])
            목적들.append(ਮੰਜਿਲ_ਕੀਮਤ)
        ਸੁਰੱਖਿਆ_ਬੰਡਲ = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼([ਸੰਗ੍ਰਹਿ_ਸਾਧਨ, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(ਸੁਰੱਖਿਆ_ਬੰਡਲ)
    if ਆਰਗੂਮੈਂਟ.tinycc:
        if not ਆਰਗੂਮੈਂਟ.sdk:
            해석기.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = ਆਰਗੂਮੈਂਟ.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            해석기.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [ਚੋਣ_ਕੀਮਤ for ਚੋਣ_ਕੀਮਤ in ਸੈਟਿੰਗ if ਚੋਣ_ਕੀਮਤ != '-mgeneral-regs-only']
        ਮੰਜਿਲ_ਕੀਮਤ = 새묶음 / '번역기.o'
        ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / '시언어번역기', '-I', ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'vendor/tinycc', '-I', ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'ਉਪਭੋਗਤਾ',
             '-I', ਬਿਲਡ_ਪਰਬੰਧ / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / '시언어번역기/번역기.c', '-o', ਮੰਜਿਲ_ਕੀਮਤ])
        ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼([ਕਨੈਕਟਰ, '--gc-sections', '-T', ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'ਉਪਭੋਗਤਾ/ਲਿੰਕ_ਖਾਕਾ.ld', '-z', 'max-page-size=4096',
             '-o', ਬਿਲਡ_ਪਰਬੰਧ / 'user/cc.elf', ਬਿਲਡ_ਪਰਬੰਧ / 'user/start.o', ਬਿਲਡ_ਪਰਬੰਧ / 'user/runtime.o', ਮੰਜਿਲ_ਕੀਮਤ] +
             [ਬਿਲਡ_ਪਰਬੰਧ / 'ccompiler' / (ਨਾਂ + '.o') for ਨਾਂ in ('ਸਾਧਾਰਨ_ਭਾਸ਼ਾ_ਰਨਟਾਈਮ_ਸਮਰਥਨ', 'ਚਲਾਓ_2', '미리번역', '되돌림')] +
             [ਬਿਲਡ_ਪਰਬੰਧ / 'user' / (ਨਾਂ + '.o') for ਨਾਂ in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = ਬਿਲਡ_ਪਰਬੰਧ / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((ਬਿਲਡ_ਪਰਬੰਧ / 'user/cc.elf').stat().st_size), 머리.read_text()))
        ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼([번역기] + ਸੈਟਿੰਗ + ['-c', ਬਿਲਡ_ਪਰਬੰਧ / 'programs.S', '-o', ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'objects/programs.o'])
        ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼([번역기] + ਸੈਟਿੰਗ + ['-std=c11', '-I', ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'posix-kor/arm64-native/포함', '-I', ਬਿਲਡ_ਪਰਬੰਧ,
             '-c', ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'ਮਸ਼ੀਨ/ਉਪਭੋਗਤਾ.c', '-o', ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'objects/user.o'])
    ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼([ਕਨੈਕਟਰ, '--gc-sections', '-T', ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / '부팅/ਲਿੰਕ_ਖਾਕਾ.ld', '-o', 새묶음 / 'kernel.elf'] +
         [ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / ਮਾਰਗ for ਮਾਰਗ in 명세['objects']] + ['--start-group'] +
         [ਸੁਰੱਖਿਆ_ਬੰਡਲ if ਮਾਰਗ == 'objects/libassh.a' else ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / ਮਾਰਗ for ਮਾਰਗ in 명세['libraries']] + ['--end-group'])
    ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    ਹੈਸ਼_ਲਿਖਤ_ਪੱਤਰ = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if ਆਰਗੂਮੈਂਟ.verify and ਹੈਸ਼_ਲਿਖਤ_ਪੱਤਰ != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + ਹੈਸ਼_ਲਿਖਤ_ਪੱਤਰ)
    print('RELINK PASS', ਹੈਸ਼_ਲਿਖਤ_ਪੱਤਰ, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    ਚਲਾਓ_2()
