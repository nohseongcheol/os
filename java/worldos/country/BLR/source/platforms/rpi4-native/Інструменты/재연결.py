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


def выканаць_каманда(Гульні_са_словамі_Тэкст):
    subprocess.check_call([str(увядзенне_значэнне) for увядзенне_значэнне in Гульні_са_словамі_Тэкст], cwd=str(기준))


def Выканаць():
    аналізатар_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    аналізатар_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 праверыць')
    аналізатар_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    аналізатар_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    аналізатар_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = аналізатар_48ee4b1b.parse_args()
    명세 = json.loads((기준 / 'relink.json').read_text())
    зборка_сістэма = 기준 / 'build'
    새묶음 = зборка_сістэма / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    злучальнік = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Архіў_інструмент = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    аддалены_Налады = json.loads((зборка_сістэма / 'remote/libassh-build.json').read_text())
    Усталёўкі = аддалены_Налады['flags']
    if 인수.libassh_archive:
        Бяспека_пакет = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', 기준 / 'аддалены_значэнне', '-I', 기준 / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Назва in аддалены_Налады['sources']:
            прызначэнне_значэнне_a0fbc067 = 새묶음 / (Path(Назва).stem + '.o')
            выканаць_каманда([번역기] + Усталёўкі + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', 기준 / Назва, '-o', прызначэнне_значэнне_a0fbc067])
            목적들.append(прызначэнне_значэнне_a0fbc067)
        Бяспека_пакет = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            выканаць_каманда([Архіў_інструмент, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Бяспека_пакет)
    if 인수.tinycc:
        if not 인수.sdk:
            аналізатар_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            аналізатар_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [вылучанае_значэнне for вылучанае_значэнне in Усталёўкі if вылучанае_значэнне != '-mgeneral-regs-only']
        прызначэнне_значэнне_a0fbc067 = 새묶음 / '번역기.o'
        выканаць_каманда([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', 기준 / '시언어번역기', '-I', 기준 / 'vendor/tinycc', '-I', 기준 / 'карыстальнік',
             '-I', зборка_сістэма / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', 기준 / '시언어번역기/번역기.c', '-o', прызначэнне_значэнне_a0fbc067])
        выканаць_каманда([злучальнік, '--gc-sections', '-T', 기준 / 'карыстальнік/сувязь_Макет.ld', '-z', 'max-page-size=4096',
             '-o', зборка_сістэма / 'user/cc.elf', зборка_сістэма / 'user/start.o', зборка_сістэма / 'user/runtime.o', прызначэнне_значэнне_a0fbc067] +
             [зборка_сістэма / 'ccompiler' / (Назва + '.o') for Назва in ('агульнамоўная_серада_выканання_апора', 'Выканаць', '미리번역', '되돌림')] +
             [зборка_сістэма / 'user' / (Назва + '.o') for Назва in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = зборка_сістэма / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((зборка_сістэма / 'user/cc.elf').stat().st_size), 머리.read_text()))
        выканаць_каманда([번역기] + Усталёўкі + ['-c', зборка_сістэма / 'programs.S', '-o', 기준 / 'objects/programs.o'])
        выканаць_каманда([번역기] + Усталёўкі + ['-std=c11', '-I', 기준 / 'posix-kor/arm64-native/포함', '-I', зборка_сістэма,
             '-c', 기준 / 'камп_ютар/карыстальнік.c', '-o', 기준 / 'objects/user.o'])
    выканаць_каманда([злучальнік, '--gc-sections', '-T', 기준 / '부팅/сувязь_Макет.ld', '-o', 새묶음 / 'kernel.elf'] +
         [기준 / ШЛЯХ for ШЛЯХ in 명세['objects']] + ['--start-group'] +
         [Бяспека_пакет if ШЛЯХ == 'objects/libassh.a' else 기준 / ШЛЯХ for ШЛЯХ in 명세['libraries']] + ['--end-group'])
    выканаць_каманда([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    хэш_файл = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and хэш_файл != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + хэш_файл)
    print('RELINK PASS', хэш_файл, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Выканаць()
