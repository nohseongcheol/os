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

परियोजना_रूट = Path(__file__).resolve().parent


def कार्यान्वयन_गर्नुहोस्_आदेश(शब्द_पाठ):
    subprocess.check_call([str(प्रविष्टि_मान) for प्रविष्टि_मान in शब्द_पाठ], cwd=str(परियोजना_रूट))


def चलाउनुहोस्():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 रुजू_गर्नुहोस्')
    해석기.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    해석기.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    해석기.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    तर्क = 해석기.parse_args()
    명세 = json.loads((परियोजना_रूट / 'relink.json').read_text())
    बनाउनुहोस्_प्रणाली = परियोजना_रूट / 'build'
    새묶음 = बनाउनुहोस्_प्रणाली / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    योजक = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    सङ्ग्रह_उपकरण = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    दूर_सेटिङहरू = json.loads((बनाउनुहोस्_प्रणाली / 'remote/libassh-build.json').read_text())
    सेटिङ = दूर_सेटिङहरू['flags']
    if तर्क.libassh_archive:
        सुरक्षा_पोको = तर्क.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', परियोजना_रूट / 'दूर_मान', '-I', परियोजना_रूट / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for नाम in दूर_सेटिङहरू['sources']:
            गन्तव्य_मान = 새묶음 / (Path(नाम).stem + '.o')
            कार्यान्वयन_गर्नुहोस्_आदेश([번역기] + सेटिङ + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', परियोजना_रूट / नाम, '-o', गन्तव्य_मान])
            목적들.append(गन्तव्य_मान)
        सुरक्षा_पोको = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            कार्यान्वयन_गर्नुहोस्_आदेश([सङ्ग्रह_उपकरण, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(सुरक्षा_पोको)
    if तर्क.tinycc:
        if not तर्क.sdk:
            해석기.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = तर्क.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            해석기.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [चयन_मान for चयन_मान in सेटिङ if चयन_मान != '-mgeneral-regs-only']
        गन्तव्य_मान = 새묶음 / '번역기.o'
        कार्यान्वयन_गर्नुहोस्_आदेश([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', परियोजना_रूट / '시언어번역기', '-I', परियोजना_रूट / 'vendor/tinycc', '-I', परियोजना_रूट / 'प्रयोगकर्ता',
             '-I', बनाउनुहोस्_प्रणाली / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', परियोजना_रूट / '시언어번역기/번역기.c', '-o', गन्तव्य_मान])
        कार्यान्वयन_गर्नुहोस्_आदेश([योजक, '--gc-sections', '-T', परियोजना_रूट / 'प्रयोगकर्ता/लिङ्क_लेआउट.ld', '-z', 'max-page-size=4096',
             '-o', बनाउनुहोस्_प्रणाली / 'user/cc.elf', बनाउनुहोस्_प्रणाली / 'user/start.o', बनाउनुहोस्_प्रणाली / 'user/runtime.o', गन्तव्य_मान] +
             [बनाउनुहोस्_प्रणाली / 'ccompiler' / (नाम + '.o') for नाम in ('सामान्य_भाषा_चालु_समय_समर्थन', 'चलाउनुहोस्', '미리번역', '되돌림')] +
             [बनाउनुहोस्_प्रणाली / 'user' / (नाम + '.o') for नाम in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = बनाउनुहोस्_प्रणाली / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((बनाउनुहोस्_प्रणाली / 'user/cc.elf').stat().st_size), 머리.read_text()))
        कार्यान्वयन_गर्नुहोस्_आदेश([번역기] + सेटिङ + ['-c', बनाउनुहोस्_प्रणाली / 'programs.S', '-o', परियोजना_रूट / 'objects/programs.o'])
        कार्यान्वयन_गर्नुहोस्_आदेश([번역기] + सेटिङ + ['-std=c11', '-I', परियोजना_रूट / 'posix-kor/arm64-native/포함', '-I', बनाउनुहोस्_प्रणाली,
             '-c', परियोजना_रूट / 'मेशिन/प्रयोगकर्ता.c', '-o', परियोजना_रूट / 'objects/user.o'])
    कार्यान्वयन_गर्नुहोस्_आदेश([योजक, '--gc-sections', '-T', परियोजना_रूट / '부팅/लिङ्क_लेआउट.ld', '-o', 새묶음 / 'kernel.elf'] +
         [परियोजना_रूट / मार्ग for मार्ग in 명세['objects']] + ['--start-group'] +
         [सुरक्षा_पोको if मार्ग == 'objects/libassh.a' else परियोजना_रूट / मार्ग for मार्ग in 명세['libraries']] + ['--end-group'])
    कार्यान्वयन_गर्नुहोस्_आदेश([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    ह्यास_फाइल = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if तर्क.verify and ह्यास_फाइल != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + ह्यास_फाइल)
    print('RELINK PASS', ह्यास_फाइल, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    चलाउनुहोस्()
