#!/usr/bin/env python3
"""명명 клип·исключение·경로를 검사한다. --시언어는 libclang декларация 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

задача_корень = Path(__file__).resolve().parents[1]
корень_репозитория = задача_корень.parents[1]

def запустить():
    анализатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    анализатор_48ee4b1b.add_argument('--C_Язык', action='store_true')
    аргументы = анализатор_48ee4b1b.parse_args()
    실패들 = []
    сумма_контракта = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    файл_СЧЁТ = 0
    параметр_таблица = {}
    вариадический_ФУНКЦИЯ = set()
    나무들 = {}
    공용번역기들 = [корень_репозитория/'compiler/компилятор.py', корень_репозитория/'compiler/ПредварительныйКомпилятор.py']
    for путь in list((задача_корень/'инструменты').glob('*.py')) + list((задача_корень/'예제').rglob('*.py')) + 공용번역기들:
        if путь.name.endswith(('이름반영.py', '이름분석.py')): continue
        файл_СЧЁТ += 1
        나무 = ast.parse(путь.read_text()); 나무들[путь] = 나무
        for ввод_ЗНАЧЕН in ast.walk(나무):
            if isinstance(ввод_ЗНАЧЕН, ast.FunctionDef):
                параметр_таблица.setdefault(ввод_ЗНАЧЕН.name, set()).update(параметр_аргумент.arg for параметр_аргумент in ввод_ЗНАЧЕН.args.args + ввод_ЗНАЧЕН.args.kwonlyargs)
                if ввод_ЗНАЧЕН.args.kwarg: вариадический_ФУНКЦИЯ.add(ввод_ЗНАЧЕН.name)
            if isinstance(ввод_ЗНАЧЕН, ast.ClassDef):
                for ФУНКЦИЯ_ЗНАЧЕН in ввод_ЗНАЧЕН.body:
                    if isinstance(ФУНКЦИЯ_ЗНАЧЕН, ast.FunctionDef) and ФУНКЦИЯ_ЗНАЧЕН.name == '__init__':
                        параметр_таблица.setdefault(ввод_ЗНАЧЕН.name, set()).update(параметр_аргумент.arg for параметр_аргумент in ФУНКЦИЯ_ЗНАЧЕН.args.args + ФУНКЦИЯ_ЗНАЧЕН.args.kwonlyargs)
            Название = ''
            if isinstance(ввод_ЗНАЧЕН, (ast.FunctionDef, ast.ClassDef)): Название = ввод_ЗНАЧЕН.name
            elif isinstance(ввод_ЗНАЧЕН, ast.Name) and isinstance(ввод_ЗНАЧЕН.ctx, ast.Store): Название = ввод_ЗНАЧЕН.id
            elif isinstance(ввод_ЗНАЧЕН, ast.arg): Название = ввод_ЗНАЧЕН.arg
            if Название and Название not in сумма_контракта and all(ord(знак_ЗНАЧЕН)<128 for знак_ЗНАЧЕН in Название):
                실패들.append('{}:{}: {}'.format(путь.relative_to(корень_репозитория), ввод_ЗНАЧЕН.lineno, Название))
    for путь, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Название = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Название not in параметр_таблица or Название in вариадический_ФУНКЦИЯ or not any(ord(знак_ЗНАЧЕН)>127 for знак_ЗНАЧЕН in Название): continue
            for параметр_аргумент in 호출.keywords:
                if параметр_аргумент.arg and параметр_аргумент.arg not in параметр_таблица[Название]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(путь.relative_to(корень_репозитория), 호출.lineno, Название, параметр_аргумент.arg))
    for строка_ввода in (задача_корень/'명명/имя_файла_сопоставление.tsv').read_text().splitlines()[1:]:
        Назад_товар, текущий_товар, Процесс_ЗНАЧЕН_ввод = строка_ввода.split('\t')
        if not (задача_корень/текущий_товар).is_file(): 실패들.append('переместить_ЗНАЧЕН файл 없음: '+текущий_товар)
        if Процесс_ЗНАЧЕН_ввод == '호환진입점유지' and not (задача_корень/Назад_товар).is_file(): 실패들.append('호환 точка_входа 없음: '+Назад_товар)
    예제 = (задача_корень.parents[1]/'example/java/ПримерСети.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for путь in sorted((задача_корень.parents[1]/'example/java').glob('*.java')):
        исходныйКод = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', путь.read_text())
        for Название in re.findall(r'\b[^\W\d]\w*\b', исходныйКод, re.UNICODE):
            if Название not in 예약어 and all(ord(знак_ЗНАЧЕН)<128 for знак_ЗНАЧЕН in Название):
                실패들.append('{}: 예제의 영어 идентификатор_ЗНАЧЕН {}'.format(путь.name, Название))
    for Название in ('Окно', 'кнопка', 'Метка', 'текстовое_поле', 'экран_элемент', 'Событие_Очередь', 'фоноваяЗадача', '실행할일', '동작받이', 'задача_уведомление', '작업'):
        исходныйКод = (задача_корень/'한국어자바/русский/свой'/(Название+'.java')).read_text()
        исходныйКод = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', исходныйКод)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', исходныйКод):
            실패들.append(Название+': русский 직접 구현에 표준 объект_ЗНАЧЕН 래퍼가 남았습니다.')
    시언어예제 = (задача_корень.parents[1]/'example/c/ПримерСети.c').read_text()
    for Название in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Название in 시언어예제: 실패들.append('C коммуникация 예제에 남은 표준 Название: '+Название)
    파이썬예제 = (задача_корень.parents[1]/'example/python/ПримерСети.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python коммуникация 예제에 남은 표준 исключение 직접 использовать_ЗНАЧЕН')
    HEAD_ЗНАЧЕН = (задача_корень.parents[1]/'posix-kor/arm64-native/объявления/сеть_ABI.h').read_text()
    for Название in ('облако_Семья', 'сокет_датаграмм', 'датаграмма_протокол', 'сокет_АДРЕС', 'облако_сокет_АДРЕС', 'Create_участник', 'написать_датаграмма_данные'):
        if re.search(r'^#define\s+'+Название+r'\b', HEAD_ЗНАЧЕН, re.M): 실패들.append('C 직접 реализация 대신 макрос_ЗНАЧЕН использовать_ЗНАЧЕН: '+Название)
    자바파일수 = 0
    for корень_ЗНАЧЕН in ('исходныйКод', 'пространство_пользователя/자바', '한국어자바'):
        for путь in (задача_корень/корень_ЗНАЧЕН).rglob('*.java'):
            자바파일수 += 1
            исходныйКод = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', путь.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', исходныйКод):
                실패들.append('{}: 한국어화되지 않은 декларация {}'.format(путь.relative_to(задача_корень), 맞음[1]))
            if корень_ЗНАЧЕН == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', исходныйКод):
                실패들.append('{}: 공개 исключение декларация'.format(путь.relative_to(задача_корень)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for путь in sorted((корень_репозитория/'os/исходныйКод').glob('*.java')):
        x86자바파일수 += 1
        исходныйКод = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', путь.read_text())
        for Название in re.findall(r'\b[^\W\d]\w*\b', исходныйКод, re.UNICODE):
            if Название not in 예약어 | 표준자바이름 and all(ord(знак_ЗНАЧЕН)<128 for знак_ЗНАЧЕН in Название):
                실패들.append('{}: свой 영어 идентификатор_ЗНАЧЕН {}'.format(путь.relative_to(корень_репозитория), Название))
    LOG_ЗАПИСЬ = {'passed': False, 'python_files': файл_СЧЁТ, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if аргументы.C_Язык:
        subprocess.check_call(['python3', str(задача_корень/'инструменты/시언어이름분석.py')])
        анализ_ЗНАЧЕН = json.loads((задача_корень/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(ошибка) for ошибка in анализ_ЗНАЧЕН['ошибка'])
        экспортировать_ABI = set(json.loads((задача_корень/'명명/규격이름.json').read_text()))
        for ввод_ЗНАЧЕН in анализ_ЗНАЧЕН['декларация'].values():
            Название = ввод_ЗНАЧЕН['Название']; путь = Path(ввод_ЗНАЧЕН['файл'])
            исходныйКод = путь.read_bytes()
            # русский 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if исходныйКод[ввод_ЗНАЧЕН['СМЕЩ_ЗНАЧЕН']:ввод_ЗНАЧЕН['СМЕЩ_ЗНАЧЕН']+len(Название)] == Название.encode() and Название not in экспортировать_ABI:
                실패들.append('{}:{}: {}'.format(путь.relative_to(задача_корень), ввод_ЗНАЧЕН['строка_ввода'], Название))
        LOG_ЗАПИСЬ['c_semantic_checked'] = True
        LOG_ЗАПИСЬ['c_source_sha256'] = {str(Path(файл).relative_to(задача_корень)):хэш_файл for файл,хэш_файл in анализ_ЗНАЧЕН['원문해시'].items()}
    LOG_ЗАПИСЬ['passed'] = not 실패들; LOG_ЗАПИСЬ['failures'] = 실패들
    цель_ЗНАЧЕН = задача_корень/'build/verification/naming'; цель_ЗНАЧЕН.mkdir(parents=True, exist_ok=True)
    (цель_ЗНАЧЕН/'report.json').write_text(json.dumps(LOG_ЗАПИСЬ, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: русский декларация·файл путь·호환 точка_входа·коммуникация 예제')

if __name__ == '__main__': запустить()
