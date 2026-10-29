#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from ejecutarComando import raízProyecto


def ponerEnMarcha():
    rutaDistribución = raízProyecto / 'dist'
    rutaDistribución.mkdir(exist_ok=True)
    pOSIX = raízProyecto.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(raízProyecto / 'build')) as rutaTrabajoEnCurso:
        juegoHerramientasDesarrollo = Path(rutaTrabajoEnCurso) / 'jkoros-native-sdk'
        listaArchivo = {
            raízProyecto.parents[1] / 'LICENSE': 'LICENSE',
            raízProyecto.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            raízProyecto / 'Herramientas/compilarSDK.py': 'compile.py',
            raízProyecto / 'Usuario/invocar.h': 'include/invocar.h',
            raízProyecto / 'denominación/nombresEnlazarMáquina.h': 'denominación/nombresEnlazarMáquina.h',
            raízProyecto / 'Usuario/DisposiciónEnlace.ld': 'user.ld',
            pOSIX / 'Encabezados/ABIArchivo.h': 'include/ABIArchivo.h',
            pOSIX / 'Encabezados/ABIRed.h': 'include/ABIRed.h',
            raízProyecto / 'build/user/start.o': 'lib/start.o',
            raízProyecto / 'build/user/runtime.o': 'lib/runtime.o',
            raízProyecto / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            raízProyecto / 'Usuario/EjemploArchivo.cpp': 'examples/EjemploArchivo.cpp',
            raízProyecto / 'Ejemplos/CodificaciónHangul/Saludo.c': 'examples/Saludo.c',
            raízProyecto / 'Ejemplos/CodificaciónHangul/valorFlujo.c': 'examples/valorFlujo.c',
            raízProyecto / 'Ejemplos/CodificaciónHangul/Saludo.cpp': 'examples/Saludo.cpp',
            raízProyecto / 'Usuario/EjemploComunicación.cpp': 'examples/EjemploComunicación.cpp',
            raízProyecto / 'build/user/demo.elf': 'examples/demo.elf',
            raízProyecto / 'build/user/network.elf': 'examples/network.elf',
        }
        manifiestoPaquete = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for datosOriginal, valorObjetivo in listaArchivo.items():
            direcciónDatosDestino = juegoHerramientasDesarrollo / valorObjetivo
            direcciónDatosDestino.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(datosOriginal), str(direcciónDatosDestino))
            manifiestoPaquete['sha256'][valorObjetivo] = hashlib.sha256(direcciónDatosDestino.read_bytes()).hexdigest()
        (juegoHerramientasDesarrollo / 'manifest.json').write_text(json.dumps(manifiestoPaquete, indent=2) + '\n')
        (juegoHerramientasDesarrollo / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/EjemploArchivo.cpp -o demo.elf\n'
            'python3 compile.py examples/Saludo.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int iniciarProgramaUsuario(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: Herramientas/ejecutarComando.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 Herramientas/ejecutarArchivo.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: númeroElementosArgumentoUsuario()/argumentoUsuario() in invocar.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        archivoComprimido = Path(rutaTrabajoEnCurso) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(archivoComprimido), 'w:gz') as datosResultado:
            datosResultado.add(str(juegoHerramientasDesarrollo), arcname=juegoHerramientasDesarrollo.name)
        archivoComprimido.replace(rutaDistribución / archivoComprimido.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        archivoComprimidoCompilador = Path(rutaTrabajoEnCurso) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(archivoComprimidoCompilador), 'w:gz') as datosResultado:
            for nombre in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                datosResultado.add(str(raízProyecto.parents[1] / nombre), arcname='jkoros-native/' + nombre)
            for rutaRelativo in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', 'CompiladorC', 'Usuario', 'denominación',
                             'Herramientas/construirCompiladorC.py', 'Herramientas/construirEspacioUsuario.py', 'CompilaciónYTransferenciaArchivo.md'):
                datosResultado.add(str(raízProyecto / rutaRelativo), arcname='jkoros-native/' + rutaRelativo)
            for nombre in ('crt.o', 'aot-runtime.o', 'SoporteEntornoEjecución.o', 'ponerEnMarcha.o', 'tiempoDeAnticipado.o', 'puenteRetornar.o'):
                archivoDestino = raízProyecto / 'build/ccompiler' / nombre
                datosResultado.add(str(archivoDestino), arcname='jkoros-native/relink/' + nombre)
            for nombre in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                datosResultado.add(str(raízProyecto / 'build/user' / nombre), arcname='jkoros-native/relink/user/' + nombre)
            datosResultado.add(str(raízProyecto / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            datosResultado.add(str(pOSIX), arcname='posix-kor/arm64-native')
        archivoComprimidoCompilador.replace(rutaDistribución / archivoComprimidoCompilador.name)
    print('SDK:', rutaDistribución / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    ponerEnMarcha()
