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


def tekeleza_amri(Neno_SMS):
    subprocess.check_call([str(ingizo_thamani) for ingizo_thamani in Neno_SMS], cwd=str(기준))


def endesha():
    kichanganuzi_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    kichanganuzi_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 thibitisha')
    kichanganuzi_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    kichanganuzi_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    kichanganuzi_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = kichanganuzi_48ee4b1b.parse_args()
    명세 = json.loads((기준 / 'relink.json').read_text())
    jenga_mfumo = 기준 / 'build'
    새묶음 = jenga_mfumo / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    kiunganisho = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Hifadhi_zana = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    kwa_mbali_Mipangilio = json.loads((jenga_mfumo / 'remote/libassh-build.json').read_text())
    Mipangilio = kwa_mbali_Mipangilio['flags']
    if 인수.libassh_archive:
        Usalama_fungasha = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', 기준 / 'kwa_mbali_thamani', '-I', 기준 / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Jina in kwa_mbali_Mipangilio['sources']:
            fikio_thamani = 새묶음 / (Path(Jina).stem + '.o')
            tekeleza_amri([번역기] + Mipangilio + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', 기준 / Jina, '-o', fikio_thamani])
            목적들.append(fikio_thamani)
        Usalama_fungasha = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            tekeleza_amri([Hifadhi_zana, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Usalama_fungasha)
    if 인수.tinycc:
        if not 인수.sdk:
            kichanganuzi_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            kichanganuzi_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [uteuzi_thamani for uteuzi_thamani in Mipangilio if uteuzi_thamani != '-mgeneral-regs-only']
        fikio_thamani = 새묶음 / '번역기.o'
        tekeleza_amri([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', 기준 / '시언어번역기', '-I', 기준 / 'vendor/tinycc', '-I', 기준 / 'mtumiaji',
             '-I', jenga_mfumo / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', 기준 / '시언어번역기/번역기.c', '-o', fikio_thamani])
        tekeleza_amri([kiunganisho, '--gc-sections', '-T', 기준 / 'mtumiaji/Kiungo_Muundo.ld', '-z', 'max-page-size=4096',
             '-o', jenga_mfumo / 'user/cc.elf', jenga_mfumo / 'user/start.o', jenga_mfumo / 'user/runtime.o', fikio_thamani] +
             [jenga_mfumo / 'ccompiler' / (Jina + '.o') for Jina in ('muda_wa_kuendesha_lugha_ya_kawaida_Auni', 'endesha', '미리번역', '되돌림')] +
             [jenga_mfumo / 'user' / (Jina + '.o') for Jina in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = jenga_mfumo / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((jenga_mfumo / 'user/cc.elf').stat().st_size), 머리.read_text()))
        tekeleza_amri([번역기] + Mipangilio + ['-c', jenga_mfumo / 'programs.S', '-o', 기준 / 'objects/programs.o'])
        tekeleza_amri([번역기] + Mipangilio + ['-std=c11', '-I', 기준 / 'posix-kor/arm64-native/포함', '-I', jenga_mfumo,
             '-c', 기준 / 'mashine/mtumiaji.c', '-o', 기준 / 'objects/user.o'])
    tekeleza_amri([kiunganisho, '--gc-sections', '-T', 기준 / '부팅/Kiungo_Muundo.ld', '-o', 새묶음 / 'kernel.elf'] +
         [기준 / njia for njia in 명세['objects']] + ['--start-group'] +
         [Usalama_fungasha if njia == 'objects/libassh.a' else 기준 / njia for njia in 명세['libraries']] + ['--end-group'])
    tekeleza_amri([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    kali_faili = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and kali_faili != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + kali_faili)
    print('RELINK PASS', kali_faili, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    endesha()
