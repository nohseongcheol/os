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

projicirati_koijen = Path(__file__).resolve().parent


def Izvrši_komanda(Word_SMS):
    subprocess.check_call([str(unos_VALUE) for unos_VALUE in Word_SMS], cwd=str(projicirati_koijen))


def Pokreni():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 potvrditi')
    해석기.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    해석기.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    해석기.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    Argumenti = 해석기.parse_args()
    명세 = json.loads((projicirati_koijen / 'relink.json').read_text())
    verzija_sistem = projicirati_koijen / 'build'
    새묶음 = verzija_sistem / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    konektor = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Arhiva_alatka = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    udaljeno_Postavke = json.loads((verzija_sistem / 'remote/libassh-build.json').read_text())
    Postavke = udaljeno_Postavke['flags']
    if Argumenti.libassh_archive:
        Sigurnost_paket = Argumenti.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', projicirati_koijen / 'udaljeno_VALUE', '-I', projicirati_koijen / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Naziv in udaljeno_Postavke['sources']:
            odredište_VALUE = 새묶음 / (Path(Naziv).stem + '.o')
            Izvrši_komanda([번역기] + Postavke + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', projicirati_koijen / Naziv, '-o', odredište_VALUE])
            목적들.append(odredište_VALUE)
        Sigurnost_paket = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            Izvrši_komanda([Arhiva_alatka, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Sigurnost_paket)
    if Argumenti.tinycc:
        if not Argumenti.sdk:
            해석기.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = Argumenti.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            해석기.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [izbor_VALUE for izbor_VALUE in Postavke if izbor_VALUE != '-mgeneral-regs-only']
        odredište_VALUE = 새묶음 / '번역기.o'
        Izvrši_komanda([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', projicirati_koijen / '시언어번역기', '-I', projicirati_koijen / 'vendor/tinycc', '-I', projicirati_koijen / 'korisnik',
             '-I', verzija_sistem / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', projicirati_koijen / '시언어번역기/번역기.c', '-o', odredište_VALUE])
        Izvrši_komanda([konektor, '--gc-sections', '-T', projicirati_koijen / 'korisnik/Veza_izgled.ld', '-z', 'max-page-size=4096',
             '-o', verzija_sistem / 'user/cc.elf', verzija_sistem / 'user/start.o', verzija_sistem / 'user/runtime.o', odredište_VALUE] +
             [verzija_sistem / 'ccompiler' / (Naziv + '.o') for Naziv in ('zajednička_jezička_biblioteka_Podrška', 'Pokreni', '미리번역', 'vratiti_most')] +
             [verzija_sistem / 'user' / (Naziv + '.o') for Naziv in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = verzija_sistem / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((verzija_sistem / 'user/cc.elf').stat().st_size), 머리.read_text()))
        Izvrši_komanda([번역기] + Postavke + ['-c', verzija_sistem / 'programs.S', '-o', projicirati_koijen / 'objects/programs.o'])
        Izvrši_komanda([번역기] + Postavke + ['-std=c11', '-I', projicirati_koijen / 'posix-kor/arm64-native/포함', '-I', verzija_sistem,
             '-c', projicirati_koijen / 'mašina/korisnik.c', '-o', projicirati_koijen / 'objects/user.o'])
    Izvrši_komanda([konektor, '--gc-sections', '-T', projicirati_koijen / '부팅/Veza_izgled.ld', '-o', 새묶음 / 'kernel.elf'] +
         [projicirati_koijen / Putanja for Putanja in 명세['objects']] + ['--start-group'] +
         [Sigurnost_paket if Putanja == 'objects/libassh.a' else projicirati_koijen / Putanja for Putanja in 명세['libraries']] + ['--end-group'])
    Izvrši_komanda([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    raspršivanje_fajl = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if Argumenti.verify and raspršivanje_fajl != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + raspršivanje_fajl)
    print('RELINK PASS', raspršivanje_fajl, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Pokreni()
