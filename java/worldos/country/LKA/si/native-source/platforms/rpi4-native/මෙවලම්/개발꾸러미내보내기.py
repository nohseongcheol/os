#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from ක්_රියාත්මක_කරන්න_විධානය import 기준


def ක්_රියාත්මක_කරන්න_2():
    배포경로 = 기준 / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = 기준.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(기준 / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        ගොනුව_ලැයිස්තුව = {
            기준.parents[1] / 'LICENSE': 'LICENSE',
            기준.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            기준 / 'මෙවලම්/개발꾸러미번역.py': 'compile.py',
            기준 / 'පරිශීලක/호출.h': 'include/호출.h',
            기준 / '명명/기계연결이름.h': '명명/기계연결이름.h',
            기준 / 'පරිශීලක/සබැඳිය_සැකැස්ම.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            기준 / 'build/user/start.o': 'lib/start.o',
            기준 / 'build/user/runtime.o': 'lib/runtime.o',
            기준 / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            기준 / 'පරිශීලක/파일예제.cpp': 'examples/파일예제.cpp',
            기준 / '예제/한글코딩/인사.c': 'examples/인사.c',
            기준 / '예제/한글코딩/දහර_අගය.c': 'examples/දහර_අගය.c',
            기준 / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            기준 / 'පරිශීලක/통신예제.cpp': 'examples/통신예제.cpp',
            기준 / 'build/user/demo.elf': 'examples/demo.elf',
            기준 / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, ඉලක්කය in ගොනුව_ලැයිස්තුව.items():
            ගමනාන්තය_දත්ත_යොමුව = 개발꾸러미 / ඉලක්කය
            ගමනාන්තය_දත්ත_යොමුව.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(ගමනාන්තය_දත්ත_යොමුව))
            꾸러미명세['sha256'][ඉලක්කය] = hashlib.sha256(ගමනාන්තය_දත්ත_යොමුව.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int ඇරඹුම_පරිශීලක_යෙදු(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: මෙවලම්/ක්_රියාත්මක_කරන්න_විධානය.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 මෙවලම්/ක්_රියාත්මක_කරන්න_ගොනුව.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: 사용자인수개수()/පරිශීලක_විස්තාරකය() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        සංරක්ෂිතය = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(සංරක්ෂිතය), 'w:gz') as 결과자료:
            결과자료.add(str(개발꾸러미), arcname=개발꾸러미.name)
        සංරක්ෂිතය.replace(배포경로 / සංරක්ෂිතය.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as 결과자료:
            for නම in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                결과자료.add(str(기준.parents[1] / නම), arcname='jkoros-native/' + නම)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'පරිශීලක', '명명',
                             'මෙවලම්/시언어번역기빌드.py', 'මෙවලම්/තැනුම_පරිශීලක_ස්ථානය.py', '파일전송과번역.md'):
                결과자료.add(str(기준 / 상대경로), arcname='jkoros-native/' + 상대경로)
            for නම in ('crt.o', 'aot-runtime.o', 'පොදු_භාෂා_ධාවන_කාලය_සහාය.o', 'ක්_රියාත්මක_කරන්න_2.o', '미리번역.o', '되돌림.o'):
                ගමනාන්ත_ගොනුව = 기준 / 'build/ccompiler' / නම
                결과자료.add(str(ගමනාන්ත_ගොනුව), arcname='jkoros-native/relink/' + නම)
            for නම in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                결과자료.add(str(기준 / 'build/user' / නම), arcname='jkoros-native/relink/user/' + නම)
            결과자료.add(str(기준 / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            결과자료.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    ක්_රියාත්මක_කරන්න_2()
