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

प्रॉजॅक्ट_रूट = Path(__file__).resolve().parent


def पाळो_दिवचो_आदेश(Word_SMS):
    subprocess.check_call([str(प्रवेश_मोल) for प्रवेश_मोल in Word_SMS], cwd=str(प्रॉजॅक्ट_रूट))


def चलोवप():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 पुनर्तपासणी_करची')
    해석기.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    해석기.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    해석기.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = 해석기.parse_args()
    명세 = json.loads((प्रॉजॅक्ट_रूट / 'relink.json').read_text())
    दाळचे_प्रणाली = प्रॉजॅक्ट_रूट / 'build'
    새묶음 = दाळचे_प्रणाली / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    कनॅक्टर = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    संग्रह_साधन = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    दुर्मीळ_मांडावळी = json.loads((दाळचे_प्रणाली / 'remote/libassh-build.json').read_text())
    मांडावळी = दुर्मीळ_मांडावळी['flags']
    if 인수.libassh_archive:
        सुरक्षा_रास = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', प्रॉजॅक्ट_रूट / 'दुर्मीळ_मोल', '-I', प्रॉजॅक्ट_रूट / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for नांव in दुर्मीळ_मांडावळी['sources']:
            नियुक्त_स्थान_मोल = 새묶음 / (Path(नांव).stem + '.o')
            पाळो_दिवचो_आदेश([번역기] + मांडावळी + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', प्रॉजॅक्ट_रूट / नांव, '-o', नियुक्त_स्थान_मोल])
            목적들.append(नियुक्त_स्थान_मोल)
        सुरक्षा_रास = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            पाळो_दिवचो_आदेश([संग्रह_साधन, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(सुरक्षा_रास)
    if 인수.tinycc:
        if not 인수.sdk:
            해석기.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            해석기.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [निवड_मोल for निवड_मोल in मांडावळी if निवड_मोल != '-mgeneral-regs-only']
        नियुक्त_स्थान_मोल = 새묶음 / '번역기.o'
        पाळो_दिवचो_आदेश([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', प्रॉजॅक्ट_रूट / '시언어번역기', '-I', प्रॉजॅक्ट_रूट / 'vendor/tinycc', '-I', प्रॉजॅक्ट_रूट / 'उपेगकर्तो',
             '-I', दाळचे_प्रणाली / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', प्रॉजॅक्ट_रूट / '시언어번역기/번역기.c', '-o', नियुक्त_स्थान_मोल])
        पाळो_दिवचो_आदेश([कनॅक्टर, '--gc-sections', '-T', प्रॉजॅक्ट_रूट / 'उपेगकर्तो/लिंक_रचणाय.ld', '-z', 'max-page-size=4096',
             '-o', दाळचे_प्रणाली / 'user/cc.elf', दाळचे_प्रणाली / 'user/start.o', दाळचे_प्रणाली / 'user/runtime.o', नियुक्त_स्थान_मोल] +
             [दाळचे_प्रणाली / 'ccompiler' / (नांव + '.o') for नांव in ('सामान्य_भास_रनटायम_तेंको', 'चलोवप', '미리번역', 'return_ब्रिज')] +
             [दाळचे_प्रणाली / 'user' / (नांव + '.o') for नांव in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = दाळचे_प्रणाली / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((दाळचे_प्रणाली / 'user/cc.elf').stat().st_size), 머리.read_text()))
        पाळो_दिवचो_आदेश([번역기] + मांडावळी + ['-c', दाळचे_प्रणाली / 'programs.S', '-o', प्रॉजॅक्ट_रूट / 'objects/programs.o'])
        पाळो_दिवचो_आदेश([번역기] + मांडावळी + ['-std=c11', '-I', प्रॉजॅक्ट_रूट / 'posix-kor/arm64-native/포함', '-I', दाळचे_प्रणाली,
             '-c', प्रॉजॅक्ट_रूट / 'यंत्र/उपेगकर्तो.c', '-o', प्रॉजॅक्ट_रूट / 'objects/user.o'])
    पाळो_दिवचो_आदेश([कनॅक्टर, '--gc-sections', '-T', प्रॉजॅक्ट_रूट / '부팅/लिंक_रचणाय.ld', '-o', 새묶음 / 'kernel.elf'] +
         [प्रॉजॅक्ट_रूट / पाथ for पाथ in 명세['objects']] + ['--start-group'] +
         [सुरक्षा_रास if पाथ == 'objects/libassh.a' else प्रॉजॅक्ट_रूट / पाथ for पाथ in 명세['libraries']] + ['--end-group'])
    पाळो_दिवचो_आदेश([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    हॅश_फायल = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and हॅश_फायल != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + हॅश_फायल)
    print('RELINK PASS', हॅश_फायल, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    चलोवप()
