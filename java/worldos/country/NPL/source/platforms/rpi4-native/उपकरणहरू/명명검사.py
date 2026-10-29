#!/usr/bin/env python3
"""명명 क्लिप·예외·경로를 검사한다. --시언어는 libclang 선언 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

परियोजना_रूट = Path(__file__).resolve().parents[1]
저장소 = परियोजना_रूट.parents[1]

def चलाउनुहोस्():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--시언어', action='store_true')
    तर्क = 해석기.parse_args()
    실패들 = []
    केस_मान = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    매개변수표 = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for मार्ग in list((परियोजना_रूट/'उपकरणहरू').glob('*.py')) + list((परियोजना_रूट/'예제').rglob('*.py')) + 공용번역기들:
        if मार्ग.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(मार्ग.read_text()); 나무들[मार्ग] = 나무
        for प्रविष्टि_मान in ast.walk(나무):
            if isinstance(प्रविष्टि_मान, ast.FunctionDef):
                매개변수표.setdefault(प्रविष्टि_मान.name, set()).update(인자.arg for 인자 in प्रविष्टि_मान.args.args + प्रविष्टि_मान.args.kwonlyargs)
                if प्रविष्टि_मान.args.kwarg: 가변매개함수.add(प्रविष्टि_मान.name)
            if isinstance(प्रविष्टि_मान, ast.ClassDef):
                for प्रकार्य_मान in प्रविष्टि_मान.body:
                    if isinstance(प्रकार्य_मान, ast.FunctionDef) and प्रकार्य_मान.name == '__init__':
                        매개변수표.setdefault(प्रविष्टि_मान.name, set()).update(인자.arg for 인자 in प्रकार्य_मान.args.args + प्रकार्य_मान.args.kwonlyargs)
            नाम = ''
            if isinstance(प्रविष्टि_मान, (ast.FunctionDef, ast.ClassDef)): नाम = प्रविष्टि_मान.name
            elif isinstance(प्रविष्टि_मान, ast.Name) and isinstance(प्रविष्टि_मान.ctx, ast.Store): नाम = प्रविष्टि_मान.id
            elif isinstance(प्रविष्टि_मान, ast.arg): नाम = प्रविष्टि_मान.arg
            if नाम and नाम not in केस_मान and all(ord(वर्ण_मान)<128 for वर्ण_मान in नाम):
                실패들.append('{}:{}: {}'.format(मार्ग.relative_to(저장소), प्रविष्टि_मान.lineno, नाम))
    for मार्ग, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            नाम = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if नाम not in 매개변수표 or नाम in 가변매개함수 or not any(ord(वर्ण_मान)>127 for वर्ण_मान in नाम): continue
            for 인자 in 호출.keywords:
                if 인자.arg and 인자.arg not in 매개변수표[नाम]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(मार्ग.relative_to(저장소), 호출.lineno, नाम, 인자.arg))
    for रेखा in (परियोजना_रूट/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, प्रक्रिया_मान_प्रविष्टि = रेखा.split('\t')
        if not (परियोजना_रूट/현재).is_file(): 실패들.append('लैजानुहोस्_मान फाइल 없음: '+현재)
        if प्रक्रिया_मान_प्रविष्टि == '호환진입점유지' and not (परियोजना_रूट/이전).is_file(): 실패들.append('호환 प्रविष्टि_अंक 없음: '+이전)
    예제 = (परियोजना_रूट.parents[1]/'example/java/सञ्जालउदाहरण.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for मार्ग in sorted((परियोजना_रूट.parents[1]/'example/java').glob('*.java')):
        स्रोत = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', मार्ग.read_text())
        for नाम in re.findall(r'\b[^\W\d]\w*\b', स्रोत, re.UNICODE):
            if नाम not in 예약어 and all(ord(वर्ण_मान)<128 for वर्ण_मान in नाम):
                실패들.append('{}: 예제의 영어 परिचायक_मान {}'.format(मार्ग.name, नाम))
    for नाम in ('창', 'बटन', 'लेबुल', 'पाठ_क्षेत्र', '화면구성요소', 'घटना_लाइन', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        स्रोत = (परियोजना_रूट/'한국어자바/नेपाली/निज'/(नाम+'.java')).read_text()
        स्रोत = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', स्रोत)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', स्रोत):
            실패들.append(नाम+': नेपाली 직접 구현에 표준 वस्तु_मान 래퍼가 남았습니다.')
    시언어예제 = (परियोजना_रूट.parents[1]/'example/c/सञ्जालउदाहरण.c').read_text()
    for नाम in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if नाम in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 नाम: '+नाम)
    파이썬예제 = (परियोजना_रूट.parents[1]/'example/python/सञ्जालउदाहरण.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 예외 직접 사용')
    머리 = (परियोजना_रूट.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for नाम in ('क्लाउड_परिवार', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+नाम+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 म्याक्रो_मान 사용: '+नाम)
    자바파일수 = 0
    for रूट_मान in ('स्रोत', 'प्रयोगकर्ता/자바', '한국어자바'):
        for मार्ग in (परियोजना_रूट/रूट_मान).rglob('*.java'):
            자바파일수 += 1
            स्रोत = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', मार्ग.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', स्रोत):
                실패들.append('{}: 한국어화되지 않은 선언 {}'.format(मार्ग.relative_to(परियोजना_रूट), 맞음[1]))
            if रूट_मान == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', स्रोत):
                실패들.append('{}: 공개 예외 선언'.format(मार्ग.relative_to(परियोजना_रूट)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for मार्ग in sorted((저장소/'os/स्रोत').glob('*.java')):
        x86자바파일수 += 1
        स्रोत = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', मार्ग.read_text())
        for नाम in re.findall(r'\b[^\W\d]\w*\b', स्रोत, re.UNICODE):
            if नाम not in 예약어 | 표준자바이름 and all(ord(वर्ण_मान)<128 for वर्ण_मान in नाम):
                실패들.append('{}: निज 영어 परिचायक_मान {}'.format(मार्ग.relative_to(저장소), नाम))
    लग_रेकर्ड = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if तर्क.시언어:
        subprocess.check_call(['python3', str(परियोजना_रूट/'उपकरणहरू/시언어이름분석.py')])
        분석 = json.loads((परियोजना_रूट/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(त्रुटि) for त्रुटि in 분석['त्रुटि'])
        공개규약 = set(json.loads((परियोजना_रूट/'명명/규격이름.json').read_text()))
        for प्रविष्टि_मान in 분석['선언'].values():
            नाम = प्रविष्टि_मान['नाम']; मार्ग = Path(प्रविष्टि_मान['फाइल'])
            स्रोत = मार्ग.read_bytes()
            # नेपाली 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if स्रोत[प्रविष्टि_मान['अफसेट_मान']:प्रविष्टि_मान['अफसेट_मान']+len(नाम)] == नाम.encode() and नाम not in 공개규약:
                실패들.append('{}:{}: {}'.format(मार्ग.relative_to(परियोजना_रूट), प्रविष्टि_मान['줄'], नाम))
        लग_रेकर्ड['c_semantic_checked'] = True
        लग_रेकर्ड['c_source_sha256'] = {str(Path(फाइल).relative_to(परियोजना_रूट)):ह्यास_फाइल for फाइल,ह्यास_फाइल in 분석['원문해시'].items()}
    लग_रेकर्ड['passed'] = not 실패들; लग_रेकर्ड['failures'] = 실패들
    गन्तव्य_मान = परियोजना_रूट/'build/verification/naming'; गन्तव्य_मान.mkdir(parents=True, exist_ok=True)
    (गन्तव्य_मान/'report.json').write_text(json.dumps(लग_रेकर्ड, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: नेपाली 선언·फाइल मार्ग·호환 प्रविष्टि_अंक·통신 예제')

if __name__ == '__main__': चलाउनुहोस्()
