#!/usr/bin/env python3
"""명명 кліп·выключэнне·경로를 검사한다. --시언어는 libclang абвяшчэнне 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]

def Выканаць():
    аналізатар_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    аналізатар_48ee4b1b.add_argument('--시언어', action='store_true')
    인수 = аналізатар_48ee4b1b.parse_args()
    실패들 = []
    зварот_значэнне = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    параметр_табліца = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for ШЛЯХ in list((기준/'Інструменты').glob('*.py')) + list((기준/'예제').rglob('*.py')) + 공용번역기들:
        if ШЛЯХ.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(ШЛЯХ.read_text()); 나무들[ШЛЯХ] = 나무
        for увядзенне_значэнне in ast.walk(나무):
            if isinstance(увядзенне_значэнне, ast.FunctionDef):
                параметр_табліца.setdefault(увядзенне_значэнне.name, set()).update(параметр_аргумент.arg for параметр_аргумент in увядзенне_значэнне.args.args + увядзенне_значэнне.args.kwonlyargs)
                if увядзенне_значэнне.args.kwarg: 가변매개함수.add(увядзенне_значэнне.name)
            if isinstance(увядзенне_значэнне, ast.ClassDef):
                for функцыя_значэнне in увядзенне_значэнне.body:
                    if isinstance(функцыя_значэнне, ast.FunctionDef) and функцыя_значэнне.name == '__init__':
                        параметр_табліца.setdefault(увядзенне_значэнне.name, set()).update(параметр_аргумент.arg for параметр_аргумент in функцыя_значэнне.args.args + функцыя_значэнне.args.kwonlyargs)
            Назва = ''
            if isinstance(увядзенне_значэнне, (ast.FunctionDef, ast.ClassDef)): Назва = увядзенне_значэнне.name
            elif isinstance(увядзенне_значэнне, ast.Name) and isinstance(увядзенне_значэнне.ctx, ast.Store): Назва = увядзенне_значэнне.id
            elif isinstance(увядзенне_значэнне, ast.arg): Назва = увядзенне_значэнне.arg
            if Назва and Назва not in зварот_значэнне and all(ord(сімвал_значэнне_068c2631)<128 for сімвал_значэнне_068c2631 in Назва):
                실패들.append('{}:{}: {}'.format(ШЛЯХ.relative_to(저장소), увядзенне_значэнне.lineno, Назва))
    for ШЛЯХ, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Назва = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Назва not in параметр_табліца or Назва in 가변매개함수 or not any(ord(сімвал_значэнне_068c2631)>127 for сімвал_значэнне_068c2631 in Назва): continue
            for параметр_аргумент in 호출.keywords:
                if параметр_аргумент.arg and параметр_аргумент.arg not in параметр_табліца[Назва]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(ШЛЯХ.relative_to(저장소), 호출.lineno, Назва, параметр_аргумент.arg))
    for лінія in (기준/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, Працэс_значэнне_увядзенне = лінія.split('\t')
        if not (기준/현재).is_file(): 실패들.append('перамясціць_значэнне Файл 없음: '+현재)
        if Працэс_значэнне_увядзенне == '호환진입점유지' and not (기준/이전).is_file(): 실패들.append('호환 увядзенне_бал 없음: '+이전)
    예제 = (기준.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for ШЛЯХ in sorted((기준.parents[1]/'example/java').glob('*.java')):
        КРЫНІЦА = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ШЛЯХ.read_text())
        for Назва in re.findall(r'\b[^\W\d]\w*\b', КРЫНІЦА, re.UNICODE):
            if Назва not in 예약어 and all(ord(сімвал_значэнне_068c2631)<128 for сімвал_значэнне_068c2631 in Назва):
                실패들.append('{}: 예제의 영어 ідэнтыфікатар_значэнне {}'.format(ШЛЯХ.name, Назва))
    for Назва in ('창', 'кнопка', 'Адмеціна', 'Тэкст_поле', '화면구성요소', 'падзея_чарга', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        КРЫНІЦА = (기준/'한국어자바/한국어/자체'/(Назва+'.java')).read_text()
        КРЫНІЦА = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', КРЫНІЦА)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', КРЫНІЦА):
            실패들.append(Назва+': 한국어 직접 구현에 표준 аб_ект_значэнне 래퍼가 남았습니다.')
    시언어예제 = (기준.parents[1]/'example/c/네트워크예제.c').read_text()
    for Назва in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Назва in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Назва: '+Назва)
    파이썬예제 = (기준.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 выключэнне 직접 사용')
    머리 = (기준.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Назва in ('воблака_Сям_я', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', '통신종단점만들기', '자료전문보내기'):
        if re.search(r'^#define\s+'+Назва+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 макрас_значэнне 사용: '+Назва)
    자바파일수 = 0
    for 뿌리 in ('КРЫНІЦА', 'карыстальнік/자바', '한국어자바'):
        for ШЛЯХ in (기준/뿌리).rglob('*.java'):
            자바파일수 += 1
            КРЫНІЦА = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ШЛЯХ.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', КРЫНІЦА):
                실패들.append('{}: 한국어화되지 않은 абвяшчэнне {}'.format(ШЛЯХ.relative_to(기준), 맞음[1]))
            if 뿌리 == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', КРЫНІЦА):
                실패들.append('{}: 공개 выключэнне абвяшчэнне'.format(ШЛЯХ.relative_to(기준)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for ШЛЯХ in sorted((저장소/'os/КРЫНІЦА').glob('*.java')):
        x86자바파일수 += 1
        КРЫНІЦА = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ШЛЯХ.read_text())
        for Назва in re.findall(r'\b[^\W\d]\w*\b', КРЫНІЦА, re.UNICODE):
            if Назва not in 예약어 | 표준자바이름 and all(ord(сімвал_значэнне_068c2631)<128 for сімвал_значэнне_068c2631 in Назва):
                실패들.append('{}: 자체 영어 ідэнтыфікатар_значэнне {}'.format(ШЛЯХ.relative_to(저장소), Назва))
    журнал_запіс = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.시언어:
        subprocess.check_call(['python3', str(기준/'Інструменты/시언어이름분석.py')])
        분석 = json.loads((기준/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(ПАМЫЛКА) for ПАМЫЛКА in 분석['ПАМЫЛКА'])
        공개규약 = set(json.loads((기준/'명명/규격이름.json').read_text()))
        for увядзенне_значэнне in 분석['абвяшчэнне'].values():
            Назва = увядзенне_значэнне['Назва']; ШЛЯХ = Path(увядзенне_значэнне['Файл'])
            КРЫНІЦА = ШЛЯХ.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if КРЫНІЦА[увядзенне_значэнне['Зрух_значэнне']:увядзенне_значэнне['Зрух_значэнне']+len(Назва)] == Назва.encode() and Назва not in 공개규약:
                실패들.append('{}:{}: {}'.format(ШЛЯХ.relative_to(기준), увядзенне_значэнне['줄'], Назва))
        журнал_запіс['c_semantic_checked'] = True
        журнал_запіс['c_source_sha256'] = {str(Path(Файл).relative_to(기준)):хэш_файл for Файл,хэш_файл in 분석['원문해시'].items()}
    журнал_запіс['passed'] = not 실패들; журнал_запіс['failures'] = 실패들
    прызначэнне_значэнне_a0fbc067 = 기준/'build/verification/naming'; прызначэнне_значэнне_a0fbc067.mkdir(parents=True, exist_ok=True)
    (прызначэнне_значэнне_a0fbc067/'report.json').write_text(json.dumps(журнал_запіс, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 абвяшчэнне·Файл ШЛЯХ·호환 увядзенне_бал·통신 예제')

if __name__ == '__main__': Выканаць()
