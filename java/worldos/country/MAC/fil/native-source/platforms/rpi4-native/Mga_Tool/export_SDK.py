#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from Mag_execute_utos import Project_root


def run():
    배포경로 = Project_root / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = Project_root.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(Project_root / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        file_list = {
            Project_root.parents[1] / 'LICENSE': 'LICENSE',
            Project_root.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            Project_root / 'Mga_Tool/SDK_bumuo.py': 'compile.py',
            Project_root / 'gumagamit/호출.h': 'include/호출.h',
            Project_root / '명명/기계연결이름.h': '명명/기계연결이름.h',
            Project_root / 'gumagamit/Link_Layout.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            Project_root / 'build/user/start.o': 'lib/start.o',
            Project_root / 'build/user/runtime.o': 'lib/runtime.o',
            Project_root / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            Project_root / 'gumagamit/파일예제.cpp': 'examples/파일예제.cpp',
            Project_root / '예제/한글코딩/인사.c': 'examples/인사.c',
            Project_root / '예제/한글코딩/Stream_VALUE.c': 'examples/Stream_VALUE.c',
            Project_root / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            Project_root / 'gumagamit/통신예제.cpp': 'examples/통신예제.cpp',
            Project_root / 'build/user/demo.elf': 'examples/demo.elf',
            Project_root / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, layunin in file_list.items():
            patutunguhan_data_email = 개발꾸러미 / layunin
            patutunguhan_data_email.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(patutunguhan_data_email))
            꾸러미명세['sha256'][layunin] = hashlib.sha256(patutunguhan_data_email.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int Start_gumagamit_app(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Mga_Tool/Mag_execute_utos.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Mga_Tool/Mag_execute_file.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: gumagamit_argumento_COUNT()/gumagamit_argumento() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Archive = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Archive), 'w:gz') as sukat_data:
            sukat_data.add(str(개발꾸러미), arcname=개발꾸러미.name)
        Archive.replace(배포경로 / Archive.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as sukat_data:
            for pangalan in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                sukat_data.add(str(Project_root.parents[1] / pangalan), arcname='jkoros-native/' + pangalan)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'gumagamit', '명명',
                             'Mga_Tool/시언어번역기빌드.py', 'Mga_Tool/build_gumagamit_SPACE.py', '파일전송과번역.md'):
                sukat_data.add(str(Project_root / 상대경로), arcname='jkoros-native/' + 상대경로)
            for pangalan in ('crt.o', 'aot-runtime.o', 'common_language_runtime_Suporta.o', 'run.o', '미리번역.o', '되돌림.o'):
                patutunguhang_file = Project_root / 'build/ccompiler' / pangalan
                sukat_data.add(str(patutunguhang_file), arcname='jkoros-native/relink/' + pangalan)
            for pangalan in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                sukat_data.add(str(Project_root / 'build/user' / pangalan), arcname='jkoros-native/relink/user/' + pangalan)
            sukat_data.add(str(Project_root / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            sukat_data.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    run()
