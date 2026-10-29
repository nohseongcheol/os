#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from үтәргә_команда import экранга_җибәрү_тамыр


def эшләтү():
    배포경로 = экранга_җибәрү_тамыр / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = экранга_җибәрү_тамыр.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(экранга_җибәрү_тамыр / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        файл_Исемлек = {
            экранга_җибәрү_тамыр.parents[1] / 'LICENSE': 'LICENSE',
            экранга_җибәрү_тамыр.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            экранга_җибәрү_тамыр / 'Кораллар/개발꾸러미번역.py': 'compile.py',
            экранга_җибәрү_тамыр / 'кулланучы/호출.h': 'include/호출.h',
            экранга_җибәрү_тамыр / '명명/기계연결이름.h': '명명/기계연결이름.h',
            экранга_җибәрү_тамыр / 'кулланучы/бәйләү_план.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            экранга_җибәрү_тамыр / 'build/user/start.o': 'lib/start.o',
            экранга_җибәрү_тамыр / 'build/user/runtime.o': 'lib/runtime.o',
            экранга_җибәрү_тамыр / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            экранга_җибәрү_тамыр / 'кулланучы/파일예제.cpp': 'examples/파일예제.cpp',
            экранга_җибәрү_тамыр / '예제/한글코딩/인사.c': 'examples/인사.c',
            экранга_җибәрү_тамыр / '예제/한글코딩/агым_VALUE.c': 'examples/агым_VALUE.c',
            экранга_җибәрү_тамыр / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            экранга_җибәрү_тамыр / 'кулланучы/통신예제.cpp': 'examples/통신예제.cpp',
            экранга_җибәрү_тамыр / 'build/user/demo.elf': 'examples/demo.elf',
            экранга_җибәрү_тамыр / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, максат_кыйммәт in файл_Исемлек.items():
            күчерү_урыны_мәгълүмат_адрес = 개발꾸러미 / максат_кыйммәт
            күчерү_урыны_мәгълүмат_адрес.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(күчерү_урыны_мәгълүмат_адрес))
            꾸러미명세['sha256'][максат_кыйммәт] = hashlib.sha256(күчерү_урыны_мәгълүмат_адрес.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int Start_кулланучы_кушымта(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Кораллар/үтәргә_команда.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Кораллар/үтәргә_файл.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: кулланучы_аргумент_COUNT()/кулланучы_аргумент() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Архив = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Архив), 'w:gz') as үлчәм_мәгълүмат:
            үлчәм_мәгълүмат.add(str(개발꾸러미), arcname=개발꾸러미.name)
        Архив.replace(배포경로 / Архив.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as үлчәм_мәгълүмат:
            for исем in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                үлчәм_мәгълүмат.add(str(экранга_җибәрү_тамыр.parents[1] / исем), arcname='jkoros-native/' + исем)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'кулланучы', '명명',
                             'Кораллар/시언어번역기빌드.py', 'Кораллар/төзү_кулланучы_өлкә.py', '파일전송과번역.md'):
                үлчәм_мәгълүмат.add(str(экранга_җибәрү_тамыр / 상대경로), arcname='jkoros-native/' + 상대경로)
            for исем in ('crt.o', 'aot-runtime.o', 'CLR_мохите_ярдәм.o', 'эшләтү.o', '미리번역.o', 'кайтару_күпер.o'):
                максат_файл = экранга_җибәрү_тамыр / 'build/ccompiler' / исем
                үлчәм_мәгълүмат.add(str(максат_файл), arcname='jkoros-native/relink/' + исем)
            for исем in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                үлчәм_мәгълүмат.add(str(экранга_җибәрү_тамыр / 'build/user' / исем), arcname='jkoros-native/relink/user/' + исем)
            үлчәм_мәгълүмат.add(str(экранга_җибәрү_тамыр / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            үлчәм_мәгълүмат.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    эшләтү()
