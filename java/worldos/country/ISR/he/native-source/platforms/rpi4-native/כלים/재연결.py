#!/usr/bin/env python3
"""הפצה_ערך 묶음에서 libassh/TinyCC를 교체하고 עצמי 커널을 נסה_שנית_ערך 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

לשקף_בסיס = Path(__file__).resolve().parent


def לבצע_פקודה(מילים_טקסט):
    subprocess.check_call([str(ערך_ערך) for ערך_ערך in מילים_טקסט], cwd=str(לשקף_בסיס))


def הפעלה():
    מנתח_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    מנתח_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 ודא_אמת')
    מנתח_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a שימוש_ערך')
    מנתח_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 נסה_שנית_ערך 컴파일하고 커널에 탑재')
    מנתח_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    ארגומנטים = מנתח_48ee4b1b.parse_args()
    מפרט = json.loads((לשקף_בסיס / 'relink.json').read_text())
    בנייה = לשקף_בסיס / 'build'
    새묶음 = בנייה / 'relinked'
    새묶음.mkdir(exist_ok=True)
    מהדר_כלי = os.environ.get('ARM64_CC', 'clang')
    מחבר = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    ארכיון_כלי = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    מרוחק_הגדרות = json.loads((בנייה / 'remote/libassh-build.json').read_text())
    הגדרות = מרוחק_הגדרות['flags']
    if ארגומנטים.libassh_archive:
        אבטחה_חבילה = ארגומנטים.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', לשקף_בסיס / 'מרוחק_ערך', '-I', לשקף_בסיס / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for שם in מרוחק_הגדרות['sources']:
            יעד_ערך = 새묶음 / (Path(שם).stem + '.o')
            לבצע_פקודה([מהדר_כלי] + הגדרות + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', לשקף_בסיס / שם, '-o', יעד_ערך])
            목적들.append(יעד_ערך)
        אבטחה_חבילה = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            לבצע_פקודה([ארכיון_כלי, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(אבטחה_חבילה)
    if ארגומנטים.tinycc:
        if not ארגומנטים.sdk:
            מנתח_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = ארגומנטים.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            מנתח_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [קטע_נבחר_ערך for קטע_נבחר_ערך in הגדרות if קטע_נבחר_ערך != '-mgeneral-regs-only']
        יעד_ערך = 새묶음 / 'מהדר_כלי.o'
        לבצע_פקודה([מהדר_כלי] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', לשקף_בסיס / 'מ_מהדר', '-I', לשקף_בסיס / 'vendor/tinycc', '-I', לשקף_בסיס / 'משתמש',
             '-I', בנייה / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', לשקף_בסיס / 'מ_מהדר/מהדר_כלי.c', '-o', יעד_ערך])
        לבצע_פקודה([מחבר, '--gc-sections', '-T', לשקף_בסיס / 'משתמש/לקשר_ניווט.ld', '-z', 'max-page-size=4096',
             '-o', בנייה / 'user/cc.elf', בנייה / 'user/start.o', בנייה / 'user/runtime.o', יעד_ערך] +
             [בנייה / 'ccompiler' / (שם + '.o') for שם in ('זמן_ריצה_תמך', 'הפעלה', '미리번역', 'החזר_גשר')] +
             [בנייה / 'user' / (שם + '.o') for שם in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        ראש_ערך = בנייה / 'programs.h'
        ראש_ערך.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((בנייה / 'user/cc.elf').stat().st_size), ראש_ערך.read_text()))
        לבצע_פקודה([מהדר_כלי] + הגדרות + ['-c', בנייה / 'programs.S', '-o', לשקף_בסיס / 'objects/programs.o'])
        לבצע_פקודה([מהדר_כלי] + הגדרות + ['-std=c11', '-I', לשקף_בסיס / 'posix-kor/arm64-native/포함', '-I', בנייה,
             '-c', לשקף_בסיס / 'מחשב/משתמש.c', '-o', לשקף_בסיס / 'objects/user.o'])
    לבצע_פקודה([מחבר, '--gc-sections', '-T', לשקף_בסיס / '부팅/לקשר_ניווט.ld', '-o', 새묶음 / 'kernel.elf'] +
         [לשקף_בסיס / נתיב for נתיב in מפרט['objects']] + ['--start-group'] +
         [אבטחה_חבילה if נתיב == 'objects/libassh.a' else לשקף_בסיס / נתיב for נתיב in מפרט['libraries']] + ['--end-group'])
    לבצע_פקודה([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    קוד_Hash_קובץ = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if ארגומנטים.verify and קוד_Hash_קובץ != מפרט['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + קוד_Hash_קובץ)
    print('RELINK PASS', קוד_Hash_קובץ, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    הפעלה()
