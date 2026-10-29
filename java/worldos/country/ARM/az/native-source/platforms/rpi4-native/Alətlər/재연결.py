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

Project_kök = Path(__file__).resolve().parent


def icra_etmək_əmr(Söz_SMS):
    subprocess.check_call([str(daxiletmə_VALUE) for daxiletmə_VALUE in Söz_SMS], cwd=str(Project_kök))


def İcra_Et():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 yoxlamaq')
    parser_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    parser_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    parser_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = parser_48ee4b1b.parse_args()
    명세 = json.loads((Project_kök / 'relink.json').read_text())
    qurmaq_sistem = Project_kök / 'build'
    새묶음 = qurmaq_sistem / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    Birləşdirici = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Arxiv_alət = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    uzaq_Parametrlər = json.loads((qurmaq_sistem / 'remote/libassh-build.json').read_text())
    Sazlama = uzaq_Parametrlər['flags']
    if 인수.libassh_archive:
        Təhlükəsizlik_paket = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', Project_kök / 'uzaq_VALUE', '-I', Project_kök / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Ad in uzaq_Parametrlər['sources']:
            təyinat_VALUE_a0fbc067 = 새묶음 / (Path(Ad).stem + '.o')
            icra_etmək_əmr([번역기] + Sazlama + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', Project_kök / Ad, '-o', təyinat_VALUE_a0fbc067])
            목적들.append(təyinat_VALUE_a0fbc067)
        Təhlükəsizlik_paket = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            icra_etmək_əmr([Arxiv_alət, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Təhlükəsizlik_paket)
    if 인수.tinycc:
        if not 인수.sdk:
            parser_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            parser_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [seçilmiş_sahə_VALUE for seçilmiş_sahə_VALUE in Sazlama if seçilmiş_sahə_VALUE != '-mgeneral-regs-only']
        təyinat_VALUE_a0fbc067 = 새묶음 / '번역기.o'
        icra_etmək_əmr([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', Project_kök / '시언어번역기', '-I', Project_kök / 'vendor/tinycc', '-I', Project_kök / 'istifadəçi',
             '-I', qurmaq_sistem / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', Project_kök / '시언어번역기/번역기.c', '-o', təyinat_VALUE_a0fbc067])
        icra_etmək_əmr([Birləşdirici, '--gc-sections', '-T', Project_kök / 'istifadəçi/keçid_Düzüm.ld', '-z', 'max-page-size=4096',
             '-o', qurmaq_sistem / 'user/cc.elf', qurmaq_sistem / 'user/start.o', qurmaq_sistem / 'user/runtime.o', təyinat_VALUE_a0fbc067] +
             [qurmaq_sistem / 'ccompiler' / (Ad + '.o') for Ad in ('ümumi_dil_icrası_Dəstək', 'İcra_Et', '미리번역', 'geri_qaytarmaq_körpü')] +
             [qurmaq_sistem / 'user' / (Ad + '.o') for Ad in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = qurmaq_sistem / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((qurmaq_sistem / 'user/cc.elf').stat().st_size), 머리.read_text()))
        icra_etmək_əmr([번역기] + Sazlama + ['-c', qurmaq_sistem / 'programs.S', '-o', Project_kök / 'objects/programs.o'])
        icra_etmək_əmr([번역기] + Sazlama + ['-std=c11', '-I', Project_kök / 'posix-kor/arm64-native/포함', '-I', qurmaq_sistem,
             '-c', Project_kök / 'maşın/istifadəçi.c', '-o', Project_kök / 'objects/user.o'])
    icra_etmək_əmr([Birləşdirici, '--gc-sections', '-T', Project_kök / '부팅/keçid_Düzüm.ld', '-o', 새묶음 / 'kernel.elf'] +
         [Project_kök / Cığır for Cığır in 명세['objects']] + ['--start-group'] +
         [Təhlükəsizlik_paket if Cığır == 'objects/libassh.a' else Project_kök / Cığır for Cığır in 명세['libraries']] + ['--end-group'])
    icra_etmək_əmr([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    heş_fayl = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and heş_fayl != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + heş_fayl)
    print('RELINK PASS', heş_fayl, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    İcra_Et()
