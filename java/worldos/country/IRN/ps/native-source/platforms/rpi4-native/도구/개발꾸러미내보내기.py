#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from 실행 import 기준


def ځغلول():
    배포경로 = 기준 / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = 기준.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(기준 / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        파일목록 = {
            기준.parents[1] / 'LICENSE': 'LICENSE',
            기준.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            기준 / '도구/개발꾸러미번역.py': 'compile.py',
            기준 / 'کارن/호출.h': 'include/호출.h',
            기준 / '명명/기계연결이름.h': '명명/기계연결이름.h',
            기준 / 'کارن/پيوند_هډوانه.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            기준 / 'build/user/start.o': 'lib/start.o',
            기준 / 'build/user/runtime.o': 'lib/runtime.o',
            기준 / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            기준 / 'کارن/파일예제.cpp': 'examples/파일예제.cpp',
            기준 / '예제/한글코딩/인사.c': 'examples/인사.c',
            기준 / '예제/한글코딩/بهنګ_ارزښت.c': 'examples/بهنګ_ارزښت.c',
            기준 / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            기준 / 'کارن/통신예제.cpp': 'examples/통신예제.cpp',
            기준 / 'build/user/demo.elf': 'examples/demo.elf',
            기준 / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, 대상 in 파일목록.items():
            موخه_اومتوک_پته = 개발꾸러미 / 대상
            موخه_اومتوک_پته.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(موخه_اومتوک_پته))
            꾸러미명세['sha256'][대상] = hashlib.sha256(موخه_اومتوک_پته.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int پيل_کارن_کاريال(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: 도구/실행.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 도구/파일실행.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: 사용자인수개수()/کارن_ارزښتوړى() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        ارشیف = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(ارشیف), 'w:gz') as 결과자료:
            결과자료.add(str(개발꾸러미), arcname=개발꾸러미.name)
        ارشیف.replace(배포경로 / ارشیف.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as 결과자료:
            for نوم in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                결과자료.add(str(기준.parents[1] / نوم), arcname='jkoros-native/' + نوم)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'کارن', '명명',
                             '도구/시언어번역기빌드.py', '도구/جوړول_کارن_تشې_پټۍ.py', '파일전송과번역.md'):
                결과자료.add(str(기준 / 상대경로), arcname='jkoros-native/' + 상대경로)
            for نوم in ('crt.o', 'aot-runtime.o', '실행지원.o', 'ځغلول.o', '미리번역.o', '되돌림.o'):
                موخې_دوتنه = 기준 / 'build/ccompiler' / نوم
                결과자료.add(str(موخې_دوتنه), arcname='jkoros-native/relink/' + نوم)
            for نوم in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                결과자료.add(str(기준 / 'build/user' / نوم), arcname='jkoros-native/relink/user/' + نوم)
            결과자료.add(str(기준 / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            결과자료.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    ځغلول()
