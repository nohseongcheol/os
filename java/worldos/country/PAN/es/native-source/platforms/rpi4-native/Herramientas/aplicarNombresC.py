#!/usr/bin/env python3
"""Declaraciones 고유번호와 UTF-8 valorByte 위치로 propio C 이름을 옮기는 일회성 이행 Herramientas.

valorExterno 구조체의 멤버, Cadena, C 표준 Función, AdaptaciónPlataforma 규약은 보존한다.
입력은 cambiarValor valorAntes 소스에 대한 examinarNombresC.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

raízProyecto = Path(__file__).resolve().parents[1]

def ejecutarComando():
    examinarValor = json.loads((raízProyecto/'build/한국어화/시언어분석.json').read_text())
    if examinarValor['error']: raise SystemExit('examinarValor 오류를 먼저 해결해야 합니다.')
    tablaNombre = json.loads((raízProyecto/'denominación/nombresC.json').read_text())
    definiciónEstándar = set(json.loads((raízProyecto/'denominación/nombresEstándar.json').read_text()))
    tablaDeclaración = examinarValor['Declaraciones']
    reemplazarHaciaDeclaración = {valorÚnico:tablaNombre[valorEntradaElemento['nombre']] for valorÚnico,valorEntradaElemento in tablaDeclaración.items()
                if valorEntradaElemento['nombre'] in tablaNombre and valorEntradaElemento['nombre'] not in definiciónEstándar}
    tablaConexión = {valorEntradaElemento['nombre']:tablaNombre[valorEntradaElemento['nombre']] for valorEntradaElemento in tablaDeclaración.values()
              if valorEntradaElemento.get('conectar')==4 and valorEntradaElemento['valorClaseTipo'] in (8,9)
              and valorEntradaElemento['nombre'] in tablaNombre and valorEntradaElemento['nombre'] not in definiciónEstándar}
    # generar AOT C·어셈블리·공개 SDK가 공유하는 바이너리 conectar 이름만 유지한다.
    valorCabecera = ['/* español árbolFuente 이름과 기존 máquina conectar valorContrato. 자동 generar: denominación/nombresC.json */',
           '#ifndef encabezadoNombresEnlazarMáquinaNativo', '#define encabezadoNombresEnlazarMáquinaNativo']
    valorCabecera += ['#define '+nombreNuevo+' '+nombreAntiguo for nombreAntiguo,nombreNuevo in sorted(tablaConexión.items())]
    valorCabecera += ['#endif','']
    (raízProyecto/'denominación/nombresEnlazarMáquina.h').write_text('\n'.join(valorCabecera))
    listaCambios = defaultdict(dict)
    for Archivo,valorDesfase,nombre,valorÚnico in examinarValor['referencia']:
        if valorÚnico in reemplazarHaciaDeclaración:
            listaCambios[Archivo][valorDesfase] = (nombre,reemplazarHaciaDeclaración[valorÚnico])
    registroEntradaDiario = ['Archivo\t원래바이트위치\t이전이름\t한국어이름']
    ignorarValor = []
    for Archivo,cambiarValor in listaCambios.items():
        ruta = Path(Archivo); original = ruta.read_bytes(); Datos = original
        for valorDesfase,(nombreAntiguo,nombreNuevo) in sorted(cambiarValor.items(),reverse=True):
            terminación = valorDesfase+len(nombreAntiguo.encode())
            if original[valorDesfase:terminación] != nombreAntiguo.encode():
                ignorarValor.append((str(ruta.relative_to(raízProyecto)),valorDesfase,nombreAntiguo));continue
            Datos = Datos[:valorDesfase]+nombreNuevo.encode()+Datos[terminación:]
            registroEntradaDiario.append('{}\t{}\t{}\t{}'.format(ruta.relative_to(raízProyecto),valorDesfase,nombreAntiguo,nombreNuevo))
        ruta.write_bytes(Datos)
    # fuentePreprocesar 매개변수는 AST의 선언으로 나타나지 않는다. fuentePreprocesar 줄만 보완한다.
    palabraLéxico = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    valorMacro = {valorEntradaElemento['nombre']:tablaNombre[valorEntradaElemento['nombre']] for valorEntradaElemento in tablaDeclaración.values()
              if valorEntradaElemento['valorClaseTipo']==501 and valorEntradaElemento['nombre'] in tablaNombre and valorEntradaElemento['nombre'] not in definiciónEstándar}
    for ruta in sorted({Path(valorEntradaElemento['Archivo']) for valorEntradaElemento in tablaDeclaración.values()}):
        listaLínea = ruta.read_text().splitlines(True); esContinuación = False
        for número,línea in enumerate(listaLínea):
            fuentePreprocesar = esContinuación or bool(re.match(r'\s*#',línea))
            esContinuación = fuentePreprocesar and línea.rstrip().endswith('\\')
            if fuentePreprocesar:
                Tabla = tablaNombre if re.match(r'\s*#\s*define\b',línea) or esContinuación else valorMacro
                listaLínea[número] = palabraLéxico.sub(lambda esCoincidente: Tabla.get(esCoincidente[0],esCoincidente[0]) if esCoincidente[0] not in definiciónEstándar else esCoincidente[0],línea)
        ruta.write_text(''.join(listaLínea))
    # 각 propio traducirFuente 단위에만 연결표를 넣는다. valorExterno 배포본에는 전파하지 않는다.
    for ruta in sorted({Path(valorEntradaElemento['Archivo']) for valorEntradaElemento in tablaDeclaración.values()}):
        if ruta.suffix not in ('.c','.cpp'):continue
        valorParRed = '../' * len(ruta.relative_to(raízProyecto).parts[:-1]) + 'denominación/nombresEnlazarMáquina.h'
        ruta.write_text('#include "'+valorParRed+'"\n'+ruta.read_text())
    (raízProyecto/'denominación/asociaciónNombreC.tsv').write_text('\n'.join(registroEntradaDiario)+'\n')
    (raízProyecto/'build/한국어화/전처리참조.json').write_text(json.dumps(ignorarValor,ensure_ascii=False,indent=2)+'\n')
    print('cambiarValor',len(registroEntradaDiario)-1,'fuentePreprocesar 재검토',len(ignorarValor),'máquina conectar',len(tablaConexión))

if __name__=='__main__': ejecutarComando()
