#!/usr/bin/env python3
"""명명 isječak·iznimka·경로를 검사한다. --시언어는 libclang deklaracija 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

akcija_korijen = Path(__file__).resolve().parents[1]
spremište_korijen = akcija_korijen.parents[1]

def Pokreni():
    analizator_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizator_48ee4b1b.add_argument('--C_Jezik', action='store_true')
    Argumenti = analizator_48ee4b1b.parse_args()
    실패들 = []
    slučaj_VALUE = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    Datoteka_COUNT = 0
    parametar_tablica = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [spremište_korijen/'compiler/kompilator.py', spremište_korijen/'compiler/기계어미리번역.py']
    for PUTANJA in list((akcija_korijen/'Alati').glob('*.py')) + list((akcija_korijen/'예제').rglob('*.py')) + 공용번역기들:
        if PUTANJA.name.endswith(('이름반영.py', '이름분석.py')): continue
        Datoteka_COUNT += 1
        나무 = ast.parse(PUTANJA.read_text()); 나무들[PUTANJA] = 나무
        for unos_VALUE in ast.walk(나무):
            if isinstance(unos_VALUE, ast.FunctionDef):
                parametar_tablica.setdefault(unos_VALUE.name, set()).update(parametar_argument.arg for parametar_argument in unos_VALUE.args.args + unos_VALUE.args.kwonlyargs)
                if unos_VALUE.args.kwarg: 가변매개함수.add(unos_VALUE.name)
            if isinstance(unos_VALUE, ast.ClassDef):
                for FUNCTION_VALUE in unos_VALUE.body:
                    if isinstance(FUNCTION_VALUE, ast.FunctionDef) and FUNCTION_VALUE.name == '__init__':
                        parametar_tablica.setdefault(unos_VALUE.name, set()).update(parametar_argument.arg for parametar_argument in FUNCTION_VALUE.args.args + FUNCTION_VALUE.args.kwonlyargs)
            Ime = ''
            if isinstance(unos_VALUE, (ast.FunctionDef, ast.ClassDef)): Ime = unos_VALUE.name
            elif isinstance(unos_VALUE, ast.Name) and isinstance(unos_VALUE.ctx, ast.Store): Ime = unos_VALUE.id
            elif isinstance(unos_VALUE, ast.arg): Ime = unos_VALUE.arg
            if Ime and Ime not in slučaj_VALUE and all(ord(znak_VALUE)<128 for znak_VALUE in Ime):
                실패들.append('{}:{}: {}'.format(PUTANJA.relative_to(spremište_korijen), unos_VALUE.lineno, Ime))
    for PUTANJA, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Ime = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Ime not in parametar_tablica or Ime in 가변매개함수 or not any(ord(znak_VALUE)>127 for znak_VALUE in Ime): continue
            for parametar_argument in 호출.keywords:
                if parametar_argument.arg and parametar_argument.arg not in parametar_tablica[Ime]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(PUTANJA.relative_to(spremište_korijen), 호출.lineno, Ime, parametar_argument.arg))
    for red in (akcija_korijen/'명명/naziv_datoteke_mapiranje.tsv').read_text().splitlines()[1:]:
        이전, redovno_artikl, Proces_VALUE_unos = red.split('\t')
        if not (akcija_korijen/redovno_artikl).is_file(): 실패들.append('pomicati_se_VALUE Datoteka 없음: '+redovno_artikl)
        if Proces_VALUE_unos == '호환진입점유지' and not (akcija_korijen/이전).is_file(): 실패들.append('호환 unos_p 없음: '+이전)
    예제 = (akcija_korijen.parents[1]/'example/java/PrimjerMreže.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for PUTANJA in sorted((akcija_korijen.parents[1]/'example/java').glob('*.java')):
        IZVOR = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', PUTANJA.read_text())
        for Ime in re.findall(r'\b[^\W\d]\w*\b', IZVOR, re.UNICODE):
            if Ime not in 예약어 and all(ord(znak_VALUE)<128 for znak_VALUE in Ime):
                실패들.append('{}: 예제의 영어 identifikator_VALUE {}'.format(PUTANJA.name, Ime))
    for Ime in ('Prozor', 'gumb', 'Natpis', 'tekstno_polje', '화면구성요소', 'događaj_red_čekanja', '작업가닥', '실행할일', '동작받이', 'akcija_obavijest', '작업'):
        IZVOR = (akcija_korijen/'한국어자바/hrvatski/vlastiti'/(Ime+'.java')).read_text()
        IZVOR = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', IZVOR)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', IZVOR):
            실패들.append(Ime+': hrvatski 직접 구현에 표준 objekt_VALUE 래퍼가 남았습니다.')
    시언어예제 = (akcija_korijen.parents[1]/'example/c/PrimjerMreže.c').read_text()
    for Ime in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Ime in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Ime: '+Ime)
    파이썬예제 = (akcija_korijen.parents[1]/'example/python/PrimjerMreže.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 iznimka 직접 uporaba_VALUE')
    머리 = (akcija_korijen.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Ime in ('oblak_linija', 'datogramska_utičnica', 'datogram_protokol', '통신주소', '인터넷통신주소', 'Create_sudionik', 'slati_datogram_podaci'):
        if re.search(r'^#define\s+'+Ime+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 makro_VALUE uporaba_VALUE: '+Ime)
    자바파일수 = 0
    for korijen_VALUE in ('IZVOR', 'korisnik/자바', '한국어자바'):
        for PUTANJA in (akcija_korijen/korijen_VALUE).rglob('*.java'):
            자바파일수 += 1
            IZVOR = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', PUTANJA.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', IZVOR):
                실패들.append('{}: 한국어화되지 않은 deklaracija {}'.format(PUTANJA.relative_to(akcija_korijen), 맞음[1]))
            if korijen_VALUE == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', IZVOR):
                실패들.append('{}: 공개 iznimka deklaracija'.format(PUTANJA.relative_to(akcija_korijen)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for PUTANJA in sorted((spremište_korijen/'os/IZVOR').glob('*.java')):
        x86자바파일수 += 1
        IZVOR = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', PUTANJA.read_text())
        for Ime in re.findall(r'\b[^\W\d]\w*\b', IZVOR, re.UNICODE):
            if Ime not in 예약어 | 표준자바이름 and all(ord(znak_VALUE)<128 for znak_VALUE in Ime):
                실패들.append('{}: vlastiti 영어 identifikator_VALUE {}'.format(PUTANJA.relative_to(spremište_korijen), Ime))
    LOG_zapis = {'passed': False, 'python_files': Datoteka_COUNT, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if Argumenti.C_Jezik:
        subprocess.check_call(['python3', str(akcija_korijen/'Alati/시언어이름분석.py')])
        analiza_VALUE = json.loads((akcija_korijen/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(GREŠKA) for GREŠKA in analiza_VALUE['GREŠKA'])
        공개규약 = set(json.loads((akcija_korijen/'명명/규격이름.json').read_text()))
        for unos_VALUE in analiza_VALUE['deklaracija'].values():
            Ime = unos_VALUE['Ime']; PUTANJA = Path(unos_VALUE['Datoteka'])
            IZVOR = PUTANJA.read_bytes()
            # hrvatski 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if IZVOR[unos_VALUE['pomak_VALUE']:unos_VALUE['pomak_VALUE']+len(Ime)] == Ime.encode() and Ime not in 공개규약:
                실패들.append('{}:{}: {}'.format(PUTANJA.relative_to(akcija_korijen), unos_VALUE['줄'], Ime))
        LOG_zapis['c_semantic_checked'] = True
        LOG_zapis['c_source_sha256'] = {str(Path(Datoteka).relative_to(akcija_korijen)):raspršivanje_Datoteka for Datoteka,raspršivanje_Datoteka in analiza_VALUE['원문해시'].items()}
    LOG_zapis['passed'] = not 실패들; LOG_zapis['failures'] = 실패들
    odredište_VALUE = akcija_korijen/'build/verification/naming'; odredište_VALUE.mkdir(parents=True, exist_ok=True)
    (odredište_VALUE/'report.json').write_text(json.dumps(LOG_zapis, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: hrvatski deklaracija·Datoteka PUTANJA·호환 unos_p·통신 예제')

if __name__ == '__main__': Pokreni()
