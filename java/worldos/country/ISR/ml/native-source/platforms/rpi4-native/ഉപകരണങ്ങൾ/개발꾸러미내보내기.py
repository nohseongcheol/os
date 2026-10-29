#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from നടപ്പാക്കുക_കമാന്_ഡ് import പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം


def നടപ്പിലാക്കുക():
    배포경로 = പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        ഫയല്_ലിസ്റ്റ് = {
            പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം.parents[1] / 'LICENSE': 'LICENSE',
            പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'ഉപകരണങ്ങൾ/개발꾸러미번역.py': 'compile.py',
            പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'ഉപയോക്താവ്/호출.h': 'include/호출.h',
            പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / '명명/기계연결이름.h': '명명/기계연결이름.h',
            പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'ഉപയോക്താവ്/ലിങ്ക്_ലേഔട്ട്.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/user/start.o': 'lib/start.o',
            പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/user/runtime.o': 'lib/runtime.o',
            പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'ഉപയോക്താവ്/파일예제.cpp': 'examples/파일예제.cpp',
            പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / '예제/한글코딩/인사.c': 'examples/인사.c',
            പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / '예제/한글코딩/സ്ട്രീം_മൂല്യം.c': 'examples/സ്ട്രീം_മൂല്യം.c',
            പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'ഉപയോക്താവ്/통신예제.cpp': 'examples/통신예제.cpp',
            പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/user/demo.elf': 'examples/demo.elf',
            പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/user/network.elf': 'examples/network.elf',
        }
        ബണ്ടിൽ_ആവിഷ്കാരം = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, ലക്_ഷ്യം in ഫയല്_ലിസ്റ്റ്.items():
            ഉദ്ദിഷ്ടസ്ഥാനം_ഡാറ്റാ_ഇമെയിൽ = 개발꾸러미 / ലക്_ഷ്യം
            ഉദ്ദിഷ്ടസ്ഥാനം_ഡാറ്റാ_ഇമെയിൽ.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(ഉദ്ദിഷ്ടസ്ഥാനം_ഡാറ്റാ_ഇമെയിൽ))
            ബണ്ടിൽ_ആവിഷ്കാരം['sha256'][ലക്_ഷ്യം] = hashlib.sha256(ഉദ്ദിഷ്ടസ്ഥാനം_ഡാറ്റാ_ഇമെയിൽ.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(ബണ്ടിൽ_ആവിഷ്കാരം, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int ആരംഭം_ഉപയോക്താവ്_പ്രോഗ്രാം(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: ഉപകരണങ്ങൾ/നടപ്പാക്കുക_കമാന്_ഡ്.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 ഉപകരണങ്ങൾ/നടപ്പാക്കുക_ഫയല്.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: 사용자인수개수()/ഉപയോക്താവ്_ആര്_ഗ്യുമെന്_റ്() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        ശേഖരം = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(ശേഖരം), 'w:gz') as അളവ്_ഡാറ്റാ:
            അളവ്_ഡാറ്റാ.add(str(개발꾸러미), arcname=개발꾸러미.name)
        ശേഖരം.replace(배포경로 / ശേഖരം.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as അളവ്_ഡാറ്റാ:
            for പേരു് in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                അളവ്_ഡാറ്റാ.add(str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം.parents[1] / പേരു്), arcname='jkoros-native/' + പേരു്)
            for ആപേക്ഷിക_പാത in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'ഉപയോക്താവ്', '명명',
                             'ഉപകരണങ്ങൾ/시언어번역기빌드.py', 'ഉപകരണങ്ങൾ/ബിൽഡ്_ഉപയോക്താവ്_സ്ഥലം.py', '파일전송과번역.md'):
                അളവ്_ഡാറ്റാ.add(str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / ആപേക്ഷിക_പാത), arcname='jkoros-native/' + ആപേക്ഷിക_പാത)
            for പേരു് in ('crt.o', 'aot-runtime.o', 'പൊതുവായ_ഭാഷ_പ്രവര്_ത്തന_സമയം_പിന്തുണ.o', 'നടപ്പിലാക്കുക.o', '미리번역.o', '되돌림.o'):
                ഉദ്ദിഷ്ടസ്ഥാന_ഫയല് = പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/ccompiler' / പേരു്
                അളവ്_ഡാറ്റാ.add(str(ഉദ്ദിഷ്ടസ്ഥാന_ഫയല്), arcname='jkoros-native/relink/' + പേരു്)
            for പേരു് in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                അളവ്_ഡാറ്റാ.add(str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/user' / പേരു്), arcname='jkoros-native/relink/user/' + പേരു്)
            അളവ്_ഡാറ്റാ.add(str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            അളവ്_ഡാറ്റാ.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    നടപ്പിലാക്കുക()
