#!/usr/bin/env python3
"""명명 Clip·예외·경로를 검사한다. --시언어는 libclang 선언 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

projezéieren_Racinn = Path(__file__).resolve().parents[1]
저장소 = projezéieren_Racinn.parents[1]

def Laf():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--시언어', action='store_true')
    인수 = 해석기.parse_args()
    실패들 = []
    Job_VALUE = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    Fichier_COUNT = 0
    매개변수표 = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for Wee in list((projezéieren_Racinn/'Tools').glob('*.py')) + list((projezéieren_Racinn/'예제').rglob('*.py')) + 공용번역기들:
        if Wee.name.endswith(('이름반영.py', '이름분석.py')): continue
        Fichier_COUNT += 1
        나무 = ast.parse(Wee.read_text()); 나무들[Wee] = 나무
        for Agab_VALUE in ast.walk(나무):
            if isinstance(Agab_VALUE, ast.FunctionDef):
                매개변수표.setdefault(Agab_VALUE.name, set()).update(인자.arg for 인자 in Agab_VALUE.args.args + Agab_VALUE.args.kwonlyargs)
                if Agab_VALUE.args.kwarg: 가변매개함수.add(Agab_VALUE.name)
            if isinstance(Agab_VALUE, ast.ClassDef):
                for FUNCTION_VALUE in Agab_VALUE.body:
                    if isinstance(FUNCTION_VALUE, ast.FunctionDef) and FUNCTION_VALUE.name == '__init__':
                        매개변수표.setdefault(Agab_VALUE.name, set()).update(인자.arg for 인자 in FUNCTION_VALUE.args.args + FUNCTION_VALUE.args.kwonlyargs)
            Numm = ''
            if isinstance(Agab_VALUE, (ast.FunctionDef, ast.ClassDef)): Numm = Agab_VALUE.name
            elif isinstance(Agab_VALUE, ast.Name) and isinstance(Agab_VALUE.ctx, ast.Store): Numm = Agab_VALUE.id
            elif isinstance(Agab_VALUE, ast.arg): Numm = Agab_VALUE.arg
            if Numm and Numm not in Job_VALUE and all(ord(Zeechen_VALUE)<128 for Zeechen_VALUE in Numm):
                실패들.append('{}:{}: {}'.format(Wee.relative_to(저장소), Agab_VALUE.lineno, Numm))
    for Wee, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Numm = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Numm not in 매개변수표 or Numm in 가변매개함수 or not any(ord(Zeechen_VALUE)>127 for Zeechen_VALUE in Numm): continue
            for 인자 in 호출.keywords:
                if 인자.arg and 인자.arg not in 매개변수표[Numm]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(Wee.relative_to(저장소), 호출.lineno, Numm, 인자.arg))
    for Zeil in (projezéieren_Racinn/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, Prozess_VALUE_Agab = Zeil.split('\t')
        if not (projezéieren_Racinn/현재).is_file(): 실패들.append('verréckelen_VALUE Fichier 없음: '+현재)
        if Prozess_VALUE_Agab == '호환진입점유지' and not (projezéieren_Racinn/이전).is_file(): 실패들.append('호환 Agab_Punkt 없음: '+이전)
    예제 = (projezéieren_Racinn.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for Wee in sorted((projezéieren_Racinn.parents[1]/'example/java').glob('*.java')):
        Quell = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Wee.read_text())
        for Numm in re.findall(r'\b[^\W\d]\w*\b', Quell, re.UNICODE):
            if Numm not in 예약어 and all(ord(Zeechen_VALUE)<128 for Zeechen_VALUE in Numm):
                실패들.append('{}: 예제의 영어 Identifikateur_VALUE {}'.format(Wee.name, Numm))
    for Numm in ('창', 'Tast', 'Numm_5ce2bd6f', 'Textfeld', '화면구성요소', 'Evenement_Schlaang', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        Quell = (projezéieren_Racinn/'한국어자바/한국어/자체'/(Numm+'.java')).read_text()
        Quell = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', Quell)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', Quell):
            실패들.append(Numm+': 한국어 직접 구현에 표준 Objet_VALUE 래퍼가 남았습니다.')
    시언어예제 = (projezéieren_Racinn.parents[1]/'example/c/네트워크예제.c').read_text()
    for Numm in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Numm in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Numm: '+Numm)
    파이썬예제 = (projezéieren_Racinn.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 예외 직접 사용')
    머리 = (projezéieren_Racinn.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Numm in ('Cloud_Famill', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+Numm+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 Makro_VALUE 사용: '+Numm)
    자바파일수 = 0
    for Racinn_VALUE in ('Quell', 'Benotzer/자바', '한국어자바'):
        for Wee in (projezéieren_Racinn/Racinn_VALUE).rglob('*.java'):
            자바파일수 += 1
            Quell = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Wee.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', Quell):
                실패들.append('{}: 한국어화되지 않은 선언 {}'.format(Wee.relative_to(projezéieren_Racinn), 맞음[1]))
            if Racinn_VALUE == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', Quell):
                실패들.append('{}: 공개 예외 선언'.format(Wee.relative_to(projezéieren_Racinn)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for Wee in sorted((저장소/'os/Quell').glob('*.java')):
        x86자바파일수 += 1
        Quell = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Wee.read_text())
        for Numm in re.findall(r'\b[^\W\d]\w*\b', Quell, re.UNICODE):
            if Numm not in 예약어 | 표준자바이름 and all(ord(Zeechen_VALUE)<128 for Zeechen_VALUE in Numm):
                실패들.append('{}: 자체 영어 Identifikateur_VALUE {}'.format(Wee.relative_to(저장소), Numm))
    LOG_Rei = {'passed': False, 'python_files': Fichier_COUNT, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(projezéieren_Racinn/'Tools/시언어이름분석.py')])
        분석 = json.loads((projezéieren_Racinn/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(Feeler) for Feeler in 분석['Feeler'])
        공개규약 = set(json.loads((projezéieren_Racinn/'명명/규격이름.json').read_text()))
        for Agab_VALUE in 분석['선언'].values():
            Numm = Agab_VALUE['Numm']; Wee = Path(Agab_VALUE['Fichier'])
            Quell = Wee.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if Quell[Agab_VALUE['OFFSET_VALUE']:Agab_VALUE['OFFSET_VALUE']+len(Numm)] == Numm.encode() and Numm not in 공개규약:
                실패들.append('{}:{}: {}'.format(Wee.relative_to(projezéieren_Racinn), Agab_VALUE['줄'], Numm))
        LOG_Rei['c_semantic_checked'] = True
        LOG_Rei['c_source_sha256'] = {str(Path(Fichier).relative_to(projezéieren_Racinn)):Hash_Fichier for Fichier,Hash_Fichier in 분석['원문해시'].items()}
    LOG_Rei['passed'] = not 실패들; LOG_Rei['failures'] = 실패들
    Zil_VALUE = projezéieren_Racinn/'build/verification/naming'; Zil_VALUE.mkdir(parents=True, exist_ok=True)
    (Zil_VALUE/'report.json').write_text(json.dumps(LOG_Rei, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 선언·Fichier Wee·호환 Agab_Punkt·통신 예제')

if __name__ == '__main__': Laf()
