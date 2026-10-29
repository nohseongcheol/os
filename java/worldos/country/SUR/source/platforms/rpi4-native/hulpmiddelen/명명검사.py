#!/usr/bin/env python3
"""명명 clip·uitzondering·경로를 검사한다. --시언어는 libclang aangifte 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

Taken_wortel = Path(__file__).resolve().parents[1]
opslagplaats_wortel = Taken_wortel.parents[1]

def starten():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--C_Taal', action='store_true')
    argumenten = parser_48ee4b1b.parse_args()
    실패들 = []
    contractwaarde = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    Bestand_AANTAL = 0
    parameter_tabel = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [opslagplaats_wortel/'compiler/compiler.py', opslagplaats_wortel/'compiler/기계어미리번역.py']
    for pad in list((Taken_wortel/'hulpmiddelen').glob('*.py')) + list((Taken_wortel/'예제').rglob('*.py')) + 공용번역기들:
        if pad.name.endswith(('이름반영.py', '이름분석.py')): continue
        Bestand_AANTAL += 1
        나무 = ast.parse(pad.read_text()); 나무들[pad] = 나무
        for invoer_WAARDE_962f286b in ast.walk(나무):
            if isinstance(invoer_WAARDE_962f286b, ast.FunctionDef):
                parameter_tabel.setdefault(invoer_WAARDE_962f286b.name, set()).update(parameter_argument.arg for parameter_argument in invoer_WAARDE_962f286b.args.args + invoer_WAARDE_962f286b.args.kwonlyargs)
                if invoer_WAARDE_962f286b.args.kwarg: 가변매개함수.add(invoer_WAARDE_962f286b.name)
            if isinstance(invoer_WAARDE_962f286b, ast.ClassDef):
                for FUNCTIE_WAARDE in invoer_WAARDE_962f286b.body:
                    if isinstance(FUNCTIE_WAARDE, ast.FunctionDef) and FUNCTIE_WAARDE.name == '__init__':
                        parameter_tabel.setdefault(invoer_WAARDE_962f286b.name, set()).update(parameter_argument.arg for parameter_argument in FUNCTIE_WAARDE.args.args + FUNCTIE_WAARDE.args.kwonlyargs)
            Naam = ''
            if isinstance(invoer_WAARDE_962f286b, (ast.FunctionDef, ast.ClassDef)): Naam = invoer_WAARDE_962f286b.name
            elif isinstance(invoer_WAARDE_962f286b, ast.Name) and isinstance(invoer_WAARDE_962f286b.ctx, ast.Store): Naam = invoer_WAARDE_962f286b.id
            elif isinstance(invoer_WAARDE_962f286b, ast.arg): Naam = invoer_WAARDE_962f286b.arg
            if Naam and Naam not in contractwaarde and all(ord(teken_WAARDE)<128 for teken_WAARDE in Naam):
                실패들.append('{}:{}: {}'.format(pad.relative_to(opslagplaats_wortel), invoer_WAARDE_962f286b.lineno, Naam))
    for pad, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Naam = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Naam not in parameter_tabel or Naam in 가변매개함수 or not any(ord(teken_WAARDE)>127 for teken_WAARDE in Naam): continue
            for parameter_argument in 호출.keywords:
                if parameter_argument.arg and parameter_argument.arg not in parameter_tabel[Naam]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(pad.relative_to(opslagplaats_wortel), 호출.lineno, Naam, parameter_argument.arg))
    for invoerregel in (Taken_wortel/'명명/bestandsnaam_toewijzing.tsv').read_text().splitlines()[1:]:
        Vorige_item, actueel_item, Proces_WAARDE_invoer = invoerregel.split('\t')
        if not (Taken_wortel/actueel_item).is_file(): 실패들.append('verplaatsen_WAARDE_83b651b8 bestand 없음: '+actueel_item)
        if Proces_WAARDE_invoer == '호환진입점유지' and not (Taken_wortel/Vorige_item).is_file(): 실패들.append('호환 beginpunt 없음: '+Vorige_item)
    예제 = (Taken_wortel.parents[1]/'example/java/Netwerkvoorbeeld.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for pad in sorted((Taken_wortel.parents[1]/'example/java').glob('*.java')):
        broncode = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', pad.read_text())
        for Naam in re.findall(r'\b[^\W\d]\w*\b', broncode, re.UNICODE):
            if Naam not in 예약어 and all(ord(teken_WAARDE)<128 for teken_WAARDE in Naam):
                실패들.append('{}: 예제의 영어 id_WAARDE {}'.format(pad.name, Naam))
    for Naam in ('Venster', 'knop', 'Etiket', 'tekstveld', 'scherm_element', 'gebeurtenis_wachtrij', 'achtergrondwerker', '실행할일', '동작받이', 'Actie_kennisgeving', '작업'):
        broncode = (Taken_wortel/'한국어자바/Nederlands/Eigen'/(Naam+'.java')).read_text()
        broncode = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', broncode)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', broncode):
            실패들.append(Naam+': Nederlands 직접 구현에 표준 object_WAARDE 래퍼가 남았습니다.')
    시언어예제 = (Taken_wortel.parents[1]/'example/c/Netwerkvoorbeeld.c').read_text()
    for Naam in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Naam in 시언어예제: 실패들.append('C communicatie 예제에 남은 표준 Naam: '+Naam)
    파이썬예제 = (Taken_wortel.parents[1]/'example/python/Netwerkvoorbeeld.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python communicatie 예제에 남은 표준 uitzondering 직접 gebruik_WAARDE')
    kop_WAARDE = (Taken_wortel.parents[1]/'posix-kor/arm64-native/declaraties/통신규약.h').read_text()
    for Naam in ('mesh_Gezin', 'datagramsocket', 'datagram_protocol', 'socket_ADRES', 'mesh_socket_ADRES', 'maken_eindpunt', 'e_mailen_datagram_gegevens'):
        if re.search(r'^#define\s+'+Naam+r'\b', kop_WAARDE, re.M): 실패들.append('C 직접 implementatie 대신 macro_WAARDE gebruik_WAARDE: '+Naam)
    자바파일수 = 0
    for wortel_WAARDE in ('broncode', 'gebruikersruimte/자바', '한국어자바'):
        for pad in (Taken_wortel/wortel_WAARDE).rglob('*.java'):
            자바파일수 += 1
            broncode = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', pad.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', broncode):
                실패들.append('{}: 한국어화되지 않은 aangifte {}'.format(pad.relative_to(Taken_wortel), 맞음[1]))
            if wortel_WAARDE == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', broncode):
                실패들.append('{}: 공개 uitzondering aangifte'.format(pad.relative_to(Taken_wortel)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for pad in sorted((opslagplaats_wortel/'os/broncode').glob('*.java')):
        x86자바파일수 += 1
        broncode = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', pad.read_text())
        for Naam in re.findall(r'\b[^\W\d]\w*\b', broncode, re.UNICODE):
            if Naam not in 예약어 | 표준자바이름 and all(ord(teken_WAARDE)<128 for teken_WAARDE in Naam):
                실패들.append('{}: Eigen 영어 id_WAARDE {}'.format(pad.relative_to(opslagplaats_wortel), Naam))
    LOG_RECORD = {'passed': False, 'python_files': Bestand_AANTAL, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if argumenten.C_Taal:
        subprocess.check_call(['python3', str(Taken_wortel/'hulpmiddelen/시언어이름분석.py')])
        Analyseren_WAARDE = json.loads((Taken_wortel/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(fout) for fout in Analyseren_WAARDE['fout'])
        공개규약 = set(json.loads((Taken_wortel/'명명/규격이름.json').read_text()))
        for invoer_WAARDE_962f286b in Analyseren_WAARDE['aangifte'].values():
            Naam = invoer_WAARDE_962f286b['Naam']; pad = Path(invoer_WAARDE_962f286b['bestand'])
            broncode = pad.read_bytes()
            # Nederlands 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if broncode[invoer_WAARDE_962f286b['VERSCHUIVING_WAARDE']:invoer_WAARDE_962f286b['VERSCHUIVING_WAARDE']+len(Naam)] == Naam.encode() and Naam not in 공개규약:
                실패들.append('{}:{}: {}'.format(pad.relative_to(Taken_wortel), invoer_WAARDE_962f286b['invoerregel'], Naam))
        LOG_RECORD['c_semantic_checked'] = True
        LOG_RECORD['c_source_sha256'] = {str(Path(bestand).relative_to(Taken_wortel)):hash_Bestand for bestand,hash_Bestand in Analyseren_WAARDE['원문해시'].items()}
    LOG_RECORD['passed'] = not 실패들; LOG_RECORD['failures'] = 실패들
    doel_WAARDE = Taken_wortel/'build/verification/naming'; doel_WAARDE.mkdir(parents=True, exist_ok=True)
    (doel_WAARDE/'report.json').write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: Nederlands aangifte·bestand pad·호환 beginpunt·communicatie 예제')

if __name__ == '__main__': starten()
