#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from executar_comando import Project_raíz


def Executar_2():
    배포경로 = Project_raíz / 'dist'
    배포경로.mkdir(exist_ok=True)
    포직스경로 = Project_raíz.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(Project_raíz / 'build')) as 작업경로:
        개발꾸러미 = Path(작업경로) / 'jkoros-native-sdk'
        Ficheiro_Lista = {
            Project_raíz.parents[1] / 'LICENSE': 'LICENSE',
            Project_raíz.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            Project_raíz / 'Ferramentas/개발꾸러미번역.py': 'compile.py',
            Project_raíz / 'usuario/호출.h': 'include/호출.h',
            Project_raíz / '명명/기계연결이름.h': '명명/기계연결이름.h',
            Project_raíz / 'usuario/Ligar_deseño.ld': 'user.ld',
            포직스경로 / '포함/파일규약.h': 'include/파일규약.h',
            포직스경로 / '포함/통신규약.h': 'include/통신규약.h',
            Project_raíz / 'build/user/start.o': 'lib/start.o',
            Project_raíz / 'build/user/runtime.o': 'lib/runtime.o',
            Project_raíz / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            Project_raíz / 'usuario/파일예제.cpp': 'examples/파일예제.cpp',
            Project_raíz / '예제/한글코딩/인사.c': 'examples/인사.c',
            Project_raíz / '예제/한글코딩/fluxo_VALOR.c': 'examples/fluxo_VALOR.c',
            Project_raíz / '예제/한글코딩/인사.cpp': 'examples/인사.cpp',
            Project_raíz / 'usuario/통신예제.cpp': 'examples/통신예제.cpp',
            Project_raíz / 'build/user/demo.elf': 'examples/demo.elf',
            Project_raíz / 'build/user/network.elf': 'examples/network.elf',
        }
        꾸러미명세 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, obxectivo_VALOR in Ficheiro_Lista.items():
            destino_datos_ENDEREZO = 개발꾸러미 / obxectivo_VALOR
            destino_datos_ENDEREZO.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(destino_datos_ENDEREZO))
            꾸러미명세['sha256'][obxectivo_VALOR] = hashlib.sha256(destino_datos_ENDEREZO.read_bytes()).hexdigest()
        (개발꾸러미 / 'manifest.json').write_text(json.dumps(꾸러미명세, indent=2) + '\n')
        (개발꾸러미 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/파일예제.cpp -o demo.elf\n'
            'python3 compile.py examples/인사.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int START_usuario_apl(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Ferramentas/executar_comando.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Ferramentas/executar_Ficheiro.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: usuario_argumento_CONTAR()/usuario_argumento() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        Arquivo = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(Arquivo), 'w:gz') as medida_datos:
            medida_datos.add(str(개발꾸러미), arcname=개발꾸러미.name)
        Arquivo.replace(배포경로 / Arquivo.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        번역기꾸러미 = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(번역기꾸러미), 'w:gz') as medida_datos:
            for Nome in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                medida_datos.add(str(Project_raíz.parents[1] / Nome), arcname='jkoros-native/' + Nome)
            for 상대경로 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', '시언어번역기', 'usuario', '명명',
                             'Ferramentas/시언어번역기빌드.py', 'Ferramentas/compilar_usuario_espazo.py', '파일전송과번역.md'):
                medida_datos.add(str(Project_raíz / 상대경로), arcname='jkoros-native/' + 상대경로)
            for Nome in ('crt.o', 'aot-runtime.o', '실행지원.o', 'Executar_2.o', '미리번역.o', 'devolver_ponte.o'):
                ficheiro_de_destino = Project_raíz / 'build/ccompiler' / Nome
                medida_datos.add(str(ficheiro_de_destino), arcname='jkoros-native/relink/' + Nome)
            for Nome in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                medida_datos.add(str(Project_raíz / 'build/user' / Nome), arcname='jkoros-native/relink/user/' + Nome)
            medida_datos.add(str(Project_raíz / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            medida_datos.add(str(포직스경로), arcname='posix-kor/arm64-native')
        번역기꾸러미.replace(배포경로 / 번역기꾸러미.name)
    print('SDK:', 배포경로 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    Executar_2()
