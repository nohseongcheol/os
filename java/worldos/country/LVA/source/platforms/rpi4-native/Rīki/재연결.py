#!/usr/bin/env python3
"""sadale_VALUE 묶음에서 libassh/TinyCC를 교체하고 savs 커널을 mēģināt_vēlreiz_VALUE 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

Project_sakne = Path(__file__).resolve().parent


def Izpildīt_komanda(Word_SMS):
    subprocess.check_call([str(ievade_VALUE) for ievade_VALUE in Word_SMS], cwd=str(Project_sakne))


def Palaist():
    parsētājs_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parsētājs_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 verificēt')
    parsētājs_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a lietot_VALUE')
    parsētājs_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 mēģināt_vēlreiz_VALUE 컴파일하고 커널에 탑재')
    parsētājs_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    Parametri = parsētājs_48ee4b1b.parse_args()
    명세 = json.loads((Project_sakne / 'relink.json').read_text())
    būvējums_sistēma = Project_sakne / 'build'
    새묶음 = būvējums_sistēma / 'relinked'
    새묶음.mkdir(exist_ok=True)
    kompilators_rīks = os.environ.get('ARM64_CC', 'clang')
    Savienotājs = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Arhīvs_rīks = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    attāls_Iestatījumi = json.loads((būvējums_sistēma / 'remote/libassh-build.json').read_text())
    Uzstādījumi = attāls_Iestatījumi['flags']
    if Parametri.libassh_archive:
        Drošība_saistīt = Parametri.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', Project_sakne / 'attāls_VALUE', '-I', Project_sakne / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Nosaukums in attāls_Iestatījumi['sources']:
            mērķis_VALUE = 새묶음 / (Path(Nosaukums).stem + '.o')
            Izpildīt_komanda([kompilators_rīks] + Uzstādījumi + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', Project_sakne / Nosaukums, '-o', mērķis_VALUE])
            목적들.append(mērķis_VALUE)
        Drošība_saistīt = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            Izpildīt_komanda([Arhīvs_rīks, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Drošība_saistīt)
    if Parametri.tinycc:
        if not Parametri.sdk:
            parsētājs_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = Parametri.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            parsētājs_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [atlase_VALUE for atlase_VALUE in Uzstādījumi if atlase_VALUE != '-mgeneral-regs-only']
        mērķis_VALUE = 새묶음 / 'kompilators_rīks.o'
        Izpildīt_komanda([kompilators_rīks] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', Project_sakne / 'C_kompilators', '-I', Project_sakne / 'vendor/tinycc', '-I', Project_sakne / 'lietotājs',
             '-I', būvējums_sistēma / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', Project_sakne / 'C_kompilators/kompilators_rīks.c', '-o', mērķis_VALUE])
        Izpildīt_komanda([Savienotājs, '--gc-sections', '-T', Project_sakne / 'lietotājs/Saite_shēma.ld', '-z', 'max-page-size=4096',
             '-o', būvējums_sistēma / 'user/cc.elf', būvējums_sistēma / 'user/start.o', būvējums_sistēma / 'user/runtime.o', mērķis_VALUE] +
             [būvējums_sistēma / 'ccompiler' / (Nosaukums + '.o') for Nosaukums in ('CLR_Atbalsts', 'Palaist', '미리번역', 'atdot_tilts')] +
             [būvējums_sistēma / 'user' / (Nosaukums + '.o') for Nosaukums in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = būvējums_sistēma / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((būvējums_sistēma / 'user/cc.elf').stat().st_size), 머리.read_text()))
        Izpildīt_komanda([kompilators_rīks] + Uzstādījumi + ['-c', būvējums_sistēma / 'programs.S', '-o', Project_sakne / 'objects/programs.o'])
        Izpildīt_komanda([kompilators_rīks] + Uzstādījumi + ['-std=c11', '-I', Project_sakne / 'posix-kor/arm64-native/포함', '-I', būvējums_sistēma,
             '-c', Project_sakne / 'mašīna/lietotājs.c', '-o', Project_sakne / 'objects/user.o'])
    Izpildīt_komanda([Savienotājs, '--gc-sections', '-T', Project_sakne / '부팅/Saite_shēma.ld', '-o', 새묶음 / 'kernel.elf'] +
         [Project_sakne / CEĻŠ for CEĻŠ in 명세['objects']] + ['--start-group'] +
         [Drošība_saistīt if CEĻŠ == 'objects/libassh.a' else Project_sakne / CEĻŠ for CEĻŠ in 명세['libraries']] + ['--end-group'])
    Izpildīt_komanda([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    jaukšana_Fails = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if Parametri.verify and jaukšana_Fails != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + jaukšana_Fails)
    print('RELINK PASS', jaukšana_Fails, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Palaist()
