#!/usr/bin/env python3
"""배포 묶음에서 libassh/TinyCC를 교체하고 자체 커널을 pokušati_ponovo_VALUE 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

radnja_koren = Path(__file__).resolve().parent


def Izvrši_komanda(Word_SMS):
    subprocess.check_call([str(stavka_VALUE) for stavka_VALUE in Word_SMS], cwd=str(radnja_koren))


def koristiti():
    analizator_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizator_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 verifikovati')
    analizator_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a koristiti_VALUE')
    analizator_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 pokušati_ponovo_VALUE 컴파일하고 커널에 탑재')
    analizator_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = analizator_48ee4b1b.parse_args()
    명세 = json.loads((radnja_koren / 'relink.json').read_text())
    verzija_sistem = radnja_koren / 'build'
    새묶음 = verzija_sistem / 'relinked'
    새묶음.mkdir(exist_ok=True)
    kompajler_alatka = os.environ.get('ARM64_CC', 'clang')
    Konektor = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Arhiva_alatka = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    udaljen_Postavke = json.loads((verzija_sistem / 'remote/libassh-build.json').read_text())
    Postavke = udaljen_Postavke['flags']
    if 인수.libassh_archive:
        Bezbednost_komplet = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', radnja_koren / 'udaljen_VALUE', '-I', radnja_koren / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for ime in udaljen_Postavke['sources']:
            odredište_VALUE = 새묶음 / (Path(ime).stem + '.o')
            Izvrši_komanda([kompajler_alatka] + Postavke + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', radnja_koren / ime, '-o', odredište_VALUE])
            목적들.append(odredište_VALUE)
        Bezbednost_komplet = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            Izvrši_komanda([Arhiva_alatka, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Bezbednost_komplet)
    if 인수.tinycc:
        if not 인수.sdk:
            analizator_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            analizator_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [izbor_VALUE for izbor_VALUE in Postavke if izbor_VALUE != '-mgeneral-regs-only']
        odredište_VALUE = 새묶음 / 'kompajler_alatka.o'
        Izvrši_komanda([kompajler_alatka] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', radnja_koren / 'C_kompajler', '-I', radnja_koren / 'vendor/tinycc', '-I', radnja_koren / 'korisnik',
             '-I', verzija_sistem / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', radnja_koren / 'C_kompajler/kompajler_alatka.c', '-o', odredište_VALUE])
        Izvrši_komanda([Konektor, '--gc-sections', '-T', radnja_koren / 'korisnik/Veza_Raspored.ld', '-z', 'max-page-size=4096',
             '-o', verzija_sistem / 'user/cc.elf', verzija_sistem / 'user/start.o', verzija_sistem / 'user/runtime.o', odredište_VALUE] +
             [verzija_sistem / 'ccompiler' / (ime + '.o') for ime in ('CLR_komponenta_Podrška', 'koristiti', '미리번역', 'vratiti_most')] +
             [verzija_sistem / 'user' / (ime + '.o') for ime in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = verzija_sistem / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((verzija_sistem / 'user/cc.elf').stat().st_size), 머리.read_text()))
        Izvrši_komanda([kompajler_alatka] + Postavke + ['-c', verzija_sistem / 'programs.S', '-o', radnja_koren / 'objects/programs.o'])
        Izvrši_komanda([kompajler_alatka] + Postavke + ['-std=c11', '-I', radnja_koren / 'posix-kor/arm64-native/포함', '-I', verzija_sistem,
             '-c', radnja_koren / 'računar/korisnik.c', '-o', radnja_koren / 'objects/user.o'])
    Izvrši_komanda([Konektor, '--gc-sections', '-T', radnja_koren / '부팅/Veza_Raspored.ld', '-o', 새묶음 / 'kernel.elf'] +
         [radnja_koren / putanja for putanja in 명세['objects']] + ['--start-group'] +
         [Bezbednost_komplet if putanja == 'objects/libassh.a' else radnja_koren / putanja for putanja in 명세['libraries']] + ['--end-group'])
    Izvrši_komanda([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    heš_Datoteka = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and heš_Datoteka != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + heš_Datoteka)
    print('RELINK PASS', heš_Datoteka, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    koristiti()
