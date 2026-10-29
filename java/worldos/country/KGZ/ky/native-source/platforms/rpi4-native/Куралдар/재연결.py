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


def аткаруу_буйрук(Сөз_СМС):
    subprocess.check_call([str(киргизме_жазуу_маани) for киргизме_жазуу_маани in Сөз_СМС], cwd=str(기준))


def Жүргүзүү():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 тууралыгын_аныктоо')
    해석기.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    해석기.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    해석기.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = 해석기.parse_args()
    명세 = json.loads((기준 / 'relink.json').read_text())
    курам_тутум = 기준 / 'build'
    새묶음 = курам_тутум / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    туташтыргыч = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Архив_курал = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    алыскы_Орнотуулар = json.loads((курам_тутум / 'remote/libassh-build.json').read_text())
    Орнотуулар = алыскы_Орнотуулар['flags']
    if 인수.libassh_archive:
        Коопсуздук_пакет = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', 기준 / 'алыскы_маани', '-I', 기준 / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Аты in алыскы_Орнотуулар['sources']:
            көздөө_жайы_маани = 새묶음 / (Path(Аты).stem + '.o')
            аткаруу_буйрук([번역기] + Орнотуулар + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', 기준 / Аты, '-o', көздөө_жайы_маани])
            목적들.append(көздөө_жайы_маани)
        Коопсуздук_пакет = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            аткаруу_буйрук([Архив_курал, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Коопсуздук_пакет)
    if 인수.tinycc:
        if not 인수.sdk:
            해석기.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            해석기.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [белгилөө_маани for белгилөө_маани in Орнотуулар if белгилөө_маани != '-mgeneral-regs-only']
        көздөө_жайы_маани = 새묶음 / '번역기.o'
        аткаруу_буйрук([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', 기준 / '시언어번역기', '-I', 기준 / 'vendor/tinycc', '-I', 기준 / 'колдонуучу',
             '-I', курам_тутум / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', 기준 / '시언어번역기/번역기.c', '-o', көздөө_жайы_маани])
        аткаруу_буйрук([туташтыргыч, '--gc-sections', '-T', 기준 / 'колдонуучу/Шилтеме_түзүлүш.ld', '-z', 'max-page-size=4096',
             '-o', курам_тутум / 'user/cc.elf', курам_тутум / 'user/start.o', курам_тутум / 'user/runtime.o', көздөө_жайы_маани] +
             [курам_тутум / 'ccompiler' / (Аты + '.o') for Аты in ('кадимки_тилдин_аткаруу_убагы_Колдоо', 'Жүргүзүү', '미리번역', '되돌림')] +
             [курам_тутум / 'user' / (Аты + '.o') for Аты in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = курам_тутум / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((курам_тутум / 'user/cc.elf').stat().st_size), 머리.read_text()))
        аткаруу_буйрук([번역기] + Орнотуулар + ['-c', курам_тутум / 'programs.S', '-o', 기준 / 'objects/programs.o'])
        аткаруу_буйрук([번역기] + Орнотуулар + ['-std=c11', '-I', 기준 / 'posix-kor/arm64-native/포함', '-I', курам_тутум,
             '-c', 기준 / 'машина/колдонуучу.c', '-o', 기준 / 'objects/user.o'])
    аткаруу_буйрук([туташтыргыч, '--gc-sections', '-T', 기준 / '부팅/Шилтеме_түзүлүш.ld', '-o', 새묶음 / 'kernel.elf'] +
         [기준 / ЖОЛ for ЖОЛ in 명세['objects']] + ['--start-group'] +
         [Коопсуздук_пакет if ЖОЛ == 'objects/libassh.a' else 기준 / ЖОЛ for ЖОЛ in 명세['libraries']] + ['--end-group'])
    аткаруу_буйрук([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    хэш_файл = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and хэш_файл != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + хэш_файл)
    print('RELINK PASS', хэш_файл, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Жүргүзүү()
