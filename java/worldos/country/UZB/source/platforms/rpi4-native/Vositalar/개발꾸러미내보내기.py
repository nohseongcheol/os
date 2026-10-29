#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from bajarmoq_buyruq import Project_ildiz


def Bajarish():
    배포경로 = Project_ildiz / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = Project_ildiz.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(Project_ildiz / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        fayl_Ro_yxat = {
            Project_ildiz.parents[1] / 'LICENSE': 'LICENSE',
            Project_ildiz.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            Project_ildiz / 'Vositalar/개발꾸러미번역.py': 'compile.py',
            Project_ildiz / 'foydalanuvchi/호출.h': 'include/호출.h',
            Project_ildiz / '명명/기계연결이름.h': '명명/기계연결이름.h',
            Project_ildiz / 'foydalanuvchi/ulash_Maket.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            Project_ildiz / 'build/user/start.o': 'lib/start.o',
            Project_ildiz / 'build/user/runtime.o': 'lib/runtime.o',
            Project_ildiz / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            Project_ildiz / 'foydalanuvchi/파일예제.cpp': 'examples/파일예제.cpp',
            Project_ildiz / '예제/한글코딩/인사.c': 'examples/인사.c',
            Project_ildiz / '예제/한글코딩/oqim_VALUE.c': 'examples/oqim_VALUE.c',
            Project_ildiz / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            Project_ildiz / 'foydalanuvchi/통신예제.cpp': 'examples/통신예제.cpp',
            Project_ildiz / 'build/user/demo.elf': 'examples/demo.elf',
            Project_ildiz / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, nishon in fayl_Ro_yxat.items():
            ko_chirish_joyi_ma_lumotlar_manzil = 개발꾸러미 / nishon
            ko_chirish_joyi_ma_lumotlar_manzil.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(ko_chirish_joyi_ma_lumotlar_manzil))
            꾸러미명세['sha256'][nishon] = hashlib.sha256(ko_chirish_joyi_ma_lumotlar_manzil.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int Start_foydalanuvchi_ilova(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Vositalar/bajarmoq_buyruq.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Vositalar/bajarmoq_fayl.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: foydalanuvchi_dalil_COUNT()/foydalanuvchi_dalil() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Arxiv = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Arxiv), 'w:gz') as o_lchov_ma_lumotlar:
            o_lchov_ma_lumotlar.add(str(개발꾸러미), arcname=개발꾸러미.name)
        Arxiv.replace(배포경로 / Arxiv.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as o_lchov_ma_lumotlar:
            for Nomi in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                o_lchov_ma_lumotlar.add(str(Project_ildiz.parents[1] / Nomi), arcname='jkoros-native/' + Nomi)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'foydalanuvchi', '명명',
                             'Vositalar/시언어번역기빌드.py', 'Vositalar/nashr_foydalanuvchi_joy.py', '파일전송과번역.md'):
                o_lchov_ma_lumotlar.add(str(Project_ildiz / 상대경로), arcname='jkoros-native/' + 상대경로)
            for Nomi in ('crt.o', 'aot-runtime.o', 'umumiy_til_ish_jarayoni_madad.o', 'Bajarish.o', '미리번역.o', '되돌림.o'):
                natijalar_fayli = Project_ildiz / 'build/ccompiler' / Nomi
                o_lchov_ma_lumotlar.add(str(natijalar_fayli), arcname='jkoros-native/relink/' + Nomi)
            for Nomi in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                o_lchov_ma_lumotlar.add(str(Project_ildiz / 'build/user' / Nomi), arcname='jkoros-native/relink/user/' + Nomi)
            o_lchov_ma_lumotlar.add(str(Project_ildiz / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            o_lchov_ma_lumotlar.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    Bajarish()
