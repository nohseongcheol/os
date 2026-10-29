#!/usr/bin/env python3
"""배포 묶음에서 libassh/TinyCC를 교체하고 lastno 커널을 znova_poskusiti_VALUE 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

pobuda_koren = Path(__file__).resolve().parent


def Izvedi_ukaz(Word_SMS):
    subprocess.check_call([str(vnos_VALUE) for vnos_VALUE in Word_SMS], cwd=str(pobuda_koren))


def Zaženi():
    razčlenjevalnik_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    razčlenjevalnik_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 확인')
    razčlenjevalnik_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a uporaba_VALUE')
    razčlenjevalnik_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 znova_poskusiti_VALUE 컴파일하고 커널에 탑재')
    razčlenjevalnik_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    Argumenti = razčlenjevalnik_48ee4b1b.parse_args()
    명세 = json.loads((pobuda_koren / 'relink.json').read_text())
    graditev_sistem = pobuda_koren / 'build'
    새묶음 = graditev_sistem / 'relinked'
    새묶음.mkdir(exist_ok=True)
    prevajalnik_orodje = os.environ.get('ARM64_CC', 'clang')
    priključek = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Arhiv_orodje = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    oddaljen_Nastavitve = json.loads((graditev_sistem / 'remote/libassh-build.json').read_text())
    Nastavitve = oddaljen_Nastavitve['flags']
    if Argumenti.libassh_archive:
        Varnost_sveženj = Argumenti.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', pobuda_koren / 'oddaljen_VALUE', '-I', pobuda_koren / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Ime in oddaljen_Nastavitve['sources']:
            cilj_VALUE = 새묶음 / (Path(Ime).stem + '.o')
            Izvedi_ukaz([prevajalnik_orodje] + Nastavitve + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', pobuda_koren / Ime, '-o', cilj_VALUE])
            목적들.append(cilj_VALUE)
        Varnost_sveženj = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            Izvedi_ukaz([Arhiv_orodje, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Varnost_sveženj)
    if Argumenti.tinycc:
        if not Argumenti.sdk:
            razčlenjevalnik_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = Argumenti.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            razčlenjevalnik_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [izbor_VALUE for izbor_VALUE in Nastavitve if izbor_VALUE != '-mgeneral-regs-only']
        cilj_VALUE = 새묶음 / 'prevajalnik_orodje.o'
        Izvedi_ukaz([prevajalnik_orodje] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', pobuda_koren / 'C_prevajalnik', '-I', pobuda_koren / 'vendor/tinycc', '-I', pobuda_koren / 'uporabnik',
             '-I', graditev_sistem / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', pobuda_koren / 'C_prevajalnik/prevajalnik_orodje.c', '-o', cilj_VALUE])
        Izvedi_ukaz([priključek, '--gc-sections', '-T', pobuda_koren / 'uporabnik/Povezava_Krmarjenje.ld', '-z', 'max-page-size=4096',
             '-o', graditev_sistem / 'user/cc.elf', graditev_sistem / 'user/start.o', graditev_sistem / 'user/runtime.o', cilj_VALUE] +
             [graditev_sistem / 'ccompiler' / (Ime + '.o') for Ime in ('skupni_jezikovni_izvajalnik_Podpora', 'Zaženi', '미리번역', 'vrni_most')] +
             [graditev_sistem / 'user' / (Ime + '.o') for Ime in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = graditev_sistem / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((graditev_sistem / 'user/cc.elf').stat().st_size), 머리.read_text()))
        Izvedi_ukaz([prevajalnik_orodje] + Nastavitve + ['-c', graditev_sistem / 'programs.S', '-o', pobuda_koren / 'objects/programs.o'])
        Izvedi_ukaz([prevajalnik_orodje] + Nastavitve + ['-std=c11', '-I', pobuda_koren / 'posix-kor/arm64-native/포함', '-I', graditev_sistem,
             '-c', pobuda_koren / 'računalnik/uporabnik.c', '-o', pobuda_koren / 'objects/user.o'])
    Izvedi_ukaz([priključek, '--gc-sections', '-T', pobuda_koren / '부팅/Povezava_Krmarjenje.ld', '-o', 새묶음 / 'kernel.elf'] +
         [pobuda_koren / POT for POT in 명세['objects']] + ['--start-group'] +
         [Varnost_sveženj if POT == 'objects/libassh.a' else pobuda_koren / POT for POT in 명세['libraries']] + ['--end-group'])
    Izvedi_ukaz([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    zgoščena_vrednost_Datoteka = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if Argumenti.verify and zgoščena_vrednost_Datoteka != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + zgoščena_vrednost_Datoteka)
    print('RELINK PASS', zgoščena_vrednost_Datoteka, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Zaženi()
