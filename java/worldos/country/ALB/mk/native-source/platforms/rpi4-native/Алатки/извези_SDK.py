#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from Изврши_наредба import Project_корен


def Изврши_2():
    배포경로 = Project_корен / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = Project_корен.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(Project_корен / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        датотека_Список = {
            Project_корен.parents[1] / 'LICENSE': 'LICENSE',
            Project_корен.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            Project_корен / 'Алатки/SDK_изгради.py': 'compile.py',
            Project_корен / 'корисник/호출.h': 'include/호출.h',
            Project_корен / '명명/기계연결이름.h': '명명/기계연결이름.h',
            Project_корен / 'корисник/Врска_Распоред.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            Project_корен / 'build/user/start.o': 'lib/start.o',
            Project_корен / 'build/user/runtime.o': 'lib/runtime.o',
            Project_корен / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            Project_корен / 'корисник/파일예제.cpp': 'examples/파일예제.cpp',
            Project_корен / '예제/한글코딩/인사.c': 'examples/인사.c',
            Project_корен / '예제/한글코딩/Stream_VALUE.c': 'examples/Stream_VALUE.c',
            Project_корен / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            Project_корен / 'корисник/통신예제.cpp': 'examples/통신예제.cpp',
            Project_корен / 'build/user/demo.elf': 'examples/demo.elf',
            Project_корен / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, цел in датотека_Список.items():
            одредиште_податоци_адреса = 개발꾸러미 / цел
            одредиште_податоци_адреса.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(одредиште_податоци_адреса))
            꾸러미명세['sha256'][цел] = hashlib.sha256(одредиште_податоци_адреса.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int Start_корисник_програма(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Алатки/Изврши_наредба.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Алатки/Изврши_датотека.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: корисник_аргумент_COUNT()/корисник_аргумент() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Архива = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Архива), 'w:gz') as мерка_податоци:
            мерка_податоци.add(str(개발꾸러미), arcname=개발꾸러미.name)
        Архива.replace(배포경로 / Архива.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as мерка_податоци:
            for Име in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                мерка_податоци.add(str(Project_корен.parents[1] / Име), arcname='jkoros-native/' + Име)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'корисник', '명명',
                             'Алатки/시언어번역기빌드.py', 'Алатки/верзија_корисник_простор.py', '파일전송과번역.md'):
                мерка_податоци.add(str(Project_корен / 상대경로), arcname='jkoros-native/' + 상대경로)
            for Име in ('crt.o', 'aot-runtime.o', 'заеднички_јазик_за_време_на_извршување_Поддршка.o', 'Изврши_2.o', '미리번역.o', '되돌림.o'):
                одредишна_датотека = Project_корен / 'build/ccompiler' / Име
                мерка_податоци.add(str(одредишна_датотека), arcname='jkoros-native/relink/' + Име)
            for Име in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                мерка_податоци.add(str(Project_корен / 'build/user' / Име), arcname='jkoros-native/relink/user/' + Име)
            мерка_податоци.add(str(Project_корен / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            мерка_податоци.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    Изврши_2()
