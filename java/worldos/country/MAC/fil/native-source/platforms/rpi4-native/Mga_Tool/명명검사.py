#!/usr/bin/env python3
"""명명 clip·pagbubukod·경로를 검사한다. --시언어는 libclang declaration 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

Project_root = Path(__file__).resolve().parents[1]
repository_root = Project_root.parents[1]

def run():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--시언어', action='store_true')
    인수 = parser_48ee4b1b.parse_args()
    실패들 = []
    kaso_VALUE = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    file_COUNT = 0
    parameter_talahanayan = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [repository_root/'compiler/컴파일러.py', repository_root/'compiler/기계어미리번역.py']
    for path in list((Project_root/'Mga_Tool').glob('*.py')) + list((Project_root/'예제').rglob('*.py')) + 공용번역기들:
        if path.name.endswith(('이름반영.py', '이름분석.py')): continue
        file_COUNT += 1
        나무 = ast.parse(path.read_text()); 나무들[path] = 나무
        for pagpasok_VALUE in ast.walk(나무):
            if isinstance(pagpasok_VALUE, ast.FunctionDef):
                parameter_talahanayan.setdefault(pagpasok_VALUE.name, set()).update(parameter_argumento.arg for parameter_argumento in pagpasok_VALUE.args.args + pagpasok_VALUE.args.kwonlyargs)
                if pagpasok_VALUE.args.kwarg: 가변매개함수.add(pagpasok_VALUE.name)
            if isinstance(pagpasok_VALUE, ast.ClassDef):
                for pormula_VALUE in pagpasok_VALUE.body:
                    if isinstance(pormula_VALUE, ast.FunctionDef) and pormula_VALUE.name == '__init__':
                        parameter_talahanayan.setdefault(pagpasok_VALUE.name, set()).update(parameter_argumento.arg for parameter_argumento in pormula_VALUE.args.args + pormula_VALUE.args.kwonlyargs)
            pangalan = ''
            if isinstance(pagpasok_VALUE, (ast.FunctionDef, ast.ClassDef)): pangalan = pagpasok_VALUE.name
            elif isinstance(pagpasok_VALUE, ast.Name) and isinstance(pagpasok_VALUE.ctx, ast.Store): pangalan = pagpasok_VALUE.id
            elif isinstance(pagpasok_VALUE, ast.arg): pangalan = pagpasok_VALUE.arg
            if pangalan and pangalan not in kaso_VALUE and all(ord(karakter_VALUE)<128 for karakter_VALUE in pangalan):
                실패들.append('{}:{}: {}'.format(path.relative_to(repository_root), pagpasok_VALUE.lineno, pangalan))
    for path, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            pangalan = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if pangalan not in parameter_talahanayan or pangalan in 가변매개함수 or not any(ord(karakter_VALUE)>127 for karakter_VALUE in pangalan): continue
            for parameter_argumento in 호출.keywords:
                if parameter_argumento.arg and parameter_argumento.arg not in parameter_talahanayan[pangalan]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(path.relative_to(repository_root), 호출.lineno, pangalan, parameter_argumento.arg))
    for linya in (Project_root/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, Proseso_VALUE_pagpasok = linya.split('\t')
        if not (Project_root/현재).is_file(): 실패들.append('ilipat_VALUE file 없음: '+현재)
        if Proseso_VALUE_pagpasok == '호환진입점유지' and not (Project_root/이전).is_file(): 실패들.append('호환 pagpasok_point 없음: '+이전)
    예제 = (Project_root.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for path in sorted((Project_root.parents[1]/'example/java').glob('*.java')):
        pinagmulan = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', path.read_text())
        for pangalan in re.findall(r'\b[^\W\d]\w*\b', pinagmulan, re.UNICODE):
            if pangalan not in 예약어 and all(ord(karakter_VALUE)<128 for karakter_VALUE in pangalan):
                실패들.append('{}: 예제의 영어 tagakilala_VALUE {}'.format(path.name, pangalan))
    for pangalan in ('창', 'button', 'label', 'SMS_field', '화면구성요소', 'kaganapan_pila', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        pinagmulan = (Project_root/'한국어자바/한국어/자체'/(pangalan+'.java')).read_text()
        pinagmulan = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', pinagmulan)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', pinagmulan):
            실패들.append(pangalan+': 한국어 직접 구현에 표준 bagay_VALUE 래퍼가 남았습니다.')
    시언어예제 = (Project_root.parents[1]/'example/c/네트워크예제.c').read_text()
    for pangalan in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if pangalan in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 pangalan: '+pangalan)
    파이썬예제 = (Project_root.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 pagbubukod 직접 사용')
    머리 = (Project_root.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for pangalan in ('cloud_Pamilya', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+pangalan+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 makro_VALUE 사용: '+pangalan)
    자바파일수 = 0
    for root_VALUE in ('pinagmulan', 'gumagamit/자바', '한국어자바'):
        for path in (Project_root/root_VALUE).rglob('*.java'):
            자바파일수 += 1
            pinagmulan = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', path.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', pinagmulan):
                실패들.append('{}: 한국어화되지 않은 declaration {}'.format(path.relative_to(Project_root), 맞음[1]))
            if root_VALUE == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', pinagmulan):
                실패들.append('{}: 공개 pagbubukod declaration'.format(path.relative_to(Project_root)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for path in sorted((repository_root/'os/pinagmulan').glob('*.java')):
        x86자바파일수 += 1
        pinagmulan = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', path.read_text())
        for pangalan in re.findall(r'\b[^\W\d]\w*\b', pinagmulan, re.UNICODE):
            if pangalan not in 예약어 | 표준자바이름 and all(ord(karakter_VALUE)<128 for karakter_VALUE in pangalan):
                실패들.append('{}: 자체 영어 tagakilala_VALUE {}'.format(path.relative_to(repository_root), pangalan))
    LOG_hanay = {'passed': False, 'python_files': file_COUNT, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(Project_root/'Mga_Tool/시언어이름분석.py')])
        분석 = json.loads((Project_root/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(error) for error in 분석['error'])
        공개규약 = set(json.loads((Project_root/'명명/규격이름.json').read_text()))
        for pagpasok_VALUE in 분석['declaration'].values():
            pangalan = pagpasok_VALUE['pangalan']; path = Path(pagpasok_VALUE['file'])
            pinagmulan = path.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if pinagmulan[pagpasok_VALUE['OFFSET_VALUE']:pagpasok_VALUE['OFFSET_VALUE']+len(pangalan)] == pangalan.encode() and pangalan not in 공개규약:
                실패들.append('{}:{}: {}'.format(path.relative_to(Project_root), pagpasok_VALUE['줄'], pangalan))
        LOG_hanay['c_semantic_checked'] = True
        LOG_hanay['c_source_sha256'] = {str(Path(file).relative_to(Project_root)):hash_file for file,hash_file in 분석['원문해시'].items()}
    LOG_hanay['passed'] = not 실패들; LOG_hanay['failures'] = 실패들
    patutunguhan_VALUE = Project_root/'build/verification/naming'; patutunguhan_VALUE.mkdir(parents=True, exist_ok=True)
    (patutunguhan_VALUE/'report.json').write_text(json.dumps(LOG_hanay, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 declaration·file path·호환 pagpasok_point·통신 예제')

if __name__ == '__main__': run()
