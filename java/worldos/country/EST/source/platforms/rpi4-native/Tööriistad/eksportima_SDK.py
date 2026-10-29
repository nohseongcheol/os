#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from Täida_käsk import Project_juur


def Käivita_2():
    turustus_tee = Project_juur / 'dist'
    turustus_tee.mkdir(exist_ok=True)
    포직스경로 = Project_juur.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(Project_juur / 'build')) as 작업경로:
        arenduskomplekt = Path(작업경로) / 'jkoros-native-sdk'
        Fail_Loend = {
            Project_juur.parents[1] / 'LICENSE': 'LICENSE',
            Project_juur.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            Project_juur / 'Tööriistad/SDK_kompileerima.py': 'compile.py',
            Project_juur / 'kasutaja/호출.h': 'include/호출.h',
            Project_juur / '명명/기계연결이름.h': '명명/기계연결이름.h',
            Project_juur / 'kasutaja/Link_küljend.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            Project_juur / 'build/user/start.o': 'lib/start.o',
            Project_juur / 'build/user/runtime.o': 'lib/runtime.o',
            Project_juur / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            Project_juur / 'kasutaja/FailiNäide.cpp': 'examples/FailiNäide.cpp',
            Project_juur / '예제/한글코딩/인사.c': 'examples/인사.c',
            Project_juur / '예제/한글코딩/voog_VALUE.c': 'examples/voog_VALUE.c',
            Project_juur / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            Project_juur / 'kasutaja/통신예제.cpp': 'examples/통신예제.cpp',
            Project_juur / 'build/user/demo.elf': 'examples/demo.elf',
            Project_juur / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, siht in Fail_Loend.items():
            sihtkoht_andmed_ADDRESS = arenduskomplekt / siht
            sihtkoht_andmed_ADDRESS.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(sihtkoht_andmed_ADDRESS))
            꾸러미명세['sha256'][siht] = hashlib.sha256(sihtkoht_andmed_ADDRESS.read_bytes()).hexdigest()
        (arenduskomplekt / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (arenduskomplekt / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/FailiNäide.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int START_kasutaja_programm(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Tööriistad/Täida_käsk.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Tööriistad/Täida_Fail.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: kasutaja_argument_COUNT()/kasutaja_argument() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Arhiiv = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Arhiiv), 'w:gz') as näitaja_andmed:
            näitaja_andmed.add(str(arenduskomplekt), arcname=arenduskomplekt.name)
        Arhiiv.replace(turustus_tee / Arhiiv.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        kompilaator_Arhiiv = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(kompilaator_Arhiiv), 'w:gz') as näitaja_andmed:
            for Nimi_2 in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                näitaja_andmed.add(str(Project_juur.parents[1] / Nimi_2), arcname='jkoros-native/' + Nimi_2)
            for suhteline_tee in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '_15_kompilaator', 'kasutaja', '명명',
                             'Tööriistad/järk_15_kompilaator.py', 'Tööriistad/järk_kasutaja_ruum.py', '파일전송과번역.md'):
                näitaja_andmed.add(str(Project_juur / suhteline_tee), arcname='jkoros-native/' + suhteline_tee)
            for Nimi_2 in ('crt.o', 'aot-runtime.o', 'CLR_tugi.o', 'Käivita_2.o', '미리번역.o', 'tagasi_saatma_sild.o'):
                sihtfail = Project_juur / 'build/ccompiler' / Nimi_2
                näitaja_andmed.add(str(sihtfail), arcname='jkoros-native/relink/' + Nimi_2)
            for Nimi_2 in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                näitaja_andmed.add(str(Project_juur / 'build/user' / Nimi_2), arcname='jkoros-native/relink/user/' + Nimi_2)
            näitaja_andmed.add(str(Project_juur / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            näitaja_andmed.add(str(포직스경로), arcname='posix-kor/arm64-native')
        kompilaator_Arhiiv.replace(turustus_tee / kompilaator_Arhiiv.name)
    print('SDK:', turustus_tee / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    Käivita_2()
