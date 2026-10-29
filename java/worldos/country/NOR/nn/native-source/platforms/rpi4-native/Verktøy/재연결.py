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

spegle_rot = Path(__file__).resolve().parent


def Utfør_kommando(Word_SMS):
    subprocess.check_call([str(oppføring_VALUE) for oppføring_VALUE in Word_SMS], cwd=str(spegle_rot))


def Køyr_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 stadfeste')
    해석기.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    해석기.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    해석기.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    Argument = 해석기.parse_args()
    명세 = json.loads((spegle_rot / 'relink.json').read_text())
    bygg_system = spegle_rot / 'build'
    새묶음 = bygg_system / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    Kopling = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Arkiv_verktøy = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    fjern_Innstillingar = json.loads((bygg_system / 'remote/libassh-build.json').read_text())
    Innstillingar = fjern_Innstillingar['flags']
    if Argument.libassh_archive:
        Tryggleik_bunt = Argument.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', spegle_rot / 'fjern_VALUE', '-I', spegle_rot / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Namn in fjern_Innstillingar['sources']:
            mål_VALUE = 새묶음 / (Path(Namn).stem + '.o')
            Utfør_kommando([번역기] + Innstillingar + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', spegle_rot / Namn, '-o', mål_VALUE])
            목적들.append(mål_VALUE)
        Tryggleik_bunt = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            Utfør_kommando([Arkiv_verktøy, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Tryggleik_bunt)
    if Argument.tinycc:
        if not Argument.sdk:
            해석기.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = Argument.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            해석기.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [merkt_område_VALUE for merkt_område_VALUE in Innstillingar if merkt_område_VALUE != '-mgeneral-regs-only']
        mål_VALUE = 새묶음 / '번역기.o'
        Utfør_kommando([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', spegle_rot / '시언어번역기', '-I', spegle_rot / 'vendor/tinycc', '-I', spegle_rot / 'brukar',
             '-I', bygg_system / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', spegle_rot / '시언어번역기/번역기.c', '-o', mål_VALUE])
        Utfør_kommando([Kopling, '--gc-sections', '-T', spegle_rot / 'brukar/kople_Oppsett.ld', '-z', 'max-page-size=4096',
             '-o', bygg_system / 'user/cc.elf', bygg_system / 'user/start.o', bygg_system / 'user/runtime.o', mål_VALUE] +
             [bygg_system / 'ccompiler' / (Namn + '.o') for Namn in ('Common_Language_Runtime_støtte', 'Køyr_2', '미리번역', 'levere_tilbake_bru')] +
             [bygg_system / 'user' / (Namn + '.o') for Namn in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = bygg_system / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((bygg_system / 'user/cc.elf').stat().st_size), 머리.read_text()))
        Utfør_kommando([번역기] + Innstillingar + ['-c', bygg_system / 'programs.S', '-o', spegle_rot / 'objects/programs.o'])
        Utfør_kommando([번역기] + Innstillingar + ['-std=c11', '-I', spegle_rot / 'posix-kor/arm64-native/포함', '-I', bygg_system,
             '-c', spegle_rot / 'maskin/brukar.c', '-o', spegle_rot / 'objects/user.o'])
    Utfør_kommando([Kopling, '--gc-sections', '-T', spegle_rot / '부팅/kople_Oppsett.ld', '-o', 새묶음 / 'kernel.elf'] +
         [spegle_rot / STIGE for STIGE in 명세['objects']] + ['--start-group'] +
         [Tryggleik_bunt if STIGE == 'objects/libassh.a' else spegle_rot / STIGE for STIGE in 명세['libraries']] + ['--end-group'])
    Utfør_kommando([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    hash_fil = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if Argument.verify and hash_fil != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + hash_fil)
    print('RELINK PASS', hash_fil, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Køyr_2()
