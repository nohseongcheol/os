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

արձակել_արմատ = Path(__file__).resolve().parent


def կատարել_հրաման(Բառ_Գրվածք):
    subprocess.check_call([str(մուտքագրում_արժեք) for մուտքագրում_արժեք in Բառ_Գրվածք], cwd=str(արձակել_արմատ))


def Գործարկել():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 հաստատել')
    해석기.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    해석기.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    해석기.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = 해석기.parse_args()
    명세 = json.loads((արձակել_արմատ / 'relink.json').read_text())
    կառուցել_համակարգ = արձակել_արմատ / 'build'
    새묶음 = կառուցել_համակարգ / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    Կապակցիչ = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Պահոց_գործիք = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    հեռակա_Կարգավորումներ = json.loads((կառուցել_համակարգ / 'remote/libassh-build.json').read_text())
    Նախընտրանքներ = հեռակա_Կարգավորումներ['flags']
    if 인수.libassh_archive:
        Անվտանգություն_փաթեթ = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', արձակել_արմատ / 'հեռակա_արժեք', '-I', արձակել_արմատ / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Անուն in հեռակա_Կարգավորումներ['sources']:
            նպատակակետ_արժեք = 새묶음 / (Path(Անուն).stem + '.o')
            կատարել_հրաման([번역기] + Նախընտրանքներ + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', արձակել_արմատ / Անուն, '-o', նպատակակետ_արժեք])
            목적들.append(նպատակակետ_արժեք)
        Անվտանգություն_փաթեթ = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            կատարել_հրաման([Պահոց_գործիք, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Անվտանգություն_փաթեթ)
    if 인수.tinycc:
        if not 인수.sdk:
            해석기.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            해석기.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [ընտրվածք_արժեք for ընտրվածք_արժեք in Նախընտրանքներ if ընտրվածք_արժեք != '-mgeneral-regs-only']
        նպատակակետ_արժեք = 새묶음 / '번역기.o'
        կատարել_հրաման([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', արձակել_արմատ / '시언어번역기', '-I', արձակել_արմատ / 'vendor/tinycc', '-I', արձակել_արմատ / 'օգտվող',
             '-I', կառուցել_համակարգ / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', արձակել_արմատ / '시언어번역기/번역기.c', '-o', նպատակակետ_արժեք])
        կատարել_հրաման([Կապակցիչ, '--gc-sections', '-T', արձակել_արմատ / 'օգտվող/կապ_Դասավորություն.ld', '-z', 'max-page-size=4096',
             '-o', կառուցել_համակարգ / 'user/cc.elf', կառուցել_համակարգ / 'user/start.o', կառուցել_համակարգ / 'user/runtime.o', նպատակակետ_արժեք] +
             [կառուցել_համակարգ / 'ccompiler' / (Անուն + '.o') for Անուն in ('սովորական_լեզվի_աշխատաժամանակ_Աջակցում', 'Գործարկել', '미리번역', 'վերադարձնել_կամուրջ')] +
             [կառուցել_համակարգ / 'user' / (Անուն + '.o') for Անուն in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = կառուցել_համակարգ / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((կառուցել_համակարգ / 'user/cc.elf').stat().st_size), 머리.read_text()))
        կատարել_հրաման([번역기] + Նախընտրանքներ + ['-c', կառուցել_համակարգ / 'programs.S', '-o', արձակել_արմատ / 'objects/programs.o'])
        կատարել_հրաման([번역기] + Նախընտրանքներ + ['-std=c11', '-I', արձակել_արմատ / 'posix-kor/arm64-native/포함', '-I', կառուցել_համակարգ,
             '-c', արձակել_արմատ / 'մեքենա/օգտվող.c', '-o', արձակել_արմատ / 'objects/user.o'])
    կատարել_հրաման([Կապակցիչ, '--gc-sections', '-T', արձակել_արմատ / '부팅/կապ_Դասավորություն.ld', '-o', 새묶음 / 'kernel.elf'] +
         [արձակել_արմատ / Ճանապարհ for Ճանապարհ in 명세['objects']] + ['--start-group'] +
         [Անվտանգություն_փաթեթ if Ճանապարհ == 'objects/libassh.a' else արձակել_արմատ / Ճանապարհ for Ճանապարհ in 명세['libraries']] + ['--end-group'])
    կատարել_հրաման([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    պատահական_տվյալներ_նիշք = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and պատահական_տվյալներ_նիշք != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + պատահական_տվյալներ_նիշք)
    print('RELINK PASS', պատահական_տվյալներ_նիշք, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Գործարկել()
