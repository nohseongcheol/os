#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from Wykonaj_polecenie import Project_korzeń


def Uruchom_2():
    dystrybucja_ścieżka = Project_korzeń / 'dist'
    dystrybucja_ścieżka.mkdir(exist_ok=True)
    포직스경로 = Project_korzeń.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(Project_korzeń / 'build')) as 작업경로:
        zestaw_deweloperski = Path(작업경로) / 'jkoros-native-sdk'
        lista_plików = {
            Project_korzeń.parents[1] / 'LICENSE': 'LICENSE',
            Project_korzeń.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            Project_korzeń / 'narzędzia/SDK_kompilować.py': 'compile.py',
            Project_korzeń / 'przestrzeń_użytkownika/호출.h': 'include/호출.h',
            Project_korzeń / '명명/기계연결이름.h': '명명/기계연결이름.h',
            Project_korzeń / 'przestrzeń_użytkownika/układ_konsolidacji.ld': 'user.ld',
            포직스경로 / 'deklaracje/Plik_ABI.h': 'include/Plik_ABI.h',
            포직스경로 / 'deklaracje/sieć_ABI.h': 'include/sieć_ABI.h',
            Project_korzeń / 'build/user/start.o': 'lib/start.o',
            Project_korzeń / 'build/user/runtime.o': 'lib/runtime.o',
            Project_korzeń / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            Project_korzeń / 'przestrzeń_użytkownika/PrzykładPliku.cpp': 'examples/PrzykładPliku.cpp',
            Project_korzeń / '예제/한글코딩/인사.c': 'examples/인사.c',
            Project_korzeń / '예제/한글코딩/Stream_WARTOŚĆ.c': 'examples/Stream_WARTOŚĆ.c',
            Project_korzeń / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            Project_korzeń / 'przestrzeń_użytkownika/통신예제.cpp': 'examples/통신예제.cpp',
            Project_korzeń / 'build/user/demo.elf': 'examples/demo.elf',
            Project_korzeń / 'build/user/network.elf': 'examples/network.elf',
        }
        pakiet_manifest = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, wartość_docelowa in lista_plików.items():
            cel_dane_ADRES = zestaw_deweloperski / wartość_docelowa
            cel_dane_ADRES.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(cel_dane_ADRES))
            pakiet_manifest['sha256'][wartość_docelowa] = hashlib.sha256(cel_dane_ADRES.read_bytes()).hexdigest()
        (zestaw_deweloperski / 'manifest.json').write_text(json.dumps(pakiet_manifest, indent=2) + '\n')
        (zestaw_deweloperski / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/PrzykładPliku.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int START_użytkownik_program(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: narzędzia/Wykonaj_polecenie.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 narzędzia/Wykonaj_Plik.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: użytkownik_argument_ILE_LICZB()/użytkownik_argument() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Archiwum = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Archiwum), 'w:gz') as KR_dane:
            KR_dane.add(str(zestaw_deweloperski), arcname=zestaw_deweloperski.name)
        Archiwum.replace(dystrybucja_ścieżka / Archiwum.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        kompilator_Archiwum = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(kompilator_Archiwum), 'w:gz') as KR_dane:
            for Nazwa in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                KR_dane.add(str(Project_korzeń.parents[1] / Nazwa), arcname='jkoros-native/' + Nazwa)
            for ścieżka_względna in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', 'C_kompilator', 'przestrzeń_użytkownika', '명명',
                             'narzędzia/BLD_C_kompilator.py', 'narzędzia/BLD_użytkownik_SPACJA.py', '파일전송과번역.md'):
                KR_dane.add(str(Project_korzeń / ścieżka_względna), arcname='jkoros-native/' + ścieżka_względna)
            for Nazwa in ('crt.o', 'aot-runtime.o', 'CLR_wsparcie.o', 'Uruchom_2.o', '미리번역.o', 'Zwrot_mostek.o'):
                plik_docelowy = Project_korzeń / 'build/ccompiler' / Nazwa
                KR_dane.add(str(plik_docelowy), arcname='jkoros-native/relink/' + Nazwa)
            for Nazwa in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                KR_dane.add(str(Project_korzeń / 'build/user' / Nazwa), arcname='jkoros-native/relink/user/' + Nazwa)
            KR_dane.add(str(Project_korzeń / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            KR_dane.add(str(포직스경로), arcname='posix-kor/arm64-native')
        kompilator_Archiwum.replace(dystrybucja_ścieżka / kompilator_Archiwum.name)
    print('SDK:', dystrybucja_ścieżka / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    Uruchom_2()
