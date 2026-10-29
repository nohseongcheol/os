#!/usr/bin/env python3
"""배포 묶음에서 libassh/TinyCC를 교체하고 propriu 커널을 reîncerca_VALUE 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

Project_rădăcină = Path(__file__).resolve().parent


def executa_comandă(Word_SMS):
    subprocess.check_call([str(intrare_VALUE) for intrare_VALUE in Word_SMS], cwd=str(Project_rădăcină))


def Pornește():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 verifica')
    parser_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a utiliza_VALUE')
    parser_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 reîncerca_VALUE 컴파일하고 커널에 탑재')
    parser_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    Argumente = parser_48ee4b1b.parse_args()
    명세 = json.loads((Project_rădăcină / 'relink.json').read_text())
    generare_sistem = Project_rădăcină / 'build'
    새묶음 = generare_sistem / 'relinked'
    새묶음.mkdir(exist_ok=True)
    compilator_instrument = os.environ.get('ARM64_CC', 'clang')
    Conector = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Arhivă_instrument = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    la_distanță_Setări = json.loads((generare_sistem / 'remote/libassh-build.json').read_text())
    Setări = la_distanță_Setări['flags']
    if Argumente.libassh_archive:
        Securitate_set = Argumente.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', Project_rădăcină / 'la_distanță_VALUE', '-I', Project_rădăcină / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Nume in la_distanță_Setări['sources']:
            destinație_VALUE = 새묶음 / (Path(Nume).stem + '.o')
            executa_comandă([compilator_instrument] + Setări + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', Project_rădăcină / Nume, '-o', destinație_VALUE])
            목적들.append(destinație_VALUE)
        Securitate_set = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            executa_comandă([Arhivă_instrument, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Securitate_set)
    if Argumente.tinycc:
        if not Argumente.sdk:
            parser_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = Argumente.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            parser_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [selecție_VALUE for selecție_VALUE in Setări if selecție_VALUE != '-mgeneral-regs-only']
        destinație_VALUE = 새묶음 / 'compilator_instrument.o'
        executa_comandă([compilator_instrument] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', Project_rădăcină / 'C_compilator', '-I', Project_rădăcină / 'vendor/tinycc', '-I', Project_rădăcină / 'utilizator',
             '-I', generare_sistem / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', Project_rădăcină / 'C_compilator/compilator_instrument.c', '-o', destinație_VALUE])
        executa_comandă([Conector, '--gc-sections', '-T', Project_rădăcină / 'utilizator/Link_Aspect.ld', '-z', 'max-page-size=4096',
             '-o', generare_sistem / 'user/cc.elf', generare_sistem / 'user/start.o', generare_sistem / 'user/runtime.o', destinație_VALUE] +
             [generare_sistem / 'ccompiler' / (Nume + '.o') for Nume in ('CLR_suport', 'Pornește', '미리번역', 'restitui_punte')] +
             [generare_sistem / 'user' / (Nume + '.o') for Nume in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = generare_sistem / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((generare_sistem / 'user/cc.elf').stat().st_size), 머리.read_text()))
        executa_comandă([compilator_instrument] + Setări + ['-c', generare_sistem / 'programs.S', '-o', Project_rădăcină / 'objects/programs.o'])
        executa_comandă([compilator_instrument] + Setări + ['-std=c11', '-I', Project_rădăcină / 'posix-kor/arm64-native/포함', '-I', generare_sistem,
             '-c', Project_rădăcină / 'mașină/utilizator.c', '-o', Project_rădăcină / 'objects/user.o'])
    executa_comandă([Conector, '--gc-sections', '-T', Project_rădăcină / '부팅/Link_Aspect.ld', '-o', 새묶음 / 'kernel.elf'] +
         [Project_rădăcină / Cale for Cale in 명세['objects']] + ['--start-group'] +
         [Securitate_set if Cale == 'objects/libassh.a' else Project_rădăcină / Cale for Cale in 명세['libraries']] + ['--end-group'])
    executa_comandă([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    cod_hash_Fișier = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if Argumente.verify and cod_hash_Fișier != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + cod_hash_Fișier)
    print('RELINK PASS', cod_hash_Fișier, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Pornește()
