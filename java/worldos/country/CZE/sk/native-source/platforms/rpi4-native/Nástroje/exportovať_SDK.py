#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from Vykonať_príkaz import akcia_koreň


def Spustiť_2():
    배포경로 = akcia_koreň / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = akcia_koreň.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(akcia_koreň / 'build')) as 작업경로:
        Development_Kit = Path(작업경로) / 'jkoros-native-sdk'
        Súbor_Zoznam = {
            akcia_koreň.parents[1] / 'LICENSE': 'LICENSE',
            akcia_koreň.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            akcia_koreň / 'Nástroje/SDK_kompilovať.py': 'compile.py',
            akcia_koreň / 'používateľ/호출.h': 'include/호출.h',
            akcia_koreň / '명명/기계연결이름.h': '명명/기계연결이름.h',
            akcia_koreň / 'používateľ/odkaz_Navigácia.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            akcia_koreň / 'build/user/start.o': 'lib/start.o',
            akcia_koreň / 'build/user/runtime.o': 'lib/runtime.o',
            akcia_koreň / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            akcia_koreň / 'používateľ/UkážkaSúboru.cpp': 'examples/UkážkaSúboru.cpp',
            akcia_koreň / '예제/한글코딩/인사.c': 'examples/인사.c',
            akcia_koreň / '예제/한글코딩/Stream_VALUE.c': 'examples/Stream_VALUE.c',
            akcia_koreň / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            akcia_koreň / 'používateľ/통신예제.cpp': 'examples/통신예제.cpp',
            akcia_koreň / 'build/user/demo.elf': 'examples/demo.elf',
            akcia_koreň / 'build/user/network.elf': 'examples/network.elf',
        }
        zväzok_manifest_zostáv = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, cieľová_hodnota in Súbor_Zoznam.items():
            cieľ_údaje_adresa = Development_Kit / cieľová_hodnota
            cieľ_údaje_adresa.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(cieľ_údaje_adresa))
            zväzok_manifest_zostáv['sha256'][cieľová_hodnota] = hashlib.sha256(cieľ_údaje_adresa.read_bytes()).hexdigest()
        (Development_Kit / 'manifest.json').write_text(json.dumps(zväzok_manifest_zostáv, indent=2) + '\n')
        (Development_Kit / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/UkážkaSúboru.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int START_používateľ_program(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Nástroje/Vykonať_príkaz.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Nástroje/Vykonať_Súbor.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: používateľ_argument_COUNT()/používateľ_argument() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Archív = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Archív), 'w:gz') as KR_údaje:
            KR_údaje.add(str(Development_Kit), arcname=Development_Kit.name)
        Archív.replace(배포경로 / Archív.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        kompilátor_Archív = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(kompilátor_Archív), 'w:gz') as KR_údaje:
            for Názov in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                KR_údaje.add(str(akcia_koreň.parents[1] / Názov), arcname='jkoros-native/' + Názov)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', 'C_kompilátor', 'používateľ', '명명',
                             'Nástroje/zostava_C_kompilátor.py', 'Nástroje/zostava_používateľ_priestor.py', '파일전송과번역.md'):
                KR_údaje.add(str(akcia_koreň / 상대경로), arcname='jkoros-native/' + 상대경로)
            for Názov in ('crt.o', 'aot-runtime.o', 'CLR_Podpora.o', 'Spustiť_2.o', '미리번역.o', 'vrátiť_most.o'):
                cieľový_súbor = akcia_koreň / 'build/ccompiler' / Názov
                KR_údaje.add(str(cieľový_súbor), arcname='jkoros-native/relink/' + Názov)
            for Názov in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                KR_údaje.add(str(akcia_koreň / 'build/user' / Názov), arcname='jkoros-native/relink/user/' + Názov)
            KR_údaje.add(str(akcia_koreň / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            KR_údaje.add(str(포직스경로), arcname='posix-kor/arm64-native')
        kompilátor_Archív.replace(배포경로 / kompilátor_Archív.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    Spustiť_2()
