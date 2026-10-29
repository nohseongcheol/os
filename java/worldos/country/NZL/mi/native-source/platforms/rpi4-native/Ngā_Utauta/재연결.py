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

whakaatu_pūtake = Path(__file__).resolve().parent


def kawe_tono(Word_TEXT):
    subprocess.check_call([str(tāurunga_uara) for tāurunga_uara in Word_TEXT], cwd=str(whakaatu_pūtake))


def whakahaere():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 manatoko')
    해석기.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    해석기.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    해석기.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = 해석기.parse_args()
    명세 = json.loads((whakaatu_pūtake / 'relink.json').read_text())
    hanga_pūnaha = whakaatu_pūtake / 'build'
    새묶음 = hanga_pūnaha / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    pūtūhono = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Pūranga_utauta = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    mamao_Ngā_Tautuhinga = json.loads((hanga_pūnaha / 'remote/libassh-build.json').read_text())
    Ngā_Tautuhinga = mamao_Ngā_Tautuhinga['flags']
    if 인수.libassh_archive:
        Haumarutanga_pūpū = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', whakaatu_pūtake / 'mamao_uara', '-I', whakaatu_pūtake / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Ingoa in mamao_Ngā_Tautuhinga['sources']:
            ūnga_uara = 새묶음 / (Path(Ingoa).stem + '.o')
            kawe_tono([번역기] + Ngā_Tautuhinga + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', whakaatu_pūtake / Ingoa, '-o', ūnga_uara])
            목적들.append(ūnga_uara)
        Haumarutanga_pūpū = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            kawe_tono([Pūranga_utauta, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Haumarutanga_pūpū)
    if 인수.tinycc:
        if not 인수.sdk:
            해석기.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            해석기.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [tīpakonga_uara for tīpakonga_uara in Ngā_Tautuhinga if tīpakonga_uara != '-mgeneral-regs-only']
        ūnga_uara = 새묶음 / '번역기.o'
        kawe_tono([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', whakaatu_pūtake / '시언어번역기', '-I', whakaatu_pūtake / 'vendor/tinycc', '-I', whakaatu_pūtake / 'kaiwhakamahi',
             '-I', hanga_pūnaha / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', whakaatu_pūtake / '시언어번역기/번역기.c', '-o', ūnga_uara])
        kawe_tono([pūtūhono, '--gc-sections', '-T', whakaatu_pūtake / 'kaiwhakamahi/Hono_Tahora.ld', '-z', 'max-page-size=4096',
             '-o', hanga_pūnaha / 'user/cc.elf', hanga_pūnaha / 'user/start.o', hanga_pūnaha / 'user/runtime.o', ūnga_uara] +
             [hanga_pūnaha / 'ccompiler' / (Ingoa + '.o') for Ingoa in ('wāhaere_reo_noa_Tautoko', 'whakahaere', '미리번역', '되돌림')] +
             [hanga_pūnaha / 'user' / (Ingoa + '.o') for Ingoa in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = hanga_pūnaha / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((hanga_pūnaha / 'user/cc.elf').stat().st_size), 머리.read_text()))
        kawe_tono([번역기] + Ngā_Tautuhinga + ['-c', hanga_pūnaha / 'programs.S', '-o', whakaatu_pūtake / 'objects/programs.o'])
        kawe_tono([번역기] + Ngā_Tautuhinga + ['-std=c11', '-I', whakaatu_pūtake / 'posix-kor/arm64-native/포함', '-I', hanga_pūnaha,
             '-c', whakaatu_pūtake / 'mīhini/kaiwhakamahi.c', '-o', whakaatu_pūtake / 'objects/user.o'])
    kawe_tono([pūtūhono, '--gc-sections', '-T', whakaatu_pūtake / '부팅/Hono_Tahora.ld', '-o', 새묶음 / 'kernel.elf'] +
         [whakaatu_pūtake / ara for ara in 명세['objects']] + ['--start-group'] +
         [Haumarutanga_pūpū if ara == 'objects/libassh.a' else whakaatu_pūtake / ara for ara in 명세['libraries']] + ['--end-group'])
    kawe_tono([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    hash_kōnae = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and hash_kōnae != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + hash_kōnae)
    print('RELINK PASS', hash_kōnae, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    whakahaere()
