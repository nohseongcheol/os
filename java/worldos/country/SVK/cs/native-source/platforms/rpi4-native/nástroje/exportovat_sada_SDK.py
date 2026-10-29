#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from Provést_příkaz import akce_kořen


def Spustit_2():
    distribuce_cesta = akce_kořen / 'dist'
    distribuce_cesta.mkdir(exist_ok=True)
    포직스경로 = akce_kořen.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(akce_kořen / 'build')) as 작업경로:
        Development_Kit = Path(작업경로) / 'jkoros-native-sdk'
        seznam_souborů = {
            akce_kořen.parents[1] / 'LICENSE': 'LICENSE',
            akce_kořen.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            akce_kořen / 'nástroje/sada_SDK_kompilovat.py': 'compile.py',
            akce_kořen / 'uživatelský_prostor/호출.h': 'include/호출.h',
            akce_kořen / '명명/기계연결이름.h': '명명/기계연결이름.h',
            akce_kořen / 'uživatelský_prostor/rozvržení_spojování.ld': 'user.ld',
            포직스경로 / 'deklarace/Soubor_ABI.h': 'include/Soubor_ABI.h',
            포직스경로 / 'deklarace/síť_ABI.h': 'include/síť_ABI.h',
            akce_kořen / 'build/user/start.o': 'lib/start.o',
            akce_kořen / 'build/user/runtime.o': 'lib/runtime.o',
            akce_kořen / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            akce_kořen / 'uživatelský_prostor/UkázkaSouboru.cpp': 'examples/UkázkaSouboru.cpp',
            akce_kořen / '예제/한글코딩/인사.c': 'examples/인사.c',
            akce_kořen / '예제/한글코딩/tok_HODNOTA.c': 'examples/tok_HODNOTA.c',
            akce_kořen / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            akce_kořen / 'uživatelský_prostor/통신예제.cpp': 'examples/통신예제.cpp',
            akce_kořen / 'build/user/demo.elf': 'examples/demo.elf',
            akce_kořen / 'build/user/network.elf': 'examples/network.elf',
        }
        sada_manifest = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, cílová_úroveň in seznam_souborů.items():
            cíl_data_ODKAZ = Development_Kit / cílová_úroveň
            cíl_data_ODKAZ.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(cíl_data_ODKAZ))
            sada_manifest['sha256'][cílová_úroveň] = hashlib.sha256(cíl_data_ODKAZ.read_bytes()).hexdigest()
        (Development_Kit / 'manifest.json').write_text(json.dumps(sada_manifest, indent=2) + '\n')
        (Development_Kit / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/UkázkaSouboru.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int START_uživatel_program(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: nástroje/Provést_příkaz.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 nástroje/Provést_Soubor.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: uživatel_argument_POČET()/uživatel_argument() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Archiv = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Archiv), 'w:gz') as KV_data:
            KV_data.add(str(Development_Kit), arcname=Development_Kit.name)
        Archiv.replace(distribuce_cesta / Archiv.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        kompilátor_Archiv = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(kompilátor_Archiv), 'w:gz') as KV_data:
            for Název in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                KV_data.add(str(akce_kořen.parents[1] / Název), arcname='jkoros-native/' + Název)
            for relativní_cesta in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', 'C_kompilátor', 'uživatelský_prostor', '명명',
                             'nástroje/BLD_C_kompilátor.py', 'nástroje/BLD_uživatel_Space.py', '파일전송과번역.md'):
                KV_data.add(str(akce_kořen / relativní_cesta), arcname='jkoros-native/' + relativní_cesta)
            for Název in ('crt.o', 'aot-runtime.o', 'CLR_vzpěra.o', 'Spustit_2.o', '미리번역.o', 'Vratka_most.o'):
                cílový_soubor = akce_kořen / 'build/ccompiler' / Název
                KV_data.add(str(cílový_soubor), arcname='jkoros-native/relink/' + Název)
            for Název in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                KV_data.add(str(akce_kořen / 'build/user' / Název), arcname='jkoros-native/relink/user/' + Název)
            KV_data.add(str(akce_kořen / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            KV_data.add(str(포직스경로), arcname='posix-kor/arm64-native')
        kompilátor_Archiv.replace(distribuce_cesta / kompilátor_Archiv.name)
    print('SDK:', distribuce_cesta / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    Spustit_2()
