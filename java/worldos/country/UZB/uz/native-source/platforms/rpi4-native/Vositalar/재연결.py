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

Project_ildiz = Path(__file__).resolve().parent


def bajarmoq_buyruq(Word_SMS):
    subprocess.check_call([str(kiritish_VALUE) for kiritish_VALUE in Word_SMS], cwd=str(Project_ildiz))


def Bajarish():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 tasdiqlamoq')
    parser_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    parser_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    parser_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = parser_48ee4b1b.parse_args()
    명세 = json.loads((Project_ildiz / 'relink.json').read_text())
    nashr_tizim = Project_ildiz / 'build'
    새묶음 = nashr_tizim / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    Ulagich = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Arxiv_vosita = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    masofaviy_Sozlamalar = json.loads((nashr_tizim / 'remote/libassh-build.json').read_text())
    Moslamalar = masofaviy_Sozlamalar['flags']
    if 인수.libassh_archive:
        Xavfsizlik_to_plam = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', Project_ildiz / 'masofaviy_VALUE', '-I', Project_ildiz / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Nomi in masofaviy_Sozlamalar['sources']:
            ko_chirish_joyi_VALUE = 새묶음 / (Path(Nomi).stem + '.o')
            bajarmoq_buyruq([번역기] + Moslamalar + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', Project_ildiz / Nomi, '-o', ko_chirish_joyi_VALUE])
            목적들.append(ko_chirish_joyi_VALUE)
        Xavfsizlik_to_plam = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            bajarmoq_buyruq([Arxiv_vosita, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Xavfsizlik_to_plam)
    if 인수.tinycc:
        if not 인수.sdk:
            parser_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            parser_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [tanlanma_VALUE for tanlanma_VALUE in Moslamalar if tanlanma_VALUE != '-mgeneral-regs-only']
        ko_chirish_joyi_VALUE = 새묶음 / '번역기.o'
        bajarmoq_buyruq([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', Project_ildiz / '시언어번역기', '-I', Project_ildiz / 'vendor/tinycc', '-I', Project_ildiz / 'foydalanuvchi',
             '-I', nashr_tizim / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', Project_ildiz / '시언어번역기/번역기.c', '-o', ko_chirish_joyi_VALUE])
        bajarmoq_buyruq([Ulagich, '--gc-sections', '-T', Project_ildiz / 'foydalanuvchi/ulash_Maket.ld', '-z', 'max-page-size=4096',
             '-o', nashr_tizim / 'user/cc.elf', nashr_tizim / 'user/start.o', nashr_tizim / 'user/runtime.o', ko_chirish_joyi_VALUE] +
             [nashr_tizim / 'ccompiler' / (Nomi + '.o') for Nomi in ('umumiy_til_ish_jarayoni_madad', 'Bajarish', '미리번역', '되돌림')] +
             [nashr_tizim / 'user' / (Nomi + '.o') for Nomi in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = nashr_tizim / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((nashr_tizim / 'user/cc.elf').stat().st_size), 머리.read_text()))
        bajarmoq_buyruq([번역기] + Moslamalar + ['-c', nashr_tizim / 'programs.S', '-o', Project_ildiz / 'objects/programs.o'])
        bajarmoq_buyruq([번역기] + Moslamalar + ['-std=c11', '-I', Project_ildiz / 'posix-kor/arm64-native/포함', '-I', nashr_tizim,
             '-c', Project_ildiz / '기계/foydalanuvchi.c', '-o', Project_ildiz / 'objects/user.o'])
    bajarmoq_buyruq([Ulagich, '--gc-sections', '-T', Project_ildiz / '부팅/ulash_Maket.ld', '-o', 새묶음 / 'kernel.elf'] +
         [Project_ildiz / yo_l for yo_l in 명세['objects']] + ['--start-group'] +
         [Xavfsizlik_to_plam if yo_l == 'objects/libassh.a' else Project_ildiz / yo_l for yo_l in 명세['libraries']] + ['--end-group'])
    bajarmoq_buyruq([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    tasodifiy_ma_lumot_fayl = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and tasodifiy_ma_lumot_fayl != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + tasodifiy_ma_lumot_fayl)
    print('RELINK PASS', tasodifiy_ma_lumot_fayl, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Bajarish()
