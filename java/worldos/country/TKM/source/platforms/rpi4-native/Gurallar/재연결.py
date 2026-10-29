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


def ýerine_ýetir_buýruk(Söz_SMS):
    subprocess.check_call([str(girizmeklik_baha) for girizmeklik_baha in Söz_SMS], cwd=str(기준))


def Bitir():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 barla')
    해석기.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    해석기.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    해석기.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = 해석기.parse_args()
    명세 = json.loads((기준 / 'relink.json').read_text())
    düz_ulgam = 기준 / 'build'
    새묶음 = düz_ulgam / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    birikdiriji = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Arhiw_gural = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    uzakdan_Sazlamalar = json.loads((düz_ulgam / 'remote/libassh-build.json').read_text())
    Düzümler = uzakdan_Sazlamalar['flags']
    if 인수.libassh_archive:
        Gorag_toplum = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', 기준 / 'uzakdan_baha', '-I', 기준 / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Ad in uzakdan_Sazlamalar['sources']:
            barylmaly_ýer_baha = 새묶음 / (Path(Ad).stem + '.o')
            ýerine_ýetir_buýruk([번역기] + Düzümler + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', 기준 / Ad, '-o', barylmaly_ýer_baha])
            목적들.append(barylmaly_ýer_baha)
        Gorag_toplum = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            ýerine_ýetir_buýruk([Arhiw_gural, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Gorag_toplum)
    if 인수.tinycc:
        if not 인수.sdk:
            해석기.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            해석기.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [saýlama_baha for saýlama_baha in Düzümler if saýlama_baha != '-mgeneral-regs-only']
        barylmaly_ýer_baha = 새묶음 / '번역기.o'
        ýerine_ýetir_buýruk([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', 기준 / '시언어번역기', '-I', 기준 / 'vendor/tinycc', '-I', 기준 / 'ulanyjy',
             '-I', düz_ulgam / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', 기준 / '시언어번역기/번역기.c', '-o', barylmaly_ýer_baha])
        ýerine_ýetir_buýruk([birikdiriji, '--gc-sections', '-T', 기준 / 'ulanyjy/Bag_Ýerleşiş.ld', '-z', 'max-page-size=4096',
             '-o', düz_ulgam / 'user/cc.elf', düz_ulgam / 'user/start.o', düz_ulgam / 'user/runtime.o', barylmaly_ýer_baha] +
             [düz_ulgam / 'ccompiler' / (Ad + '.o') for Ad in ('umumy_dil_işlediş_gurşawy_Goldaw', 'Bitir', '미리번역', '되돌림')] +
             [düz_ulgam / 'user' / (Ad + '.o') for Ad in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = düz_ulgam / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((düz_ulgam / 'user/cc.elf').stat().st_size), 머리.read_text()))
        ýerine_ýetir_buýruk([번역기] + Düzümler + ['-c', düz_ulgam / 'programs.S', '-o', 기준 / 'objects/programs.o'])
        ýerine_ýetir_buýruk([번역기] + Düzümler + ['-std=c11', '-I', 기준 / 'posix-kor/arm64-native/포함', '-I', düz_ulgam,
             '-c', 기준 / 'kompýuter/ulanyjy.c', '-o', 기준 / 'objects/user.o'])
    ýerine_ýetir_buýruk([birikdiriji, '--gc-sections', '-T', 기준 / '부팅/Bag_Ýerleşiş.ld', '-o', 새묶음 / 'kernel.elf'] +
         [기준 / Ýol for Ýol in 명세['objects']] + ['--start-group'] +
         [Gorag_toplum if Ýol == 'objects/libassh.a' else 기준 / Ýol for Ýol in 명세['libraries']] + ['--end-group'])
    ýerine_ýetir_buýruk([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    heş_kody_faýl = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and heş_kody_faýl != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + heş_kody_faýl)
    print('RELINK PASS', heş_kody_faýl, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Bitir()
