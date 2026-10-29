#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from អនុវត្ត_ពាក្យបញ្ជា import បញ្ចាំង_ឬស


def រត់():
    배포경로 = បញ្ចាំង_ឬស / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = បញ្ចាំង_ឬស.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(បញ្ចាំង_ឬស / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        ឯកសារ_បញ្ជី = {
            បញ្ចាំង_ឬស.parents[1] / 'LICENSE': 'LICENSE',
            បញ្ចាំង_ឬស.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            បញ្ចាំង_ឬស / 'ឧបករណ៍/개발꾸러미번역.py': 'compile.py',
            បញ្ចាំង_ឬស / 'អ្នកប្រើ/호출.h': 'include/호출.h',
            បញ្ចាំង_ឬស / '명명/기계연결이름.h': '명명/기계연결이름.h',
            បញ្ចាំង_ឬស / 'អ្នកប្រើ/តំណ_ប្លង់.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            បញ្ចាំង_ឬស / 'build/user/start.o': 'lib/start.o',
            បញ្ចាំង_ឬស / 'build/user/runtime.o': 'lib/runtime.o',
            បញ្ចាំង_ឬស / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            បញ្ចាំង_ឬស / 'អ្នកប្រើ/파일예제.cpp': 'examples/파일예제.cpp',
            បញ្ចាំង_ឬស / '예제/한글코딩/인사.c': 'examples/인사.c',
            បញ្ចាំង_ឬស / '예제/한글코딩/ស្ទ្រីម_តំលៃ.c': 'examples/ស្ទ្រីម_តំលៃ.c',
            បញ្ចាំង_ឬស / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            បញ្ចាំង_ឬស / 'អ្នកប្រើ/통신예제.cpp': 'examples/통신예제.cpp',
            បញ្ចាំង_ឬស / 'build/user/demo.elf': 'examples/demo.elf',
            បញ្ចាំង_ឬស / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, គោលដៅ in ឯកសារ_បញ្ជី.items():
            ទិសដៅ_ទិន្នន័យ_អ៊ីម៉ែល = 개발꾸러미 / គោលដៅ
            ទិសដៅ_ទិន្នន័យ_អ៊ីម៉ែល.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(ទិសដៅ_ទិន្នន័យ_អ៊ីម៉ែល))
            꾸러미명세['sha256'][គោលដៅ] = hashlib.sha256(ទិសដៅ_ទិន្នន័យ_អ៊ីម៉ែល.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int ផ្តើម_អ្នកប្រើ_កម្មវិធី(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: ឧបករណ៍/អនុវត្ត_ពាក្យបញ្ជា.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 ឧបករណ៍/អនុវត្ត_ឯកសារ.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: 사용자인수개수()/អ្នកប្រើ_អាគុយម៉ង់() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        ប័ណ្ណសារ = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(ប័ណ្ណសារ), 'w:gz') as ការវាស់វែង_ទិន្នន័យ:
            ការវាស់វែង_ទិន្នន័យ.add(str(개발꾸러미), arcname=개발꾸러미.name)
        ប័ណ្ណសារ.replace(배포경로 / ប័ណ្ណសារ.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as ការវាស់វែង_ទិន្នន័យ:
            for ឈ្មោះ in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                ការវាស់វែង_ទិន្នន័យ.add(str(បញ្ចាំង_ឬស.parents[1] / ឈ្មោះ), arcname='jkoros-native/' + ឈ្មោះ)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'អ្នកប្រើ', '명명',
                             'ឧបករណ៍/시언어번역기빌드.py', 'ឧបករណ៍/ចងក្រង_អ្នកប្រើ_លំហ.py', '파일전송과번역.md'):
                ការវាស់វែង_ទិន្នន័យ.add(str(បញ្ចាំង_ឬស / 상대경로), arcname='jkoros-native/' + 상대경로)
            for ឈ្មោះ in ('crt.o', 'aot-runtime.o', 'ដំណើរការភាសាទូទៅ_ទម្រ.o', 'រត់.o', '미리번역.o', '되돌림.o'):
                ទិសដៅឯកសារ = បញ្ចាំង_ឬស / 'build/ccompiler' / ឈ្មោះ
                ការវាស់វែង_ទិន្នន័យ.add(str(ទិសដៅឯកសារ), arcname='jkoros-native/relink/' + ឈ្មោះ)
            for ឈ្មោះ in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                ការវាស់វែង_ទិន្នន័យ.add(str(បញ្ចាំង_ឬស / 'build/user' / ឈ្មោះ), arcname='jkoros-native/relink/user/' + ឈ្មោះ)
            ការវាស់វែង_ទិន្នន័យ.add(str(បញ្ចាំង_ឬស / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            ការវាស់វែង_ទិន្នន័យ.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    រត់()
