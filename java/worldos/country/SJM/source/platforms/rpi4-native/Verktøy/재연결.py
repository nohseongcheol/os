#!/usr/bin/env python3
"""distribusjon_VERDI 묶음에서 libassh/TinyCC를 교체하고 eget 커널을 prøve_på_nytt_VERDI 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

speile_rot = Path(__file__).resolve().parent


def Utfør_kommando(ord_SMS):
    subprocess.check_call([str(oppføring_VERDI) for oppføring_VERDI in ord_SMS], cwd=str(speile_rot))


def Kjør_2():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 bekrefte')
    parser_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a bruk_VERDI')
    parser_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 prøve_på_nytt_VERDI 컴파일하고 커널에 탑재')
    parser_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    Argumenter = parser_48ee4b1b.parse_args()
    명세 = json.loads((speile_rot / 'relink.json').read_text())
    bygg_System = speile_rot / 'build'
    새묶음 = bygg_System / 'relinked'
    새묶음.mkdir(exist_ok=True)
    kompilator_verktøy = os.environ.get('ARM64_CC', 'clang')
    Kobling = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Arkiv_verktøy = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    ekstern_Innstillinger = json.loads((bygg_System / 'remote/libassh-build.json').read_text())
    Innstillinger = ekstern_Innstillinger['flags']
    if Argumenter.libassh_archive:
        Sikkerhet_bunt = Argumenter.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', speile_rot / 'ekstern_VERDI_28edcfa1', '-I', speile_rot / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Navn in ekstern_Innstillinger['sources']:
            mål_VERDI = 새묶음 / (Path(Navn).stem + '.o')
            Utfør_kommando([kompilator_verktøy] + Innstillinger + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', speile_rot / Navn, '-o', mål_VERDI])
            목적들.append(mål_VERDI)
        Sikkerhet_bunt = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            Utfør_kommando([Arkiv_verktøy, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Sikkerhet_bunt)
    if Argumenter.tinycc:
        if not Argumenter.sdk:
            parser_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        utviklet_materiale = Argumenter.sdk.resolve()
        산술 = sorted((utviklet_materiale / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (utviklet_materiale / 'usr/include/stdio.h').is_file():
            parser_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [merket_område_VERDI for merket_område_VERDI in Innstillinger if merket_område_VERDI != '-mgeneral-regs-only']
        mål_VERDI = 새묶음 / 'kompilator_verktøy.o'
        Utfør_kommando([kompilator_verktøy] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', speile_rot / 'C_kompilator', '-I', speile_rot / 'vendor/tinycc', '-I', speile_rot / 'bruker',
             '-I', bygg_System / 'ccompiler', '-isystem', utviklet_materiale / 'usr/include', '-c', speile_rot / 'C_kompilator/kompilator_verktøy.c', '-o', mål_VERDI])
        Utfør_kommando([Kobling, '--gc-sections', '-T', speile_rot / 'bruker/koble_Oppsett.ld', '-z', 'max-page-size=4096',
             '-o', bygg_System / 'user/cc.elf', bygg_System / 'user/start.o', bygg_System / 'user/runtime.o', mål_VERDI] +
             [bygg_System / 'ccompiler' / (Navn + '.o') for Navn in ('CLR_støtte', 'Kjør_2', '미리번역', 'return_bro')] +
             [bygg_System / 'user' / (Navn + '.o') for Navn in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = bygg_System / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((bygg_System / 'user/cc.elf').stat().st_size), 머리.read_text()))
        Utfør_kommando([kompilator_verktøy] + Innstillinger + ['-c', bygg_System / 'programs.S', '-o', speile_rot / 'objects/programs.o'])
        Utfør_kommando([kompilator_verktøy] + Innstillinger + ['-std=c11', '-I', speile_rot / 'posix-kor/arm64-native/포함', '-I', bygg_System,
             '-c', speile_rot / 'maskin/bruker.c', '-o', speile_rot / 'objects/user.o'])
    Utfør_kommando([Kobling, '--gc-sections', '-T', speile_rot / '부팅/koble_Oppsett.ld', '-o', 새묶음 / 'kernel.elf'] +
         [speile_rot / Sti for Sti in 명세['objects']] + ['--start-group'] +
         [Sikkerhet_bunt if Sti == 'objects/libassh.a' else speile_rot / Sti for Sti in 명세['libraries']] + ['--end-group'])
    Utfør_kommando([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    hash_Fil = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if Argumenter.verify and hash_Fil != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + hash_Fil)
    print('RELINK PASS', hash_Fil, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Kjør_2()
