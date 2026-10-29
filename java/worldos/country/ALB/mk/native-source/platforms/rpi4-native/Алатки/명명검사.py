#!/usr/bin/env python3
"""명명 клип·исклучок·경로를 검사한다. --시언어는 libclang декларација 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

Project_корен = Path(__file__).resolve().parents[1]
склад_корен = Project_корен.parents[1]

def Изврши_2():
    анализатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    анализатор_48ee4b1b.add_argument('--시언어', action='store_true')
    Аргументи = анализатор_48ee4b1b.parse_args()
    실패들 = []
    задача_VALUE_102996da = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    датотека_COUNT = 0
    параметар_табела = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [склад_корен/'compiler/컴파일러.py', склад_корен/'compiler/기계어미리번역.py']
    for ПАТЕКА in list((Project_корен/'Алатки').glob('*.py')) + list((Project_корен/'예제').rglob('*.py')) + 공용번역기들:
        if ПАТЕКА.name.endswith(('이름반영.py', '이름분석.py')): continue
        датотека_COUNT += 1
        나무 = ast.parse(ПАТЕКА.read_text()); 나무들[ПАТЕКА] = 나무
        for внес_VALUE in ast.walk(나무):
            if isinstance(внес_VALUE, ast.FunctionDef):
                параметар_табела.setdefault(внес_VALUE.name, set()).update(параметар_аргумент.arg for параметар_аргумент in внес_VALUE.args.args + внес_VALUE.args.kwonlyargs)
                if внес_VALUE.args.kwarg: 가변매개함수.add(внес_VALUE.name)
            if isinstance(внес_VALUE, ast.ClassDef):
                for ФУНКЦИЈА_VALUE in внес_VALUE.body:
                    if isinstance(ФУНКЦИЈА_VALUE, ast.FunctionDef) and ФУНКЦИЈА_VALUE.name == '__init__':
                        параметар_табела.setdefault(внес_VALUE.name, set()).update(параметар_аргумент.arg for параметар_аргумент in ФУНКЦИЈА_VALUE.args.args + ФУНКЦИЈА_VALUE.args.kwonlyargs)
            Име = ''
            if isinstance(внес_VALUE, (ast.FunctionDef, ast.ClassDef)): Име = внес_VALUE.name
            elif isinstance(внес_VALUE, ast.Name) and isinstance(внес_VALUE.ctx, ast.Store): Име = внес_VALUE.id
            elif isinstance(внес_VALUE, ast.arg): Име = внес_VALUE.arg
            if Име and Име not in задача_VALUE_102996da and all(ord(знак_VALUE)<128 for знак_VALUE in Име):
                실패들.append('{}:{}: {}'.format(ПАТЕКА.relative_to(склад_корен), внес_VALUE.lineno, Име))
    for ПАТЕКА, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Име = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Име not in параметар_табела or Име in 가변매개함수 or not any(ord(знак_VALUE)>127 for знак_VALUE in Име): continue
            for параметар_аргумент in 호출.keywords:
                if параметар_аргумент.arg and параметар_аргумент.arg not in параметар_табела[Име]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(ПАТЕКА.relative_to(склад_корен), 호출.lineno, Име, параметар_аргумент.arg))
    for ред in (Project_корен/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, Процес_VALUE_внес = ред.split('\t')
        if not (Project_корен/현재).is_file(): 실패들.append('премести_VALUE Датотека 없음: '+현재)
        if Процес_VALUE_внес == '호환진입점유지' and not (Project_корен/이전).is_file(): 실패들.append('호환 внес_поен 없음: '+이전)
    예제 = (Project_корен.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for ПАТЕКА in sorted((Project_корен.parents[1]/'example/java').glob('*.java')):
        ИЗВОР = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ПАТЕКА.read_text())
        for Име in re.findall(r'\b[^\W\d]\w*\b', ИЗВОР, re.UNICODE):
            if Име not in 예약어 and all(ord(знак_VALUE)<128 for знак_VALUE in Име):
                실패들.append('{}: 예제의 영어 идентификатор_VALUE {}'.format(ПАТЕКА.name, Име))
    for Име in ('창', 'копче', 'Ознака', 'СМС_поле', '화면구성요소', 'настан_ред_на_чекање', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        ИЗВОР = (Project_корен/'한국어자바/Македонски/자체'/(Име+'.java')).read_text()
        ИЗВОР = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', ИЗВОР)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', ИЗВОР):
            실패들.append(Име+': Македонски 직접 구현에 표준 објект_VALUE 래퍼가 남았습니다.')
    시언어예제 = (Project_корен.parents[1]/'example/c/네트워크예제.c').read_text()
    for Име in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Име in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Име: '+Име)
    파이썬예제 = (Project_корен.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 исклучок 직접 사용')
    머리 = (Project_корен.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Име in ('облак_семејни', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+Име+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 макро_VALUE 사용: '+Име)
    자바파일수 = 0
    for корен_VALUE in ('ИЗВОР', 'корисник/자바', '한국어자바'):
        for ПАТЕКА in (Project_корен/корен_VALUE).rglob('*.java'):
            자바파일수 += 1
            ИЗВОР = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ПАТЕКА.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', ИЗВОР):
                실패들.append('{}: 한국어화되지 않은 декларација {}'.format(ПАТЕКА.relative_to(Project_корен), 맞음[1]))
            if корен_VALUE == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', ИЗВОР):
                실패들.append('{}: 공개 исклучок декларација'.format(ПАТЕКА.relative_to(Project_корен)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for ПАТЕКА in sorted((склад_корен/'os/ИЗВОР').glob('*.java')):
        x86자바파일수 += 1
        ИЗВОР = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ПАТЕКА.read_text())
        for Име in re.findall(r'\b[^\W\d]\w*\b', ИЗВОР, re.UNICODE):
            if Име not in 예약어 | 표준자바이름 and all(ord(знак_VALUE)<128 for знак_VALUE in Име):
                실패들.append('{}: 자체 영어 идентификатор_VALUE {}'.format(ПАТЕКА.relative_to(склад_корен), Име))
    LOG_ред = {'passed': False, 'python_files': датотека_COUNT, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if Аргументи.시언어:
        subprocess.check_call(['python3', str(Project_корен/'Алатки/시언어이름분석.py')])
        분석 = json.loads((Project_корен/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(ГРЕШКА) for ГРЕШКА in 분석['ГРЕШКА'])
        공개규약 = set(json.loads((Project_корен/'명명/규격이름.json').read_text()))
        for внес_VALUE in 분석['декларација'].values():
            Име = внес_VALUE['Име']; ПАТЕКА = Path(внес_VALUE['Датотека'])
            ИЗВОР = ПАТЕКА.read_bytes()
            # Македонски 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if ИЗВОР[внес_VALUE['OFFSET_VALUE']:внес_VALUE['OFFSET_VALUE']+len(Име)] == Име.encode() and Име not in 공개규약:
                실패들.append('{}:{}: {}'.format(ПАТЕКА.relative_to(Project_корен), внес_VALUE['줄'], Име))
        LOG_ред['c_semantic_checked'] = True
        LOG_ред['c_source_sha256'] = {str(Path(Датотека).relative_to(Project_корен)):хаш_датотека for Датотека,хаш_датотека in 분석['원문해시'].items()}
    LOG_ред['passed'] = not 실패들; LOG_ред['failures'] = 실패들
    одредиште_VALUE = Project_корен/'build/verification/naming'; одредиште_VALUE.mkdir(parents=True, exist_ok=True)
    (одредиште_VALUE/'report.json').write_text(json.dumps(LOG_ред, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: Македонски декларација·Датотека ПАТЕКА·호환 внес_поен·통신 예제')

if __name__ == '__main__': Изврши_2()
