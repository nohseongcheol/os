#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from Suorita_komento import aloite_juuri


def Suorita_2():
    jakelu_polku = aloite_juuri / 'dist'
    jakelu_polku.mkdir(exist_ok=True)
    포직스경로 = aloite_juuri.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(aloite_juuri / 'build')) as 작업경로:
        ohjelmankehityspaketti = Path(작업경로) / 'jkoros-native-sdk'
        tiedostoluettelo = {
            aloite_juuri.parents[1] / 'LICENSE': 'LICENSE',
            aloite_juuri.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            aloite_juuri / 'työkalut/SDK_kääntää.py': 'compile.py',
            aloite_juuri / 'käyttäjätila/호출.h': 'include/호출.h',
            aloite_juuri / '명명/기계연결이름.h': '명명/기계연결이름.h',
            aloite_juuri / 'käyttäjätila/linkitysasettelu.ld': 'user.ld',
            포직스경로 / 'esittelyt/파일규약.h': 'include/파일규약.h',
            포직스경로 / 'esittelyt/통신규약.h': 'include/통신규약.h',
            aloite_juuri / 'build/user/start.o': 'lib/start.o',
            aloite_juuri / 'build/user/runtime.o': 'lib/runtime.o',
            aloite_juuri / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            aloite_juuri / 'käyttäjätila/Tiedostoesimerkki.cpp': 'examples/Tiedostoesimerkki.cpp',
            aloite_juuri / '예제/한글코딩/인사.c': 'examples/인사.c',
            aloite_juuri / '예제/한글코딩/virta_ARVO.c': 'examples/virta_ARVO.c',
            aloite_juuri / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            aloite_juuri / 'käyttäjätila/통신예제.cpp': 'examples/통신예제.cpp',
            aloite_juuri / 'build/user/demo.elf': 'examples/demo.elf',
            aloite_juuri / 'build/user/network.elf': 'examples/network.elf',
        }
        nippu_kokoonpanotiedot = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, tavoite in tiedostoluettelo.items():
            kohde_data_OSOITE = ohjelmankehityspaketti / tavoite
            kohde_data_OSOITE.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(kohde_data_OSOITE))
            nippu_kokoonpanotiedot['sha256'][tavoite] = hashlib.sha256(kohde_data_OSOITE.read_bytes()).hexdigest()
        (ohjelmankehityspaketti / 'manifest.json').write_text(json.dumps(nippu_kokoonpanotiedot, indent=2) + '\n')
        (ohjelmankehityspaketti / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/Tiedostoesimerkki.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int alku_käyttäjä_ohjelma(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: työkalut/Suorita_komento.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 työkalut/Suorita_Tiedosto.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: käyttäjä_argumentti_LASKE()/käyttäjä_argumentti() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Arkisto = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Arkisto), 'w:gz') as KR_data:
            KR_data.add(str(ohjelmankehityspaketti), arcname=ohjelmankehityspaketti.name)
        Arkisto.replace(jakelu_polku / Arkisto.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        kääntäjä_Arkisto = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(kääntäjä_Arkisto), 'w:gz') as KR_data:
            for Nimi in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                KR_data.add(str(aloite_juuri.parents[1] / Nimi), arcname='jkoros-native/' + Nimi)
            for suhteellinen_polku in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', 'C_kääntäjä', 'käyttäjätila', '명명',
                             'työkalut/kääntää_C_kääntäjä.py', 'työkalut/kääntää_käyttäjä_tila.py', '파일전송과번역.md'):
                KR_data.add(str(aloite_juuri / suhteellinen_polku), arcname='jkoros-native/' + suhteellinen_polku)
            for Nimi in ('crt.o', 'aot-runtime.o', 'CLR_Tuki.o', 'Suorita_2.o', '미리번역.o', 'palauttaa_silta.o'):
                kohdetiedosto = aloite_juuri / 'build/ccompiler' / Nimi
                KR_data.add(str(kohdetiedosto), arcname='jkoros-native/relink/' + Nimi)
            for Nimi in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                KR_data.add(str(aloite_juuri / 'build/user' / Nimi), arcname='jkoros-native/relink/user/' + Nimi)
            KR_data.add(str(aloite_juuri / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            KR_data.add(str(포직스경로), arcname='posix-kor/arm64-native')
        kääntäjä_Arkisto.replace(jakelu_polku / kääntäjä_Arkisto.name)
    print('SDK:', jakelu_polku / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    Suorita_2()
