#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from kawe_tono import whakaatu_pūtake


def whakahaere():
    배포경로 = whakaatu_pūtake / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = whakaatu_pūtake.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(whakaatu_pūtake / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        kōnae_Rārangi = {
            whakaatu_pūtake.parents[1] / 'LICENSE': 'LICENSE',
            whakaatu_pūtake.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            whakaatu_pūtake / 'Ngā_Utauta/개발꾸러미번역.py': 'compile.py',
            whakaatu_pūtake / 'kaiwhakamahi/호출.h': 'include/호출.h',
            whakaatu_pūtake / '명명/기계연결이름.h': '명명/기계연결이름.h',
            whakaatu_pūtake / 'kaiwhakamahi/Hono_Tahora.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            whakaatu_pūtake / 'build/user/start.o': 'lib/start.o',
            whakaatu_pūtake / 'build/user/runtime.o': 'lib/runtime.o',
            whakaatu_pūtake / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            whakaatu_pūtake / 'kaiwhakamahi/파일예제.cpp': 'examples/파일예제.cpp',
            whakaatu_pūtake / '예제/한글코딩/인사.c': 'examples/인사.c',
            whakaatu_pūtake / '예제/한글코딩/roma_uara.c': 'examples/roma_uara.c',
            whakaatu_pūtake / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            whakaatu_pūtake / 'kaiwhakamahi/통신예제.cpp': 'examples/통신예제.cpp',
            whakaatu_pūtake / 'build/user/demo.elf': 'examples/demo.elf',
            whakaatu_pūtake / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, ūnga in kōnae_Rārangi.items():
            ūnga_raraunga_ADDRESS = 개발꾸러미 / ūnga
            ūnga_raraunga_ADDRESS.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(ūnga_raraunga_ADDRESS))
            꾸러미명세['sha256'][ūnga] = hashlib.sha256(ūnga_raraunga_ADDRESS.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int Start_kaiwhakamahi_kaupapa(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Ngā_Utauta/kawe_tono.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Ngā_Utauta/kawe_kōnae.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: kaiwhakamahi_tohenga_COUNT()/kaiwhakamahi_tohenga() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Pūranga = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Pūranga), 'w:gz') as mēhua_raraunga:
            mēhua_raraunga.add(str(개발꾸러미), arcname=개발꾸러미.name)
        Pūranga.replace(배포경로 / Pūranga.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as mēhua_raraunga:
            for Ingoa in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                mēhua_raraunga.add(str(whakaatu_pūtake.parents[1] / Ingoa), arcname='jkoros-native/' + Ingoa)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'kaiwhakamahi', '명명',
                             'Ngā_Utauta/시언어번역기빌드.py', 'Ngā_Utauta/hanga_kaiwhakamahi_wāhi.py', '파일전송과번역.md'):
                mēhua_raraunga.add(str(whakaatu_pūtake / 상대경로), arcname='jkoros-native/' + 상대경로)
            for Ingoa in ('crt.o', 'aot-runtime.o', 'wāhaere_reo_noa_Tautoko.o', 'whakahaere.o', '미리번역.o', '되돌림.o'):
                kōnae_ūnga_ffac9b48 = whakaatu_pūtake / 'build/ccompiler' / Ingoa
                mēhua_raraunga.add(str(kōnae_ūnga_ffac9b48), arcname='jkoros-native/relink/' + Ingoa)
            for Ingoa in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                mēhua_raraunga.add(str(whakaatu_pūtake / 'build/user' / Ingoa), arcname='jkoros-native/relink/user/' + Ingoa)
            mēhua_raraunga.add(str(whakaatu_pūtake / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            mēhua_raraunga.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    whakahaere()
