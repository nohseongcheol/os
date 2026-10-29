#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from eżegwixxa_kmand import pprojetta_għerq


def serje():
    배포경로 = pprojetta_għerq / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = pprojetta_għerq.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(pprojetta_għerq / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        fajl_Lista = {
            pprojetta_għerq.parents[1] / 'LICENSE': 'LICENSE',
            pprojetta_għerq.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            pprojetta_għerq / 'Għodod/개발꾸러미번역.py': 'compile.py',
            pprojetta_għerq / 'utent/호출.h': 'include/호출.h',
            pprojetta_għerq / '명명/기계연결이름.h': '명명/기계연결이름.h',
            pprojetta_għerq / 'utent/Link_Tqassim.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            pprojetta_għerq / 'build/user/start.o': 'lib/start.o',
            pprojetta_għerq / 'build/user/runtime.o': 'lib/runtime.o',
            pprojetta_għerq / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            pprojetta_għerq / 'utent/파일예제.cpp': 'examples/파일예제.cpp',
            pprojetta_għerq / '예제/한글코딩/인사.c': 'examples/인사.c',
            pprojetta_għerq / '예제/한글코딩/Stream_VALUE.c': 'examples/Stream_VALUE.c',
            pprojetta_għerq / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            pprojetta_għerq / 'utent/통신예제.cpp': 'examples/통신예제.cpp',
            pprojetta_għerq / 'build/user/demo.elf': 'examples/demo.elf',
            pprojetta_għerq / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, mira in fajl_Lista.items():
            destinazzjoni_data_ADDRESS = 개발꾸러미 / mira
            destinazzjoni_data_ADDRESS.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(destinazzjoni_data_ADDRESS))
            꾸러미명세['sha256'][mira] = hashlib.sha256(destinazzjoni_data_ADDRESS.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int Bidu_utent_programm(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Għodod/eżegwixxa_kmand.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Għodod/eżegwixxa_fajl.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: utent_argument_COUNT()/utent_argument() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Arkivju = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Arkivju), 'w:gz') as miżura_data:
            miżura_data.add(str(개발꾸러미), arcname=개발꾸러미.name)
        Arkivju.replace(배포경로 / Arkivju.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as miżura_data:
            for isem in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                miżura_data.add(str(pprojetta_għerq.parents[1] / isem), arcname='jkoros-native/' + isem)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'utent', '명명',
                             'Għodod/시언어번역기빌드.py', 'Għodod/bena_utent_SPACE.py', '파일전송과번역.md'):
                miżura_data.add(str(pprojetta_għerq / 상대경로), arcname='jkoros-native/' + 상대경로)
            for isem in ('crt.o', 'aot-runtime.o', 'tħaddim_tal_lingwa_komuni_Appoġġ.o', 'serje.o', '미리번역.o', '되돌림.o'):
                fajl_tad_destinazzjoni = pprojetta_għerq / 'build/ccompiler' / isem
                miżura_data.add(str(fajl_tad_destinazzjoni), arcname='jkoros-native/relink/' + isem)
            for isem in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                miżura_data.add(str(pprojetta_għerq / 'build/user' / isem), arcname='jkoros-native/relink/user/' + isem)
            miżura_data.add(str(pprojetta_għerq / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            miżura_data.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    serje()
