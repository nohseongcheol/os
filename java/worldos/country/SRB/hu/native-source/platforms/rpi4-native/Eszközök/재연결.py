#!/usr/bin/env python3
"""elosztás_ÉRTÉK 묶음에서 libassh/TinyCC를 교체하고 saját 커널을 újrapróbál_ÉRTÉK 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

teendő_gyök = Path(__file__).resolve().parent


def végrehajt_parancs(szó_SMS):
    subprocess.check_call([str(bejegyzés_ÉRTÉK) for bejegyzés_ÉRTÉK in szó_SMS], cwd=str(teendő_gyök))


def Futtatás():
    elemző_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    elemző_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 igazol')
    elemző_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a használ_ÉRTÉK')
    elemző_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 újrapróbál_ÉRTÉK 컴파일하고 커널에 탑재')
    elemző_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    Argumentumok = elemző_48ee4b1b.parse_args()
    명세 = json.loads((teendő_gyök / 'relink.json').read_text())
    épít_Rendszer = teendő_gyök / 'build'
    새묶음 = épít_Rendszer / 'relinked'
    새묶음.mkdir(exist_ok=True)
    fordítóprogram_eszköz = os.environ.get('ARM64_CC', 'clang')
    Összekötő = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    archív_eszköz = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    távoli_Gépház = json.loads((épít_Rendszer / 'remote/libassh-build.json').read_text())
    Beállítások = távoli_Gépház['flags']
    if Argumentumok.libassh_archive:
        Biztonság_köteg = Argumentumok.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', teendő_gyök / 'távoli_ÉRTÉK', '-I', teendő_gyök / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Név in távoli_Gépház['sources']:
            cél_ÉRTÉK = 새묶음 / (Path(Név).stem + '.o')
            végrehajt_parancs([fordítóprogram_eszköz] + Beállítások + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', teendő_gyök / Név, '-o', cél_ÉRTÉK])
            목적들.append(cél_ÉRTÉK)
        Biztonság_köteg = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            végrehajt_parancs([archív_eszköz, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Biztonság_köteg)
    if Argumentumok.tinycc:
        if not Argumentumok.sdk:
            elemző_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = Argumentumok.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            elemző_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [kijelölés_ÉRTÉK for kijelölés_ÉRTÉK in Beállítások if kijelölés_ÉRTÉK != '-mgeneral-regs-only']
        cél_ÉRTÉK = 새묶음 / 'fordítóprogram_eszköz.o'
        végrehajt_parancs([fordítóprogram_eszköz] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', teendő_gyök / 'C_fordítóprogram', '-I', teendő_gyök / 'vendor/tinycc', '-I', teendő_gyök / 'felhasználó',
             '-I', épít_Rendszer / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', teendő_gyök / 'C_fordítóprogram/fordítóprogram_eszköz.c', '-o', cél_ÉRTÉK])
        végrehajt_parancs([Összekötő, '--gc-sections', '-T', teendő_gyök / 'felhasználó/csatol_Navigáció.ld', '-z', 'max-page-size=4096',
             '-o', épít_Rendszer / 'user/cc.elf', épít_Rendszer / 'user/start.o', épít_Rendszer / 'user/runtime.o', cél_ÉRTÉK] +
             [épít_Rendszer / 'ccompiler' / (Név + '.o') for Név in ('CLR_támogat', 'Futtatás', '미리번역', 'visszaküld_híd')] +
             [épít_Rendszer / 'user' / (Név + '.o') for Név in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = épít_Rendszer / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((épít_Rendszer / 'user/cc.elf').stat().st_size), 머리.read_text()))
        végrehajt_parancs([fordítóprogram_eszköz] + Beállítások + ['-c', épít_Rendszer / 'programs.S', '-o', teendő_gyök / 'objects/programs.o'])
        végrehajt_parancs([fordítóprogram_eszköz] + Beállítások + ['-std=c11', '-I', teendő_gyök / 'posix-kor/arm64-native/포함', '-I', épít_Rendszer,
             '-c', teendő_gyök / 'gép/felhasználó.c', '-o', teendő_gyök / 'objects/user.o'])
    végrehajt_parancs([Összekötő, '--gc-sections', '-T', teendő_gyök / '부팅/csatol_Navigáció.ld', '-o', 새묶음 / 'kernel.elf'] +
         [teendő_gyök / ÚTVONAL for ÚTVONAL in 명세['objects']] + ['--start-group'] +
         [Biztonság_köteg if ÚTVONAL == 'objects/libassh.a' else teendő_gyök / ÚTVONAL for ÚTVONAL in 명세['libraries']] + ['--end-group'])
    végrehajt_parancs([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    kivonat_Fájl = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if Argumentumok.verify and kivonat_Fájl != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + kivonat_Fájl)
    print('RELINK PASS', kivonat_Fájl, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Futtatás()
