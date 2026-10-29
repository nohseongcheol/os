#!/usr/bin/env python3
"""배포 묶음에서 libassh/TinyCC를 교체하고 vlastiti 커널을 pokušati_ponovno_VALUE 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

akcija_korijen = Path(__file__).resolve().parent


def Izvrši_naredba(Word_SMS):
    subprocess.check_call([str(unos_VALUE) for unos_VALUE in Word_SMS], cwd=str(akcija_korijen))


def Pokreni():
    analizator_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizator_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 provjeriti')
    analizator_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a uporaba_VALUE')
    analizator_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 pokušati_ponovno_VALUE 컴파일하고 커널에 탑재')
    analizator_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    Argumenti = analizator_48ee4b1b.parse_args()
    명세 = json.loads((akcija_korijen / 'relink.json').read_text())
    međuverzija_sustav = akcija_korijen / 'build'
    새묶음 = međuverzija_sustav / 'relinked'
    새묶음.mkdir(exist_ok=True)
    kompilator_alat = os.environ.get('ARM64_CC', 'clang')
    Poveznik = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Arhiva_alat = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    udaljeno_Postavke = json.loads((međuverzija_sustav / 'remote/libassh-build.json').read_text())
    Postavke = udaljeno_Postavke['flags']
    if Argumenti.libassh_archive:
        Sigurnost_komplet = Argumenti.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', akcija_korijen / 'udaljeno_VALUE', '-I', akcija_korijen / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Ime in udaljeno_Postavke['sources']:
            odredište_VALUE = 새묶음 / (Path(Ime).stem + '.o')
            Izvrši_naredba([kompilator_alat] + Postavke + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', akcija_korijen / Ime, '-o', odredište_VALUE])
            목적들.append(odredište_VALUE)
        Sigurnost_komplet = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            Izvrši_naredba([Arhiva_alat, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Sigurnost_komplet)
    if Argumenti.tinycc:
        if not Argumenti.sdk:
            analizator_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = Argumenti.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            analizator_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [odabir_VALUE for odabir_VALUE in Postavke if odabir_VALUE != '-mgeneral-regs-only']
        odredište_VALUE = 새묶음 / 'kompilator_alat.o'
        Izvrši_naredba([kompilator_alat] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', akcija_korijen / 'C_kompilator', '-I', akcija_korijen / 'vendor/tinycc', '-I', akcija_korijen / 'korisnik',
             '-I', međuverzija_sustav / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', akcija_korijen / 'C_kompilator/kompilator_alat.c', '-o', odredište_VALUE])
        Izvrši_naredba([Poveznik, '--gc-sections', '-T', akcija_korijen / 'korisnik/veza_Raspored.ld', '-z', 'max-page-size=4096',
             '-o', međuverzija_sustav / 'user/cc.elf', međuverzija_sustav / 'user/start.o', međuverzija_sustav / 'user/runtime.o', odredište_VALUE] +
             [međuverzija_sustav / 'ccompiler' / (Ime + '.o') for Ime in ('CLR_Podrška', 'Pokreni', '미리번역', 'vratiti_most')] +
             [međuverzija_sustav / 'user' / (Ime + '.o') for Ime in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = međuverzija_sustav / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((međuverzija_sustav / 'user/cc.elf').stat().st_size), 머리.read_text()))
        Izvrši_naredba([kompilator_alat] + Postavke + ['-c', međuverzija_sustav / 'programs.S', '-o', akcija_korijen / 'objects/programs.o'])
        Izvrši_naredba([kompilator_alat] + Postavke + ['-std=c11', '-I', akcija_korijen / 'posix-kor/arm64-native/포함', '-I', međuverzija_sustav,
             '-c', akcija_korijen / 'stroj/korisnik.c', '-o', akcija_korijen / 'objects/user.o'])
    Izvrši_naredba([Poveznik, '--gc-sections', '-T', akcija_korijen / '부팅/veza_Raspored.ld', '-o', 새묶음 / 'kernel.elf'] +
         [akcija_korijen / PUTANJA for PUTANJA in 명세['objects']] + ['--start-group'] +
         [Sigurnost_komplet if PUTANJA == 'objects/libassh.a' else akcija_korijen / PUTANJA for PUTANJA in 명세['libraries']] + ['--end-group'])
    Izvrši_naredba([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    raspršivanje_Datoteka = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if Argumenti.verify and raspršivanje_Datoteka != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + raspršivanje_Datoteka)
    print('RELINK PASS', raspršivanje_Datoteka, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Pokreni()
