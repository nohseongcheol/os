#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from köra_kommando import åtgärd_rot


def Kör():
    fördelning_väg = åtgärd_rot / 'dist'
    fördelning_väg.mkdir(exist_ok=True)
    포직스경로 = åtgärd_rot.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(åtgärd_rot / 'build')) as 작업경로:
        development_kit = Path(작업경로) / 'jkoros-native-sdk'
        fillista = {
            åtgärd_rot.parents[1] / 'LICENSE': 'LICENSE',
            åtgärd_rot.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            åtgärd_rot / 'verktyg/SDK_kompilera.py': 'compile.py',
            åtgärd_rot / 'användarutrymme/호출.h': 'include/호출.h',
            åtgärd_rot / '명명/기계연결이름.h': '명명/기계연결이름.h',
            åtgärd_rot / 'användarutrymme/länkningslayout.ld': 'user.ld',
            포직스경로 / 'deklarationer/파일규약.h': 'include/파일규약.h',
            포직스경로 / 'deklarationer/통신규약.h': 'include/통신규약.h',
            åtgärd_rot / 'build/user/start.o': 'lib/start.o',
            åtgärd_rot / 'build/user/runtime.o': 'lib/runtime.o',
            åtgärd_rot / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            åtgärd_rot / 'användarutrymme/Filexempel.cpp': 'examples/Filexempel.cpp',
            åtgärd_rot / '예제/한글코딩/인사.c': 'examples/인사.c',
            åtgärd_rot / '예제/한글코딩/flöde_värde.c': 'examples/flöde_värde.c',
            åtgärd_rot / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            åtgärd_rot / 'användarutrymme/통신예제.cpp': 'examples/통신예제.cpp',
            åtgärd_rot / 'build/user/demo.elf': 'examples/demo.elf',
            åtgärd_rot / 'build/user/network.elf': 'examples/network.elf',
        }
        bunt_manifest = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, mål in fillista.items():
            mål_data_ADRESS = development_kit / mål
            mål_data_ADRESS.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(mål_data_ADRESS))
            bunt_manifest['sha256'][mål] = hashlib.sha256(mål_data_ADRESS.read_bytes()).hexdigest()
        (development_kit / 'manifest.json').write_text(json.dumps(bunt_manifest, indent=2) + '\n')
        (development_kit / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/Filexempel.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int START_användare_app(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: verktyg/köra_kommando.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 verktyg/köra_fil.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: användare_argument_ANTAL()/användare_argument() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Arkiv = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Arkiv), 'w:gz') as KR_data:
            KR_data.add(str(development_kit), arcname=development_kit.name)
        Arkiv.replace(fördelning_väg / Arkiv.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        kompilerare_Arkiv = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(kompilerare_Arkiv), 'w:gz') as KR_data:
            for Namn in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                KR_data.add(str(åtgärd_rot.parents[1] / Namn), arcname='jkoros-native/' + Namn)
            for relativ_sökväg in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', 'C_kompilerare', 'användarutrymme', '명명',
                             'verktyg/version_C_kompilerare.py', 'verktyg/version_användare_Space.py', '파일전송과번역.md'):
                KR_data.add(str(åtgärd_rot / relativ_sökväg), arcname='jkoros-native/' + relativ_sökväg)
            for Namn in ('crt.o', 'aot-runtime.o', 'CLR_stöd.o', 'Kör.o', '미리번역.o', 'Retur_brygga.o'):
                målfil = åtgärd_rot / 'build/ccompiler' / Namn
                KR_data.add(str(målfil), arcname='jkoros-native/relink/' + Namn)
            for Namn in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                KR_data.add(str(åtgärd_rot / 'build/user' / Namn), arcname='jkoros-native/relink/user/' + Namn)
            KR_data.add(str(åtgärd_rot / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            KR_data.add(str(포직스경로), arcname='posix-kor/arm64-native')
        kompilerare_Arkiv.replace(fördelning_väg / kompilerare_Arkiv.name)
    print('SDK:', fördelning_väg / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    Kör()
