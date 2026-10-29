#!/usr/bin/env python3
"""distributie_WAARDE 묶음에서 libassh/TinyCC를 교체하고 Eigen 커널을 opnieuw_proberen_WAARDE 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

Taken_wortel = Path(__file__).resolve().parent


def Uitvoeren_opdracht(Word_sms):
    subprocess.check_call([str(invoer_WAARDE_962f286b) for invoer_WAARDE_962f286b in Word_sms], cwd=str(Taken_wortel))


def starten():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 bevestigen')
    parser_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a gebruik_WAARDE')
    parser_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 opnieuw_proberen_WAARDE 컴파일하고 커널에 탑재')
    parser_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    argumenten = parser_48ee4b1b.parse_args()
    specificatie = json.loads((Taken_wortel / 'relink.json').read_text())
    bouwen = Taken_wortel / 'build'
    새묶음 = bouwen / 'relinked'
    새묶음.mkdir(exist_ok=True)
    compiler_hulpmiddel = os.environ.get('ARM64_CC', 'clang')
    connector = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Archief_hulpmiddel = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    extern_Instellingen = json.loads((bouwen / 'remote/libassh-build.json').read_text())
    Instellingen = extern_Instellingen['flags']
    if argumenten.libassh_archive:
        Beveiliging_bundel = argumenten.libassh_archive.resolve()
    else:
        목적들 = []
        declaraties = ['-I', Taken_wortel / 'extern_WAARDE_28edcfa1', '-I', Taken_wortel / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Naam in extern_Instellingen['sources']:
            doel_WAARDE = 새묶음 / (Path(Naam).stem + '.o')
            Uitvoeren_opdracht([compiler_hulpmiddel] + Instellingen + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + declaraties +
                 ['-c', Taken_wortel / Naam, '-o', doel_WAARDE])
            목적들.append(doel_WAARDE)
        Beveiliging_bundel = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            Uitvoeren_opdracht([Archief_hulpmiddel, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Beveiliging_bundel)
    if argumenten.tinycc:
        if not argumenten.sdk:
            parser_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        ontwikkeling = argumenten.sdk.resolve()
        산술 = sorted((ontwikkeling / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (ontwikkeling / 'usr/include/stdio.h').is_file():
            parser_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [selectie_WAARDE for selectie_WAARDE in Instellingen if selectie_WAARDE != '-mgeneral-regs-only']
        doel_WAARDE = 새묶음 / 'compiler_hulpmiddel.o'
        Uitvoeren_opdracht([compiler_hulpmiddel] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', Taken_wortel / 'C_compiler', '-I', Taken_wortel / 'vendor/tinycc', '-I', Taken_wortel / 'gebruikersruimte',
             '-I', bouwen / 'ccompiler', '-isystem', ontwikkeling / 'usr/include', '-c', Taken_wortel / 'C_compiler/compiler_hulpmiddel.c', '-o', doel_WAARDE])
        Uitvoeren_opdracht([connector, '--gc-sections', '-T', Taken_wortel / 'gebruikersruimte/koppelindeling.ld', '-z', 'max-page-size=4096',
             '-o', bouwen / 'user/cc.elf', bouwen / 'user/start.o', bouwen / 'user/runtime.o', doel_WAARDE] +
             [bouwen / 'ccompiler' / (Naam + '.o') for Naam in ('CLR_steun', 'starten', '미리번역', 'Retour_brug')] +
             [bouwen / 'user' / (Naam + '.o') for Naam in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        kop_WAARDE = bouwen / 'programs.h'
        kop_WAARDE.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((bouwen / 'user/cc.elf').stat().st_size), kop_WAARDE.read_text()))
        Uitvoeren_opdracht([compiler_hulpmiddel] + Instellingen + ['-c', bouwen / 'programs.S', '-o', Taken_wortel / 'objects/programs.o'])
        Uitvoeren_opdracht([compiler_hulpmiddel] + Instellingen + ['-std=c11', '-I', Taken_wortel / 'posix-kor/arm64-native/declaraties', '-I', bouwen,
             '-c', Taken_wortel / 'machine/gebruikersruimte.c', '-o', Taken_wortel / 'objects/user.o'])
    Uitvoeren_opdracht([connector, '--gc-sections', '-T', Taken_wortel / 'machineopstart/koppelindeling.ld', '-o', 새묶음 / 'kernel.elf'] +
         [Taken_wortel / pad for pad in specificatie['objects']] + ['--start-group'] +
         [Beveiliging_bundel if pad == 'objects/libassh.a' else Taken_wortel / pad for pad in specificatie['libraries']] + ['--end-group'])
    Uitvoeren_opdracht([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    hash_Bestand = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if argumenten.verify and hash_Bestand != specificatie['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + hash_Bestand)
    print('RELINK PASS', hash_Bestand, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    starten()
