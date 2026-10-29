#!/usr/bin/env python3
"""distribution_VÆRDI 묶음에서 libassh/TinyCC를 교체하고 eget 커널을 prøve_igen_VÆRDI 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

To_do_rod = Path(__file__).resolve().parent


def Udfør_kommando(Ord_sms):
    subprocess.check_call([str(post_VÆRDI_962f286b) for post_VÆRDI_962f286b in Ord_sms], cwd=str(To_do_rod))


def Kør_2():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 bekræfte')
    parser_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a brug_VÆRDI')
    parser_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 prøve_igen_VÆRDI 컴파일하고 커널에 탑재')
    parser_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    Argumenter = parser_48ee4b1b.parse_args()
    명세 = json.loads((To_do_rod / 'relink.json').read_text())
    build_System = To_do_rod / 'build'
    새묶음 = build_System / 'relinked'
    새묶음.mkdir(exist_ok=True)
    compiler_værktøj = os.environ.get('ARM64_CC', 'clang')
    connector = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Arkiv_værktøj = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    fjern_Indstillinger = json.loads((build_System / 'remote/libassh-build.json').read_text())
    Indstillinger = fjern_Indstillinger['flags']
    if Argumenter.libassh_archive:
        Sikkerhed_bundt = Argumenter.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', To_do_rod / 'fjern_VÆRDI', '-I', To_do_rod / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Navn in fjern_Indstillinger['sources']:
            destination_VÆRDI = 새묶음 / (Path(Navn).stem + '.o')
            Udfør_kommando([compiler_værktøj] + Indstillinger + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', To_do_rod / Navn, '-o', destination_VÆRDI])
            목적들.append(destination_VÆRDI)
        Sikkerhed_bundt = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            Udfør_kommando([Arkiv_værktøj, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Sikkerhed_bundt)
    if Argumenter.tinycc:
        if not Argumenter.sdk:
            parser_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        udvikling = Argumenter.sdk.resolve()
        산술 = sorted((udvikling / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (udvikling / 'usr/include/stdio.h').is_file():
            parser_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [markering_VÆRDI for markering_VÆRDI in Indstillinger if markering_VÆRDI != '-mgeneral-regs-only']
        destination_VÆRDI = 새묶음 / 'compiler_værktøj.o'
        Udfør_kommando([compiler_værktøj] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', To_do_rod / 'C_compiler', '-I', To_do_rod / 'vendor/tinycc', '-I', To_do_rod / 'bruger',
             '-I', build_System / 'ccompiler', '-isystem', udvikling / 'usr/include', '-c', To_do_rod / 'C_compiler/compiler_værktøj.c', '-o', destination_VÆRDI])
        Udfør_kommando([connector, '--gc-sections', '-T', To_do_rod / 'bruger/Link_Layout.ld', '-z', 'max-page-size=4096',
             '-o', build_System / 'user/cc.elf', build_System / 'user/start.o', build_System / 'user/runtime.o', destination_VÆRDI] +
             [build_System / 'ccompiler' / (Navn + '.o') for Navn in ('CLR_støtte', 'Kør_2', '미리번역', 'returnere_bro')] +
             [build_System / 'user' / (Navn + '.o') for Navn in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = build_System / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((build_System / 'user/cc.elf').stat().st_size), 머리.read_text()))
        Udfør_kommando([compiler_værktøj] + Indstillinger + ['-c', build_System / 'programs.S', '-o', To_do_rod / 'objects/programs.o'])
        Udfør_kommando([compiler_værktøj] + Indstillinger + ['-std=c11', '-I', To_do_rod / 'posix-kor/arm64-native/포함', '-I', build_System,
             '-c', To_do_rod / 'maskine/bruger.c', '-o', To_do_rod / 'objects/user.o'])
    Udfør_kommando([connector, '--gc-sections', '-T', To_do_rod / '부팅/Link_Layout.ld', '-o', 새묶음 / 'kernel.elf'] +
         [To_do_rod / Sti for Sti in 명세['objects']] + ['--start-group'] +
         [Sikkerhed_bundt if Sti == 'objects/libassh.a' else To_do_rod / Sti for Sti in 명세['libraries']] + ['--end-group'])
    Udfør_kommando([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    hash_fil = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if Argumenter.verify and hash_fil != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + hash_fil)
    print('RELINK PASS', hash_fil, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Kør_2()
