#!/usr/bin/env python3
"""gốcCâyKhoNguồn 전체의 tựThân 원문을 목록화한다. giáTrịBênNgoài/sinh 코드는 giáTrịViệcĐếm 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

gốcCâyDựÁn = Path(__file__).resolve().parents[1]
gốcCâyKhoNguồn = gốcCâyDựÁn.parents[1]

def chạy():
    giáTrịLoạiTrừ = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    bảnGhiNhậtKý = []
    for giáTrịThưMục, danhSáchCácCon, cácMụcTệp in os.walk(str(gốcCâyKhoNguồn)):
        danhSáchCácCon[:] = sorted(tên for tên in danhSáchCácCon if tên not in giáTrịLoạiTrừ)
        for tên in sorted(cácMụcTệp):
            đườngDẫn = Path(giáTrịThưMục)/tên
            if đườngDẫn.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            DữLiệu = đườngDẫn.read_bytes()
            giáTrịMục = {'path': str(đườngDẫn.relative_to(gốcCâyKhoNguồn)), 'sha256': hashlib.sha256(DữLiệu).hexdigest(),
                  'ascii_filename': all(ord(giáTrịKýTự)<128 for giáTrịKýTự in đườngDẫn.stem)}
            if đườngDẫn.suffix == '.py':
                cácKhaiBáoCònLại = []
                try:
                    for giáTrịNútCây in ast.walk(ast.parse(DữLiệu.decode('utf-8-sig'))):
                        từTừVựng = ''
                        if isinstance(giáTrịNútCây, (ast.FunctionDef, ast.ClassDef)): từTừVựng = giáTrịNútCây.name
                        elif isinstance(giáTrịNútCây, ast.arg): từTừVựng = giáTrịNútCây.arg
                        elif isinstance(giáTrịNútCây, ast.Name) and isinstance(giáTrịNútCây.ctx, ast.Store): từTừVựng = giáTrịNútCây.id
                        if từTừVựng and all(ord(giáTrịKýTự)<128 for giáTrịKýTự in từTừVựng) and từTừVựng != '_' and not từTừVựng.startswith('__'):
                            cácKhaiBáoCònLại.append({'name': từTừVựng, 'line': giáTrịNútCây.lineno})
                    giáTrịMục['ascii_python_declarations'] = cácKhaiBáoCònLại
                except (SyntaxError, UnicodeError) as lỗi:
                    giáTrịMục['parse_error'] = str(lỗi)
            bảnGhiNhậtKý.append(giáTrịMục)
    kếtQuả = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(giáTrịLoạiTrừ), 'files': bảnGhiNhậtKý,
          'file_count': len(bảnGhiNhậtKý), 'ascii_filename_count': sum(giáTrịMục['ascii_filename'] for giáTrịMục in bảnGhiNhậtKý),
          'python_files_with_ascii_declarations': sum(bool(giáTrịMục.get('ascii_python_declarations')) for giáTrịMục in bảnGhiNhậtKý),
          'all_repository_identifiers_korean': False,
          'note': '표준 nốiKết 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    giáTrịĐích = gốcCâyDựÁn/'build/verification/naming'; giáTrịĐích.mkdir(parents=True, exist_ok=True)
    (giáTrịĐích/'source-review.json').write_text(json.dumps(kếtQuả, ensure_ascii=False, indent=2)+'\n')
    print('mãNguồn', kếtQuả['file_count'], '개; ASCII vănBảnTênTệp', kếtQuả['ascii_filename_count'],
          '개; 영어 선언이 남은 Python Tệp', kếtQuả['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': chạy()
