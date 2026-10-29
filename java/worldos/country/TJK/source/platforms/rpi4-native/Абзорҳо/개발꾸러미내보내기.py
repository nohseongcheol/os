#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from иҷро_кардан_фармон import 기준


def порча():
    배포경로 = 기준 / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = 기준.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(기준 / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        файл_Рӯйхат = {
            기준.parents[1] / 'LICENSE': 'LICENSE',
            기준.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            기준 / 'Абзорҳо/개발꾸러미번역.py': 'compile.py',
            기준 / 'корбар/호출.h': 'include/호출.h',
            기준 / '명명/기계연결이름.h': '명명/기계연결이름.h',
            기준 / 'корбар/Пайванд_Тарҳбандӣ.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            기준 / 'build/user/start.o': 'lib/start.o',
            기준 / 'build/user/runtime.o': 'lib/runtime.o',
            기준 / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            기준 / 'корбар/파일예제.cpp': 'examples/파일예제.cpp',
            기준 / '예제/한글코딩/인사.c': 'examples/인사.c',
            기준 / '예제/한글코딩/ҷараён_қимат.c': 'examples/ҷараён_қимат.c',
            기준 / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            기준 / 'корбар/통신예제.cpp': 'examples/통신예제.cpp',
            기준 / 'build/user/demo.elf': 'examples/demo.elf',
            기준 / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, ҳадаф in файл_Рӯйхат.items():
            ҷои_таъинот_иттилоот_суроға = 개발꾸러미 / ҳадаф
            ҷои_таъинот_иттилоот_суроға.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(ҷои_таъинот_иттилоот_суроға))
            꾸러미명세['sha256'][ҳадаф] = hashlib.sha256(ҷои_таъинот_иттилоот_суроға.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int Оғоз_корбар_барнома(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Абзорҳо/иҷро_кардан_фармон.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Абзорҳо/иҷро_кардан_файл.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: 사용자인수개수()/корбар_аргумент() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Бойгонӣ = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Бойгонӣ), 'w:gz') as 결과자료:
            결과자료.add(str(개발꾸러미), arcname=개발꾸러미.name)
        Бойгонӣ.replace(배포경로 / Бойгонӣ.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as 결과자료:
            for Ном in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                결과자료.add(str(기준.parents[1] / Ном), arcname='jkoros-native/' + Ном)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'корбар', '명명',
                             'Абзорҳо/시언어번역기빌드.py', 'Абзорҳо/сохт_корбар_фазо.py', '파일전송과번역.md'):
                결과자료.add(str(기준 / 상대경로), arcname='jkoros-native/' + 상대경로)
            for Ном in ('crt.o', 'aot-runtime.o', 'вақти_иҷрои_умумии_забон_Дастгирӣ.o', 'порча.o', '미리번역.o', '되돌림.o'):
                файли_ниҳоӣ = 기준 / 'build/ccompiler' / Ном
                결과자료.add(str(файли_ниҳоӣ), arcname='jkoros-native/relink/' + Ном)
            for Ном in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                결과자료.add(str(기준 / 'build/user' / Ном), arcname='jkoros-native/relink/user/' + Ном)
            결과자료.add(str(기준 / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            결과자료.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    порча()
