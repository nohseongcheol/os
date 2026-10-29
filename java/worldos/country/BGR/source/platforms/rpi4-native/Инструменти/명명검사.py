#!/usr/bin/env python3
"""명명 клип·изключение·경로를 검사한다. --시언어는 libclang декларация 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

проект_корен = Path(__file__).resolve().parents[1]
хранилище_корен = проект_корен.parents[1]

def Стартиране():
    анализатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    анализатор_48ee4b1b.add_argument('--시언어', action='store_true')
    Параметри = анализатор_48ee4b1b.parse_args()
    실패들 = []
    случай_стойност = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    параметър_таблица = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [хранилище_корен/'compiler/компилатор.py', хранилище_корен/'compiler/기계어미리번역.py']
    for ПЪТ in list((проект_корен/'Инструменти').glob('*.py')) + list((проект_корен/'예제').rglob('*.py')) + 공용번역기들:
        if ПЪТ.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(ПЪТ.read_text()); 나무들[ПЪТ] = 나무
        for запис_стойност in ast.walk(나무):
            if isinstance(запис_стойност, ast.FunctionDef):
                параметър_таблица.setdefault(запис_стойност.name, set()).update(параметър_аргумент.arg for параметър_аргумент in запис_стойност.args.args + запис_стойност.args.kwonlyargs)
                if запис_стойност.args.kwarg: 가변매개함수.add(запис_стойност.name)
            if isinstance(запис_стойност, ast.ClassDef):
                for функция_стойност in запис_стойност.body:
                    if isinstance(функция_стойност, ast.FunctionDef) and функция_стойност.name == '__init__':
                        параметър_таблица.setdefault(запис_стойност.name, set()).update(параметър_аргумент.arg for параметър_аргумент in функция_стойност.args.args + функция_стойност.args.kwonlyargs)
            Име = ''
            if isinstance(запис_стойност, (ast.FunctionDef, ast.ClassDef)): Име = запис_стойност.name
            elif isinstance(запис_стойност, ast.Name) and isinstance(запис_стойност.ctx, ast.Store): Име = запис_стойност.id
            elif isinstance(запис_стойност, ast.arg): Име = запис_стойност.arg
            if Име and Име not in случай_стойност and all(ord(знак_стойност)<128 for знак_стойност in Име):
                실패들.append('{}:{}: {}'.format(ПЪТ.relative_to(хранилище_корен), запис_стойност.lineno, Име))
    for ПЪТ, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Име = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Име not in параметър_таблица or Име in 가변매개함수 or not any(ord(знак_стойност)>127 for знак_стойност in Име): continue
            for параметър_аргумент in 호출.keywords:
                if параметър_аргумент.arg and параметър_аргумент.arg not in параметър_таблица[Име]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(ПЪТ.relative_to(хранилище_корен), 호출.lineno, Име, параметър_аргумент.arg))
    for ред in (проект_корен/'명명/име_на_файл_съпоставяне.tsv').read_text().splitlines()[1:]:
        이전, в_срок_артикул, Процес_стойност_запис = ред.split('\t')
        if not (проект_корен/в_срок_артикул).is_file(): 실패들.append('движа_се_стойност Файл 없음: '+в_срок_артикул)
        if Процес_стойност_запис == '호환진입점유지' and not (проект_корен/이전).is_file(): 실패들.append('호환 запис_пункт 없음: '+이전)
    예제 = (проект_корен.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for ПЪТ in sorted((проект_корен.parents[1]/'example/java').glob('*.java')):
        ИЗТОЧНИК = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ПЪТ.read_text())
        for Име in re.findall(r'\b[^\W\d]\w*\b', ИЗТОЧНИК, re.UNICODE):
            if Име not in 예약어 and all(ord(знак_стойност)<128 for знак_стойност in Име):
                실패들.append('{}: 예제의 영어 Идентификатор_стойност {}'.format(ПЪТ.name, Име))
    for Име in ('Прозорец', 'бутон', 'Етикет', 'текстово_поле', '화면구성요소', 'събитие_опашка', '작업가닥', '실행할일', '동작받이', 'проект_предупреждение', '작업'):
        ИЗТОЧНИК = (проект_корен/'한국어자바/Български/자체'/(Име+'.java')).read_text()
        ИЗТОЧНИК = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', ИЗТОЧНИК)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', ИЗТОЧНИК):
            실패들.append(Име+': Български 직접 구현에 표준 обект_стойност 래퍼가 남았습니다.')
    시언어예제 = (проект_корен.parents[1]/'example/c/네트워크예제.c').read_text()
    for Име in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Име in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Име: '+Име)
    파이썬예제 = (проект_корен.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 изключение 직접 използвам_стойност')
    머리 = (проект_корен.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Име in ('облак_семейни', 'дейтаграмно_гнездо', 'дейтаграма_протокол', '통신주소', '인터넷통신주소', 'Създаване_участник', 'изпращам_дейтаграма_данни'):
        if re.search(r'^#define\s+'+Име+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 макрос_стойност използвам_стойност: '+Име)
    자바파일수 = 0
    for корен_стойност in ('ИЗТОЧНИК', 'потребител/자바', '한국어자바'):
        for ПЪТ in (проект_корен/корен_стойност).rglob('*.java'):
            자바파일수 += 1
            ИЗТОЧНИК = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ПЪТ.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', ИЗТОЧНИК):
                실패들.append('{}: 한국어화되지 않은 декларация {}'.format(ПЪТ.relative_to(проект_корен), 맞음[1]))
            if корен_стойност == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', ИЗТОЧНИК):
                실패들.append('{}: 공개 изключение декларация'.format(ПЪТ.relative_to(проект_корен)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for ПЪТ in sorted((хранилище_корен/'os/ИЗТОЧНИК').glob('*.java')):
        x86자바파일수 += 1
        ИЗТОЧНИК = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ПЪТ.read_text())
        for Име in re.findall(r'\b[^\W\d]\w*\b', ИЗТОЧНИК, re.UNICODE):
            if Име not in 예약어 | 표준자바이름 and all(ord(знак_стойност)<128 for знак_стойност in Име):
                실패들.append('{}: 자체 영어 Идентификатор_стойност {}'.format(ПЪТ.relative_to(хранилище_корен), Име))
    регистрирам_запис = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if Параметри.시언어:
        subprocess.check_call(['python3', str(проект_корен/'Инструменти/시언어이름분석.py')])
        Анализ_стойност = json.loads((проект_корен/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(ГРЕШКА) for ГРЕШКА in Анализ_стойност['ГРЕШКА'])
        공개규약 = set(json.loads((проект_корен/'명명/규격이름.json').read_text()))
        for запис_стойност in Анализ_стойност['декларация'].values():
            Име = запис_стойност['Име']; ПЪТ = Path(запис_стойност['Файл'])
            ИЗТОЧНИК = ПЪТ.read_bytes()
            # Български 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if ИЗТОЧНИК[запис_стойност['Изместване_стойност']:запис_стойност['Изместване_стойност']+len(Име)] == Име.encode() and Име not in 공개규약:
                실패들.append('{}:{}: {}'.format(ПЪТ.relative_to(проект_корен), запис_стойност['줄'], Име))
        регистрирам_запис['c_semantic_checked'] = True
        регистрирам_запис['c_source_sha256'] = {str(Path(Файл).relative_to(проект_корен)):хеширане_Файл for Файл,хеширане_Файл in Анализ_стойност['원문해시'].items()}
    регистрирам_запис['passed'] = not 실패들; регистрирам_запис['failures'] = 실패들
    местоназначение_стойност = проект_корен/'build/verification/naming'; местоназначение_стойност.mkdir(parents=True, exist_ok=True)
    (местоназначение_стойност/'report.json').write_text(json.dumps(регистрирам_запис, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: Български декларация·Файл ПЪТ·호환 запис_пункт·통신 예제')

if __name__ == '__main__': Стартиране()
