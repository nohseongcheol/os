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

Project_erro = Path(__file__).resolve().parent


def exekutatu_komando(Word_SMS):
    subprocess.check_call([str(sarrera_balio) for sarrera_balio in Word_SMS], cwd=str(Project_erro))


def Exekutatu_2():
    analizatzaile_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizatzaile_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 egiaztatu')
    analizatzaile_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    analizatzaile_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    analizatzaile_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    Argumentuak = analizatzaile_48ee4b1b.parse_args()
    명세 = json.loads((Project_erro / 'relink.json').read_text())
    eraiki_sistema = Project_erro / 'build'
    새묶음 = eraiki_sistema / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    konektore = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    artxibo_tresna = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    urruneko_Ezarpenak = json.loads((eraiki_sistema / 'remote/libassh-build.json').read_text())
    Ezarpenak = urruneko_Ezarpenak['flags']
    if Argumentuak.libassh_archive:
        segurtasun_multzo = Argumentuak.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', Project_erro / 'urruneko_balio', '-I', Project_erro / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Izena in urruneko_Ezarpenak['sources']:
            helburu_balio_a0fbc067 = 새묶음 / (Path(Izena).stem + '.o')
            exekutatu_komando([번역기] + Ezarpenak + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', Project_erro / Izena, '-o', helburu_balio_a0fbc067])
            목적들.append(helburu_balio_a0fbc067)
        segurtasun_multzo = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            exekutatu_komando([artxibo_tresna, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(segurtasun_multzo)
    if Argumentuak.tinycc:
        if not Argumentuak.sdk:
            analizatzaile_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = Argumentuak.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            analizatzaile_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [hautapen_balio for hautapen_balio in Ezarpenak if hautapen_balio != '-mgeneral-regs-only']
        helburu_balio_a0fbc067 = 새묶음 / '번역기.o'
        exekutatu_komando([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', Project_erro / '시언어번역기', '-I', Project_erro / 'vendor/tinycc', '-I', Project_erro / 'erabiltzaile',
             '-I', eraiki_sistema / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', Project_erro / '시언어번역기/번역기.c', '-o', helburu_balio_a0fbc067])
        exekutatu_komando([konektore, '--gc-sections', '-T', Project_erro / 'erabiltzaile/lotu_diseinu.ld', '-z', 'max-page-size=4096',
             '-o', eraiki_sistema / 'user/cc.elf', eraiki_sistema / 'user/start.o', eraiki_sistema / 'user/runtime.o', helburu_balio_a0fbc067] +
             [eraiki_sistema / 'ccompiler' / (Izena + '.o') for Izena in ('실행지원', 'Exekutatu_2', '미리번역', 'itzuli_zubi')] +
             [eraiki_sistema / 'user' / (Izena + '.o') for Izena in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = eraiki_sistema / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((eraiki_sistema / 'user/cc.elf').stat().st_size), 머리.read_text()))
        exekutatu_komando([번역기] + Ezarpenak + ['-c', eraiki_sistema / 'programs.S', '-o', Project_erro / 'objects/programs.o'])
        exekutatu_komando([번역기] + Ezarpenak + ['-std=c11', '-I', Project_erro / 'posix-kor/arm64-native/포함', '-I', eraiki_sistema,
             '-c', Project_erro / 'gailu/erabiltzaile.c', '-o', Project_erro / 'objects/user.o'])
    exekutatu_komando([konektore, '--gc-sections', '-T', Project_erro / '부팅/lotu_diseinu.ld', '-o', 새묶음 / 'kernel.elf'] +
         [Project_erro / Bide_izena for Bide_izena in 명세['objects']] + ['--start-group'] +
         [segurtasun_multzo if Bide_izena == 'objects/libassh.a' else Project_erro / Bide_izena for Bide_izena in 명세['libraries']] + ['--end-group'])
    exekutatu_komando([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    hash_fitxategi = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if Argumentuak.verify and hash_fitxategi != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + hash_fitxategi)
    print('RELINK PASS', hash_fitxategi, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Exekutatu_2()
