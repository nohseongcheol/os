#!/usr/bin/env python3
"""명명 клип·예외·경로를 검사한다. --시언어는 libclang 선언 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def Жүргүзүү():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--시언어', action='store_true')
    인수 = 해석기.parse_args()
    실패들 = []
    иш_маани = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    매개변수표 = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for ЖОЛ in list((기준/'Куралдар').glob('*.py')) + list((기준/'예제').rglob('*.py')) + 공용번역기들:
        if ЖОЛ.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(ЖОЛ.read_text()); 나무들[ЖОЛ] = 나무
        for киргизме_жазуу_маани in ast.walk(나무):
            if isinstance(киргизме_жазуу_маани, ast.FunctionDef):
                매개변수표.setdefault(киргизме_жазуу_маани.name, set()).update(인자.arg for 인자 in киргизме_жазуу_маани.args.args + киргизме_жазуу_маани.args.kwonlyargs)
                if киргизме_жазуу_маани.args.kwarg: 가변매개함수.add(киргизме_жазуу_маани.name)
            if isinstance(киргизме_жазуу_маани, ast.ClassDef):
                for функция_маани in киргизме_жазуу_маани.body:
                    if isinstance(функция_маани, ast.FunctionDef) and функция_маани.name == '__init__':
                        매개변수표.setdefault(киргизме_жазуу_маани.name, set()).update(인자.arg for 인자 in функция_маани.args.args + функция_маани.args.kwonlyargs)
            Аты = ''
            if isinstance(киргизме_жазуу_маани, (ast.FunctionDef, ast.ClassDef)): Аты = киргизме_жазуу_маани.name
            elif isinstance(киргизме_жазуу_маани, ast.Name) and isinstance(киргизме_жазуу_маани.ctx, ast.Store): Аты = киргизме_жазуу_маани.id
            elif isinstance(киргизме_жазуу_маани, ast.arg): Аты = киргизме_жазуу_маани.arg
            if Аты and Аты not in иш_маани and all(ord(символ_маани_068c2631)<128 for символ_маани_068c2631 in Аты):
                실패들.append('{}:{}: {}'.format(ЖОЛ.relative_to(저장소), киргизме_жазуу_маани.lineno, Аты))
    for ЖОЛ, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Аты = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Аты not in 매개변수표 or Аты in 가변매개함수 or not any(ord(символ_маани_068c2631)>127 for символ_маани_068c2631 in Аты): continue
            for 인자 in 호출.keywords:
                if 인자.arg and 인자.arg not in 매개변수표[Аты]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(ЖОЛ.relative_to(저장소), 호출.lineno, Аты, 인자.arg))
    for сап in (기준/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, Процесс_маани_киргизме_жазуу = сап.split('\t')
        if not (기준/현재).is_file(): 실패들.append('жылдыруу_маани Файл 없음: '+현재)
        if Процесс_маани_киргизме_жазуу == '호환진입점유지' and not (기준/이전).is_file(): 실패들.append('호환 киргизме_жазуу_упай 없음: '+이전)
    예제 = (기준.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for ЖОЛ in sorted((기준.parents[1]/'example/java').glob('*.java')):
        Булак = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ЖОЛ.read_text())
        for Аты in re.findall(r'\b[^\W\d]\w*\b', Булак, re.UNICODE):
            if Аты not in 예약어 and all(ord(символ_маани_068c2631)<128 for символ_маани_068c2631 in Аты):
                실패들.append('{}: 예제의 영어 аныктагыч_маани {}'.format(ЖОЛ.name, Аты))
    for Аты in ('창', 'баскыч', 'метка', 'текст_талаасы', '화면구성요소', 'окуя_кезек', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        Булак = (기준/'한국어자바/한국어/자체'/(Аты+'.java')).read_text()
        Булак = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', Булак)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', Булак):
            실패들.append(Аты+': 한국어 직접 구현에 표준 объект_маани 래퍼가 남았습니다.')
    시언어예제 = (기준.parents[1]/'example/c/네트워크예제.c').read_text()
    for Аты in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Аты in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Аты: '+Аты)
    파이썬예제 = (기준.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 예외 직접 사용')
    머리 = (기준.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Аты in ('Интернет_Үй_бүлө', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+Аты+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 макро_маани 사용: '+Аты)
    자바파일수 = 0
    for 뿌리 in ('Булак', 'колдонуучу/자바', '한국어자바'):
        for ЖОЛ in (기준/뿌리).rglob('*.java'):
            자바파일수 += 1
            Булак = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ЖОЛ.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', Булак):
                실패들.append('{}: 한국어화되지 않은 선언 {}'.format(ЖОЛ.relative_to(기준), 맞음[1]))
            if 뿌리 == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', Булак):
                실패들.append('{}: 공개 예외 선언'.format(ЖОЛ.relative_to(기준)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for ЖОЛ in sorted((저장소/'os/Булак').glob('*.java')):
        x86자바파일수 += 1
        Булак = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ЖОЛ.read_text())
        for Аты in re.findall(r'\b[^\W\d]\w*\b', Булак, re.UNICODE):
            if Аты not in 예약어 | 표준자바이름 and all(ord(символ_маани_068c2631)<128 for символ_маани_068c2631 in Аты):
                실패들.append('{}: 자체 영어 аныктагыч_маани {}'.format(ЖОЛ.relative_to(저장소), Аты))
    жазуу_катар = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(기준/'Куралдар/시언어이름분석.py')])
        분석 = json.loads((기준/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(Ката) for Ката in 분석['Ката'])
        공개규약 = set(json.loads((기준/'명명/규격이름.json').read_text()))
        for киргизме_жазуу_маани in 분석['선언'].values():
            Аты = киргизме_жазуу_маани['Аты']; ЖОЛ = Path(киргизме_жазуу_маани['Файл'])
            Булак = ЖОЛ.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if Булак[киргизме_жазуу_маани['Жылбышуу_маани']:киргизме_жазуу_маани['Жылбышуу_маани']+len(Аты)] == Аты.encode() and Аты not in 공개규약:
                실패들.append('{}:{}: {}'.format(ЖОЛ.relative_to(기준), киргизме_жазуу_маани['줄'], Аты))
        жазуу_катар['c_semantic_checked'] = True
        жазуу_катар['c_source_sha256'] = {str(Path(Файл).relative_to(기준)):хэш_файл for Файл,хэш_файл in 분석['원문해시'].items()}
    жазуу_катар['passed'] = not 실패들; жазуу_катар['failures'] = 실패들
    көздөө_жайы_маани = 기준/'build/verification/naming'; көздөө_жайы_маани.mkdir(parents=True, exist_ok=True)
    (көздөө_жайы_маани/'report.json').write_text(json.dumps(жазуу_катар, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 선언·Файл ЖОЛ·호환 киргизме_жазуу_упай·통신 예제')

if __name__ == '__main__': Жүргүзүү()
