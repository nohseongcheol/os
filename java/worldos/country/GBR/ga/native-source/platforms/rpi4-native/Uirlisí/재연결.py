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

teilgean_fréamh = Path(__file__).resolve().parent


def Rith_ordú(Word_SMS):
    subprocess.check_call([str(iontráil_VALUE) for iontráil_VALUE in Word_SMS], cwd=str(teilgean_fréamh))


def Rith_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 fíoraigh')
    해석기.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    해석기.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    해석기.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    Argóintí = 해석기.parse_args()
    명세 = json.loads((teilgean_fréamh / 'relink.json').read_text())
    tóg_córas = teilgean_fréamh / 'build'
    새묶음 = tóg_córas / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    nascóir = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Cartlann_uirlis = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    cianda_Socruithe = json.loads((tóg_córas / 'remote/libassh-build.json').read_text())
    Socruithe = cianda_Socruithe['flags']
    if Argóintí.libassh_archive:
        Slándáil_beart = Argóintí.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', teilgean_fréamh / 'cianda_VALUE', '-I', teilgean_fréamh / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Ainm in cianda_Socruithe['sources']:
            sprioc_VALUE = 새묶음 / (Path(Ainm).stem + '.o')
            Rith_ordú([번역기] + Socruithe + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', teilgean_fréamh / Ainm, '-o', sprioc_VALUE])
            목적들.append(sprioc_VALUE)
        Slándáil_beart = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            Rith_ordú([Cartlann_uirlis, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Slándáil_beart)
    if Argóintí.tinycc:
        if not Argóintí.sdk:
            해석기.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = Argóintí.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            해석기.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [roghnú_VALUE for roghnú_VALUE in Socruithe if roghnú_VALUE != '-mgeneral-regs-only']
        sprioc_VALUE = 새묶음 / '번역기.o'
        Rith_ordú([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', teilgean_fréamh / '시언어번역기', '-I', teilgean_fréamh / 'vendor/tinycc', '-I', teilgean_fréamh / 'úsáideoir',
             '-I', tóg_córas / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', teilgean_fréamh / '시언어번역기/번역기.c', '-o', sprioc_VALUE])
        Rith_ordú([nascóir, '--gc-sections', '-T', teilgean_fréamh / 'úsáideoir/Nasc_dáileadh.ld', '-z', 'max-page-size=4096',
             '-o', tóg_córas / 'user/cc.elf', tóg_córas / 'user/start.o', tóg_córas / 'user/runtime.o', sprioc_VALUE] +
             [tóg_córas / 'ccompiler' / (Ainm + '.o') for Ainm in ('am_rite_teanga_coiteann_Tacaíocht', 'Rith_2', '미리번역', 'return_traschóiritheoir')] +
             [tóg_córas / 'user' / (Ainm + '.o') for Ainm in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = tóg_córas / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((tóg_córas / 'user/cc.elf').stat().st_size), 머리.read_text()))
        Rith_ordú([번역기] + Socruithe + ['-c', tóg_córas / 'programs.S', '-o', teilgean_fréamh / 'objects/programs.o'])
        Rith_ordú([번역기] + Socruithe + ['-std=c11', '-I', teilgean_fréamh / 'posix-kor/arm64-native/포함', '-I', tóg_córas,
             '-c', teilgean_fréamh / 'meaisín/úsáideoir.c', '-o', teilgean_fréamh / 'objects/user.o'])
    Rith_ordú([nascóir, '--gc-sections', '-T', teilgean_fréamh / '부팅/Nasc_dáileadh.ld', '-o', 새묶음 / 'kernel.elf'] +
         [teilgean_fréamh / CONAIR for CONAIR in 명세['objects']] + ['--start-group'] +
         [Slándáil_beart if CONAIR == 'objects/libassh.a' else teilgean_fréamh / CONAIR for CONAIR in 명세['libraries']] + ['--end-group'])
    Rith_ordú([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    hais_comhad = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if Argóintí.verify and hais_comhad != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + hais_comhad)
    print('RELINK PASS', hais_comhad, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Rith_2()
