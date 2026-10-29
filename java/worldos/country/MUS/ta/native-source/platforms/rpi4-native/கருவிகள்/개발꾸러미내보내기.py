#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from இயக்கு_கட்டளை import திட்டப்பணி_மூலம்


def செயல்படுத்துக():
    배포경로 = திட்டப்பணி_மூலம் / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = திட்டப்பணி_மூலம்.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(திட்டப்பணி_மூலம் / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        கோப்பு_பட்டியல் = {
            திட்டப்பணி_மூலம்.parents[1] / 'LICENSE': 'LICENSE',
            திட்டப்பணி_மூலம்.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            திட்டப்பணி_மூலம் / 'கருவிகள்/개발꾸러미번역.py': 'compile.py',
            திட்டப்பணி_மூலம் / 'பயனர்/호출.h': 'include/호출.h',
            திட்டப்பணி_மூலம் / '명명/기계연결이름.h': '명명/기계연결이름.h',
            திட்டப்பணி_மூலம் / 'பயனர்/இணை_லேஅவுட்.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            திட்டப்பணி_மூலம் / 'build/user/start.o': 'lib/start.o',
            திட்டப்பணி_மூலம் / 'build/user/runtime.o': 'lib/runtime.o',
            திட்டப்பணி_மூலம் / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            திட்டப்பணி_மூலம் / 'பயனர்/파일예제.cpp': 'examples/파일예제.cpp',
            திட்டப்பணி_மூலம் / '예제/한글코딩/인사.c': 'examples/인사.c',
            திட்டப்பணி_மூலம் / '예제/한글코딩/தொடரோடி_மதிப்பு.c': 'examples/தொடரோடி_மதிப்பு.c',
            திட்டப்பணி_மூலம் / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            திட்டப்பணி_மூலம் / 'பயனர்/통신예제.cpp': 'examples/통신예제.cpp',
            திட்டப்பணி_மூலம் / 'build/user/demo.elf': 'examples/demo.elf',
            திட்டப்பணி_மூலம் / 'build/user/network.elf': 'examples/network.elf',
        }
        மூட்டை_தொற்றம் = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, இலக்கு in கோப்பு_பட்டியல்.items():
            இலக்கு_தரவு_முகவரி = 개발꾸러미 / இலக்கு
            இலக்கு_தரவு_முகவரி.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(இலக்கு_தரவு_முகவரி))
            மூட்டை_தொற்றம்['sha256'][இலக்கு] = hashlib.sha256(இலக்கு_தரவு_முகவரி.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(மூட்டை_தொற்றம், indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int தொடங்கு_பயனர்_நிரல்(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: கருவிகள்/இயக்கு_கட்டளை.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 கருவிகள்/இயக்கு_கோப்பு.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: 사용자인수개수()/பயனர்_மதிப்புரு() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        காப்பகம் = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(காப்பகம்), 'w:gz') as அளவிடக்கூடியது_தரவு:
            அளவிடக்கூடியது_தரவு.add(str(개발꾸러미), arcname=개발꾸러미.name)
        காப்பகம்.replace(배포경로 / காப்பகம்.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as அளவிடக்கூடியது_தரவு:
            for பெயர் in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                அளவிடக்கூடியது_தரவு.add(str(திட்டப்பணி_மூலம்.parents[1] / பெயர்), arcname='jkoros-native/' + பெயர்)
            for தொடர்புடைய_பாதை in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'பயனர்', '명명',
                             'கருவிகள்/시언어번역기빌드.py', 'கருவிகள்/தொகு_பயனர்_தளம்.py', '파일전송과번역.md'):
                அளவிடக்கூடியது_தரவு.add(str(திட்டப்பணி_மூலம் / தொடர்புடைய_பாதை), arcname='jkoros-native/' + தொடர்புடைய_பாதை)
            for பெயர் in ('crt.o', 'aot-runtime.o', 'பொது_மொழி_இயக்க_நேரம்_ஆதரவு.o', 'செயல்படுத்துக.o', '미리번역.o', '되돌림.o'):
                இலக்குக்_கோப்பு = திட்டப்பணி_மூலம் / 'build/ccompiler' / பெயர்
                அளவிடக்கூடியது_தரவு.add(str(இலக்குக்_கோப்பு), arcname='jkoros-native/relink/' + பெயர்)
            for பெயர் in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                அளவிடக்கூடியது_தரவு.add(str(திட்டப்பணி_மூலம் / 'build/user' / பெயர்), arcname='jkoros-native/relink/user/' + பெயர்)
            அளவிடக்கூடியது_தரவு.add(str(திட்டப்பணி_மூலம் / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            அளவிடக்கூடியது_தரவு.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    செயல்படுத்துக()
