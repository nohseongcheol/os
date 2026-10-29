"""독립된 propio ABI ELF64와 로더 rechazarValor Pruebas 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from construirPython import crearPython
from construirBibliotecaJava import crearBibliotecaJava
from construirCompiladorC import crearCompiladorC


def crearEspacioUsuario(rutaRaíz, rutaRepositorio, CompiladorC, compiladorCpp, herramientaEnlazador, herramientaArchivoComprimido, bitsConfiguración, ejecutarComando):
    bitsConfiguración = [valorAjustes for valorAjustes in bitsConfiguración if valorAjustes != '-mgeneral-regs-only']
    construirRuta = rutaRaíz / 'build'
    salida = construirRuta / 'user'
    salida.mkdir(exist_ok=True)
    datosOriginal = rutaRaíz / 'Usuario'
    pOSIX = rutaRepositorio / 'posix-kor/arm64-native'
    rutaIncluir = ['-I', datosOriginal, '-I', pOSIX / 'Encabezados', '-I', salida]
    for herramientaCompilador, regiónAdicional, ruta, nombre in [
            (CompiladorC, [], datosOriginal / 'ponerEnMarcha.S', 'start.o'),
            (CompiladorC, ['-std=c11'], datosOriginal / 'ejecutarComando.c', 'runtime.o'),
            (CompiladorC, ['-std=c11'], pOSIX / 'puenteUsuario.c', 'posix.o'),
            (compiladorCpp, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], datosOriginal / 'EjemploArchivo.cpp', 'demo.o'),
            (compiladorCpp, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], datosOriginal / 'EjemploComunicación.cpp', 'network.o'),
            (CompiladorC, ['-std=c11'], datosOriginal / 'PruebaProtección.c', 'fault.o'),
            (CompiladorC, ['-std=c11'], datosOriginal / 'Editor.c', 'vi.o')]:
        ejecutarComando([herramientaCompilador] + bitsConfiguración + regiónAdicional + rutaIncluir + ['-Wall', '-Wextra', '-Werror', '-c', ruta, '-o', salida / nombre])
    ejecutarComando([herramientaArchivoComprimido, 'rcs', construirRuta / 'libposix-kor-user.a', salida / 'posix.o'])
    for nombre in ('demo', 'fault', 'network', 'vi'):
        ejecutarComando([herramientaEnlazador, '-T', datosOriginal / 'DisposiciónEnlace.ld', '-z', 'max-page-size=4096', '-o', salida / (nombre + '.elf'),
             salida / 'start.o', salida / 'runtime.o', salida / (nombre + '.o'), construirRuta / 'libposix-kor-user.a'])
    crearBibliotecaJava(rutaRaíz, ejecutarComando)
    # 기존 propio Java Compilador/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(construirRuta)) as rutaTrabajoEnCurso:
        rutaClase = Path(rutaTrabajoEnCurso)
        ejecutarComando(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', rutaClase, '-sourcepath', rutaClase, '-d', rutaClase] +
            [posiciónDatos for posiciónDatos in sorted((rutaRepositorio / 'os/Usuario/Java').glob('*.java')) if posiciónDatos.name != 'MáquinaVirtualJava.java'] + sorted((datosOriginal / 'Java').glob('*.java')))
        ejecutarComando(['sh', rutaRepositorio / 'compiler/tiempoDeAnticipado.sh', '--entry', 'EntradaElementoHerramienta.ponerEnMarcha',
             '--profile', 'user', '--heap-words', '1048576', '-o', salida / 'java-tools.c'] + sorted(rutaClase.glob('*.class')))
    bibliotecaDescompresión = rutaRaíz / 'vendor/uzlib'
    for ruta, nombre in [(salida / 'java-tools.c', 'java-tools.o'), (datosOriginal / 'puenteJava.c', 'java-link.o'),
                       (datosOriginal / 'Paquete.c', 'jar.o')] + [(bibliotecaDescompresión / (nombre + '.c'), nombre + '.o') for nombre in ('tinflate', 'crc32', 'adler32')]:
        ejecutarComando([CompiladorC] + bitsConfiguración + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', bibliotecaDescompresión] + rutaIncluir + ['-c', ruta, '-o', salida / nombre])
    ejecutarComando([herramientaEnlazador, '-T', datosOriginal / 'DisposiciónEnlace.ld', '-z', 'max-page-size=4096', '-o', salida / 'java-tools.elf'] +
        [salida / nombre for nombre in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    crearPython(rutaRaíz, CompiladorC, herramientaEnlazador)
    crearCompiladorC(rutaRaíz, rutaRepositorio, CompiladorC, herramientaEnlazador, bitsConfiguración, ejecutarComando)
    válido = (salida / 'demo.elf').read_bytes()
    desfaseEncabezadoPrograma = struct.unpack_from('<Q', válido, 32)[0]
    listaEncabezado = [desfaseEncabezadoPrograma + númeroElementosElementoLista * 56 for númeroElementosElementoLista in range(struct.unpack_from('<H', válido, 56)[0])]
    cargas = [posiciónDatos for posiciónDatos in listaEncabezado if struct.unpack_from('<I', válido, posiciónDatos)[0] == 1]
    texto, Datos = cargas[:2]
    direcciónComando = struct.unpack_from('<Q', válido, texto + 16)[0]
    direcciónDatos = struct.unpack_from('<Q', válido, Datos + 16)[0]
    ABILlamada = válido.index(b'JKOROS\0')
    pruebaCaso = [('empty', b''), ('short', válido[:63])]
    modificaciones = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', direcciónComando + 1), ('data-entry', 24, 'Q', direcciónDatos),
               ('outside-file', texto + 32, 'Q', len(válido) + 1), ('short-memory', texto + 40, 'Q', 1),
               ('kernel-address', texto + 16, 'Q', 0x80000), ('memory-overflow', texto + 40, 'Q', 2**64 - 1),
               ('writable-code', texto + 4, 'I', 7), ('missing-abi', ABILlamada, 'B', ord('X')),
               ('wrong-abi', ABILlamada + 8, 'I', 2), ('dynamic', texto, 'I', 2),
               ('unaligned-load', texto + 16, 'Q', direcciónComando + 8),
               ('overlap', Datos + 16, 'Q', direcciónComando)]
    for nombre, valorDesfase, formatoDatos, valor in modificaciones:
        cambiado = bytearray(válido); struct.pack_into('<' + formatoDatos, cambiado, valorDesfase, valor)
        pruebaCaso.append((nombre, bytes(cambiado)))
    bloquesBinarios = [(nombre.replace('-', '_'), salida / (nombre + '.elf')) for nombre in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for índiceBuscar, (nombre, datosCargaÚtil) in enumerate(pruebaCaso):
        ruta = salida / ('invalid-{}.elf'.format(nombre)); ruta.write_bytes(datosCargaÚtil)
        bloquesBinarios.append(('invalid_{}'.format(índiceBuscar), ruta))
    ensamblador, valorEncabezado = ['.section .rodata.user,"a"'], []
    tamaños = {}
    for nombre, ruta in bloquesBinarios:
        valorSímbolo = 'user_blob_' + nombre
        tamaños[nombre] = ruta.stat().st_size
        # 생성한 valorParRed 경로만 넣어 프로젝트 경로의 공백/comilla 영향을 피한다.
        ensamblador += ['.balign 16', '.global ' + valorSímbolo, valorSímbolo + ':', '.incbin "{}"'.format(ruta.relative_to(rutaRaíz))]
        valorEncabezado.append('extern const unsigned char {}[];'.format(valorSímbolo))
    ensamblador.append('.section .note.GNU-stack,"",%progbits')
    valorEncabezado += ['static const programa entradasCódigoEjecutable[] = {', '{user_blob_demo, %d, 0},' % tamaños['demo']]
    valorEncabezado += ['{user_blob_fault, %d, %d},' % (tamaños['fault'], valorReenviado) for valorReenviado in range(8)]
    valorEncabezado += ['{user_blob_network, %d, 0},' % tamaños['network']]
    valorEncabezado += ['{user_blob_java_tools, %d, %d},' % (tamaños['java_tools'], modoMétodo) for modoMétodo in (0, 1)]
    valorEncabezado += ['{user_blob_python, %d, 0},' % tamaños['python'], '{user_blob_vi, %d, 0},' % tamaños['vi']]
    valorEncabezado += ['{user_blob_java_tools, %d, 2},' % tamaños['java_tools']]
    valorEncabezado += ['{user_blob_cc, %d, 0},' % tamaños['cc']]
    valorEncabezado += ['{user_blob_cc, %d, 1},' % tamaños['cc']]
    valorEncabezado += ['};', 'static const programa ejecutablesInválido[] = {']
    valorEncabezado += ['{user_blob_invalid_%d, %d, 0},' % (índiceOrdinal, len(datosCargaÚtil)) for índiceOrdinal, (_, datosCargaÚtil) in enumerate(pruebaCaso)]
    valorEncabezado += ['};']
    (construirRuta / 'programs.S').write_text('\n'.join(ensamblador) + '\n')
    (construirRuta / 'programs.h').write_text('\n'.join(valorEncabezado) + '\n')
    (salida / 'invalid-cases.txt').write_text('\n'.join(nombre for nombre, _ in pruebaCaso) + '\n')
    ejecutarComando([CompiladorC] + bitsConfiguración + ['-c', construirRuta / 'programs.S', '-o', construirRuta / 'programs.o'])
