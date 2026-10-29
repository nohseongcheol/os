#!/usr/bin/env python3
"""명명 кліп·виняток·경로를 검사한다. --시언어는 libclang оголошення_4f4f026b 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

Дії_корінь = Path(__file__).resolve().parents[1]
репозиторій_корінь = Дії_корінь.parents[1]

def запустити():
    аналізатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    аналізатор_48ee4b1b.add_argument('--시언어', action='store_true')
    аргументи = аналізатор_48ee4b1b.parse_args()
    실패들 = []
    контракт_значення = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    파일수 = 0
    параметр_таблиця = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [репозиторій_корінь/'compiler/компілятор.py', репозиторій_корінь/'compiler/기계어미리번역.py']
    for шлях in list((Дії_корінь/'інструменти').glob('*.py')) + list((Дії_корінь/'예제').rglob('*.py')) + 공용번역기들:
        if шлях.name.endswith(('이름반영.py', '이름분석.py')): continue
        파일수 += 1
        나무 = ast.parse(шлях.read_text()); 나무들[шлях] = 나무
        for запис_значення_962f286b in ast.walk(나무):
            if isinstance(запис_значення_962f286b, ast.FunctionDef):
                параметр_таблиця.setdefault(запис_значення_962f286b.name, set()).update(параметр_аргумент.arg for параметр_аргумент in запис_значення_962f286b.args.args + запис_значення_962f286b.args.kwonlyargs)
                if запис_значення_962f286b.args.kwarg: 가변매개함수.add(запис_значення_962f286b.name)
            if isinstance(запис_значення_962f286b, ast.ClassDef):
                for функція_значення in запис_значення_962f286b.body:
                    if isinstance(функція_значення, ast.FunctionDef) and функція_значення.name == '__init__':
                        параметр_таблиця.setdefault(запис_значення_962f286b.name, set()).update(параметр_аргумент.arg for параметр_аргумент in функція_значення.args.args + функція_значення.args.kwonlyargs)
            Назва = ''
            if isinstance(запис_значення_962f286b, (ast.FunctionDef, ast.ClassDef)): Назва = запис_значення_962f286b.name
            elif isinstance(запис_значення_962f286b, ast.Name) and isinstance(запис_значення_962f286b.ctx, ast.Store): Назва = запис_значення_962f286b.id
            elif isinstance(запис_значення_962f286b, ast.arg): Назва = запис_значення_962f286b.arg
            if Назва and Назва not in контракт_значення and all(ord(символ_значення_068c2631)<128 for символ_значення_068c2631 in Назва):
                실패들.append('{}:{}: {}'.format(шлях.relative_to(репозиторій_корінь), запис_значення_962f286b.lineno, Назва))
    for шлях, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Назва = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Назва not in параметр_таблиця or Назва in 가변매개함수 or not any(ord(символ_значення_068c2631)>127 for символ_значення_068c2631 in Назва): continue
            for параметр_аргумент in 호출.keywords:
                if параметр_аргумент.arg and параметр_аргумент.arg not in параметр_таблиця[Назва]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(шлях.relative_to(репозиторій_корінь), 호출.lineno, Назва, параметр_аргумент.arg))
    for рядок_введення in (Дії_корінь/'명명/ім_я_файлу_зіставлення.tsv').read_text().splitlines()[1:]:
        이전, чинний_елемент, процес_значення_запис = рядок_введення.split('\t')
        if not (Дії_корінь/чинний_елемент).is_file(): 실패들.append('переміщати_значення файл 없음: '+чинний_елемент)
        if процес_значення_запис == '호환진입점유지' and not (Дії_корінь/이전).is_file(): 실패들.append('호환 запис_бал 없음: '+이전)
    예제 = (Дії_корінь.parents[1]/'example/java/ПрикладМережі.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for шлях in sorted((Дії_корінь.parents[1]/'example/java').glob('*.java')):
        вихіднийКод = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', шлях.read_text())
        for Назва in re.findall(r'\b[^\W\d]\w*\b', вихіднийКод, re.UNICODE):
            if Назва not in 예약어 and all(ord(символ_значення_068c2631)<128 for символ_значення_068c2631 in Назва):
                실패들.append('{}: 예제의 영어 ідентифікатор_значення {}'.format(шлях.name, Назва))
    for Назва in ('Вікно', 'кнопка', 'Мітка', 'текстове_поле', '화면구성요소', 'подія_черга', 'фоноваЗадача', '실행할일', '동작받이', 'Дія_повідомлення', '작업'):
        вихіднийКод = (Дії_корінь/'한국어자바/українська/своє'/(Назва+'.java')).read_text()
        вихіднийКод = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', вихіднийКод)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', вихіднийКод):
            실패들.append(Назва+': українська 직접 구현에 표준 об_єкт_значення 래퍼가 남았습니다.')
    시언어예제 = (Дії_корінь.parents[1]/'example/c/ПрикладМережі.c').read_text()
    for Назва in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Назва in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Назва: '+Назва)
    파이썬예제 = (Дії_корінь.parents[1]/'example/python/ПрикладМережі.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 виняток 직접 використання_значення')
    머리 = (Дії_корінь.parents[1]/'posix-kor/arm64-native/оголошення/통신규약.h').read_text()
    for Назва in ('хмара_сім_я', 'сокет_дейтаграми', 'дейтаграма_протокол', 'сокет_адреса', 'хмара_сокет_адреса', 'Створення_учасник', 'надсилати_дейтаграма_дані'):
        if re.search(r'^#define\s+'+Назва+r'\b', 머리, re.M): 실패들.append('C 직접 реалізація 대신 макрос_значення використання_значення: '+Назва)
    자바파일수 = 0
    for корінь_значення in ('вихіднийКод', 'простір_користувача/자바', '한국어자바'):
        for шлях in (Дії_корінь/корінь_значення).rglob('*.java'):
            자바파일수 += 1
            вихіднийКод = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', шлях.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', вихіднийКод):
                실패들.append('{}: 한국어화되지 않은 оголошення_4f4f026b {}'.format(шлях.relative_to(Дії_корінь), 맞음[1]))
            if корінь_значення == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', вихіднийКод):
                실패들.append('{}: 공개 виняток оголошення_4f4f026b'.format(шлях.relative_to(Дії_корінь)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for шлях in sorted((репозиторій_корінь/'os/вихіднийКод').glob('*.java')):
        x86자바파일수 += 1
        вихіднийКод = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', шлях.read_text())
        for Назва in re.findall(r'\b[^\W\d]\w*\b', вихіднийКод, re.UNICODE):
            if Назва not in 예약어 | 표준자바이름 and all(ord(символ_значення_068c2631)<128 for символ_значення_068c2631 in Назва):
                실패들.append('{}: своє 영어 ідентифікатор_значення {}'.format(шлях.relative_to(репозиторій_корінь), Назва))
    журнал_запис = {'passed': False, 'python_files': 파일수, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if аргументи.시언어:
        subprocess.check_call(['python3', str(Дії_корінь/'інструменти/시언어이름분석.py')])
        Аналіз_значення = json.loads((Дії_корінь/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(ПОМИЛКА) for ПОМИЛКА in Аналіз_значення['ПОМИЛКА'])
        공개규약 = set(json.loads((Дії_корінь/'명명/규격이름.json').read_text()))
        for запис_значення_962f286b in Аналіз_значення['оголошення_4f4f026b'].values():
            Назва = запис_значення_962f286b['Назва']; шлях = Path(запис_значення_962f286b['файл'])
            вихіднийКод = шлях.read_bytes()
            # українська 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if вихіднийКод[запис_значення_962f286b['Зміщена_копія_значення']:запис_значення_962f286b['Зміщена_копія_значення']+len(Назва)] == Назва.encode() and Назва not in 공개규약:
                실패들.append('{}:{}: {}'.format(шлях.relative_to(Дії_корінь), запис_значення_962f286b['рядок_введення'], Назва))
        журнал_запис['c_semantic_checked'] = True
        журнал_запис['c_source_sha256'] = {str(Path(файл).relative_to(Дії_корінь)):геш_код_Файл for файл,геш_код_Файл in Аналіз_значення['원문해시'].items()}
    журнал_запис['passed'] = not 실패들; журнал_запис['failures'] = 실패들
    місце_значення = Дії_корінь/'build/verification/naming'; місце_значення.mkdir(parents=True, exist_ok=True)
    (місце_значення/'report.json').write_text(json.dumps(журнал_запис, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: українська оголошення_4f4f026b·файл шлях·호환 запис_бал·통신 예제')

if __name__ == '__main__': запустити()
