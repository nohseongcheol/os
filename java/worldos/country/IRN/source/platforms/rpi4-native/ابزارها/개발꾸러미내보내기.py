#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from اجرا_فرمان import نمایش_دادن_جذر


def اجرا_2():
    배포경로 = نمایش_دادن_جذر / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = نمایش_دادن_جذر.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(نمایش_دادن_جذر / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        فایل_لیست = {
            نمایش_دادن_جذر.parents[1] / 'LICENSE': 'LICENSE',
            نمایش_دادن_جذر.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            نمایش_دادن_جذر / 'ابزارها/개발꾸러미번역.py': 'compile.py',
            نمایش_دادن_جذر / 'کاربر/호출.h': 'include/호출.h',
            نمایش_دادن_جذر / '명명/기계연결이름.h': '명명/기계연결이름.h',
            نمایش_دادن_جذر / 'کاربر/پیوند_پیمایش.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            نمایش_دادن_جذر / 'build/user/start.o': 'lib/start.o',
            نمایش_دادن_جذر / 'build/user/runtime.o': 'lib/runtime.o',
            نمایش_دادن_جذر / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            نمایش_دادن_جذر / 'کاربر/نمونهپرونده.cpp': 'examples/نمونهپرونده.cpp',
            نمایش_دادن_جذر / '예제/한글코딩/인사.c': 'examples/인사.c',
            نمایش_دادن_جذر / '예제/한글코딩/جریان_مقدار.c': 'examples/جریان_مقدار.c',
            نمایش_دادن_جذر / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            نمایش_دادن_جذر / 'کاربر/통신예제.cpp': 'examples/통신예제.cpp',
            نمایش_دادن_جذر / 'build/user/demo.elf': 'examples/demo.elf',
            نمایش_دادن_جذر / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, هدف in فایل_لیست.items():
            مقصد_داده_ها_آدرس = 개발꾸러미 / هدف
            مقصد_داده_ها_آدرس.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(مقصد_داده_ها_آدرس))
            꾸러미명세['sha256'][هدف] = hashlib.sha256(مقصد_داده_ها_آدرس.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/نمونهپرونده.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int شروع_کاربر_برنامه(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: ابزارها/اجرا_فرمان.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 ابزارها/اجرا_فایل.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: 사용자인수개수()/کاربر_آرگومان() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        آرشیو = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(آرشیو), 'w:gz') as سنجش_داده_ها:
            سنجش_داده_ها.add(str(개발꾸러미), arcname=개발꾸러미.name)
        آرشیو.replace(배포경로 / آرشیو.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as سنجش_داده_ها:
            for نام in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                سنجش_داده_ها.add(str(نمایش_دادن_جذر.parents[1] / نام), arcname='jkoros-native/' + نام)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'کاربر', '명명',
                             'ابزارها/시언어번역기빌드.py', 'ابزارها/ساخت_کاربر_فضا.py', '파일전송과번역.md'):
                سنجش_داده_ها.add(str(نمایش_دادن_جذر / 상대경로), arcname='jkoros-native/' + 상대경로)
            for نام in ('crt.o', 'aot-runtime.o', 'زمان_اجرای_زبان_مشترک_پشتیبان.o', 'اجرا_2.o', '미리번역.o', 'بازگرداندن_پل.o'):
                پرونده_مقصد = نمایش_دادن_جذر / 'build/ccompiler' / نام
                سنجش_داده_ها.add(str(پرونده_مقصد), arcname='jkoros-native/relink/' + نام)
            for نام in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                سنجش_داده_ها.add(str(نمایش_دادن_جذر / 'build/user' / نام), arcname='jkoros-native/relink/user/' + نام)
            سنجش_داده_ها.add(str(نمایش_دادن_جذر / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            سنجش_داده_ها.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    اجرا_2()
