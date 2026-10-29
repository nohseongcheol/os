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

기준 = Path(__file__).resolve().parent


def ukwenza_umyalelo(Igama_I_SMS):
    subprocess.check_call([str(ufako_nkcukacha_ixabiso) for ufako_nkcukacha_ixabiso in Igama_I_SMS], cwd=str(기준))


def Phumeza():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 ngqinisisa')
    해석기.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    해석기.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    해석기.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = 해석기.parse_args()
    명세 = json.loads((기준 / 'relink.json').read_text())
    yakha_inkqubo = 기준 / 'build'
    새묶음 = yakha_inkqubo / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    isidibanisi = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Uvimba_isixhobo_sokutayipha = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    kude_Iisetingi = json.loads((yakha_inkqubo / 'remote/libassh-build.json').read_text())
    Imimiselo = kude_Iisetingi['flags']
    if 인수.libassh_archive:
        Ukhuseleko_umqulu = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', 기준 / 'kude_ixabiso', '-I', 기준 / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Igama in kude_Iisetingi['sources']:
            indawo_ekuyiwa_kuyo_ixabiso = 새묶음 / (Path(Igama).stem + '.o')
            ukwenza_umyalelo([번역기] + Imimiselo + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', 기준 / Igama, '-o', indawo_ekuyiwa_kuyo_ixabiso])
            목적들.append(indawo_ekuyiwa_kuyo_ixabiso)
        Ukhuseleko_umqulu = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            ukwenza_umyalelo([Uvimba_isixhobo_sokutayipha, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Ukhuseleko_umqulu)
    if 인수.tinycc:
        if not 인수.sdk:
            해석기.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            해석기.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [ukukhetha_ixabiso for ukukhetha_ixabiso in Imimiselo if ukukhetha_ixabiso != '-mgeneral-regs-only']
        indawo_ekuyiwa_kuyo_ixabiso = 새묶음 / '번역기.o'
        ukwenza_umyalelo([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', 기준 / '시언어번역기', '-I', 기준 / 'vendor/tinycc', '-I', 기준 / 'umsebenzisi',
             '-I', yakha_inkqubo / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', 기준 / '시언어번역기/번역기.c', '-o', indawo_ekuyiwa_kuyo_ixabiso])
        ukwenza_umyalelo([isidibanisi, '--gc-sections', '-T', 기준 / 'umsebenzisi/Ilinki_ubume.ld', '-z', 'max-page-size=4096',
             '-o', yakha_inkqubo / 'user/cc.elf', yakha_inkqubo / 'user/start.o', yakha_inkqubo / 'user/runtime.o', indawo_ekuyiwa_kuyo_ixabiso] +
             [yakha_inkqubo / 'ccompiler' / (Igama + '.o') for Igama in ('ixesha_lokusebenza_kolwimi_oluqhelekileyo_inkxaso', 'Phumeza', '미리번역', '되돌림')] +
             [yakha_inkqubo / 'user' / (Igama + '.o') for Igama in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = yakha_inkqubo / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((yakha_inkqubo / 'user/cc.elf').stat().st_size), 머리.read_text()))
        ukwenza_umyalelo([번역기] + Imimiselo + ['-c', yakha_inkqubo / 'programs.S', '-o', 기준 / 'objects/programs.o'])
        ukwenza_umyalelo([번역기] + Imimiselo + ['-std=c11', '-I', 기준 / 'posix-kor/arm64-native/포함', '-I', yakha_inkqubo,
             '-c', 기준 / 'umatshini/umsebenzisi.c', '-o', 기준 / 'objects/user.o'])
    ukwenza_umyalelo([isidibanisi, '--gc-sections', '-T', 기준 / '부팅/Ilinki_ubume.ld', '-o', 새묶음 / 'kernel.elf'] +
         [기준 / INDLELA for INDLELA in 명세['objects']] + ['--start-group'] +
         [Ukhuseleko_umqulu if INDLELA == 'objects/libassh.a' else 기준 / INDLELA for INDLELA in 명세['libraries']] + ['--end-group'])
    ukwenza_umyalelo([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    i_hash_ifayile = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and i_hash_ifayile != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + i_hash_ifayile)
    print('RELINK PASS', i_hash_ifayile, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Phumeza()
