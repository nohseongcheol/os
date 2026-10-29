#!/usr/bin/env python3
"""배포 묶음에서 libassh/TinyCC를 교체하고 निज 커널을 다시 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

प्रोजेक्ट_करें_मूल = Path(__file__).resolve().parent


def निष्पादित_करें_आदेश(शब्द_पाठ):
    subprocess.check_call([str(एन्ट्री_मान) for एन्ट्री_मान in शब्द_पाठ], cwd=str(प्रोजेक्ट_करें_मूल))


def चलाएँ():
    पार्सर_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    पार्सर_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 सत्यापित_करें')
    पार्सर_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    पार्सर_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    पार्सर_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    तर्क = पार्सर_48ee4b1b.parse_args()
    명세 = json.loads((प्रोजेक्ट_करें_मूल / 'relink.json').read_text())
    बिल्ड_सिस्टम = प्रोजेक्ट_करें_मूल / 'build'
    새묶음 = बिल्ड_सिस्टम / 'relinked'
    새묶음.mkdir(exist_ok=True)
    कंपाइलर_उपकरण = os.environ.get('ARM64_CC', 'clang')
    कनेक्टर = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    संग्रह_उपकरण = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    दूरस्थ_सेटिंग = json.loads((बिल्ड_सिस्टम / 'remote/libassh-build.json').read_text())
    विन्यास = दूरस्थ_सेटिंग['flags']
    if तर्क.libassh_archive:
        सुरक्षा_बंडल = तर्क.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', प्रोजेक्ट_करें_मूल / 'दूरस्थ_मान', '-I', प्रोजेक्ट_करें_मूल / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for नाम in दूरस्थ_सेटिंग['sources']:
            गंतव्य_मान = 새묶음 / (Path(नाम).stem + '.o')
            निष्पादित_करें_आदेश([कंपाइलर_उपकरण] + विन्यास + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', प्रोजेक्ट_करें_मूल / नाम, '-o', गंतव्य_मान])
            목적들.append(गंतव्य_मान)
        सुरक्षा_बंडल = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            निष्पादित_करें_आदेश([संग्रह_उपकरण, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(सुरक्षा_बंडल)
    if तर्क.tinycc:
        if not तर्क.sdk:
            पार्सर_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = तर्क.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            पार्सर_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [चयन_मान for चयन_मान in विन्यास if चयन_मान != '-mgeneral-regs-only']
        गंतव्य_मान = 새묶음 / 'कंपाइलर_उपकरण.o'
        निष्पादित_करें_आदेश([कंपाइलर_उपकरण] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', प्रोजेक्ट_करें_मूल / 'सी_कंपाइलर', '-I', प्रोजेक्ट_करें_मूल / 'vendor/tinycc', '-I', प्रोजेक्ट_करें_मूल / 'उपयोगकर्ता',
             '-I', बिल्ड_सिस्टम / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', प्रोजेक्ट_करें_मूल / 'सी_कंपाइलर/कंपाइलर_उपकरण.c', '-o', गंतव्य_मान])
        निष्पादित_करें_आदेश([कनेक्टर, '--gc-sections', '-T', प्रोजेक्ट_करें_मूल / 'उपयोगकर्ता/लिंक_लेआउट.ld', '-z', 'max-page-size=4096',
             '-o', बिल्ड_सिस्टम / 'user/cc.elf', बिल्ड_सिस्टम / 'user/start.o', बिल्ड_सिस्टम / 'user/runtime.o', गंतव्य_मान] +
             [बिल्ड_सिस्टम / 'ccompiler' / (नाम + '.o') for नाम in ('निष्पादनसहायता', 'चलाएँ', '미리번역', 'वापस_करें_ब्रिज')] +
             [बिल्ड_सिस्टम / 'user' / (नाम + '.o') for नाम in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = बिल्ड_सिस्टम / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((बिल्ड_सिस्टम / 'user/cc.elf').stat().st_size), 머리.read_text()))
        निष्पादित_करें_आदेश([कंपाइलर_उपकरण] + विन्यास + ['-c', बिल्ड_सिस्टम / 'programs.S', '-o', प्रोजेक्ट_करें_मूल / 'objects/programs.o'])
        निष्पादित_करें_आदेश([कंपाइलर_उपकरण] + विन्यास + ['-std=c11', '-I', प्रोजेक्ट_करें_मूल / 'posix-kor/arm64-native/포함', '-I', बिल्ड_सिस्टम,
             '-c', प्रोजेक्ट_करें_मूल / 'यंत्र/उपयोगकर्ता.c', '-o', प्रोजेक्ट_करें_मूल / 'objects/user.o'])
    निष्पादित_करें_आदेश([कनेक्टर, '--gc-sections', '-T', प्रोजेक्ट_करें_मूल / '부팅/लिंक_लेआउट.ld', '-o', 새묶음 / 'kernel.elf'] +
         [प्रोजेक्ट_करें_मूल / पथ for पथ in 명세['objects']] + ['--start-group'] +
         [सुरक्षा_बंडल if पथ == 'objects/libassh.a' else प्रोजेक्ट_करें_मूल / पथ for पथ in 명세['libraries']] + ['--end-group'])
    निष्पादित_करें_आदेश([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    हैश_फ़ाइल = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if तर्क.verify and हैश_फ़ाइल != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + हैश_फ़ाइल)
    print('RELINK PASS', हैश_फ़ाइल, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    चलाएँ()
