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

projezéieren_Racinn = Path(__file__).resolve().parent


def ausféieren_Befeel(Word_SMS):
    subprocess.check_call([str(Agab_VALUE) for Agab_VALUE in Word_SMS], cwd=str(projezéieren_Racinn))


def Laf():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 verifizéieren')
    해석기.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    해석기.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    해석기.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = 해석기.parse_args()
    명세 = json.loads((projezéieren_Racinn / 'relink.json').read_text())
    Build_System = projezéieren_Racinn / 'build'
    새묶음 = Build_System / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    Konnektor = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Archiv_Tool = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    extern_Astellungen = json.loads((Build_System / 'remote/libassh-build.json').read_text())
    Astellungen = extern_Astellungen['flags']
    if 인수.libassh_archive:
        Sécherheet_Bëndel = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', projezéieren_Racinn / 'extern_VALUE', '-I', projezéieren_Racinn / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Numm in extern_Astellungen['sources']:
            Zil_VALUE = 새묶음 / (Path(Numm).stem + '.o')
            ausféieren_Befeel([번역기] + Astellungen + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', projezéieren_Racinn / Numm, '-o', Zil_VALUE])
            목적들.append(Zil_VALUE)
        Sécherheet_Bëndel = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            ausféieren_Befeel([Archiv_Tool, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Sécherheet_Bëndel)
    if 인수.tinycc:
        if not 인수.sdk:
            해석기.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            해석기.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [Auswiel_VALUE for Auswiel_VALUE in Astellungen if Auswiel_VALUE != '-mgeneral-regs-only']
        Zil_VALUE = 새묶음 / '번역기.o'
        ausféieren_Befeel([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', projezéieren_Racinn / '시언어번역기', '-I', projezéieren_Racinn / 'vendor/tinycc', '-I', projezéieren_Racinn / 'Benotzer',
             '-I', Build_System / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', projezéieren_Racinn / '시언어번역기/번역기.c', '-o', Zil_VALUE])
        ausféieren_Befeel([Konnektor, '--gc-sections', '-T', projezéieren_Racinn / 'Benotzer/Link_Layout.ld', '-z', 'max-page-size=4096',
             '-o', Build_System / 'user/cc.elf', Build_System / 'user/start.o', Build_System / 'user/runtime.o', Zil_VALUE] +
             [Build_System / 'ccompiler' / (Numm + '.o') for Numm in ('Common_Language_Runtime_Support', 'Laf', '미리번역', '되돌림')] +
             [Build_System / 'user' / (Numm + '.o') for Numm in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = Build_System / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((Build_System / 'user/cc.elf').stat().st_size), 머리.read_text()))
        ausféieren_Befeel([번역기] + Astellungen + ['-c', Build_System / 'programs.S', '-o', projezéieren_Racinn / 'objects/programs.o'])
        ausféieren_Befeel([번역기] + Astellungen + ['-std=c11', '-I', projezéieren_Racinn / 'posix-kor/arm64-native/포함', '-I', Build_System,
             '-c', projezéieren_Racinn / 'Computer/Benotzer.c', '-o', projezéieren_Racinn / 'objects/user.o'])
    ausféieren_Befeel([Konnektor, '--gc-sections', '-T', projezéieren_Racinn / '부팅/Link_Layout.ld', '-o', 새묶음 / 'kernel.elf'] +
         [projezéieren_Racinn / Wee for Wee in 명세['objects']] + ['--start-group'] +
         [Sécherheet_Bëndel if Wee == 'objects/libassh.a' else projezéieren_Racinn / Wee for Wee in 명세['libraries']] + ['--end-group'])
    ausféieren_Befeel([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    Hash_Fichier = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and Hash_Fichier != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + Hash_Fichier)
    print('RELINK PASS', Hash_Fichier, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Laf()
