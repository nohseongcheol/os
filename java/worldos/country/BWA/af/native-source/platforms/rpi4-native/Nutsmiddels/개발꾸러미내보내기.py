#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from uitvoer_bevel import Project_wortel


def Loop():
    배포경로 = Project_wortel / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = Project_wortel.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(Project_wortel / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        lêer_Lys = {
            Project_wortel.parents[1] / 'LICENSE': 'LICENSE',
            Project_wortel.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            Project_wortel / 'Nutsmiddels/개발꾸러미번역.py': 'compile.py',
            Project_wortel / 'gebruiker/호출.h': 'include/호출.h',
            Project_wortel / '명명/기계연결이름.h': '명명/기계연결이름.h',
            Project_wortel / 'gebruiker/Skakel_Uitleg.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            Project_wortel / 'build/user/start.o': 'lib/start.o',
            Project_wortel / 'build/user/runtime.o': 'lib/runtime.o',
            Project_wortel / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            Project_wortel / 'gebruiker/파일예제.cpp': 'examples/파일예제.cpp',
            Project_wortel / '예제/한글코딩/인사.c': 'examples/인사.c',
            Project_wortel / '예제/한글코딩/Stream_VALUE.c': 'examples/Stream_VALUE.c',
            Project_wortel / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            Project_wortel / 'gebruiker/통신예제.cpp': 'examples/통신예제.cpp',
            Project_wortel / 'build/user/demo.elf': 'examples/demo.elf',
            Project_wortel / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, teiken in lêer_Lys.items():
            bestemming_data_adres = 개발꾸러미 / teiken
            bestemming_data_adres.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(bestemming_data_adres))
            꾸러미명세['sha256'][teiken] = hashlib.sha256(bestemming_data_adres.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int BEGIN_gebruiker_program(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Nutsmiddels/uitvoer_bevel.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Nutsmiddels/uitvoer_lêer.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: gebruiker_argument_COUNT()/gebruiker_argument() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Argief = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Argief), 'w:gz') as maatreël_data:
            maatreël_data.add(str(개발꾸러미), arcname=개발꾸러미.name)
        Argief.replace(배포경로 / Argief.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as maatreël_data:
            for Naam in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                maatreël_data.add(str(Project_wortel.parents[1] / Naam), arcname='jkoros-native/' + Naam)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'gebruiker', '명명',
                             'Nutsmiddels/시언어번역기빌드.py', 'Nutsmiddels/bou_gebruiker_ruimte.py', '파일전송과번역.md'):
                maatreël_data.add(str(Project_wortel / 상대경로), arcname='jkoros-native/' + 상대경로)
            for Naam in ('crt.o', 'aot-runtime.o', 'algemene_taallooptyd_Bystand.o', 'Loop.o', '미리번역.o', 'teruggee_brug.o'):
                bestemmingslêer = Project_wortel / 'build/ccompiler' / Naam
                maatreël_data.add(str(bestemmingslêer), arcname='jkoros-native/relink/' + Naam)
            for Naam in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                maatreël_data.add(str(Project_wortel / 'build/user' / Naam), arcname='jkoros-native/relink/user/' + Naam)
            maatreël_data.add(str(Project_wortel / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            maatreël_data.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    Loop()
