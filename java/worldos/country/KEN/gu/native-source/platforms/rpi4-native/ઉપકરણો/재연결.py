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

પ્રોજેક્ટ_રૂટ = Path(__file__).resolve().parent


def અમલ_કરો_આદેશ(શબ્દ_પાઠ):
    subprocess.check_call([str(પ્રવેશ_મૂલ્ય) for પ્રવેશ_મૂલ્ય in શબ્દ_પાઠ], cwd=str(પ્રોજેક્ટ_રૂટ))


def ચલાવો_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 ચકાસવું')
    해석기.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    해석기.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    해석기.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    દલીલો = 해석기.parse_args()
    명세 = json.loads((પ્રોજેક્ટ_રૂટ / 'relink.json').read_text())
    બિલ્ડ_સિસ્ટમ = પ્રોજેક્ટ_રૂટ / 'build'
    새묶음 = બિલ્ડ_સિસ્ટમ / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    કનેક્ટર = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    સંગ્રહ_ઉપકરણ = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    રિમોટ_સેટિંગ્સ = json.loads((બિલ્ડ_સિસ્ટમ / 'remote/libassh-build.json').read_text())
    સુયોજના = રિમોટ_સેટિંગ્સ['flags']
    if દલીલો.libassh_archive:
        સુરક્ષા_બન્ડલ = દલીલો.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', પ્રોજેક્ટ_રૂટ / 'રિમોટ_મૂલ્ય', '-I', પ્રોજેક્ટ_રૂટ / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for નામ in રિમોટ_સેટિંગ્સ['sources']:
            ગંતવ્ય_મૂલ્ય = 새묶음 / (Path(નામ).stem + '.o')
            અમલ_કરો_આદેશ([번역기] + સુયોજના + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', પ્રોજેક્ટ_રૂટ / નામ, '-o', ગંતવ્ય_મૂલ્ય])
            목적들.append(ગંતવ્ય_મૂલ્ય)
        સુરક્ષા_બન્ડલ = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            અમલ_કરો_આદેશ([સંગ્રહ_ઉપકરણ, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(સુરક્ષા_બન્ડલ)
    if દલીલો.tinycc:
        if not દલીલો.sdk:
            해석기.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = દલીલો.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            해석기.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [ચયન_મૂલ્ય for ચયન_મૂલ્ય in સુયોજના if ચયન_મૂલ્ય != '-mgeneral-regs-only']
        ગંતવ્ય_મૂલ્ય = 새묶음 / '번역기.o'
        અમલ_કરો_આદેશ([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', પ્રોજેક્ટ_રૂટ / '시언어번역기', '-I', પ્રોજેક્ટ_રૂટ / 'vendor/tinycc', '-I', પ્રોજેક્ટ_રૂટ / 'ઉપયોગકર્તા',
             '-I', બિલ્ડ_સિસ્ટમ / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', પ્રોજેક્ટ_રૂટ / '시언어번역기/번역기.c', '-o', ગંતવ્ય_મૂલ્ય])
        અમલ_કરો_આદેશ([કનેક્ટર, '--gc-sections', '-T', પ્રોજેક્ટ_રૂટ / 'ઉપયોગકર્તા/લિંક_લેઆઉટ.ld', '-z', 'max-page-size=4096',
             '-o', બિલ્ડ_સિસ્ટમ / 'user/cc.elf', બિલ્ડ_સિસ્ટમ / 'user/start.o', બિલ્ડ_સિસ્ટમ / 'user/runtime.o', ગંતવ્ય_મૂલ્ય] +
             [બિલ્ડ_સિસ્ટમ / 'ccompiler' / (નામ + '.o') for નામ in ('સામાન્ય_ભાષા_રનટાઇમ_સપોર્ટ', 'ચલાવો_2', '미리번역', '되돌림')] +
             [બિલ્ડ_સિસ્ટમ / 'user' / (નામ + '.o') for નામ in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = બિલ્ડ_સિસ્ટમ / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((બિલ્ડ_સિસ્ટમ / 'user/cc.elf').stat().st_size), 머리.read_text()))
        અમલ_કરો_આદેશ([번역기] + સુયોજના + ['-c', બિલ્ડ_સિસ્ટમ / 'programs.S', '-o', પ્રોજેક્ટ_રૂટ / 'objects/programs.o'])
        અમલ_કરો_આદેશ([번역기] + સુયોજના + ['-std=c11', '-I', પ્રોજેક્ટ_રૂટ / 'posix-kor/arm64-native/포함', '-I', બિલ્ડ_સિસ્ટમ,
             '-c', પ્રોજેક્ટ_રૂટ / 'મશીન/ઉપયોગકર્તા.c', '-o', પ્રોજેક્ટ_રૂટ / 'objects/user.o'])
    અમલ_કરો_આદેશ([કનેક્ટર, '--gc-sections', '-T', પ્રોજેક્ટ_રૂટ / '부팅/લિંક_લેઆઉટ.ld', '-o', 새묶음 / 'kernel.elf'] +
         [પ્રોજેક્ટ_રૂટ / પથ for પથ in 명세['objects']] + ['--start-group'] +
         [સુરક્ષા_બન્ડલ if પથ == 'objects/libassh.a' else પ્રોજેક્ટ_રૂટ / પથ for પથ in 명세['libraries']] + ['--end-group'])
    અમલ_કરો_આદેશ([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    હૅશ_ફાઇલ = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if દલીલો.verify and હૅશ_ફાઇલ != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + હૅશ_ફાઇલ)
    print('RELINK PASS', હૅશ_ફાઇલ, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    ચલાવો_2()
