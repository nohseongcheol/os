#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from নিষ্পাদন_আদেশ import 기준


def সঞ্চালন():
    배포경로 = 기준 / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = 기준.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(기준 / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        ফাইল_সূচী = {
            기준.parents[1] / 'LICENSE': 'LICENSE',
            기준.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            기준 / 'সঁজুলিসমূহ/개발꾸러미번역.py': 'compile.py',
            기준 / 'ব্যৱহাৰকৰ্তা/호출.h': 'include/호출.h',
            기준 / '명명/기계연결이름.h': '명명/기계연결이름.h',
            기준 / 'ব্যৱহাৰকৰ্তা/লিংক_লেআউট.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            기준 / 'build/user/start.o': 'lib/start.o',
            기준 / 'build/user/runtime.o': 'lib/runtime.o',
            기준 / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            기준 / 'ব্যৱহাৰকৰ্তা/파일예제.cpp': 'examples/파일예제.cpp',
            기준 / '예제/한글코딩/인사.c': 'examples/인사.c',
            기준 / '예제/한글코딩/ষ্ট্ৰিম_মান.c': 'examples/ষ্ট্ৰিম_মান.c',
            기준 / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            기준 / 'ব্যৱহাৰকৰ্তা/통신예제.cpp': 'examples/통신예제.cpp',
            기준 / 'build/user/demo.elf': 'examples/demo.elf',
            기준 / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, লক্ষ্য in ফাইল_সূচী.items():
            গন্তব্য_স্থান_ডাটা_ঠিকনা = 개발꾸러미 / লক্ষ্য
            গন্তব্য_স্থান_ডাটা_ঠিকনা.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(গন্তব্য_স্থান_ডাটা_ঠিকনা))
            꾸러미명세['sha256'][লক্ষ্য] = hashlib.sha256(গন্তব্য_স্থান_ডাটা_ঠিকনা.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int আৰম্ভ_ব্যৱহাৰকৰ্তা_এপ্প্(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: সঁজুলিসমূহ/নিষ্পাদন_আদেশ.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 সঁজুলিসমূহ/নিষ্পাদন_ফাইল.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: 사용자인수개수()/ব্যৱহাৰকৰ্তা_যুক্তি() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        অভিলেখাগাৰ = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(অভিলেখাগাৰ), 'w:gz') as পৰিমাপ_ডাটা:
            পৰিমাপ_ডাটা.add(str(개발꾸러미), arcname=개발꾸러미.name)
        অভিলেখাগাৰ.replace(배포경로 / অভিলেখাগাৰ.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as পৰিমাপ_ডাটা:
            for নাম in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                পৰিমাপ_ডাটা.add(str(기준.parents[1] / নাম), arcname='jkoros-native/' + নাম)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'ব্যৱহাৰকৰ্তা', '명명',
                             'সঁজুলিসমূহ/시언어번역기빌드.py', 'সঁজুলিসমূহ/বিল্ড_ব্যৱহাৰকৰ্তা_স্থান.py', '파일전송과번역.md'):
                পৰিমাপ_ডাটা.add(str(기준 / 상대경로), arcname='jkoros-native/' + 상대경로)
            for নাম in ('crt.o', 'aot-runtime.o', 'উমৈহতীয়া_ভাষা_ৰানটাইম_সমর্থন.o', 'সঞ্চালন.o', '미리번역.o', '되돌림.o'):
                গন্তব্য_ফাইল = 기준 / 'build/ccompiler' / নাম
                পৰিমাপ_ডাটা.add(str(গন্তব্য_ফাইল), arcname='jkoros-native/relink/' + নাম)
            for নাম in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                পৰিমাপ_ডাটা.add(str(기준 / 'build/user' / নাম), arcname='jkoros-native/relink/user/' + নাম)
            পৰিমাপ_ডাটা.add(str(기준 / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            পৰিমাপ_ডাটা.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    সঞ্চালন()
