#!/usr/bin/env python3
"""libclang Declaraciones·referencia 위치를 수집한다. valorExterno 헤더의 멤버는 변환하지 않는다."""
import ctypes as fuenteC
import hashlib
import json
from pathlib import Path

raízProyecto = Path(__file__).resolve().parents[1]
implementación = fuenteC.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class Cadena(fuenteC.Structure): _fields_ = [('Datos',fuenteC.c_void_p),('mostrarValor',fuenteC.c_uint)]
class valorCursor(fuenteC.Structure): _fields_ = [('valorClaseTipo',fuenteC.c_uint),('valorAuxiliar',fuenteC.c_int),('Datos',fuenteC.c_void_p*3)]
class posición(fuenteC.Structure): _fields_ = [('Datos',fuenteC.c_void_p*2),('valorDesfase',fuenteC.c_uint)]
def Función(nombre, resultadoRetornar, *argumentos):
    valorEntradaElemento = getattr(implementación, nombre); valorEntradaElemento.restype = resultadoRetornar; valorEntradaElemento.argtypes = list(argumentos); return valorEntradaElemento
obtenerTexto = Función('clang_getCString',fuenteC.c_char_p,Cadena)
liberarTexto = Función('clang_disposeString',None,Cadena)
def texto(valor):
    resultado = (obtenerTexto(valor) or b'').decode('utf-8'); liberarTexto(valor); return resultado
obtenerNombre = Función('clang_getCursorSpelling',Cadena,valorCursor)
obtenerReferencia = Función('clang_getCursorReferenced',valorCursor,valorCursor)
obtenerPosición = Función('clang_getCursorLocation',posición,valorCursor)
posiciónArchivo = Función('clang_getFileLocation',None,posición,fuenteC.POINTER(fuenteC.c_void_p),fuenteC.POINTER(fuenteC.c_uint),fuenteC.POINTER(fuenteC.c_uint),fuenteC.POINTER(fuenteC.c_uint))
nombreEntradaElementoArchivo = Función('clang_getFileName',Cadena,fuenteC.c_void_p)
nombreÚnico = Función('clang_getCursorUSR',Cadena,valorCursor)
claseTipoConexión = Función('clang_getCursorLinkage',fuenteC.c_uint,valorCursor)
tipoVisitado = fuenteC.CFUNCTYPE(fuenteC.c_uint,valorCursor,valorCursor,fuenteC.c_void_p)
visitarValor = Función('clang_visitChildren',fuenteC.c_uint,valorCursor,tipoVisitado,fuenteC.c_void_p)
generar = Función('clang_createIndex',fuenteC.c_void_p,fuenteC.c_int,fuenteC.c_int)
examinarValor = Función('clang_parseTranslationUnit',fuenteC.c_void_p,fuenteC.c_void_p,fuenteC.c_char_p,fuenteC.POINTER(fuenteC.c_char_p),fuenteC.c_int,fuenteC.c_void_p,fuenteC.c_uint,fuenteC.c_uint)
valorRaíz = Función('clang_getTranslationUnitCursor',valorCursor,fuenteC.c_void_p)
programaTerminarSesión = Función('clang_disposeTranslationUnit',None,fuenteC.c_void_p)
númeroElementosDiagnóstico = Función('clang_getNumDiagnostics',fuenteC.c_uint,fuenteC.c_void_p)
obtenerDiagnóstico = Función('clang_getDiagnostic',fuenteC.c_void_p,fuenteC.c_void_p,fuenteC.c_uint)
valorGravedad = Función('clang_getDiagnosticSeverity',fuenteC.c_uint,fuenteC.c_void_p)
mensajeDiagnóstico = Función('clang_getDiagnosticSpelling',Cadena,fuenteC.c_void_p)
liberarDiagnóstico = Función('clang_disposeDiagnostic',None,fuenteC.c_void_p)

def índicePosición(valorEntradaElemento):
    Archivo = fuenteC.c_void_p(); línea = fuenteC.c_uint(); entradaElementoRanura = fuenteC.c_uint(); valorDesfase = fuenteC.c_uint()
    posiciónArchivo(obtenerPosición(valorEntradaElemento),fuenteC.byref(Archivo),fuenteC.byref(línea),fuenteC.byref(entradaElementoRanura),fuenteC.byref(valorDesfase))
    return (texto(nombreEntradaElementoArchivo(Archivo)) if Archivo else '', valorDesfase.value, línea.value)

def ejecutarComando():
    índiceBuscar = generar(0,0); listaDeclaraciones = {}; listaReferencias = []; errores = []
    # herramientaCompilador.c는 propio Declaraciones 없이 TinyCC valorExterno 단일 traducirFuente 단위만 포함한다.
    # valorExterno 선언을 propio 이름으로 세지 않으며, datosEfectivo 빌드에서는 procesamientoContinuar 컴파일한다.
    archivoPropioRecurso = {str(ruta.resolve()) for ruta in raízProyecto.rglob('*') if ruta.suffix in ('.c','.h','.cpp','.inc')
              and not set(ruta.relative_to(raízProyecto).parts)&{'build','dist','vendor','__pycache__'}
              and ruta.relative_to(raízProyecto).as_posix() != 'CompiladorC/herramientaCompilador.c'}
    valorComún = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(raízProyecto/'Usuario'),
          '-I'+str(raízProyecto.parents[1]/'posix-kor/arm64-native/Encabezados'),'-I'+str(raízProyecto/'build'),'-I'+str(raízProyecto/'build/user'),
          '-I'+str(raízProyecto/'build/remote'),'-I'+str(raízProyecto/'vendor/bearssl/inc'),
          '-I'+str(raízProyecto/'vendor/bearssl/src'),'-I'+str(raízProyecto/'vendor/libassh/src'),
          '-I'+str(raízProyecto/'vendor/lwip/src/include'),'-I'+str(raízProyecto/'PilaRed'),
          '-I'+str(raízProyecto/'valorRemoto'),'-I'+str(raízProyecto/'CompiladorC')]
    for ruta in sorted(Path(nombre) for nombre in archivoPropioRecurso if nombre.endswith(('.c','.cpp'))):
        argumentos = valorComún + ['-std=c++11' if ruta.suffix=='.cpp' else '-std=c11']
        if 'PilaRed' in ruta.parts: argumentos += ['-I'+str(raízProyecto/'PilaRed'),'-I'+str(raízProyecto/'vendor/lwip/src/include')]
        if 'CompiladorC' in ruta.parts:
            argumentos += ['-I'+str(raízProyecto/'CompiladorC'),'-I'+str(raízProyecto/'vendor/tinycc'),'-I'+str(raízProyecto/'build/ccompiler'),
                    '-isystem',str(raízProyecto.parent/'rpi4/build/rootfs/usr/include')]
        if 'puentePython' in ruta.parts:
            argumentos += ['-I'+str(raízProyecto/'puentePython'),'-I'+str(raízProyecto/'build/micropython-1.24.1'),'-I'+str(raízProyecto/'build/python'),'-isystem','/usr/include/newlib']
        if 'valorRemoto' in ruta.parts:
            argumentos += ['-isystem', '/usr/include/newlib']
        if 'valorDistribución' in ruta.parts: argumentos += ['-D__JKOROS__=1']
        if ruta.name=='Paquete.c': argumentos += ['-I'+str(raízProyecto/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        valorGrupo = (fuenteC.c_char_p*len(argumentos))(*[valorEntradaElemento.encode() for valorEntradaElemento in argumentos])
        unidadTraducción = examinarValor(índiceBuscar,str(ruta).encode(),valorGrupo,len(argumentos),None,0,1)
        for número in range(númeroElementosDiagnóstico(unidadTraducción)):
            valorDiagnóstico = obtenerDiagnóstico(unidadTraducción,número)
            if valorGravedad(valorDiagnóstico)>=3: errores.append((str(ruta.relative_to(raízProyecto)),texto(mensajeDiagnóstico(valorDiagnóstico))))
            liberarDiagnóstico(valorDiagnóstico)
        @tipoVisitado
        def inspeccionarValor(valorEntradaElemento,valorPadre,Datos):
            Archivo,valorDesfase,línea = índicePosición(valorEntradaElemento)
            if Archivo not in archivoPropioRecurso: return 2 if valorEntradaElemento.valorClaseTipo==300 else 1
            palabraLéxico = texto(obtenerNombre(valorEntradaElemento))
            if not palabraLéxico or any(ord(valorCarácter)>127 for valorCarácter in palabraLéxico): return 2
            if valorEntradaElemento.valorClaseTipo in (2,3,4,5,6,7,8,9,10,20,21,501):
                valorÚnico = texto(nombreÚnico(valorEntradaElemento)) or Archivo+':'+str(valorDesfase)
                listaDeclaraciones[valorÚnico] = {'Archivo':Archivo,'valorDesfase':valorDesfase,'línea':línea,'valorClaseTipo':valorEntradaElemento.valorClaseTipo,'nombre':palabraLéxico,'conectar':claseTipoConexión(valorEntradaElemento)}
                listaReferencias.append((Archivo,valorDesfase,palabraLéxico,valorÚnico))
            else:
                referencia = obtenerReferencia(valorEntradaElemento)
                archivoReferencia,_,_ = índicePosición(referencia)
                if archivoReferencia in archivoPropioRecurso:
                    valorÚnico = texto(nombreÚnico(referencia)); listaReferencias.append((Archivo,valorDesfase,texto(obtenerNombre(referencia)),valorÚnico))
            return 2
        visitarValor(valorRaíz(unidadTraducción),inspeccionarValor,None)
        programaTerminarSesión(unidadTraducción)
    valorDestino = raízProyecto/'build/한국어화/시언어분석.json'
    valorDestino.parent.mkdir(parents=True, exist_ok=True)
    listaResúmenesHash = {Archivo:hashlib.sha256(Path(Archivo).read_bytes()).hexdigest() for Archivo in sorted(archivoPropioRecurso)}
    valorDestino.write_text(json.dumps({'Declaraciones':listaDeclaraciones,'referencia':listaReferencias,'error':errores,'원문해시':listaResúmenesHash},ensure_ascii=False,indent=2)+'\n')
    print('Declaraciones',len(listaDeclaraciones),'referencia',len(listaReferencias),'error',len(errores))
    for error in errores: print(*error)

if __name__=='__main__': ejecutarComando()
