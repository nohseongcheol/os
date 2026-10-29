#!/usr/bin/env python3
"""代碼庫根 전체의 內建 원문을 목록화한다. 外部值/生成 코드는 計數中值 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

項目根 = Path(__file__).resolve().parents[1]
代碼庫根 = 項目根.parents[1]

def 運行():
    排除值 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    日誌記錄 = []
    for 目錄值, 子項列列表, 檔案條目列 in os.walk(str(代碼庫根)):
        子項列列表[:] = sorted(名稱 for 名稱 in 子項列列表 if 名稱 not in 排除值)
        for 名稱 in sorted(檔案條目列):
            路徑 = Path(目錄值)/名稱
            if 路徑.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            資料 = 路徑.read_bytes()
            條目值 = {'path': str(路徑.relative_to(代碼庫根)), 'sha256': hashlib.sha256(資料).hexdigest(),
                  'ascii_filename': all(ord(字元值)<128 for 字元值 in 路徑.stem)}
            if 路徑.suffix == '.py':
                剩餘聲明列 = []
                try:
                    for 節點值 in ast.walk(ast.parse(資料.decode('utf-8-sig'))):
                        詞法用機器字 = ''
                        if isinstance(節點值, (ast.FunctionDef, ast.ClassDef)): 詞法用機器字 = 節點值.name
                        elif isinstance(節點值, ast.arg): 詞法用機器字 = 節點值.arg
                        elif isinstance(節點值, ast.Name) and isinstance(節點值.ctx, ast.Store): 詞法用機器字 = 節點值.id
                        if 詞法用機器字 and all(ord(字元值)<128 for 字元值 in 詞法用機器字) and 詞法用機器字 != '_' and not 詞法用機器字.startswith('__'):
                            剩餘聲明列.append({'name': 詞法用機器字, 'line': 節點值.lineno})
                    條目值['ascii_python_declarations'] = 剩餘聲明列
                except (SyntaxError, UnicodeError) as 錯誤:
                    條目值['parse_error'] = str(錯誤)
            日誌記錄.append(條目值)
    結果 = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(排除值), 'files': 日誌記錄,
          'file_count': len(日誌記錄), 'ascii_filename_count': sum(條目值['ascii_filename'] for 條目值 in 日誌記錄),
          'python_files_with_ascii_declarations': sum(bool(條目值.get('ascii_python_declarations')) for 條目值 in 日誌記錄),
          'all_repository_identifiers_korean': False,
          'note': '표준 連接 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    目的地址值 = 項目根/'build/verification/naming'; 目的地址值.mkdir(parents=True, exist_ok=True)
    (目的地址值/'source-review.json').write_text(json.dumps(結果, ensure_ascii=False, indent=2)+'\n')
    print('原始碼', 結果['file_count'], '개; ASCII 檔案名稱文本', 結果['ascii_filename_count'],
          '개; 영어 선언이 남은 Python 檔案', 結果['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': 運行()
