#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from végrehajt_parancs import teendő_gyök


def Futtatás():
    elosztás_útvonal = teendő_gyök / 'dist'
    elosztás_útvonal.mkdir(exist_ok=True)
    포직스경로 = teendő_gyök.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(teendő_gyök / 'build')) as 작업경로:
        fejlesztőkészlet = Path(작업경로) / 'jkoros-native-sdk'
        fájllista = {
            teendő_gyök.parents[1] / 'LICENSE': 'LICENSE',
            teendő_gyök.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            teendő_gyök / 'Eszközök/SDK_épít.py': 'compile.py',
            teendő_gyök / 'felhasználó/호출.h': 'include/호출.h',
            teendő_gyök / '명명/기계연결이름.h': '명명/기계연결이름.h',
            teendő_gyök / 'felhasználó/csatol_Navigáció.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            teendő_gyök / 'build/user/start.o': 'lib/start.o',
            teendő_gyök / 'build/user/runtime.o': 'lib/runtime.o',
            teendő_gyök / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            teendő_gyök / 'felhasználó/FájlPélda.cpp': 'examples/FájlPélda.cpp',
            teendő_gyök / '예제/한글코딩/인사.c': 'examples/인사.c',
            teendő_gyök / '예제/한글코딩/Stream_ÉRTÉK.c': 'examples/Stream_ÉRTÉK.c',
            teendő_gyök / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            teendő_gyök / 'felhasználó/통신예제.cpp': 'examples/통신예제.cpp',
            teendő_gyök / 'build/user/demo.elf': 'examples/demo.elf',
            teendő_gyök / 'build/user/network.elf': 'examples/network.elf',
        }
        köteg_jegyzékfájl = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, cél in fájllista.items():
            cél_adat_CÍM = fejlesztőkészlet / cél
            cél_adat_CÍM.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(cél_adat_CÍM))
            köteg_jegyzékfájl['sha256'][cél] = hashlib.sha256(cél_adat_CÍM.read_bytes()).hexdigest()
        (fejlesztőkészlet / 'manifest.json').write_text(json.dumps(köteg_jegyzékfájl, indent=2) + '\n')
        (fejlesztőkészlet / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/FájlPélda.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int START_felhasználó_app(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Eszközök/végrehajt_parancs.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Eszközök/végrehajt_Fájl.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: felhasználó_argumentum_DARAB()/felhasználó_argumentum() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        archív = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(archív), 'w:gz') as KR_adat:
            KR_adat.add(str(fejlesztőkészlet), arcname=fejlesztőkészlet.name)
        archív.replace(elosztás_útvonal / archív.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        fordítóprogram_archív = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(fordítóprogram_archív), 'w:gz') as KR_adat:
            for Név in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                KR_adat.add(str(teendő_gyök.parents[1] / Név), arcname='jkoros-native/' + Név)
            for relatív_elérési_út in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', 'C_fordítóprogram', 'felhasználó', '명명',
                             'Eszközök/épít_C_fordítóprogram.py', 'Eszközök/épít_felhasználó_tér.py', '파일전송과번역.md'):
                KR_adat.add(str(teendő_gyök / relatív_elérési_út), arcname='jkoros-native/' + relatív_elérési_út)
            for Név in ('crt.o', 'aot-runtime.o', 'CLR_támogat.o', 'Futtatás.o', '미리번역.o', 'visszaküld_híd.o'):
                célfájl = teendő_gyök / 'build/ccompiler' / Név
                KR_adat.add(str(célfájl), arcname='jkoros-native/relink/' + Név)
            for Név in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                KR_adat.add(str(teendő_gyök / 'build/user' / Név), arcname='jkoros-native/relink/user/' + Név)
            KR_adat.add(str(teendő_gyök / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            KR_adat.add(str(포직스경로), arcname='posix-kor/arm64-native')
        fordítóprogram_archív.replace(elosztás_útvonal / fordítóprogram_archív.name)
    print('SDK:', elosztás_útvonal / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    Futtatás()
