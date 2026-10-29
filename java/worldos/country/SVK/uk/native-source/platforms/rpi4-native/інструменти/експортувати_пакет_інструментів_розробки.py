#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from Виконати_команда import Дії_корінь


def запустити():
    배포경로 = Дії_корінь / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = Дії_корінь.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(Дії_корінь / 'build')) as 작업경로:
        пакет_розробки = Path(작업경로) / 'jkoros-native-sdk'
        Файл_список = {
            Дії_корінь.parents[1] / 'LICENSE': 'LICENSE',
            Дії_корінь.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            Дії_корінь / 'інструменти/пакет_інструментів_розробки_компілювати.py': 'compile.py',
            Дії_корінь / 'простір_користувача/호출.h': 'include/호출.h',
            Дії_корінь / '명명/기계연결이름.h': '명명/기계연결이름.h',
            Дії_корінь / 'простір_користувача/схема_компонування.ld': 'user.ld',
            포직스경로 / 'оголошення/파일규약.h': 'include/파일규약.h',
            포직스경로 / 'оголошення/통신규약.h': 'include/통신규약.h',
            Дії_корінь / 'build/user/start.o': 'lib/start.o',
            Дії_корінь / 'build/user/runtime.o': 'lib/runtime.o',
            Дії_корінь / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            Дії_корінь / 'простір_користувача/ПрикладФайлу.cpp': 'examples/ПрикладФайлу.cpp',
            Дії_корінь / '예제/한글코딩/인사.c': 'examples/인사.c',
            Дії_корінь / '예제/한글코딩/потік_значення.c': 'examples/потік_значення.c',
            Дії_корінь / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            Дії_корінь / 'простір_користувача/통신예제.cpp': 'examples/통신예제.cpp',
            Дії_корінь / 'build/user/demo.elf': 'examples/demo.elf',
            Дії_корінь / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, мета in Файл_список.items():
            місце_дані_адреса = пакет_розробки / мета
            місце_дані_адреса.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(місце_дані_адреса))
            꾸러미명세['sha256'][мета] = hashlib.sha256(місце_дані_адреса.read_bytes()).hexdigest()
        (пакет_розробки / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (пакет_розробки / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/ПрикладФайлу.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int ПУСК_користувач_програма(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: інструменти/Виконати_команда.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 інструменти/Виконати_Файл.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: 사용자인수개수()/користувач_аргумент() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Архів = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Архів), 'w:gz') as КР_дані:
            КР_дані.add(str(пакет_розробки), arcname=пакет_розробки.name)
        Архів.replace(배포경로 / Архів.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        компілятор_Архів = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(компілятор_Архів), 'w:gz') as КР_дані:
            for Назва in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                КР_дані.add(str(Дії_корінь.parents[1] / Назва), arcname='jkoros-native/' + Назва)
            for відносний_шлях in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'простір_користувача', '명명',
                             'інструменти/시언어번역기빌드.py', 'інструменти/збірка_користувач_ПРОБІЛ.py', '파일전송과번역.md'):
                КР_дані.add(str(Дії_корінь / відносний_шлях), arcname='jkoros-native/' + відносний_шлях)
            for Назва in ('crt.o', 'aot-runtime.o', 'загальномовне_середовище_виконання_опора.o', 'запустити.o', '미리번역.o', 'повернути_міст.o'):
                кінцевий_файл = Дії_корінь / 'build/ccompiler' / Назва
                КР_дані.add(str(кінцевий_файл), arcname='jkoros-native/relink/' + Назва)
            for Назва in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                КР_дані.add(str(Дії_корінь / 'build/user' / Назва), arcname='jkoros-native/relink/user/' + Назва)
            КР_дані.add(str(Дії_корінь / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            КР_дані.add(str(포직스경로), arcname='posix-kor/arm64-native')
        компілятор_Архів.replace(배포경로 / компілятор_Архів.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    запустити()
