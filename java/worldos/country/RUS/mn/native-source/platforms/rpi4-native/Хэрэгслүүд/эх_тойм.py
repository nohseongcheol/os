#!/usr/bin/env python3
"""저장소 전체의 자체 원문을 목록화한다. 외부/생성 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def Ажиллуулах():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    бичих_мөр_6e8b375a = []
    for лавлах_утга, 하위들, 파일들 in os.walk(str(저장소)):
        하위들[:] = sorted(Нэр for Нэр in 하위들 if Нэр not in 제외)
        for Нэр in sorted(파일들):
            ЗАМ = Path(лавлах_утга)/Нэр
            if ЗАМ.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            өгөгдөл = ЗАМ.read_bytes()
            оролт_утга = {'path': str(ЗАМ.relative_to(저장소)), 'sha256': hashlib.sha256(өгөгдөл).hexdigest(),
                  'ascii_filename': all(ord(тэмдэгт_утга)<128 for тэмдэгт_утга in ЗАМ.stem)}
            if ЗАМ.suffix == '.py':
                남은선언 = []
                try:
                    for зангилаа_утга in ast.walk(ast.parse(өгөгдөл.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(зангилаа_утга, (ast.FunctionDef, ast.ClassDef)): 낱말 = зангилаа_утга.name
                        elif isinstance(зангилаа_утга, ast.arg): 낱말 = зангилаа_утга.arg
                        elif isinstance(зангилаа_утга, ast.Name) and isinstance(зангилаа_утга.ctx, ast.Store): 낱말 = зангилаа_утга.id
                        if 낱말 and all(ord(тэмдэгт_утга)<128 for тэмдэгт_утга in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': зангилаа_утга.lineno})
                    оролт_утга['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as Алдаа:
                    оролт_утга['parse_error'] = str(Алдаа)
            бичих_мөр_6e8b375a.append(оролт_утга)
    결과 = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': бичих_мөр_6e8b375a,
          'file_count': len(бичих_мөр_6e8b375a), 'ascii_filename_count': sum(оролт_утга['ascii_filename'] for оролт_утга in бичих_мөр_6e8b375a),
          'python_files_with_ascii_declarations': sum(bool(оролт_утга.get('ascii_python_declarations')) for оролт_утга in бичих_мөр_6e8b375a),
          'all_repository_identifiers_korean': False,
          'note': '표준 Холбох 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    товлосон_газар_утга = 기준/'build/verification/naming'; товлосон_газар_утга.mkdir(parents=True, exist_ok=True)
    (товлосон_газар_утга/'source-review.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2)+'\n')
    print('ЭХ', 결과['file_count'], '개; ASCII файл_нэр_Бичвэр', 결과['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Файл', 결과['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': Ажиллуулах()
