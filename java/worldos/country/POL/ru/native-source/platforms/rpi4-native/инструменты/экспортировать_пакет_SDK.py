#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from 실행 import задача_корень


def запустить():
    распределение_путь = задача_корень / 'dist'
    распределение_путь.mkdir(exist_ok=True)
    포직스경로 = задача_корень.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(задача_корень / 'build')) as 작업경로:
        комплект_SDK = Path(작업경로) / 'jkoros-native-sdk'
        список_файлов = {
            задача_корень.parents[1] / 'LICENSE': 'LICENSE',
            задача_корень.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            задача_корень / 'инструменты/пакет_SDK_компилировать.py': 'compile.py',
            задача_корень / 'пространство_пользователя/호출.h': 'include/호출.h',
            задача_корень / '명명/기계연결이름.h': '명명/기계연결이름.h',
            задача_корень / 'пространство_пользователя/схема_компоновки.ld': 'user.ld',
            포직스경로 / 'объявления/файл_ABI.h': 'include/файл_ABI.h',
            포직스경로 / 'объявления/сеть_ABI.h': 'include/сеть_ABI.h',
            задача_корень / 'build/user/start.o': 'lib/start.o',
            задача_корень / 'build/user/runtime.o': 'lib/runtime.o',
            задача_корень / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            задача_корень / 'пространство_пользователя/ПримерФайла.cpp': 'examples/ПримерФайла.cpp',
            задача_корень / '예제/한글코딩/приветствие_ae353e94.c': 'examples/приветствие_ae353e94.c',
            задача_корень / '예제/한글코딩/поток_ЗНАЧЕН.c': 'examples/поток_ЗНАЧЕН.c',
            задача_корень / '예제/한글코딩/приветствие_ae353e94.cpp': 'examples/приветствие_ae353e94.cpp',
            задача_корень / 'пространство_пользователя/통신예제.cpp': 'examples/통신예제.cpp',
            задача_корень / 'build/user/demo.elf': 'examples/demo.elf',
            задача_корень / 'build/user/network.elf': 'examples/network.elf',
        }
        пакет_манифест = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, целевое_значение in список_файлов.items():
            цель_данные_АДРЕС = комплект_SDK / целевое_значение
            цель_данные_АДРЕС.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(цель_данные_АДРЕС))
            пакет_манифест['sha256'][целевое_значение] = hashlib.sha256(цель_данные_АДРЕС.read_bytes()).hexdigest()
        (комплект_SDK / 'manifest.json').write_text(json.dumps(пакет_манифест, indent=2) + '\n')
        (комплект_SDK / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/ПримерФайла.cpp -o demo.elf\n'
            'python3 compile.py examples/приветствие_ae353e94.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int Пуск_пользователь_программа(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: инструменты/실행.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 инструменты/Выполнить_файл.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: пользователь_аргумент_СЧЁТ()/пользователь_аргумент() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Архив = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Архив), 'w:gz') as KR_данные:
            KR_данные.add(str(комплект_SDK), arcname=комплект_SDK.name)
        Архив.replace(распределение_путь / Архив.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        компилятор_Архив = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(компилятор_Архив), 'w:gz') as KR_данные:
            for Название in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                KR_данные.add(str(задача_корень.parents[1] / Название), arcname='jkoros-native/' + Название)
            for относительный_путь in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', 'C_компилятор', 'пространство_пользователя', '명명',
                             'инструменты/BLD_C_компилятор.py', 'инструменты/BLD_пользователь_место.py', '파일전송과번역.md'):
                KR_данные.add(str(задача_корень / относительный_путь), arcname='jkoros-native/' + относительный_путь)
            for Название in ('crt.o', 'aot-runtime.o', 'ПоддержкаВыполнения.o', 'запустить.o', '미리번역.o', 'Возврат_мост.o'):
                конечный_файл = задача_корень / 'build/ccompiler' / Название
                KR_данные.add(str(конечный_файл), arcname='jkoros-native/relink/' + Название)
            for Название in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                KR_данные.add(str(задача_корень / 'build/user' / Название), arcname='jkoros-native/relink/user/' + Название)
            KR_данные.add(str(задача_корень / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            KR_данные.add(str(포직스경로), arcname='posix-kor/arm64-native')
        компилятор_Архив.replace(распределение_путь / компилятор_Архив.name)
    print('SDK:', распределение_путь / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    запустить()
