#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from изпълнявам_команда import проект_корен


def Стартиране():
    배포경로 = проект_корен / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = проект_корен.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(проект_корен / 'build')) as 작업경로:
        развоен_пакет = Path(작업경로) / 'jkoros-native-sdk'
        Файл_Списък = {
            проект_корен.parents[1] / 'LICENSE': 'LICENSE',
            проект_корен.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            проект_корен / 'Инструменти/софтуерен_развоен_пакет_компилирам.py': 'compile.py',
            проект_корен / 'потребител/호출.h': 'include/호출.h',
            проект_корен / '명명/기계연결이름.h': '명명/기계연결이름.h',
            проект_корен / 'потребител/Връзка_схема.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            проект_корен / 'build/user/start.o': 'lib/start.o',
            проект_корен / 'build/user/runtime.o': 'lib/runtime.o',
            проект_корен / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            проект_корен / 'потребител/파일예제.cpp': 'examples/파일예제.cpp',
            проект_корен / '예제/한글코딩/인사.c': 'examples/인사.c',
            проект_корен / '예제/한글코딩/поток_стойност.c': 'examples/поток_стойност.c',
            проект_корен / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            проект_корен / 'потребител/통신예제.cpp': 'examples/통신예제.cpp',
            проект_корен / 'build/user/demo.elf': 'examples/demo.elf',
            проект_корен / 'build/user/network.elf': 'examples/network.elf',
        }
        пакет_манифест = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, цел in Файл_Списък.items():
            местоназначение_данни_адрес = развоен_пакет / цел
            местоназначение_данни_адрес.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(местоназначение_данни_адрес))
            пакет_манифест['sha256'][цел] = hashlib.sha256(местоназначение_данни_адрес.read_bytes()).hexdigest()
        (развоен_пакет / 'manifest.json').write_text(json.dumps(пакет_манифест, indent=2) + '\n')
        (развоен_пакет / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int Старт_потребител_програма(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Инструменти/изпълнявам_команда.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Инструменти/изпълнявам_Файл.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: 사용자인수개수()/потребител_аргумент() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Архив = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Архив), 'w:gz') as мярка_данни:
            мярка_данни.add(str(развоен_пакет), arcname=развоен_пакет.name)
        Архив.replace(배포경로 / Архив.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        компилатор_Архив = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(компилатор_Архив), 'w:gz') as мярка_данни:
            for Име in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                мярка_данни.add(str(проект_корен.parents[1] / Име), arcname='jkoros-native/' + Име)
            for относителен_път in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'потребител', '명명',
                             'Инструменти/시언어번역기빌드.py', 'Инструменти/компилация_потребител_ИНТЕРВАЛ.py', '파일전송과번역.md'):
                мярка_данни.add(str(проект_корен / относителен_път), arcname='jkoros-native/' + относителен_път)
            for Име in ('crt.o', 'aot-runtime.o', 'обща_езикова_среда_Поддръжка.o', 'Стартиране.o', '미리번역.o', 'връщам_мост.o'):
                файл_местоназначение = проект_корен / 'build/ccompiler' / Име
                мярка_данни.add(str(файл_местоназначение), arcname='jkoros-native/relink/' + Име)
            for Име in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                мярка_данни.add(str(проект_корен / 'build/user' / Име), arcname='jkoros-native/relink/user/' + Име)
            мярка_данни.add(str(проект_корен / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            мярка_данни.add(str(포직스경로), arcname='posix-kor/arm64-native')
        компилатор_Архив.replace(배포경로 / компилатор_Архив.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    Стартиране()
