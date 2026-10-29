#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from निष्पादित_करें_आदेश import प्रोजेक्ट_करें_मूल


def चलाएँ():
    배포경로 = प्रोजेक्ट_करें_मूल / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = प्रोजेक्ट_करें_मूल.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(प्रोजेक्ट_करें_मूल / 'build')) as 작업경로:
        डेवलपमेंट_किट = Path(작업경로) / 'jkoros-native-sdk'
        फ़ाइल_सूची = {
            प्रोजेक्ट_करें_मूल.parents[1] / 'LICENSE': 'LICENSE',
            प्रोजेक्ट_करें_मूल.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            प्रोजेक्ट_करें_मूल / 'उपकरण/सॉफ़्टवेयर_डेवलपमेंट_किट_कंपाइल.py': 'compile.py',
            प्रोजेक्ट_करें_मूल / 'उपयोगकर्ता/호출.h': 'include/호출.h',
            प्रोजेक्ट_करें_मूल / '명명/기계연결이름.h': '명명/기계연결이름.h',
            प्रोजेक्ट_करें_मूल / 'उपयोगकर्ता/लिंक_लेआउट.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            प्रोजेक्ट_करें_मूल / 'build/user/start.o': 'lib/start.o',
            प्रोजेक्ट_करें_मूल / 'build/user/runtime.o': 'lib/runtime.o',
            प्रोजेक्ट_करें_मूल / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            प्रोजेक्ट_करें_मूल / 'उपयोगकर्ता/संचिकाउदाहरण.cpp': 'examples/संचिकाउदाहरण.cpp',
            प्रोजेक्ट_करें_मूल / '예제/한글코딩/अभिनन्दन_ae353e94.c': 'examples/अभिनन्दन_ae353e94.c',
            प्रोजेक्ट_करें_मूल / '예제/한글코딩/स्ट्रीम_मान.c': 'examples/स्ट्रीम_मान.c',
            प्रोजेक्ट_करें_मूल / '예제/한글코딩/अभिनन्दन_ae353e94.cpp': 'examples/अभिनन्दन_ae353e94.cpp',
            प्रोजेक्ट_करें_मूल / 'उपयोगकर्ता/통신예제.cpp': 'examples/통신예제.cpp',
            प्रोजेक्ट_करें_मूल / 'build/user/demo.elf': 'examples/demo.elf',
            प्रोजेक्ट_करें_मूल / 'build/user/network.elf': 'examples/network.elf',
        }
        बंडल_सूची = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, लक्ष्य in फ़ाइल_सूची.items():
            गंतव्य_डेटा_पता = डेवलपमेंट_किट / लक्ष्य
            गंतव्य_डेटा_पता.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(गंतव्य_डेटा_पता))
            बंडल_सूची['sha256'][लक्ष्य] = hashlib.sha256(गंतव्य_डेटा_पता.read_bytes()).hexdigest()
        (डेवलपमेंट_किट / 'manifest.json').write_text(json.dumps(बंडल_सूची, indent=2) + '\n')
        (डेवलपमेंट_किट / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/संचिकाउदाहरण.cpp -o demo.elf\n'
            'python3 compile.py examples/अभिनन्दन_ae353e94.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int प्रारंभ_उपयोगकर्ता_ऐप(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: उपकरण/निष्पादित_करें_आदेश.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 उपकरण/निष्पादित_करें_फ़ाइल.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: 사용자인수개수()/उपयोगकर्ता_तर्क() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        संग्रह = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(संग्रह), 'w:gz') as परिणाम_डेटा:
            परिणाम_डेटा.add(str(डेवलपमेंट_किट), arcname=डेवलपमेंट_किट.name)
        संग्रह.replace(배포경로 / संग्रह.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        कंपाइलर_संग्रह = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(कंपाइलर_संग्रह), 'w:gz') as परिणाम_डेटा:
            for नाम in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                परिणाम_डेटा.add(str(प्रोजेक्ट_करें_मूल.parents[1] / नाम), arcname='jkoros-native/' + नाम)
            for संबंधित_पथ in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', 'सी_कंपाइलर', 'उपयोगकर्ता', '명명',
                             'उपकरण/बिल्ड_सी_कंपाइलर.py', 'उपकरण/बिल्ड_उपयोगकर्ता_स्थान.py', '파일전송과번역.md'):
                परिणाम_डेटा.add(str(प्रोजेक्ट_करें_मूल / संबंधित_पथ), arcname='jkoros-native/' + संबंधित_पथ)
            for नाम in ('crt.o', 'aot-runtime.o', 'निष्पादनसहायता.o', 'चलाएँ.o', '미리번역.o', 'वापस_करें_ब्रिज.o'):
                गंतव्य_फ़ाइल = प्रोजेक्ट_करें_मूल / 'build/ccompiler' / नाम
                परिणाम_डेटा.add(str(गंतव्य_फ़ाइल), arcname='jkoros-native/relink/' + नाम)
            for नाम in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                परिणाम_डेटा.add(str(प्रोजेक्ट_करें_मूल / 'build/user' / नाम), arcname='jkoros-native/relink/user/' + नाम)
            परिणाम_डेटा.add(str(प्रोजेक्ट_करें_मूल / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            परिणाम_डेटा.add(str(포직스경로), arcname='posix-kor/arm64-native')
        कंपाइलर_संग्रह.replace(배포경로 / कंपाइलर_संग्रह.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    चलाएँ()
