#!/usr/bin/env python3
"""배포 묶음에서 libassh/TinyCC를 교체하고 vlastné 커널을 skúsiť_znova_VALUE 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

akcia_koreň = Path(__file__).resolve().parent


def Vykonať_príkaz(Word_SMS):
    subprocess.check_call([str(položka_VALUE) for položka_VALUE in Word_SMS], cwd=str(akcia_koreň))


def Spustiť_2():
    analyzátor_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analyzátor_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 overiť')
    analyzátor_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a používať_VALUE')
    analyzátor_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 skúsiť_znova_VALUE 컴파일하고 커널에 탑재')
    analyzátor_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    Argumenty = analyzátor_48ee4b1b.parse_args()
    명세 = json.loads((akcia_koreň / 'relink.json').read_text())
    zostava_systém = akcia_koreň / 'build'
    새묶음 = zostava_systém / 'relinked'
    새묶음.mkdir(exist_ok=True)
    kompilátor_nástroj = os.environ.get('ARM64_CC', 'clang')
    Spojnica = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Archív_nástroj = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    vzdialený_Nastavenia = json.loads((zostava_systém / 'remote/libassh-build.json').read_text())
    Nastavenia = vzdialený_Nastavenia['flags']
    if Argumenty.libassh_archive:
        Zabezpečenie_zväzok = Argumenty.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', akcia_koreň / 'vzdialený_VALUE', '-I', akcia_koreň / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Názov in vzdialený_Nastavenia['sources']:
            cieľ_VALUE = 새묶음 / (Path(Názov).stem + '.o')
            Vykonať_príkaz([kompilátor_nástroj] + Nastavenia + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', akcia_koreň / Názov, '-o', cieľ_VALUE])
            목적들.append(cieľ_VALUE)
        Zabezpečenie_zväzok = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            Vykonať_príkaz([Archív_nástroj, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Zabezpečenie_zväzok)
    if Argumenty.tinycc:
        if not Argumenty.sdk:
            analyzátor_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = Argumenty.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            analyzátor_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [výber_VALUE for výber_VALUE in Nastavenia if výber_VALUE != '-mgeneral-regs-only']
        cieľ_VALUE = 새묶음 / 'kompilátor_nástroj.o'
        Vykonať_príkaz([kompilátor_nástroj] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', akcia_koreň / 'C_kompilátor', '-I', akcia_koreň / 'vendor/tinycc', '-I', akcia_koreň / 'používateľ',
             '-I', zostava_systém / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', akcia_koreň / 'C_kompilátor/kompilátor_nástroj.c', '-o', cieľ_VALUE])
        Vykonať_príkaz([Spojnica, '--gc-sections', '-T', akcia_koreň / 'používateľ/odkaz_Navigácia.ld', '-z', 'max-page-size=4096',
             '-o', zostava_systém / 'user/cc.elf', zostava_systém / 'user/start.o', zostava_systém / 'user/runtime.o', cieľ_VALUE] +
             [zostava_systém / 'ccompiler' / (Názov + '.o') for Názov in ('CLR_Podpora', 'Spustiť_2', '미리번역', 'vrátiť_most')] +
             [zostava_systém / 'user' / (Názov + '.o') for Názov in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = zostava_systém / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((zostava_systém / 'user/cc.elf').stat().st_size), 머리.read_text()))
        Vykonať_príkaz([kompilátor_nástroj] + Nastavenia + ['-c', zostava_systém / 'programs.S', '-o', akcia_koreň / 'objects/programs.o'])
        Vykonať_príkaz([kompilátor_nástroj] + Nastavenia + ['-std=c11', '-I', akcia_koreň / 'posix-kor/arm64-native/포함', '-I', zostava_systém,
             '-c', akcia_koreň / 'počítač_5eb260fa/používateľ.c', '-o', akcia_koreň / 'objects/user.o'])
    Vykonať_príkaz([Spojnica, '--gc-sections', '-T', akcia_koreň / '부팅/odkaz_Navigácia.ld', '-o', 새묶음 / 'kernel.elf'] +
         [akcia_koreň / Cesta for Cesta in 명세['objects']] + ['--start-group'] +
         [Zabezpečenie_zväzok if Cesta == 'objects/libassh.a' else akcia_koreň / Cesta for Cesta in 명세['libraries']] + ['--end-group'])
    Vykonať_príkaz([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    hodnota_hash_Súbor = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if Argumenty.verify and hodnota_hash_Súbor != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + hodnota_hash_Súbor)
    print('RELINK PASS', hodnota_hash_Súbor, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Spustiť_2()
