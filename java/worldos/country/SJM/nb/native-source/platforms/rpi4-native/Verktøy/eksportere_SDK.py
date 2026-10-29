#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from Utfør_kommando import speile_rot


def Kjør_2():
    distribusjon_bane = speile_rot / 'dist'
    distribusjon_bane.mkdir(exist_ok=True)
    포직스경로 = speile_rot.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(speile_rot / 'build')) as 작업경로:
        utviklingspakke = Path(작업경로) / 'jkoros-native-sdk'
        filliste = {
            speile_rot.parents[1] / 'LICENSE': 'LICENSE',
            speile_rot.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            speile_rot / 'Verktøy/SDK_kompilere.py': 'compile.py',
            speile_rot / 'bruker/호출.h': 'include/호출.h',
            speile_rot / '명명/기계연결이름.h': '명명/기계연결이름.h',
            speile_rot / 'bruker/koble_Oppsett.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            speile_rot / 'build/user/start.o': 'lib/start.o',
            speile_rot / 'build/user/runtime.o': 'lib/runtime.o',
            speile_rot / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            speile_rot / 'bruker/Fileksempel.cpp': 'examples/Fileksempel.cpp',
            speile_rot / '예제/한글코딩/인사.c': 'examples/인사.c',
            speile_rot / '예제/한글코딩/strøm_VERDI.c': 'examples/strøm_VERDI.c',
            speile_rot / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            speile_rot / 'bruker/통신예제.cpp': 'examples/통신예제.cpp',
            speile_rot / 'build/user/demo.elf': 'examples/demo.elf',
            speile_rot / 'build/user/network.elf': 'examples/network.elf',
        }
        bunt_manifest = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, mål in filliste.items():
            mål_data_e_post = utviklingspakke / mål
            mål_data_e_post.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(mål_data_e_post))
            bunt_manifest['sha256'][mål] = hashlib.sha256(mål_data_e_post.read_bytes()).hexdigest()
        (utviklingspakke / 'manifest.json').write_text(json.dumps(bunt_manifest, indent=2) + '\n')
        (utviklingspakke / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/Fileksempel.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int START_bruker_app(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Verktøy/Utfør_kommando.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Verktøy/Utfør_Fil.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: bruker_argument_ANTALL()/bruker_argument() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Arkiv = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Arkiv), 'w:gz') as KR_data:
            KR_data.add(str(utviklingspakke), arcname=utviklingspakke.name)
        Arkiv.replace(distribusjon_bane / Arkiv.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        kompilator_Arkiv = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(kompilator_Arkiv), 'w:gz') as KR_data:
            for Navn in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                KR_data.add(str(speile_rot.parents[1] / Navn), arcname='jkoros-native/' + Navn)
            for relativ_bane in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', 'C_kompilator', 'bruker', '명명',
                             'Verktøy/bygg_C_kompilator.py', 'Verktøy/bygg_bruker_Space.py', '파일전송과번역.md'):
                KR_data.add(str(speile_rot / relativ_bane), arcname='jkoros-native/' + relativ_bane)
            for Navn in ('crt.o', 'aot-runtime.o', 'CLR_støtte.o', 'Kjør_2.o', '미리번역.o', 'return_bro.o'):
                målfil = speile_rot / 'build/ccompiler' / Navn
                KR_data.add(str(målfil), arcname='jkoros-native/relink/' + Navn)
            for Navn in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                KR_data.add(str(speile_rot / 'build/user' / Navn), arcname='jkoros-native/relink/user/' + Navn)
            KR_data.add(str(speile_rot / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            KR_data.add(str(포직스경로), arcname='posix-kor/arm64-native')
        kompilator_Arkiv.replace(distribusjon_bane / kompilator_Arkiv.name)
    print('SDK:', distribusjon_bane / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    Kjør_2()
