#!/usr/bin/env python3
"""保管庫根 전체의 内蔵 원문을 목록화한다. 外部値/生成 코드는 計数中値 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

計画根 = Path(__file__).resolve().parents[1]
保管庫根 = 計画根.parents[1]

def 起動処理():
    除外値 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    履歴記録記録 = []
    for ディレクトリ値, 子一覧一覧, ファイル登録項目一覧 in os.walk(str(保管庫根)):
        子一覧一覧[:] = sorted(名前 for 名前 in 子一覧一覧 if 名前 not in 除外値)
        for 名前 in sorted(ファイル登録項目一覧):
            経路 = Path(ディレクトリ値)/名前
            if 経路.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            データ = 経路.read_bytes()
            入口値 = {'path': str(経路.relative_to(保管庫根)), 'sha256': hashlib.sha256(データ).hexdigest(),
                  'ascii_filename': all(ord(文字値)<128 for 文字値 in 経路.stem)}
            if 経路.suffix == '.py':
                残り宣言一覧 = []
                try:
                    for 節点値 in ast.walk(ast.parse(データ.decode('utf-8-sig'))):
                        字句用語 = ''
                        if isinstance(節点値, (ast.FunctionDef, ast.ClassDef)): 字句用語 = 節点値.name
                        elif isinstance(節点値, ast.arg): 字句用語 = 節点値.arg
                        elif isinstance(節点値, ast.Name) and isinstance(節点値.ctx, ast.Store): 字句用語 = 節点値.id
                        if 字句用語 and all(ord(文字値)<128 for 文字値 in 字句用語) and 字句用語 != '_' and not 字句用語.startswith('__'):
                            残り宣言一覧.append({'name': 字句用語, 'line': 節点値.lineno})
                    入口値['ascii_python_declarations'] = 残り宣言一覧
                except (SyntaxError, UnicodeError) as エラー:
                    入口値['parse_error'] = str(エラー)
            履歴記録記録.append(入口値)
    結果 = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(除外値), 'files': 履歴記録記録,
          'file_count': len(履歴記録記録), 'ascii_filename_count': sum(入口値['ascii_filename'] for 入口値 in 履歴記録記録),
          'python_files_with_ascii_declarations': sum(bool(入口値.get('ascii_python_declarations')) for 入口値 in 履歴記録記録),
          'all_repository_identifiers_korean': False,
          'note': '표준 接続 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    宛先値 = 計画根/'build/verification/naming'; 宛先値.mkdir(parents=True, exist_ok=True)
    (宛先値/'source-review.json').write_text(json.dumps(結果, ensure_ascii=False, indent=2)+'\n')
    print('ソース', 結果['file_count'], '개; ASCII ファイル名前本文', 結果['ascii_filename_count'],
          '개; 영어 선언이 남은 Python ファイル', 結果['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': 起動処理()
