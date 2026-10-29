#!/usr/bin/env python3
"""naming clip·exception·경로를 검사한다. --시언어는 libclang Declaration 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

projectRoot = Path(__file__).resolve().parents[1]
repositoryRoot = projectRoot.parents[1]

def run():
    Parser = argparse.ArgumentParser(description=__doc__)
    Parser.add_argument('--cLanguage', action='store_true')
    arguments = Parser.parse_args()
    failures = []
    contractValue = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    fileCount = 0
    parameterTable = {}
    variadicFunction = set()
    astNodes = {}
    sharedCompilers = [repositoryRoot/'compiler/Compiler.py', repositoryRoot/'compiler/AheadOfTimeCompiler.py']
    for path in list((projectRoot/'tools').glob('*.py')) + list((projectRoot/'examples').rglob('*.py')) + sharedCompilers:
        if path.name.endswith(('이름반영.py', '이름분석.py')): continue
        fileCount += 1
        astNode = ast.parse(path.read_text()); astNodes[path] = astNode
        for entryValue in ast.walk(astNode):
            if isinstance(entryValue, ast.FunctionDef):
                parameterTable.setdefault(entryValue.name, set()).update(parameterArgument.arg for parameterArgument in entryValue.args.args + entryValue.args.kwonlyargs)
                if entryValue.args.kwarg: variadicFunction.add(entryValue.name)
            if isinstance(entryValue, ast.ClassDef):
                for functionValue in entryValue.body:
                    if isinstance(functionValue, ast.FunctionDef) and functionValue.name == '__init__':
                        parameterTable.setdefault(entryValue.name, set()).update(parameterArgument.arg for parameterArgument in functionValue.args.args + functionValue.args.kwonlyargs)
            name = ''
            if isinstance(entryValue, (ast.FunctionDef, ast.ClassDef)): name = entryValue.name
            elif isinstance(entryValue, ast.Name) and isinstance(entryValue.ctx, ast.Store): name = entryValue.id
            elif isinstance(entryValue, ast.arg): name = entryValue.arg
            if name and name not in contractValue and all(ord(characterValue)<128 for characterValue in name):
                failures.append('{}:{}: {}'.format(path.relative_to(repositoryRoot), entryValue.lineno, name))
    for path, astNode in astNodes.items():
        for invoke in ast.walk(astNode):
            if not isinstance(invoke, ast.Call): continue
            name = invoke.func.id if isinstance(invoke.func, ast.Name) else invoke.func.attr if isinstance(invoke.func, ast.Attribute) else ''
            if name not in parameterTable or name in variadicFunction or not any(ord(characterValue)>127 for characterValue in name): continue
            for parameterArgument in invoke.keywords:
                if parameterArgument.arg and parameterArgument.arg not in parameterTable[name]:
                    failures.append('{}:{}: {}의 매개변수 {}'.format(path.relative_to(repositoryRoot), invoke.lineno, name, parameterArgument.arg))
    for line in (projectRoot/'naming/fileNameMapping.tsv').read_text().splitlines()[1:]:
        previousItem, currentItem, processValueEntry = line.split('\t')
        if not (projectRoot/currentItem).is_file(): failures.append('moveValue file missingMethod: '+currentItem)
        if processValueEntry == '호환진입점유지' and not (projectRoot/previousItem).is_file(): failures.append('호환 entryPoint missingMethod: '+previousItem)
    examples = (projectRoot.parents[1]/'example/java/NetworkExample.java').read_text()
    for forbiddenCalls in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if forbiddenCalls in examples: failures.append('네트워크 예제에 남은 표준 직접 invoke: '+forbiddenCalls)
    # 사용자가 읽는 Java 예제는 reservedWords/리터럴을 제외한 식별자도 buildAll 한국어다.
    reservedWords = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for path in sorted((projectRoot.parents[1]/'example/java').glob('*.java')):
        source = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', path.read_text())
        for name in re.findall(r'\b[^\W\d]\w*\b', source, re.UNICODE):
            if name not in reservedWords and all(ord(characterValue)<128 for characterValue in name):
                failures.append('{}: 예제의 영어 identifierValue {}'.format(path.name, name))
    for name in ('window', 'button', 'label', 'TextField', 'ScreenElement', 'EventQueue', 'worker', 'RunnableTask', 'ActionReceiver', 'ActionNotice', 'performTask'):
        source = (projectRoot/'NativeJava/English/Native'/(name+'.java')).read_text()
        source = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', source)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', source):
            failures.append(name+': English 직접 구현에 표준 objectValue 래퍼가 남았습니다.')
    cExample = (projectRoot.parents[1]/'example/c/NetworkExample.c').read_text()
    for name in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if name in cExample: failures.append('C communication 예제에 남은 표준 name: '+name)
    pythonExample = (projectRoot.parents[1]/'example/python/NetworkExample.py').read_text()
    if 'OSError' in pythonExample or '.args' in pythonExample: failures.append('Python communication 예제에 남은 표준 exception 직접 useValue')
    headValue = (projectRoot.parents[1]/'posix-kor/arm64-native/headers/NetworkABI.h').read_text()
    for name in ('InternetFamily', 'DatagramSocket', 'DatagramProtocol', 'SocketAddress', 'InternetSocketAddress', 'createEndpoint', 'sendDatagramData'):
        if re.search(r'^#define\s+'+name+r'\b', headValue, re.M): failures.append('C 직접 implementation 대신 macroValue useValue: '+name)
    javaFileCount = 0
    for rootValue in ('source', 'User/Java', 'NativeJava'):
        for path in (projectRoot/rootValue).rglob('*.java'):
            javaFileCount += 1
            source = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', path.read_text())
            for isMatched in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', source):
                failures.append('{}: 한국어화되지 않은 Declaration {}'.format(path.relative_to(projectRoot), isMatched[1]))
            if rootValue == 'NativeJava' and re.search(r'\bthrows\s+[A-Za-z]', source):
                failures.append('{}: 공개 exception Declaration'.format(path.relative_to(projectRoot)))
    x86JavaFileCount = 0
    standardJavaNames = {'String', 'length', 'charAt'}
    for path in sorted((repositoryRoot/'os/source').glob('*.java')):
        x86JavaFileCount += 1
        source = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', path.read_text())
        for name in re.findall(r'\b[^\W\d]\w*\b', source, re.UNICODE):
            if name not in reservedWords | standardJavaNames and all(ord(characterValue)<128 for characterValue in name):
                failures.append('{}: Native 영어 identifierValue {}'.format(path.relative_to(repositoryRoot), name))
    logRecord = {'passed': False, 'python_files': fileCount, 'java_files': javaFileCount,
          'x86_java_files': x86JavaFileCount, 'host_compiler_python_files': len(sharedCompilers), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if arguments.cLanguage:
        subprocess.check_call(['python3', str(projectRoot/'tools/analyzeCNames.py')])
        analyzeValue = json.loads((projectRoot/'build/한국어화/시언어분석.json').read_text())
        failures.extend(str(error) for error in analyzeValue['error'])
        exportAbi = set(json.loads((projectRoot/'naming/standardNames.json').read_text()))
        for entryValue in analyzeValue['Declaration'].values():
            name = entryValue['name']; path = Path(entryValue['file'])
            source = path.read_bytes()
            # English 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if source[entryValue['offsetValue']:entryValue['offsetValue']+len(name)] == name.encode() and name not in exportAbi:
                failures.append('{}:{}: {}'.format(path.relative_to(projectRoot), entryValue['line'], name))
        logRecord['c_semantic_checked'] = True
        logRecord['c_source_sha256'] = {str(Path(file).relative_to(projectRoot)):hashFile for file,hashFile in analyzeValue['원문해시'].items()}
    logRecord['passed'] = not failures; logRecord['failures'] = failures
    destinationValue = projectRoot/'build/verification/naming'; destinationValue.mkdir(parents=True, exist_ok=True)
    (destinationValue/'report.json').write_text(json.dumps(logRecord, ensure_ascii=False, indent=2)+'\n')
    if failures: raise SystemExit('\n'.join(failures))
    print('PASS: English Declaration·file path·호환 entryPoint·communication examples')

if __name__ == '__main__': run()
