#!/usr/bin/env python3
"""distribuce_HODNOTA 묶음에서 libassh/TinyCC를 교체하고 vlastní 커널을 zkusit_znovu_HODNOTA 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

akce_kořen = Path(__file__).resolve().parent


def Provést_příkaz(Word_SMS):
    subprocess.check_call([str(položka_HODNOTA) for položka_HODNOTA in Word_SMS], cwd=str(akce_kořen))


def Spustit_2():
    analyzátor_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analyzátor_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 ověřit')
    analyzátor_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a použít_HODNOTA')
    analyzátor_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 zkusit_znovu_HODNOTA 컴파일하고 커널에 탑재')
    analyzátor_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    argumenty = analyzátor_48ee4b1b.parse_args()
    명세 = json.loads((akce_kořen / 'relink.json').read_text())
    BLD_Systém = akce_kořen / 'build'
    새묶음 = BLD_Systém / 'relinked'
    새묶음.mkdir(exist_ok=True)
    kompilátor_nástroj = os.environ.get('ARM64_CC', 'clang')
    Spojnice = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Archiv_nástroj = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    vzdálený_Nastavení = json.loads((BLD_Systém / 'remote/libassh-build.json').read_text())
    Nastavení = vzdálený_Nastavení['flags']
    if argumenty.libassh_archive:
        Zabezpečení_sada = argumenty.libassh_archive.resolve()
    else:
        목적들 = []
        deklarace = ['-I', akce_kořen / 'vzdálený_HODNOTA', '-I', akce_kořen / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Název in vzdálený_Nastavení['sources']:
            cíl_HODNOTA = 새묶음 / (Path(Název).stem + '.o')
            Provést_příkaz([kompilátor_nástroj] + Nastavení + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + deklarace +
                 ['-c', akce_kořen / Název, '-o', cíl_HODNOTA])
            목적들.append(cíl_HODNOTA)
        Zabezpečení_sada = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            Provést_příkaz([Archiv_nástroj, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Zabezpečení_sada)
    if argumenty.tinycc:
        if not argumenty.sdk:
            analyzátor_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = argumenty.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            analyzátor_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [výběr_HODNOTA for výběr_HODNOTA in Nastavení if výběr_HODNOTA != '-mgeneral-regs-only']
        cíl_HODNOTA = 새묶음 / 'kompilátor_nástroj.o'
        Provést_příkaz([kompilátor_nástroj] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', akce_kořen / 'C_kompilátor', '-I', akce_kořen / 'vendor/tinycc', '-I', akce_kořen / 'uživatelský_prostor',
             '-I', BLD_Systém / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', akce_kořen / 'C_kompilátor/kompilátor_nástroj.c', '-o', cíl_HODNOTA])
        Provést_příkaz([Spojnice, '--gc-sections', '-T', akce_kořen / 'uživatelský_prostor/rozvržení_spojování.ld', '-z', 'max-page-size=4096',
             '-o', BLD_Systém / 'user/cc.elf', BLD_Systém / 'user/start.o', BLD_Systém / 'user/runtime.o', cíl_HODNOTA] +
             [BLD_Systém / 'ccompiler' / (Název + '.o') for Název in ('CLR_vzpěra', 'Spustit_2', '미리번역', 'Vratka_most')] +
             [BLD_Systém / 'user' / (Název + '.o') for Název in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = BLD_Systém / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((BLD_Systém / 'user/cc.elf').stat().st_size), 머리.read_text()))
        Provést_příkaz([kompilátor_nástroj] + Nastavení + ['-c', BLD_Systém / 'programs.S', '-o', akce_kořen / 'objects/programs.o'])
        Provést_příkaz([kompilátor_nástroj] + Nastavení + ['-std=c11', '-I', akce_kořen / 'posix-kor/arm64-native/deklarace', '-I', BLD_Systém,
             '-c', akce_kořen / 'počítač/uživatelský_prostor.c', '-o', akce_kořen / 'objects/user.o'])
    Provést_příkaz([Spojnice, '--gc-sections', '-T', akce_kořen / 'spuštění_stroje/rozvržení_spojování.ld', '-o', 새묶음 / 'kernel.elf'] +
         [akce_kořen / cesta_2 for cesta_2 in 명세['objects']] + ['--start-group'] +
         [Zabezpečení_sada if cesta_2 == 'objects/libassh.a' else akce_kořen / cesta_2 for cesta_2 in 명세['libraries']] + ['--end-group'])
    Provést_příkaz([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    hodnota_hash_Soubor = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if argumenty.verify and hodnota_hash_Soubor != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + hodnota_hash_Soubor)
    print('RELINK PASS', hodnota_hash_Soubor, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Spustit_2()
