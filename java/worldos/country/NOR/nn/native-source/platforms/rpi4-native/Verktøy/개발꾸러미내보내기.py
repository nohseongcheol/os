#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from Utfør_kommando import spegle_rot


def Køyr_2():
    배포경로 = spegle_rot / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = spegle_rot.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(spegle_rot / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        fil_Liste = {
            spegle_rot.parents[1] / 'LICENSE': 'LICENSE',
            spegle_rot.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            spegle_rot / 'Verktøy/개발꾸러미번역.py': 'compile.py',
            spegle_rot / 'brukar/호출.h': 'include/호출.h',
            spegle_rot / '명명/기계연결이름.h': '명명/기계연결이름.h',
            spegle_rot / 'brukar/kople_Oppsett.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            spegle_rot / 'build/user/start.o': 'lib/start.o',
            spegle_rot / 'build/user/runtime.o': 'lib/runtime.o',
            spegle_rot / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            spegle_rot / 'brukar/파일예제.cpp': 'examples/파일예제.cpp',
            spegle_rot / '예제/한글코딩/인사.c': 'examples/인사.c',
            spegle_rot / '예제/한글코딩/Stream_VALUE.c': 'examples/Stream_VALUE.c',
            spegle_rot / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            spegle_rot / 'brukar/통신예제.cpp': 'examples/통신예제.cpp',
            spegle_rot / 'build/user/demo.elf': 'examples/demo.elf',
            spegle_rot / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, mål in fil_Liste.items():
            mål_data_ADDRESS = 개발꾸러미 / mål
            mål_data_ADDRESS.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(mål_data_ADDRESS))
            꾸러미명세['sha256'][mål] = hashlib.sha256(mål_data_ADDRESS.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int START_brukar_app(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Verktøy/Utfør_kommando.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Verktøy/Utfør_fil.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: brukar_argument_COUNT()/brukar_argument() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Arkiv = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Arkiv), 'w:gz') as forretningsmål_data:
            forretningsmål_data.add(str(개발꾸러미), arcname=개발꾸러미.name)
        Arkiv.replace(배포경로 / Arkiv.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as forretningsmål_data:
            for Namn in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                forretningsmål_data.add(str(spegle_rot.parents[1] / Namn), arcname='jkoros-native/' + Namn)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'brukar', '명명',
                             'Verktøy/시언어번역기빌드.py', 'Verktøy/bygg_brukar_område.py', '파일전송과번역.md'):
                forretningsmål_data.add(str(spegle_rot / 상대경로), arcname='jkoros-native/' + 상대경로)
            for Namn in ('crt.o', 'aot-runtime.o', 'Common_Language_Runtime_støtte.o', 'Køyr_2.o', '미리번역.o', 'levere_tilbake_bru.o'):
                målfil = spegle_rot / 'build/ccompiler' / Namn
                forretningsmål_data.add(str(målfil), arcname='jkoros-native/relink/' + Namn)
            for Namn in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                forretningsmål_data.add(str(spegle_rot / 'build/user' / Namn), arcname='jkoros-native/relink/user/' + Namn)
            forretningsmål_data.add(str(spegle_rot / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            forretningsmål_data.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    Køyr_2()
