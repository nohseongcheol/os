#!/usr/bin/env python3
"""fördelning_värde 묶음에서 libassh/TinyCC를 교체하고 eget 커널을 försöka_igen_värde 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

åtgärd_rot = Path(__file__).resolve().parent


def köra_kommando(Ord_SMS):
    subprocess.check_call([str(post_värde) for post_värde in Ord_SMS], cwd=str(åtgärd_rot))


def Kör():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 verifiera')
    parser_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a använda_värde')
    parser_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 försöka_igen_värde 컴파일하고 커널에 탑재')
    parser_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    argument = parser_48ee4b1b.parse_args()
    명세 = json.loads((åtgärd_rot / 'relink.json').read_text())
    version_System = åtgärd_rot / 'build'
    새묶음 = version_System / 'relinked'
    새묶음.mkdir(exist_ok=True)
    kompilerare_verktyg = os.environ.get('ARM64_CC', 'clang')
    Koppling = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Arkiv_verktyg = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    fjärr_Inställningar = json.loads((version_System / 'remote/libassh-build.json').read_text())
    Inställningar = fjärr_Inställningar['flags']
    if argument.libassh_archive:
        Säkerhet_bunt = argument.libassh_archive.resolve()
    else:
        목적들 = []
        deklarationer = ['-I', åtgärd_rot / 'fjärr_värde', '-I', åtgärd_rot / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Namn in fjärr_Inställningar['sources']:
            mål_värde = 새묶음 / (Path(Namn).stem + '.o')
            köra_kommando([kompilerare_verktyg] + Inställningar + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + deklarationer +
                 ['-c', åtgärd_rot / Namn, '-o', mål_värde])
            목적들.append(mål_värde)
        Säkerhet_bunt = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            köra_kommando([Arkiv_verktyg, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Säkerhet_bunt)
    if argument.tinycc:
        if not argument.sdk:
            parser_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        utveckling = argument.sdk.resolve()
        산술 = sorted((utveckling / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (utveckling / 'usr/include/stdio.h').is_file():
            parser_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [markering_värde for markering_värde in Inställningar if markering_värde != '-mgeneral-regs-only']
        mål_värde = 새묶음 / 'kompilerare_verktyg.o'
        köra_kommando([kompilerare_verktyg] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', åtgärd_rot / 'C_kompilerare', '-I', åtgärd_rot / 'vendor/tinycc', '-I', åtgärd_rot / 'användarutrymme',
             '-I', version_System / 'ccompiler', '-isystem', utveckling / 'usr/include', '-c', åtgärd_rot / 'C_kompilerare/kompilerare_verktyg.c', '-o', mål_värde])
        köra_kommando([Koppling, '--gc-sections', '-T', åtgärd_rot / 'användarutrymme/länkningslayout.ld', '-z', 'max-page-size=4096',
             '-o', version_System / 'user/cc.elf', version_System / 'user/start.o', version_System / 'user/runtime.o', mål_värde] +
             [version_System / 'ccompiler' / (Namn + '.o') for Namn in ('CLR_stöd', 'Kör', '미리번역', 'Retur_brygga')] +
             [version_System / 'user' / (Namn + '.o') for Namn in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = version_System / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((version_System / 'user/cc.elf').stat().st_size), 머리.read_text()))
        köra_kommando([kompilerare_verktyg] + Inställningar + ['-c', version_System / 'programs.S', '-o', åtgärd_rot / 'objects/programs.o'])
        köra_kommando([kompilerare_verktyg] + Inställningar + ['-std=c11', '-I', åtgärd_rot / 'posix-kor/arm64-native/deklarationer', '-I', version_System,
             '-c', åtgärd_rot / 'dator/användarutrymme.c', '-o', åtgärd_rot / 'objects/user.o'])
    köra_kommando([Koppling, '--gc-sections', '-T', åtgärd_rot / 'maskinstart/länkningslayout.ld', '-o', 새묶음 / 'kernel.elf'] +
         [åtgärd_rot / sökväg_2 for sökväg_2 in 명세['objects']] + ['--start-group'] +
         [Säkerhet_bunt if sökväg_2 == 'objects/libassh.a' else åtgärd_rot / sökväg_2 for sökväg_2 in 명세['libraries']] + ['--end-group'])
    köra_kommando([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    hash_fil = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if argument.verify and hash_fil != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + hash_fil)
    print('RELINK PASS', hash_fil, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Kör()
