#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from Executa_ordre import Project_rel


def Executa_2():
    배포경로 = Project_rel / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = Project_rel.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(Project_rel / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        arxiu_Llista = {
            Project_rel.parents[1] / 'LICENSE': 'LICENSE',
            Project_rel.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            Project_rel / 'Eines/개발꾸러미번역.py': 'compile.py',
            Project_rel / 'usuari/호출.h': 'include/호출.h',
            Project_rel / '명명/기계연결이름.h': '명명/기계연결이름.h',
            Project_rel / 'usuari/enllaç_disseny.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            Project_rel / 'build/user/start.o': 'lib/start.o',
            Project_rel / 'build/user/runtime.o': 'lib/runtime.o',
            Project_rel / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            Project_rel / 'usuari/ExempleFitxer.cpp': 'examples/ExempleFitxer.cpp',
            Project_rel / '예제/한글코딩/인사.c': 'examples/인사.c',
            Project_rel / '예제/한글코딩/flux_VALOR.c': 'examples/flux_VALOR.c',
            Project_rel / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            Project_rel / 'usuari/통신예제.cpp': 'examples/통신예제.cpp',
            Project_rel / 'build/user/demo.elf': 'examples/demo.elf',
            Project_rel / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, objectiu in arxiu_Llista.items():
            destinació_dades_ADREÇA = 개발꾸러미 / objectiu
            destinació_dades_ADREÇA.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(destinació_dades_ADREÇA))
            꾸러미명세['sha256'][objectiu] = hashlib.sha256(destinació_dades_ADREÇA.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/ExempleFitxer.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int Inici_usuari_programa(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Eines/Executa_ordre.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Eines/Executa_arxiu.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: usuari_arg_COMPT()/usuari_arg() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Arxiu = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Arxiu), 'w:gz') as mesura_dades:
            mesura_dades.add(str(개발꾸러미), arcname=개발꾸러미.name)
        Arxiu.replace(배포경로 / Arxiu.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as mesura_dades:
            for Nom in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                mesura_dades.add(str(Project_rel.parents[1] / Nom), arcname='jkoros-native/' + Nom)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'usuari', '명명',
                             'Eines/시언어번역기빌드.py', 'Eines/generar_usuari_espai.py', '파일전송과번역.md'):
                mesura_dades.add(str(Project_rel / 상대경로), arcname='jkoros-native/' + 상대경로)
            for Nom in ('crt.o', 'aot-runtime.o', '실행지원.o', 'Executa_2.o', '미리번역.o', 'tornar_les_tasques_pont.o'):
                fitxer_de_destinació = Project_rel / 'build/ccompiler' / Nom
                mesura_dades.add(str(fitxer_de_destinació), arcname='jkoros-native/relink/' + Nom)
            for Nom in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                mesura_dades.add(str(Project_rel / 'build/user' / Nom), arcname='jkoros-native/relink/user/' + Nom)
            mesura_dades.add(str(Project_rel / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            mesura_dades.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    Executa_2()
