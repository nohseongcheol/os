#!/usr/bin/env python3
"""वितरण_मूल्य 묶음에서 libassh/TinyCC를 교체하고 स्वकीय 커널을 पुनःप्रयत्न_मूल्य 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

प्रोजेक्ट_मूळ = Path(__file__).resolve().parent


def आज्ञा_कार्यवाही_करा(शब्द_मजकूर):
    subprocess.check_call([str(प्रविष्टी_मूल्य) for प्रविष्टी_मूल्य in शब्द_मजकूर], cwd=str(प्रोजेक्ट_मूळ))


def सुरू_करा():
    व्याकरणविश्लेषक_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    व्याकरणविश्लेषक_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 पडताळा')
    व्याकरणविश्लेषक_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 सुधारा_मूल्य·컴파일한 libassh.a वापर_मूल्य')
    व्याकरणविश्लेषक_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 पुनःप्रयत्न_मूल्य 컴파일하고 커널에 탑재')
    व्याकरणविश्लेषक_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    बाबी = व्याकरणविश्लेषक_48ee4b1b.parse_args()
    विनिर्देश = json.loads((प्रोजेक्ट_मूळ / 'relink.json').read_text())
    सिस्टम_बांधणी = प्रोजेक्ट_मूळ / 'build'
    नवे_बंडल = सिस्टम_बांधणी / 'relinked'
    नवे_बंडल.mkdir(exist_ok=True)
    संकलक_साधन = os.environ.get('ARM64_CC', 'clang')
    कनेक्टर = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    संग्रह_साधन = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    दूरस्_थ_सेटिंग्ज = json.loads((सिस्टम_बांधणी / 'remote/libassh-build.json').read_text())
    संयोजना = दूरस्_थ_सेटिंग्ज['flags']
    if बाबी.libassh_archive:
        सुरक्षा_बंडल = बाबी.libassh_archive.resolve()
    else:
        गंतव्ये = []
        घोषणाशीर्षे = ['-I', प्रोजेक्ट_मूळ / 'दूरस्_थ_मूल्य', '-I', प्रोजेक्ट_मूळ / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for नाव in दूरस्_थ_सेटिंग्ज['sources']:
            गंतव्यस्थान_मूल्य = नवे_बंडल / (Path(नाव).stem + '.o')
            आज्ञा_कार्यवाही_करा([संकलक_साधन] + संयोजना + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + घोषणाशीर्षे +
                 ['-c', प्रोजेक्ट_मूळ / नाव, '-o', गंतव्यस्थान_मूल्य])
            गंतव्ये.append(गंतव्यस्थान_मूल्य)
        सुरक्षा_बंडल = नवे_बंडल / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(नवे_बंडल)) as तात्पुरते_मूल्य:
            तात्पुरते_बंडल = Path(तात्पुरते_मूल्य) / 'libassh.a'
            आज्ञा_कार्यवाही_करा([संग्रह_साधन, 'rcs', तात्पुरते_बंडल] + गंतव्ये)
            तात्पुरते_बंडल.replace(सुरक्षा_बंडल)
    if बाबी.tinycc:
        if not बाबी.sdk:
            व्याकरणविश्लेषक_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        विकास = बाबी.sdk.resolve()
        अंकगणिती_मूल्य = sorted((विकास / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not अंकगणिती_मूल्य or not (विकास / 'usr/include/stdio.h').is_file():
            व्याकरणविश्लेषक_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        चालू_कॉन्फिगर = [निवड_मूल्य for निवड_मूल्य in संयोजना if निवड_मूल्य != '-mgeneral-regs-only']
        गंतव्यस्थान_मूल्य = नवे_बंडल / 'संकलक_साधन.o'
        आज्ञा_कार्यवाही_करा([संकलक_साधन] + चालू_कॉन्फिगर + ['-ffunction-sections', '-fdata-sections',
             '-I', प्रोजेक्ट_मूळ / 'सी_संकलक', '-I', प्रोजेक्ट_मूळ / 'vendor/tinycc', '-I', प्रोजेक्ट_मूळ / 'प्रयोक्ता',
             '-I', सिस्टम_बांधणी / 'ccompiler', '-isystem', विकास / 'usr/include', '-c', प्रोजेक्ट_मूळ / 'सी_संकलक/संकलक_साधन.c', '-o', गंतव्यस्थान_मूल्य])
        आज्ञा_कार्यवाही_करा([कनेक्टर, '--gc-sections', '-T', प्रोजेक्ट_मूळ / 'प्रयोक्ता/लिंक_लेआउट.ld', '-z', 'max-page-size=4096',
             '-o', सिस्टम_बांधणी / 'user/cc.elf', सिस्टम_बांधणी / 'user/start.o', सिस्टम_बांधणी / 'user/runtime.o', गंतव्यस्थान_मूल्य] +
             [सिस्टम_बांधणी / 'ccompiler' / (नाव + '.o') for नाव in ('सामान्य_भाषा_रनटाइम_समर्थन', 'सुरू_करा', 'आगाऊ_संबंधित_वेळ', 'परतकरा_ब्रिज')] +
             [सिस्टम_बांधणी / 'user' / (नाव + '.o') for नाव in ('jar', 'tinflate', 'crc32', 'adler32')] + [अंकगणिती_मूल्य[-1]])
        शीर्ष_मूल्य = सिस्टम_बांधणी / 'programs.h'
        शीर्ष_मूल्य.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda आहे_समान: आहे_समान.group(1) + str((सिस्टम_बांधणी / 'user/cc.elf').stat().st_size), शीर्ष_मूल्य.read_text()))
        आज्ञा_कार्यवाही_करा([संकलक_साधन] + संयोजना + ['-c', सिस्टम_बांधणी / 'programs.S', '-o', प्रोजेक्ट_मूळ / 'objects/programs.o'])
        आज्ञा_कार्यवाही_करा([संकलक_साधन] + संयोजना + ['-std=c11', '-I', प्रोजेक्ट_मूळ / 'posix-kor/arm64-native/घोषणाशीर्षे', '-I', सिस्टम_बांधणी,
             '-c', प्रोजेक्ट_मूळ / 'मशीन/प्रयोक्ता.c', '-o', प्रोजेक्ट_मूळ / 'objects/user.o'])
    आज्ञा_कार्यवाही_करा([कनेक्टर, '--gc-sections', '-T', प्रोजेक्ट_मूळ / 'प्रणालीप्रारंभ/लिंक_लेआउट.ld', '-o', नवे_बंडल / 'kernel.elf'] +
         [प्रोजेक्ट_मूळ / मार्ग for मार्ग in विनिर्देश['objects']] + ['--start-group'] +
         [सुरक्षा_बंडल if मार्ग == 'objects/libassh.a' else प्रोजेक्ट_मूळ / मार्ग for मार्ग in विनिर्देश['libraries']] + ['--end-group'])
    आज्ञा_कार्यवाही_करा([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', नवे_बंडल / 'kernel.elf', नवे_बंडल / 'kernel8.img'])
    हॅश_संचिका = hashlib.sha256((नवे_बंडल / 'kernel8.img').read_bytes()).hexdigest()
    if बाबी.verify and हॅश_संचिका != विनिर्देश['kernel_sha256']:
        raise SystemExit('पुन्हाजोडा_संचारटोक 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + हॅश_संचिका)
    print('RELINK PASS', हॅश_संचिका, नवे_बंडल / 'kernel8.img')


if __name__ == '__main__':
    सुरू_करा()
