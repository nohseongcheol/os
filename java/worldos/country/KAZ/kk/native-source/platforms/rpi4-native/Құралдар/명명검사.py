#!/usr/bin/env python3
"""명명 клип·ерекшелік·경로를 검사한다. --시언어는 libclang мәлімдеме 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

жоба_түбір = Path(__file__).resolve().parents[1]
репозиторий_түбір = жоба_түбір.parents[1]

def Орындау_2():
    талдау_құралы_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    талдау_құралы_48ee4b1b.add_argument('--시언어', action='store_true')
    Аргументтер = талдау_құралы_48ee4b1b.parse_args()
    실패들 = []
    іс_мән = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    параметр_кесте = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [репозиторий_түбір/'compiler/컴파일러.py', репозиторий_түбір/'compiler/기계어미리번역.py']
    for Жол_2 in list((жоба_түбір/'Құралдар').glob('*.py')) + list((жоба_түбір/'예제').rglob('*.py')) + 공용번역기들:
        if Жол_2.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(Жол_2.read_text()); 나무들[Жол_2] = 나무
        for енгізу_мән in ast.walk(나무):
            if isinstance(енгізу_мән, ast.FunctionDef):
                параметр_кесте.setdefault(енгізу_мән.name, set()).update(параметр_аргумент.arg for параметр_аргумент in енгізу_мән.args.args + енгізу_мән.args.kwonlyargs)
                if енгізу_мән.args.kwarg: 가변매개함수.add(енгізу_мән.name)
            if isinstance(енгізу_мән, ast.ClassDef):
                for функция_мән in енгізу_мән.body:
                    if isinstance(функция_мән, ast.FunctionDef) and функция_мән.name == '__init__':
                        параметр_кесте.setdefault(енгізу_мән.name, set()).update(параметр_аргумент.arg for параметр_аргумент in функция_мән.args.args + функция_мән.args.kwonlyargs)
            Аты = ''
            if isinstance(енгізу_мән, (ast.FunctionDef, ast.ClassDef)): Аты = енгізу_мән.name
            elif isinstance(енгізу_мән, ast.Name) and isinstance(енгізу_мән.ctx, ast.Store): Аты = енгізу_мән.id
            elif isinstance(енгізу_мән, ast.arg): Аты = енгізу_мән.arg
            if Аты and Аты not in іс_мән and all(ord(таңба_мән)<128 for таңба_мән in Аты):
                실패들.append('{}:{}: {}'.format(Жол_2.relative_to(репозиторий_түбір), енгізу_мән.lineno, Аты))
    for Жол_2, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Аты = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Аты not in параметр_кесте or Аты in 가변매개함수 or not any(ord(таңба_мән)>127 for таңба_мән in Аты): continue
            for параметр_аргумент in 호출.keywords:
                if параметр_аргумент.arg and параметр_аргумент.arg not in параметр_кесте[Аты]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(Жол_2.relative_to(репозиторий_түбір), 호출.lineno, Аты, параметр_аргумент.arg))
    for Жол in (жоба_түбір/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, ток_элемент, Процесс_мән_енгізу = Жол.split('\t')
        if not (жоба_түбір/ток_элемент).is_file(): 실패들.append('жылжыту_мән Файл 없음: '+ток_элемент)
        if Процесс_мән_енгізу == '호환진입점유지' and not (жоба_түбір/이전).is_file(): 실패들.append('호환 енгізу_ұпай 없음: '+이전)
    예제 = (жоба_түбір.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for Жол_2 in sorted((жоба_түбір.parents[1]/'example/java').glob('*.java')):
        Неден = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Жол_2.read_text())
        for Аты in re.findall(r'\b[^\W\d]\w*\b', Неден, re.UNICODE):
            if Аты not in 예약어 and all(ord(таңба_мән)<128 for таңба_мән in Аты):
                실패들.append('{}: 예제의 영어 идентификатор_мән {}'.format(Жол_2.name, Аты))
    for Аты in ('Терезе', 'батырма', 'Белгі', 'мәтіндік_өріс', '화면구성요소', 'оқиға_кезек', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        Неден = (жоба_түбір/'한국어자바/한국어/자체'/(Аты+'.java')).read_text()
        Неден = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', Неден)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', Неден):
            실패들.append(Аты+': 한국어 직접 구현에 표준 нысан_мән 래퍼가 남았습니다.')
    시언어예제 = (жоба_түбір.parents[1]/'example/c/네트워크예제.c').read_text()
    for Аты in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Аты in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Аты: '+Аты)
    파이썬예제 = (жоба_түбір.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 ерекшелік 직접 사용')
    머리 = (жоба_түбір.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Аты in ('бұлт_топ', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', 'жасау_қатысушы', '자료전문보내기'):
        if re.search(r'^#define\s+'+Аты+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 макрос_мән 사용: '+Аты)
    자바파일수 = 0
    for түбір_мән in ('Неден', 'пайдаланушы/자바', '한국어자바'):
        for Жол_2 in (жоба_түбір/түбір_мән).rglob('*.java'):
            자바파일수 += 1
            Неден = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Жол_2.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', Неден):
                실패들.append('{}: 한국어화되지 않은 мәлімдеме {}'.format(Жол_2.relative_to(жоба_түбір), 맞음[1]))
            if түбір_мән == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', Неден):
                실패들.append('{}: 공개 ерекшелік мәлімдеме'.format(Жол_2.relative_to(жоба_түбір)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for Жол_2 in sorted((репозиторий_түбір/'os/Неден').glob('*.java')):
        x86자바파일수 += 1
        Неден = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Жол_2.read_text())
        for Аты in re.findall(r'\b[^\W\d]\w*\b', Неден, re.UNICODE):
            if Аты not in 예약어 | 표준자바이름 and all(ord(таңба_мән)<128 for таңба_мән in Аты):
                실패들.append('{}: 자체 영어 идентификатор_мән {}'.format(Жол_2.relative_to(репозиторий_түбір), Аты))
    журнал_жол = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if Аргументтер.시언어:
        subprocess.check_call(['python3', str(жоба_түбір/'Құралдар/시언어이름분석.py')])
        Талдау_мән = json.loads((жоба_түбір/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(Қате) for Қате in Талдау_мән['Қате'])
        공개규약 = set(json.loads((жоба_түбір/'명명/규격이름.json').read_text()))
        for енгізу_мән in Талдау_мән['мәлімдеме'].values():
            Аты = енгізу_мән['Аты']; Жол_2 = Path(енгізу_мән['Файл'])
            Неден = Жол_2.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if Неден[енгізу_мән['жылжыту_мән_450fc799']:енгізу_мән['жылжыту_мән_450fc799']+len(Аты)] == Аты.encode() and Аты not in 공개규약:
                실패들.append('{}:{}: {}'.format(Жол_2.relative_to(жоба_түбір), енгізу_мән['Жол'], Аты))
        журнал_жол['c_semantic_checked'] = True
        журнал_жол['c_source_sha256'] = {str(Path(Файл).relative_to(жоба_түбір)):хэш_файл for Файл,хэш_файл in Талдау_мән['원문해시'].items()}
    журнал_жол['passed'] = not 실패들; журнал_жол['failures'] = 실패들
    тағайындау_мән = жоба_түбір/'build/verification/naming'; тағайындау_мән.mkdir(parents=True, exist_ok=True)
    (тағайындау_мән/'report.json').write_text(json.dumps(журнал_жол, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 мәлімдеме·Файл Жол_2·호환 енгізу_ұпай·통신 예제')

if __name__ == '__main__': Орындау_2()
