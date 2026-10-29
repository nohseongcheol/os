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

기준 = Path(__file__).resolve().parent


def gukora_ibwiriza(Ijambo_SMS):
    subprocess.check_call([str(icyinjizwa_agaciro) for icyinjizwa_agaciro in Ijambo_SMS], cwd=str(기준))


def ihuriro():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 gusuzuma')
    해석기.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    해석기.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    해석기.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = 해석기.parse_args()
    명세 = json.loads((기준 / 'relink.json').read_text())
    gusohora_sisitemu = 기준 / 'build'
    새묶음 = gusohora_sisitemu / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    agahuza = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    gushyingura_igikoresho = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    kure_Amagenamiterere = json.loads((gusohora_sisitemu / 'remote/libassh-build.json').read_text())
    Amagenamiterere = kure_Amagenamiterere['flags']
    if 인수.libassh_archive:
        Umutekano_ipaki = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', 기준 / 'kure_agaciro', '-I', 기준 / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Izina in kure_Amagenamiterere['sources']:
            aho_ijya_agaciro = 새묶음 / (Path(Izina).stem + '.o')
            gukora_ibwiriza([번역기] + Amagenamiterere + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', 기준 / Izina, '-o', aho_ijya_agaciro])
            목적들.append(aho_ijya_agaciro)
        Umutekano_ipaki = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            gukora_ibwiriza([gushyingura_igikoresho, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Umutekano_ipaki)
    if 인수.tinycc:
        if not 인수.sdk:
            해석기.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            해석기.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [ihitamo_agaciro for ihitamo_agaciro in Amagenamiterere if ihitamo_agaciro != '-mgeneral-regs-only']
        aho_ijya_agaciro = 새묶음 / '번역기.o'
        gukora_ibwiriza([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', 기준 / '시언어번역기', '-I', 기준 / 'vendor/tinycc', '-I', 기준 / 'ukoresha',
             '-I', gusohora_sisitemu / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', 기준 / '시언어번역기/번역기.c', '-o', aho_ijya_agaciro])
        gukora_ibwiriza([agahuza, '--gc-sections', '-T', 기준 / 'ukoresha/Ihuza_Imimerere.ld', '-z', 'max-page-size=4096',
             '-o', gusohora_sisitemu / 'user/cc.elf', gusohora_sisitemu / 'user/start.o', gusohora_sisitemu / 'user/runtime.o', aho_ijya_agaciro] +
             [gusohora_sisitemu / 'ccompiler' / (Izina + '.o') for Izina in ('igihe_ururimi_rukorwamo_Ubufasha', 'ihuriro', '미리번역', '되돌림')] +
             [gusohora_sisitemu / 'user' / (Izina + '.o') for Izina in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = gusohora_sisitemu / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((gusohora_sisitemu / 'user/cc.elf').stat().st_size), 머리.read_text()))
        gukora_ibwiriza([번역기] + Amagenamiterere + ['-c', gusohora_sisitemu / 'programs.S', '-o', 기준 / 'objects/programs.o'])
        gukora_ibwiriza([번역기] + Amagenamiterere + ['-std=c11', '-I', 기준 / 'posix-kor/arm64-native/포함', '-I', gusohora_sisitemu,
             '-c', 기준 / 'imashini/ukoresha.c', '-o', 기준 / 'objects/user.o'])
    gukora_ibwiriza([agahuza, '--gc-sections', '-T', 기준 / '부팅/Ihuza_Imimerere.ld', '-o', 새묶음 / 'kernel.elf'] +
         [기준 / Inzira for Inzira in 명세['objects']] + ['--start-group'] +
         [Umutekano_ipaki if Inzira == 'objects/libassh.a' else 기준 / Inzira for Inzira in 명세['libraries']] + ['--end-group'])
    gukora_ibwiriza([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    hashi_dosiye = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and hashi_dosiye != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + hashi_dosiye)
    print('RELINK PASS', hashi_dosiye, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    ihuriro()
