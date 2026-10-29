"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def crearCompiladorC(rutaRaíz, rutaRepositorio, CompiladorC, herramientaEnlazador, bitsConfiguración, ejecutarComando):
    datosResultado = rutaRaíz / 'build/ccompiler'; datosResultado.mkdir(exist_ok=True)
    datosOriginal = rutaRaíz / 'CompiladorC'
    origenSuperior = rutaRaíz / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    juegoHerramientasDesarrollo = rutaRaíz / 'vendor/sdk'
    if not (juegoHerramientasDesarrollo/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    elementosIntegrados = sorted((juegoHerramientasDesarrollo/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not elementosIntegrados: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    bitsConfiguración = [valorAjustes for valorAjustes in bitsConfiguración if valorAjustes != '-mgeneral-regs-only']
    inclusiones = ['-I', datosOriginal, '-I', origenSuperior, '-I', rutaRaíz/'Usuario', '-I', datosResultado, '-isystem', juegoHerramientasDesarrollo/'usr/include']
    ejecutarComando([CompiladorC]+bitsConfiguración+['-ffunction-sections','-fdata-sections']+inclusiones+['-c',datosOriginal/'soporteInicioSistema.c','-o',datosResultado/'crt.o'])
    ejecutarComando([CompiladorC]+bitsConfiguración+['-I',rutaRepositorio/'posix-kor/arm64-native/Encabezados']+inclusiones+['-c',datosOriginal/'entornoEjecuciónCompilaciónAnticipada.c','-o',datosResultado/'aot-runtime.o'])
    recursosVisuales = [('/sdk/include/'+posiciónDatos.name,posiciónDatos) for posiciónDatos in sorted((rutaRepositorio/'posix-kor/arm64-native/Encabezados').glob('*.h'))]
    recursosVisuales += [('/sdk/include/'+posiciónDatos.name,posiciónDatos) for posiciónDatos in sorted((origenSuperior/'include').glob('*.h'))]
    recursosVisuales += [('/sdk/include/'+posiciónDatos.name,posiciónDatos) for posiciónDatos in sorted((datosOriginal/'encabezadosDesarrollo').glob('*.h'))]
    recursosVisuales += [('/sdk/lib/start.o',rutaRaíz/'build/user/start.o'),('/sdk/lib/crt.o',datosResultado/'crt.o'),('/sdk/lib/aot-runtime.o',datosResultado/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',rutaRaíz/'build/libposix-kor-user.a')]
    valorEncabezado=['typedef struct { const char *nombre; const unsigned char *Datos; unsigned tamaño; } recursoCompilador;']
    for índiceOrdinal,(_,ruta) in enumerate(recursosVisuales):
        valorEncabezado.append('static const unsigned char 탑재자원_%d[] = {%s};'%(índiceOrdinal,','.join(str(datosTemporal) for datosTemporal in ruta.read_bytes())))
    valorEncabezado.append('static const recursoCompilador recursosCompilador[] = {')
    for índiceOrdinal,(nombre,ruta) in enumerate(recursosVisuales): valorEncabezado.append('{%s, 탑재자원_%d, %d},'%(json.dumps(nombre,ensure_ascii=False),índiceOrdinal,ruta.stat().st_size))
    valorEncabezado.append('};');(datosResultado/'resources.h').write_text('\n'.join(valorEncabezado)+'\n',encoding='utf-8')
    archivosDestino=[]
    for nombre in ('herramientaCompilador.c','SoporteEntornoEjecución.c','ponerEnMarcha.c','tiempoDeAnticipado.c','puenteRetornar.S'):
        archivoDestino=datosResultado/(Path(nombre).stem+'.o');archivosDestino.append(archivoDestino)
        ejecutarComando([CompiladorC]+bitsConfiguración+['-ffunction-sections','-fdata-sections']+inclusiones+['-c',datosOriginal/nombre,'-o',archivoDestino])
    archivoCódigoEjecutable=rutaRaíz/'build/user/cc.elf'
    ejecutarComando([herramientaEnlazador,'--gc-sections','-T',rutaRaíz/'Usuario/DisposiciónEnlace.ld','-z','max-page-size=4096','-o',archivoCódigoEjecutable,
         rutaRaíz/'build/user/start.o',rutaRaíz/'build/user/runtime.o']+archivosDestino+
         [rutaRaíz/'build/user'/nombre for nombre in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[elementosIntegrados[-1]])
