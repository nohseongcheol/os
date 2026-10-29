#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from Izvrši_naredba import akcija_korijen


def Pokreni():
    배포경로 = akcija_korijen / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = akcija_korijen.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(akcija_korijen / 'build')) as 작업경로:
        set_razvojnih_alata = Path(작업경로) / 'jkoros-native-sdk'
        Datoteka_Popis = {
            akcija_korijen.parents[1] / 'LICENSE': 'LICENSE',
            akcija_korijen.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            akcija_korijen / 'Alati/SDK_programski_prevesti.py': 'compile.py',
            akcija_korijen / 'korisnik/호출.h': 'include/호출.h',
            akcija_korijen / '명명/기계연결이름.h': '명명/기계연결이름.h',
            akcija_korijen / 'korisnik/veza_Raspored.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            akcija_korijen / 'build/user/start.o': 'lib/start.o',
            akcija_korijen / 'build/user/runtime.o': 'lib/runtime.o',
            akcija_korijen / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            akcija_korijen / 'korisnik/PrimjerDatoteke.cpp': 'examples/PrimjerDatoteke.cpp',
            akcija_korijen / '예제/한글코딩/인사.c': 'examples/인사.c',
            akcija_korijen / '예제/한글코딩/tok_VALUE.c': 'examples/tok_VALUE.c',
            akcija_korijen / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            akcija_korijen / 'korisnik/통신예제.cpp': 'examples/통신예제.cpp',
            akcija_korijen / 'build/user/demo.elf': 'examples/demo.elf',
            akcija_korijen / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, cilj in Datoteka_Popis.items():
            odredište_podaci_adresa = set_razvojnih_alata / cilj
            odredište_podaci_adresa.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(odredište_podaci_adresa))
            꾸러미명세['sha256'][cilj] = hashlib.sha256(odredište_podaci_adresa.read_bytes()).hexdigest()
        (set_razvojnih_alata / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (set_razvojnih_alata / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/PrimjerDatoteke.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int START_korisnik_program(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Alati/Izvrši_naredba.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Alati/Izvrši_Datoteka.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: korisnik_argument_COUNT()/korisnik_argument() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Arhiva = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Arhiva), 'w:gz') as KR_podaci:
            KR_podaci.add(str(set_razvojnih_alata), arcname=set_razvojnih_alata.name)
        Arhiva.replace(배포경로 / Arhiva.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        kompilator_Arhiva = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(kompilator_Arhiva), 'w:gz') as KR_podaci:
            for Ime in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                KR_podaci.add(str(akcija_korijen.parents[1] / Ime), arcname='jkoros-native/' + Ime)
            for relativni_put in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', 'C_kompilator', 'korisnik', '명명',
                             'Alati/međuverzija_C_kompilator.py', 'Alati/međuverzija_korisnik_Space.py', '파일전송과번역.md'):
                KR_podaci.add(str(akcija_korijen / relativni_put), arcname='jkoros-native/' + relativni_put)
            for Ime in ('crt.o', 'aot-runtime.o', 'CLR_Podrška.o', 'Pokreni.o', '미리번역.o', 'vratiti_most.o'):
                odredišna_datoteka = akcija_korijen / 'build/ccompiler' / Ime
                KR_podaci.add(str(odredišna_datoteka), arcname='jkoros-native/relink/' + Ime)
            for Ime in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                KR_podaci.add(str(akcija_korijen / 'build/user' / Ime), arcname='jkoros-native/relink/user/' + Ime)
            KR_podaci.add(str(akcija_korijen / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            KR_podaci.add(str(포직스경로), arcname='posix-kor/arm64-native')
        kompilator_Arhiva.replace(배포경로 / kompilator_Arhiva.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    Pokreni()
