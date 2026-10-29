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

አሳይ_ስር = Path(__file__).resolve().parent


def ፈጽም_ትእዛዝ(ቃል_ጽሁፍ):
    subprocess.check_call([str(ምዝግብ_እሴት) for ምዝግብ_እሴት in ቃል_ጽሁፍ], cwd=str(አሳይ_ስር))


def ማስኬጃ():
    አግልሎ_ማስቀመጥ_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    አግልሎ_ማስቀመጥ_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 አረጋግጥ')
    አግልሎ_ማስቀመጥ_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    አግልሎ_ማስቀመጥ_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    አግልሎ_ማስቀመጥ_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = አግልሎ_ማስቀመጥ_48ee4b1b.parse_args()
    명세 = json.loads((አሳይ_ስር / 'relink.json').read_text())
    ግንብ_ስርዓት = አሳይ_ስር / 'build'
    새묶음 = ግንብ_ስርዓት / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    አገናኝ = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    ከዝን_መሳሪያ = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    የሩቅ_ቅንብሮች = json.loads((ግንብ_ስርዓት / 'remote/libassh-build.json').read_text())
    ማሰናጃዎች = የሩቅ_ቅንብሮች['flags']
    if 인수.libassh_archive:
        መድህን_ቀርቅብ = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', አሳይ_ስር / 'የሩቅ_እሴት', '-I', አሳይ_ስር / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for ስም in የሩቅ_ቅንብሮች['sources']:
            መድረሻ_እሴት = 새묶음 / (Path(ስም).stem + '.o')
            ፈጽም_ትእዛዝ([번역기] + ማሰናጃዎች + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', አሳይ_ስር / ስም, '-o', መድረሻ_እሴት])
            목적들.append(መድረሻ_እሴት)
        መድህን_ቀርቅብ = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            ፈጽም_ትእዛዝ([ከዝን_መሳሪያ, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(መድህን_ቀርቅብ)
    if 인수.tinycc:
        if not 인수.sdk:
            አግልሎ_ማስቀመጥ_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            አግልሎ_ማስቀመጥ_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [የተመረጠ_እሴት for የተመረጠ_እሴት in ማሰናጃዎች if የተመረጠ_እሴት != '-mgeneral-regs-only']
        መድረሻ_እሴት = 새묶음 / '번역기.o'
        ፈጽም_ትእዛዝ([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', አሳይ_ስር / '시언어번역기', '-I', አሳይ_ስር / 'vendor/tinycc', '-I', አሳይ_ስር / 'ተጠቃሚ',
             '-I', ግንብ_ስርዓት / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', አሳይ_ስር / '시언어번역기/번역기.c', '-o', መድረሻ_እሴት])
        ፈጽም_ትእዛዝ([አገናኝ, '--gc-sections', '-T', አሳይ_ስር / 'ተጠቃሚ/አገናኝ_አሰሳ.ld', '-z', 'max-page-size=4096',
             '-o', ግንብ_ስርዓት / 'user/cc.elf', ግንብ_ስርዓት / 'user/start.o', ግንብ_ስርዓት / 'user/runtime.o', መድረሻ_እሴት] +
             [ግንብ_ስርዓት / 'ccompiler' / (ስም + '.o') for ስም in ('የጋራ_ቋንቋ_ማስኬጃ_ጊዜ_ድገፍ', 'ማስኬጃ', '미리번역', '되돌림')] +
             [ግንብ_ስርዓት / 'user' / (ስም + '.o') for ስም in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = ግንብ_ስርዓት / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((ግንብ_ስርዓት / 'user/cc.elf').stat().st_size), 머리.read_text()))
        ፈጽም_ትእዛዝ([번역기] + ማሰናጃዎች + ['-c', ግንብ_ስርዓት / 'programs.S', '-o', አሳይ_ስር / 'objects/programs.o'])
        ፈጽም_ትእዛዝ([번역기] + ማሰናጃዎች + ['-std=c11', '-I', አሳይ_ስር / 'posix-kor/arm64-native/포함', '-I', ግንብ_ስርዓት,
             '-c', አሳይ_ስር / 'ማሽን/ተጠቃሚ.c', '-o', አሳይ_ስር / 'objects/user.o'])
    ፈጽም_ትእዛዝ([አገናኝ, '--gc-sections', '-T', አሳይ_ስር / '부팅/አገናኝ_አሰሳ.ld', '-o', 새묶음 / 'kernel.elf'] +
         [አሳይ_ስር / መተላለፊያ for መተላለፊያ in 명세['objects']] + ['--start-group'] +
         [መድህን_ቀርቅብ if መተላለፊያ == 'objects/libassh.a' else አሳይ_ስር / መተላለፊያ for መተላለፊያ in 명세['libraries']] + ['--end-group'])
    ፈጽም_ትእዛዝ([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    ሃሽ_ፋይል = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and ሃሽ_ፋይል != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + ሃሽ_ፋይል)
    print('RELINK PASS', ሃሽ_ፋይል, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    ማስኬጃ()
