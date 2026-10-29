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


def ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(말):
    subprocess.check_call([str(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ) for Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ in 말], cwd=str(기준))


def ᎠᎢᏎᏍᏗ():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 ᎰᎯᏳᏓ')
    해석기.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    해석기.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    해석기.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = 해석기.parse_args()
    명세 = json.loads((기준 / 'relink.json').read_text())
    ᎪᏢᏍᎩ_ᏄᏍᏗᏓᏅᎢ = 기준 / 'build'
    새묶음 = ᎪᏢᏍᎩ_ᏄᏍᏗᏓᏅᎢ / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    ᎫᏓᎸᏙᏗ = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    ᎠᏍᏆᏂᎪᏛᎢ_ᎬᏔᏂᏓᏍᏗ = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    원격설정 = json.loads((ᎪᏢᏍᎩ_ᏄᏍᏗᏓᏅᎢ / 'remote/libassh-build.json').read_text())
    ᏕᎦᎧᎲᎢ = 원격설정['flags']
    if 인수.libassh_archive:
        ᎤᎦᏎᏍᏗ_ᎦᏇᏅᎯ = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', 기준 / '원격', '-I', 기준 / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for ᏚᏙᎥᎢ in 원격설정['sources']:
            ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ = 새묶음 / (Path(ᏚᏙᎥᎢ).stem + '.o')
            ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ([번역기] + ᏕᎦᎧᎲᎢ + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', 기준 / ᏚᏙᎥᎢ, '-o', ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ])
            목적들.append(ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ)
        ᎤᎦᏎᏍᏗ_ᎦᏇᏅᎯ = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ([ᎠᏍᏆᏂᎪᏛᎢ_ᎬᏔᏂᏓᏍᏗ, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(ᎤᎦᏎᏍᏗ_ᎦᏇᏅᎯ)
    if 인수.tinycc:
        if not 인수.sdk:
            해석기.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            해석기.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [ᏗᏑᏰᏓ_ᏧᎬᏩᎶᏗᏯ for ᏗᏑᏰᏓ_ᏧᎬᏩᎶᏗᏯ in ᏕᎦᎧᎲᎢ if ᏗᏑᏰᏓ_ᏧᎬᏩᎶᏗᏯ != '-mgeneral-regs-only']
        ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ = 새묶음 / '번역기.o'
        ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', 기준 / '시언어번역기', '-I', 기준 / 'vendor/tinycc', '-I', 기준 / 'ᎬᏗᏍᎩ',
             '-I', ᎪᏢᏍᎩ_ᏄᏍᏗᏓᏅᎢ / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', 기준 / '시언어번역기/번역기.c', '-o', ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ])
        ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ([ᎫᏓᎸᏙᏗ, '--gc-sections', '-T', 기준 / 'ᎬᏗᏍᎩ/ᎫᏓᎸᎢ_ᏱᎬᏂ.ld', '-z', 'max-page-size=4096',
             '-o', ᎪᏢᏍᎩ_ᏄᏍᏗᏓᏅᎢ / 'user/cc.elf', ᎪᏢᏍᎩ_ᏄᏍᏗᏓᏅᎢ / 'user/start.o', ᎪᏢᏍᎩ_ᏄᏍᏗᏓᏅᎢ / 'user/runtime.o', ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ] +
             [ᎪᏢᏍᎩ_ᏄᏍᏗᏓᏅᎢ / 'ccompiler' / (ᏚᏙᎥᎢ + '.o') for ᏚᏙᎥᎢ in ('실행지원', 'ᎠᎢᏎᏍᏗ', '미리번역', '되돌림')] +
             [ᎪᏢᏍᎩ_ᏄᏍᏗᏓᏅᎢ / 'user' / (ᏚᏙᎥᎢ + '.o') for ᏚᏙᎥᎢ in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = ᎪᏢᏍᎩ_ᏄᏍᏗᏓᏅᎢ / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((ᎪᏢᏍᎩ_ᏄᏍᏗᏓᏅᎢ / 'user/cc.elf').stat().st_size), 머리.read_text()))
        ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ([번역기] + ᏕᎦᎧᎲᎢ + ['-c', ᎪᏢᏍᎩ_ᏄᏍᏗᏓᏅᎢ / 'programs.S', '-o', 기준 / 'objects/programs.o'])
        ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ([번역기] + ᏕᎦᎧᎲᎢ + ['-std=c11', '-I', 기준 / 'posix-kor/arm64-native/포함', '-I', ᎪᏢᏍᎩ_ᏄᏍᏗᏓᏅᎢ,
             '-c', 기준 / '기계/ᎬᏗᏍᎩ.c', '-o', 기준 / 'objects/user.o'])
    ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ([ᎫᏓᎸᏙᏗ, '--gc-sections', '-T', 기준 / '부팅/ᎫᏓᎸᎢ_ᏱᎬᏂ.ld', '-o', 새묶음 / 'kernel.elf'] +
         [기준 / ᎠᏍᏓᏩᏛᏍᏗ for ᎠᏍᏓᏩᏛᏍᏗ in 명세['objects']] + ['--start-group'] +
         [ᎤᎦᏎᏍᏗ_ᎦᏇᏅᎯ if ᎠᏍᏓᏩᏛᏍᏗ == 'objects/libassh.a' else 기준 / ᎠᏍᏓᏩᏛᏍᏗ for ᎠᏍᏓᏩᏛᏍᏗ in 명세['libraries']] + ['--end-group'])
    ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    해시 = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and 해시 != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + 해시)
    print('RELINK PASS', 해시, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    ᎠᎢᏎᏍᏗ()
