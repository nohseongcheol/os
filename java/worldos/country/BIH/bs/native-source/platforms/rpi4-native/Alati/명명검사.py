#!/usr/bin/env python3
"""명명 isječak·izuzetak·경로를 검사한다. --시언어는 libclang 선언 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

projicirati_koijen = Path(__file__).resolve().parents[1]
저장소 = projicirati_koijen.parents[1]

def Pokreni():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--시언어', action='store_true')
    Argumenti = 해석기.parse_args()
    실패들 = []
    slučaj_VALUE = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    fajl_COUNT = 0
    parametar_tabela = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [저장소/'compiler/컴파일러.py', 저장소/'compiler/기계어미리번역.py']
    for Putanja in list((projicirati_koijen/'Alati').glob('*.py')) + list((projicirati_koijen/'예제').rglob('*.py')) + 공용번역기들:
        if Putanja.name.endswith(('이름반영.py', '이름분석.py')): continue
        fajl_COUNT += 1
        나무 = ast.parse(Putanja.read_text()); 나무들[Putanja] = 나무
        for unos_VALUE in ast.walk(나무):
            if isinstance(unos_VALUE, ast.FunctionDef):
                parametar_tabela.setdefault(unos_VALUE.name, set()).update(parametar_argument.arg for parametar_argument in unos_VALUE.args.args + unos_VALUE.args.kwonlyargs)
                if unos_VALUE.args.kwarg: 가변매개함수.add(unos_VALUE.name)
            if isinstance(unos_VALUE, ast.ClassDef):
                for FUNCTION_VALUE in unos_VALUE.body:
                    if isinstance(FUNCTION_VALUE, ast.FunctionDef) and FUNCTION_VALUE.name == '__init__':
                        parametar_tabela.setdefault(unos_VALUE.name, set()).update(parametar_argument.arg for parametar_argument in FUNCTION_VALUE.args.args + FUNCTION_VALUE.args.kwonlyargs)
            Naziv = ''
            if isinstance(unos_VALUE, (ast.FunctionDef, ast.ClassDef)): Naziv = unos_VALUE.name
            elif isinstance(unos_VALUE, ast.Name) and isinstance(unos_VALUE.ctx, ast.Store): Naziv = unos_VALUE.id
            elif isinstance(unos_VALUE, ast.arg): Naziv = unos_VALUE.arg
            if Naziv and Naziv not in slučaj_VALUE and all(ord(znak_VALUE)<128 for znak_VALUE in Naziv):
                실패들.append('{}:{}: {}'.format(Putanja.relative_to(저장소), unos_VALUE.lineno, Naziv))
    for Putanja, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Naziv = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Naziv not in parametar_tabela or Naziv in 가변매개함수 or not any(ord(znak_VALUE)>127 for znak_VALUE in Naziv): continue
            for parametar_argument in 호출.keywords:
                if parametar_argument.arg and parametar_argument.arg not in parametar_tabela[Naziv]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(Putanja.relative_to(저장소), 호출.lineno, Naziv, parametar_argument.arg))
    for Linija in (projicirati_koijen/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        이전, trenutno_stavka, proces_VALUE_unos = Linija.split('\t')
        if not (projicirati_koijen/trenutno_stavka).is_file(): 실패들.append('pomaći_VALUE Fajl 없음: '+trenutno_stavka)
        if proces_VALUE_unos == '호환진입점유지' and not (projicirati_koijen/이전).is_file(): 실패들.append('호환 unos_p 없음: '+이전)
    예제 = (projicirati_koijen.parents[1]/'example/java/네트워크예제.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for Putanja in sorted((projicirati_koijen.parents[1]/'example/java').glob('*.java')):
        IZVOR = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Putanja.read_text())
        for Naziv in re.findall(r'\b[^\W\d]\w*\b', IZVOR, re.UNICODE):
            if Naziv not in 예약어 and all(ord(znak_VALUE)<128 for znak_VALUE in Naziv):
                실패들.append('{}: 예제의 영어 identifikator_VALUE {}'.format(Putanja.name, Naziv))
    for Naziv in ('창', 'dugme', 'Oznaka', 'SMS_polje', '화면구성요소', 'događaj_redoslijed', '작업가닥', '실행할일', '동작받이', '동작알림', '작업'):
        IZVOR = (projicirati_koijen/'한국어자바/한국어/자체'/(Naziv+'.java')).read_text()
        IZVOR = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', IZVOR)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', IZVOR):
            실패들.append(Naziv+': 한국어 직접 구현에 표준 objekt_VALUE 래퍼가 남았습니다.')
    시언어예제 = (projicirati_koijen.parents[1]/'example/c/네트워크예제.c').read_text()
    for Naziv in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Naziv in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Naziv: '+Naziv)
    파이썬예제 = (projicirati_koijen.parents[1]/'example/python/네트워크예제.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 izuzetak 직접 사용')
    머리 = (projicirati_koijen.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Naziv in ('oblak_Porodica', '전문통신', '전문전송규약', '통신주소', '인터넷통신주소', 'Create_završna_tačka', '자료전문보내기'):
        if re.search(r'^#define\s+'+Naziv+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 makronaredba_VALUE 사용: '+Naziv)
    자바파일수 = 0
    for koijen_VALUE in ('IZVOR', 'korisnik/자바', '한국어자바'):
        for Putanja in (projicirati_koijen/koijen_VALUE).rglob('*.java'):
            자바파일수 += 1
            IZVOR = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Putanja.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', IZVOR):
                실패들.append('{}: 한국어화되지 않은 선언 {}'.format(Putanja.relative_to(projicirati_koijen), 맞음[1]))
            if koijen_VALUE == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', IZVOR):
                실패들.append('{}: 공개 izuzetak 선언'.format(Putanja.relative_to(projicirati_koijen)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for Putanja in sorted((저장소/'os/IZVOR').glob('*.java')):
        x86자바파일수 += 1
        IZVOR = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Putanja.read_text())
        for Naziv in re.findall(r'\b[^\W\d]\w*\b', IZVOR, re.UNICODE):
            if Naziv not in 예약어 | 표준자바이름 and all(ord(znak_VALUE)<128 for znak_VALUE in Naziv):
                실패들.append('{}: 자체 영어 identifikator_VALUE {}'.format(Putanja.relative_to(저장소), Naziv))
    LOG_red = {'passed': False, 'python_files': fajl_COUNT, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if Argumenti.시언어:
        subprocess.check_call(['python3', str(projicirati_koijen/'Alati/시언어이름분석.py')])
        분석 = json.loads((projicirati_koijen/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(GRESKA) for GRESKA in 분석['GRESKA'])
        공개규약 = set(json.loads((projicirati_koijen/'명명/규격이름.json').read_text()))
        for unos_VALUE in 분석['선언'].values():
            Naziv = unos_VALUE['Naziv']; Putanja = Path(unos_VALUE['Fajl'])
            IZVOR = Putanja.read_bytes()
            # 한국어 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if IZVOR[unos_VALUE['Pomak_VALUE']:unos_VALUE['Pomak_VALUE']+len(Naziv)] == Naziv.encode() and Naziv not in 공개규약:
                실패들.append('{}:{}: {}'.format(Putanja.relative_to(projicirati_koijen), unos_VALUE['Linija'], Naziv))
        LOG_red['c_semantic_checked'] = True
        LOG_red['c_source_sha256'] = {str(Path(Fajl).relative_to(projicirati_koijen)):raspršivanje_fajl for Fajl,raspršivanje_fajl in 분석['원문해시'].items()}
    LOG_red['passed'] = not 실패들; LOG_red['failures'] = 실패들
    odredište_VALUE = projicirati_koijen/'build/verification/naming'; odredište_VALUE.mkdir(parents=True, exist_ok=True)
    (odredište_VALUE/'report.json').write_text(json.dumps(LOG_red, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: 한국어 선언·Fajl Putanja·호환 unos_p·통신 예제')

if __name__ == '__main__': Pokreni()
