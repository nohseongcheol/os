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

Project_rrënjë = Path(__file__).resolve().parent


def zbatoj_komandë(Word_SMS):
    subprocess.check_call([str(futje_VALUE) for futje_VALUE in Word_SMS], cwd=str(Project_rrënjë))


def Ekzekuto():
    analizues_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizues_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 verifikoj')
    analizues_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    analizues_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    analizues_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    Argumente = analizues_48ee4b1b.parse_args()
    명세 = json.loads((Project_rrënjë / 'relink.json').read_text())
    ndërtoj_sistem = Project_rrënjë / 'build'
    새묶음 = ndërtoj_sistem / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    bashkues = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    arkiv_vegël = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    në_largësi_cilësimet = json.loads((ndërtoj_sistem / 'remote/libassh-build.json').read_text())
    Rregullime = në_largësi_cilësimet['flags']
    if Argumente.libassh_archive:
        siguri_grupoj = Argumente.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', Project_rrënjë / 'në_largësi_VALUE', '-I', Project_rrënjë / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Emër in në_largësi_cilësimet['sources']:
            vendmbërritje_VALUE = 새묶음 / (Path(Emër).stem + '.o')
            zbatoj_komandë([번역기] + Rregullime + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', Project_rrënjë / Emër, '-o', vendmbërritje_VALUE])
            목적들.append(vendmbërritje_VALUE)
        siguri_grupoj = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            zbatoj_komandë([arkiv_vegël, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(siguri_grupoj)
    if Argumente.tinycc:
        if not Argumente.sdk:
            analizues_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = Argumente.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            analizues_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [përzgjedhje_VALUE for përzgjedhje_VALUE in Rregullime if përzgjedhje_VALUE != '-mgeneral-regs-only']
        vendmbërritje_VALUE = 새묶음 / '번역기.o'
        zbatoj_komandë([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', Project_rrënjë / '시언어번역기', '-I', Project_rrënjë / 'vendor/tinycc', '-I', Project_rrënjë / 'përdorues',
             '-I', ndërtoj_sistem / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', Project_rrënjë / '시언어번역기/번역기.c', '-o', vendmbërritje_VALUE])
        zbatoj_komandë([bashkues, '--gc-sections', '-T', Project_rrënjë / 'përdorues/lidh_Navigimi.ld', '-z', 'max-page-size=4096',
             '-o', ndërtoj_sistem / 'user/cc.elf', ndërtoj_sistem / 'user/start.o', ndërtoj_sistem / 'user/runtime.o', vendmbërritje_VALUE] +
             [ndërtoj_sistem / 'ccompiler' / (Emër + '.o') for Emër in ('koha_e_ekzekutimit_të_gjuhës_së_zakonshme_Mbështetje', 'Ekzekuto', '미리번역', 'Kthe_urë')] +
             [ndërtoj_sistem / 'user' / (Emër + '.o') for Emër in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = ndërtoj_sistem / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((ndërtoj_sistem / 'user/cc.elf').stat().st_size), 머리.read_text()))
        zbatoj_komandë([번역기] + Rregullime + ['-c', ndërtoj_sistem / 'programs.S', '-o', Project_rrënjë / 'objects/programs.o'])
        zbatoj_komandë([번역기] + Rregullime + ['-std=c11', '-I', Project_rrënjë / 'posix-kor/arm64-native/포함', '-I', ndërtoj_sistem,
             '-c', Project_rrënjë / 'makinë/përdorues.c', '-o', Project_rrënjë / 'objects/user.o'])
    zbatoj_komandë([bashkues, '--gc-sections', '-T', Project_rrënjë / '부팅/lidh_Navigimi.ld', '-o', 새묶음 / 'kernel.elf'] +
         [Project_rrënjë / POZICIONI for POZICIONI in 명세['objects']] + ['--start-group'] +
         [siguri_grupoj if POZICIONI == 'objects/libassh.a' else Project_rrënjë / POZICIONI for POZICIONI in 명세['libraries']] + ['--end-group'])
    zbatoj_komandë([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    hash_skedar = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if Argumente.verify and hash_skedar != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + hash_skedar)
    print('RELINK PASS', hash_skedar, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Ekzekuto()
