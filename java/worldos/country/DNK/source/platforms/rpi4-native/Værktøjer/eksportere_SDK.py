#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from Udfør_kommando import To_do_rod


def Kør_2():
    distribution_sti = To_do_rod / 'dist'
    distribution_sti.mkdir(exist_ok=True)
    포직스경로 = To_do_rod.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(To_do_rod / 'build')) as 작업경로:
        Development_Kit = Path(작업경로) / 'jkoros-native-sdk'
        filliste = {
            To_do_rod.parents[1] / 'LICENSE': 'LICENSE',
            To_do_rod.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            To_do_rod / 'Værktøjer/SDK_kompilere.py': 'compile.py',
            To_do_rod / 'bruger/호출.h': 'include/호출.h',
            To_do_rod / '명명/기계연결이름.h': '명명/기계연결이름.h',
            To_do_rod / 'bruger/Link_Layout.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            To_do_rod / 'build/user/start.o': 'lib/start.o',
            To_do_rod / 'build/user/runtime.o': 'lib/runtime.o',
            To_do_rod / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            To_do_rod / 'bruger/Fileksempel.cpp': 'examples/Fileksempel.cpp',
            To_do_rod / '예제/한글코딩/인사.c': 'examples/인사.c',
            To_do_rod / '예제/한글코딩/strøm_VÆRDI.c': 'examples/strøm_VÆRDI.c',
            To_do_rod / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            To_do_rod / 'bruger/통신예제.cpp': 'examples/통신예제.cpp',
            To_do_rod / 'build/user/demo.elf': 'examples/demo.elf',
            To_do_rod / 'build/user/network.elf': 'examples/network.elf',
        }
        bundt_manifest = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, mål in filliste.items():
            destination_data_mail = Development_Kit / mål
            destination_data_mail.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(destination_data_mail))
            bundt_manifest['sha256'][mål] = hashlib.sha256(destination_data_mail.read_bytes()).hexdigest()
        (Development_Kit / 'manifest.json').write_text(json.dumps(bundt_manifest, indent=2) + '\n')
        (Development_Kit / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/Fileksempel.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int START_bruger_app(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Værktøjer/Udfør_kommando.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Værktøjer/Udfør_fil.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: bruger_argument_TÆL()/bruger_argument() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Arkiv = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Arkiv), 'w:gz') as KR_data:
            KR_data.add(str(Development_Kit), arcname=Development_Kit.name)
        Arkiv.replace(distribution_sti / Arkiv.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        compiler_Arkiv = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(compiler_Arkiv), 'w:gz') as KR_data:
            for Navn in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                KR_data.add(str(To_do_rod.parents[1] / Navn), arcname='jkoros-native/' + Navn)
            for relativ_sti in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', 'C_compiler', 'bruger', '명명',
                             'Værktøjer/build_C_compiler.py', 'Værktøjer/build_bruger_Space.py', '파일전송과번역.md'):
                KR_data.add(str(To_do_rod / relativ_sti), arcname='jkoros-native/' + relativ_sti)
            for Navn in ('crt.o', 'aot-runtime.o', 'CLR_støtte.o', 'Kør_2.o', '미리번역.o', 'returnere_bro.o'):
                destinationsfil = To_do_rod / 'build/ccompiler' / Navn
                KR_data.add(str(destinationsfil), arcname='jkoros-native/relink/' + Navn)
            for Navn in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                KR_data.add(str(To_do_rod / 'build/user' / Navn), arcname='jkoros-native/relink/user/' + Navn)
            KR_data.add(str(To_do_rod / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            KR_data.add(str(포직스경로), arcname='posix-kor/arm64-native')
        compiler_Arkiv.replace(distribution_sti / compiler_Arkiv.name)
    print('SDK:', distribution_sti / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    Kør_2()
