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


def Гүйцэтгэх_команд(Үгэн_Бичвэр):
    subprocess.check_call([str(оролт_утга) for оролт_утга in Үгэн_Бичвэр], cwd=str(기준))


def Ажиллуулах():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 шалгах')
    해석기.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    해석기.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    해석기.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = 해석기.parse_args()
    명세 = json.loads((기준 / 'relink.json').read_text())
    хувилбар_систем = 기준 / 'build'
    새묶음 = хувилбар_систем / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    холбогч = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Архив_хэрэгсэл = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    алсын_Тохиргоо = json.loads((хувилбар_систем / 'remote/libassh-build.json').read_text())
    Тохиргоо = алсын_Тохиргоо['flags']
    if 인수.libassh_archive:
        хамгаалалт_багц = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', 기준 / 'алсын_утга', '-I', 기준 / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Нэр in алсын_Тохиргоо['sources']:
            товлосон_газар_утга = 새묶음 / (Path(Нэр).stem + '.o')
            Гүйцэтгэх_команд([번역기] + Тохиргоо + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', 기준 / Нэр, '-o', товлосон_газар_утга])
            목적들.append(товлосон_газар_утга)
        хамгаалалт_багц = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            Гүйцэтгэх_команд([Архив_хэрэгсэл, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(хамгаалалт_багц)
    if 인수.tinycc:
        if not 인수.sdk:
            해석기.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            해석기.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [сонгосон_хэсэг_утга for сонгосон_хэсэг_утга in Тохиргоо if сонгосон_хэсэг_утга != '-mgeneral-regs-only']
        товлосон_газар_утга = 새묶음 / '번역기.o'
        Гүйцэтгэх_команд([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', 기준 / '시언어번역기', '-I', 기준 / 'vendor/tinycc', '-I', 기준 / 'хэрэглэгч',
             '-I', хувилбар_систем / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', 기준 / '시언어번역기/번역기.c', '-o', товлосон_газар_утга])
        Гүйцэтгэх_команд([холбогч, '--gc-sections', '-T', 기준 / 'хэрэглэгч/Холбох_Бүдүүвч.ld', '-z', 'max-page-size=4096',
             '-o', хувилбар_систем / 'user/cc.elf', хувилбар_систем / 'user/start.o', хувилбар_систем / 'user/runtime.o', товлосон_газар_утга] +
             [хувилбар_систем / 'ccompiler' / (Нэр + '.o') for Нэр in ('түгээмэл_хэлний_ажиллах_үе_тусламж', 'Ажиллуулах', '미리번역', '되돌림')] +
             [хувилбар_систем / 'user' / (Нэр + '.o') for Нэр in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = хувилбар_систем / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((хувилбар_систем / 'user/cc.elf').stat().st_size), 머리.read_text()))
        Гүйцэтгэх_команд([번역기] + Тохиргоо + ['-c', хувилбар_систем / 'programs.S', '-o', 기준 / 'objects/programs.o'])
        Гүйцэтгэх_команд([번역기] + Тохиргоо + ['-std=c11', '-I', 기준 / 'posix-kor/arm64-native/포함', '-I', хувилбар_систем,
             '-c', 기준 / 'компьютер/хэрэглэгч.c', '-o', 기준 / 'objects/user.o'])
    Гүйцэтгэх_команд([холбогч, '--gc-sections', '-T', 기준 / '부팅/Холбох_Бүдүүвч.ld', '-o', 새묶음 / 'kernel.elf'] +
         [기준 / ЗАМ for ЗАМ in 명세['objects']] + ['--start-group'] +
         [хамгаалалт_багц if ЗАМ == 'objects/libassh.a' else 기준 / ЗАМ for ЗАМ in 명세['libraries']] + ['--end-group'])
    Гүйцэтгэх_команд([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл_файл = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл_файл != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл_файл)
    print('RELINK PASS', Оруулсан_мэдээллийг_өөрчлөх_хэрэгсэл_файл, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Ажиллуулах()
