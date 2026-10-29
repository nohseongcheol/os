#!/usr/bin/env python3
"""명명 klip·istisno·경로를 검사한다. --시언어는 libclang e_lon_qilish 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

Project_ildiz = Path(__file__).resolve().parents[1]
repozitoriy_ildiz = Project_ildiz.parents[1]

def Bajarish():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--시언어', action='store_true')
    인수 = parser_48ee4b1b.parse_args()
    실패들 = []
    murojaat_VALUE = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    fayl_COUNT = 0
    매개변수표 = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [repozitoriy_ildiz/'compiler/컴파일러.py', repozitoriy_ildiz/'compiler/기계어미리번역.py']
    for yo_l in list((Project_ildiz/'Vositalar').glob('*.py')) + list((Project_ildiz/'예제').rglob('*.py')) + 공용번역기들:
        if yo_l.name.endswith(('이름반영.py', '이름분석.py')): continue
        fayl_COUNT += 1
        나무 = ast.parse(yo_l.read_text()); 나무들[yo_l] = 나무
        for kiritish_VALUE in ast.walk(나무):
            if isinstance(kiritish_VALUE, ast.FunctionDef):
                매개변수표.setdefault(kiritish_VALUE.name, set()).update(인자.arg for 인자 in kiritish_VALUE.args.args + kiritish_VALUE.args.kwonlyargs)
                if kiritish_VALUE.args.kwarg: 가변매개함수.add(kiritish_VALUE.name)
            if isinstance(kiritish_VALUE, ast.ClassDef):
                for FUNCTION_VALUE in kiritish_VALUE.body:
                    if isinstance(FUNCTION_VALUE, ast.FunctionDef) and FUNCTION_VALUE.name == '__init__':
                        매개변수표.setdefault(kiritish_VALUE.name, set()).update(인자.arg for 인자 in FUNCTION_VALUE.args.args + FUNCTION_VALUE.args.kwonlyargs)
            Nomi = ''
            if isinstance(kiritish_VALUE, (ast.FunctionDef, ast.ClassDef)): Nomi = kiritish_VALUE.name
            elif isinstance(kiritish_VALUE, ast.Name) and isinstance(kiritish_VALUE.ctx, ast.Store): Nomi = kiritish_VALUE.id
            elif isinstance(kiritish_VALUE, ast.arg): Nomi = kiritish_VALUE.arg
            if Nomi and Nomi not in murojaat_VALUE and all(ord(belgi_VALUE)<128 for belgi_VALUE in Nomi):
                실패들.append('{}:{}: {}'.format(yo_l.relative_to(repozitoriy_ildiz), kiritish_VALUE.lineno, Nomi))
    for yo_l, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Nomi = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Nomi not in 매개변수표 or Nomi in 가변매개함수 or not any(ord(belgi_VALUE)>127 for belgi_VALUE in Nomi): continue
            for 인자 in 호출.keywords:
                if 인자.arg and 인자.arg not in 매개변수표[Nomi]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(yo_l.relative_to(repozitoriy_ildiz), 호출.lineno, Nomi, 인자.arg))
    for satr in (Project_ildiz/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, Jarayon_VALUE_kiritish = satr.split('\t')
        if not (Project_ildiz/현재).is_file(): 실패들.append('ko_chirmoq_VALUE Fayl 없음: '+현재)
        if Jarayon_VALUE_kiritish == '호환진입점유지' and not (Project_ildiz/이전).is_file(): 실패들.append('호환 kiritish_nuqta 없음: '+이전)
    예제 = (Project_ildiz.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for yo_l in sorted((Project_ildiz.parents[1]/'example/java').glob('*.java')):
        manba = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', yo_l.read_text())
        for Nomi in re.findall(r'\b[^\W\d]\w*\b', manba, re.UNICODE):
            if Nomi not in 예약어 and all(ord(belgi_VALUE)<128 for belgi_VALUE in Nomi):
                실패들.append('{}: 예제의 영어 identifikator_VALUE {}'.format(yo_l.name, Nomi))
    for Nomi in ('창', 'tugma', 'Yorliq', 'SMS_ma_lumotlar_maydoni', '화면구성요소', 'hodisa_navbat', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        manba = (Project_ildiz/'한국어자바/한국어/자체'/(Nomi+'.java')).read_text()
        manba = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', manba)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', manba):
            실패들.append(Nomi+': 한국어 직접 구현에 표준 obyekt_VALUE 래퍼가 남았습니다.')
    시언어예제 = (Project_ildiz.parents[1]/'example/c/네트워크예제.c').read_text()
    for Nomi in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Nomi in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Nomi: '+Nomi)
    파이썬예제 = (Project_ildiz.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 istisno 직접 사용')
    머리 = (Project_ildiz.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Nomi in ('bulut_Oila', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+Nomi+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 makro_VALUE 사용: '+Nomi)
    자바파일수 = 0
    for ildiz_VALUE in ('manba', 'foydalanuvchi/자바', '한국어자바'):
        for yo_l in (Project_ildiz/ildiz_VALUE).rglob('*.java'):
            자바파일수 += 1
            manba = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', yo_l.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', manba):
                실패들.append('{}: 한국어화되지 않은 e_lon_qilish {}'.format(yo_l.relative_to(Project_ildiz), 맞음[1]))
            if ildiz_VALUE == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', manba):
                실패들.append('{}: 공개 istisno e_lon_qilish'.format(yo_l.relative_to(Project_ildiz)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for yo_l in sorted((repozitoriy_ildiz/'os/manba').glob('*.java')):
        x86자바파일수 += 1
        manba = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', yo_l.read_text())
        for Nomi in re.findall(r'\b[^\W\d]\w*\b', manba, re.UNICODE):
            if Nomi not in 예약어 | 표준자바이름 and all(ord(belgi_VALUE)<128 for belgi_VALUE in Nomi):
                실패들.append('{}: 자체 영어 identifikator_VALUE {}'.format(yo_l.relative_to(repozitoriy_ildiz), Nomi))
    LOG_satr = {'passed': False, 'python_files': fayl_COUNT, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(Project_ildiz/'Vositalar/시언어이름분석.py')])
        분석 = json.loads((Project_ildiz/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(Xato) for Xato in 분석['Xato'])
        공개규약 = set(json.loads((Project_ildiz/'명명/규격이름.json').read_text()))
        for kiritish_VALUE in 분석['e_lon_qilish'].values():
            Nomi = kiritish_VALUE['Nomi']; yo_l = Path(kiritish_VALUE['Fayl'])
            manba = yo_l.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if manba[kiritish_VALUE['OFFSET_VALUE']:kiritish_VALUE['OFFSET_VALUE']+len(Nomi)] == Nomi.encode() and Nomi not in 공개규약:
                실패들.append('{}:{}: {}'.format(yo_l.relative_to(Project_ildiz), kiritish_VALUE['줄'], Nomi))
        LOG_satr['c_semantic_checked'] = True
        LOG_satr['c_source_sha256'] = {str(Path(Fayl).relative_to(Project_ildiz)):tasodifiy_ma_lumot_fayl for Fayl,tasodifiy_ma_lumot_fayl in 분석['원문해시'].items()}
    LOG_satr['passed'] = not 실패들; LOG_satr['failures'] = 실패들
    ko_chirish_joyi_VALUE = Project_ildiz/'build/verification/naming'; ko_chirish_joyi_VALUE.mkdir(parents=True, exist_ok=True)
    (ko_chirish_joyi_VALUE/'report.json').write_text(json.dumps(LOG_satr, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 e_lon_qilish·Fayl yo_l·호환 kiritish_nuqta·통신 예제')

if __name__ == '__main__': Bajarish()
