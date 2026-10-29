#!/usr/bin/env python3
"""ຣີໂພຊິທໍຣີ_ເລກຮາກ 전체의 자체 원문을 목록화한다. 외부/ສ້າງ_167eff27 코드는 세기 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

ໂຄງ_ການ_ເລກຮາກ = Path(__file__).resolve().parents[1]
ຣີໂພຊິທໍຣີ_ເລກຮາກ = ໂຄງ_ການ_ເລກຮາກ.parents[1]

def ແລ່ນ():
    제외 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    ບັນທຶກ_ແຖວ = []
    for ກຸ່ມຂໍ້ມູນ_ຄ່າ, 하위들, 파일들 in os.walk(str(ຣີໂພຊິທໍຣີ_ເລກຮາກ)):
        하위들[:] = sorted(ຊື່ for ຊື່ in 하위들 if ຊື່ not in 제외)
        for ຊື່ in sorted(파일들):
            ທາງໂຄຈອນ = Path(ກຸ່ມຂໍ້ມູນ_ຄ່າ)/ຊື່
            if ທາງໂຄຈອນ.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            ຂໍ້ມູນ = ທາງໂຄຈອນ.read_bytes()
            ເຂົ້າໃນ_ຄ່າ = {'path': str(ທາງໂຄຈອນ.relative_to(ຣີໂພຊິທໍຣີ_ເລກຮາກ)), 'sha256': hashlib.sha256(ຂໍ້ມູນ).hexdigest(),
                  'ascii_filename': all(ord(ຕົວອັກສອນ_ຄ່າ)<128 for ຕົວອັກສອນ_ຄ່າ in ທາງໂຄຈອນ.stem)}
            if ທາງໂຄຈອນ.suffix == '.py':
                남은선언 = []
                try:
                    for ຈອມ_ຄ່າ in ast.walk(ast.parse(ຂໍ້ມູນ.decode('utf-8-sig'))):
                        낱말 = ''
                        if isinstance(ຈອມ_ຄ່າ, (ast.FunctionDef, ast.ClassDef)): 낱말 = ຈອມ_ຄ່າ.name
                        elif isinstance(ຈອມ_ຄ່າ, ast.arg): 낱말 = ຈອມ_ຄ່າ.arg
                        elif isinstance(ຈອມ_ຄ່າ, ast.Name) and isinstance(ຈອມ_ຄ່າ.ctx, ast.Store): 낱말 = ຈອມ_ຄ່າ.id
                        if 낱말 and all(ord(ຕົວອັກສອນ_ຄ່າ)<128 for ຕົວອັກສອນ_ຄ່າ in 낱말) and 낱말 != '_' and not 낱말.startswith('__'):
                            남은선언.append({'name': 낱말, 'line': ຈອມ_ຄ່າ.lineno})
                    ເຂົ້າໃນ_ຄ່າ['ascii_python_declarations'] = 남은선언
                except (SyntaxError, UnicodeError) as ຂໍ້ຜິດພາດ:
                    ເຂົ້າໃນ_ຄ່າ['parse_error'] = str(ຂໍ້ຜິດພາດ)
            ບັນທຶກ_ແຖວ.append(ເຂົ້າໃນ_ຄ່າ)
    ມາດຕະການ = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(제외), 'files': ບັນທຶກ_ແຖວ,
          'file_count': len(ບັນທຶກ_ແຖວ), 'ascii_filename_count': sum(ເຂົ້າໃນ_ຄ່າ['ascii_filename'] for ເຂົ້າໃນ_ຄ່າ in ບັນທຶກ_ແຖວ),
          'python_files_with_ascii_declarations': sum(bool(ເຂົ້າໃນ_ຄ່າ.get('ascii_python_declarations')) for ເຂົ້າໃນ_ຄ່າ in ບັນທຶກ_ແຖວ),
          'all_repository_identifiers_korean': False,
          'note': '표준 ເຊື່ອມຕໍ່ 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    ປາຍທາງ_ຄ່າ = ໂຄງ_ການ_ເລກຮາກ/'build/verification/naming'; ປາຍທາງ_ຄ່າ.mkdir(parents=True, exist_ok=True)
    (ປາຍທາງ_ຄ່າ/'source-review.json').write_text(json.dumps(ມາດຕະການ, ensure_ascii=False, indent=2)+'\n')
    print('ແຫຼ່ງທີ່ມາ', ມາດຕະການ['file_count'], '개; ASCII ຟາຍ_ຊື່_ຂໍ້ຄວາມ', ມາດຕະການ['ascii_filename_count'],
          '개; 영어 선언이 남은 Python ຟາຍ', ມາດຕະການ['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': ແລ່ນ()
