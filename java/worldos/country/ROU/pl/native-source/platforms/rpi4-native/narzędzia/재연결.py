#!/usr/bin/env python3
"""dystrybucja_WARTOŚĆ 묶음에서 libassh/TinyCC를 교체하고 własny 커널을 다시 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

Project_korzeń = Path(__file__).resolve().parent


def Wykonaj_polecenie(Word_SMS):
    subprocess.check_call([str(wpis_WARTOŚĆ) for wpis_WARTOŚĆ in Word_SMS], cwd=str(Project_korzeń))


def Uruchom_2():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 확인')
    parser_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a używać_WARTOŚĆ')
    parser_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    parser_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    argumenty = parser_48ee4b1b.parse_args()
    명세 = json.loads((Project_korzeń / 'relink.json').read_text())
    BLD_System = Project_korzeń / 'build'
    새묶음 = BLD_System / 'relinked'
    새묶음.mkdir(exist_ok=True)
    kompilator_narzędzie = os.environ.get('ARM64_CC', 'clang')
    Łącznik = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Archiwum_narzędzie = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    zdalny_Ustawienia = json.loads((BLD_System / 'remote/libassh-build.json').read_text())
    Ustawienia = zdalny_Ustawienia['flags']
    if argumenty.libassh_archive:
        Zabezpieczenia_pakiet = argumenty.libassh_archive.resolve()
    else:
        목적들 = []
        deklaracje = ['-I', Project_korzeń / 'zdalny_WARTOŚĆ', '-I', Project_korzeń / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Nazwa in zdalny_Ustawienia['sources']:
            cel_WARTOŚĆ = 새묶음 / (Path(Nazwa).stem + '.o')
            Wykonaj_polecenie([kompilator_narzędzie] + Ustawienia + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + deklaracje +
                 ['-c', Project_korzeń / Nazwa, '-o', cel_WARTOŚĆ])
            목적들.append(cel_WARTOŚĆ)
        Zabezpieczenia_pakiet = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            Wykonaj_polecenie([Archiwum_narzędzie, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Zabezpieczenia_pakiet)
    if argumenty.tinycc:
        if not argumenty.sdk:
            parser_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        materiał_pochodny = argumenty.sdk.resolve()
        산술 = sorted((materiał_pochodny / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (materiał_pochodny / 'usr/include/stdio.h').is_file():
            parser_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [zaznaczenie_WARTOŚĆ for zaznaczenie_WARTOŚĆ in Ustawienia if zaznaczenie_WARTOŚĆ != '-mgeneral-regs-only']
        cel_WARTOŚĆ = 새묶음 / 'kompilator_narzędzie.o'
        Wykonaj_polecenie([kompilator_narzędzie] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', Project_korzeń / 'C_kompilator', '-I', Project_korzeń / 'vendor/tinycc', '-I', Project_korzeń / 'przestrzeń_użytkownika',
             '-I', BLD_System / 'ccompiler', '-isystem', materiał_pochodny / 'usr/include', '-c', Project_korzeń / 'C_kompilator/kompilator_narzędzie.c', '-o', cel_WARTOŚĆ])
        Wykonaj_polecenie([Łącznik, '--gc-sections', '-T', Project_korzeń / 'przestrzeń_użytkownika/układ_konsolidacji.ld', '-z', 'max-page-size=4096',
             '-o', BLD_System / 'user/cc.elf', BLD_System / 'user/start.o', BLD_System / 'user/runtime.o', cel_WARTOŚĆ] +
             [BLD_System / 'ccompiler' / (Nazwa + '.o') for Nazwa in ('CLR_wsparcie', 'Uruchom_2', '미리번역', 'Zwrot_mostek')] +
             [BLD_System / 'user' / (Nazwa + '.o') for Nazwa in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = BLD_System / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((BLD_System / 'user/cc.elf').stat().st_size), 머리.read_text()))
        Wykonaj_polecenie([kompilator_narzędzie] + Ustawienia + ['-c', BLD_System / 'programs.S', '-o', Project_korzeń / 'objects/programs.o'])
        Wykonaj_polecenie([kompilator_narzędzie] + Ustawienia + ['-std=c11', '-I', Project_korzeń / 'posix-kor/arm64-native/deklaracje', '-I', BLD_System,
             '-c', Project_korzeń / 'maszyna/przestrzeń_użytkownika.c', '-o', Project_korzeń / 'objects/user.o'])
    Wykonaj_polecenie([Łącznik, '--gc-sections', '-T', Project_korzeń / 'rozruch_maszyny/układ_konsolidacji.ld', '-o', 새묶음 / 'kernel.elf'] +
         [Project_korzeń / ścieżka_2 for ścieżka_2 in 명세['objects']] + ['--start-group'] +
         [Zabezpieczenia_pakiet if ścieżka_2 == 'objects/libassh.a' else Project_korzeń / ścieżka_2 for ścieżka_2 in 명세['libraries']] + ['--end-group'])
    Wykonaj_polecenie([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    skrót_Plik = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if argumenty.verify and skrót_Plik != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + skrót_Plik)
    print('RELINK PASS', skrót_Plik, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Uruchom_2()
