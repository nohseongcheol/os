#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from Esegui_comando import azione_radice


def avvia():
    distribuzione_percorso = azione_radice / 'dist'
    distribuzione_percorso.mkdir(exist_ok=True)
    포직스경로 = azione_radice.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(azione_radice / 'build')) as 작업경로:
        kit_di_sviluppo = Path(작업경로) / 'jkoros-native-sdk'
        elenco_file = {
            azione_radice.parents[1] / 'LICENSE': 'LICENSE',
            azione_radice.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            azione_radice / 'strumenti/SDK_compilare.py': 'compile.py',
            azione_radice / 'spazio_utente/호출.h': 'include/호출.h',
            azione_radice / '명명/기계연결이름.h': '명명/기계연결이름.h',
            azione_radice / 'spazio_utente/disposizione_di_collegamento.ld': 'user.ld',
            포직스경로 / 'dichiarazioni/File_ABI.h': 'include/File_ABI.h',
            포직스경로 / 'dichiarazioni/rete_ABI.h': 'include/rete_ABI.h',
            azione_radice / 'build/user/start.o': 'lib/start.o',
            azione_radice / 'build/user/runtime.o': 'lib/runtime.o',
            azione_radice / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            azione_radice / 'spazio_utente/EsempioFile.cpp': 'examples/EsempioFile.cpp',
            azione_radice / '예제/한글코딩/messaggio_di_saluto_ae353e94.c': 'examples/messaggio_di_saluto_ae353e94.c',
            azione_radice / '예제/한글코딩/Stream_VALORE.c': 'examples/Stream_VALORE.c',
            azione_radice / '예제/한글코딩/messaggio_di_saluto_ae353e94.cpp': 'examples/messaggio_di_saluto_ae353e94.cpp',
            azione_radice / 'spazio_utente/통신예제.cpp': 'examples/통신예제.cpp',
            azione_radice / 'build/user/demo.elf': 'examples/demo.elf',
            azione_radice / 'build/user/network.elf': 'examples/network.elf',
        }
        aggregare_manifesto = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, target in elenco_file.items():
            meta_dati_e_mail = kit_di_sviluppo / target
            meta_dati_e_mail.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(meta_dati_e_mail))
            aggregare_manifesto['sha256'][target] = hashlib.sha256(meta_dati_e_mail.read_bytes()).hexdigest()
        (kit_di_sviluppo / 'manifest.json').write_text(json.dumps(aggregare_manifesto, indent=2) + '\n')
        (kit_di_sviluppo / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/EsempioFile.cpp -o demo.elf\n'
            'python3 compile.py examples/messaggio_di_saluto_ae353e94.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int START_USER_app(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: strumenti/Esegui_comando.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 strumenti/Esegui_File.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: USER_argomento_CONTA_NUMERI()/USER_argomento() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Archivio = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Archivio), 'w:gz') as KR_dati:
            KR_dati.add(str(kit_di_sviluppo), arcname=kit_di_sviluppo.name)
        Archivio.replace(distribuzione_percorso / Archivio.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        compilatore_Archivio = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(compilatore_Archivio), 'w:gz') as KR_dati:
            for Nome in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                KR_dati.add(str(azione_radice.parents[1] / Nome), arcname='jkoros-native/' + Nome)
            for percorso_relativo in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', 'C_compilatore', 'spazio_utente', '명명',
                             'strumenti/BLD_C_compilatore.py', 'strumenti/BLD_USER_Space.py', '파일전송과번역.md'):
                KR_dati.add(str(azione_radice / percorso_relativo), arcname='jkoros-native/' + percorso_relativo)
            for Nome in ('crt.o', 'aot-runtime.o', 'CLR_Supporto.o', 'avvia.o', '미리번역.o', 'Reso_bridge.o'):
                file_di_destinazione = azione_radice / 'build/ccompiler' / Nome
                KR_dati.add(str(file_di_destinazione), arcname='jkoros-native/relink/' + Nome)
            for Nome in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                KR_dati.add(str(azione_radice / 'build/user' / Nome), arcname='jkoros-native/relink/user/' + Nome)
            KR_dati.add(str(azione_radice / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            KR_dati.add(str(포직스경로), arcname='posix-kor/arm64-native')
        compilatore_Archivio.replace(distribuzione_percorso / compilatore_Archivio.name)
    print('SDK:', distribuzione_percorso / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    avvia()
