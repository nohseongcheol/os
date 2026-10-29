#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from exekutatu_komando import Project_erro


def Exekutatu_2():
    배포경로 = Project_erro / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = Project_erro.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(Project_erro / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        fitxategi_Zerrenda = {
            Project_erro.parents[1] / 'LICENSE': 'LICENSE',
            Project_erro.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            Project_erro / 'Tresnak/개발꾸러미번역.py': 'compile.py',
            Project_erro / 'erabiltzaile/호출.h': 'include/호출.h',
            Project_erro / '명명/기계연결이름.h': '명명/기계연결이름.h',
            Project_erro / 'erabiltzaile/lotu_diseinu.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            Project_erro / 'build/user/start.o': 'lib/start.o',
            Project_erro / 'build/user/runtime.o': 'lib/runtime.o',
            Project_erro / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            Project_erro / 'erabiltzaile/파일예제.cpp': 'examples/파일예제.cpp',
            Project_erro / '예제/한글코딩/인사.c': 'examples/인사.c',
            Project_erro / '예제/한글코딩/Stream_balio.c': 'examples/Stream_balio.c',
            Project_erro / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            Project_erro / 'erabiltzaile/통신예제.cpp': 'examples/통신예제.cpp',
            Project_erro / 'build/user/demo.elf': 'examples/demo.elf',
            Project_erro / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, helburu_balio in fitxategi_Zerrenda.items():
            helburu_datuak_helbide = 개발꾸러미 / helburu_balio
            helburu_datuak_helbide.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(helburu_datuak_helbide))
            꾸러미명세['sha256'][helburu_balio] = hashlib.sha256(helburu_datuak_helbide.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int HASI_erabiltzaile_aplik(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Tresnak/exekutatu_komando.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Tresnak/exekutatu_fitxategi.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: erabiltzaile_arg_ZENBATU()/erabiltzaile_arg() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        artxibo = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(artxibo), 'w:gz') as neurria_datuak:
            neurria_datuak.add(str(개발꾸러미), arcname=개발꾸러미.name)
        artxibo.replace(배포경로 / artxibo.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as neurria_datuak:
            for Izena in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                neurria_datuak.add(str(Project_erro.parents[1] / Izena), arcname='jkoros-native/' + Izena)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'erabiltzaile', '명명',
                             'Tresnak/시언어번역기빌드.py', 'Tresnak/eraiki_erabiltzaile_gune.py', '파일전송과번역.md'):
                neurria_datuak.add(str(Project_erro / 상대경로), arcname='jkoros-native/' + 상대경로)
            for Izena in ('crt.o', 'aot-runtime.o', '실행지원.o', 'Exekutatu_2.o', '미리번역.o', 'itzuli_zubi.o'):
                helburuko_fitxategi = Project_erro / 'build/ccompiler' / Izena
                neurria_datuak.add(str(helburuko_fitxategi), arcname='jkoros-native/relink/' + Izena)
            for Izena in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                neurria_datuak.add(str(Project_erro / 'build/user' / Izena), arcname='jkoros-native/relink/user/' + Izena)
            neurria_datuak.add(str(Project_erro / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            neurria_datuak.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    Exekutatu_2()
