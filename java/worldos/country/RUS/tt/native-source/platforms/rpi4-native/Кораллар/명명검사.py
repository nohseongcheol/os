#!/usr/bin/env python3
"""명명 клип·예외·경로를 검사한다. --시언어는 libclang 선언 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

экранга_җибәрү_тамыр = Path(__file__).resolve().parents[1]
저장소 = экранга_җибәрү_тамыр.parents[1]

def эшләтү():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--시언어', action='store_true')
    인수 = 해석기.parse_args()
    실패들 = []
    бирем_VALUE_102996da = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    файл_COUNT = 0
    매개변수표 = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for Yul in list((экранга_җибәрү_тамыр/'Кораллар').glob('*.py')) + list((экранга_җибәрү_тамыр/'예제').rglob('*.py')) + 공용번역기들:
        if Yul.name.endswith(('이름반영.py', '이름분석.py')): continue
        файл_COUNT += 1
        나무 = ast.parse(Yul.read_text()); 나무들[Yul] = 나무
        for кертү_VALUE in ast.walk(나무):
            if isinstance(кертү_VALUE, ast.FunctionDef):
                매개변수표.setdefault(кертү_VALUE.name, set()).update(인자.arg for 인자 in кертү_VALUE.args.args + кертү_VALUE.args.kwonlyargs)
                if кертү_VALUE.args.kwarg: 가변매개함수.add(кертү_VALUE.name)
            if isinstance(кертү_VALUE, ast.ClassDef):
                for ФУНКЦИЯ_VALUE in кертү_VALUE.body:
                    if isinstance(ФУНКЦИЯ_VALUE, ast.FunctionDef) and ФУНКЦИЯ_VALUE.name == '__init__':
                        매개변수표.setdefault(кертү_VALUE.name, set()).update(인자.arg for 인자 in ФУНКЦИЯ_VALUE.args.args + ФУНКЦИЯ_VALUE.args.kwonlyargs)
            исем = ''
            if isinstance(кертү_VALUE, (ast.FunctionDef, ast.ClassDef)): исем = кертү_VALUE.name
            elif isinstance(кертү_VALUE, ast.Name) and isinstance(кертү_VALUE.ctx, ast.Store): исем = кертү_VALUE.id
            elif isinstance(кертү_VALUE, ast.arg): исем = кертү_VALUE.arg
            if исем and исем not in бирем_VALUE_102996da and all(ord(символ_VALUE_068c2631)<128 for символ_VALUE_068c2631 in исем):
                실패들.append('{}:{}: {}'.format(Yul.relative_to(저장소), кертү_VALUE.lineno, исем))
    for Yul, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            исем = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if исем not in 매개변수표 or исем in 가변매개함수 or not any(ord(символ_VALUE_068c2631)>127 for символ_VALUE_068c2631 in исем): continue
            for 인자 in 호출.keywords:
                if 인자.arg and 인자.arg not in 매개변수표[исем]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(Yul.relative_to(저장소), 호출.lineno, исем, 인자.arg))
    for юл in (экранга_җибәрү_тамыр/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, Процесс_VALUE_кертү = юл.split('\t')
        if not (экранга_җибәрү_тамыр/현재).is_file(): 실패들.append('күчерү_VALUE Birem 없음: '+현재)
        if Процесс_VALUE_кертү == '호환진입점유지' and not (экранга_җибәрү_тамыр/이전).is_file(): 실패들.append('호환 кертү_балл 없음: '+이전)
    예제 = (экранга_җибәрү_тамыр.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for Yul in sorted((экранга_җибәрү_тамыр.parents[1]/'example/java').glob('*.java')):
        чыганак = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Yul.read_text())
        for исем in re.findall(r'\b[^\W\d]\w*\b', чыганак, re.UNICODE):
            if исем not in 예약어 and all(ord(символ_VALUE_068c2631)<128 for символ_VALUE_068c2631 in исем):
                실패들.append('{}: 예제의 영어 күрсәткеч_VALUE {}'.format(Yul.name, исем))
    for исем in ('창', 'төймә', 'тамга', 'текст_кыры', '화면구성요소', 'вакыйга_чират', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        чыганак = (экранга_җибәрү_тамыр/'한국어자바/Татарча/자체'/(исем+'.java')).read_text()
        чыганак = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', чыганак)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', чыганак):
            실패들.append(исем+': Татарча 직접 구현에 표준 объект_VALUE 래퍼가 남았습니다.')
    시언어예제 = (экранга_җибәрү_тамыр.parents[1]/'example/c/네트워크예제.c').read_text()
    for исем in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if исем in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 исем: '+исем)
    파이썬예제 = (экранга_җибәрү_тамыр.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 예외 직접 사용')
    머리 = (экранга_җибәрү_тамыр.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for исем in ('болыт_Гаилә', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+исем+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 макрос_VALUE 사용: '+исем)
    자바파일수 = 0
    for тамыр_VALUE in ('чыганак', 'кулланучы/자바', '한국어자바'):
        for Yul in (экранга_җибәрү_тамыр/тамыр_VALUE).rglob('*.java'):
            자바파일수 += 1
            чыганак = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Yul.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', чыганак):
                실패들.append('{}: 한국어화되지 않은 선언 {}'.format(Yul.relative_to(экранга_җибәрү_тамыр), 맞음[1]))
            if тамыр_VALUE == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', чыганак):
                실패들.append('{}: 공개 예외 선언'.format(Yul.relative_to(экранга_җибәрү_тамыр)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for Yul in sorted((저장소/'os/чыганак').glob('*.java')):
        x86자바파일수 += 1
        чыганак = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Yul.read_text())
        for исем in re.findall(r'\b[^\W\d]\w*\b', чыганак, re.UNICODE):
            if исем not in 예약어 | 표준자바이름 and all(ord(символ_VALUE_068c2631)<128 for символ_VALUE_068c2631 in исем):
                실패들.append('{}: 자체 영어 күрсәткеч_VALUE {}'.format(Yul.relative_to(저장소), исем))
    LOG_юл = {'passed': False, 'python_files': файл_COUNT, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(экранга_җибәрү_тамыр/'Кораллар/시언어이름분석.py')])
        분석 = json.loads((экранга_җибәрү_тамыр/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(Хата) for Хата in 분석['Хата'])
        공개규약 = set(json.loads((экранга_җибәрү_тамыр/'명명/규격이름.json').read_text()))
        for кертү_VALUE in 분석['선언'].values():
            исем = кертү_VALUE['исем']; Yul = Path(кертү_VALUE['Birem'])
            чыганак = Yul.read_bytes()
            # Татарча 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if чыганак[кертү_VALUE['OFFSET_VALUE']:кертү_VALUE['OFFSET_VALUE']+len(исем)] == исем.encode() and исем not in 공개규약:
                실패들.append('{}:{}: {}'.format(Yul.relative_to(экранга_җибәрү_тамыр), кертү_VALUE['줄'], исем))
        LOG_юл['c_semantic_checked'] = True
        LOG_юл['c_source_sha256'] = {str(Path(Birem).relative_to(экранга_җибәрү_тамыр)):Хәш_файл for Birem,Хәш_файл in 분석['원문해시'].items()}
    LOG_юл['passed'] = not 실패들; LOG_юл['failures'] = 실패들
    күчерү_урыны_VALUE = экранга_җибәрү_тамыр/'build/verification/naming'; күчерү_урыны_VALUE.mkdir(parents=True, exist_ok=True)
    (күчерү_урыны_VALUE/'report.json').write_text(json.dumps(LOG_юл, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: Татарча 선언·Birem Yul·호환 кертү_балл·통신 예제')

if __name__ == '__main__': эшләтү()
