#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from Executar_comando import ação_raiz


def iniciar():
    distribuição_caminho = ação_raiz / 'dist'
    distribuição_caminho.mkdir(exist_ok=True)
    포직스경로 = ação_raiz.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(ação_raiz / 'build')) as 작업경로:
        kit_de_desenvolvimento = Path(작업경로) / 'jkoros-native-sdk'
        lista_de_arquivos = {
            ação_raiz.parents[1] / 'LICENSE': 'LICENSE',
            ação_raiz.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            ação_raiz / 'ferramentas/SDK_compilar.py': 'compile.py',
            ação_raiz / 'espaço_do_utilizador/호출.h': 'include/호출.h',
            ação_raiz / '명명/기계연결이름.h': '명명/기계연결이름.h',
            ação_raiz / 'espaço_do_utilizador/disposição_de_ligação.ld': 'user.ld',
            포직스경로 / 'declarações/Arquivo_ABI.h': 'include/Arquivo_ABI.h',
            포직스경로 / 'declarações/rede_ABI.h': 'include/rede_ABI.h',
            ação_raiz / 'build/user/start.o': 'lib/start.o',
            ação_raiz / 'build/user/runtime.o': 'lib/runtime.o',
            ação_raiz / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            ação_raiz / 'espaço_do_utilizador/ExemploFicheiro.cpp': 'examples/ExemploFicheiro.cpp',
            ação_raiz / '예제/한글코딩/saudação_ae353e94.c': 'examples/saudação_ae353e94.c',
            ação_raiz / '예제/한글코딩/fluxo_VALOR.c': 'examples/fluxo_VALOR.c',
            ação_raiz / '예제/한글코딩/saudação_ae353e94.cpp': 'examples/saudação_ae353e94.cpp',
            ação_raiz / 'espaço_do_utilizador/통신예제.cpp': 'examples/통신예제.cpp',
            ação_raiz / 'build/user/demo.elf': 'examples/demo.elf',
            ação_raiz / 'build/user/network.elf': 'examples/network.elf',
        }
        grupo_manifesto = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 원본자료, meta in lista_de_arquivos.items():
            destino_dados_email = kit_de_desenvolvimento / meta
            destino_dados_email.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(원본자료), str(destino_dados_email))
            grupo_manifesto['sha256'][meta] = hashlib.sha256(destino_dados_email.read_bytes()).hexdigest()
        (kit_de_desenvolvimento / 'manifest.json').write_text(json.dumps(grupo_manifesto, indent=2) + '\n')
        (kit_de_desenvolvimento / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/ExemploFicheiro.cpp -o demo.elf\n'
            'python3 compile.py examples/saudação_ae353e94.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int START_usuário_app(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: ferramentas/Executar_comando.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 ferramentas/Executar_Arquivo.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: usuário_argumento_CONT_NÚM()/usuário_argumento() in 호출.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        arquivo = Path(작업경로) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(arquivo), 'w:gz') as RC_dados:
            RC_dados.add(str(kit_de_desenvolvimento), arcname=kit_de_desenvolvimento.name)
        arquivo.replace(distribuição_caminho / arquivo.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        compilador_arquivo = Path(작업경로) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(compilador_arquivo), 'w:gz') as RC_dados:
            for Nome in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                RC_dados.add(str(ação_raiz.parents[1] / Nome), arcname='jkoros-native/' + Nome)
            for caminho_relativo in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', 'C_compilador', 'espaço_do_utilizador', '명명',
                             'ferramentas/BLD_C_compilador.py', 'ferramentas/BLD_usuário_ESPAÇO.py', '파일전송과번역.md'):
                RC_dados.add(str(ação_raiz / caminho_relativo), arcname='jkoros-native/' + caminho_relativo)
            for Nome in ('crt.o', 'aot-runtime.o', 'SuporteExecução.o', 'iniciar.o', '미리번역.o', 'devolver_ponte.o'):
                arquivo_de_destino = ação_raiz / 'build/ccompiler' / Nome
                RC_dados.add(str(arquivo_de_destino), arcname='jkoros-native/relink/' + Nome)
            for Nome in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                RC_dados.add(str(ação_raiz / 'build/user' / Nome), arcname='jkoros-native/relink/user/' + Nome)
            RC_dados.add(str(ação_raiz / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            RC_dados.add(str(포직스경로), arcname='posix-kor/arm64-native')
        compilador_arquivo.replace(distribuição_caminho / compilador_arquivo.name)
    print('SDK:', distribuição_caminho / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    iniciar()
