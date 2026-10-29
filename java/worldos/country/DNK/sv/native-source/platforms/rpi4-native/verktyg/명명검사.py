#!/usr/bin/env python3
"""명명 klipp·fel_31f743d2·경로를 검사한다. --시언어는 libclang deklaration 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

åtgärd_rot = Path(__file__).resolve().parents[1]
centrallager_rot = åtgärd_rot.parents[1]

def Kör():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--C_Språk', action='store_true')
    argument = parser_48ee4b1b.parse_args()
    실패들 = []
    kontraktsvärde = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    fil_ANTAL = 0
    parameter_tabell = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [centrallager_rot/'compiler/kompilerare.py', centrallager_rot/'compiler/기계어미리번역.py']
    for sökväg_2 in list((åtgärd_rot/'verktyg').glob('*.py')) + list((åtgärd_rot/'예제').rglob('*.py')) + 공용번역기들:
        if sökväg_2.name.endswith(('이름반영.py', '이름분석.py')): continue
        fil_ANTAL += 1
        나무 = ast.parse(sökväg_2.read_text()); 나무들[sökväg_2] = 나무
        for post_värde in ast.walk(나무):
            if isinstance(post_värde, ast.FunctionDef):
                parameter_tabell.setdefault(post_värde.name, set()).update(parameter_argument.arg for parameter_argument in post_värde.args.args + post_värde.args.kwonlyargs)
                if post_värde.args.kwarg: 가변매개함수.add(post_värde.name)
            if isinstance(post_värde, ast.ClassDef):
                for FUNKTION_värde in post_värde.body:
                    if isinstance(FUNKTION_värde, ast.FunctionDef) and FUNKTION_värde.name == '__init__':
                        parameter_tabell.setdefault(post_värde.name, set()).update(parameter_argument.arg for parameter_argument in FUNKTION_värde.args.args + FUNKTION_värde.args.kwonlyargs)
            Namn = ''
            if isinstance(post_värde, (ast.FunctionDef, ast.ClassDef)): Namn = post_värde.name
            elif isinstance(post_värde, ast.Name) and isinstance(post_värde.ctx, ast.Store): Namn = post_värde.id
            elif isinstance(post_värde, ast.arg): Namn = post_värde.arg
            if Namn and Namn not in kontraktsvärde and all(ord(tecken_värde)<128 for tecken_värde in Namn):
                실패들.append('{}:{}: {}'.format(sökväg_2.relative_to(centrallager_rot), post_värde.lineno, Namn))
    for sökväg_2, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Namn = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Namn not in parameter_tabell or Namn in 가변매개함수 or not any(ord(tecken_värde)>127 for tecken_värde in Namn): continue
            for parameter_argument in 호출.keywords:
                if parameter_argument.arg and parameter_argument.arg not in parameter_tabell[Namn]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(sökväg_2.relative_to(centrallager_rot), 호출.lineno, Namn, parameter_argument.arg))
    for inmatningsrad in (åtgärd_rot/'명명/filnamn_mappning.tsv').read_text().splitlines()[1:]:
        Föregående_objekt, aktuellt_objekt, Process_värde_post = inmatningsrad.split('\t')
        if not (åtgärd_rot/aktuellt_objekt).is_file(): 실패들.append('flytta_värde filnamn 없음: '+aktuellt_objekt)
        if Process_värde_post == '호환진입점유지' and not (åtgärd_rot/Föregående_objekt).is_file(): 실패들.append('호환 startpunkt 없음: '+Föregående_objekt)
    예제 = (åtgärd_rot.parents[1]/'example/java/Nätverksexempel.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for sökväg_2 in sorted((åtgärd_rot.parents[1]/'example/java').glob('*.java')):
        källfil = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', sökväg_2.read_text())
        for Namn in re.findall(r'\b[^\W\d]\w*\b', källfil, re.UNICODE):
            if Namn not in 예약어 and all(ord(tecken_värde)<128 for tecken_värde in Namn):
                실패들.append('{}: 예제의 영어 identifierare_värde {}'.format(sökväg_2.name, Namn))
    for Namn in ('Fönster', 'knapp', 'Etikett', 'textfält', 'skärmbild_element', 'händelse_kö', 'arbete', '실행할일', '동작받이', '동작알림', '작업'):
        källfil = (åtgärd_rot/'한국어자바/Svenska/eget'/(Namn+'.java')).read_text()
        källfil = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', källfil)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', källfil):
            실패들.append(Namn+': Svenska 직접 구현에 표준 objekt_värde 래퍼가 남았습니다.')
    시언어예제 = (åtgärd_rot.parents[1]/'example/c/Nätverksexempel.c').read_text()
    for Namn in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Namn in 시언어예제: 실패들.append('C kommunikation 예제에 남은 표준 Namn: '+Namn)
    파이썬예제 = (åtgärd_rot.parents[1]/'example/python/Nätverksexempel.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python kommunikation 예제에 남은 표준 fel_31f743d2 직접 använda_värde')
    머리 = (åtgärd_rot.parents[1]/'posix-kor/arm64-native/deklarationer/통신규약.h').read_text()
    for Namn in ('nät_serie', 'datagramsocket', 'datagram_protokoll', 'socket_ADRESS', 'nät_socket_ADRESS', 'Skapa_deltagare', 'skicka_datagram_data'):
        if re.search(r'^#define\s+'+Namn+r'\b', 머리, re.M): 실패들.append('C 직접 implementation 대신 makro_värde använda_värde: '+Namn)
    자바파일수 = 0
    for rot_värde in ('källfil', 'användarutrymme/자바', '한국어자바'):
        for sökväg_2 in (åtgärd_rot/rot_värde).rglob('*.java'):
            자바파일수 += 1
            källfil = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', sökväg_2.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', källfil):
                실패들.append('{}: 한국어화되지 않은 deklaration {}'.format(sökväg_2.relative_to(åtgärd_rot), 맞음[1]))
            if rot_värde == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', källfil):
                실패들.append('{}: 공개 fel_31f743d2 deklaration'.format(sökväg_2.relative_to(åtgärd_rot)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for sökväg_2 in sorted((centrallager_rot/'os/källfil').glob('*.java')):
        x86자바파일수 += 1
        källfil = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', sökväg_2.read_text())
        for Namn in re.findall(r'\b[^\W\d]\w*\b', källfil, re.UNICODE):
            if Namn not in 예약어 | 표준자바이름 and all(ord(tecken_värde)<128 for tecken_värde in Namn):
                실패들.append('{}: eget 영어 identifierare_värde {}'.format(sökväg_2.relative_to(centrallager_rot), Namn))
    LOG_POST = {'passed': False, 'python_files': fil_ANTAL, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if argument.C_Språk:
        subprocess.check_call(['python3', str(åtgärd_rot/'verktyg/시언어이름분석.py')])
        Analysera_värde = json.loads((åtgärd_rot/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(fel) for fel in Analysera_värde['fel'])
        공개규약 = set(json.loads((åtgärd_rot/'명명/규격이름.json').read_text()))
        for post_värde in Analysera_värde['deklaration'].values():
            Namn = post_värde['Namn']; sökväg_2 = Path(post_värde['filnamn'])
            källfil = sökväg_2.read_bytes()
            # Svenska 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if källfil[post_värde['FÖRSKJUTNING_värde']:post_värde['FÖRSKJUTNING_värde']+len(Namn)] == Namn.encode() and Namn not in 공개규약:
                실패들.append('{}:{}: {}'.format(sökväg_2.relative_to(åtgärd_rot), post_värde['inmatningsrad'], Namn))
        LOG_POST['c_semantic_checked'] = True
        LOG_POST['c_source_sha256'] = {str(Path(filnamn).relative_to(åtgärd_rot)):hash_fil for filnamn,hash_fil in Analysera_värde['원문해시'].items()}
    LOG_POST['passed'] = not 실패들; LOG_POST['failures'] = 실패들
    mål_värde = åtgärd_rot/'build/verification/naming'; mål_värde.mkdir(parents=True, exist_ok=True)
    (mål_värde/'report.json').write_text(json.dumps(LOG_POST, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: Svenska deklaration·filnamn sökväg_2·호환 startpunkt·kommunikation 예제')

if __name__ == '__main__': Kör()
