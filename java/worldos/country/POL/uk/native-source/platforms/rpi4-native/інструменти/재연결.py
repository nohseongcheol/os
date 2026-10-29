#!/usr/bin/env python3
"""배포 묶음에서 libassh/TinyCC를 교체하고 своє 커널을 пробувати_знову_значення 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

Дії_корінь = Path(__file__).resolve().parent


def Виконати_команда(Ігри_в_слова_Текст):
    subprocess.check_call([str(запис_значення_962f286b) for запис_значення_962f286b in Ігри_в_слова_Текст], cwd=str(Дії_корінь))


def запустити():
    аналізатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    аналізатор_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 перевіряти')
    аналізатор_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a використання_значення')
    аналізатор_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 пробувати_знову_значення 컴파일하고 커널에 탑재')
    аналізатор_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    аргументи = аналізатор_48ee4b1b.parse_args()
    명세 = json.loads((Дії_корінь / 'relink.json').read_text())
    збирання = Дії_корінь / 'build'
    새묶음 = збирання / 'relinked'
    새묶음.mkdir(exist_ok=True)
    компілятор_інструмент = os.environ.get('ARM64_CC', 'clang')
    Конектор = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Архів_інструмент = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    віддалений_Настройки = json.loads((збирання / 'remote/libassh-build.json').read_text())
    Налаштування = віддалений_Настройки['flags']
    if аргументи.libassh_archive:
        захист_набір = аргументи.libassh_archive.resolve()
    else:
        목적들 = []
        оголошення = ['-I', Дії_корінь / 'віддалений_значення', '-I', Дії_корінь / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Назва in віддалений_Настройки['sources']:
            місце_значення = 새묶음 / (Path(Назва).stem + '.o')
            Виконати_команда([компілятор_інструмент] + Налаштування + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + оголошення +
                 ['-c', Дії_корінь / Назва, '-o', місце_значення])
            목적들.append(місце_значення)
        захист_набір = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            Виконати_команда([Архів_інструмент, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(захист_набір)
    if аргументи.tinycc:
        if not аргументи.sdk:
            аналізатор_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = аргументи.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            аналізатор_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [вибране_значення for вибране_значення in Налаштування if вибране_значення != '-mgeneral-regs-only']
        місце_значення = 새묶음 / 'компілятор_інструмент.o'
        Виконати_команда([компілятор_інструмент] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', Дії_корінь / '시언어번역기', '-I', Дії_корінь / 'vendor/tinycc', '-I', Дії_корінь / 'простір_користувача',
             '-I', збирання / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', Дії_корінь / '시언어번역기/компілятор_інструмент.c', '-o', місце_значення])
        Виконати_команда([Конектор, '--gc-sections', '-T', Дії_корінь / 'простір_користувача/схема_компонування.ld', '-z', 'max-page-size=4096',
             '-o', збирання / 'user/cc.elf', збирання / 'user/start.o', збирання / 'user/runtime.o', місце_значення] +
             [збирання / 'ccompiler' / (Назва + '.o') for Назва in ('загальномовне_середовище_виконання_опора', 'запустити', '미리번역', 'повернути_міст')] +
             [збирання / 'user' / (Назва + '.o') for Назва in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = збирання / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((збирання / 'user/cc.elf').stat().st_size), 머리.read_text()))
        Виконати_команда([компілятор_інструмент] + Налаштування + ['-c', збирання / 'programs.S', '-o', Дії_корінь / 'objects/programs.o'])
        Виконати_команда([компілятор_інструмент] + Налаштування + ['-std=c11', '-I', Дії_корінь / 'posix-kor/arm64-native/оголошення', '-I', збирання,
             '-c', Дії_корінь / 'комп_ютер/простір_користувача.c', '-o', Дії_корінь / 'objects/user.o'])
    Виконати_команда([Конектор, '--gc-sections', '-T', Дії_корінь / 'запуск_машини/схема_компонування.ld', '-o', 새묶음 / 'kernel.elf'] +
         [Дії_корінь / шлях for шлях in 명세['objects']] + ['--start-group'] +
         [захист_набір if шлях == 'objects/libassh.a' else Дії_корінь / шлях for шлях in 명세['libraries']] + ['--end-group'])
    Виконати_команда([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    геш_код_Файл = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if аргументи.verify and геш_код_Файл != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + геш_код_Файл)
    print('RELINK PASS', геш_код_Файл, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    запустити()
