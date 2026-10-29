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


def yenza_umyalo(Amagama_I_SMS):
    subprocess.check_call([str(okufakwayo_inani) for okufakwayo_inani in Amagama_I_SMS], cwd=str(기준))


def Sebenzisa():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 qiniseka')
    해석기.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    해석기.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    해석기.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = 해석기.parse_args()
    명세 = json.loads((기준 / 'relink.json').read_text())
    akha_isistimu = 기준 / 'build'
    새묶음 = akha_isistimu / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    isixhumanisi = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    londoloza_ithuluzi = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    kude_Amasethingi = json.loads((akha_isistimu / 'remote/libassh-build.json').read_text())
    Izinhlelo = kude_Amasethingi['flags']
    if 인수.libassh_archive:
        ukuphepha_isigaxa = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', 기준 / 'kude_inani', '-I', 기준 / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Igama in kude_Amasethingi['sources']:
            isikhumulo_inani = 새묶음 / (Path(Igama).stem + '.o')
            yenza_umyalo([번역기] + Izinhlelo + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', 기준 / Igama, '-o', isikhumulo_inani])
            목적들.append(isikhumulo_inani)
        ukuphepha_isigaxa = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            yenza_umyalo([londoloza_ithuluzi, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(ukuphepha_isigaxa)
    if 인수.tinycc:
        if not 인수.sdk:
            해석기.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            해석기.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [okukhethiwe_inani for okukhethiwe_inani in Izinhlelo if okukhethiwe_inani != '-mgeneral-regs-only']
        isikhumulo_inani = 새묶음 / '번역기.o'
        yenza_umyalo([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', 기준 / '시언어번역기', '-I', 기준 / 'vendor/tinycc', '-I', 기준 / 'umsebenzisi',
             '-I', akha_isistimu / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', 기준 / '시언어번역기/번역기.c', '-o', isikhumulo_inani])
        yenza_umyalo([isixhumanisi, '--gc-sections', '-T', 기준 / 'umsebenzisi/xhuma_I_layout.ld', '-z', 'max-page-size=4096',
             '-o', akha_isistimu / 'user/cc.elf', akha_isistimu / 'user/start.o', akha_isistimu / 'user/runtime.o', isikhumulo_inani] +
             [akha_isistimu / 'ccompiler' / (Igama + '.o') for Igama in ('isikhathi_sokusebenza_solimi_esivamile_uxhaso', 'Sebenzisa', '미리번역', '되돌림')] +
             [akha_isistimu / 'user' / (Igama + '.o') for Igama in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = akha_isistimu / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((akha_isistimu / 'user/cc.elf').stat().st_size), 머리.read_text()))
        yenza_umyalo([번역기] + Izinhlelo + ['-c', akha_isistimu / 'programs.S', '-o', 기준 / 'objects/programs.o'])
        yenza_umyalo([번역기] + Izinhlelo + ['-std=c11', '-I', 기준 / 'posix-kor/arm64-native/포함', '-I', akha_isistimu,
             '-c', 기준 / 'umshini/umsebenzisi.c', '-o', 기준 / 'objects/user.o'])
    yenza_umyalo([isixhumanisi, '--gc-sections', '-T', 기준 / '부팅/xhuma_I_layout.ld', '-o', 새묶음 / 'kernel.elf'] +
         [기준 / Indlela_2 for Indlela_2 in 명세['objects']] + ['--start-group'] +
         [ukuphepha_isigaxa if Indlela_2 == 'objects/libassh.a' else 기준 / Indlela_2 for Indlela_2 in 명세['libraries']] + ['--end-group'])
    yenza_umyalo([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    i_hash_ifayela = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and i_hash_ifayela != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + i_hash_ifayela)
    print('RELINK PASS', i_hash_ifayela, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Sebenzisa()
