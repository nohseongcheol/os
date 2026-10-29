#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from შესრულება_ბრძანება import პროეცირება_ფესვი


def გაშვება():
    배포경로 = პროეცირება_ფესვი / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = პროეცირება_ფესვი.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(პროეცირება_ფესვი / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        ფაილი_სია = {
            პროეცირება_ფესვი.parents[1] / 'LICENSE': 'LICENSE',
            პროეცირება_ფესვი.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            პროეცირება_ფესვი / 'ხელსაწყოები/개발꾸러미번역.py': 'compile.py',
            პროეცირება_ფესვი / 'მომხმარებელი/호출.h': 'include/호출.h',
            პროეცირება_ფესვი / '명명/기계연결이름.h': '명명/기계연결이름.h',
            პროეცირება_ფესვი / 'მომხმარებელი/ბმული_განლაგება.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            პროეცირება_ფესვი / 'build/user/start.o': 'lib/start.o',
            პროეცირება_ფესვი / 'build/user/runtime.o': 'lib/runtime.o',
            პროეცირება_ფესვი / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            პროეცირება_ფესვი / 'მომხმარებელი/파일예제.cpp': 'examples/파일예제.cpp',
            პროეცირება_ფესვი / '예제/한글코딩/인사.c': 'examples/인사.c',
            პროეცირება_ფესვი / '예제/한글코딩/ნაკადი_მნიშვნელობა.c': 'examples/ნაკადი_მნიშვნელობა.c',
            პროეცირება_ფესვი / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            პროეცირება_ფესვი / 'მომხმარებელი/통신예제.cpp': 'examples/통신예제.cpp',
            პროეცირება_ფესვი / 'build/user/demo.elf': 'examples/demo.elf',
            პროეცირება_ფესვი / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, მიზანი in ფაილი_სია.items():
            მიმართულება_მონაცემები_მისამართი = 개발꾸러미 / მიზანი
            მიმართულება_მონაცემები_მისამართი.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(მიმართულება_მონაცემები_მისამართი))
            꾸러미명세['sha256'][მიზანი] = hashlib.sha256(მიმართულება_მონაცემები_მისამართი.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int დაწყება_მომხმარებელი_აპი(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: ხელსაწყოები/შესრულება_ბრძანება.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 ხელსაწყოები/შესრულება_ფაილი.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: 사용자인수개수()/მომხმარებელი_არგუმენტი() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        არქივი = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(არქივი), 'w:gz') as გაზომვა_მონაცემები:
            გაზომვა_მონაცემები.add(str(개발꾸러미), arcname=개발꾸러미.name)
        არქივი.replace(배포경로 / არქივი.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as გაზომვა_მონაცემები:
            for სახელი in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                გაზომვა_მონაცემები.add(str(პროეცირება_ფესვი.parents[1] / სახელი), arcname='jkoros-native/' + სახელი)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'მომხმარებელი', '명명',
                             'ხელსაწყოები/시언어번역기빌드.py', 'ხელსაწყოები/აწყობა_მომხმარებელი_სივრცე.py', '파일전송과번역.md'):
                გაზომვა_მონაცემები.add(str(პროეცირება_ფესვი / 상대경로), arcname='jkoros-native/' + 상대경로)
            for სახელი in ('crt.o', 'aot-runtime.o', 'საერთო_ენობრივი_გარემო_მხარდაჭერა.o', 'გაშვება.o', '미리번역.o', 'დაბრუნება_ხიდი.o'):
                დანიშნულების_ფაილი = პროეცირება_ფესვი / 'build/ccompiler' / სახელი
                გაზომვა_მონაცემები.add(str(დანიშნულების_ფაილი), arcname='jkoros-native/relink/' + სახელი)
            for სახელი in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                გაზომვა_მონაცემები.add(str(პროეცირება_ფესვი / 'build/user' / სახელი), arcname='jkoros-native/relink/user/' + სახელი)
            გაზომვა_მონაცემები.add(str(პროეცირება_ფესვი / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            გაზომვა_მონაცემები.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    გაშვება()
