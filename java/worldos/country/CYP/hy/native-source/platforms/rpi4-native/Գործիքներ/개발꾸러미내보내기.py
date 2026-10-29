#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from կատարել_հրաման import արձակել_արմատ


def Գործարկել():
    배포경로 = արձակել_արմատ / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = արձակել_արմատ.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(արձակել_արմատ / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        նիշք_Ցուցակ = {
            արձակել_արմատ.parents[1] / 'LICENSE': 'LICENSE',
            արձակել_արմատ.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            արձակել_արմատ / 'Գործիքներ/개발꾸러미번역.py': 'compile.py',
            արձակել_արմատ / 'օգտվող/호출.h': 'include/호출.h',
            արձակել_արմատ / '명명/기계연결이름.h': '명명/기계연결이름.h',
            արձակել_արմատ / 'օգտվող/կապ_Դասավորություն.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            արձակել_արմատ / 'build/user/start.o': 'lib/start.o',
            արձակել_արմատ / 'build/user/runtime.o': 'lib/runtime.o',
            արձակել_արմատ / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            արձակել_արմատ / 'օգտվող/파일예제.cpp': 'examples/파일예제.cpp',
            արձակել_արմատ / '예제/한글코딩/인사.c': 'examples/인사.c',
            արձակել_արմատ / '예제/한글코딩/հոսք_արժեք.c': 'examples/հոսք_արժեք.c',
            արձակել_արմատ / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            արձակել_արմատ / 'օգտվող/통신예제.cpp': 'examples/통신예제.cpp',
            արձակել_արմատ / 'build/user/demo.elf': 'examples/demo.elf',
            արձակել_արմատ / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, թիրախ in նիշք_Ցուցակ.items():
            նպատակակետ_տվյալ_հասցե = 개발꾸러미 / թիրախ
            նպատակակետ_տվյալ_հասցե.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(նպատակակետ_տվյալ_հասցե))
            꾸러미명세['sha256'][թիրախ] = hashlib.sha256(նպատակակետ_տվյալ_հասցե.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int Մեկնարկ_օգտվող_ծրագիր(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Գործիքներ/կատարել_հրաման.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Գործիքներ/կատարել_նիշք.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: 사용자인수개수()/օգտվող_արգումենտ() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Պահոց = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Պահոց), 'w:gz') as չափ_տվյալ:
            չափ_տվյալ.add(str(개발꾸러미), arcname=개발꾸러미.name)
        Պահոց.replace(배포경로 / Պահոց.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as չափ_տվյալ:
            for Անուն in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                չափ_տվյալ.add(str(արձակել_արմատ.parents[1] / Անուն), arcname='jkoros-native/' + Անուն)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'օգտվող', '명명',
                             'Գործիքներ/시언어번역기빌드.py', 'Գործիքներ/կառուցել_օգտվող_տեղ.py', '파일전송과번역.md'):
                չափ_տվյալ.add(str(արձակել_արմատ / 상대경로), arcname='jkoros-native/' + 상대경로)
            for Անուն in ('crt.o', 'aot-runtime.o', 'սովորական_լեզվի_աշխատաժամանակ_Աջակցում.o', 'Գործարկել.o', '미리번역.o', 'վերադարձնել_կամուրջ.o'):
                նշանակման_նիշք = արձակել_արմատ / 'build/ccompiler' / Անուն
                չափ_տվյալ.add(str(նշանակման_նիշք), arcname='jkoros-native/relink/' + Անուն)
            for Անուն in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                չափ_տվյալ.add(str(արձակել_արմատ / 'build/user' / Անուն), arcname='jkoros-native/relink/user/' + Անուն)
            չափ_տվյալ.add(str(արձակել_արմատ / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            չափ_տվյալ.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    Գործարկել()
