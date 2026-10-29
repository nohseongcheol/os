#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ import ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍


def ଚଳାନ୍ତୁ():
    배포경로 = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        ଫାଇଲ୍_ତାଲିକା = {
            ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍.parents[1] / 'LICENSE': 'LICENSE',
            ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'ଉପକରଣସମୂହ/개발꾸러미번역.py': 'compile.py',
            ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'ଉପଭୋକ୍ତା/호출.h': 'include/호출.h',
            ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / '명명/기계연결이름.h': '명명/기계연결이름.h',
            ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'ଉପଭୋକ୍ତା/ଲିଙ୍କ୍_ଲେଆଉଟ୍.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/user/start.o': 'lib/start.o',
            ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/user/runtime.o': 'lib/runtime.o',
            ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'ଉପଭୋକ୍ତା/파일예제.cpp': 'examples/파일예제.cpp',
            ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / '예제/한글코딩/인사.c': 'examples/인사.c',
            ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / '예제/한글코딩/ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ.c': 'examples/ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ.c',
            ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'ଉପଭୋକ୍ତା/통신예제.cpp': 'examples/통신예제.cpp',
            ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/user/demo.elf': 'examples/demo.elf',
            ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, ଲକ୍ଷ୍ୟସ୍ଥଳ in ଫାଇଲ୍_ତାଲିକା.items():
            ଲକ୍ଷସ୍ଥଳ_ଡାଟା_ଠିକଣା = 개발꾸러미 / ଲକ୍ଷ୍ୟସ୍ଥଳ
            ଲକ୍ଷସ୍ଥଳ_ଡାଟା_ଠିକଣା.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(ଲକ୍ଷସ୍ଥଳ_ଡାଟା_ଠିକଣା))
            꾸러미명세['sha256'][ଲକ୍ଷ୍ୟସ୍ଥଳ] = hashlib.sha256(ଲକ୍ଷସ୍ଥଳ_ଡାଟା_ଠିକଣା.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int ଆରମ୍ଭ_ଉପଭୋକ୍ତା_ଅନୁପ୍ରୟୋଗ(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: ଉପକରଣସମୂହ/ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 ଉପକରଣସମୂହ/ନିର୍ବାହ_କରିବା_ଫାଇଲ୍.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: 사용자인수개수()/ଉପଭୋକ୍ତା_ଯୁକ୍ତି() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        ଅଭିଲେଖାଗାର = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(ଅଭିଲେଖାଗାର), 'w:gz') as ମାପ_ଡାଟା:
            ମାପ_ଡାଟା.add(str(개발꾸러미), arcname=개발꾸러미.name)
        ଅଭିଲେଖାଗାର.replace(배포경로 / ଅଭିଲେଖାଗାର.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as ମାପ_ଡାଟା:
            for ନାମ in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                ମାପ_ଡାଟା.add(str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍.parents[1] / ନାମ), arcname='jkoros-native/' + ନାମ)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'ଉପଭୋକ୍ତା', '명명',
                             'ଉପକରଣସମୂହ/시언어번역기빌드.py', 'ଉପକରଣସମୂହ/ବିଲ୍ଡ୍_ଉପଭୋକ୍ତା_ସ୍ଥାନ.py', '파일전송과번역.md'):
                ମାପ_ଡାଟା.add(str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 상대경로), arcname='jkoros-native/' + 상대경로)
            for ନାମ in ('crt.o', 'aot-runtime.o', 'ସାଧାରଣ_ଭାଷା_ରନ୍_ଟାଇମ୍_ସମର୍ଥନ.o', 'ଚଳାନ୍ତୁ.o', '미리번역.o', '되돌림.o'):
                ଲକ୍ଷସ୍ଥଳ_ଫାଇଲ୍ = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/ccompiler' / ନାମ
                ମାପ_ଡାଟା.add(str(ଲକ୍ଷସ୍ଥଳ_ଫାଇଲ୍), arcname='jkoros-native/relink/' + ନାମ)
            for ନାମ in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                ମାପ_ଡାଟା.add(str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/user' / ନାମ), arcname='jkoros-native/relink/user/' + ନାମ)
            ମାପ_ଡାଟା.add(str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            ମାପ_ଡାଟା.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    ଚଳାନ୍ତୁ()
