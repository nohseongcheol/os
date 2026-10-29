#!/usr/bin/env python3
"""denominación recortar·excepción·경로를 검사한다. --시언어는 libclang Declaraciones 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

raízProyecto = Path(__file__).resolve().parents[1]
raízRepositorio = raízProyecto.parents[1]

def ponerEnMarcha():
    Analizador = argparse.ArgumentParser(description=__doc__)
    Analizador.add_argument('--lenguaC', action='store_true')
    argumentos = Analizador.parse_args()
    fallos = []
    valorContrato = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    númeroElementosArchivo = 0
    tablaParámetro = {}
    funciónArgumentosVariables = set()
    nodosAST = {}
    compiladoresCompartido = [raízRepositorio/'compiler/Compilador.py', raízRepositorio/'compiler/CompilaciónAnticipada.py']
    for ruta in list((raízProyecto/'Herramientas').glob('*.py')) + list((raízProyecto/'Ejemplos').rglob('*.py')) + compiladoresCompartido:
        if ruta.name.endswith(('이름반영.py', '이름분석.py')): continue
        númeroElementosArchivo += 1
        nodoAST = ast.parse(ruta.read_text()); nodosAST[ruta] = nodoAST
        for valorEntradaElemento in ast.walk(nodoAST):
            if isinstance(valorEntradaElemento, ast.FunctionDef):
                tablaParámetro.setdefault(valorEntradaElemento.name, set()).update(argumentoParámetro.arg for argumentoParámetro in valorEntradaElemento.args.args + valorEntradaElemento.args.kwonlyargs)
                if valorEntradaElemento.args.kwarg: funciónArgumentosVariables.add(valorEntradaElemento.name)
            if isinstance(valorEntradaElemento, ast.ClassDef):
                for Función in valorEntradaElemento.body:
                    if isinstance(Función, ast.FunctionDef) and Función.name == '__init__':
                        tablaParámetro.setdefault(valorEntradaElemento.name, set()).update(argumentoParámetro.arg for argumentoParámetro in Función.args.args + Función.args.kwonlyargs)
            nombre = ''
            if isinstance(valorEntradaElemento, (ast.FunctionDef, ast.ClassDef)): nombre = valorEntradaElemento.name
            elif isinstance(valorEntradaElemento, ast.Name) and isinstance(valorEntradaElemento.ctx, ast.Store): nombre = valorEntradaElemento.id
            elif isinstance(valorEntradaElemento, ast.arg): nombre = valorEntradaElemento.arg
            if nombre and nombre not in valorContrato and all(ord(valorCarácter)<128 for valorCarácter in nombre):
                fallos.append('{}:{}: {}'.format(ruta.relative_to(raízRepositorio), valorEntradaElemento.lineno, nombre))
    for ruta, nodoAST in nodosAST.items():
        for invocar in ast.walk(nodoAST):
            if not isinstance(invocar, ast.Call): continue
            nombre = invocar.func.id if isinstance(invocar.func, ast.Name) else invocar.func.attr if isinstance(invocar.func, ast.Attribute) else ''
            if nombre not in tablaParámetro or nombre in funciónArgumentosVariables or not any(ord(valorCarácter)>127 for valorCarácter in nombre): continue
            for argumentoParámetro in invocar.keywords:
                if argumentoParámetro.arg and argumentoParámetro.arg not in tablaParámetro[nombre]:
                    fallos.append('{}:{}: {}의 매개변수 {}'.format(ruta.relative_to(raízRepositorio), invocar.lineno, nombre, argumentoParámetro.arg))
    for línea in (raízProyecto/'denominación/asociaciónNombreArchivo.tsv').read_text().splitlines()[1:]:
        elementoListaElementoPrevio, elementoListaActual, entradaElementoValorProceso = línea.split('\t')
        if not (raízProyecto/elementoListaActual).is_file(): fallos.append('valorMover Archivo métodoAusente: '+elementoListaActual)
        if entradaElementoValorProceso == '호환진입점유지' and not (raízProyecto/elementoListaElementoPrevio).is_file(): fallos.append('호환 puntoEntradaElemento métodoAusente: '+elementoListaElementoPrevio)
    Ejemplos = (raízProyecto.parents[1]/'example/java/EjemploRed.java').read_text()
    for llamadasProhibido in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if llamadasProhibido in Ejemplos: fallos.append('네트워크 예제에 남은 표준 직접 invocar: '+llamadasProhibido)
    # 사용자가 읽는 Java 예제는 palabrasReservado/리터럴을 제외한 식별자도 construirTodos 한국어다.
    palabrasReservado = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for ruta in sorted((raízProyecto.parents[1]/'example/java').glob('*.java')):
        fuente = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ruta.read_text())
        for nombre in re.findall(r'\b[^\W\d]\w*\b', fuente, re.UNICODE):
            if nombre not in palabrasReservado and all(ord(valorCarácter)<128 for valorCarácter in nombre):
                fallos.append('{}: 예제의 영어 valorIdentificador {}'.format(ruta.name, nombre))
    for nombre in ('ventana', 'botón', 'etiqueta', 'CampoTexto', 'ElementoPantalla', 'ColaEvento', 'tareaFondo', 'TareaTareaEjecutable', 'ReceptorAcción', 'NotificaciónAcción', 'Tarea'):
        fuente = (raízProyecto/'JavaEspañol/español/propio'/(nombre+'.java')).read_text()
        fuente = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', fuente)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', fuente):
            fallos.append(nombre+': español 직접 구현에 표준 valorObjeto 래퍼가 남았습니다.')
    ejemploC = (raízProyecto.parents[1]/'example/c/EjemploRed.c').read_text()
    for nombre in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if nombre in ejemploC: fallos.append('C Comunicación 예제에 남은 표준 nombre: '+nombre)
    ejemploPython = (raízProyecto.parents[1]/'example/python/EjemploRed.py').read_text()
    if 'OSError' in ejemploPython or '.args' in ejemploPython: fallos.append('Python Comunicación 예제에 남은 표준 excepción 직접 valorUsar')
    valorCabecera = (raízProyecto.parents[1]/'posix-kor/arm64-native/Encabezados/ABIRed.h').read_text()
    for nombre in ('FamiliaInternet', 'ConectorRedDatagrama', 'ProtocoloDatagrama', 'DirecciónConectorRed', 'DirecciónConectorRedInternet', 'crearExtremo', 'enviarDatosDatagrama'):
        if re.search(r'^#define\s+'+nombre+r'\b', valorCabecera, re.M): fallos.append('C 직접 implementación 대신 valorMacro valorUsar: '+nombre)
    númeroElementosArchivoJava = 0
    for valorRaíz in ('fuente', 'Usuario/Java', 'JavaEspañol'):
        for ruta in (raízProyecto/valorRaíz).rglob('*.java'):
            númeroElementosArchivoJava += 1
            fuente = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ruta.read_text())
            for esCoincidente in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', fuente):
                fallos.append('{}: 한국어화되지 않은 Declaraciones {}'.format(ruta.relative_to(raízProyecto), esCoincidente[1]))
            if valorRaíz == 'JavaEspañol' and re.search(r'\bthrows\s+[A-Za-z]', fuente):
                fallos.append('{}: 공개 excepción Declaraciones'.format(ruta.relative_to(raízProyecto)))
    númeroArchivosJavaX86 = 0
    nombresJavaEstándar = {'String', 'length', 'charAt'}
    for ruta in sorted((raízRepositorio/'os/fuente').glob('*.java')):
        númeroArchivosJavaX86 += 1
        fuente = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ruta.read_text())
        for nombre in re.findall(r'\b[^\W\d]\w*\b', fuente, re.UNICODE):
            if nombre not in palabrasReservado | nombresJavaEstándar and all(ord(valorCarácter)<128 for valorCarácter in nombre):
                fallos.append('{}: propio 영어 valorIdentificador {}'.format(ruta.relative_to(raízRepositorio), nombre))
    registroEntradaDiario = {'passed': False, 'python_files': númeroElementosArchivo, 'java_files': númeroElementosArchivoJava,
          'x86_java_files': númeroArchivosJavaX86, 'host_compiler_python_files': len(compiladoresCompartido), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if argumentos.lenguaC:
        subprocess.check_call(['python3', str(raízProyecto/'Herramientas/examinarNombresC.py')])
        examinarValor = json.loads((raízProyecto/'build/한국어화/시언어분석.json').read_text())
        fallos.extend(str(error) for error in examinarValor['error'])
        aBIExportar = set(json.loads((raízProyecto/'denominación/nombresEstándar.json').read_text()))
        for valorEntradaElemento in examinarValor['Declaraciones'].values():
            nombre = valorEntradaElemento['nombre']; ruta = Path(valorEntradaElemento['Archivo'])
            fuente = ruta.read_bytes()
            # español 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if fuente[valorEntradaElemento['valorDesfase']:valorEntradaElemento['valorDesfase']+len(nombre)] == nombre.encode() and nombre not in aBIExportar:
                fallos.append('{}:{}: {}'.format(ruta.relative_to(raízProyecto), valorEntradaElemento['línea'], nombre))
        registroEntradaDiario['c_semantic_checked'] = True
        registroEntradaDiario['c_source_sha256'] = {str(Path(Archivo).relative_to(raízProyecto)):archivoResumenHash for Archivo,archivoResumenHash in examinarValor['원문해시'].items()}
    registroEntradaDiario['passed'] = not fallos; registroEntradaDiario['failures'] = fallos
    valorDestino = raízProyecto/'build/verification/naming'; valorDestino.mkdir(parents=True, exist_ok=True)
    (valorDestino/'report.json').write_text(json.dumps(registroEntradaDiario, ensure_ascii=False, indent=2)+'\n')
    if fallos: raise SystemExit('\n'.join(fallos))
    print('PASS: español Declaraciones·Archivo ruta·호환 puntoEntradaElemento·Comunicación Ejemplos')

if __name__ == '__main__': ponerEnMarcha()
