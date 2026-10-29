#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from అమలు_చేయి_ఆదేశం import ప్రొజెక్ట్_మూలం


def నడుపుము():
    배포경로 = ప్రొజెక్ట్_మూలం / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = ప్రొజెక్ట్_మూలం.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(ప్రొజెక్ట్_మూలం / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        ఫైలు_జాబితా = {
            ప్రొజెక్ట్_మూలం.parents[1] / 'LICENSE': 'LICENSE',
            ప్రొజెక్ట్_మూలం.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            ప్రొజెక్ట్_మూలం / 'ఉపకరణాలు/개발꾸러미번역.py': 'compile.py',
            ప్రొజెక్ట్_మూలం / 'వినియోగదారు/호출.h': 'include/호출.h',
            ప్రొజెక్ట్_మూలం / '명명/기계연결이름.h': '명명/기계연결이름.h',
            ప్రొజెక్ట్_మూలం / 'వినియోగదారు/బంధం_లేవుట్.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            ప్రొజెక్ట్_మూలం / 'build/user/start.o': 'lib/start.o',
            ప్రొజెక్ట్_మూలం / 'build/user/runtime.o': 'lib/runtime.o',
            ప్రొజెక్ట్_మూలం / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            ప్రొజెక్ట్_మూలం / 'వినియోగదారు/파일예제.cpp': 'examples/파일예제.cpp',
            ప్రొజెక్ట్_మూలం / '예제/한글코딩/인사.c': 'examples/인사.c',
            ప్రొజెక్ట్_మూలం / '예제/한글코딩/ధార_మూల్యం.c': 'examples/ధార_మూల్యం.c',
            ప్రొజెక్ట్_మూలం / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            ప్రొజెక్ట్_మూలం / 'వినియోగదారు/통신예제.cpp': 'examples/통신예제.cpp',
            ప్రొజెక్ట్_మూలం / 'build/user/demo.elf': 'examples/demo.elf',
            ప్రొజెక్ట్_మూలం / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, లక్ష్యం in ఫైలు_జాబితా.items():
            గమ్యం_డేటా_ఇమెయిల్ = 개발꾸러미 / లక్ష్యం
            గమ్యం_డేటా_ఇమెయిల్.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(గమ్యం_డేటా_ఇమెయిల్))
            꾸러미명세['sha256'][లక్ష్యం] = hashlib.sha256(గమ్యం_డేటా_ఇమెయిల్.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int ప్రారంభం_వినియోగదారు_అనువర్తనం(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: ఉపకరణాలు/అమలు_చేయి_ఆదేశం.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 ఉపకరణాలు/అమలు_చేయి_ఫైలు.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: 사용자인수개수()/వినియోగదారు_కారకం() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        ఆర్కైవ్ = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(ఆర్కైవ్), 'w:gz') as ప్రమాణం_డేటా:
            ప్రమాణం_డేటా.add(str(개발꾸러미), arcname=개발꾸러미.name)
        ఆర్కైవ్.replace(배포경로 / ఆర్కైవ్.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as ప్రమాణం_డేటా:
            for పేరు in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                ప్రమాణం_డేటా.add(str(ప్రొజెక్ట్_మూలం.parents[1] / పేరు), arcname='jkoros-native/' + పేరు)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'వినియోగదారు', '명명',
                             'ఉపకరణాలు/시언어번역기빌드.py', 'ఉపకరణాలు/బిల్డ్_వినియోగదారు_ఖాళీ.py', '파일전송과번역.md'):
                ప్రమాణం_డేటా.add(str(ప్రొజెక్ట్_మూలం / 상대경로), arcname='jkoros-native/' + 상대경로)
            for పేరు in ('crt.o', 'aot-runtime.o', 'సాధారణ_భాష_అమలు_సమయం_మద్దతు.o', 'నడుపుము.o', '미리번역.o', '되돌림.o'):
                గమ్యఫైల్ = ప్రొజెక్ట్_మూలం / 'build/ccompiler' / పేరు
                ప్రమాణం_డేటా.add(str(గమ్యఫైల్), arcname='jkoros-native/relink/' + పేరు)
            for పేరు in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                ప్రమాణం_డేటా.add(str(ప్రొజెక్ట్_మూలం / 'build/user' / పేరు), arcname='jkoros-native/relink/user/' + పేరు)
            ప్రమాణం_డేటా.add(str(ప్రొజెక్ట్_మూలం / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            ప్రమాణం_డేటా.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    నడుపుము()
