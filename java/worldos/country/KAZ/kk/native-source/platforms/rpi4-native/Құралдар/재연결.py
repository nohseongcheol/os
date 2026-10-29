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

жоба_түбір = Path(__file__).resolve().parent


def орындау_пәрмен(Сөз_Мәтін):
    subprocess.check_call([str(енгізу_мән) for енгізу_мән in Сөз_Мәтін], cwd=str(жоба_түбір))


def Орындау_2():
    талдау_құралы_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    талдау_құралы_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 тексеру')
    талдау_құралы_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    талдау_құралы_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    талдау_құралы_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    Аргументтер = талдау_құралы_48ee4b1b.parse_args()
    сипаттама = json.loads((жоба_түбір / 'relink.json').read_text())
    құрастыру_жүйе = жоба_түбір / 'build'
    새묶음 = құрастыру_жүйе / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    Қосқыш = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Мұрағат_құрал = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    원격설정 = json.loads((құрастыру_жүйе / 'remote/libassh-build.json').read_text())
    Баптаулар = 원격설정['flags']
    if Аргументтер.libassh_archive:
        Қауіпсіздік_жинау = Аргументтер.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', жоба_түбір / '원격', '-I', жоба_түбір / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Аты in 원격설정['sources']:
            тағайындау_мән = 새묶음 / (Path(Аты).stem + '.o')
            орындау_пәрмен([번역기] + Баптаулар + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', жоба_түбір / Аты, '-o', тағайындау_мән])
            목적들.append(тағайындау_мән)
        Қауіпсіздік_жинау = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            орындау_пәрмен([Мұрағат_құрал, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Қауіпсіздік_жинау)
    if Аргументтер.tinycc:
        if not Аргументтер.sdk:
            талдау_құралы_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = Аргументтер.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            талдау_құралы_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [таңдау_мән for таңдау_мән in Баптаулар if таңдау_мән != '-mgeneral-regs-only']
        тағайындау_мән = 새묶음 / '번역기.o'
        орындау_пәрмен([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', жоба_түбір / '시언어번역기', '-I', жоба_түбір / 'vendor/tinycc', '-I', жоба_түбір / 'пайдаланушы',
             '-I', құрастыру_жүйе / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', жоба_түбір / '시언어번역기/번역기.c', '-o', тағайындау_мән])
        орындау_пәрмен([Қосқыш, '--gc-sections', '-T', жоба_түбір / 'пайдаланушы/Cілтеме_макет.ld', '-z', 'max-page-size=4096',
             '-o', құрастыру_жүйе / 'user/cc.elf', құрастыру_жүйе / 'user/start.o', құрастыру_жүйе / 'user/runtime.o', тағайындау_мән] +
             [құрастыру_жүйе / 'ccompiler' / (Аты + '.o') for Аты in ('CLR_ортасы_тіреу', 'Орындау_2', '미리번역', 'қайтару_көпір')] +
             [құрастыру_жүйе / 'user' / (Аты + '.o') for Аты in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = құрастыру_жүйе / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((құрастыру_жүйе / 'user/cc.elf').stat().st_size), 머리.read_text()))
        орындау_пәрмен([번역기] + Баптаулар + ['-c', құрастыру_жүйе / 'programs.S', '-o', жоба_түбір / 'objects/programs.o'])
        орындау_пәрмен([번역기] + Баптаулар + ['-std=c11', '-I', жоба_түбір / 'posix-kor/arm64-native/포함', '-I', құрастыру_жүйе,
             '-c', жоба_түбір / 'компьютер/пайдаланушы.c', '-o', жоба_түбір / 'objects/user.o'])
    орындау_пәрмен([Қосқыш, '--gc-sections', '-T', жоба_түбір / '부팅/Cілтеме_макет.ld', '-o', 새묶음 / 'kernel.elf'] +
         [жоба_түбір / Жол_2 for Жол_2 in сипаттама['objects']] + ['--start-group'] +
         [Қауіпсіздік_жинау if Жол_2 == 'objects/libassh.a' else жоба_түбір / Жол_2 for Жол_2 in сипаттама['libraries']] + ['--end-group'])
    орындау_пәрмен([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    хэш_файл = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if Аргументтер.verify and хэш_файл != сипаттама['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + хэш_файл)
    print('RELINK PASS', хэш_файл, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Орындау_2()
