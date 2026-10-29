#!/usr/bin/env python3
"""명명 क्लिप·예외·경로를 검사한다. --시언어는 libclang 선언 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

प्रॉजॅक्ट_रूट = Path(__file__).resolve().parents[1]
저장소 = प्रॉजॅक्ट_रूट.parents[1]

def चलोवप():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--시언어', action='store_true')
    인수 = 해석기.parse_args()
    실패들 = []
    काम_मोल = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    फायल_COUNT = 0
    매개변수표 = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for पाथ in list((प्रॉजॅक्ट_रूट/'साधनां').glob('*.py')) + list((प्रॉजॅक्ट_रूट/'예제').rglob('*.py')) + 공용번역기들:
        if पाथ.name.endswith(('이름반영.py', '이름분석.py')): continue
        फायल_COUNT += 1
        나무 = ast.parse(पाथ.read_text()); 나무들[पाथ] = 나무
        for प्रवेश_मोल in ast.walk(나무):
            if isinstance(प्रवेश_मोल, ast.FunctionDef):
                매개변수표.setdefault(प्रवेश_मोल.name, set()).update(인자.arg for 인자 in प्रवेश_मोल.args.args + प्रवेश_मोल.args.kwonlyargs)
                if प्रवेश_मोल.args.kwarg: 가변매개함수.add(प्रवेश_मोल.name)
            if isinstance(प्रवेश_मोल, ast.ClassDef):
                for फंक्शन_मोल in प्रवेश_मोल.body:
                    if isinstance(फंक्शन_मोल, ast.FunctionDef) and फंक्शन_मोल.name == '__init__':
                        매개변수표.setdefault(प्रवेश_मोल.name, set()).update(인자.arg for 인자 in फंक्शन_मोल.args.args + फंक्शन_मोल.args.kwonlyargs)
            नांव = ''
            if isinstance(प्रवेश_मोल, (ast.FunctionDef, ast.ClassDef)): नांव = प्रवेश_मोल.name
            elif isinstance(प्रवेश_मोल, ast.Name) and isinstance(प्रवेश_मोल.ctx, ast.Store): नांव = प्रवेश_मोल.id
            elif isinstance(प्रवेश_मोल, ast.arg): नांव = प्रवेश_मोल.arg
            if नांव and नांव not in काम_मोल and all(ord(वर्ण_मोल)<128 for वर्ण_मोल in नांव):
                실패들.append('{}:{}: {}'.format(पाथ.relative_to(저장소), प्रवेश_मोल.lineno, नांव))
    for पाथ, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            नांव = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if नांव not in 매개변수표 or नांव in 가변매개함수 or not any(ord(वर्ण_मोल)>127 for वर्ण_मोल in नांव): continue
            for 인자 in 호출.keywords:
                if 인자.arg and 인자.arg not in 매개변수표[नांव]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(पाथ.relative_to(저장소), 호출.lineno, नांव, 인자.arg))
    for रेग in (प्रॉजॅक्ट_रूट/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, प्रक्रिया_मोल_प्रवेश = रेग.split('\t')
        if not (प्रॉजॅक्ट_रूट/현재).is_file(): 실패들.append('हालोवचें_मोल फायल 없음: '+현재)
        if प्रक्रिया_मोल_प्रवेश == '호환진입점유지' and not (प्रॉजॅक्ट_रूट/이전).is_file(): 실패들.append('호환 प्रवेश_पॉयंट 없음: '+이전)
    예제 = (प्रॉजॅक्ट_रूट.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for पाथ in sorted((प्रॉजॅक्ट_रूट.parents[1]/'example/java').glob('*.java')):
        स्त्रोत = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', पाथ.read_text())
        for नांव in re.findall(r'\b[^\W\d]\w*\b', स्त्रोत, re.UNICODE):
            if नांव not in 예약어 and all(ord(वर्ण_मोल)<128 for वर्ण_मोल in नांव):
                실패들.append('{}: 예제의 영어 वळखुपी_मोल {}'.format(पाथ.name, नांव))
    for नांव in ('창', 'बटन', 'लेबल', 'लिखीत_मळ', '화면구성요소', 'प्रसंग_प्रतिक्षावळ', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        स्त्रोत = (प्रॉजॅक्ट_रूट/'한국어자바/한국어/자체'/(नांव+'.java')).read_text()
        स्त्रोत = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', स्त्रोत)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', स्त्रोत):
            실패들.append(नांव+': 한국어 직접 구현에 표준 ऑब्जॅक्ट_मोल 래퍼가 남았습니다.')
    시언어예제 = (प्रॉजॅक्ट_रूट.parents[1]/'example/c/네트워크예제.c').read_text()
    for नांव in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if नांव in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 नांव: '+नांव)
    파이썬예제 = (प्रॉजॅक्ट_रूट.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 예외 직접 사용')
    머리 = (प्रॉजॅक्ट_रूट.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for नांव in ('कूप_कुटुंब', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+नांव+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 मॅक्रो_मोल 사용: '+नांव)
    자바파일수 = 0
    for रूट_मोल in ('स्त्रोत', 'उपेगकर्तो/자바', '한국어자바'):
        for पाथ in (प्रॉजॅक्ट_रूट/रूट_मोल).rglob('*.java'):
            자바파일수 += 1
            स्त्रोत = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', पाथ.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', स्त्रोत):
                실패들.append('{}: 한국어화되지 않은 선언 {}'.format(पाथ.relative_to(प्रॉजॅक्ट_रूट), 맞음[1]))
            if रूट_मोल == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', स्त्रोत):
                실패들.append('{}: 공개 예외 선언'.format(पाथ.relative_to(प्रॉजॅक्ट_रूट)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for पाथ in sorted((저장소/'os/स्त्रोत').glob('*.java')):
        x86자바파일수 += 1
        स्त्रोत = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', पाथ.read_text())
        for नांव in re.findall(r'\b[^\W\d]\w*\b', स्त्रोत, re.UNICODE):
            if नांव not in 예약어 | 표준자바이름 and all(ord(वर्ण_मोल)<128 for वर्ण_मोल in नांव):
                실패들.append('{}: 자체 영어 वळखुपी_मोल {}'.format(पाथ.relative_to(저장소), नांव))
    LOG_नोंद = {'passed': False, 'python_files': फायल_COUNT, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(प्रॉजॅक्ट_रूट/'साधनां/시언어이름분석.py')])
        분석 = json.loads((प्रॉजॅक्ट_रूट/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(चूक) for चूक in 분석['चूक'])
        공개규약 = set(json.loads((प्रॉजॅक्ट_रूट/'명명/규격이름.json').read_text()))
        for प्रवेश_मोल in 분석['선언'].values():
            नांव = प्रवेश_मोल['नांव']; पाथ = Path(प्रवेश_मोल['फायल'])
            स्त्रोत = पाथ.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if स्त्रोत[प्रवेश_मोल['ऑफसॅट_मोल']:प्रवेश_मोल['ऑफसॅट_मोल']+len(नांव)] == नांव.encode() and नांव not in 공개규약:
                실패들.append('{}:{}: {}'.format(पाथ.relative_to(प्रॉजॅक्ट_रूट), प्रवेश_मोल['줄'], नांव))
        LOG_नोंद['c_semantic_checked'] = True
        LOG_नोंद['c_source_sha256'] = {str(Path(फायल).relative_to(प्रॉजॅक्ट_रूट)):हॅश_फायल for फायल,हॅश_फायल in 분석['원문해시'].items()}
    LOG_नोंद['passed'] = not 실패들; LOG_नोंद['failures'] = 실패들
    नियुक्त_स्थान_मोल = प्रॉजॅक्ट_रूट/'build/verification/naming'; नियुक्त_स्थान_मोल.mkdir(parents=True, exist_ok=True)
    (नियुक्त_स्थान_मोल/'report.json').write_text(json.dumps(LOG_नोंद, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 선언·फायल पाथ·호환 प्रवेश_पॉयंट·통신 예제')

if __name__ == '__main__': चलोवप()
