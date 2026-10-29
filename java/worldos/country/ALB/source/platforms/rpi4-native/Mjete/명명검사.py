#!/usr/bin/env python3
"""명명 fragment·përjashtim·경로를 검사한다. --시언어는 libclang deklarata 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

Project_rrënjë = Path(__file__).resolve().parents[1]
depo_rrënjë = Project_rrënjë.parents[1]

def Ekzekuto():
    analizues_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizues_48ee4b1b.add_argument('--시언어', action='store_true')
    Argumente = analizues_48ee4b1b.parse_args()
    실패들 = []
    punë_VALUE = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    skedar_COUNT = 0
    parametër_tabelë = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [depo_rrënjë/'compiler/컴파일러.py', depo_rrënjë/'compiler/기계어미리번역.py']
    for POZICIONI in list((Project_rrënjë/'Mjete').glob('*.py')) + list((Project_rrënjë/'예제').rglob('*.py')) + 공용번역기들:
        if POZICIONI.name.endswith(('이름반영.py', '이름분석.py')): continue
        skedar_COUNT += 1
        나무 = ast.parse(POZICIONI.read_text()); 나무들[POZICIONI] = 나무
        for futje_VALUE in ast.walk(나무):
            if isinstance(futje_VALUE, ast.FunctionDef):
                parametër_tabelë.setdefault(futje_VALUE.name, set()).update(parametër_argument.arg for parametër_argument in futje_VALUE.args.args + futje_VALUE.args.kwonlyargs)
                if futje_VALUE.args.kwarg: 가변매개함수.add(futje_VALUE.name)
            if isinstance(futje_VALUE, ast.ClassDef):
                for FUNCTION_VALUE in futje_VALUE.body:
                    if isinstance(FUNCTION_VALUE, ast.FunctionDef) and FUNCTION_VALUE.name == '__init__':
                        parametër_tabelë.setdefault(futje_VALUE.name, set()).update(parametër_argument.arg for parametër_argument in FUNCTION_VALUE.args.args + FUNCTION_VALUE.args.kwonlyargs)
            Emër = ''
            if isinstance(futje_VALUE, (ast.FunctionDef, ast.ClassDef)): Emër = futje_VALUE.name
            elif isinstance(futje_VALUE, ast.Name) and isinstance(futje_VALUE.ctx, ast.Store): Emër = futje_VALUE.id
            elif isinstance(futje_VALUE, ast.arg): Emër = futje_VALUE.arg
            if Emër and Emër not in punë_VALUE and all(ord(karakter_VALUE)<128 for karakter_VALUE in Emër):
                실패들.append('{}:{}: {}'.format(POZICIONI.relative_to(depo_rrënjë), futje_VALUE.lineno, Emër))
    for POZICIONI, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Emër = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Emër not in parametër_tabelë or Emër in 가변매개함수 or not any(ord(karakter_VALUE)>127 for karakter_VALUE in Emër): continue
            for parametër_argument in 호출.keywords:
                if parametër_argument.arg and parametër_argument.arg not in parametër_tabelë[Emër]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(POZICIONI.relative_to(depo_rrënjë), 호출.lineno, Emër, parametër_argument.arg))
    for linjë in (Project_rrënjë/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, Proces_VALUE_futje = linjë.split('\t')
        if not (Project_rrënjë/현재).is_file(): 실패들.append('lëviz_VALUE Kartelë 없음: '+현재)
        if Proces_VALUE_futje == '호환진입점유지' and not (Project_rrënjë/이전).is_file(): 실패들.append('호환 futje_p 없음: '+이전)
    예제 = (Project_rrënjë.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for POZICIONI in sorted((Project_rrënjë.parents[1]/'example/java').glob('*.java')):
        BURIMI = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', POZICIONI.read_text())
        for Emër in re.findall(r'\b[^\W\d]\w*\b', BURIMI, re.UNICODE):
            if Emër not in 예약어 and all(ord(karakter_VALUE)<128 for karakter_VALUE in Emër):
                실패들.append('{}: 예제의 영어 identifikues_VALUE {}'.format(POZICIONI.name, Emër))
    for Emër in ('Dritare', 'Buton', 'Etiketë', 'SMS_fushë', '화면구성요소', 'ngjarje_radhë', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        BURIMI = (Project_rrënjë/'한국어자바/한국어/자체'/(Emër+'.java')).read_text()
        BURIMI = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', BURIMI)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', BURIMI):
            실패들.append(Emër+': 한국어 직접 구현에 표준 objekt_VALUE 래퍼가 남았습니다.')
    시언어예제 = (Project_rrënjë.parents[1]/'example/c/네트워크예제.c').read_text()
    for Emër in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Emër in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Emër: '+Emër)
    파이썬예제 = (Project_rrënjë.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 përjashtim 직접 사용')
    머리 = (Project_rrënjë.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Emër in ('Internet_Familja', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+Emër+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 makro_VALUE 사용: '+Emër)
    자바파일수 = 0
    for rrënjë_VALUE in ('BURIMI', 'përdorues/자바', '한국어자바'):
        for POZICIONI in (Project_rrënjë/rrënjë_VALUE).rglob('*.java'):
            자바파일수 += 1
            BURIMI = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', POZICIONI.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', BURIMI):
                실패들.append('{}: 한국어화되지 않은 deklarata {}'.format(POZICIONI.relative_to(Project_rrënjë), 맞음[1]))
            if rrënjë_VALUE == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', BURIMI):
                실패들.append('{}: 공개 përjashtim deklarata'.format(POZICIONI.relative_to(Project_rrënjë)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for POZICIONI in sorted((depo_rrënjë/'os/BURIMI').glob('*.java')):
        x86자바파일수 += 1
        BURIMI = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', POZICIONI.read_text())
        for Emër in re.findall(r'\b[^\W\d]\w*\b', BURIMI, re.UNICODE):
            if Emër not in 예약어 | 표준자바이름 and all(ord(karakter_VALUE)<128 for karakter_VALUE in Emër):
                실패들.append('{}: 자체 영어 identifikues_VALUE {}'.format(POZICIONI.relative_to(depo_rrënjë), Emër))
    LOG_RECORD = {'passed': False, 'python_files': skedar_COUNT, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if Argumente.시언어:
        subprocess.check_call(['python3', str(Project_rrënjë/'Mjete/시언어이름분석.py')])
        분석 = json.loads((Project_rrënjë/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(GABIM) for GABIM in 분석['GABIM'])
        공개규약 = set(json.loads((Project_rrënjë/'명명/규격이름.json').read_text()))
        for futje_VALUE in 분석['deklarata'].values():
            Emër = futje_VALUE['Emër']; POZICIONI = Path(futje_VALUE['Kartelë'])
            BURIMI = POZICIONI.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if BURIMI[futje_VALUE['OFFSET_VALUE']:futje_VALUE['OFFSET_VALUE']+len(Emër)] == Emër.encode() and Emër not in 공개규약:
                실패들.append('{}:{}: {}'.format(POZICIONI.relative_to(Project_rrënjë), futje_VALUE['줄'], Emër))
        LOG_RECORD['c_semantic_checked'] = True
        LOG_RECORD['c_source_sha256'] = {str(Path(Kartelë).relative_to(Project_rrënjë)):hash_skedar for Kartelë,hash_skedar in 분석['원문해시'].items()}
    LOG_RECORD['passed'] = not 실패들; LOG_RECORD['failures'] = 실패들
    vendmbërritje_VALUE = Project_rrënjë/'build/verification/naming'; vendmbërritje_VALUE.mkdir(parents=True, exist_ok=True)
    (vendmbërritje_VALUE/'report.json').write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 deklarata·Kartelë POZICIONI·호환 futje_p·통신 예제')

if __name__ == '__main__': Ekzekuto()
