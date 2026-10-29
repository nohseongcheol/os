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

திட்டப்பணி_மூலம் = Path(__file__).resolve().parent


def இயக்கு_கட்டளை(சொல்_உரை):
    subprocess.check_call([str(உள்ளீடு_மதிப்பு) for உள்ளீடு_மதிப்பு in சொல்_உரை], cwd=str(திட்டப்பணி_மூலம்))


def செயல்படுத்துக():
    பார்சர்_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    பார்சர்_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 சரிபார்')
    பார்சர்_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    பார்சர்_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    பார்சர்_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    செயலுருபுகள் = பார்சர்_48ee4b1b.parse_args()
    명세 = json.loads((திட்டப்பணி_மூலம் / 'relink.json').read_text())
    தொகு_முறைமை = திட்டப்பணி_மூலம் / 'build'
    새묶음 = தொகு_முறைமை / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    இணைப்பான் = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    காப்பகம்_கருவி = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    தொலைநிலை_அமைப்புகள் = json.loads((தொகு_முறைமை / 'remote/libassh-build.json').read_text())
    அமைப்புகள் = தொலைநிலை_அமைப்புகள்['flags']
    if செயலுருபுகள்.libassh_archive:
        பாதுகாப்பு_மூட்டை = செயலுருபுகள்.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', திட்டப்பணி_மூலம் / 'தொலைநிலை_மதிப்பு', '-I', திட்டப்பணி_மூலம் / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for பெயர் in தொலைநிலை_அமைப்புகள்['sources']:
            இலக்கு_மதிப்பு = 새묶음 / (Path(பெயர்).stem + '.o')
            இயக்கு_கட்டளை([번역기] + அமைப்புகள் + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', திட்டப்பணி_மூலம் / பெயர், '-o', இலக்கு_மதிப்பு])
            목적들.append(இலக்கு_மதிப்பு)
        பாதுகாப்பு_மூட்டை = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            இயக்கு_கட்டளை([காப்பகம்_கருவி, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(பாதுகாப்பு_மூட்டை)
    if செயலுருபுகள்.tinycc:
        if not செயலுருபுகள்.sdk:
            பார்சர்_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = செயலுருபுகள்.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            பார்சர்_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [தேர்வு_மதிப்பு for தேர்வு_மதிப்பு in அமைப்புகள் if தேர்வு_மதிப்பு != '-mgeneral-regs-only']
        இலக்கு_மதிப்பு = 새묶음 / '번역기.o'
        இயக்கு_கட்டளை([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', திட்டப்பணி_மூலம் / '시언어번역기', '-I', திட்டப்பணி_மூலம் / 'vendor/tinycc', '-I', திட்டப்பணி_மூலம் / 'பயனர்',
             '-I', தொகு_முறைமை / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', திட்டப்பணி_மூலம் / '시언어번역기/번역기.c', '-o', இலக்கு_மதிப்பு])
        இயக்கு_கட்டளை([இணைப்பான், '--gc-sections', '-T', திட்டப்பணி_மூலம் / 'பயனர்/இணை_லேஅவுட்.ld', '-z', 'max-page-size=4096',
             '-o', தொகு_முறைமை / 'user/cc.elf', தொகு_முறைமை / 'user/start.o', தொகு_முறைமை / 'user/runtime.o', இலக்கு_மதிப்பு] +
             [தொகு_முறைமை / 'ccompiler' / (பெயர் + '.o') for பெயர் in ('பொது_மொழி_இயக்க_நேரம்_ஆதரவு', 'செயல்படுத்துக', '미리번역', '되돌림')] +
             [தொகு_முறைமை / 'user' / (பெயர் + '.o') for பெயர் in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = தொகு_முறைமை / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((தொகு_முறைமை / 'user/cc.elf').stat().st_size), 머리.read_text()))
        இயக்கு_கட்டளை([번역기] + அமைப்புகள் + ['-c', தொகு_முறைமை / 'programs.S', '-o', திட்டப்பணி_மூலம் / 'objects/programs.o'])
        இயக்கு_கட்டளை([번역기] + அமைப்புகள் + ['-std=c11', '-I', திட்டப்பணி_மூலம் / 'posix-kor/arm64-native/포함', '-I', தொகு_முறைமை,
             '-c', திட்டப்பணி_மூலம் / 'இயந்திரம்/பயனர்.c', '-o', திட்டப்பணி_மூலம் / 'objects/user.o'])
    இயக்கு_கட்டளை([இணைப்பான், '--gc-sections', '-T', திட்டப்பணி_மூலம் / '부팅/இணை_லேஅவுட்.ld', '-o', 새묶음 / 'kernel.elf'] +
         [திட்டப்பணி_மூலம் / பாதை_2 for பாதை_2 in 명세['objects']] + ['--start-group'] +
         [பாதுகாப்பு_மூட்டை if பாதை_2 == 'objects/libassh.a' else திட்டப்பணி_மூலம் / பாதை_2 for பாதை_2 in 명세['libraries']] + ['--end-group'])
    இயக்கு_கட்டளை([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    ஹாஷ்_கோப்பு = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if செயலுருபுகள்.verify and ஹாஷ்_கோப்பு != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + ஹாஷ்_கோப்பு)
    print('RELINK PASS', ஹாஷ்_கோப்பு, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    செயல்படுத்துக()
