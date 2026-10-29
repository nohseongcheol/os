#!/usr/bin/env python3
"""명명 klipas·išimtis·경로를 검사한다. --시언어는 libclang deklaracija 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

Project_šaknis = Path(__file__).resolve().parents[1]
saugykla_šaknis = Project_šaknis.parents[1]

def Paleisti():
    analizatorius_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizatorius_48ee4b1b.add_argument('--C_Kalba', action='store_true')
    Argumentai = analizatorius_48ee4b1b.parse_args()
    실패들 = []
    sutarties_vertė = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    Failas_COUNT = 0
    parametras_lentelė = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [saugykla_šaknis/'compiler/kompiliatorius.py', saugykla_šaknis/'compiler/기계어미리번역.py']
    for KELIAS in list((Project_šaknis/'Įrankiai').glob('*.py')) + list((Project_šaknis/'예제').rglob('*.py')) + 공용번역기들:
        if KELIAS.name.endswith(('이름반영.py', '이름분석.py')): continue
        Failas_COUNT += 1
        나무 = ast.parse(KELIAS.read_text()); 나무들[KELIAS] = 나무
        for įrašas_VALUE in ast.walk(나무):
            if isinstance(įrašas_VALUE, ast.FunctionDef):
                parametras_lentelė.setdefault(įrašas_VALUE.name, set()).update(parametras_argumentas.arg for parametras_argumentas in įrašas_VALUE.args.args + įrašas_VALUE.args.kwonlyargs)
                if įrašas_VALUE.args.kwarg: 가변매개함수.add(įrašas_VALUE.name)
            if isinstance(įrašas_VALUE, ast.ClassDef):
                for FUNCTION_VALUE in įrašas_VALUE.body:
                    if isinstance(FUNCTION_VALUE, ast.FunctionDef) and FUNCTION_VALUE.name == '__init__':
                        parametras_lentelė.setdefault(įrašas_VALUE.name, set()).update(parametras_argumentas.arg for parametras_argumentas in FUNCTION_VALUE.args.args + FUNCTION_VALUE.args.kwonlyargs)
            Pavadinimas_2 = ''
            if isinstance(įrašas_VALUE, (ast.FunctionDef, ast.ClassDef)): Pavadinimas_2 = įrašas_VALUE.name
            elif isinstance(įrašas_VALUE, ast.Name) and isinstance(įrašas_VALUE.ctx, ast.Store): Pavadinimas_2 = įrašas_VALUE.id
            elif isinstance(įrašas_VALUE, ast.arg): Pavadinimas_2 = įrašas_VALUE.arg
            if Pavadinimas_2 and Pavadinimas_2 not in sutarties_vertė and all(ord(simbolis_VALUE_068c2631)<128 for simbolis_VALUE_068c2631 in Pavadinimas_2):
                실패들.append('{}:{}: {}'.format(KELIAS.relative_to(saugykla_šaknis), įrašas_VALUE.lineno, Pavadinimas_2))
    for KELIAS, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Pavadinimas_2 = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Pavadinimas_2 not in parametras_lentelė or Pavadinimas_2 in 가변매개함수 or not any(ord(simbolis_VALUE_068c2631)>127 for simbolis_VALUE_068c2631 in Pavadinimas_2): continue
            for parametras_argumentas in 호출.keywords:
                if parametras_argumentas.arg and parametras_argumentas.arg not in parametras_lentelė[Pavadinimas_2]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(KELIAS.relative_to(saugykla_šaknis), 호출.lineno, Pavadinimas_2, parametras_argumentas.arg))
    for Eilutė in (Project_šaknis/'명명/failo_vardas_susiejimas.tsv').read_text().splitlines()[1:]:
        이전, dabartinis_prekė, Procesas_VALUE_įrašas = Eilutė.split('\t')
        if not (Project_šaknis/dabartinis_prekė).is_file(): 실패들.append('judėti_VALUE Failas 없음: '+dabartinis_prekė)
        if Procesas_VALUE_įrašas == '호환진입점유지' and not (Project_šaknis/이전).is_file(): 실패들.append('호환 įrašas_p 없음: '+이전)
    예제 = (Project_šaknis.parents[1]/'example/java/TinkloPavyzdys.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for KELIAS in sorted((Project_šaknis.parents[1]/'example/java').glob('*.java')):
        ŠALTINIS = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', KELIAS.read_text())
        for Pavadinimas_2 in re.findall(r'\b[^\W\d]\w*\b', ŠALTINIS, re.UNICODE):
            if Pavadinimas_2 not in 예약어 and all(ord(simbolis_VALUE_068c2631)<128 for simbolis_VALUE_068c2631 in Pavadinimas_2):
                실패들.append('{}: 예제의 영어 identifikatorius_VALUE {}'.format(KELIAS.name, Pavadinimas_2))
    for Pavadinimas_2 in ('Langas', 'mygtukas', 'Pavadinimas', 'teksto_laukas', '화면구성요소', 'įvykis_eilė', 'darbininkas', '실행할일', '동작받이', 'gavinys_pranešimas', '작업'):
        ŠALTINIS = (Project_šaknis/'한국어자바/Lietuvių/savas'/(Pavadinimas_2+'.java')).read_text()
        ŠALTINIS = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', ŠALTINIS)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', ŠALTINIS):
            실패들.append(Pavadinimas_2+': Lietuvių 직접 구현에 표준 objektas_VALUE 래퍼가 남았습니다.')
    시언어예제 = (Project_šaknis.parents[1]/'example/c/TinkloPavyzdys.c').read_text()
    for Pavadinimas_2 in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Pavadinimas_2 in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Pavadinimas_2: '+Pavadinimas_2)
    파이썬예제 = (Project_šaknis.parents[1]/'example/python/TinkloPavyzdys.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 išimtis 직접 naudoti_VALUE')
    머리 = (Project_šaknis.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Pavadinimas_2 in ('debesis_Šeima', 'paketų_maršruto_schemos_jungtis', 'paketų_kelio_schema_protokolas', '통신주소', '인터넷통신주소', 'kurti_dalyvis', 'siųsti_paketų_kelio_schema_duomenys'):
        if re.search(r'^#define\s+'+Pavadinimas_2+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 makrokomanda_VALUE naudoti_VALUE: '+Pavadinimas_2)
    자바파일수 = 0
    for šaknis_VALUE in ('ŠALTINIS', 'naudotojas/자바', '한국어자바'):
        for KELIAS in (Project_šaknis/šaknis_VALUE).rglob('*.java'):
            자바파일수 += 1
            ŠALTINIS = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', KELIAS.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', ŠALTINIS):
                실패들.append('{}: 한국어화되지 않은 deklaracija {}'.format(KELIAS.relative_to(Project_šaknis), 맞음[1]))
            if šaknis_VALUE == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', ŠALTINIS):
                실패들.append('{}: 공개 išimtis deklaracija'.format(KELIAS.relative_to(Project_šaknis)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for KELIAS in sorted((saugykla_šaknis/'os/ŠALTINIS').glob('*.java')):
        x86자바파일수 += 1
        ŠALTINIS = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', KELIAS.read_text())
        for Pavadinimas_2 in re.findall(r'\b[^\W\d]\w*\b', ŠALTINIS, re.UNICODE):
            if Pavadinimas_2 not in 예약어 | 표준자바이름 and all(ord(simbolis_VALUE_068c2631)<128 for simbolis_VALUE_068c2631 in Pavadinimas_2):
                실패들.append('{}: savas 영어 identifikatorius_VALUE {}'.format(KELIAS.relative_to(saugykla_šaknis), Pavadinimas_2))
    LOG_RECORD = {'passed': False, 'python_files': Failas_COUNT, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if Argumentai.C_Kalba:
        subprocess.check_call(['python3', str(Project_šaknis/'Įrankiai/시언어이름분석.py')])
        Analizė_VALUE = json.loads((Project_šaknis/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(KLAIDA) for KLAIDA in Analizė_VALUE['KLAIDA'])
        공개규약 = set(json.loads((Project_šaknis/'명명/규격이름.json').read_text()))
        for įrašas_VALUE in Analizė_VALUE['deklaracija'].values():
            Pavadinimas_2 = įrašas_VALUE['Pavadinimas_2']; KELIAS = Path(įrašas_VALUE['Failas'])
            ŠALTINIS = KELIAS.read_bytes()
            # Lietuvių 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if ŠALTINIS[įrašas_VALUE['OFFSET_VALUE']:įrašas_VALUE['OFFSET_VALUE']+len(Pavadinimas_2)] == Pavadinimas_2.encode() and Pavadinimas_2 not in 공개규약:
                실패들.append('{}:{}: {}'.format(KELIAS.relative_to(Project_šaknis), įrašas_VALUE['Eilutė'], Pavadinimas_2))
        LOG_RECORD['c_semantic_checked'] = True
        LOG_RECORD['c_source_sha256'] = {str(Path(Failas).relative_to(Project_šaknis)):maiša_Failas for Failas,maiša_Failas in Analizė_VALUE['원문해시'].items()}
    LOG_RECORD['passed'] = not 실패들; LOG_RECORD['failures'] = 실패들
    vieta_VALUE = Project_šaknis/'build/verification/naming'; vieta_VALUE.mkdir(parents=True, exist_ok=True)
    (vieta_VALUE/'report.json').write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: Lietuvių deklaracija·Failas KELIAS·호환 įrašas_p·통신 예제')

if __name__ == '__main__': Paleisti()
