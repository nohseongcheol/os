#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from орындау_пәрмен import жоба_түбір


def Орындау_2():
    배포경로 = жоба_түбір / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = жоба_түбір.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(жоба_түбір / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        файл_Тізім = {
            жоба_түбір.parents[1] / 'LICENSE': 'LICENSE',
            жоба_түбір.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            жоба_түбір / 'Құралдар/бағдарламалық_құралды_әзірлеуге_арналған_құралдар_жиынтығы_құрастыру.py': 'compile.py',
            жоба_түбір / 'пайдаланушы/호출.h': 'include/호출.h',
            жоба_түбір / '명명/기계연결이름.h': '명명/기계연결이름.h',
            жоба_түбір / 'пайдаланушы/Cілтеме_макет.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            жоба_түбір / 'build/user/start.o': 'lib/start.o',
            жоба_түбір / 'build/user/runtime.o': 'lib/runtime.o',
            жоба_түбір / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            жоба_түбір / 'пайдаланушы/파일예제.cpp': 'examples/파일예제.cpp',
            жоба_түбір / '예제/한글코딩/인사.c': 'examples/인사.c',
            жоба_түбір / '예제/한글코딩/ағым_мән.c': 'examples/ағым_мән.c',
            жоба_түбір / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            жоба_түбір / 'пайдаланушы/통신예제.cpp': 'examples/통신예제.cpp',
            жоба_түбір / 'build/user/demo.elf': 'examples/demo.elf',
            жоба_түбір / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, мақсатты_мән in файл_Тізім.items():
            тағайындау_деректер_мекенжай = 개발꾸러미 / мақсатты_мән
            тағайындау_деректер_мекенжай.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(тағайындау_деректер_мекенжай))
            꾸러미명세['sha256'][мақсатты_мән] = hashlib.sha256(тағайындау_деректер_мекенжай.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int басы_пайдаланушы_бағдарлама(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Құралдар/орындау_пәрмен.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Құралдар/орындау_файл.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: 사용자인수개수()/пайдаланушы_аргумент() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Мұрағат = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Мұрағат), 'w:gz') as өлшем_деректер:
            өлшем_деректер.add(str(개발꾸러미), arcname=개발꾸러미.name)
        Мұрағат.replace(배포경로 / Мұрағат.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as өлшем_деректер:
            for Аты in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                өлшем_деректер.add(str(жоба_түбір.parents[1] / Аты), arcname='jkoros-native/' + Аты)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'пайдаланушы', '명명',
                             'Құралдар/시언어번역기빌드.py', 'Құралдар/құрастыру_пайдаланушы_орын.py', '파일전송과번역.md'):
                өлшем_деректер.add(str(жоба_түбір / 상대경로), arcname='jkoros-native/' + 상대경로)
            for Аты in ('crt.o', 'aot-runtime.o', 'CLR_ортасы_тіреу.o', 'Орындау_2.o', '미리번역.o', 'қайтару_көпір.o'):
                тағайындалған_файл = жоба_түбір / 'build/ccompiler' / Аты
                өлшем_деректер.add(str(тағайындалған_файл), arcname='jkoros-native/relink/' + Аты)
            for Аты in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                өлшем_деректер.add(str(жоба_түбір / 'build/user' / Аты), arcname='jkoros-native/relink/user/' + Аты)
            өлшем_деректер.add(str(жоба_түбір / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            өлшем_деректер.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    Орындау_2()
