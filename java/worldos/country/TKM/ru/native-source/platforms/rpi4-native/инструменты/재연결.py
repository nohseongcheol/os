#!/usr/bin/env python3
"""распределение_ЗНАЧЕН 묶음에서 libassh/TinyCC를 교체하고 свой 커널을 повторить_попытку_ЗНАЧЕН 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

задача_корень = Path(__file__).resolve().parent


def 실행(Word_SMS):
    subprocess.check_call([str(ввод_ЗНАЧЕН) for ввод_ЗНАЧЕН in Word_SMS], cwd=str(задача_корень))


def запустить():
    анализатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    анализатор_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 проверять')
    анализатор_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a использовать_ЗНАЧЕН')
    анализатор_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 повторить_попытку_ЗНАЧЕН 컴파일하고 커널에 탑재')
    анализатор_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    аргументы = анализатор_48ee4b1b.parse_args()
    спецификация = json.loads((задача_корень / 'relink.json').read_text())
    сборка = задача_корень / 'build'
    새묶음 = сборка / 'relinked'
    새묶음.mkdir(exist_ok=True)
    компилятор_средство = os.environ.get('ARM64_CC', 'clang')
    разъем = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Архив_средство = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    удаленный_Настройки = json.loads((сборка / 'remote/libassh-build.json').read_text())
    Настройки = удаленный_Настройки['flags']
    if аргументы.libassh_archive:
        Безопасность_пакет = аргументы.libassh_archive.resolve()
    else:
        목적들 = []
        объявления = ['-I', задача_корень / 'удаленный_ЗНАЧЕН', '-I', задача_корень / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Название in удаленный_Настройки['sources']:
            цель_ЗНАЧЕН = 새묶음 / (Path(Название).stem + '.o')
            실행([компилятор_средство] + Настройки + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + объявления +
                 ['-c', задача_корень / Название, '-o', цель_ЗНАЧЕН])
            목적들.append(цель_ЗНАЧЕН)
        Безопасность_пакет = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            실행([Архив_средство, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Безопасность_пакет)
    if аргументы.tinycc:
        if not аргументы.sdk:
            анализатор_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = аргументы.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            анализатор_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [выделение_ЗНАЧЕН for выделение_ЗНАЧЕН in Настройки if выделение_ЗНАЧЕН != '-mgeneral-regs-only']
        цель_ЗНАЧЕН = 새묶음 / 'компилятор_средство.o'
        실행([компилятор_средство] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', задача_корень / 'C_компилятор', '-I', задача_корень / 'vendor/tinycc', '-I', задача_корень / 'пространство_пользователя',
             '-I', сборка / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', задача_корень / 'C_компилятор/компилятор_средство.c', '-o', цель_ЗНАЧЕН])
        실행([разъем, '--gc-sections', '-T', задача_корень / 'пространство_пользователя/схема_компоновки.ld', '-z', 'max-page-size=4096',
             '-o', сборка / 'user/cc.elf', сборка / 'user/start.o', сборка / 'user/runtime.o', цель_ЗНАЧЕН] +
             [сборка / 'ccompiler' / (Название + '.o') for Название in ('ПоддержкаВыполнения', 'запустить', '미리번역', 'Возврат_мост')] +
             [сборка / 'user' / (Название + '.o') for Название in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        HEAD_ЗНАЧЕН = сборка / 'programs.h'
        HEAD_ЗНАЧЕН.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((сборка / 'user/cc.elf').stat().st_size), HEAD_ЗНАЧЕН.read_text()))
        실행([компилятор_средство] + Настройки + ['-c', сборка / 'programs.S', '-o', задача_корень / 'objects/programs.o'])
        실행([компилятор_средство] + Настройки + ['-std=c11', '-I', задача_корень / 'posix-kor/arm64-native/объявления', '-I', сборка,
             '-c', задача_корень / 'компьютер_5eb260fa/пространство_пользователя.c', '-o', задача_корень / 'objects/user.o'])
    실행([разъем, '--gc-sections', '-T', задача_корень / 'запуск_машины/схема_компоновки.ld', '-o', 새묶음 / 'kernel.elf'] +
         [задача_корень / путь for путь in спецификация['objects']] + ['--start-group'] +
         [Безопасность_пакет if путь == 'objects/libassh.a' else задача_корень / путь for путь in спецификация['libraries']] + ['--end-group'])
    실행([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    хэш_файл = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if аргументы.verify and хэш_файл != спецификация['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + хэш_файл)
    print('RELINK PASS', хэш_файл, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    запустить()
