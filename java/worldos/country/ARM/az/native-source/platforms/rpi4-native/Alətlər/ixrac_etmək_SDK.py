#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from icra_etmək_əmr import Project_kök


def İcra_Et():
    배포경로 = Project_kök / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = Project_kök.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(Project_kök / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        fayl_Siyahı = {
            Project_kök.parents[1] / 'LICENSE': 'LICENSE',
            Project_kök.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            Project_kök / 'Alətlər/SDK_qurmaq.py': 'compile.py',
            Project_kök / 'istifadəçi/호출.h': 'include/호출.h',
            Project_kök / '명명/기계연결이름.h': '명명/기계연결이름.h',
            Project_kök / 'istifadəçi/keçid_Düzüm.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            Project_kök / 'build/user/start.o': 'lib/start.o',
            Project_kök / 'build/user/runtime.o': 'lib/runtime.o',
            Project_kök / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            Project_kök / 'istifadəçi/파일예제.cpp': 'examples/파일예제.cpp',
            Project_kök / '예제/한글코딩/인사.c': 'examples/인사.c',
            Project_kök / '예제/한글코딩/axın_VALUE.c': 'examples/axın_VALUE.c',
            Project_kök / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            Project_kök / 'istifadəçi/통신예제.cpp': 'examples/통신예제.cpp',
            Project_kök / 'build/user/demo.elf': 'examples/demo.elf',
            Project_kök / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, hədəf in fayl_Siyahı.items():
            təyinat_verilənlər_ünvan = 개발꾸러미 / hədəf
            təyinat_verilənlər_ünvan.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(təyinat_verilənlər_ünvan))
            꾸러미명세['sha256'][hədəf] = hashlib.sha256(təyinat_verilənlər_ünvan.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int Başla_istifadəçi_proqram(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Alətlər/icra_etmək_əmr.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Alətlər/icra_etmək_fayl.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: istifadəçi_arqument_COUNT()/istifadəçi_arqument() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Arxiv = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Arxiv), 'w:gz') as ölçü_verilənlər:
            ölçü_verilənlər.add(str(개발꾸러미), arcname=개발꾸러미.name)
        Arxiv.replace(배포경로 / Arxiv.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as ölçü_verilənlər:
            for Ad in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                ölçü_verilənlər.add(str(Project_kök.parents[1] / Ad), arcname='jkoros-native/' + Ad)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'istifadəçi', '명명',
                             'Alətlər/시언어번역기빌드.py', 'Alətlər/qurmaq_istifadəçi_məkan.py', '파일전송과번역.md'):
                ölçü_verilənlər.add(str(Project_kök / 상대경로), arcname='jkoros-native/' + 상대경로)
            for Ad in ('crt.o', 'aot-runtime.o', 'ümumi_dil_icrası_Dəstək.o', 'İcra_Et.o', '미리번역.o', 'geri_qaytarmaq_körpü.o'):
                təyinat_faylı = Project_kök / 'build/ccompiler' / Ad
                ölçü_verilənlər.add(str(təyinat_faylı), arcname='jkoros-native/relink/' + Ad)
            for Ad in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                ölçü_verilənlər.add(str(Project_kök / 'build/user' / Ad), arcname='jkoros-native/relink/user/' + Ad)
            ölçü_verilənlər.add(str(Project_kök / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            ölçü_verilənlər.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    İcra_Et()
