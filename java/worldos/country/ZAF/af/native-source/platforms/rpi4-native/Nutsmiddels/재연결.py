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

Project_wortel = Path(__file__).resolve().parent


def uitvoer_bevel(Word_SMS):
    subprocess.check_call([str(inskrywing_VALUE) for inskrywing_VALUE in Word_SMS], cwd=str(Project_wortel))


def Loop():
    ontleder_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ontleder_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 verifieer')
    ontleder_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    ontleder_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    ontleder_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = ontleder_48ee4b1b.parse_args()
    명세 = json.loads((Project_wortel / 'relink.json').read_text())
    bou_stelsel = Project_wortel / 'build'
    새묶음 = bou_stelsel / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    Verbinder = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Argief_nutsmiddel = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    afstands_Instellings = json.loads((bou_stelsel / 'remote/libassh-build.json').read_text())
    Instellings = afstands_Instellings['flags']
    if 인수.libassh_archive:
        Sekuriteit_bondel = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', Project_wortel / 'afstands_VALUE', '-I', Project_wortel / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Naam in afstands_Instellings['sources']:
            bestemming_VALUE = 새묶음 / (Path(Naam).stem + '.o')
            uitvoer_bevel([번역기] + Instellings + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', Project_wortel / Naam, '-o', bestemming_VALUE])
            목적들.append(bestemming_VALUE)
        Sekuriteit_bondel = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            uitvoer_bevel([Argief_nutsmiddel, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Sekuriteit_bondel)
    if 인수.tinycc:
        if not 인수.sdk:
            ontleder_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            ontleder_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [seleksie_VALUE for seleksie_VALUE in Instellings if seleksie_VALUE != '-mgeneral-regs-only']
        bestemming_VALUE = 새묶음 / '번역기.o'
        uitvoer_bevel([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', Project_wortel / '시언어번역기', '-I', Project_wortel / 'vendor/tinycc', '-I', Project_wortel / 'gebruiker',
             '-I', bou_stelsel / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', Project_wortel / '시언어번역기/번역기.c', '-o', bestemming_VALUE])
        uitvoer_bevel([Verbinder, '--gc-sections', '-T', Project_wortel / 'gebruiker/Skakel_Uitleg.ld', '-z', 'max-page-size=4096',
             '-o', bou_stelsel / 'user/cc.elf', bou_stelsel / 'user/start.o', bou_stelsel / 'user/runtime.o', bestemming_VALUE] +
             [bou_stelsel / 'ccompiler' / (Naam + '.o') for Naam in ('algemene_taallooptyd_Bystand', 'Loop', '미리번역', 'teruggee_brug')] +
             [bou_stelsel / 'user' / (Naam + '.o') for Naam in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = bou_stelsel / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((bou_stelsel / 'user/cc.elf').stat().st_size), 머리.read_text()))
        uitvoer_bevel([번역기] + Instellings + ['-c', bou_stelsel / 'programs.S', '-o', Project_wortel / 'objects/programs.o'])
        uitvoer_bevel([번역기] + Instellings + ['-std=c11', '-I', Project_wortel / 'posix-kor/arm64-native/포함', '-I', bou_stelsel,
             '-c', Project_wortel / 'masjien/gebruiker.c', '-o', Project_wortel / 'objects/user.o'])
    uitvoer_bevel([Verbinder, '--gc-sections', '-T', Project_wortel / '부팅/Skakel_Uitleg.ld', '-o', 새묶음 / 'kernel.elf'] +
         [Project_wortel / Pad for Pad in 명세['objects']] + ['--start-group'] +
         [Sekuriteit_bondel if Pad == 'objects/libassh.a' else Project_wortel / Pad for Pad in 명세['libraries']] + ['--end-group'])
    uitvoer_bevel([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    huts_lêer = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and huts_lêer != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + huts_lêer)
    print('RELINK PASS', huts_lêer, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Loop()
