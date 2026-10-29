#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from Изврши_команда import пројектовати_корен


def Покрени():
    배포경로 = пројектовати_корен / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = пројектовати_корен.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(пројектовати_корен / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        фајл_Листа = {
            пројектовати_корен.parents[1] / 'LICENSE': 'LICENSE',
            пројектовати_корен.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            пројектовати_корен / 'Алатке/개발꾸러미번역.py': 'compile.py',
            пројектовати_корен / 'корисник/호출.h': 'include/호출.h',
            пројектовати_корен / '명명/기계연결이름.h': '명명/기계연결이름.h',
            пројектовати_корен / 'корисник/Веза_изглед.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            пројектовати_корен / 'build/user/start.o': 'lib/start.o',
            пројектовати_корен / 'build/user/runtime.o': 'lib/runtime.o',
            пројектовати_корен / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            пројектовати_корен / 'корисник/파일예제.cpp': 'examples/파일예제.cpp',
            пројектовати_корен / '예제/한글코딩/인사.c': 'examples/인사.c',
            пројектовати_корен / '예제/한글코딩/ток_вриједност.c': 'examples/ток_вриједност.c',
            пројектовати_корен / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            пројектовати_корен / 'корисник/통신예제.cpp': 'examples/통신예제.cpp',
            пројектовати_корен / 'build/user/demo.elf': 'examples/demo.elf',
            пројектовати_корен / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, циљ in фајл_Листа.items():
            одредиште_подаци_адреса = 개발꾸러미 / циљ
            одредиште_подаци_адреса.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(одредиште_подаци_адреса))
            꾸러미명세['sha256'][циљ] = hashlib.sha256(одредиште_подаци_адреса.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int Старт_корисник_програм(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Алатке/Изврши_команда.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Алатке/Изврши_фајл.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: 사용자인수개수()/корисник_аргумент() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Архива = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Архива), 'w:gz') as мера_подаци:
            мера_подаци.add(str(개발꾸러미), arcname=개발꾸러미.name)
        Архива.replace(배포경로 / Архива.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as мера_подаци:
            for Назив in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                мера_подаци.add(str(пројектовати_корен.parents[1] / Назив), arcname='jkoros-native/' + Назив)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'корисник', '명명',
                             'Алатке/시언어번역기빌드.py', 'Алатке/градити_корисник_простор.py', '파일전송과번역.md'):
                мера_подаци.add(str(пројектовати_корен / 상대경로), arcname='jkoros-native/' + 상대경로)
            for Назив in ('crt.o', 'aot-runtime.o', 'заједничка_извршна_језичка_компонента_Подршка.o', 'Покрени.o', '미리번역.o', 'вратити_мост.o'):
                одредишни_фајл = пројектовати_корен / 'build/ccompiler' / Назив
                мера_подаци.add(str(одредишни_фајл), arcname='jkoros-native/relink/' + Назив)
            for Назив in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                мера_подаци.add(str(пројектовати_корен / 'build/user' / Назив), arcname='jkoros-native/relink/user/' + Назив)
            мера_подаци.add(str(пројектовати_корен / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            мера_подаци.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    Покрени()
