#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ import 기준


def ᎠᎢᏎᏍᏗ():
    배포경로 = 기준 / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = 기준.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(기준 / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        ᎠᏍᏆᏂᎪᏙᏗ_ᏕᎦᏅᏅᏛ = {
            기준.parents[1] / 'LICENSE': 'LICENSE',
            기준.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            기준 / '도구/개발꾸러미번역.py': 'compile.py',
            기준 / 'ᎬᏗᏍᎩ/호출.h': 'include/호출.h',
            기준 / '명명/기계연결이름.h': '명명/기계연결이름.h',
            기준 / 'ᎬᏗᏍᎩ/ᎫᏓᎸᎢ_ᏱᎬᏂ.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            기준 / 'build/user/start.o': 'lib/start.o',
            기준 / 'build/user/runtime.o': 'lib/runtime.o',
            기준 / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            기준 / 'ᎬᏗᏍᎩ/파일예제.cpp': 'examples/파일예제.cpp',
            기준 / '예제/한글코딩/인사.c': 'examples/인사.c',
            기준 / '예제/한글코딩/ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ.c': 'examples/ᎤᏪᎬ_ᏧᎬᏩᎶᏗᏯ.c',
            기준 / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            기준 / 'ᎬᏗᏍᎩ/통신예제.cpp': 'examples/통신예제.cpp',
            기준 / 'build/user/demo.elf': 'examples/demo.elf',
            기준 / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, ᎠᏉᏅᏗᎢ in ᎠᏍᏆᏂᎪᏙᏗ_ᏕᎦᏅᏅᏛ.items():
            ᏮᎦᏛᎢ_ᎦᏟᏌᏅᎯ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ = 개발꾸러미 / ᎠᏉᏅᏗᎢ
            ᏮᎦᏛᎢ_ᎦᏟᏌᏅᎯ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(ᏮᎦᏛᎢ_ᎦᏟᏌᏅᎯ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ))
            꾸러미명세['sha256'][ᎠᏉᏅᏗᎢ] = hashlib.sha256(ᏮᎦᏛᎢ_ᎦᏟᏌᏅᎯ_ᎪᏪᎵ_ᏫᏗᎦᏅᏗ.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int ᎭᏂᎩᏍᏓ_ᎬᏗᏍᎩ_ᎬᏙᏗ(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: 도구/ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 도구/ᎠᎴᏅᏗᏱ_ᎠᏍᏆᏂᎪᏙᏗ.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: 사용자인수개수()/ᎬᏗᏍᎩ_ᏗᏓᎦᏘᎸᏍᏗ() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        ᎠᏍᏆᏂᎪᏛᎢ = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(ᎠᏍᏆᏂᎪᏛᎢ), 'w:gz') as 결과자료:
            결과자료.add(str(개발꾸러미), arcname=개발꾸러미.name)
        ᎠᏍᏆᏂᎪᏛᎢ.replace(배포경로 / ᎠᏍᏆᏂᎪᏛᎢ.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as 결과자료:
            for ᏚᏙᎥᎢ in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                결과자료.add(str(기준.parents[1] / ᏚᏙᎥᎢ), arcname='jkoros-native/' + ᏚᏙᎥᎢ)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'ᎬᏗᏍᎩ', '명명',
                             '도구/시언어번역기빌드.py', '도구/ᎪᏢᏍᎩ_ᎬᏗᏍᎩ_SPACE.py', '파일전송과번역.md'):
                결과자료.add(str(기준 / 상대경로), arcname='jkoros-native/' + 상대경로)
            for ᏚᏙᎥᎢ in ('crt.o', 'aot-runtime.o', '실행지원.o', 'ᎠᎢᏎᏍᏗ.o', '미리번역.o', '되돌림.o'):
                ᏮᎦᏛᎢ_ᎠᏍᏆᏂᎪᏙᏗ = 기준 / 'build/ccompiler' / ᏚᏙᎥᎢ
                결과자료.add(str(ᏮᎦᏛᎢ_ᎠᏍᏆᏂᎪᏙᏗ), arcname='jkoros-native/relink/' + ᏚᏙᎥᎢ)
            for ᏚᏙᎥᎢ in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                결과자료.add(str(기준 / 'build/user' / ᏚᏙᎥᎢ), arcname='jkoros-native/relink/user/' + ᏚᏙᎥᎢ)
            결과자료.add(str(기준 / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            결과자료.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    ᎠᎢᏎᏍᏗ()
