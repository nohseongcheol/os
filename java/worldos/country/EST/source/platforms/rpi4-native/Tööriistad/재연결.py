#!/usr/bin/env python3
"""turustus_VALUE 묶음에서 libassh/TinyCC를 교체하고 oma 커널을 uuesti_proovima_VALUE 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

Project_juur = Path(__file__).resolve().parent


def Täida_käsk(Word_SMS):
    subprocess.check_call([str(kirje_VALUE) for kirje_VALUE in Word_SMS], cwd=str(Project_juur))


def Käivita_2():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 kinnitama')
    parser_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a kasutus_VALUE')
    parser_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 uuesti_proovima_VALUE 컴파일하고 커널에 탑재')
    parser_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    Argumendid = parser_48ee4b1b.parse_args()
    명세 = json.loads((Project_juur / 'relink.json').read_text())
    järk_süsteem = Project_juur / 'build'
    새묶음 = järk_süsteem / 'relinked'
    새묶음.mkdir(exist_ok=True)
    kompilaator_tööriist = os.environ.get('ARM64_CC', 'clang')
    liitmik = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Arhiiv_tööriist = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    kauge_Sätted = json.loads((järk_süsteem / 'remote/libassh-build.json').read_text())
    Seaded = kauge_Sätted['flags']
    if Argumendid.libassh_archive:
        Turve_kogum = Argumendid.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', Project_juur / 'kauge_VALUE', '-I', Project_juur / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Nimi_2 in kauge_Sätted['sources']:
            sihtkoht_VALUE = 새묶음 / (Path(Nimi_2).stem + '.o')
            Täida_käsk([kompilaator_tööriist] + Seaded + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', Project_juur / Nimi_2, '-o', sihtkoht_VALUE])
            목적들.append(sihtkoht_VALUE)
        Turve_kogum = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            Täida_käsk([Arhiiv_tööriist, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Turve_kogum)
    if Argumendid.tinycc:
        if not Argumendid.sdk:
            parser_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = Argumendid.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            parser_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [valim_VALUE for valim_VALUE in Seaded if valim_VALUE != '-mgeneral-regs-only']
        sihtkoht_VALUE = 새묶음 / 'kompilaator_tööriist.o'
        Täida_käsk([kompilaator_tööriist] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', Project_juur / '_15_kompilaator', '-I', Project_juur / 'vendor/tinycc', '-I', Project_juur / 'kasutaja',
             '-I', järk_süsteem / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', Project_juur / '_15_kompilaator/kompilaator_tööriist.c', '-o', sihtkoht_VALUE])
        Täida_käsk([liitmik, '--gc-sections', '-T', Project_juur / 'kasutaja/Link_küljend.ld', '-z', 'max-page-size=4096',
             '-o', järk_süsteem / 'user/cc.elf', järk_süsteem / 'user/start.o', järk_süsteem / 'user/runtime.o', sihtkoht_VALUE] +
             [järk_süsteem / 'ccompiler' / (Nimi_2 + '.o') for Nimi_2 in ('CLR_tugi', 'Käivita_2', '미리번역', 'tagasi_saatma_sild')] +
             [järk_süsteem / 'user' / (Nimi_2 + '.o') for Nimi_2 in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = järk_süsteem / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((järk_süsteem / 'user/cc.elf').stat().st_size), 머리.read_text()))
        Täida_käsk([kompilaator_tööriist] + Seaded + ['-c', järk_süsteem / 'programs.S', '-o', Project_juur / 'objects/programs.o'])
        Täida_käsk([kompilaator_tööriist] + Seaded + ['-std=c11', '-I', Project_juur / 'posix-kor/arm64-native/포함', '-I', järk_süsteem,
             '-c', Project_juur / 'arvuti/kasutaja.c', '-o', Project_juur / 'objects/user.o'])
    Täida_käsk([liitmik, '--gc-sections', '-T', Project_juur / '부팅/Link_küljend.ld', '-o', 새묶음 / 'kernel.elf'] +
         [Project_juur / RADA for RADA in 명세['objects']] + ['--start-group'] +
         [Turve_kogum if RADA == 'objects/libassh.a' else Project_juur / RADA for RADA in 명세['libraries']] + ['--end-group'])
    Täida_käsk([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    räsikood_Fail = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if Argumendid.verify and räsikood_Fail != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + räsikood_Fail)
    print('RELINK PASS', räsikood_Fail, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Käivita_2()
