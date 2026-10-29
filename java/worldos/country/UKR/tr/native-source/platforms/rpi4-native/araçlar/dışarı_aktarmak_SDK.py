#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from yürütmek_komut import işlem_kök


def çalıştır():
    dağıtım_yol = işlem_kök / 'dist'
    dağıtım_yol.mkdir(exist_ok=True)
    포직스경로 = işlem_kök.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(işlem_kök / 'build')) as 작업경로:
        geliştirme_seti = Path(작업경로) / 'jkoros-native-sdk'
        dosya_listesi = {
            işlem_kök.parents[1] / 'LICENSE': 'LICENSE',
            işlem_kök.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            işlem_kök / 'araçlar/SDK_derlemek.py': 'compile.py',
            işlem_kök / 'kullanıcı_alanı/호출.h': 'include/호출.h',
            işlem_kök / '명명/기계연결이름.h': '명명/기계연결이름.h',
            işlem_kök / 'kullanıcı_alanı/bağlama_düzeni.ld': 'user.ld',
            포직스경로 / 'bildirimler/Dosya_ABI.h': 'include/Dosya_ABI.h',
            포직스경로 / 'bildirimler/ağ_ABI.h': 'include/ağ_ABI.h',
            işlem_kök / 'build/user/start.o': 'lib/start.o',
            işlem_kök / 'build/user/runtime.o': 'lib/runtime.o',
            işlem_kök / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            işlem_kök / 'kullanıcı_alanı/DosyaÖrneği.cpp': 'examples/DosyaÖrneği.cpp',
            işlem_kök / '예제/한글코딩/인사.c': 'examples/인사.c',
            işlem_kök / '예제/한글코딩/akış_değer.c': 'examples/akış_değer.c',
            işlem_kök / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            işlem_kök / 'kullanıcı_alanı/통신예제.cpp': 'examples/통신예제.cpp',
            işlem_kök / 'build/user/demo.elf': 'examples/demo.elf',
            işlem_kök / 'build/user/network.elf': 'examples/network.elf',
        }
        paket_iş_bildirim = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, hedef in dosya_listesi.items():
            hedef_veri_ADRES = geliştirme_seti / hedef
            hedef_veri_ADRES.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(hedef_veri_ADRES))
            paket_iş_bildirim['sha256'][hedef] = hashlib.sha256(hedef_veri_ADRES.read_bytes()).hexdigest()
        (geliştirme_seti / 'manifest.json').write_text(json.dumps(paket_iş_bildirim, indent=2) + '\n')
        (geliştirme_seti / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/DosyaÖrneği.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int Start_kullanıcı_program(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: araçlar/yürütmek_komut.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 araçlar/yürütmek_Dosya.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: kullanıcı_bağımsız_değişken_BAĞ_DEĞ_SAY()/kullanıcı_bağımsız_değişken() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Arşiv = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Arşiv), 'w:gz') as KR_veri:
            KR_veri.add(str(geliştirme_seti), arcname=geliştirme_seti.name)
        Arşiv.replace(dağıtım_yol / Arşiv.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        derleyici_Arşiv = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(derleyici_Arşiv), 'w:gz') as KR_veri:
            for İsim in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                KR_veri.add(str(işlem_kök.parents[1] / İsim), arcname='jkoros-native/' + İsim)
            for göreli_yol in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', 'C_derleyici', 'kullanıcı_alanı', '명명',
                             'araçlar/BLD_C_derleyici.py', 'araçlar/BLD_kullanıcı_yer.py', '파일전송과번역.md'):
                KR_veri.add(str(işlem_kök / göreli_yol), arcname='jkoros-native/' + göreli_yol)
            for İsim in ('crt.o', 'aot-runtime.o', 'CLR_Destek.o', 'çalıştır.o', '미리번역.o', 'İade_köprü.o'):
                hedef_dosya = işlem_kök / 'build/ccompiler' / İsim
                KR_veri.add(str(hedef_dosya), arcname='jkoros-native/relink/' + İsim)
            for İsim in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                KR_veri.add(str(işlem_kök / 'build/user' / İsim), arcname='jkoros-native/relink/user/' + İsim)
            KR_veri.add(str(işlem_kök / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            KR_veri.add(str(포직스경로), arcname='posix-kor/arm64-native')
        derleyici_Arşiv.replace(dağıtım_yol / derleyici_Arşiv.name)
    print('SDK:', dağıtım_yol / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    çalıştır()
