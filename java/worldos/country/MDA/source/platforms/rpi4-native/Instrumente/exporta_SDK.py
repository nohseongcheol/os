#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from executa_comandă import Project_rădăcină


def Pornește():
    배포경로 = Project_rădăcină / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = Project_rădăcină.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(Project_rădăcină / 'build')) as 작업경로:
        kit_de_dezvoltare = Path(작업경로) / 'jkoros-native-sdk'
        Fișier_Listă = {
            Project_rădăcină.parents[1] / 'LICENSE': 'LICENSE',
            Project_rădăcină.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            Project_rădăcină / 'Instrumente/SDK_compilare.py': 'compile.py',
            Project_rădăcină / 'utilizator/호출.h': 'include/호출.h',
            Project_rădăcină / '명명/기계연결이름.h': '명명/기계연결이름.h',
            Project_rădăcină / 'utilizator/Link_Aspect.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            Project_rădăcină / 'build/user/start.o': 'lib/start.o',
            Project_rădăcină / 'build/user/runtime.o': 'lib/runtime.o',
            Project_rădăcină / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            Project_rădăcină / 'utilizator/ExempluFișier.cpp': 'examples/ExempluFișier.cpp',
            Project_rădăcină / '예제/한글코딩/인사.c': 'examples/인사.c',
            Project_rădăcină / '예제/한글코딩/flux_VALUE.c': 'examples/flux_VALUE.c',
            Project_rădăcină / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            Project_rădăcină / 'utilizator/통신예제.cpp': 'examples/통신예제.cpp',
            Project_rădăcină / 'build/user/demo.elf': 'examples/demo.elf',
            Project_rădăcină / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, țintă in Fișier_Listă.items():
            destinație_date_adresa = kit_de_dezvoltare / țintă
            destinație_date_adresa.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(destinație_date_adresa))
            꾸러미명세['sha256'][țintă] = hashlib.sha256(destinație_date_adresa.read_bytes()).hexdigest()
        (kit_de_dezvoltare / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (kit_de_dezvoltare / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/ExempluFișier.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int buta_utilizator_program(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Instrumente/executa_comandă.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Instrumente/executa_Fișier.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: utilizator_argument_COUNT()/utilizator_argument() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Arhivă = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Arhivă), 'w:gz') as KR_date:
            KR_date.add(str(kit_de_dezvoltare), arcname=kit_de_dezvoltare.name)
        Arhivă.replace(배포경로 / Arhivă.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        compilator_Arhivă = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(compilator_Arhivă), 'w:gz') as KR_date:
            for Nume in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                KR_date.add(str(Project_rădăcină.parents[1] / Nume), arcname='jkoros-native/' + Nume)
            for cale_relativă in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', 'C_compilator', 'utilizator', '명명',
                             'Instrumente/generare_C_compilator.py', 'Instrumente/generare_utilizator_SPAȚIU.py', '파일전송과번역.md'):
                KR_date.add(str(Project_rădăcină / cale_relativă), arcname='jkoros-native/' + cale_relativă)
            for Nume in ('crt.o', 'aot-runtime.o', 'CLR_suport.o', 'Pornește.o', '미리번역.o', 'restitui_punte.o'):
                fișier_destinație = Project_rădăcină / 'build/ccompiler' / Nume
                KR_date.add(str(fișier_destinație), arcname='jkoros-native/relink/' + Nume)
            for Nume in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                KR_date.add(str(Project_rădăcină / 'build/user' / Nume), arcname='jkoros-native/relink/user/' + Nume)
            KR_date.add(str(Project_rădăcină / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            KR_date.add(str(포직스경로), arcname='posix-kor/arm64-native')
        compilator_Arhivă.replace(배포경로 / compilator_Arhivă.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    Pornește()
