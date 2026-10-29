#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from ausféieren_Befeel import projezéieren_Racinn


def Laf():
    배포경로 = projezéieren_Racinn / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = projezéieren_Racinn.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(projezéieren_Racinn / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        Fichier_Lëscht = {
            projezéieren_Racinn.parents[1] / 'LICENSE': 'LICENSE',
            projezéieren_Racinn.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            projezéieren_Racinn / 'Tools/개발꾸러미번역.py': 'compile.py',
            projezéieren_Racinn / 'Benotzer/호출.h': 'include/호출.h',
            projezéieren_Racinn / '명명/기계연결이름.h': '명명/기계연결이름.h',
            projezéieren_Racinn / 'Benotzer/Link_Layout.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            projezéieren_Racinn / 'build/user/start.o': 'lib/start.o',
            projezéieren_Racinn / 'build/user/runtime.o': 'lib/runtime.o',
            projezéieren_Racinn / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            projezéieren_Racinn / 'Benotzer/파일예제.cpp': 'examples/파일예제.cpp',
            projezéieren_Racinn / '예제/한글코딩/인사.c': 'examples/인사.c',
            projezéieren_Racinn / '예제/한글코딩/Stream_VALUE.c': 'examples/Stream_VALUE.c',
            projezéieren_Racinn / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            projezéieren_Racinn / 'Benotzer/통신예제.cpp': 'examples/통신예제.cpp',
            projezéieren_Racinn / 'build/user/demo.elf': 'examples/demo.elf',
            projezéieren_Racinn / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, Zil in Fichier_Lëscht.items():
            Zil_Daten_Adress = 개발꾸러미 / Zil
            Zil_Daten_Adress.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(Zil_Daten_Adress))
            꾸러미명세['sha256'][Zil] = hashlib.sha256(Zil_Daten_Adress.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int Start_Benotzer_App(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Tools/ausféieren_Befeel.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Tools/ausféieren_Fichier.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: Benotzer_Argument_COUNT()/Benotzer_Argument() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Archiv = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Archiv), 'w:gz') as Mooss_Daten:
            Mooss_Daten.add(str(개발꾸러미), arcname=개발꾸러미.name)
        Archiv.replace(배포경로 / Archiv.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as Mooss_Daten:
            for Numm in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                Mooss_Daten.add(str(projezéieren_Racinn.parents[1] / Numm), arcname='jkoros-native/' + Numm)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'Benotzer', '명명',
                             'Tools/시언어번역기빌드.py', 'Tools/Build_Benotzer_Plaz.py', '파일전송과번역.md'):
                Mooss_Daten.add(str(projezéieren_Racinn / 상대경로), arcname='jkoros-native/' + 상대경로)
            for Numm in ('crt.o', 'aot-runtime.o', 'Common_Language_Runtime_Support.o', 'Laf.o', '미리번역.o', '되돌림.o'):
                Zilfichier = projezéieren_Racinn / 'build/ccompiler' / Numm
                Mooss_Daten.add(str(Zilfichier), arcname='jkoros-native/relink/' + Numm)
            for Numm in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                Mooss_Daten.add(str(projezéieren_Racinn / 'build/user' / Numm), arcname='jkoros-native/relink/user/' + Numm)
            Mooss_Daten.add(str(projezéieren_Racinn / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            Mooss_Daten.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    Laf()
