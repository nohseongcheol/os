#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from phethagatša_taelo import 기준


def Diriša():
    배포경로 = 기준 / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = 기준.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(기준 / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        faele_Lenaneo = {
            기준.parents[1] / 'LICENSE': 'LICENSE',
            기준.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            기준 / 'Ditholosi/개발꾸러미번역.py': 'compile.py',
            기준 / 'mošomiši/호출.h': 'include/호출.h',
            기준 / '명명/기계연결이름.h': '명명/기계연결이름.h',
            기준 / 'mošomiši/linke_Sebopego.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            기준 / 'build/user/start.o': 'lib/start.o',
            기준 / 'build/user/runtime.o': 'lib/runtime.o',
            기준 / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            기준 / 'mošomiši/파일예제.cpp': 'examples/파일예제.cpp',
            기준 / '예제/한글코딩/인사.c': 'examples/인사.c',
            기준 / '예제/한글코딩/Stream_boleng.c': 'examples/Stream_boleng.c',
            기준 / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            기준 / 'mošomiši/통신예제.cpp': 'examples/통신예제.cpp',
            기준 / 'build/user/demo.elf': 'examples/demo.elf',
            기준 / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, nepo in faele_Lenaneo.items():
            boyo_data_atrese = 개발꾸러미 / nepo
            boyo_data_atrese.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(boyo_data_atrese))
            꾸러미명세['sha256'][nepo] = hashlib.sha256(boyo_data_atrese.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int Thomišo_mošomiši_tirišo(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Ditholosi/phethagatša_taelo.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Ditholosi/phethagatša_faele.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: 사용자인수개수()/mošomiši_akumente() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Akhaebe = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Akhaebe), 'w:gz') as 결과자료:
            결과자료.add(str(개발꾸러미), arcname=개발꾸러미.name)
        Akhaebe.replace(배포경로 / Akhaebe.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as 결과자료:
            for Leina in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                결과자료.add(str(기준.parents[1] / Leina), arcname='jkoros-native/' + Leina)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'mošomiši', '명명',
                             'Ditholosi/시언어번역기빌드.py', 'Ditholosi/aga_mošomiši_sekgoba.py', '파일전송과번역.md'):
                결과자료.add(str(기준 / 상대경로), arcname='jkoros-native/' + 상대경로)
            for Leina in ('crt.o', 'aot-runtime.o', 'lebakanako_la_polelotlwaelwa_Thekgo.o', 'Diriša.o', '미리번역.o', '되돌림.o'):
                faele_ya_bobolokelo = 기준 / 'build/ccompiler' / Leina
                결과자료.add(str(faele_ya_bobolokelo), arcname='jkoros-native/relink/' + Leina)
            for Leina in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                결과자료.add(str(기준 / 'build/user' / Leina), arcname='jkoros-native/relink/user/' + Leina)
            결과자료.add(str(기준 / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            결과자료.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    Diriša()
