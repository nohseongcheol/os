#!/usr/bin/env python3
"""명명 klip·izuzetak·경로를 검사한다. --시언어는 libclang deklaracija 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

radnja_koren = Path(__file__).resolve().parents[1]
depo_koren = radnja_koren.parents[1]

def koristiti():
    analizator_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizator_48ee4b1b.add_argument('--C_jezik', action='store_true')
    인수 = analizator_48ee4b1b.parse_args()
    실패들 = []
    ugovor_VALUE = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    Datoteka_COUNT = 0
    parametar_tabela = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [depo_koren/'compiler/kompajler.py', depo_koren/'compiler/기계어미리번역.py']
    for putanja in list((radnja_koren/'Alatke').glob('*.py')) + list((radnja_koren/'예제').rglob('*.py')) + 공용번역기들:
        if putanja.name.endswith(('이름반영.py', '이름분석.py')): continue
        Datoteka_COUNT += 1
        나무 = ast.parse(putanja.read_text()); 나무들[putanja] = 나무
        for stavka_VALUE in ast.walk(나무):
            if isinstance(stavka_VALUE, ast.FunctionDef):
                parametar_tabela.setdefault(stavka_VALUE.name, set()).update(parametar_argument.arg for parametar_argument in stavka_VALUE.args.args + stavka_VALUE.args.kwonlyargs)
                if stavka_VALUE.args.kwarg: 가변매개함수.add(stavka_VALUE.name)
            if isinstance(stavka_VALUE, ast.ClassDef):
                for FUNCTION_VALUE in stavka_VALUE.body:
                    if isinstance(FUNCTION_VALUE, ast.FunctionDef) and FUNCTION_VALUE.name == '__init__':
                        parametar_tabela.setdefault(stavka_VALUE.name, set()).update(parametar_argument.arg for parametar_argument in FUNCTION_VALUE.args.args + FUNCTION_VALUE.args.kwonlyargs)
            ime = ''
            if isinstance(stavka_VALUE, (ast.FunctionDef, ast.ClassDef)): ime = stavka_VALUE.name
            elif isinstance(stavka_VALUE, ast.Name) and isinstance(stavka_VALUE.ctx, ast.Store): ime = stavka_VALUE.id
            elif isinstance(stavka_VALUE, ast.arg): ime = stavka_VALUE.arg
            if ime and ime not in ugovor_VALUE and all(ord(znak_VALUE)<128 for znak_VALUE in ime):
                실패들.append('{}:{}: {}'.format(putanja.relative_to(depo_koren), stavka_VALUE.lineno, ime))
    for putanja, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            ime = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if ime not in parametar_tabela or ime in 가변매개함수 or not any(ord(znak_VALUE)>127 for znak_VALUE in ime): continue
            for parametar_argument in 호출.keywords:
                if parametar_argument.arg and parametar_argument.arg not in parametar_tabela[ime]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(putanja.relative_to(depo_koren), 호출.lineno, ime, parametar_argument.arg))
    for red in (radnja_koren/'명명/ime_datoteke_mapiranje.tsv').read_text().splitlines()[1:]:
        이전, aktuelno_stavka, Proces_VALUE_stavka = red.split('\t')
        if not (radnja_koren/aktuelno_stavka).is_file(): 실패들.append('premestiti_VALUE Datoteka 없음: '+aktuelno_stavka)
        if Proces_VALUE_stavka == '호환진입점유지' and not (radnja_koren/이전).is_file(): 실패들.append('호환 stavka_p 없음: '+이전)
    예제 = (radnja_koren.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for putanja in sorted((radnja_koren.parents[1]/'example/java').glob('*.java')):
        izvor = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', putanja.read_text())
        for ime in re.findall(r'\b[^\W\d]\w*\b', izvor, re.UNICODE):
            if ime not in 예약어 and all(ord(znak_VALUE)<128 for znak_VALUE in ime):
                실패들.append('{}: 예제의 영어 identifikator_VALUE {}'.format(putanja.name, ime))
    for ime in ('창', 'taster', 'oznaka', 'tekstualno_polje', '화면구성요소', 'događaj_red', '작업가닥', '실행할일', '동작받이', 'radnja_obaveštavanje', '작업'):
        izvor = (radnja_koren/'한국어자바/한국어/자체'/(ime+'.java')).read_text()
        izvor = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', izvor)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', izvor):
            실패들.append(ime+': 한국어 직접 구현에 표준 objekat_VALUE 래퍼가 남았습니다.')
    시언어예제 = (radnja_koren.parents[1]/'example/c/네트워크예제.c').read_text()
    for ime in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if ime in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 ime: '+ime)
    파이썬예제 = (radnja_koren.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 izuzetak 직접 koristiti_VALUE')
    머리 = (radnja_koren.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for ime in ('oblak_Porodica', 'datagramski_priključak', 'datagram_protokol', '통신주소', '인터넷통신주소', 'Create_učesnik', 'poslati_datagram_podaci'):
        if re.search(r'^#define\s+'+ime+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 makro_VALUE koristiti_VALUE: '+ime)
    자바파일수 = 0
    for koren_VALUE in ('izvor', 'korisnik/자바', '한국어자바'):
        for putanja in (radnja_koren/koren_VALUE).rglob('*.java'):
            자바파일수 += 1
            izvor = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', putanja.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', izvor):
                실패들.append('{}: 한국어화되지 않은 deklaracija {}'.format(putanja.relative_to(radnja_koren), 맞음[1]))
            if koren_VALUE == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', izvor):
                실패들.append('{}: 공개 izuzetak deklaracija'.format(putanja.relative_to(radnja_koren)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for putanja in sorted((depo_koren/'os/izvor').glob('*.java')):
        x86자바파일수 += 1
        izvor = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', putanja.read_text())
        for ime in re.findall(r'\b[^\W\d]\w*\b', izvor, re.UNICODE):
            if ime not in 예약어 | 표준자바이름 and all(ord(znak_VALUE)<128 for znak_VALUE in ime):
                실패들.append('{}: 자체 영어 identifikator_VALUE {}'.format(putanja.relative_to(depo_koren), ime))
    LOG_snimi = {'passed': False, 'python_files': Datoteka_COUNT, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if 인수.C_jezik:
        subprocess.check_call(['python3', str(radnja_koren/'Alatke/시언어이름분석.py')])
        Analiza_VALUE = json.loads((radnja_koren/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(greška) for greška in Analiza_VALUE['greška'])
        공개규약 = set(json.loads((radnja_koren/'명명/규격이름.json').read_text()))
        for stavka_VALUE in Analiza_VALUE['deklaracija'].values():
            ime = stavka_VALUE['ime']; putanja = Path(stavka_VALUE['Datoteka'])
            izvor = putanja.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if izvor[stavka_VALUE['Pomak_VALUE']:stavka_VALUE['Pomak_VALUE']+len(ime)] == ime.encode() and ime not in 공개규약:
                실패들.append('{}:{}: {}'.format(putanja.relative_to(radnja_koren), stavka_VALUE['줄'], ime))
        LOG_snimi['c_semantic_checked'] = True
        LOG_snimi['c_source_sha256'] = {str(Path(Datoteka).relative_to(radnja_koren)):heš_Datoteka for Datoteka,heš_Datoteka in Analiza_VALUE['원문해시'].items()}
    LOG_snimi['passed'] = not 실패들; LOG_snimi['failures'] = 실패들
    odredište_VALUE = radnja_koren/'build/verification/naming'; odredište_VALUE.mkdir(parents=True, exist_ok=True)
    (odredište_VALUE/'report.json').write_text(json.dumps(LOG_snimi, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 deklaracija·Datoteka putanja·호환 stavka_p·통신 예제')

if __name__ == '__main__': koristiti()
