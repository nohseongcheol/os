#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from Izvrši_komanda import radnja_koren


def koristiti():
    배포경로 = radnja_koren / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = radnja_koren.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(radnja_koren / 'build')) as 작업경로:
        komplet_za_razvoj_programa = Path(작업경로) / 'jkoros-native-sdk'
        Datoteka_Lista = {
            radnja_koren.parents[1] / 'LICENSE': 'LICENSE',
            radnja_koren.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            radnja_koren / 'Alatke/SDK_kompajlirati.py': 'compile.py',
            radnja_koren / 'korisnik/호출.h': 'include/호출.h',
            radnja_koren / '명명/기계연결이름.h': '명명/기계연결이름.h',
            radnja_koren / 'korisnik/Veza_Raspored.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            radnja_koren / 'build/user/start.o': 'lib/start.o',
            radnja_koren / 'build/user/runtime.o': 'lib/runtime.o',
            radnja_koren / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            radnja_koren / 'korisnik/파일예제.cpp': 'examples/파일예제.cpp',
            radnja_koren / '예제/한글코딩/인사.c': 'examples/인사.c',
            radnja_koren / '예제/한글코딩/tok_VALUE.c': 'examples/tok_VALUE.c',
            radnja_koren / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            radnja_koren / 'korisnik/통신예제.cpp': 'examples/통신예제.cpp',
            radnja_koren / 'build/user/demo.elf': 'examples/demo.elf',
            radnja_koren / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, cilj in Datoteka_Lista.items():
            odredište_podaci_adresa = komplet_za_razvoj_programa / cilj
            odredište_podaci_adresa.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(odredište_podaci_adresa))
            꾸러미명세['sha256'][cilj] = hashlib.sha256(odredište_podaci_adresa.read_bytes()).hexdigest()
        (komplet_za_razvoj_programa / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (komplet_za_razvoj_programa / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int START_korisnik_program(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Alatke/Izvrši_komanda.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Alatke/Izvrši_Datoteka.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: korisnik_argument_COUNT()/korisnik_argument() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Arhiva = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Arhiva), 'w:gz') as KR_podaci:
            KR_podaci.add(str(komplet_za_razvoj_programa), arcname=komplet_za_razvoj_programa.name)
        Arhiva.replace(배포경로 / Arhiva.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        kompajler_Arhiva = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(kompajler_Arhiva), 'w:gz') as KR_podaci:
            for ime in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                KR_podaci.add(str(radnja_koren.parents[1] / ime), arcname='jkoros-native/' + ime)
            for relativna_putanja in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', 'C_kompajler', 'korisnik', '명명',
                             'Alatke/verzija_C_kompajler.py', 'Alatke/verzija_korisnik_prostor.py', '파일전송과번역.md'):
                KR_podaci.add(str(radnja_koren / relativna_putanja), arcname='jkoros-native/' + relativna_putanja)
            for ime in ('crt.o', 'aot-runtime.o', 'CLR_komponenta_Podrška.o', 'koristiti.o', '미리번역.o', 'vratiti_most.o'):
                odredišna_datoteka = radnja_koren / 'build/ccompiler' / ime
                KR_podaci.add(str(odredišna_datoteka), arcname='jkoros-native/relink/' + ime)
            for ime in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                KR_podaci.add(str(radnja_koren / 'build/user' / ime), arcname='jkoros-native/relink/user/' + ime)
            KR_podaci.add(str(radnja_koren / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            KR_podaci.add(str(포직스경로), arcname='posix-kor/arm64-native')
        kompajler_Arhiva.replace(배포경로 / kompajler_Arhiva.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    koristiti()
