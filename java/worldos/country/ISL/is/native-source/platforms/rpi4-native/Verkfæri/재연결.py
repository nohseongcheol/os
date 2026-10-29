#!/usr/bin/env python3
"""dreifing_VALUE 묶음에서 libassh/TinyCC를 교체하고 eigin 커널을 다시 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

verk_rót = Path(__file__).resolve().parent


def keyra_skipun(Word_SMS):
    subprocess.check_call([str(færsla_VALUE) for færsla_VALUE in Word_SMS], cwd=str(verk_rót))


def Keyra_2():
    þáttari_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    þáttari_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 sannprófa')
    þáttari_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    þáttari_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    þáttari_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    Viðföng = þáttari_48ee4b1b.parse_args()
    명세 = json.loads((verk_rót / 'relink.json').read_text())
    smíð_kerfi = verk_rót / 'build'
    새묶음 = smíð_kerfi / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    Tengill = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Safn_verkfæri = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    fjartengdur_Stillingar = json.loads((smíð_kerfi / 'remote/libassh-build.json').read_text())
    Stillingar = fjartengdur_Stillingar['flags']
    if Viðföng.libassh_archive:
        Öryggi_búnt = Viðföng.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', verk_rót / 'fjartengdur_VALUE', '-I', verk_rót / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Heiti in fjartengdur_Stillingar['sources']:
            endastaður_VALUE = 새묶음 / (Path(Heiti).stem + '.o')
            keyra_skipun([번역기] + Stillingar + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', verk_rót / Heiti, '-o', endastaður_VALUE])
            목적들.append(endastaður_VALUE)
        Öryggi_búnt = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            keyra_skipun([Safn_verkfæri, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Öryggi_búnt)
    if Viðföng.tinycc:
        if not Viðföng.sdk:
            þáttari_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = Viðföng.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            þáttari_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [val_VALUE for val_VALUE in Stillingar if val_VALUE != '-mgeneral-regs-only']
        endastaður_VALUE = 새묶음 / '번역기.o'
        keyra_skipun([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', verk_rót / '시언어번역기', '-I', verk_rót / 'vendor/tinycc', '-I', verk_rót / 'notandi',
             '-I', smíð_kerfi / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', verk_rót / '시언어번역기/번역기.c', '-o', endastaður_VALUE])
        keyra_skipun([Tengill, '--gc-sections', '-T', verk_rót / 'notandi/tengja_útlit.ld', '-z', 'max-page-size=4096',
             '-o', smíð_kerfi / 'user/cc.elf', smíð_kerfi / 'user/start.o', smíð_kerfi / 'user/runtime.o', endastaður_VALUE] +
             [smíð_kerfi / 'ccompiler' / (Heiti + '.o') for Heiti in ('CLR_Aðstoð', 'Keyra_2', '미리번역', 'skila_brú')] +
             [smíð_kerfi / 'user' / (Heiti + '.o') for Heiti in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = smíð_kerfi / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((smíð_kerfi / 'user/cc.elf').stat().st_size), 머리.read_text()))
        keyra_skipun([번역기] + Stillingar + ['-c', smíð_kerfi / 'programs.S', '-o', verk_rót / 'objects/programs.o'])
        keyra_skipun([번역기] + Stillingar + ['-std=c11', '-I', verk_rót / 'posix-kor/arm64-native/포함', '-I', smíð_kerfi,
             '-c', verk_rót / 'vél/notandi.c', '-o', verk_rót / 'objects/user.o'])
    keyra_skipun([Tengill, '--gc-sections', '-T', verk_rót / '부팅/tengja_útlit.ld', '-o', 새묶음 / 'kernel.elf'] +
         [verk_rót / SLÓÐ for SLÓÐ in 명세['objects']] + ['--start-group'] +
         [Öryggi_búnt if SLÓÐ == 'objects/libassh.a' else verk_rót / SLÓÐ for SLÓÐ in 명세['libraries']] + ['--end-group'])
    keyra_skipun([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    tæting_skrá = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if Viðföng.verify and tæting_skrá != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + tæting_skrá)
    print('RELINK PASS', tæting_skrá, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Keyra_2()
