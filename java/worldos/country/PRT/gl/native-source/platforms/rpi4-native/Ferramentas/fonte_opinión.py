#!/usr/bin/env python3
"""repositorio_raíz 전체의 자체 원문을 목록화한다. externo_VALOR/xerar 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

Project_raíz = Path(__file__).resolve().parents[1]
repositorio_raíz = Project_raíz.parents[1]

def Executar_2():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_fila = []
    for directorio_VALOR, 하위들, 파일들 in os.walk(str(repositorio_raíz)):
        하위들[:] = sorted(Nome for Nome in 하위들 if Nome not in 제외)
        for Nome in sorted(파일들):
            CAMIÑO = Path(directorio_VALOR)/Nome
            if CAMIÑO.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            datos = CAMIÑO.read_bytes()
            introdución_VALOR = {'path': str(CAMIÑO.relative_to(repositorio_raíz)), 'sha256': hashlib.sha256(datos).hexdigest(),
                  'ascii_filename': all(ord(carácter_VALOR)<128 for carácter_VALOR in CAMIÑO.stem)}
            if CAMIÑO.suffix == '.py':
                남은선언 = []
                try:
                    for nó_VALOR in ast.walk(ast.parse(datos.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(nó_VALOR, (ast.FunctionDef, ast.ClassDef)): 낱말 = nó_VALOR.name
                        elif isinstance(nó_VALOR, ast.arg): 낱말 = nó_VALOR.arg
                        elif isinstance(nó_VALOR, ast.Name) and isinstance(nó_VALOR.ctx, ast.Store): 낱말 = nó_VALOR.id
                        if 낱말 and all(ord(carácter_VALOR)<128 for carácter_VALOR in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': nó_VALOR.lineno})
                    introdución_VALOR['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as ERRO:
                    introdución_VALOR['parse_error'] = str(ERRO)
            LOG_fila.append(introdución_VALOR)
    RESULTANTE = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_fila,
          'file_count': len(LOG_fila), 'ascii_filename_count': sum(introdución_VALOR['ascii_filename'] for introdución_VALOR in LOG_fila),
          'python_files_with_ascii_declarations': sum(bool(introdución_VALOR.get('ascii_python_declarations')) for introdución_VALOR in LOG_fila),
          'all_repository_identifiers_korean': False,
          'note': '표준 Conectar 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    destino_VALOR = Project_raíz/'build/verification/naming'; destino_VALOR.mkdir(parents=True, exist_ok=True)
    (destino_VALOR/'source-review.json').write_text(json.dumps(RESULTANTE, ensure_ascii=False, indent=2)+'\n')
    print('FONTE', RESULTANTE['file_count'], '개; ASCII Ficheiro_nome_SMS', RESULTANTE['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Ficheiro', RESULTANTE['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Executar_2()
