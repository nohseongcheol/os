#!/usr/bin/env python3
"""명명 klip·salbuespen·경로를 검사한다. --시언어는 libclang deklarazio 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

Project_erro = Path(__file__).resolve().parents[1]
biltegi_erro = Project_erro.parents[1]

def Exekutatu_2():
    analizatzaile_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizatzaile_48ee4b1b.add_argument('--시언어', action='store_true')
    Argumentuak = analizatzaile_48ee4b1b.parse_args()
    실패들 = []
    kasu_balio = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    fitxategi_ZENBATU = 0
    parametro_taula = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [biltegi_erro/'compiler/컴파일러.py', biltegi_erro/'compiler/기계어미리번역.py']
    for Bide_izena in list((Project_erro/'Tresnak').glob('*.py')) + list((Project_erro/'예제').rglob('*.py')) + 공용번역기들:
        if Bide_izena.name.endswith(('이름반영.py', '이름분석.py')): continue
        fitxategi_ZENBATU += 1
        나무 = ast.parse(Bide_izena.read_text()); 나무들[Bide_izena] = 나무
        for sarrera_balio in ast.walk(나무):
            if isinstance(sarrera_balio, ast.FunctionDef):
                parametro_taula.setdefault(sarrera_balio.name, set()).update(parametro_arg.arg for parametro_arg in sarrera_balio.args.args + sarrera_balio.args.kwonlyargs)
                if sarrera_balio.args.kwarg: 가변매개함수.add(sarrera_balio.name)
            if isinstance(sarrera_balio, ast.ClassDef):
                for FUNTZIOA_balio in sarrera_balio.body:
                    if isinstance(FUNTZIOA_balio, ast.FunctionDef) and FUNTZIOA_balio.name == '__init__':
                        parametro_taula.setdefault(sarrera_balio.name, set()).update(parametro_arg.arg for parametro_arg in FUNTZIOA_balio.args.args + FUNTZIOA_balio.args.kwonlyargs)
            Izena = ''
            if isinstance(sarrera_balio, (ast.FunctionDef, ast.ClassDef)): Izena = sarrera_balio.name
            elif isinstance(sarrera_balio, ast.Name) and isinstance(sarrera_balio.ctx, ast.Store): Izena = sarrera_balio.id
            elif isinstance(sarrera_balio, ast.arg): Izena = sarrera_balio.arg
            if Izena and Izena not in kasu_balio and all(ord(karaktere_balio)<128 for karaktere_balio in Izena):
                실패들.append('{}:{}: {}'.format(Bide_izena.relative_to(biltegi_erro), sarrera_balio.lineno, Izena))
    for Bide_izena, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Izena = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Izena not in parametro_taula or Izena in 가변매개함수 or not any(ord(karaktere_balio)>127 for karaktere_balio in Izena): continue
            for parametro_arg in 호출.keywords:
                if parametro_arg.arg and parametro_arg.arg not in parametro_taula[Izena]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(Bide_izena.relative_to(biltegi_erro), 호출.lineno, Izena, parametro_arg.arg))
    for Marra in (Project_erro/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, 현재, prozesu_balio_sarrera = Marra.split('\t')
        if not (Project_erro/현재).is_file(): 실패들.append('eraman_balio Fitxategia 없음: '+현재)
        if prozesu_balio_sarrera == '호환진입점유지' and not (Project_erro/이전).is_file(): 실패들.append('호환 sarrera_p 없음: '+이전)
    예제 = (Project_erro.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for Bide_izena in sorted((Project_erro.parents[1]/'example/java').glob('*.java')):
        ITURBURUA = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Bide_izena.read_text())
        for Izena in re.findall(r'\b[^\W\d]\w*\b', ITURBURUA, re.UNICODE):
            if Izena not in 예약어 and all(ord(karaktere_balio)<128 for karaktere_balio in Izena):
                실패들.append('{}: 예제의 영어 identifikatzaile_balio {}'.format(Bide_izena.name, Izena))
    for Izena in ('Leihoa', 'botoia', 'Etiketa', 'SMS_eremu', '화면구성요소', 'gertaera_ilara', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        ITURBURUA = (Project_erro/'한국어자바/Euskara/자체'/(Izena+'.java')).read_text()
        ITURBURUA = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', ITURBURUA)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', ITURBURUA):
            실패들.append(Izena+': Euskara 직접 구현에 표준 objektu_balio 래퍼가 남았습니다.')
    시언어예제 = (Project_erro.parents[1]/'example/c/네트워크예제.c').read_text()
    for Izena in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Izena in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Izena: '+Izena)
    파이썬예제 = (Project_erro.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 salbuespen 직접 사용')
    머리 = (Project_erro.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Izena in ('hodei_sorta', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', 'sortu_amaiera_puntu', '자료전문보내기'):
        if re.search(r'^#define\s+'+Izena+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 makro_balio 사용: '+Izena)
    자바파일수 = 0
    for erro_balio in ('ITURBURUA', 'erabiltzaile/자바', '한국어자바'):
        for Bide_izena in (Project_erro/erro_balio).rglob('*.java'):
            자바파일수 += 1
            ITURBURUA = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Bide_izena.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', ITURBURUA):
                실패들.append('{}: 한국어화되지 않은 deklarazio {}'.format(Bide_izena.relative_to(Project_erro), 맞음[1]))
            if erro_balio == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', ITURBURUA):
                실패들.append('{}: 공개 salbuespen deklarazio'.format(Bide_izena.relative_to(Project_erro)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for Bide_izena in sorted((biltegi_erro/'os/ITURBURUA').glob('*.java')):
        x86자바파일수 += 1
        ITURBURUA = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Bide_izena.read_text())
        for Izena in re.findall(r'\b[^\W\d]\w*\b', ITURBURUA, re.UNICODE):
            if Izena not in 예약어 | 표준자바이름 and all(ord(karaktere_balio)<128 for karaktere_balio in Izena):
                실패들.append('{}: 자체 영어 identifikatzaile_balio {}'.format(Bide_izena.relative_to(biltegi_erro), Izena))
    LOG_marka = {'passed': False, 'python_files': fitxategi_ZENBATU, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if Argumentuak.시언어:
        subprocess.check_call(['python3', str(Project_erro/'Tresnak/시언어이름분석.py')])
        Analizatu_balio = json.loads((Project_erro/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(errorea) for errorea in Analizatu_balio['errorea'])
        공개규약 = set(json.loads((Project_erro/'명명/규격이름.json').read_text()))
        for sarrera_balio in Analizatu_balio['deklarazio'].values():
            Izena = sarrera_balio['Izena']; Bide_izena = Path(sarrera_balio['Fitxategia'])
            ITURBURUA = Bide_izena.read_bytes()
            # Euskara 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if ITURBURUA[sarrera_balio['Geruzak_balio']:sarrera_balio['Geruzak_balio']+len(Izena)] == Izena.encode() and Izena not in 공개규약:
                실패들.append('{}:{}: {}'.format(Bide_izena.relative_to(Project_erro), sarrera_balio['Marra'], Izena))
        LOG_marka['c_semantic_checked'] = True
        LOG_marka['c_source_sha256'] = {str(Path(Fitxategia).relative_to(Project_erro)):hash_fitxategi for Fitxategia,hash_fitxategi in Analizatu_balio['원문해시'].items()}
    LOG_marka['passed'] = not 실패들; LOG_marka['failures'] = 실패들
    helburu_balio_a0fbc067 = Project_erro/'build/verification/naming'; helburu_balio_a0fbc067.mkdir(parents=True, exist_ok=True)
    (helburu_balio_a0fbc067/'report.json').write_text(json.dumps(LOG_marka, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: Euskara deklarazio·Fitxategia Bide_izena·호환 sarrera_p·통신 예제')

if __name__ == '__main__': Exekutatu_2()
