#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from Vykdyti_komanda import Project_šaknis


def Paleisti():
    paskirstymas_kelias = Project_šaknis / 'dist'
    paskirstymas_kelias.mkdir(exist_ok=True)
    포직스경로 = Project_šaknis.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(Project_šaknis / 'build')) as 작업경로:
        programuotojo_rinkinys = Path(작업경로) / 'jkoros-native-sdk'
        Failas_Sąrašas = {
            Project_šaknis.parents[1] / 'LICENSE': 'LICENSE',
            Project_šaknis.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            Project_šaknis / 'Įrankiai/SDK_kompiliuoti.py': 'compile.py',
            Project_šaknis / 'naudotojas/호출.h': 'include/호출.h',
            Project_šaknis / '명명/기계연결이름.h': '명명/기계연결이름.h',
            Project_šaknis / 'naudotojas/sieti_schema.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            Project_šaknis / 'build/user/start.o': 'lib/start.o',
            Project_šaknis / 'build/user/runtime.o': 'lib/runtime.o',
            Project_šaknis / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            Project_šaknis / 'naudotojas/FailoPavyzdys.cpp': 'examples/FailoPavyzdys.cpp',
            Project_šaknis / '예제/한글코딩/인사.c': 'examples/인사.c',
            Project_šaknis / '예제/한글코딩/Stream_VALUE.c': 'examples/Stream_VALUE.c',
            Project_šaknis / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            Project_šaknis / 'naudotojas/통신예제.cpp': 'examples/통신예제.cpp',
            Project_šaknis / 'build/user/demo.elf': 'examples/demo.elf',
            Project_šaknis / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, tikslas in Failas_Sąrašas.items():
            vieta_duomenys_ADDRESS = programuotojo_rinkinys / tikslas
            vieta_duomenys_ADDRESS.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(vieta_duomenys_ADDRESS))
            꾸러미명세['sha256'][tikslas] = hashlib.sha256(vieta_duomenys_ADDRESS.read_bytes()).hexdigest()
        (programuotojo_rinkinys / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (programuotojo_rinkinys / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/FailoPavyzdys.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int Start_naudotojas_programa(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Įrankiai/Vykdyti_komanda.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Įrankiai/Vykdyti_Failas.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: naudotojas_argumentas_COUNT()/naudotojas_argumentas() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Archyvas = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Archyvas), 'w:gz') as KR_duomenys:
            KR_duomenys.add(str(programuotojo_rinkinys), arcname=programuotojo_rinkinys.name)
        Archyvas.replace(paskirstymas_kelias / Archyvas.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        kompiliatorius_Archyvas = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(kompiliatorius_Archyvas), 'w:gz') as KR_duomenys:
            for Pavadinimas_2 in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                KR_duomenys.add(str(Project_šaknis.parents[1] / Pavadinimas_2), arcname='jkoros-native/' + Pavadinimas_2)
            for santykinis_kelias in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', 'C_kompiliatorius', 'naudotojas', '명명',
                             'Įrankiai/kompiliuoti_C_kompiliatorius.py', 'Įrankiai/kompiliuoti_naudotojas_erdvė.py', '파일전송과번역.md'):
                KR_duomenys.add(str(Project_šaknis / santykinis_kelias), arcname='jkoros-native/' + santykinis_kelias)
            for Pavadinimas_2 in ('crt.o', 'aot-runtime.o', 'CLR_pagalba.o', 'Paleisti.o', '미리번역.o', 'grąžinti_tiltas.o'):
                paskirties_failas = Project_šaknis / 'build/ccompiler' / Pavadinimas_2
                KR_duomenys.add(str(paskirties_failas), arcname='jkoros-native/relink/' + Pavadinimas_2)
            for Pavadinimas_2 in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                KR_duomenys.add(str(Project_šaknis / 'build/user' / Pavadinimas_2), arcname='jkoros-native/relink/user/' + Pavadinimas_2)
            KR_duomenys.add(str(Project_šaknis / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            KR_duomenys.add(str(포직스경로), arcname='posix-kor/arm64-native')
        kompiliatorius_Archyvas.replace(paskirstymas_kelias / kompiliatorius_Archyvas.name)
    print('SDK:', paskirstymas_kelias / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    Paleisti()
