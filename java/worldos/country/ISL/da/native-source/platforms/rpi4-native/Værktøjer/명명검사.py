#!/usr/bin/env python3
"""명명 klippe·undtagelse·경로를 검사한다. --시언어는 libclang erklæring 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

To_do_rod = Path(__file__).resolve().parents[1]
lager_rod = To_do_rod.parents[1]

def Kør_2():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--C_Sprog', action='store_true')
    Argumenter = parser_48ee4b1b.parse_args()
    실패들 = []
    kontraktværdi = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    fil_TÆL = 0
    parameter_tabel = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [lager_rod/'compiler/compiler.py', lager_rod/'compiler/기계어미리번역.py']
    for Sti in list((To_do_rod/'Værktøjer').glob('*.py')) + list((To_do_rod/'예제').rglob('*.py')) + 공용번역기들:
        if Sti.name.endswith(('이름반영.py', '이름분석.py')): continue
        fil_TÆL += 1
        나무 = ast.parse(Sti.read_text()); 나무들[Sti] = 나무
        for post_VÆRDI_962f286b in ast.walk(나무):
            if isinstance(post_VÆRDI_962f286b, ast.FunctionDef):
                parameter_tabel.setdefault(post_VÆRDI_962f286b.name, set()).update(parameter_argument.arg for parameter_argument in post_VÆRDI_962f286b.args.args + post_VÆRDI_962f286b.args.kwonlyargs)
                if post_VÆRDI_962f286b.args.kwarg: 가변매개함수.add(post_VÆRDI_962f286b.name)
            if isinstance(post_VÆRDI_962f286b, ast.ClassDef):
                for FUNKTION_VÆRDI in post_VÆRDI_962f286b.body:
                    if isinstance(FUNKTION_VÆRDI, ast.FunctionDef) and FUNKTION_VÆRDI.name == '__init__':
                        parameter_tabel.setdefault(post_VÆRDI_962f286b.name, set()).update(parameter_argument.arg for parameter_argument in FUNKTION_VÆRDI.args.args + FUNKTION_VÆRDI.args.kwonlyargs)
            Navn = ''
            if isinstance(post_VÆRDI_962f286b, (ast.FunctionDef, ast.ClassDef)): Navn = post_VÆRDI_962f286b.name
            elif isinstance(post_VÆRDI_962f286b, ast.Name) and isinstance(post_VÆRDI_962f286b.ctx, ast.Store): Navn = post_VÆRDI_962f286b.id
            elif isinstance(post_VÆRDI_962f286b, ast.arg): Navn = post_VÆRDI_962f286b.arg
            if Navn and Navn not in kontraktværdi and all(ord(tegn_VÆRDI)<128 for tegn_VÆRDI in Navn):
                실패들.append('{}:{}: {}'.format(Sti.relative_to(lager_rod), post_VÆRDI_962f286b.lineno, Navn))
    for Sti, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Navn = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Navn not in parameter_tabel or Navn in 가변매개함수 or not any(ord(tegn_VÆRDI)>127 for tegn_VÆRDI in Navn): continue
            for parameter_argument in 호출.keywords:
                if parameter_argument.arg and parameter_argument.arg not in parameter_tabel[Navn]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(Sti.relative_to(lager_rod), 호출.lineno, Navn, parameter_argument.arg))
    for Linje in (To_do_rod/'명명/filnavn_tilknytning.tsv').read_text().splitlines()[1:]:
        Forrige_vare, aktuel_vare, Proces_VÆRDI_post = Linje.split('\t')
        if not (To_do_rod/aktuel_vare).is_file(): 실패들.append('flytte_VÆRDI_83b651b8 Fil 없음: '+aktuel_vare)
        if Proces_VÆRDI_post == '호환진입점유지' and not (To_do_rod/Forrige_vare).is_file(): 실패들.append('호환 indgangspunkt 없음: '+Forrige_vare)
    예제 = (To_do_rod.parents[1]/'example/java/Netværkseksempel.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for Sti in sorted((To_do_rod.parents[1]/'example/java').glob('*.java')):
        KILDE = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Sti.read_text())
        for Navn in re.findall(r'\b[^\W\d]\w*\b', KILDE, re.UNICODE):
            if Navn not in 예약어 and all(ord(tegn_VÆRDI)<128 for tegn_VÆRDI in Navn):
                실패들.append('{}: 예제의 영어 identifikator_VÆRDI {}'.format(Sti.name, Navn))
    for Navn in ('Vindue', 'knap', 'Etiket', 'tekstfelt', 'skærmbillede_element', 'hændelse_kø', 'arbejder', '실행할일', '동작받이', '동작알림', '작업'):
        KILDE = (To_do_rod/'한국어자바/Dansk/eget'/(Navn+'.java')).read_text()
        KILDE = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', KILDE)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', KILDE):
            실패들.append(Navn+': Dansk 직접 구현에 표준 objekt_VÆRDI 래퍼가 남았습니다.')
    시언어예제 = (To_do_rod.parents[1]/'example/c/Netværkseksempel.c').read_text()
    for Navn in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Navn in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Navn: '+Navn)
    파이썬예제 = (To_do_rod.parents[1]/'example/python/Netværkseksempel.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 undtagelse 직접 brug_VÆRDI')
    머리 = (To_do_rod.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Navn in ('net_serie', 'datagram_socket', 'datagram_protokol', 'socket_mail', 'net_socket_mail', 'åbne_slutpunkt', 'maile_datagram_data'):
        if re.search(r'^#define\s+'+Navn+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 makro_VÆRDI brug_VÆRDI: '+Navn)
    자바파일수 = 0
    for rod_VÆRDI in ('KILDE', 'bruger/자바', '한국어자바'):
        for Sti in (To_do_rod/rod_VÆRDI).rglob('*.java'):
            자바파일수 += 1
            KILDE = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Sti.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', KILDE):
                실패들.append('{}: 한국어화되지 않은 erklæring {}'.format(Sti.relative_to(To_do_rod), 맞음[1]))
            if rod_VÆRDI == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', KILDE):
                실패들.append('{}: 공개 undtagelse erklæring'.format(Sti.relative_to(To_do_rod)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for Sti in sorted((lager_rod/'os/KILDE').glob('*.java')):
        x86자바파일수 += 1
        KILDE = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Sti.read_text())
        for Navn in re.findall(r'\b[^\W\d]\w*\b', KILDE, re.UNICODE):
            if Navn not in 예약어 | 표준자바이름 and all(ord(tegn_VÆRDI)<128 for tegn_VÆRDI in Navn):
                실패들.append('{}: eget 영어 identifikator_VÆRDI {}'.format(Sti.relative_to(lager_rod), Navn))
    LOG_post = {'passed': False, 'python_files': fil_TÆL, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if Argumenter.C_Sprog:
        subprocess.check_call(['python3', str(To_do_rod/'Værktøjer/시언어이름분석.py')])
        Analyse_VÆRDI = json.loads((To_do_rod/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(fejl) for fejl in Analyse_VÆRDI['fejl'])
        공개규약 = set(json.loads((To_do_rod/'명명/규격이름.json').read_text()))
        for post_VÆRDI_962f286b in Analyse_VÆRDI['erklæring'].values():
            Navn = post_VÆRDI_962f286b['Navn']; Sti = Path(post_VÆRDI_962f286b['Fil'])
            KILDE = Sti.read_bytes()
            # Dansk 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if KILDE[post_VÆRDI_962f286b['FORSKYDNING_VÆRDI']:post_VÆRDI_962f286b['FORSKYDNING_VÆRDI']+len(Navn)] == Navn.encode() and Navn not in 공개규약:
                실패들.append('{}:{}: {}'.format(Sti.relative_to(To_do_rod), post_VÆRDI_962f286b['Linje'], Navn))
        LOG_post['c_semantic_checked'] = True
        LOG_post['c_source_sha256'] = {str(Path(Fil).relative_to(To_do_rod)):hash_fil for Fil,hash_fil in Analyse_VÆRDI['원문해시'].items()}
    LOG_post['passed'] = not 실패들; LOG_post['failures'] = 실패들
    destination_VÆRDI = To_do_rod/'build/verification/naming'; destination_VÆRDI.mkdir(parents=True, exist_ok=True)
    (destination_VÆRDI/'report.json').write_text(json.dumps(LOG_post, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: Dansk erklæring·Fil Sti·호환 indgangspunkt·통신 예제')

if __name__ == '__main__': Kør_2()
