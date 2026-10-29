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

tilg_freumh = Path(__file__).resolve().parent


def gnìomhaich_àithne(Word_SMS):
    subprocess.check_call([str(cur_a_steach_VALUE) for cur_a_steach_VALUE in Word_SMS], cwd=str(tilg_freumh))


def ruith():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 dearbh')
    해석기.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    해석기.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    해석기.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = 해석기.parse_args()
    명세 = json.loads((tilg_freumh / 'relink.json').read_text())
    tog_siostam = tilg_freumh / 'build'
    새묶음 = tog_siostam / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    ceanglaiche = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    taisg_inneal = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    cian_roghainnean = json.loads((tog_siostam / 'remote/libassh-build.json').read_text())
    roghainnean = cian_roghainnean['flags']
    if 인수.libassh_archive:
        tèarainteachd_trusgan = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', tilg_freumh / 'cian_VALUE', '-I', tilg_freumh / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Ainm in cian_roghainnean['sources']:
            ceann_uidhe_VALUE = 새묶음 / (Path(Ainm).stem + '.o')
            gnìomhaich_àithne([번역기] + roghainnean + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', tilg_freumh / Ainm, '-o', ceann_uidhe_VALUE])
            목적들.append(ceann_uidhe_VALUE)
        tèarainteachd_trusgan = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            gnìomhaich_àithne([taisg_inneal, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(tèarainteachd_trusgan)
    if 인수.tinycc:
        if not 인수.sdk:
            해석기.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            해석기.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [taghadh_VALUE for taghadh_VALUE in roghainnean if taghadh_VALUE != '-mgeneral-regs-only']
        ceann_uidhe_VALUE = 새묶음 / '번역기.o'
        gnìomhaich_àithne([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', tilg_freumh / '시언어번역기', '-I', tilg_freumh / 'vendor/tinycc', '-I', tilg_freumh / 'cleachdaiche',
             '-I', tog_siostam / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', tilg_freumh / '시언어번역기/번역기.c', '-o', ceann_uidhe_VALUE])
        gnìomhaich_àithne([ceanglaiche, '--gc-sections', '-T', tilg_freumh / 'cleachdaiche/ceangal_co_dhealbhachd.ld', '-z', 'max-page-size=4096',
             '-o', tog_siostam / 'user/cc.elf', tog_siostam / 'user/start.o', tog_siostam / 'user/runtime.o', ceann_uidhe_VALUE] +
             [tog_siostam / 'ccompiler' / (Ainm + '.o') for Ainm in ('Common_Language_Runtime_taic', 'ruith', '미리번역', 'return_drochaid')] +
             [tog_siostam / 'user' / (Ainm + '.o') for Ainm in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = tog_siostam / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((tog_siostam / 'user/cc.elf').stat().st_size), 머리.read_text()))
        gnìomhaich_àithne([번역기] + roghainnean + ['-c', tog_siostam / 'programs.S', '-o', tilg_freumh / 'objects/programs.o'])
        gnìomhaich_àithne([번역기] + roghainnean + ['-std=c11', '-I', tilg_freumh / 'posix-kor/arm64-native/포함', '-I', tog_siostam,
             '-c', tilg_freumh / 'inneal/cleachdaiche.c', '-o', tilg_freumh / 'objects/user.o'])
    gnìomhaich_àithne([ceanglaiche, '--gc-sections', '-T', tilg_freumh / '부팅/ceangal_co_dhealbhachd.ld', '-o', 새묶음 / 'kernel.elf'] +
         [tilg_freumh / Slighe for Slighe in 명세['objects']] + ['--start-group'] +
         [tèarainteachd_trusgan if Slighe == 'objects/libassh.a' else tilg_freumh / Slighe for Slighe in 명세['libraries']] + ['--end-group'])
    gnìomhaich_àithne([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    hais_faidhle = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and hais_faidhle != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + hais_faidhle)
    print('RELINK PASS', hais_faidhle, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    ruith()
