#!/usr/bin/env python3
"""raízRepositorio 전체의 propio 원문을 목록화한다. valorExterno/generar 코드는 valorConteoEnCurso 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

raízProyecto = Path(__file__).resolve().parents[1]
raízRepositorio = raízProyecto.parents[1]

def ponerEnMarcha():
    valorExcluir = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    registroEntradaDiario = []
    for valorDirectorio, listaHijos, entradasArchivo in os.walk(str(raízRepositorio)):
        listaHijos[:] = sorted(nombre for nombre in listaHijos if nombre not in valorExcluir)
        for nombre in sorted(entradasArchivo):
            ruta = Path(valorDirectorio)/nombre
            if ruta.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            Datos = ruta.read_bytes()
            valorEntradaElemento = {'path': str(ruta.relative_to(raízRepositorio)), 'sha256': hashlib.sha256(Datos).hexdigest(),
                  'ascii_filename': all(ord(valorCarácter)<128 for valorCarácter in ruta.stem)}
            if ruta.suffix == '.py':
                declaracionesRestante = []
                try:
                    for valorNodo in ast.walk(ast.parse(Datos.decode('utf-8-sig'))):
                        palabraLéxico = ''
                        if isinstance(valorNodo, (ast.FunctionDef, ast.ClassDef)): palabraLéxico = valorNodo.name
                        elif isinstance(valorNodo, ast.arg): palabraLéxico = valorNodo.arg
                        elif isinstance(valorNodo, ast.Name) and isinstance(valorNodo.ctx, ast.Store): palabraLéxico = valorNodo.id
                        if palabraLéxico and all(ord(valorCarácter)<128 for valorCarácter in palabraLéxico) and palabraLéxico != '_' and not palabraLéxico.startswith('__'):
                            declaracionesRestante.append({'name': palabraLéxico, 'line': valorNodo.lineno})
                    valorEntradaElemento['ascii_python_declarations'] = declaracionesRestante
                except (SyntaxError, UnicodeError) as error:
                    valorEntradaElemento['parse_error'] = str(error)
            registroEntradaDiario.append(valorEntradaElemento)
    resultado = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(valorExcluir), 'files': registroEntradaDiario,
          'file_count': len(registroEntradaDiario), 'ascii_filename_count': sum(valorEntradaElemento['ascii_filename'] for valorEntradaElemento in registroEntradaDiario),
          'python_files_with_ascii_declarations': sum(bool(valorEntradaElemento.get('ascii_python_declarations')) for valorEntradaElemento in registroEntradaDiario),
          'all_repository_identifiers_korean': False,
          'note': '표준 conectar 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    valorDestino = raízProyecto/'build/verification/naming'; valorDestino.mkdir(parents=True, exist_ok=True)
    (valorDestino/'source-review.json').write_text(json.dumps(resultado, ensure_ascii=False, indent=2)+'\n')
    print('fuente', resultado['file_count'], '개; ASCII textoNombreArchivo', resultado['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Archivo', resultado['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': ponerEnMarcha()
