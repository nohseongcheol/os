#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from keyra_skipun import verk_rót


def Keyra_2():
    dreifing_slóð = verk_rót / 'dist'
    dreifing_slóð.mkdir(exist_ok=True)
    포직스경로 = verk_rót.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(verk_rót / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        skrá_Listi = {
            verk_rót.parents[1] / 'LICENSE': 'LICENSE',
            verk_rót.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            verk_rót / 'Verkfæri/개발꾸러미번역.py': 'compile.py',
            verk_rót / 'notandi/호출.h': 'include/호출.h',
            verk_rót / '명명/기계연결이름.h': '명명/기계연결이름.h',
            verk_rót / 'notandi/tengja_útlit.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            verk_rót / 'build/user/start.o': 'lib/start.o',
            verk_rót / 'build/user/runtime.o': 'lib/runtime.o',
            verk_rót / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            verk_rót / 'notandi/Skráardæmi.cpp': 'examples/Skráardæmi.cpp',
            verk_rót / '예제/한글코딩/인사.c': 'examples/인사.c',
            verk_rót / '예제/한글코딩/Stream_VALUE.c': 'examples/Stream_VALUE.c',
            verk_rót / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            verk_rót / 'notandi/통신예제.cpp': 'examples/통신예제.cpp',
            verk_rót / 'build/user/demo.elf': 'examples/demo.elf',
            verk_rót / 'build/user/network.elf': 'examples/network.elf',
        }
        búnt_skrá = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, markmið in skrá_Listi.items():
            endastaður_gögn_slóð = 개발꾸러미 / markmið
            endastaður_gögn_slóð.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(endastaður_gögn_slóð))
            búnt_skrá['sha256'][markmið] = hashlib.sha256(endastaður_gögn_slóð.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(búnt_skrá, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/Skráardæmi.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int Opna_notandi_forrit(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Verkfæri/keyra_skipun.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Verkfæri/keyra_skrá.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: notandi_frumbreyta_COUNT()/notandi_frumbreyta() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Safn = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Safn), 'w:gz') as mæld_stærð_gögn:
            mæld_stærð_gögn.add(str(개발꾸러미), arcname=개발꾸러미.name)
        Safn.replace(dreifing_slóð / Safn.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as mæld_stærð_gögn:
            for Heiti in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                mæld_stærð_gögn.add(str(verk_rót.parents[1] / Heiti), arcname='jkoros-native/' + Heiti)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'notandi', '명명',
                             'Verkfæri/시언어번역기빌드.py', 'Verkfæri/smíð_notandi_svæði.py', '파일전송과번역.md'):
                mæld_stærð_gögn.add(str(verk_rót / 상대경로), arcname='jkoros-native/' + 상대경로)
            for Heiti in ('crt.o', 'aot-runtime.o', 'CLR_Aðstoð.o', 'Keyra_2.o', '미리번역.o', 'skila_brú.o'):
                viðtökuskrá = verk_rót / 'build/ccompiler' / Heiti
                mæld_stærð_gögn.add(str(viðtökuskrá), arcname='jkoros-native/relink/' + Heiti)
            for Heiti in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                mæld_stærð_gögn.add(str(verk_rót / 'build/user' / Heiti), arcname='jkoros-native/relink/user/' + Heiti)
            mæld_stærð_gögn.add(str(verk_rót / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            mæld_stærð_gögn.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(dreifing_slóð / 번역기꾸러미.name)
    print('SDK:', dreifing_slóð / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    Keyra_2()
