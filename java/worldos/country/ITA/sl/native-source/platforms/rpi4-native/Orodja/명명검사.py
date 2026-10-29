#!/usr/bin/env python3
"""명명 izrezek·izjema·경로를 검사한다. --시언어는 libclang deklaracija 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

pobuda_koren = Path(__file__).resolve().parents[1]
shramba_koren = pobuda_koren.parents[1]

def Zaženi():
    razčlenjevalnik_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    razčlenjevalnik_48ee4b1b.add_argument('--C_jezik', action='store_true')
    Argumenti = razčlenjevalnik_48ee4b1b.parse_args()
    실패들 = []
    primer_VALUE = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    Datoteka_COUNT = 0
    parameter_tabela = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [shramba_koren/'compiler/prevajalnik.py', shramba_koren/'compiler/기계어미리번역.py']
    for POT in list((pobuda_koren/'Orodja').glob('*.py')) + list((pobuda_koren/'예제').rglob('*.py')) + 공용번역기들:
        if POT.name.endswith(('이름반영.py', '이름분석.py')): continue
        Datoteka_COUNT += 1
        나무 = ast.parse(POT.read_text()); 나무들[POT] = 나무
        for vnos_VALUE in ast.walk(나무):
            if isinstance(vnos_VALUE, ast.FunctionDef):
                parameter_tabela.setdefault(vnos_VALUE.name, set()).update(parameter_argument.arg for parameter_argument in vnos_VALUE.args.args + vnos_VALUE.args.kwonlyargs)
                if vnos_VALUE.args.kwarg: 가변매개함수.add(vnos_VALUE.name)
            if isinstance(vnos_VALUE, ast.ClassDef):
                for FUNCTION_VALUE in vnos_VALUE.body:
                    if isinstance(FUNCTION_VALUE, ast.FunctionDef) and FUNCTION_VALUE.name == '__init__':
                        parameter_tabela.setdefault(vnos_VALUE.name, set()).update(parameter_argument.arg for parameter_argument in FUNCTION_VALUE.args.args + FUNCTION_VALUE.args.kwonlyargs)
            Ime = ''
            if isinstance(vnos_VALUE, (ast.FunctionDef, ast.ClassDef)): Ime = vnos_VALUE.name
            elif isinstance(vnos_VALUE, ast.Name) and isinstance(vnos_VALUE.ctx, ast.Store): Ime = vnos_VALUE.id
            elif isinstance(vnos_VALUE, ast.arg): Ime = vnos_VALUE.arg
            if Ime and Ime not in primer_VALUE and all(ord(znak_VALUE)<128 for znak_VALUE in Ime):
                실패들.append('{}:{}: {}'.format(POT.relative_to(shramba_koren), vnos_VALUE.lineno, Ime))
    for POT, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Ime = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Ime not in parameter_tabela or Ime in 가변매개함수 or not any(ord(znak_VALUE)>127 for znak_VALUE in Ime): continue
            for parameter_argument in 호출.keywords:
                if parameter_argument.arg and parameter_argument.arg not in parameter_tabela[Ime]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(POT.relative_to(shramba_koren), 호출.lineno, Ime, parameter_argument.arg))
    for Črtni in (pobuda_koren/'명명/ime_datoteke_preslikava.tsv').read_text().splitlines()[1:]:
        이전, sprotno_element, Proces_VALUE_vnos = Črtni.split('\t')
        if not (pobuda_koren/sprotno_element).is_file(): 실패들.append('premikati_VALUE Datoteka 없음: '+sprotno_element)
        if Proces_VALUE_vnos == '호환진입점유지' and not (pobuda_koren/이전).is_file(): 실패들.append('호환 vnos_p 없음: '+이전)
    예제 = (pobuda_koren.parents[1]/'example/java/PrimerOmrežja.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for POT in sorted((pobuda_koren.parents[1]/'example/java').glob('*.java')):
        VIR = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', POT.read_text())
        for Ime in re.findall(r'\b[^\W\d]\w*\b', VIR, re.UNICODE):
            if Ime not in 예약어 and all(ord(znak_VALUE)<128 for znak_VALUE in Ime):
                실패들.append('{}: 예제의 영어 identifikator_VALUE {}'.format(POT.name, Ime))
    for Ime in ('창', 'Gumb', 'Oznaka', 'SMS_polje', '화면구성요소', 'dogodek_čakalna_vrsta', '작업가닥', '실행할일', '동작받이', 'akcija_obvestilo', '작업'):
        VIR = (pobuda_koren/'한국어자바/slovenščina/lastno'/(Ime+'.java')).read_text()
        VIR = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', VIR)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', VIR):
            실패들.append(Ime+': slovenščina 직접 구현에 표준 predmet_VALUE 래퍼가 남았습니다.')
    시언어예제 = (pobuda_koren.parents[1]/'example/c/PrimerOmrežja.c').read_text()
    for Ime in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Ime in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Ime: '+Ime)
    파이썬예제 = (pobuda_koren.parents[1]/'example/python/PrimerOmrežja.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 izjema 직접 uporaba_VALUE')
    머리 = (pobuda_koren.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Ime in ('oblak_Družina', 'vtičnica_za_prenos_datagramov', 'datagram_protokol', 'vtičnica_naslov', 'oblak_vtičnica_naslov', 'Ustvari_končna_točka', 'poslati_datagram_podatki'):
        if re.search(r'^#define\s+'+Ime+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 makro_VALUE uporaba_VALUE: '+Ime)
    자바파일수 = 0
    for koren_VALUE in ('VIR', 'uporabnik/자바', '한국어자바'):
        for POT in (pobuda_koren/koren_VALUE).rglob('*.java'):
            자바파일수 += 1
            VIR = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', POT.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', VIR):
                실패들.append('{}: 한국어화되지 않은 deklaracija {}'.format(POT.relative_to(pobuda_koren), 맞음[1]))
            if koren_VALUE == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', VIR):
                실패들.append('{}: 공개 izjema deklaracija'.format(POT.relative_to(pobuda_koren)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for POT in sorted((shramba_koren/'os/VIR').glob('*.java')):
        x86자바파일수 += 1
        VIR = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', POT.read_text())
        for Ime in re.findall(r'\b[^\W\d]\w*\b', VIR, re.UNICODE):
            if Ime not in 예약어 | 표준자바이름 and all(ord(znak_VALUE)<128 for znak_VALUE in Ime):
                실패들.append('{}: lastno 영어 identifikator_VALUE {}'.format(POT.relative_to(shramba_koren), Ime))
    LOG_zapis = {'passed': False, 'python_files': Datoteka_COUNT, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if Argumenti.C_jezik:
        subprocess.check_call(['python3', str(pobuda_koren/'Orodja/시언어이름분석.py')])
        analiza_VALUE = json.loads((pobuda_koren/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(NAPAKA) for NAPAKA in analiza_VALUE['NAPAKA'])
        공개규약 = set(json.loads((pobuda_koren/'명명/규격이름.json').read_text()))
        for vnos_VALUE in analiza_VALUE['deklaracija'].values():
            Ime = vnos_VALUE['Ime']; POT = Path(vnos_VALUE['Datoteka'])
            VIR = POT.read_bytes()
            # slovenščina 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if VIR[vnos_VALUE['odmik_VALUE']:vnos_VALUE['odmik_VALUE']+len(Ime)] == Ime.encode() and Ime not in 공개규약:
                실패들.append('{}:{}: {}'.format(POT.relative_to(pobuda_koren), vnos_VALUE['Črtni'], Ime))
        LOG_zapis['c_semantic_checked'] = True
        LOG_zapis['c_source_sha256'] = {str(Path(Datoteka).relative_to(pobuda_koren)):zgoščena_vrednost_Datoteka for Datoteka,zgoščena_vrednost_Datoteka in analiza_VALUE['원문해시'].items()}
    LOG_zapis['passed'] = not 실패들; LOG_zapis['failures'] = 실패들
    cilj_VALUE = pobuda_koren/'build/verification/naming'; cilj_VALUE.mkdir(parents=True, exist_ok=True)
    (cilj_VALUE/'report.json').write_text(json.dumps(LOG_zapis, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: slovenščina deklaracija·Datoteka POT·호환 vnos_p·통신 예제')

if __name__ == '__main__': Zaženi()
