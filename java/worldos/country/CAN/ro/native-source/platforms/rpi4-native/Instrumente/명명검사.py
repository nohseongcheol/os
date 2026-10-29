#!/usr/bin/env python3
"""명명 clip·excepție·경로를 검사한다. --시언어는 libclang declarație 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

Project_rădăcină = Path(__file__).resolve().parents[1]
depozit_rădăcină = Project_rădăcină.parents[1]

def Pornește():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--C_Limbi_străine', action='store_true')
    Argumente = parser_48ee4b1b.parse_args()
    실패들 = []
    caz_VALUE = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    Fișier_COUNT = 0
    parametru_tabel = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [depozit_rădăcină/'compiler/compilator.py', depozit_rădăcină/'compiler/기계어미리번역.py']
    for Cale in list((Project_rădăcină/'Instrumente').glob('*.py')) + list((Project_rădăcină/'예제').rglob('*.py')) + 공용번역기들:
        if Cale.name.endswith(('이름반영.py', '이름분석.py')): continue
        Fișier_COUNT += 1
        나무 = ast.parse(Cale.read_text()); 나무들[Cale] = 나무
        for intrare_VALUE in ast.walk(나무):
            if isinstance(intrare_VALUE, ast.FunctionDef):
                parametru_tabel.setdefault(intrare_VALUE.name, set()).update(parametru_argument.arg for parametru_argument in intrare_VALUE.args.args + intrare_VALUE.args.kwonlyargs)
                if intrare_VALUE.args.kwarg: 가변매개함수.add(intrare_VALUE.name)
            if isinstance(intrare_VALUE, ast.ClassDef):
                for funcție_VALUE in intrare_VALUE.body:
                    if isinstance(funcție_VALUE, ast.FunctionDef) and funcție_VALUE.name == '__init__':
                        parametru_tabel.setdefault(intrare_VALUE.name, set()).update(parametru_argument.arg for parametru_argument in funcție_VALUE.args.args + funcție_VALUE.args.kwonlyargs)
            Nume = ''
            if isinstance(intrare_VALUE, (ast.FunctionDef, ast.ClassDef)): Nume = intrare_VALUE.name
            elif isinstance(intrare_VALUE, ast.Name) and isinstance(intrare_VALUE.ctx, ast.Store): Nume = intrare_VALUE.id
            elif isinstance(intrare_VALUE, ast.arg): Nume = intrare_VALUE.arg
            if Nume and Nume not in caz_VALUE and all(ord(caracter_VALUE)<128 for caracter_VALUE in Nume):
                실패들.append('{}:{}: {}'.format(Cale.relative_to(depozit_rădăcină), intrare_VALUE.lineno, Nume))
    for Cale, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Nume = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Nume not in parametru_tabel or Nume in 가변매개함수 or not any(ord(caracter_VALUE)>127 for caracter_VALUE in Nume): continue
            for parametru_argument in 호출.keywords:
                if parametru_argument.arg and parametru_argument.arg not in parametru_tabel[Nume]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(Cale.relative_to(depozit_rădăcină), 호출.lineno, Nume, parametru_argument.arg))
    for Linie in (Project_rădăcină/'명명/nume_de_fișier_mapare.tsv').read_text().splitlines()[1:]:
        Anteriorul_element, curent_element, Proces_VALUE_intrare = Linie.split('\t')
        if not (Project_rădăcină/curent_element).is_file(): 실패들.append('muta_VALUE_83b651b8 Fișier 없음: '+curent_element)
        if Proces_VALUE_intrare == '호환진입점유지' and not (Project_rădăcină/Anteriorul_element).is_file(): 실패들.append('호환 intrare_p 없음: '+Anteriorul_element)
    예제 = (Project_rădăcină.parents[1]/'example/java/ExempluRețea.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for Cale in sorted((Project_rădăcină.parents[1]/'example/java').glob('*.java')):
        SURSĂ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Cale.read_text())
        for Nume in re.findall(r'\b[^\W\d]\w*\b', SURSĂ, re.UNICODE):
            if Nume not in 예약어 and all(ord(caracter_VALUE)<128 for caracter_VALUE in Nume):
                실패들.append('{}: 예제의 영어 identificator_VALUE {}'.format(Cale.name, Nume))
    for Nume in ('Fereastră', 'buton', 'Etichetă', 'câmp_text', '화면구성요소', 'eveniment_coadă', '작업가닥', '실행할일', '동작받이', 'Acțiune_înștiințare', '작업'):
        SURSĂ = (Project_rădăcină/'한국어자바/Română/propriu'/(Nume+'.java')).read_text()
        SURSĂ = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', SURSĂ)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', SURSĂ):
            실패들.append(Nume+': Română 직접 구현에 표준 obiect_VALUE 래퍼가 남았습니다.')
    시언어예제 = (Project_rădăcină.parents[1]/'example/c/ExempluRețea.c').read_text()
    for Nume in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Nume in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Nume: '+Nume)
    파이썬예제 = (Project_rădăcină.parents[1]/'example/python/ExempluRețea.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 excepție 직접 utiliza_VALUE')
    머리 = (Project_rădăcină.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Nume in ('cloud_Familie', 'racord_diagramă_informații', 'diagramă_informații_protocol', '통신주소', '인터넷통신주소', 'crea_participant', 'trimite_diagramă_informații_date'):
        if re.search(r'^#define\s+'+Nume+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 macrocomandă_VALUE utiliza_VALUE: '+Nume)
    자바파일수 = 0
    for rădăcină_VALUE in ('SURSĂ', 'utilizator/자바', '한국어자바'):
        for Cale in (Project_rădăcină/rădăcină_VALUE).rglob('*.java'):
            자바파일수 += 1
            SURSĂ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Cale.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', SURSĂ):
                실패들.append('{}: 한국어화되지 않은 declarație {}'.format(Cale.relative_to(Project_rădăcină), 맞음[1]))
            if rădăcină_VALUE == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', SURSĂ):
                실패들.append('{}: 공개 excepție declarație'.format(Cale.relative_to(Project_rădăcină)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for Cale in sorted((depozit_rădăcină/'os/SURSĂ').glob('*.java')):
        x86자바파일수 += 1
        SURSĂ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Cale.read_text())
        for Nume in re.findall(r'\b[^\W\d]\w*\b', SURSĂ, re.UNICODE):
            if Nume not in 예약어 | 표준자바이름 and all(ord(caracter_VALUE)<128 for caracter_VALUE in Nume):
                실패들.append('{}: propriu 영어 identificator_VALUE {}'.format(Cale.relative_to(depozit_rădăcină), Nume))
    LOG_RECORD = {'passed': False, 'python_files': Fișier_COUNT, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if Argumente.C_Limbi_străine:
        subprocess.check_call(['python3', str(Project_rădăcină/'Instrumente/시언어이름분석.py')])
        Analiză_VALUE = json.loads((Project_rădăcină/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(eroare) for eroare in Analiză_VALUE['eroare'])
        공개규약 = set(json.loads((Project_rădăcină/'명명/규격이름.json').read_text()))
        for intrare_VALUE in Analiză_VALUE['declarație'].values():
            Nume = intrare_VALUE['Nume']; Cale = Path(intrare_VALUE['Fișier'])
            SURSĂ = Cale.read_bytes()
            # Română 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if SURSĂ[intrare_VALUE['OFFSET_VALUE']:intrare_VALUE['OFFSET_VALUE']+len(Nume)] == Nume.encode() and Nume not in 공개규약:
                실패들.append('{}:{}: {}'.format(Cale.relative_to(Project_rădăcină), intrare_VALUE['Linie'], Nume))
        LOG_RECORD['c_semantic_checked'] = True
        LOG_RECORD['c_source_sha256'] = {str(Path(Fișier).relative_to(Project_rădăcină)):cod_hash_Fișier for Fișier,cod_hash_Fișier in Analiză_VALUE['원문해시'].items()}
    LOG_RECORD['passed'] = not 실패들; LOG_RECORD['failures'] = 실패들
    destinație_VALUE = Project_rădăcină/'build/verification/naming'; destinație_VALUE.mkdir(parents=True, exist_ok=True)
    (destinație_VALUE/'report.json').write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: Română declarație·Fișier Cale·호환 intrare_p·통신 예제')

if __name__ == '__main__': Pornește()
