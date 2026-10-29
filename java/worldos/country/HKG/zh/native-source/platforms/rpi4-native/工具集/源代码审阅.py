#!/usr/bin/env python3
"""代码库根 전체의 内置 원문을 목록화한다. 外部值/生成 코드는 计数中值 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

项目根 = Path(__file__).resolve().parents[1]
代码库根 = 项目根.parents[1]

def 运行():
    排除值 = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    日志记录 = []
    for 目录值, 子项列列表, 文件条目列 in os.walk(str(代码库根)):
        子项列列表[:] = sorted(名称 for 名称 in 子项列列表 if 名称 not in 排除值)
        for 名称 in sorted(文件条目列):
            路径 = Path(目录值)/名称
            if 路径.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            数据 = 路径.read_bytes()
            条目值 = {'path': str(路径.relative_to(代码库根)), 'sha256': hashlib.sha256(数据).hexdigest(),
                  'ascii_filename': all(ord(字符值)<128 for 字符值 in 路径.stem)}
            if 路径.suffix == '.py':
                剩余声明列 = []
                try:
                    for 节点值 in ast.walk(ast.parse(数据.decode('utf-8-sig'))):
                        词法用机器字 = ''
                        if isinstance(节点值, (ast.FunctionDef, ast.ClassDef)): 词法用机器字 = 节点值.name
                        elif isinstance(节点值, ast.arg): 词法用机器字 = 节点值.arg
                        elif isinstance(节点值, ast.Name) and isinstance(节点值.ctx, ast.Store): 词法用机器字 = 节点值.id
                        if 词法用机器字 and all(ord(字符值)<128 for 字符值 in 词法用机器字) and 词法用机器字 != '_' and not 词法用机器字.startswith('__'):
                            剩余声明列.append({'name': 词法用机器字, 'line': 节点值.lineno})
                    条目值['ascii_python_declarations'] = 剩余声明列
                except (SyntaxError, UnicodeError) as 错误:
                    条目值['parse_error'] = str(错误)
            日志记录.append(条目值)
    结果 = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(排除值), 'files': 日志记录,
          'file_count': len(日志记录), 'ascii_filename_count': sum(条目值['ascii_filename'] for 条目值 in 日志记录),
          'python_files_with_ascii_declarations': sum(bool(条目值.get('ascii_python_declarations')) for 条目值 in 日志记录),
          'all_repository_identifiers_korean': False,
          'note': '표준 连接 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    目的地址值 = 项目根/'build/verification/naming'; 目的地址值.mkdir(parents=True, exist_ok=True)
    (目的地址值/'source-review.json').write_text(json.dumps(结果, ensure_ascii=False, indent=2)+'\n')
    print('源代码', 结果['file_count'], '개; ASCII 文件名称文本', 结果['ascii_filename_count'],
          '개; 영어 선언이 남은 Python 文件', 结果['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': 运行()
