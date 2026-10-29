#!/usr/bin/env python3
"""명명 क्लिप·अपवाद·경로를 검사한다. --시언어는 libclang घोषणा 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

प्रोजेक्ट_करें_मूल = Path(__file__).resolve().parents[1]
संग्रह_मूल = प्रोजेक्ट_करें_मूल.parents[1]

def चलाएँ():
    पार्सर_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    पार्सर_48ee4b1b.add_argument('--सी_भाषा', action='store_true')
    तर्क = पार्सर_48ee4b1b.parse_args()
    실패들 = []
    मामला_मान = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    पैरामीटर_तालिका = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [संग्रह_मूल/'compiler/कंपाइलर.py', संग्रह_मूल/'compiler/पूर्वसंकलक.py']
    for पथ in list((प्रोजेक्ट_करें_मूल/'उपकरण').glob('*.py')) + list((प्रोजेक्ट_करें_मूल/'예제').rglob('*.py')) + 공용번역기들:
        if पथ.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(पथ.read_text()); 나무들[पथ] = 나무
        for एन्ट्री_मान in ast.walk(나무):
            if isinstance(एन्ट्री_मान, ast.FunctionDef):
                पैरामीटर_तालिका.setdefault(एन्ट्री_मान.name, set()).update(पैरामीटर_तर्क.arg for पैरामीटर_तर्क in एन्ट्री_मान.args.args + एन्ट्री_मान.args.kwonlyargs)
                if एन्ट्री_मान.args.kwarg: 가변매개함수.add(एन्ट्री_मान.name)
            if isinstance(एन्ट्री_मान, ast.ClassDef):
                for फ़ंक्_शन_मान in एन्ट्री_मान.body:
                    if isinstance(फ़ंक्_शन_मान, ast.FunctionDef) and फ़ंक्_शन_मान.name == '__init__':
                        पैरामीटर_तालिका.setdefault(एन्ट्री_मान.name, set()).update(पैरामीटर_तर्क.arg for पैरामीटर_तर्क in फ़ंक्_शन_मान.args.args + फ़ंक्_शन_मान.args.kwonlyargs)
            नाम = ''
            if isinstance(एन्ट्री_मान, (ast.FunctionDef, ast.ClassDef)): नाम = एन्ट्री_मान.name
            elif isinstance(एन्ट्री_मान, ast.Name) and isinstance(एन्ट्री_मान.ctx, ast.Store): नाम = एन्ट्री_मान.id
            elif isinstance(एन्ट्री_मान, ast.arg): नाम = एन्ट्री_मान.arg
            if नाम and नाम not in मामला_मान and all(ord(कैरेक्टर_मान)<128 for कैरेक्टर_मान in नाम):
                실패들.append('{}:{}: {}'.format(पथ.relative_to(संग्रह_मूल), एन्ट्री_मान.lineno, नाम))
    for पथ, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            नाम = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if नाम not in पैरामीटर_तालिका or नाम in 가변매개함수 or not any(ord(कैरेक्टर_मान)>127 for कैरेक्टर_मान in नाम): continue
            for पैरामीटर_तर्क in 호출.keywords:
                if पैरामीटर_तर्क.arg and पैरामीटर_तर्क.arg not in पैरामीटर_तालिका[नाम]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(पथ.relative_to(संग्रह_मूल), 호출.lineno, नाम, पैरामीटर_तर्क.arg))
    for पंक्ति in (प्रोजेक्ट_करें_मूल/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, अद्यतित_आइटम, प्रक्रिया_मान_एन्ट्री = पंक्ति.split('\t')
        if not (प्रोजेक्ट_करें_मूल/अद्यतित_आइटम).is_file(): 실패들.append('ले_जाएँ_मान संचिका 없음: '+अद्यतित_आइटम)
        if प्रक्रिया_मान_एन्ट्री == '호환진입점유지' and not (प्रोजेक्ट_करें_मूल/이전).is_file(): 실패들.append('호환 प्रवेश_बिदुं 없음: '+이전)
    예제 = (प्रोजेक्ट_करें_मूल.parents[1]/'example/java/जालउदाहरण.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for पथ in sorted((प्रोजेक्ट_करें_मूल.parents[1]/'example/java').glob('*.java')):
        स्रोत = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', पथ.read_text())
        for नाम in re.findall(r'\b[^\W\d]\w*\b', स्रोत, re.UNICODE):
            if नाम not in 예약어 and all(ord(कैरेक्टर_मान)<128 for कैरेक्टर_मान in नाम):
                실패들.append('{}: 예제의 영어 पहचानकर्ता_मान {}'.format(पथ.name, नाम))
    for नाम in ('खिड़की', 'बटन', 'लेबल', 'पाठ_फ़ील्ड', '화면구성요소', 'घटना_कतार', 'कार्यसूत्र', '실행할일', '동작받이', 'एक्शन_सूचना', '작업'):
        स्रोत = (प्रोजेक्ट_करें_मूल/'한국어자바/हिंदी/निज'/(नाम+'.java')).read_text()
        स्रोत = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', स्रोत)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', स्रोत):
            실패들.append(नाम+': हिंदी 직접 구현에 표준 ऑब्जेक्ट_मान 래퍼가 남았습니다.')
    시언어예제 = (प्रोजेक्ट_करें_मूल.parents[1]/'example/c/जालउदाहरण.c').read_text()
    for नाम in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if नाम in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 नाम: '+नाम)
    파이썬예제 = (प्रोजेक्ट_करें_मूल.parents[1]/'example/python/जालउदाहरण.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 अपवाद 직접 사용')
    머리 = (प्रोजेक्ट_करें_मूल.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for नाम in ('क्लाउड_समूह', '전문통신', '전문전송규약', 'सॉकेट_पता', 'क्लाउड_सॉकेट_पता', 'बनाएँ_एंडपॉइंट', '자료전문보내기'):
        if re.search(r'^#define\s+'+नाम+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 मैक्रो_मान 사용: '+नाम)
    자바파일수 = 0
    for मूल_मान in ('स्रोत', 'उपयोगकर्ता/자바', '한국어자바'):
        for पथ in (प्रोजेक्ट_करें_मूल/मूल_मान).rglob('*.java'):
            자바파일수 += 1
            स्रोत = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', पथ.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', स्रोत):
                실패들.append('{}: 한국어화되지 않은 घोषणा {}'.format(पथ.relative_to(प्रोजेक्ट_करें_मूल), 맞음[1]))
            if मूल_मान == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', स्रोत):
                실패들.append('{}: 공개 अपवाद घोषणा'.format(पथ.relative_to(प्रोजेक्ट_करें_मूल)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for पथ in sorted((संग्रह_मूल/'os/स्रोत').glob('*.java')):
        x86자바파일수 += 1
        स्रोत = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', पथ.read_text())
        for नाम in re.findall(r'\b[^\W\d]\w*\b', स्रोत, re.UNICODE):
            if नाम not in 예약어 | 표준자바이름 and all(ord(कैरेक्टर_मान)<128 for कैरेक्टर_मान in नाम):
                실패들.append('{}: निज 영어 पहचानकर्ता_मान {}'.format(पथ.relative_to(संग्रह_मूल), नाम))
    लॉग_रिकॉर्ड = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if तर्क.सी_भाषा:
        subprocess.check_call(['python3', str(प्रोजेक्ट_करें_मूल/'उपकरण/시언어이름분석.py')])
        विश्लेषण_मान = json.loads((प्रोजेक्ट_करें_मूल/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(त्रुटि) for त्रुटि in विश्लेषण_मान['त्रुटि'])
        공개규약 = set(json.loads((प्रोजेक्ट_करें_मूल/'명명/규격이름.json').read_text()))
        for एन्ट्री_मान in विश्लेषण_मान['घोषणा'].values():
            नाम = एन्ट्री_मान['नाम']; पथ = Path(एन्ट्री_मान['संचिका'])
            स्रोत = पथ.read_bytes()
            # हिंदी 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if स्रोत[एन्ट्री_मान['ऑफ़सेट_मान']:एन्ट्री_मान['ऑफ़सेट_मान']+len(नाम)] == नाम.encode() and नाम not in 공개규약:
                실패들.append('{}:{}: {}'.format(पथ.relative_to(प्रोजेक्ट_करें_मूल), एन्ट्री_मान['पंक्ति'], नाम))
        लॉग_रिकॉर्ड['c_semantic_checked'] = True
        लॉग_रिकॉर्ड['c_source_sha256'] = {str(Path(संचिका).relative_to(प्रोजेक्ट_करें_मूल)):हैश_फ़ाइल for संचिका,हैश_फ़ाइल in विश्लेषण_मान['원문해시'].items()}
    लॉग_रिकॉर्ड['passed'] = not 실패들; लॉग_रिकॉर्ड['failures'] = 실패들
    गंतव्य_मान = प्रोजेक्ट_करें_मूल/'build/verification/naming'; गंतव्य_मान.mkdir(parents=True, exist_ok=True)
    (गंतव्य_मान/'report.json').write_text(json.dumps(लॉग_रिकॉर्ड, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: हिंदी घोषणा·संचिका पथ·호환 प्रवेश_बिदुं·통신 예제')

if __name__ == '__main__': चलाएँ()
