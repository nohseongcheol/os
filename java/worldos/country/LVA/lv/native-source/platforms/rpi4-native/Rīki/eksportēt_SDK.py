#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from Izpildīt_komanda import Project_sakne


def Palaist():
    sadale_ceļš = Project_sakne / 'dist'
    sadale_ceļš.mkdir(exist_ok=True)
    포직스경로 = Project_sakne.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(Project_sakne / 'build')) as 작업경로:
        programmizstrādes_komplekts = Path(작업경로) / 'jkoros-native-sdk'
        Fails_Saraksts = {
            Project_sakne.parents[1] / 'LICENSE': 'LICENSE',
            Project_sakne.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            Project_sakne / 'Rīki/SDK_kompilēt.py': 'compile.py',
            Project_sakne / 'lietotājs/호출.h': 'include/호출.h',
            Project_sakne / '명명/기계연결이름.h': '명명/기계연결이름.h',
            Project_sakne / 'lietotājs/Saite_shēma.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            Project_sakne / 'build/user/start.o': 'lib/start.o',
            Project_sakne / 'build/user/runtime.o': 'lib/runtime.o',
            Project_sakne / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            Project_sakne / 'lietotājs/DatnesPiemērs.cpp': 'examples/DatnesPiemērs.cpp',
            Project_sakne / '예제/한글코딩/인사.c': 'examples/인사.c',
            Project_sakne / '예제/한글코딩/Stream_VALUE.c': 'examples/Stream_VALUE.c',
            Project_sakne / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            Project_sakne / 'lietotājs/통신예제.cpp': 'examples/통신예제.cpp',
            Project_sakne / 'build/user/demo.elf': 'examples/demo.elf',
            Project_sakne / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, mērķis in Fails_Saraksts.items():
            mērķis_dati_adrese = programmizstrādes_komplekts / mērķis
            mērķis_dati_adrese.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(mērķis_dati_adrese))
            꾸러미명세['sha256'][mērķis] = hashlib.sha256(mērķis_dati_adrese.read_bytes()).hexdigest()
        (programmizstrādes_komplekts / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (programmizstrādes_komplekts / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/DatnesPiemērs.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int Sākt_lietotājs_programma(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Rīki/Izpildīt_komanda.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Rīki/Izpildīt_Fails.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: lietotājs_arg_COUNT()/lietotājs_arg() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Arhīvs = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Arhīvs), 'w:gz') as mērs_dati:
            mērs_dati.add(str(programmizstrādes_komplekts), arcname=programmizstrādes_komplekts.name)
        Arhīvs.replace(sadale_ceļš / Arhīvs.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        kompilators_Arhīvs = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(kompilators_Arhīvs), 'w:gz') as mērs_dati:
            for Nosaukums in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                mērs_dati.add(str(Project_sakne.parents[1] / Nosaukums), arcname='jkoros-native/' + Nosaukums)
            for relatīvais_ceļš in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', 'C_kompilators', 'lietotājs', '명명',
                             'Rīki/būvējums_C_kompilators.py', 'Rīki/būvējums_lietotājs_telpa.py', '파일전송과번역.md'):
                mērs_dati.add(str(Project_sakne / relatīvais_ceļš), arcname='jkoros-native/' + relatīvais_ceļš)
            for Nosaukums in ('crt.o', 'aot-runtime.o', 'CLR_Atbalsts.o', 'Palaist.o', '미리번역.o', 'atdot_tilts.o'):
                mērķa_fails = Project_sakne / 'build/ccompiler' / Nosaukums
                mērs_dati.add(str(mērķa_fails), arcname='jkoros-native/relink/' + Nosaukums)
            for Nosaukums in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                mērs_dati.add(str(Project_sakne / 'build/user' / Nosaukums), arcname='jkoros-native/relink/user/' + Nosaukums)
            mērs_dati.add(str(Project_sakne / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            mērs_dati.add(str(포직스경로), arcname='posix-kor/arm64-native')
        kompilators_Arhīvs.replace(sadale_ceļš / kompilators_Arhīvs.name)
    print('SDK:', sadale_ceļš / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    Palaist()
