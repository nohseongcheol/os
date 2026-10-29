#!/usr/bin/env python3
"""명명 clip·eithriad·경로를 검사한다. --시언어는 libclang 선언 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

prosiect_gwraidd = Path(__file__).resolve().parents[1]
저장소 = prosiect_gwraidd.parents[1]

def Gweithredu_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--시언어', action='store_true')
    인수 = 해석기.parse_args()
    실패들 = []
    tasg_VALUE = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    ffeil_COUNT = 0
    paramedr_tabl = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for LLWYBR in list((prosiect_gwraidd/'Offer').glob('*.py')) + list((prosiect_gwraidd/'예제').rglob('*.py')) + 공용번역기들:
        if LLWYBR.name.endswith(('이름반영.py', '이름분석.py')): continue
        ffeil_COUNT += 1
        나무 = ast.parse(LLWYBR.read_text()); 나무들[LLWYBR] = 나무
        for cofnod_VALUE in ast.walk(나무):
            if isinstance(cofnod_VALUE, ast.FunctionDef):
                paramedr_tabl.setdefault(cofnod_VALUE.name, set()).update(paramedr_arg.arg for paramedr_arg in cofnod_VALUE.args.args + cofnod_VALUE.args.kwonlyargs)
                if cofnod_VALUE.args.kwarg: 가변매개함수.add(cofnod_VALUE.name)
            if isinstance(cofnod_VALUE, ast.ClassDef):
                for SWYDDOGAETH_VALUE in cofnod_VALUE.body:
                    if isinstance(SWYDDOGAETH_VALUE, ast.FunctionDef) and SWYDDOGAETH_VALUE.name == '__init__':
                        paramedr_tabl.setdefault(cofnod_VALUE.name, set()).update(paramedr_arg.arg for paramedr_arg in SWYDDOGAETH_VALUE.args.args + SWYDDOGAETH_VALUE.args.kwonlyargs)
            Enw = ''
            if isinstance(cofnod_VALUE, (ast.FunctionDef, ast.ClassDef)): Enw = cofnod_VALUE.name
            elif isinstance(cofnod_VALUE, ast.Name) and isinstance(cofnod_VALUE.ctx, ast.Store): Enw = cofnod_VALUE.id
            elif isinstance(cofnod_VALUE, ast.arg): Enw = cofnod_VALUE.arg
            if Enw and Enw not in tasg_VALUE and all(ord(nod_VALUE)<128 for nod_VALUE in Enw):
                실패들.append('{}:{}: {}'.format(LLWYBR.relative_to(저장소), cofnod_VALUE.lineno, Enw))
    for LLWYBR, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Enw = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Enw not in paramedr_tabl or Enw in 가변매개함수 or not any(ord(nod_VALUE)>127 for nod_VALUE in Enw): continue
            for paramedr_arg in 호출.keywords:
                if paramedr_arg.arg and paramedr_arg.arg not in paramedr_tabl[Enw]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(LLWYBR.relative_to(저장소), 호출.lineno, Enw, paramedr_arg.arg))
    for llinell in (prosiect_gwraidd/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, Proses_VALUE_cofnod = llinell.split('\t')
        if not (prosiect_gwraidd/현재).is_file(): 실패들.append('symud_VALUE Ffeil 없음: '+현재)
        if Proses_VALUE_cofnod == '호환진입점유지' and not (prosiect_gwraidd/이전).is_file(): 실패들.append('호환 cofnod_p 없음: '+이전)
    예제 = (prosiect_gwraidd.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for LLWYBR in sorted((prosiect_gwraidd.parents[1]/'example/java').glob('*.java')):
        FFYNHONNELL = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', LLWYBR.read_text())
        for Enw in re.findall(r'\b[^\W\d]\w*\b', FFYNHONNELL, re.UNICODE):
            if Enw not in 예약어 and all(ord(nod_VALUE)<128 for nod_VALUE in Enw):
                실패들.append('{}: 예제의 영어 dynodwr_VALUE {}'.format(LLWYBR.name, Enw))
    for Enw in ('창', 'botwm', 'label', 'maes_testun', '화면구성요소', 'digwyddiad_ciw', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        FFYNHONNELL = (prosiect_gwraidd/'한국어자바/Cymraeg/자체'/(Enw+'.java')).read_text()
        FFYNHONNELL = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', FFYNHONNELL)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', FFYNHONNELL):
            실패들.append(Enw+': Cymraeg 직접 구현에 표준 gwrthrych_VALUE 래퍼가 남았습니다.')
    시언어예제 = (prosiect_gwraidd.parents[1]/'example/c/네트워크예제.c').read_text()
    for Enw in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Enw in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Enw: '+Enw)
    파이썬예제 = (prosiect_gwraidd.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 eithriad 직접 사용')
    머리 = (prosiect_gwraidd.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Enw in ('cwmwl_Teulu', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+Enw+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 macro_VALUE 사용: '+Enw)
    자바파일수 = 0
    for gwraidd_VALUE in ('FFYNHONNELL', 'defnyddiwr/자바', '한국어자바'):
        for LLWYBR in (prosiect_gwraidd/gwraidd_VALUE).rglob('*.java'):
            자바파일수 += 1
            FFYNHONNELL = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', LLWYBR.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', FFYNHONNELL):
                실패들.append('{}: 한국어화되지 않은 선언 {}'.format(LLWYBR.relative_to(prosiect_gwraidd), 맞음[1]))
            if gwraidd_VALUE == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', FFYNHONNELL):
                실패들.append('{}: 공개 eithriad 선언'.format(LLWYBR.relative_to(prosiect_gwraidd)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for LLWYBR in sorted((저장소/'os/FFYNHONNELL').glob('*.java')):
        x86자바파일수 += 1
        FFYNHONNELL = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', LLWYBR.read_text())
        for Enw in re.findall(r'\b[^\W\d]\w*\b', FFYNHONNELL, re.UNICODE):
            if Enw not in 예약어 | 표준자바이름 and all(ord(nod_VALUE)<128 for nod_VALUE in Enw):
                실패들.append('{}: 자체 영어 dynodwr_VALUE {}'.format(LLWYBR.relative_to(저장소), Enw))
    LOG_rhes = {'passed': False, 'python_files': ffeil_COUNT, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(prosiect_gwraidd/'Offer/시언어이름분석.py')])
        Dadansoddi_VALUE = json.loads((prosiect_gwraidd/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(Gwall) for Gwall in Dadansoddi_VALUE['Gwall'])
        공개규약 = set(json.loads((prosiect_gwraidd/'명명/규격이름.json').read_text()))
        for cofnod_VALUE in Dadansoddi_VALUE['선언'].values():
            Enw = cofnod_VALUE['Enw']; LLWYBR = Path(cofnod_VALUE['Ffeil'])
            FFYNHONNELL = LLWYBR.read_bytes()
            # Cymraeg 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if FFYNHONNELL[cofnod_VALUE['OFFSET_VALUE']:cofnod_VALUE['OFFSET_VALUE']+len(Enw)] == Enw.encode() and Enw not in 공개규약:
                실패들.append('{}:{}: {}'.format(LLWYBR.relative_to(prosiect_gwraidd), cofnod_VALUE['줄'], Enw))
        LOG_rhes['c_semantic_checked'] = True
        LOG_rhes['c_source_sha256'] = {str(Path(Ffeil).relative_to(prosiect_gwraidd)):hash_ffeil for Ffeil,hash_ffeil in Dadansoddi_VALUE['원문해시'].items()}
    LOG_rhes['passed'] = not 실패들; LOG_rhes['failures'] = 실패들
    cyrchfan_VALUE = prosiect_gwraidd/'build/verification/naming'; cyrchfan_VALUE.mkdir(parents=True, exist_ok=True)
    (cyrchfan_VALUE/'report.json').write_text(json.dumps(LOG_rhes, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: Cymraeg 선언·Ffeil LLWYBR·호환 cofnod_p·통신 예제')

if __name__ == '__main__': Gweithredu_2()
