#!/usr/bin/env python3
"""명명 klips·izņēmums·경로를 검사한다. --시언어는 libclang deklarācija 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

Project_sakne = Path(__file__).resolve().parents[1]
repozitorijs_sakne = Project_sakne.parents[1]

def Palaist():
    parsētājs_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parsētājs_48ee4b1b.add_argument('--C_Valodas', action='store_true')
    Parametri = parsētājs_48ee4b1b.parse_args()
    실패들 = []
    līguma_vērtība = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    Fails_COUNT = 0
    parametrs_tabula = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [repozitorijs_sakne/'compiler/kompilators.py', repozitorijs_sakne/'compiler/기계어미리번역.py']
    for CEĻŠ in list((Project_sakne/'Rīki').glob('*.py')) + list((Project_sakne/'예제').rglob('*.py')) + 공용번역기들:
        if CEĻŠ.name.endswith(('이름반영.py', '이름분석.py')): continue
        Fails_COUNT += 1
        나무 = ast.parse(CEĻŠ.read_text()); 나무들[CEĻŠ] = 나무
        for ievade_VALUE in ast.walk(나무):
            if isinstance(ievade_VALUE, ast.FunctionDef):
                parametrs_tabula.setdefault(ievade_VALUE.name, set()).update(parametrs_arg.arg for parametrs_arg in ievade_VALUE.args.args + ievade_VALUE.args.kwonlyargs)
                if ievade_VALUE.args.kwarg: 가변매개함수.add(ievade_VALUE.name)
            if isinstance(ievade_VALUE, ast.ClassDef):
                for FUNCTION_VALUE in ievade_VALUE.body:
                    if isinstance(FUNCTION_VALUE, ast.FunctionDef) and FUNCTION_VALUE.name == '__init__':
                        parametrs_tabula.setdefault(ievade_VALUE.name, set()).update(parametrs_arg.arg for parametrs_arg in FUNCTION_VALUE.args.args + FUNCTION_VALUE.args.kwonlyargs)
            Nosaukums = ''
            if isinstance(ievade_VALUE, (ast.FunctionDef, ast.ClassDef)): Nosaukums = ievade_VALUE.name
            elif isinstance(ievade_VALUE, ast.Name) and isinstance(ievade_VALUE.ctx, ast.Store): Nosaukums = ievade_VALUE.id
            elif isinstance(ievade_VALUE, ast.arg): Nosaukums = ievade_VALUE.arg
            if Nosaukums and Nosaukums not in līguma_vērtība and all(ord(rakstzīme_VALUE)<128 for rakstzīme_VALUE in Nosaukums):
                실패들.append('{}:{}: {}'.format(CEĻŠ.relative_to(repozitorijs_sakne), ievade_VALUE.lineno, Nosaukums))
    for CEĻŠ, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Nosaukums = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Nosaukums not in parametrs_tabula or Nosaukums in 가변매개함수 or not any(ord(rakstzīme_VALUE)>127 for rakstzīme_VALUE in Nosaukums): continue
            for parametrs_arg in 호출.keywords:
                if parametrs_arg.arg and parametrs_arg.arg not in parametrs_tabula[Nosaukums]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(CEĻŠ.relative_to(repozitorijs_sakne), 호출.lineno, Nosaukums, parametrs_arg.arg))
    for Līniju in (Project_sakne/'명명/faila_nosaukums_kartēšana.tsv').read_text().splitlines()[1:]:
        이전, pašreizējais_krājums, Process_VALUE_ievade = Līniju.split('\t')
        if not (Project_sakne/pašreizējais_krājums).is_file(): 실패들.append('pārvietot_VALUE Fails 없음: '+pašreizējais_krājums)
        if Process_VALUE_ievade == '호환진입점유지' and not (Project_sakne/이전).is_file(): 실패들.append('호환 ieejas_punkts 없음: '+이전)
    예제 = (Project_sakne.parents[1]/'example/java/TīklaPiemērs.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for CEĻŠ in sorted((Project_sakne.parents[1]/'example/java').glob('*.java')):
        AVOTS = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', CEĻŠ.read_text())
        for Nosaukums in re.findall(r'\b[^\W\d]\w*\b', AVOTS, re.UNICODE):
            if Nosaukums not in 예약어 and all(ord(rakstzīme_VALUE)<128 for rakstzīme_VALUE in Nosaukums):
                실패들.append('{}: 예제의 영어 identifikators_VALUE {}'.format(CEĻŠ.name, Nosaukums))
    for Nosaukums in ('Logs', 'Pogas', 'Etiķete', 'teksta_lauks', '화면구성요소', 'notikums_rinda', 'nodarbinātais', '실행할일', '동작받이', 'darbība_informēšana', '작업'):
        AVOTS = (Project_sakne/'한국어자바/Latviešu/savs'/(Nosaukums+'.java')).read_text()
        AVOTS = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', AVOTS)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', AVOTS):
            실패들.append(Nosaukums+': Latviešu 직접 구현에 표준 objekts_VALUE 래퍼가 남았습니다.')
    시언어예제 = (Project_sakne.parents[1]/'example/c/TīklaPiemērs.c').read_text()
    for Nosaukums in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Nosaukums in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Nosaukums: '+Nosaukums)
    파이썬예제 = (Project_sakne.parents[1]/'example/python/TīklaPiemērs.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 izņēmums 직접 lietot_VALUE')
    머리 = (Project_sakne.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Nosaukums in ('mākonis_saime', 'datogrammas_ligzda', 'datogramma_protokols', '통신주소', '인터넷통신주소', 'atvērt_dalībnieks', 'sūtīt_datogramma_dati'):
        if re.search(r'^#define\s+'+Nosaukums+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 makro_VALUE lietot_VALUE: '+Nosaukums)
    자바파일수 = 0
    for sakne_VALUE in ('AVOTS', 'lietotājs/자바', '한국어자바'):
        for CEĻŠ in (Project_sakne/sakne_VALUE).rglob('*.java'):
            자바파일수 += 1
            AVOTS = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', CEĻŠ.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', AVOTS):
                실패들.append('{}: 한국어화되지 않은 deklarācija {}'.format(CEĻŠ.relative_to(Project_sakne), 맞음[1]))
            if sakne_VALUE == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', AVOTS):
                실패들.append('{}: 공개 izņēmums deklarācija'.format(CEĻŠ.relative_to(Project_sakne)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for CEĻŠ in sorted((repozitorijs_sakne/'os/AVOTS').glob('*.java')):
        x86자바파일수 += 1
        AVOTS = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', CEĻŠ.read_text())
        for Nosaukums in re.findall(r'\b[^\W\d]\w*\b', AVOTS, re.UNICODE):
            if Nosaukums not in 예약어 | 표준자바이름 and all(ord(rakstzīme_VALUE)<128 for rakstzīme_VALUE in Nosaukums):
                실패들.append('{}: savs 영어 identifikators_VALUE {}'.format(CEĻŠ.relative_to(repozitorijs_sakne), Nosaukums))
    LOG_RECORD = {'passed': False, 'python_files': Fails_COUNT, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if Parametri.C_Valodas:
        subprocess.check_call(['python3', str(Project_sakne/'Rīki/시언어이름분석.py')])
        analīze_VALUE = json.loads((Project_sakne/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(Kļūda) for Kļūda in analīze_VALUE['Kļūda'])
        공개규약 = set(json.loads((Project_sakne/'명명/규격이름.json').read_text()))
        for ievade_VALUE in analīze_VALUE['deklarācija'].values():
            Nosaukums = ievade_VALUE['Nosaukums']; CEĻŠ = Path(ievade_VALUE['Fails'])
            AVOTS = CEĻŠ.read_bytes()
            # Latviešu 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if AVOTS[ievade_VALUE['Nobīde_VALUE']:ievade_VALUE['Nobīde_VALUE']+len(Nosaukums)] == Nosaukums.encode() and Nosaukums not in 공개규약:
                실패들.append('{}:{}: {}'.format(CEĻŠ.relative_to(Project_sakne), ievade_VALUE['Līniju'], Nosaukums))
        LOG_RECORD['c_semantic_checked'] = True
        LOG_RECORD['c_source_sha256'] = {str(Path(Fails).relative_to(Project_sakne)):jaukšana_Fails for Fails,jaukšana_Fails in analīze_VALUE['원문해시'].items()}
    LOG_RECORD['passed'] = not 실패들; LOG_RECORD['failures'] = 실패들
    mērķis_VALUE = Project_sakne/'build/verification/naming'; mērķis_VALUE.mkdir(parents=True, exist_ok=True)
    (mērķis_VALUE/'report.json').write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: Latviešu deklarācija·Fails CEĻŠ·호환 ieejas_punkts·통신 예제')

if __name__ == '__main__': Palaist()
