#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/생성 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def Phumeza():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    ilog_umqolo = []
    for isalathisi_ixabiso_e5561a2b, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(Igama for Igama in 하위들 if Igama not in 제외)
        for Igama in sorted(파일들):
            INDLELA = Path(isalathisi_ixabiso_e5561a2b)/Igama
            if INDLELA.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            iingcombolo = INDLELA.read_bytes()
            ufako_nkcukacha_ixabiso = {'path': str(INDLELA.relative_to(저장소)), 'sha256': hashlib.sha256(iingcombolo).hexdigest(),
                  'ascii_filename': all(ord(ikharakhtha_ixabiso)<128 for ikharakhtha_ixabiso in INDLELA.stem)}
            if INDLELA.suffix == '.py':
                남은선언 = []
                try:
                    for inowudi_ixabiso in ast.walk(ast.parse(iingcombolo.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(inowudi_ixabiso, (ast.FunctionDef, ast.ClassDef)): 낱말 = inowudi_ixabiso.name
                        elif isinstance(inowudi_ixabiso, ast.arg): 낱말 = inowudi_ixabiso.arg
                        elif isinstance(inowudi_ixabiso, ast.Name) and isinstance(inowudi_ixabiso.ctx, ast.Store): 낱말 = inowudi_ixabiso.id
                        if 낱말 and all(ord(ikharakhtha_ixabiso)<128 for ikharakhtha_ixabiso in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': inowudi_ixabiso.lineno})
                    ufako_nkcukacha_ixabiso['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as Impazamo:
                    ufako_nkcukacha_ixabiso['parse_error'] = str(Impazamo)
            ilog_umqolo.append(ufako_nkcukacha_ixabiso)
    결과 = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': ilog_umqolo,
          'file_count': len(ilog_umqolo), 'ascii_filename_count': sum(ufako_nkcukacha_ixabiso['ascii_filename'] for ufako_nkcukacha_ixabiso in ilog_umqolo),
          'python_files_with_ascii_declarations': sum(bool(ufako_nkcukacha_ixabiso.get('ascii_python_declarations')) for ufako_nkcukacha_ixabiso in ilog_umqolo),
          'all_repository_identifiers_korean': False,
          'note': '표준 Nxulumanisa 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    indawo_ekuyiwa_kuyo_ixabiso = 기준/'build/verification/naming'; indawo_ekuyiwa_kuyo_ixabiso.mkdir(parents=True, exist_ok=True)
    (indawo_ekuyiwa_kuyo_ixabiso/'source-review.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2)+'\n')
    print('UMTHOMBO', 결과['file_count'], '개; ASCII ifayile_igama_I_SMS', 결과['ascii_filename_count'],
          '개; 영어 선언이 남은 Python iFayili', 결과['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Phumeza()
