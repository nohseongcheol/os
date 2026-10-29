#!/usr/bin/env python3
"""ที่เก็บ_ราก 전체의 เอง 원문을 목록화한다. ภายนอก_ค่า/สร้าง_167eff27 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

แสดง_ราก = Path(__file__).resolve().parents[1]
ที่เก็บ_ราก = แสดง_ราก.parents[1]

def เรียกใช้งาน():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    บันทึก_สถิติ = []
    for ไดเรกทอรี_ค่า, 하위들, 파일들 in os.walk(str(ที่เก็บ_ราก)):
        하위들[:] = sorted(ชื่อ for ชื่อ in 하위들 if ชื่อ not in 제외)
        for ชื่อ in sorted(파일들):
            เส้นทาง = Path(ไดเรกทอรี_ค่า)/ชื่อ
            if เส้นทาง.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            ข้อมูล = เส้นทาง.read_bytes()
            รายการ_ค่า = {'path': str(เส้นทาง.relative_to(ที่เก็บ_ราก)), 'sha256': hashlib.sha256(ข้อมูล).hexdigest(),
                  'ascii_filename': all(ord(อักขระ_ค่า)<128 for อักขระ_ค่า in เส้นทาง.stem)}
            if เส้นทาง.suffix == '.py':
                남은선언 = []
                try:
                    for โหนด_ค่า in ast.walk(ast.parse(ข้อมูล.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(โหนด_ค่า, (ast.FunctionDef, ast.ClassDef)): 낱말 = โหนด_ค่า.name
                        elif isinstance(โหนด_ค่า, ast.arg): 낱말 = โหนด_ค่า.arg
                        elif isinstance(โหนด_ค่า, ast.Name) and isinstance(โหนด_ค่า.ctx, ast.Store): 낱말 = โหนด_ค่า.id
                        if 낱말 and all(ord(อักขระ_ค่า)<128 for อักขระ_ค่า in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': โหนด_ค่า.lineno})
                    รายการ_ค่า['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as ข้อผิดพลาด:
                    รายการ_ค่า['parse_error'] = str(ข้อผิดพลาด)
            บันทึก_สถิติ.append(รายการ_ค่า)
    ผลลัพธ์ = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': บันทึก_สถิติ,
          'file_count': len(บันทึก_สถิติ), 'ascii_filename_count': sum(รายการ_ค่า['ascii_filename'] for รายการ_ค่า in บันทึก_สถิติ),
          'python_files_with_ascii_declarations': sum(bool(รายการ_ค่า.get('ascii_python_declarations')) for รายการ_ค่า in บันทึก_สถิติ),
          'all_repository_identifiers_korean': False,
          'note': '표준 เชื่อมต่อ 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    ปลายทาง_ค่า_a0fbc067 = แสดง_ราก/'build/verification/naming'; ปลายทาง_ค่า_a0fbc067.mkdir(parents=True, exist_ok=True)
    (ปลายทาง_ค่า_a0fbc067/'source-review.json').write_text(json.dumps(ผลลัพธ์, ensure_ascii=False, indent=2)+'\n')
    print('รหัสต้นฉบับ', ผลลัพธ์['file_count'], '개; ASCII ชื่อแฟ้ม_ข้อความ', ผลลัพธ์['ascii_filename_count'],
          '개; 영어 선언이 남은 Python แฟ้ม', ผลลัพธ์['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': เรียกใช้งาน()
