#!/usr/bin/env python3
"""jakelu_ARVO 묶음에서 libassh/TinyCC를 교체하고 oma 커널을 yrittää_uudelleen_ARVO 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

aloite_juuri = Path(__file__).resolve().parent


def Suorita_komento(Word_SMS):
    subprocess.check_call([str(merkintä_ARVO_962f286b) for merkintä_ARVO_962f286b in Word_SMS], cwd=str(aloite_juuri))


def Suorita_2():
    jäsennin_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    jäsennin_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 tarkistaa')
    jäsennin_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a käyttö_ARVO')
    jäsennin_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 yrittää_uudelleen_ARVO 컴파일하고 커널에 탑재')
    jäsennin_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    argumentit = jäsennin_48ee4b1b.parse_args()
    määritys = json.loads((aloite_juuri / 'relink.json').read_text())
    kääntää_Järjestelmä = aloite_juuri / 'build'
    새묶음 = kääntää_Järjestelmä / 'relinked'
    새묶음.mkdir(exist_ok=True)
    kääntäjä_työkalu = os.environ.get('ARM64_CC', 'clang')
    liitin = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Arkisto_työkalu = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    etä_Asetukset = json.loads((kääntää_Järjestelmä / 'remote/libassh-build.json').read_text())
    Asetukset = etä_Asetukset['flags']
    if argumentit.libassh_archive:
        suojaus_nippu = argumentit.libassh_archive.resolve()
    else:
        목적들 = []
        esittelyt = ['-I', aloite_juuri / 'etä_ARVO', '-I', aloite_juuri / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Nimi in etä_Asetukset['sources']:
            kohde_ARVO = 새묶음 / (Path(Nimi).stem + '.o')
            Suorita_komento([kääntäjä_työkalu] + Asetukset + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + esittelyt +
                 ['-c', aloite_juuri / Nimi, '-o', kohde_ARVO])
            목적들.append(kohde_ARVO)
        suojaus_nippu = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            Suorita_komento([Arkisto_työkalu, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(suojaus_nippu)
    if argumentit.tinycc:
        if not argumentit.sdk:
            jäsennin_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        kehitystuote = argumentit.sdk.resolve()
        산술 = sorted((kehitystuote / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (kehitystuote / 'usr/include/stdio.h').is_file():
            jäsennin_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [valinta_ARVO for valinta_ARVO in Asetukset if valinta_ARVO != '-mgeneral-regs-only']
        kohde_ARVO = 새묶음 / 'kääntäjä_työkalu.o'
        Suorita_komento([kääntäjä_työkalu] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', aloite_juuri / 'C_kääntäjä', '-I', aloite_juuri / 'vendor/tinycc', '-I', aloite_juuri / 'käyttäjätila',
             '-I', kääntää_Järjestelmä / 'ccompiler', '-isystem', kehitystuote / 'usr/include', '-c', aloite_juuri / 'C_kääntäjä/kääntäjä_työkalu.c', '-o', kohde_ARVO])
        Suorita_komento([liitin, '--gc-sections', '-T', aloite_juuri / 'käyttäjätila/linkitysasettelu.ld', '-z', 'max-page-size=4096',
             '-o', kääntää_Järjestelmä / 'user/cc.elf', kääntää_Järjestelmä / 'user/start.o', kääntää_Järjestelmä / 'user/runtime.o', kohde_ARVO] +
             [kääntää_Järjestelmä / 'ccompiler' / (Nimi + '.o') for Nimi in ('CLR_Tuki', 'Suorita_2', '미리번역', 'palauttaa_silta')] +
             [kääntää_Järjestelmä / 'user' / (Nimi + '.o') for Nimi in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = kääntää_Järjestelmä / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((kääntää_Järjestelmä / 'user/cc.elf').stat().st_size), 머리.read_text()))
        Suorita_komento([kääntäjä_työkalu] + Asetukset + ['-c', kääntää_Järjestelmä / 'programs.S', '-o', aloite_juuri / 'objects/programs.o'])
        Suorita_komento([kääntäjä_työkalu] + Asetukset + ['-std=c11', '-I', aloite_juuri / 'posix-kor/arm64-native/esittelyt', '-I', kääntää_Järjestelmä,
             '-c', aloite_juuri / 'kone/käyttäjätila.c', '-o', aloite_juuri / 'objects/user.o'])
    Suorita_komento([liitin, '--gc-sections', '-T', aloite_juuri / 'koneen_käynnistys/linkitysasettelu.ld', '-o', 새묶음 / 'kernel.elf'] +
         [aloite_juuri / polku_2 for polku_2 in määritys['objects']] + ['--start-group'] +
         [suojaus_nippu if polku_2 == 'objects/libassh.a' else aloite_juuri / polku_2 for polku_2 in määritys['libraries']] + ['--end-group'])
    Suorita_komento([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    hajautusarvo_Tiedosto = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if argumentit.verify and hajautusarvo_Tiedosto != määritys['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + hajautusarvo_Tiedosto)
    print('RELINK PASS', hajautusarvo_Tiedosto, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Suorita_2()
