#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from Izvrši_komanda import projicirati_koijen


def Pokreni():
    배포경로 = projicirati_koijen / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = projicirati_koijen.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(projicirati_koijen / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        fajl_spisak = {
            projicirati_koijen.parents[1] / 'LICENSE': 'LICENSE',
            projicirati_koijen.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            projicirati_koijen / 'Alati/SDK_napraviti.py': 'compile.py',
            projicirati_koijen / 'korisnik/호출.h': 'include/호출.h',
            projicirati_koijen / '명명/기계연결이름.h': '명명/기계연결이름.h',
            projicirati_koijen / 'korisnik/Veza_izgled.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            projicirati_koijen / 'build/user/start.o': 'lib/start.o',
            projicirati_koijen / 'build/user/runtime.o': 'lib/runtime.o',
            projicirati_koijen / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            projicirati_koijen / 'korisnik/파일예제.cpp': 'examples/파일예제.cpp',
            projicirati_koijen / '예제/한글코딩/인사.c': 'examples/인사.c',
            projicirati_koijen / '예제/한글코딩/tok_VALUE.c': 'examples/tok_VALUE.c',
            projicirati_koijen / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            projicirati_koijen / 'korisnik/통신예제.cpp': 'examples/통신예제.cpp',
            projicirati_koijen / 'build/user/demo.elf': 'examples/demo.elf',
            projicirati_koijen / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, cilj in fajl_spisak.items():
            odredište_podaci_adresa = 개발꾸러미 / cilj
            odredište_podaci_adresa.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(odredište_podaci_adresa))
            꾸러미명세['sha256'][cilj] = hashlib.sha256(odredište_podaci_adresa.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int START_korisnik_program(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Alati/Izvrši_komanda.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Alati/Izvrši_fajl.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: korisnik_argument_COUNT()/korisnik_argument() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Arhiva = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Arhiva), 'w:gz') as mjera_podaci:
            mjera_podaci.add(str(개발꾸러미), arcname=개발꾸러미.name)
        Arhiva.replace(배포경로 / Arhiva.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as mjera_podaci:
            for Naziv in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                mjera_podaci.add(str(projicirati_koijen.parents[1] / Naziv), arcname='jkoros-native/' + Naziv)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'korisnik', '명명',
                             'Alati/시언어번역기빌드.py', 'Alati/verzija_korisnik_prostor.py', '파일전송과번역.md'):
                mjera_podaci.add(str(projicirati_koijen / 상대경로), arcname='jkoros-native/' + 상대경로)
            for Naziv in ('crt.o', 'aot-runtime.o', 'zajednička_jezička_biblioteka_Podrška.o', 'Pokreni.o', '미리번역.o', 'vratiti_most.o'):
                odredišni_fajl = projicirati_koijen / 'build/ccompiler' / Naziv
                mjera_podaci.add(str(odredišni_fajl), arcname='jkoros-native/relink/' + Naziv)
            for Naziv in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                mjera_podaci.add(str(projicirati_koijen / 'build/user' / Naziv), arcname='jkoros-native/relink/user/' + Naziv)
            mjera_podaci.add(str(projicirati_koijen / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            mjera_podaci.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    Pokreni()
