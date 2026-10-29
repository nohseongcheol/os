#!/usr/bin/env python3
"""radice_del_repository 전체의 nativo 원문을 목록화한다. esterno_VALORE/generare 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

azione_radice = Path(__file__).resolve().parents[1]
radice_del_repository = azione_radice.parents[1]

def avvia():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    LOG_riga = []
    for elenco_VALORE, 하위들, 파일들 in os.walk(str(radice_del_repository)):
        하위들[:] = sorted(Nome for Nome in 하위들 if Nome not in 제외)
        for Nome in sorted(파일들):
            percorso = Path(elenco_VALORE)/Nome
            if percorso.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            dati = percorso.read_bytes()
            voce_VALORE = {'path': str(percorso.relative_to(radice_del_repository)), 'sha256': hashlib.sha256(dati).hexdigest(),
                  'ascii_filename': all(ord(carattere_VALORE)<128 for carattere_VALORE in percorso.stem)}
            if percorso.suffix == '.py':
                남은선언 = []
                try:
                    for nodo_VALORE in ast.walk(ast.parse(dati.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(nodo_VALORE, (ast.FunctionDef, ast.ClassDef)): 낱말 = nodo_VALORE.name
                        elif isinstance(nodo_VALORE, ast.arg): 낱말 = nodo_VALORE.arg
                        elif isinstance(nodo_VALORE, ast.Name) and isinstance(nodo_VALORE.ctx, ast.Store): 낱말 = nodo_VALORE.id
                        if 낱말 and all(ord(carattere_VALORE)<128 for carattere_VALORE in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': nodo_VALORE.lineno})
                    voce_VALORE['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as errore:
                    voce_VALORE['parse_error'] = str(errore)
            LOG_riga.append(voce_VALORE)
    risultato = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': LOG_riga,
          'file_count': len(LOG_riga), 'ascii_filename_count': sum(voce_VALORE['ascii_filename'] for voce_VALORE in LOG_riga),
          'python_files_with_ascii_declarations': sum(bool(voce_VALORE.get('ascii_python_declarations')) for voce_VALORE in LOG_riga),
          'all_repository_identifiers_korean': False,
          'note': '표준 Connetti 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    meta_VALORE = azione_radice/'build/verification/naming'; meta_VALORE.mkdir(parents=True, exist_ok=True)
    (meta_VALORE/'source-review.json').write_text(json.dumps(risultato, ensure_ascii=False, indent=2)+'\n')
    print('codiceSorgente', risultato['file_count'], '개; ASCII nome_file_SMS', risultato['ascii_filename_count'],
          '개; 영어 선언이 남은 Python file', risultato['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': avvia()
