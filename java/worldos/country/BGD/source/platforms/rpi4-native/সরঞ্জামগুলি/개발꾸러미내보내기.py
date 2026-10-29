#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from কার্যকর_করুন_আদেশ import প্রকল্প_মূল


def চালনা():
    배포경로 = প্রকল্প_মূল / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = প্রকল্প_মূল.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(প্রকল্প_মূল / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        ফাইল_তালিকা = {
            প্রকল্প_মূল.parents[1] / 'LICENSE': 'LICENSE',
            প্রকল্প_মূল.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            প্রকল্প_মূল / 'সরঞ্জামগুলি/개발꾸러미번역.py': 'compile.py',
            প্রকল্প_মূল / 'ব্যবহারকারী/호출.h': 'include/호출.h',
            প্রকল্প_মূল / '명명/기계연결이름.h': '명명/기계연결이름.h',
            প্রকল্প_মূল / 'ব্যবহারকারী/লিংক_লেআউট.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            প্রকল্প_মূল / 'build/user/start.o': 'lib/start.o',
            প্রকল্প_মূল / 'build/user/runtime.o': 'lib/runtime.o',
            প্রকল্প_মূল / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            প্রকল্প_মূল / 'ব্যবহারকারী/ফাইলনমুনা.cpp': 'examples/ফাইলনমুনা.cpp',
            প্রকল্প_মূল / '예제/한글코딩/인사.c': 'examples/인사.c',
            প্রকল্প_মূল / '예제/한글코딩/প্রবাহ_মান.c': 'examples/প্রবাহ_মান.c',
            প্রকল্প_মূল / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            প্রকল্প_মূল / 'ব্যবহারকারী/통신예제.cpp': 'examples/통신예제.cpp',
            প্রকল্প_মূল / 'build/user/demo.elf': 'examples/demo.elf',
            প্রকল্প_মূল / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, লক্ষ্য in ফাইল_তালিকা.items():
            গন্তব্য_ডাটা_ইমেইল = 개발꾸러미 / লক্ষ্য
            গন্তব্য_ডাটা_ইমেইল.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(গন্তব্য_ডাটা_ইমেইল))
            꾸러미명세['sha256'][লক্ষ্য] = hashlib.sha256(গন্তব্য_ডাটা_ইমেইল.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/ফাইলনমুনা.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int শুরু_ব্যবহারকারী_অ্যাপ(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: সরঞ্জামগুলি/কার্যকর_করুন_আদেশ.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 সরঞ্জামগুলি/কার্যকর_করুন_ফাইল.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: 사용자인수개수()/ব্যবহারকারী_যুক্তি() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        সংগ্রহ_করা = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(সংগ্রহ_করা), 'w:gz') as পরিমাপ_ডাটা:
            পরিমাপ_ডাটা.add(str(개발꾸러미), arcname=개발꾸러미.name)
        সংগ্রহ_করা.replace(배포경로 / সংগ্রহ_করা.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as পরিমাপ_ডাটা:
            for নাম in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                পরিমাপ_ডাটা.add(str(প্রকল্প_মূল.parents[1] / নাম), arcname='jkoros-native/' + নাম)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'ব্যবহারকারী', '명명',
                             'সরঞ্জামগুলি/시언어번역기빌드.py', 'সরঞ্জামগুলি/গঠন_ব্যবহারকারী_স্পেস.py', '파일전송과번역.md'):
                পরিমাপ_ডাটা.add(str(প্রকল্প_মূল / 상대경로), arcname='jkoros-native/' + 상대경로)
            for নাম in ('crt.o', 'aot-runtime.o', 'সাধারণ_ভাষা_রানটাইম_সমর্থন.o', 'চালনা.o', '미리번역.o', '되돌림.o'):
                গন্তব্য_ফাইল = প্রকল্প_মূল / 'build/ccompiler' / নাম
                পরিমাপ_ডাটা.add(str(গন্তব্য_ফাইল), arcname='jkoros-native/relink/' + নাম)
            for নাম in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                পরিমাপ_ডাটা.add(str(প্রকল্প_মূল / 'build/user' / নাম), arcname='jkoros-native/relink/user/' + নাম)
            পরিমাপ_ডাটা.add(str(প্রকল্প_মূল / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            পরিমাপ_ডাটা.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    চালনা()
