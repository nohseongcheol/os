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


def mee_nnyemiwu(Mkpụrụokwu_SMS):
    subprocess.check_call([str(ndebà_valuu) for ndebà_valuu in Mkpụrụokwu_SMS], cwd=str(기준))


def Bido():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 nkwàdo_eziokwū')
    해석기.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    해석기.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    해석기.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = 해석기.parse_args()
    명세 = json.loads((기준 / 'relink.json').read_text())
    wue_sistèm = 기준 / 'build'
    새묶음 = wue_sistèm / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    ṅjikọta = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    ọkpụ_ngwaọrụ = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    ebe_dị̀anyā_Mwube = json.loads((wue_sistèm / 'remote/libassh-build.json').read_text())
    Mwube = ebe_dị̀anyā_Mwube['flags']
    if 인수.libassh_archive:
        Nche_ngwungwu = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', 기준 / 'ebe_dị̀anyā_valuu', '-I', 기준 / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Aha in ebe_dị̀anyā_Mwube['sources']:
            ebemwèga_valuu = 새묶음 / (Path(Aha).stem + '.o')
            mee_nnyemiwu([번역기] + Mwube + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', 기준 / Aha, '-o', ebemwèga_valuu])
            목적들.append(ebemwèga_valuu)
        Nche_ngwungwu = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            mee_nnyemiwu([ọkpụ_ngwaọrụ, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Nche_ngwungwu)
    if 인수.tinycc:
        if not 인수.sdk:
            해석기.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            해석기.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [ebenhọrọ_valuu for ebenhọrọ_valuu in Mwube if ebenhọrọ_valuu != '-mgeneral-regs-only']
        ebemwèga_valuu = 새묶음 / '번역기.o'
        mee_nnyemiwu([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', 기준 / '시언어번역기', '-I', 기준 / 'vendor/tinycc', '-I', 기준 / 'òjìàrụ',
             '-I', wue_sistèm / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', 기준 / '시언어번역기/번역기.c', '-o', ebemwèga_valuu])
        mee_nnyemiwu([ṅjikọta, '--gc-sections', '-T', 기준 / 'òjìàrụ/Njikọ_Nhàzi.ld', '-z', 'max-page-size=4096',
             '-o', wue_sistèm / 'user/cc.elf', wue_sistèm / 'user/start.o', wue_sistèm / 'user/runtime.o', ebemwèga_valuu] +
             [wue_sistèm / 'ccompiler' / (Aha + '.o') for Aha in ('ọgịga_oge_otu_asụsụ_nkwado', 'Bido', '미리번역', '되돌림')] +
             [wue_sistèm / 'user' / (Aha + '.o') for Aha in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = wue_sistèm / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((wue_sistèm / 'user/cc.elf').stat().st_size), 머리.read_text()))
        mee_nnyemiwu([번역기] + Mwube + ['-c', wue_sistèm / 'programs.S', '-o', 기준 / 'objects/programs.o'])
        mee_nnyemiwu([번역기] + Mwube + ['-std=c11', '-I', 기준 / 'posix-kor/arm64-native/포함', '-I', wue_sistèm,
             '-c', 기준 / 'ngwa_komputa/òjìàrụ.c', '-o', 기준 / 'objects/user.o'])
    mee_nnyemiwu([ṅjikọta, '--gc-sections', '-T', 기준 / '부팅/Njikọ_Nhàzi.ld', '-o', 새묶음 / 'kernel.elf'] +
         [기준 / ụzọ_ozi for ụzọ_ozi in 명세['objects']] + ['--start-group'] +
         [Nche_ngwungwu if ụzọ_ozi == 'objects/libassh.a' else 기준 / ụzọ_ozi for ụzọ_ozi in 명세['libraries']] + ['--end-group'])
    mee_nnyemiwu([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    di_ike_ọbọakwụkwọ = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and di_ike_ọbọakwụkwọ != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + di_ike_ọbọakwụkwọ)
    print('RELINK PASS', di_ike_ọbọakwụkwọ, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Bido()
