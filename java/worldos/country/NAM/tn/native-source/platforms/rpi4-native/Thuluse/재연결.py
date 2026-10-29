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


def diragatsa_Taelo(Lefoko_SMS):
    subprocess.check_call([str(tsenyo_Boleng) for tsenyo_Boleng in Lefoko_SMS], cwd=str(기준))


def dirisa():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 netefatsa')
    해석기.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    해석기.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    해석기.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = 해석기.parse_args()
    명세 = json.loads((기준 / 'relink.json').read_text())
    aga_tsamaiso = 기준 / 'build'
    새묶음 = aga_tsamaiso / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    segolaganyi = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    boloka_sediriswa = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    kgakala_Diseting = json.loads((aga_tsamaiso / 'remote/libassh-build.json').read_text())
    Diseting = kgakala_Diseting['flags']
    if 인수.libassh_archive:
        tshireletso_ngatanngwe = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', 기준 / 'kgakala_Boleng', '-I', 기준 / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for leina in kgakala_Diseting['sources']:
            bogorogelo_Boleng = 새묶음 / (Path(leina).stem + '.o')
            diragatsa_Taelo([번역기] + Diseting + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', 기준 / leina, '-o', bogorogelo_Boleng])
            목적들.append(bogorogelo_Boleng)
        tshireletso_ngatanngwe = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            diragatsa_Taelo([boloka_sediriswa, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(tshireletso_ngatanngwe)
    if 인수.tinycc:
        if not 인수.sdk:
            해석기.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            해석기.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [tlhopho_Boleng for tlhopho_Boleng in Diseting if tlhopho_Boleng != '-mgeneral-regs-only']
        bogorogelo_Boleng = 새묶음 / '번역기.o'
        diragatsa_Taelo([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', 기준 / '시언어번역기', '-I', 기준 / 'vendor/tinycc', '-I', 기준 / 'modirisi',
             '-I', aga_tsamaiso / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', 기준 / '시언어번역기/번역기.c', '-o', bogorogelo_Boleng])
        diragatsa_Taelo([segolaganyi, '--gc-sections', '-T', 기준 / 'modirisi/Kgokagano_Boalo.ld', '-z', 'max-page-size=4096',
             '-o', aga_tsamaiso / 'user/cc.elf', aga_tsamaiso / 'user/start.o', aga_tsamaiso / 'user/runtime.o', bogorogelo_Boleng] +
             [aga_tsamaiso / 'ccompiler' / (leina + '.o') for leina in ('nakotsamaiso_ya_puo_e_e_tlwaelegileng_Thuso', 'dirisa', '미리번역', '되돌림')] +
             [aga_tsamaiso / 'user' / (leina + '.o') for leina in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = aga_tsamaiso / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((aga_tsamaiso / 'user/cc.elf').stat().st_size), 머리.read_text()))
        diragatsa_Taelo([번역기] + Diseting + ['-c', aga_tsamaiso / 'programs.S', '-o', 기준 / 'objects/programs.o'])
        diragatsa_Taelo([번역기] + Diseting + ['-std=c11', '-I', 기준 / 'posix-kor/arm64-native/포함', '-I', aga_tsamaiso,
             '-c', 기준 / 'motšhine/modirisi.c', '-o', 기준 / 'objects/user.o'])
    diragatsa_Taelo([segolaganyi, '--gc-sections', '-T', 기준 / '부팅/Kgokagano_Boalo.ld', '-o', 새묶음 / 'kernel.elf'] +
         [기준 / tsela for tsela in 명세['objects']] + ['--start-group'] +
         [tshireletso_ngatanngwe if tsela == 'objects/libassh.a' else 기준 / tsela for tsela in 명세['libraries']] + ['--end-group'])
    diragatsa_Taelo([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    heše_faele = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and heše_faele != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + heše_faele)
    print('RELINK PASS', heše_faele, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    dirisa()
