#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from Uitvoeren_opdracht import Taken_wortel


def starten():
    distributie_pad = Taken_wortel / 'dist'
    distributie_pad.mkdir(exist_ok=True)
    포직스경로 = Taken_wortel.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(Taken_wortel / 'build')) as 작업경로:
        Development_Kit = Path(작업경로) / 'jkoros-native-sdk'
        bestandslijst = {
            Taken_wortel.parents[1] / 'LICENSE': 'LICENSE',
            Taken_wortel.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            Taken_wortel / 'hulpmiddelen/SDK_compileren.py': 'compile.py',
            Taken_wortel / 'gebruikersruimte/호출.h': 'include/호출.h',
            Taken_wortel / '명명/기계연결이름.h': '명명/기계연결이름.h',
            Taken_wortel / 'gebruikersruimte/koppelindeling.ld': 'user.ld',
            포직스경로 / 'declaraties/파일규약.h': 'include/파일규약.h',
            포직스경로 / 'declaraties/통신규약.h': 'include/통신규약.h',
            Taken_wortel / 'build/user/start.o': 'lib/start.o',
            Taken_wortel / 'build/user/runtime.o': 'lib/runtime.o',
            Taken_wortel / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            Taken_wortel / 'gebruikersruimte/Bestandsvoorbeeld.cpp': 'examples/Bestandsvoorbeeld.cpp',
            Taken_wortel / '예제/한글코딩/인사.c': 'examples/인사.c',
            Taken_wortel / '예제/한글코딩/Stream_WAARDE.c': 'examples/Stream_WAARDE.c',
            Taken_wortel / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            Taken_wortel / 'gebruikersruimte/통신예제.cpp': 'examples/통신예제.cpp',
            Taken_wortel / 'build/user/demo.elf': 'examples/demo.elf',
            Taken_wortel / 'build/user/network.elf': 'examples/network.elf',
        }
        bundel_manifest = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, doel in bestandslijst.items():
            doel_gegevens_ADRES = Development_Kit / doel
            doel_gegevens_ADRES.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(doel_gegevens_ADRES))
            bundel_manifest['sha256'][doel] = hashlib.sha256(doel_gegevens_ADRES.read_bytes()).hexdigest()
        (Development_Kit / 'manifest.json').write_text(json.dumps(bundel_manifest, indent=2) + '\n')
        (Development_Kit / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/Bestandsvoorbeeld.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int START_gebruiker_app(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: hulpmiddelen/Uitvoeren_opdracht.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 hulpmiddelen/Uitvoeren_Bestand.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: gebruiker_argument_AANTAL()/gebruiker_argument() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Archief = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Archief), 'w:gz') as HR_gegevens:
            HR_gegevens.add(str(Development_Kit), arcname=Development_Kit.name)
        Archief.replace(distributie_pad / Archief.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        compiler_Archief = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(compiler_Archief), 'w:gz') as HR_gegevens:
            for Naam in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                HR_gegevens.add(str(Taken_wortel.parents[1] / Naam), arcname='jkoros-native/' + Naam)
            for relatief_pad in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', 'C_compiler', 'gebruikersruimte', '명명',
                             'hulpmiddelen/build_C_compiler.py', 'hulpmiddelen/build_gebruiker_Space.py', '파일전송과번역.md'):
                HR_gegevens.add(str(Taken_wortel / relatief_pad), arcname='jkoros-native/' + relatief_pad)
            for Naam in ('crt.o', 'aot-runtime.o', 'CLR_steun.o', 'starten.o', '미리번역.o', 'Retour_brug.o'):
                doelbestand = Taken_wortel / 'build/ccompiler' / Naam
                HR_gegevens.add(str(doelbestand), arcname='jkoros-native/relink/' + Naam)
            for Naam in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                HR_gegevens.add(str(Taken_wortel / 'build/user' / Naam), arcname='jkoros-native/relink/user/' + Naam)
            HR_gegevens.add(str(Taken_wortel / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            HR_gegevens.add(str(포직스경로), arcname='posix-kor/arm64-native')
        compiler_Archief.replace(distributie_pad / compiler_Archief.name)
    print('SDK:', distributie_pad / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    starten()
