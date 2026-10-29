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


def gudanar_Umarni(Microsoft_Word_SMS):
    subprocess.check_call([str(Mashigar_bayanai_Daraja) for Mashigar_bayanai_Daraja in Microsoft_Word_SMS], cwd=str(기준))


def Tafiyar_da():
    tatsar_manhaja_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    tatsar_manhaja_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 Tabbatar_da')
    tatsar_manhaja_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    tatsar_manhaja_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    tatsar_manhaja_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = tatsar_manhaja_48ee4b1b.parse_args()
    명세 = json.loads((기준 / 'relink.json').read_text())
    Gina_na_ura = 기준 / 'build'
    새묶음 = Gina_na_ura / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    na_urar_haɗawa = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Rumbun_ajiya_kayan_aiki = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    na_nesa_Saituna = json.loads((Gina_na_ura / 'remote/libassh-build.json').read_text())
    Saituna = na_nesa_Saituna['flags']
    if 인수.libassh_archive:
        Tsaro_dami = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', 기준 / 'na_nesa_Daraja', '-I', 기준 / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Suna in na_nesa_Saituna['sources']:
            Zangon_ƙarshe_Daraja = 새묶음 / (Path(Suna).stem + '.o')
            gudanar_Umarni([번역기] + Saituna + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', 기준 / Suna, '-o', Zangon_ƙarshe_Daraja])
            목적들.append(Zangon_ƙarshe_Daraja)
        Tsaro_dami = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            gudanar_Umarni([Rumbun_ajiya_kayan_aiki, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Tsaro_dami)
    if 인수.tinycc:
        if not 인수.sdk:
            tatsar_manhaja_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            tatsar_manhaja_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [bangaren_zaɓi_Daraja for bangaren_zaɓi_Daraja in Saituna if bangaren_zaɓi_Daraja != '-mgeneral-regs-only']
        Zangon_ƙarshe_Daraja = 새묶음 / '번역기.o'
        gudanar_Umarni([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', 기준 / '시언어번역기', '-I', 기준 / 'vendor/tinycc', '-I', 기준 / 'Mai_anfani_da_kwamfuta',
             '-I', Gina_na_ura / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', 기준 / '시언어번역기/번역기.c', '-o', Zangon_ƙarshe_Daraja])
        gudanar_Umarni([na_urar_haɗawa, '--gc-sections', '-T', 기준 / 'Mai_anfani_da_kwamfuta/Kafa_Zagaye.ld', '-z', 'max-page-size=4096',
             '-o', Gina_na_ura / 'user/cc.elf', Gina_na_ura / 'user/start.o', Gina_na_ura / 'user/runtime.o', Zangon_ƙarshe_Daraja] +
             [Gina_na_ura / 'ccompiler' / (Suna + '.o') for Suna in ('lokacin_bude_yaren_gama_gari_taimako', 'Tafiyar_da', '미리번역', '되돌림')] +
             [Gina_na_ura / 'user' / (Suna + '.o') for Suna in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = Gina_na_ura / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((Gina_na_ura / 'user/cc.elf').stat().st_size), 머리.read_text()))
        gudanar_Umarni([번역기] + Saituna + ['-c', Gina_na_ura / 'programs.S', '-o', 기준 / 'objects/programs.o'])
        gudanar_Umarni([번역기] + Saituna + ['-std=c11', '-I', 기준 / 'posix-kor/arm64-native/포함', '-I', Gina_na_ura,
             '-c', 기준 / 'na_ura_mai_kwakwalwa/Mai_anfani_da_kwamfuta.c', '-o', 기준 / 'objects/user.o'])
    gudanar_Umarni([na_urar_haɗawa, '--gc-sections', '-T', 기준 / '부팅/Kafa_Zagaye.ld', '-o', 새묶음 / 'kernel.elf'] +
         [기준 / Hanyar_shiga for Hanyar_shiga in 명세['objects']] + ['--start-group'] +
         [Tsaro_dami if Hanyar_shiga == 'objects/libassh.a' else 기준 / Hanyar_shiga for Hanyar_shiga in 명세['libraries']] + ['--end-group'])
    gudanar_Umarni([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    hash_Fayil = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and hash_Fayil != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + hash_Fayil)
    print('RELINK PASS', hash_Fayil, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Tafiyar_da()
