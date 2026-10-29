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

prosiect_gwraidd = Path(__file__).resolve().parent


def Gweithredu_gorchymyn(Word_SMS):
    subprocess.check_call([str(cofnod_VALUE) for cofnod_VALUE in Word_SMS], cwd=str(prosiect_gwraidd))


def Gweithredu_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 dilysu')
    해석기.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    해석기.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    해석기.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = 해석기.parse_args()
    명세 = json.loads((prosiect_gwraidd / 'relink.json').read_text())
    llunio_system = prosiect_gwraidd / 'build'
    새묶음 = llunio_system / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    cysylltydd = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Archif_offeryn = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    pell_Gosodiadau = json.loads((llunio_system / 'remote/libassh-build.json').read_text())
    Gosodiadau = pell_Gosodiadau['flags']
    if 인수.libassh_archive:
        Diogelwch_bwndel = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', prosiect_gwraidd / 'pell_VALUE', '-I', prosiect_gwraidd / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Enw in pell_Gosodiadau['sources']:
            cyrchfan_VALUE = 새묶음 / (Path(Enw).stem + '.o')
            Gweithredu_gorchymyn([번역기] + Gosodiadau + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', prosiect_gwraidd / Enw, '-o', cyrchfan_VALUE])
            목적들.append(cyrchfan_VALUE)
        Diogelwch_bwndel = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            Gweithredu_gorchymyn([Archif_offeryn, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Diogelwch_bwndel)
    if 인수.tinycc:
        if not 인수.sdk:
            해석기.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            해석기.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [dewisiad_VALUE for dewisiad_VALUE in Gosodiadau if dewisiad_VALUE != '-mgeneral-regs-only']
        cyrchfan_VALUE = 새묶음 / '번역기.o'
        Gweithredu_gorchymyn([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', prosiect_gwraidd / '시언어번역기', '-I', prosiect_gwraidd / 'vendor/tinycc', '-I', prosiect_gwraidd / 'defnyddiwr',
             '-I', llunio_system / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', prosiect_gwraidd / '시언어번역기/번역기.c', '-o', cyrchfan_VALUE])
        Gweithredu_gorchymyn([cysylltydd, '--gc-sections', '-T', prosiect_gwraidd / 'defnyddiwr/Dolen_Llywio.ld', '-z', 'max-page-size=4096',
             '-o', llunio_system / 'user/cc.elf', llunio_system / 'user/start.o', llunio_system / 'user/runtime.o', cyrchfan_VALUE] +
             [llunio_system / 'ccompiler' / (Enw + '.o') for Enw in ('amser_rhedeg_iaith_gyffredin_Cymorth', 'Gweithredu_2', '미리번역', 'return_pont')] +
             [llunio_system / 'user' / (Enw + '.o') for Enw in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = llunio_system / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((llunio_system / 'user/cc.elf').stat().st_size), 머리.read_text()))
        Gweithredu_gorchymyn([번역기] + Gosodiadau + ['-c', llunio_system / 'programs.S', '-o', prosiect_gwraidd / 'objects/programs.o'])
        Gweithredu_gorchymyn([번역기] + Gosodiadau + ['-std=c11', '-I', prosiect_gwraidd / 'posix-kor/arm64-native/포함', '-I', llunio_system,
             '-c', prosiect_gwraidd / 'peiriant/defnyddiwr.c', '-o', prosiect_gwraidd / 'objects/user.o'])
    Gweithredu_gorchymyn([cysylltydd, '--gc-sections', '-T', prosiect_gwraidd / '부팅/Dolen_Llywio.ld', '-o', 새묶음 / 'kernel.elf'] +
         [prosiect_gwraidd / LLWYBR for LLWYBR in 명세['objects']] + ['--start-group'] +
         [Diogelwch_bwndel if LLWYBR == 'objects/libassh.a' else prosiect_gwraidd / LLWYBR for LLWYBR in 명세['libraries']] + ['--end-group'])
    Gweithredu_gorchymyn([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    hash_ffeil = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and hash_ffeil != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + hash_ffeil)
    print('RELINK PASS', hash_ffeil, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Gweithredu_2()
