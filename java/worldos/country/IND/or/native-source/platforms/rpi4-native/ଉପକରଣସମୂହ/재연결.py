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

ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ = Path(__file__).resolve().parent


def ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(말):
    subprocess.check_call([str(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ) for ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ in 말], cwd=str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍))


def ଚଳାନ୍ତୁ():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 ଯାଞ୍ଚ୍_କରିବା')
    해석기.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    해석기.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    해석기.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = 해석기.parse_args()
    명세 = json.loads((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'relink.json').read_text())
    ବିଲ୍ଡ୍_ସିଷ୍ଟମ = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build'
    새묶음 = ବିଲ୍ଡ୍_ସିଷ୍ଟମ / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    ସଂଲଗ୍ନକ = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    ଅଭିଲେଖାଗାର_ଉପକରଣ = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    ଦୂରବର୍ତ୍ତୀ_ସେଟିଂସ୍ = json.loads((ବିଲ୍ଡ୍_ସିଷ୍ଟମ / 'remote/libassh-build.json').read_text())
    ବିନ୍ଯାସ = ଦୂରବର୍ତ୍ତୀ_ସେଟିଂସ୍['flags']
    if 인수.libassh_archive:
        ନିରାପତ୍ତା_ବଣ୍ଡଲ୍ = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ', '-I', ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for ନାମ in ଦୂରବର୍ତ୍ତୀ_ସେଟିଂସ୍['sources']:
            ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ = 새묶음 / (Path(ନାମ).stem + '.o')
            ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ([번역기] + ବିନ୍ଯାସ + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / ନାମ, '-o', ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ])
            목적들.append(ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ)
        ନିରାପତ୍ତା_ବଣ୍ଡଲ୍ = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ([ଅଭିଲେଖାଗାର_ଉପକରଣ, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(ନିରାପତ୍ତା_ବଣ୍ଡଲ୍)
    if 인수.tinycc:
        if not 인수.sdk:
            해석기.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            해석기.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [ଚୟନ_ମୂଲ୍ୟ for ଚୟନ_ମୂଲ୍ୟ in ବିନ୍ଯାସ if ଚୟନ_ମୂଲ୍ୟ != '-mgeneral-regs-only']
        ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ = 새묶음 / '번역기.o'
        ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / '시언어번역기', '-I', ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'vendor/tinycc', '-I', ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'ଉପଭୋକ୍ତା',
             '-I', ବିଲ୍ଡ୍_ସିଷ୍ଟମ / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / '시언어번역기/번역기.c', '-o', ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ])
        ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ([ସଂଲଗ୍ନକ, '--gc-sections', '-T', ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'ଉପଭୋକ୍ତା/ଲିଙ୍କ୍_ଲେଆଉଟ୍.ld', '-z', 'max-page-size=4096',
             '-o', ବିଲ୍ଡ୍_ସିଷ୍ଟମ / 'user/cc.elf', ବିଲ୍ଡ୍_ସିଷ୍ଟମ / 'user/start.o', ବିଲ୍ଡ୍_ସିଷ୍ଟମ / 'user/runtime.o', ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ] +
             [ବିଲ୍ଡ୍_ସିଷ୍ଟମ / 'ccompiler' / (ନାମ + '.o') for ନାମ in ('ସାଧାରଣ_ଭାଷା_ରନ୍_ଟାଇମ୍_ସମର୍ଥନ', 'ଚଳାନ୍ତୁ', '미리번역', '되돌림')] +
             [ବିଲ୍ଡ୍_ସିଷ୍ଟମ / 'user' / (ନାମ + '.o') for ନାମ in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = ବିଲ୍ଡ୍_ସିଷ୍ଟମ / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((ବିଲ୍ଡ୍_ସିଷ୍ଟମ / 'user/cc.elf').stat().st_size), 머리.read_text()))
        ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ([번역기] + ବିନ୍ଯାସ + ['-c', ବିଲ୍ଡ୍_ସିଷ୍ଟମ / 'programs.S', '-o', ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'objects/programs.o'])
        ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ([번역기] + ବିନ୍ଯାସ + ['-std=c11', '-I', ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'posix-kor/arm64-native/포함', '-I', ବିଲ୍ଡ୍_ସିଷ୍ଟମ,
             '-c', ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'ମେସିନ୍/ଉପଭୋକ୍ତା.c', '-o', ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'objects/user.o'])
    ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ([ସଂଲଗ୍ନକ, '--gc-sections', '-T', ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / '부팅/ଲିଙ୍କ୍_ଲେଆଉଟ୍.ld', '-o', 새묶음 / 'kernel.elf'] +
         [ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / ପଥ for ପଥ in 명세['objects']] + ['--start-group'] +
         [ନିରାପତ୍ତା_ବଣ୍ଡଲ୍ if ପଥ == 'objects/libassh.a' else ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / ପଥ for ପଥ in 명세['libraries']] + ['--end-group'])
    ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    ହାସ୍_ଫାଇଲ୍ = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and ହାସ୍_ଫାଇଲ୍ != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + ହାସ୍_ଫାଇଲ୍)
    print('RELINK PASS', ହାସ୍_ଫାଇଲ୍, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    ଚଳାନ୍ତୁ()
