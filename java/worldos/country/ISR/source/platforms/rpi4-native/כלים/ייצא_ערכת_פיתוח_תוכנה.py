#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from לבצע_פקודה import לשקף_בסיס


def הפעלה():
    הפצה_נתיב = לשקף_בסיס / 'dist'
    הפצה_נתיב.mkdir(exist_ok=True)
    포직스경로 = לשקף_בסיס.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(לשקף_בסיס / 'build')) as 작업경로:
        ערכת_פיתוח = Path(작업경로) / 'jkoros-native-sdk'
        קובץ_רשימה = {
            לשקף_בסיס.parents[1] / 'LICENSE': 'LICENSE',
            לשקף_בסיס.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            לשקף_בסיס / 'כלים/ערכת_פיתוח_תוכנה_בנה.py': 'compile.py',
            לשקף_בסיס / 'משתמש/호출.h': 'include/호출.h',
            לשקף_בסיס / '명명/기계연결이름.h': '명명/기계연결이름.h',
            לשקף_בסיס / 'משתמש/לקשר_ניווט.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            לשקף_בסיס / 'build/user/start.o': 'lib/start.o',
            לשקף_בסיס / 'build/user/runtime.o': 'lib/runtime.o',
            לשקף_בסיס / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            לשקף_בסיס / 'משתמש/דוגמתקובץ.cpp': 'examples/דוגמתקובץ.cpp',
            לשקף_בסיס / '예제/한글코딩/인사.c': 'examples/인사.c',
            לשקף_בסיס / '예제/한글코딩/זרם_ערך.c': 'examples/זרם_ערך.c',
            לשקף_בסיס / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            לשקף_בסיס / 'משתמש/통신예제.cpp': 'examples/통신예제.cpp',
            לשקף_בסיס / 'build/user/demo.elf': 'examples/demo.elf',
            לשקף_בסיס / 'build/user/network.elf': 'examples/network.elf',
        }
        חבילה_מניפסט = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, יעד in קובץ_רשימה.items():
            יעד_נתונים_למען = ערכת_פיתוח / יעד
            יעד_נתונים_למען.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(יעד_נתונים_למען))
            חבילה_מניפסט['sha256'][יעד] = hashlib.sha256(יעד_נתונים_למען.read_bytes()).hexdigest()
        (ערכת_פיתוח / 'manifest.json').write_text(json.dumps(חבילה_מניפסט, indent=2) + '\n')
        (ערכת_פיתוח / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/דוגמתקובץ.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int התחל_משתמש_תוכנית(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: כלים/לבצע_פקודה.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 כלים/לבצע_קובץ.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: 사용자인수개수()/משתמש_ארגומנט() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        ארכיון = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(ארכיון), 'w:gz') as תוצאה_נתונים:
            תוצאה_נתונים.add(str(ערכת_פיתוח), arcname=ערכת_פיתוח.name)
        ארכיון.replace(הפצה_נתיב / ארכיון.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        מהדר_ארכיון = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(מהדר_ארכיון), 'w:gz') as תוצאה_נתונים:
            for שם in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                תוצאה_נתונים.add(str(לשקף_בסיס.parents[1] / שם), arcname='jkoros-native/' + שם)
            for נתיב_יחסי in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', 'מ_מהדר', 'משתמש', '명명',
                             'כלים/בנה_מ_מהדר.py', 'כלים/בנה_משתמש_חלל.py', '파일전송과번역.md'):
                תוצאה_נתונים.add(str(לשקף_בסיס / נתיב_יחסי), arcname='jkoros-native/' + נתיב_יחסי)
            for שם in ('crt.o', 'aot-runtime.o', 'זמן_ריצה_תמך.o', 'הפעלה.o', '미리번역.o', 'החזר_גשר.o'):
                קובץ_יעד_ffac9b48 = לשקף_בסיס / 'build/ccompiler' / שם
                תוצאה_נתונים.add(str(קובץ_יעד_ffac9b48), arcname='jkoros-native/relink/' + שם)
            for שם in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                תוצאה_נתונים.add(str(לשקף_בסיס / 'build/user' / שם), arcname='jkoros-native/relink/user/' + שם)
            תוצאה_נתונים.add(str(לשקף_בסיס / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            תוצאה_נתונים.add(str(포직스경로), arcname='posix-kor/arm64-native')
        מהדר_ארכיון.replace(הפצה_נתיב / מהדר_ארכיון.name)
    print('SDK:', הפצה_נתיב / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    הפעלה()
