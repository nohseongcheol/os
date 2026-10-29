#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from Izvedi_ukaz import pobuda_koren


def Zaženi():
    배포경로 = pobuda_koren / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = pobuda_koren.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(pobuda_koren / 'build')) as 작업경로:
        razvijalski_komplet = Path(작업경로) / 'jkoros-native-sdk'
        Datoteka_Seznam = {
            pobuda_koren.parents[1] / 'LICENSE': 'LICENSE',
            pobuda_koren.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            pobuda_koren / 'Orodja/komplet_za_razvoj_programske_opreme_prevajati.py': 'compile.py',
            pobuda_koren / 'uporabnik/호출.h': 'include/호출.h',
            pobuda_koren / '명명/기계연결이름.h': '명명/기계연결이름.h',
            pobuda_koren / 'uporabnik/Povezava_Krmarjenje.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            pobuda_koren / 'build/user/start.o': 'lib/start.o',
            pobuda_koren / 'build/user/runtime.o': 'lib/runtime.o',
            pobuda_koren / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            pobuda_koren / 'uporabnik/PrimerDatoteke.cpp': 'examples/PrimerDatoteke.cpp',
            pobuda_koren / '예제/한글코딩/인사.c': 'examples/인사.c',
            pobuda_koren / '예제/한글코딩/tok_VALUE.c': 'examples/tok_VALUE.c',
            pobuda_koren / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            pobuda_koren / 'uporabnik/통신예제.cpp': 'examples/통신예제.cpp',
            pobuda_koren / 'build/user/demo.elf': 'examples/demo.elf',
            pobuda_koren / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, tarča in Datoteka_Seznam.items():
            cilj_podatki_naslov = razvijalski_komplet / tarča
            cilj_podatki_naslov.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(cilj_podatki_naslov))
            꾸러미명세['sha256'][tarča] = hashlib.sha256(cilj_podatki_naslov.read_bytes()).hexdigest()
        (razvijalski_komplet / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (razvijalski_komplet / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/PrimerDatoteke.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int Start_uporabnik_aplikacija(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Orodja/Izvedi_ukaz.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Orodja/Izvedi_Datoteka.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: uporabnik_argument_COUNT()/uporabnik_argument() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Arhiv = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Arhiv), 'w:gz') as KR_podatki:
            KR_podatki.add(str(razvijalski_komplet), arcname=razvijalski_komplet.name)
        Arhiv.replace(배포경로 / Arhiv.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        prevajalnik_Arhiv = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(prevajalnik_Arhiv), 'w:gz') as KR_podatki:
            for Ime in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                KR_podatki.add(str(pobuda_koren.parents[1] / Ime), arcname='jkoros-native/' + Ime)
            for relativna_pot in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', 'C_prevajalnik', 'uporabnik', '명명',
                             'Orodja/graditev_C_prevajalnik.py', 'Orodja/graditev_uporabnik_Space.py', '파일전송과번역.md'):
                KR_podatki.add(str(pobuda_koren / relativna_pot), arcname='jkoros-native/' + relativna_pot)
            for Ime in ('crt.o', 'aot-runtime.o', 'skupni_jezikovni_izvajalnik_Podpora.o', 'Zaženi.o', '미리번역.o', 'vrni_most.o'):
                ciljna_datoteka = pobuda_koren / 'build/ccompiler' / Ime
                KR_podatki.add(str(ciljna_datoteka), arcname='jkoros-native/relink/' + Ime)
            for Ime in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                KR_podatki.add(str(pobuda_koren / 'build/user' / Ime), arcname='jkoros-native/relink/user/' + Ime)
            KR_podatki.add(str(pobuda_koren / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            KR_podatki.add(str(포직스경로), arcname='posix-kor/arm64-native')
        prevajalnik_Arhiv.replace(배포경로 / prevajalnik_Arhiv.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    Zaženi()
