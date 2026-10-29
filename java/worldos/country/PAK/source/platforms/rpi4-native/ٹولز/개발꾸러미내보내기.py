#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from نفاذ_کریں_حکم import عکس_ڈالنا_روٹ


def چلائیں():
    배포경로 = عکس_ڈالنا_روٹ / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = عکس_ڈالنا_روٹ.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(عکس_ڈالنا_روٹ / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        فائل_فہرست = {
            عکس_ڈالنا_روٹ.parents[1] / 'LICENSE': 'LICENSE',
            عکس_ڈالنا_روٹ.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            عکس_ڈالنا_روٹ / 'ٹولز/개발꾸러미번역.py': 'compile.py',
            عکس_ڈالنا_روٹ / 'صارف/호출.h': 'include/호출.h',
            عکس_ڈالنا_روٹ / '명명/기계연결이름.h': '명명/기계연결이름.h',
            عکس_ڈالنا_روٹ / 'صارف/ربط_ترتیب.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            عکس_ڈالنا_روٹ / 'build/user/start.o': 'lib/start.o',
            عکس_ڈالنا_روٹ / 'build/user/runtime.o': 'lib/runtime.o',
            عکس_ڈالنا_روٹ / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            عکس_ڈالنا_روٹ / 'صارف/فائلمثال.cpp': 'examples/فائلمثال.cpp',
            عکس_ڈالنا_روٹ / '예제/한글코딩/인사.c': 'examples/인사.c',
            عکس_ڈالنا_روٹ / '예제/한글코딩/بہاؤ_قدر.c': 'examples/بہاؤ_قدر.c',
            عکس_ڈالنا_روٹ / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            عکس_ڈالنا_روٹ / 'صارف/통신예제.cpp': 'examples/통신예제.cpp',
            عکس_ڈالنا_روٹ / 'build/user/demo.elf': 'examples/demo.elf',
            عکس_ڈالنا_روٹ / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, ہدف in فائل_فہرست.items():
            منزل_مقصود_کوائف_پتہ = 개발꾸러미 / ہدف
            منزل_مقصود_کوائف_پتہ.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(منزل_مقصود_کوائف_پتہ))
            꾸러미명세['sha256'][ہدف] = hashlib.sha256(منزل_مقصود_کوائف_پتہ.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/فائلمثال.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int ابتدا_صارف_ایپ(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: ٹولز/نفاذ_کریں_حکم.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 ٹولز/نفاذ_کریں_فائل.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: 사용자인수개수()/صارف_دلائل() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        محفوظ = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(محفوظ), 'w:gz') as پیمائش_کوائف:
            پیمائش_کوائف.add(str(개발꾸러미), arcname=개발꾸러미.name)
        محفوظ.replace(배포경로 / محفوظ.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as پیمائش_کوائف:
            for نام in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                پیمائش_کوائف.add(str(عکس_ڈالنا_روٹ.parents[1] / نام), arcname='jkoros-native/' + نام)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'صارف', '명명',
                             'ٹولز/시언어번역기빌드.py', 'ٹولز/بلڈ_صارف_اسپیس.py', '파일전송과번역.md'):
                پیمائش_کوائف.add(str(عکس_ڈالنا_روٹ / 상대경로), arcname='jkoros-native/' + 상대경로)
            for نام in ('crt.o', 'aot-runtime.o', 'عام_زبان_چلت_عرصہ_معاونت.o', 'چلائیں.o', '미리번역.o', '되돌림.o'):
                مقصود_فائل = عکس_ڈالنا_روٹ / 'build/ccompiler' / نام
                پیمائش_کوائف.add(str(مقصود_فائل), arcname='jkoros-native/relink/' + نام)
            for نام in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                پیمائش_کوائف.add(str(عکس_ڈالنا_روٹ / 'build/user' / نام), arcname='jkoros-native/relink/user/' + نام)
            پیمائش_کوائف.add(str(عکس_ڈالنا_روٹ / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            پیمائش_کوائف.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    چلائیں()
