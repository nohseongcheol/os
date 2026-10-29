#!/usr/bin/env python3
"""paskirstymas_VALUE 묶음에서 libassh/TinyCC를 교체하고 savas 커널을 kartoti_VALUE 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

Project_šaknis = Path(__file__).resolve().parent


def Vykdyti_komanda(Word_SMS):
    subprocess.check_call([str(įrašas_VALUE) for įrašas_VALUE in Word_SMS], cwd=str(Project_šaknis))


def Paleisti():
    analizatorius_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizatorius_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 patvirtinti')
    analizatorius_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a naudoti_VALUE')
    analizatorius_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 kartoti_VALUE 컴파일하고 커널에 탑재')
    analizatorius_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    Argumentai = analizatorius_48ee4b1b.parse_args()
    명세 = json.loads((Project_šaknis / 'relink.json').read_text())
    kompiliuoti_sistema = Project_šaknis / 'build'
    새묶음 = kompiliuoti_sistema / 'relinked'
    새묶음.mkdir(exist_ok=True)
    kompiliatorius_įrankis = os.environ.get('ARM64_CC', 'clang')
    Jungtis = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Archyvas_įrankis = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    nuotolinis_Parametrai = json.loads((kompiliuoti_sistema / 'remote/libassh-build.json').read_text())
    Nustatymai = nuotolinis_Parametrai['flags']
    if Argumentai.libassh_archive:
        Sauga_paketas = Argumentai.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', Project_šaknis / 'nuotolinis_VALUE', '-I', Project_šaknis / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Pavadinimas_2 in nuotolinis_Parametrai['sources']:
            vieta_VALUE = 새묶음 / (Path(Pavadinimas_2).stem + '.o')
            Vykdyti_komanda([kompiliatorius_įrankis] + Nustatymai + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', Project_šaknis / Pavadinimas_2, '-o', vieta_VALUE])
            목적들.append(vieta_VALUE)
        Sauga_paketas = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            Vykdyti_komanda([Archyvas_įrankis, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Sauga_paketas)
    if Argumentai.tinycc:
        if not Argumentai.sdk:
            analizatorius_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = Argumentai.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            analizatorius_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [žymėjimas_VALUE for žymėjimas_VALUE in Nustatymai if žymėjimas_VALUE != '-mgeneral-regs-only']
        vieta_VALUE = 새묶음 / 'kompiliatorius_įrankis.o'
        Vykdyti_komanda([kompiliatorius_įrankis] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', Project_šaknis / 'C_kompiliatorius', '-I', Project_šaknis / 'vendor/tinycc', '-I', Project_šaknis / 'naudotojas',
             '-I', kompiliuoti_sistema / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', Project_šaknis / 'C_kompiliatorius/kompiliatorius_įrankis.c', '-o', vieta_VALUE])
        Vykdyti_komanda([Jungtis, '--gc-sections', '-T', Project_šaknis / 'naudotojas/sieti_schema.ld', '-z', 'max-page-size=4096',
             '-o', kompiliuoti_sistema / 'user/cc.elf', kompiliuoti_sistema / 'user/start.o', kompiliuoti_sistema / 'user/runtime.o', vieta_VALUE] +
             [kompiliuoti_sistema / 'ccompiler' / (Pavadinimas_2 + '.o') for Pavadinimas_2 in ('CLR_pagalba', 'Paleisti', '미리번역', 'grąžinti_tiltas')] +
             [kompiliuoti_sistema / 'user' / (Pavadinimas_2 + '.o') for Pavadinimas_2 in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = kompiliuoti_sistema / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((kompiliuoti_sistema / 'user/cc.elf').stat().st_size), 머리.read_text()))
        Vykdyti_komanda([kompiliatorius_įrankis] + Nustatymai + ['-c', kompiliuoti_sistema / 'programs.S', '-o', Project_šaknis / 'objects/programs.o'])
        Vykdyti_komanda([kompiliatorius_įrankis] + Nustatymai + ['-std=c11', '-I', Project_šaknis / 'posix-kor/arm64-native/포함', '-I', kompiliuoti_sistema,
             '-c', Project_šaknis / 'mašina/naudotojas.c', '-o', Project_šaknis / 'objects/user.o'])
    Vykdyti_komanda([Jungtis, '--gc-sections', '-T', Project_šaknis / '부팅/sieti_schema.ld', '-o', 새묶음 / 'kernel.elf'] +
         [Project_šaknis / KELIAS for KELIAS in 명세['objects']] + ['--start-group'] +
         [Sauga_paketas if KELIAS == 'objects/libassh.a' else Project_šaknis / KELIAS for KELIAS in 명세['libraries']] + ['--end-group'])
    Vykdyti_komanda([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    maiša_Failas = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if Argumentai.verify and maiša_Failas != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + maiša_Failas)
    print('RELINK PASS', maiša_Failas, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Paleisti()
