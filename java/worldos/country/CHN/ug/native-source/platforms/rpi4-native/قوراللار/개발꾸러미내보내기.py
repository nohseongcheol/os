#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from ئىجرا_قىلىش_بۇيرۇق import كۆرسىتىش_يىلتىز


def ئىجرا_قىل_2():
    배포경로 = كۆرسىتىش_يىلتىز / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = كۆرسىتىش_يىلتىز.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(كۆرسىتىش_يىلتىز / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        ھۆججەت_تىزىم = {
            كۆرسىتىش_يىلتىز.parents[1] / 'LICENSE': 'LICENSE',
            كۆرسىتىش_يىلتىز.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            كۆرسىتىش_يىلتىز / 'قوراللار/개발꾸러미번역.py': 'compile.py',
            كۆرسىتىش_يىلتىز / 'ئىشلەتكۈچى/호출.h': 'include/호출.h',
            كۆرسىتىش_يىلتىز / '명명/기계연결이름.h': '명명/기계연결이름.h',
            كۆرسىتىش_يىلتىز / 'ئىشلەتكۈچى/ئۇلانما_لايىھە.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            كۆرسىتىش_يىلتىز / 'build/user/start.o': 'lib/start.o',
            كۆرسىتىش_يىلتىز / 'build/user/runtime.o': 'lib/runtime.o',
            كۆرسىتىش_يىلتىز / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            كۆرسىتىش_يىلتىز / 'ئىشلەتكۈچى/파일예제.cpp': 'examples/파일예제.cpp',
            كۆرسىتىش_يىلتىز / '예제/한글코딩/인사.c': 'examples/인사.c',
            كۆرسىتىش_يىلتىز / '예제/한글코딩/ئېقىم_قىممىتى.c': 'examples/ئېقىم_قىممىتى.c',
            كۆرسىتىش_يىلتىز / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            كۆرسىتىش_يىلتىز / 'ئىشلەتكۈچى/통신예제.cpp': 'examples/통신예제.cpp',
            كۆرسىتىش_يىلتىز / 'build/user/demo.elf': 'examples/demo.elf',
            كۆرسىتىش_يىلتىز / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, نىشان in ھۆججەت_تىزىم.items():
            نىشان_مەلۇمات_ئادرېس = 개발꾸러미 / نىشان
            نىشان_مەلۇمات_ئادرېس.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(نىشان_مەلۇمات_ئادرېس))
            꾸러미명세['sha256'][نىشان] = hashlib.sha256(نىشان_مەلۇمات_ئادرېس.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int باشلاش_ئىشلەتكۈچى_ئەپ(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: قوراللار/ئىجرا_قىلىش_بۇيرۇق.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 قوراللار/ئىجرا_قىلىش_ھۆججەت.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: 사용자인수개수()/ئىشلەتكۈچى_دەلىل() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        ئارخىپ = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(ئارخىپ), 'w:gz') as ئۆلچەم_مەلۇمات:
            ئۆلچەم_مەلۇمات.add(str(개발꾸러미), arcname=개발꾸러미.name)
        ئارخىپ.replace(배포경로 / ئارخىپ.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as ئۆلچەم_مەلۇمات:
            for ئاتى in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                ئۆلچەم_مەلۇمات.add(str(كۆرسىتىش_يىلتىز.parents[1] / ئاتى), arcname='jkoros-native/' + ئاتى)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'ئىشلەتكۈچى', '명명',
                             'قوراللار/시언어번역기빌드.py', 'قوراللار/نۇسخا_ئىشلەتكۈچى_بوشلۇق.py', '파일전송과번역.md'):
                ئۆلچەم_مەلۇمات.add(str(كۆرسىتىش_يىلتىز / 상대경로), arcname='jkoros-native/' + 상대경로)
            for ئاتى in ('crt.o', 'aot-runtime.o', 'ئورتاق_تىل_ئىجرا_ۋاقتى_قوللاش.o', 'ئىجرا_قىل_2.o', '미리번역.o', 'قايتۇرۇپ_بېرىش_كۆۋرۈك.o'):
                نىشان_ھۆججەت = كۆرسىتىش_يىلتىز / 'build/ccompiler' / ئاتى
                ئۆلچەم_مەلۇمات.add(str(نىشان_ھۆججەت), arcname='jkoros-native/relink/' + ئاتى)
            for ئاتى in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                ئۆلچەم_مەلۇمات.add(str(كۆرسىتىش_يىلتىز / 'build/user' / ئاتى), arcname='jkoros-native/relink/user/' + ئاتى)
            ئۆلچەم_مەلۇمات.add(str(كۆرسىتىش_يىلتىز / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            ئۆلچەم_مەلۇمات.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    ئىجرا_قىل_2()
