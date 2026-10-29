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


def иҷро_кардан_фармон(Калимабозӣ_Матн):
    subprocess.check_call([str(ворида_қимат) for ворида_қимат in Калимабозӣ_Матн], cwd=str(기준))


def порча():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 тасдиқ_кардан')
    해석기.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    해석기.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    해석기.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = 해석기.parse_args()
    명세 = json.loads((기준 / 'relink.json').read_text())
    сохт_система = 기준 / 'build'
    새묶음 = сохт_система / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    васлгар = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Бойгонӣ_абзор = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    дурдаст_Танзимот = json.loads((сохт_система / 'remote/libassh-build.json').read_text())
    Танзимот = дурдаст_Танзимот['flags']
    if 인수.libassh_archive:
        Амният_баста = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', 기준 / 'дурдаст_қимат', '-I', 기준 / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Ном in дурдаст_Танзимот['sources']:
            ҷои_таъинот_қимат = 새묶음 / (Path(Ном).stem + '.o')
            иҷро_кардан_фармон([번역기] + Танзимот + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', 기준 / Ном, '-o', ҷои_таъинот_қимат])
            목적들.append(ҷои_таъинот_қимат)
        Амният_баста = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            иҷро_кардан_фармон([Бойгонӣ_абзор, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Амният_баста)
    if 인수.tinycc:
        if not 인수.sdk:
            해석기.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            해석기.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [интихоб_қимат for интихоб_қимат in Танзимот if интихоб_қимат != '-mgeneral-regs-only']
        ҷои_таъинот_қимат = 새묶음 / '번역기.o'
        иҷро_кардан_фармон([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', 기준 / '시언어번역기', '-I', 기준 / 'vendor/tinycc', '-I', 기준 / 'корбар',
             '-I', сохт_система / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', 기준 / '시언어번역기/번역기.c', '-o', ҷои_таъинот_қимат])
        иҷро_кардан_фармон([васлгар, '--gc-sections', '-T', 기준 / 'корбар/Пайванд_Тарҳбандӣ.ld', '-z', 'max-page-size=4096',
             '-o', сохт_система / 'user/cc.elf', сохт_система / 'user/start.o', сохт_система / 'user/runtime.o', ҷои_таъинот_қимат] +
             [сохт_система / 'ccompiler' / (Ном + '.o') for Ном in ('вақти_иҷрои_умумии_забон_Дастгирӣ', 'порча', '미리번역', '되돌림')] +
             [сохт_система / 'user' / (Ном + '.o') for Ном in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = сохт_система / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((сохт_система / 'user/cc.elf').stat().st_size), 머리.read_text()))
        иҷро_кардан_фармон([번역기] + Танзимот + ['-c', сохт_система / 'programs.S', '-o', 기준 / 'objects/programs.o'])
        иҷро_кардан_фармон([번역기] + Танзимот + ['-std=c11', '-I', 기준 / 'posix-kor/arm64-native/포함', '-I', сохт_система,
             '-c', 기준 / 'компютер/корбар.c', '-o', 기준 / 'objects/user.o'])
    иҷро_кардан_фармон([васлгар, '--gc-sections', '-T', 기준 / '부팅/Пайванд_Тарҳбандӣ.ld', '-o', 새묶음 / 'kernel.elf'] +
         [기준 / масир for масир in 명세['objects']] + ['--start-group'] +
         [Амният_баста if масир == 'objects/libassh.a' else 기준 / масир for масир in 명세['libraries']] + ['--end-group'])
    иҷро_кардан_фармон([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    ҳэш_файл = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and ҳэш_файл != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + ҳэш_файл)
    print('RELINK PASS', ҳэш_файл, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    порча()
