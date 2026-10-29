#!/usr/bin/env python3
"""dipòsit_rel 전체의 propi 원문을 목록화한다. extern_VALOR/generar 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

Project_rel = Path(__file__).resolve().parents[1]
dipòsit_rel = Project_rel.parents[1]

def Executa_2():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_fila = []
    for directori_VALOR, 하위들, 파일들 in os.walk(str(dipòsit_rel)):
        하위들[:] = sorted(Nom for Nom in 하위들 if Nom not in 제외)
        for Nom in sorted(파일들):
            Camí = Path(directori_VALOR)/Nom
            if Camí.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            dades = Camí.read_bytes()
            introducció_VALOR = {'path': str(Camí.relative_to(dipòsit_rel)), 'sha256': hashlib.sha256(dades).hexdigest(),
                  'ascii_filename': all(ord(caràcter_VALOR)<128 for caràcter_VALOR in Camí.stem)}
            if Camí.suffix == '.py':
                남은선언 = []
                try:
                    for node_VALOR in ast.walk(ast.parse(dades.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(node_VALOR, (ast.FunctionDef, ast.ClassDef)): 낱말 = node_VALOR.name
                        elif isinstance(node_VALOR, ast.arg): 낱말 = node_VALOR.arg
                        elif isinstance(node_VALOR, ast.Name) and isinstance(node_VALOR.ctx, ast.Store): 낱말 = node_VALOR.id
                        if 낱말 and all(ord(caràcter_VALOR)<128 for caràcter_VALOR in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': node_VALOR.lineno})
                    introducció_VALOR['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as s_ha_produït_un_error:
                    introducció_VALOR['parse_error'] = str(s_ha_produït_un_error)
            LOG_fila.append(introducció_VALOR)
    RESULTAT = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_fila,
          'file_count': len(LOG_fila), 'ascii_filename_count': sum(introducció_VALOR['ascii_filename'] for introducció_VALOR in LOG_fila),
          'python_files_with_ascii_declarations': sum(bool(introducció_VALOR.get('ascii_python_declarations')) for introducció_VALOR in LOG_fila),
          'all_repository_identifiers_korean': False,
          'note': '표준 Connecta 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    destinació_VALOR = Project_rel/'build/verification/naming'; destinació_VALOR.mkdir(parents=True, exist_ok=True)
    (destinació_VALOR/'source-review.json').write_text(json.dumps(RESULTAT, ensure_ascii=False, indent=2)+'\n')
    print('FONT', RESULTAT['file_count'], '개; ASCII nom_d_arxiu_SMS', RESULTAT['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Fitxer', RESULTAT['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Executa_2()
