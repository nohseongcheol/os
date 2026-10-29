#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/생성 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def 시작():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    papattivik_sanimukutaak = []
    for tukimuagutiit_atuutilik, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(atiq for atiq in 하위들 if atiq not in 제외)
        for atiq in sorted(파일들):
            aqqut = Path(tukimuagutiit_atuutilik)/atiq
            if aqqut.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            titiqqat = aqqut.read_bytes()
            Iliniku_atuutilik = {'path': str(aqqut.relative_to(저장소)), 'sha256': hashlib.sha256(titiqqat).hexdigest(),
                  'ascii_filename': all(ord(immikkuuqtuq_atuutilik)<128 for immikkuuqtuq_atuutilik in aqqut.stem)}
            if aqqut.suffix == '.py':
                남은선언 = []
                try:
                    for attavigijaq_atuutilik in ast.walk(ast.parse(titiqqat.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(attavigijaq_atuutilik, (ast.FunctionDef, ast.ClassDef)): 낱말 = attavigijaq_atuutilik.name
                        elif isinstance(attavigijaq_atuutilik, ast.arg): 낱말 = attavigijaq_atuutilik.arg
                        elif isinstance(attavigijaq_atuutilik, ast.Name) and isinstance(attavigijaq_atuutilik.ctx, ast.Store): 낱말 = attavigijaq_atuutilik.id
                        if 낱말 and all(ord(immikkuuqtuq_atuutilik)<128 for immikkuuqtuq_atuutilik in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': attavigijaq_atuutilik.lineno})
                    Iliniku_atuutilik['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as tammarniq:
                    Iliniku_atuutilik['parse_error'] = str(tammarniq)
            papattivik_sanimukutaak.append(Iliniku_atuutilik)
    결과 = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': papattivik_sanimukutaak,
          'file_count': len(papattivik_sanimukutaak), 'ascii_filename_count': sum(Iliniku_atuutilik['ascii_filename'] for Iliniku_atuutilik in papattivik_sanimukutaak),
          'python_files_with_ascii_declarations': sum(bool(Iliniku_atuutilik.get('ascii_python_declarations')) for Iliniku_atuutilik in papattivik_sanimukutaak),
          'all_repository_identifiers_korean': False,
          'note': '표준 kasurli 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    namunngarvik_atuutilik = 기준/'build/verification/naming'; namunngarvik_atuutilik.mkdir(parents=True, exist_ok=True)
    (namunngarvik_atuutilik/'source-review.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2)+'\n')
    print('pivviujuq', 결과['file_count'], '개; ASCII ini_atiq_titiqqaq', 결과['ascii_filename_count'],
          '개; 영어 선언이 남은 Python ini', 결과['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': 시작()
