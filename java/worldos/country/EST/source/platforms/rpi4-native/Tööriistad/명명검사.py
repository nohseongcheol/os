#!/usr/bin/env python3
"""명명 klipp·erand·경로를 검사한다. --시언어는 libclang deklaratsioon 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

Project_juur = Path(__file__).resolve().parents[1]
hoidla_juur = Project_juur.parents[1]

def Käivita_2():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--_15_Keeled', action='store_true')
    Argumendid = parser_48ee4b1b.parse_args()
    실패들 = []
    lepingu_väärtus = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    Fail_COUNT = 0
    parameeter_tabel = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [hoidla_juur/'compiler/kompilaator.py', hoidla_juur/'compiler/기계어미리번역.py']
    for RADA in list((Project_juur/'Tööriistad').glob('*.py')) + list((Project_juur/'예제').rglob('*.py')) + 공용번역기들:
        if RADA.name.endswith(('이름반영.py', '이름분석.py')): continue
        Fail_COUNT += 1
        나무 = ast.parse(RADA.read_text()); 나무들[RADA] = 나무
        for kirje_VALUE in ast.walk(나무):
            if isinstance(kirje_VALUE, ast.FunctionDef):
                parameeter_tabel.setdefault(kirje_VALUE.name, set()).update(parameeter_argument.arg for parameeter_argument in kirje_VALUE.args.args + kirje_VALUE.args.kwonlyargs)
                if kirje_VALUE.args.kwarg: 가변매개함수.add(kirje_VALUE.name)
            if isinstance(kirje_VALUE, ast.ClassDef):
                for FUNCTION_VALUE in kirje_VALUE.body:
                    if isinstance(FUNCTION_VALUE, ast.FunctionDef) and FUNCTION_VALUE.name == '__init__':
                        parameeter_tabel.setdefault(kirje_VALUE.name, set()).update(parameeter_argument.arg for parameeter_argument in FUNCTION_VALUE.args.args + FUNCTION_VALUE.args.kwonlyargs)
            Nimi_2 = ''
            if isinstance(kirje_VALUE, (ast.FunctionDef, ast.ClassDef)): Nimi_2 = kirje_VALUE.name
            elif isinstance(kirje_VALUE, ast.Name) and isinstance(kirje_VALUE.ctx, ast.Store): Nimi_2 = kirje_VALUE.id
            elif isinstance(kirje_VALUE, ast.arg): Nimi_2 = kirje_VALUE.arg
            if Nimi_2 and Nimi_2 not in lepingu_väärtus and all(ord(märk_VALUE)<128 for märk_VALUE in Nimi_2):
                실패들.append('{}:{}: {}'.format(RADA.relative_to(hoidla_juur), kirje_VALUE.lineno, Nimi_2))
    for RADA, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Nimi_2 = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Nimi_2 not in parameeter_tabel or Nimi_2 in 가변매개함수 or not any(ord(märk_VALUE)>127 for märk_VALUE in Nimi_2): continue
            for parameeter_argument in 호출.keywords:
                if parameeter_argument.arg and parameeter_argument.arg not in parameeter_tabel[Nimi_2]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(RADA.relative_to(hoidla_juur), 호출.lineno, Nimi_2, parameeter_argument.arg))
    for Joon in (Project_juur/'명명/failinimi_vastendamine.tsv').read_text().splitlines()[1:]:
        이전, tähtaja_piires_kaup, Joonis_VALUE_kirje = Joon.split('\t')
        if not (Project_juur/tähtaja_piires_kaup).is_file(): 실패들.append('liigutama_VALUE Fail 없음: '+tähtaja_piires_kaup)
        if Joonis_VALUE_kirje == '호환진입점유지' and not (Project_juur/이전).is_file(): 실패들.append('호환 kirje_p 없음: '+이전)
    예제 = (Project_juur.parents[1]/'example/java/VõrguNäide.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for RADA in sorted((Project_juur.parents[1]/'example/java').glob('*.java')):
        ALLIKAS = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', RADA.read_text())
        for Nimi_2 in re.findall(r'\b[^\W\d]\w*\b', ALLIKAS, re.UNICODE):
            if Nimi_2 not in 예약어 and all(ord(märk_VALUE)<128 for märk_VALUE in Nimi_2):
                실패들.append('{}: 예제의 영어 identifikaator_VALUE {}'.format(RADA.name, Nimi_2))
    for Nimi_2 in ('창', 'nupp', 'Silt', 'tekstiväli', '화면구성요소', 'sündmus_järjekord', 'töötaja', '실행할일', '동작받이', 'Toiming_teatamine', '작업'):
        ALLIKAS = (Project_juur/'한국어자바/Eesti/oma'/(Nimi_2+'.java')).read_text()
        ALLIKAS = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', ALLIKAS)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', ALLIKAS):
            실패들.append(Nimi_2+': Eesti 직접 구현에 표준 objekt_VALUE 래퍼가 남았습니다.')
    시언어예제 = (Project_juur.parents[1]/'example/c/VõrguNäide.c').read_text()
    for Nimi_2 in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Nimi_2 in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Nimi_2: '+Nimi_2)
    파이썬예제 = (Project_juur.parents[1]/'example/python/VõrguNäide.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 erand 직접 kasutus_VALUE')
    머리 = (Project_juur.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Nimi_2 in ('pilv_Pere', 'datagrammisokkel', 'datagramm_protokoll', '통신주소', '인터넷통신주소', 'avama_osaleja', 'saatma_datagramm_andmed'):
        if re.search(r'^#define\s+'+Nimi_2+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 makro_VALUE kasutus_VALUE: '+Nimi_2)
    자바파일수 = 0
    for juur_VALUE in ('ALLIKAS', 'kasutaja/자바', '한국어자바'):
        for RADA in (Project_juur/juur_VALUE).rglob('*.java'):
            자바파일수 += 1
            ALLIKAS = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', RADA.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', ALLIKAS):
                실패들.append('{}: 한국어화되지 않은 deklaratsioon {}'.format(RADA.relative_to(Project_juur), 맞음[1]))
            if juur_VALUE == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', ALLIKAS):
                실패들.append('{}: 공개 erand deklaratsioon'.format(RADA.relative_to(Project_juur)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for RADA in sorted((hoidla_juur/'os/ALLIKAS').glob('*.java')):
        x86자바파일수 += 1
        ALLIKAS = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', RADA.read_text())
        for Nimi_2 in re.findall(r'\b[^\W\d]\w*\b', ALLIKAS, re.UNICODE):
            if Nimi_2 not in 예약어 | 표준자바이름 and all(ord(märk_VALUE)<128 for märk_VALUE in Nimi_2):
                실패들.append('{}: oma 영어 identifikaator_VALUE {}'.format(RADA.relative_to(hoidla_juur), Nimi_2))
    LOG_kirje = {'passed': False, 'python_files': Fail_COUNT, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if Argumendid._15_Keeled:
        subprocess.check_call(['python3', str(Project_juur/'Tööriistad/시언어이름분석.py')])
        Analüüs_VALUE = json.loads((Project_juur/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(VIGA) for VIGA in Analüüs_VALUE['VIGA'])
        공개규약 = set(json.loads((Project_juur/'명명/규격이름.json').read_text()))
        for kirje_VALUE in Analüüs_VALUE['deklaratsioon'].values():
            Nimi_2 = kirje_VALUE['Nimi_2']; RADA = Path(kirje_VALUE['Fail'])
            ALLIKAS = RADA.read_bytes()
            # Eesti 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if ALLIKAS[kirje_VALUE['nihe_VALUE']:kirje_VALUE['nihe_VALUE']+len(Nimi_2)] == Nimi_2.encode() and Nimi_2 not in 공개규약:
                실패들.append('{}:{}: {}'.format(RADA.relative_to(Project_juur), kirje_VALUE['Joon'], Nimi_2))
        LOG_kirje['c_semantic_checked'] = True
        LOG_kirje['c_source_sha256'] = {str(Path(Fail).relative_to(Project_juur)):räsikood_Fail for Fail,räsikood_Fail in Analüüs_VALUE['원문해시'].items()}
    LOG_kirje['passed'] = not 실패들; LOG_kirje['failures'] = 실패들
    sihtkoht_VALUE = Project_juur/'build/verification/naming'; sihtkoht_VALUE.mkdir(parents=True, exist_ok=True)
    (sihtkoht_VALUE/'report.json').write_text(json.dumps(LOG_kirje, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: Eesti deklaratsioon·Fail RADA·호환 kirje_p·통신 예제')

if __name__ == '__main__': Käivita_2()
