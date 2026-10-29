#!/usr/bin/env python3
"""repositoryRoot 전체의 Native 원문을 목록화한다. externalValue/generate 코드는 countingValue 전에 제외한다."""
import ast
import hashlib
import json
import os
from pathlib import Path

projectRoot = Path(__file__).resolve().parents[1]
repositoryRoot = projectRoot.parents[1]

def run():
    excludeValue = {'build', 'dist', 'vendor', '.git', '.vbox', '__pycache__', '.venv'}
    logRecord = []
    for directoryValue, childrenList, fileEntries in os.walk(str(repositoryRoot)):
        childrenList[:] = sorted(name for name in childrenList if name not in excludeValue)
        for name in sorted(fileEntries):
            path = Path(directoryValue)/name
            if path.suffix not in ('.java', '.c', '.h', '.cpp', '.py'): continue
            data = path.read_bytes()
            entryValue = {'path': str(path.relative_to(repositoryRoot)), 'sha256': hashlib.sha256(data).hexdigest(),
                  'ascii_filename': all(ord(characterValue)<128 for characterValue in path.stem)}
            if path.suffix == '.py':
                remainingDeclarations = []
                try:
                    for nodeValue in ast.walk(ast.parse(data.decode('utf-8-sig'))):
                        lexicalWord = ''
                        if isinstance(nodeValue, (ast.FunctionDef, ast.ClassDef)): lexicalWord = nodeValue.name
                        elif isinstance(nodeValue, ast.arg): lexicalWord = nodeValue.arg
                        elif isinstance(nodeValue, ast.Name) and isinstance(nodeValue.ctx, ast.Store): lexicalWord = nodeValue.id
                        if lexicalWord and all(ord(characterValue)<128 for characterValue in lexicalWord) and lexicalWord != '_' and not lexicalWord.startswith('__'):
                            remainingDeclarations.append({'name': lexicalWord, 'line': nodeValue.lineno})
                    entryValue['ascii_python_declarations'] = remainingDeclarations
                except (SyntaxError, UnicodeError) as error:
                    entryValue['parse_error'] = str(error)
            logRecord.append(entryValue)
    result = {'scope': 'first-party Java/C/C++/Python, entire jkoros repository',
          'excluded_directory_names': sorted(excludeValue), 'files': logRecord,
          'file_count': len(logRecord), 'ascii_filename_count': sum(entryValue['ascii_filename'] for entryValue in logRecord),
          'python_files_with_ascii_declarations': sum(bool(entryValue.get('ascii_python_declarations')) for entryValue in logRecord),
          'all_repository_identifiers_korean': False,
          'note': '표준 connect 계약과 호환 진입점도 목록에 포함한다. ASCII가 곧 결함이라는 뜻은 아니다. C 의미 분석은 naming/report.json을 본다.'}
    destinationValue = projectRoot/'build/verification/naming'; destinationValue.mkdir(parents=True, exist_ok=True)
    (destinationValue/'source-review.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print('source', result['file_count'], '개; ASCII fileNameText', result['ascii_filename_count'],
          '개; 영어 선언이 남은 Python file', result['python_files_with_ascii_declarations'], '개')

if __name__ == '__main__': run()
