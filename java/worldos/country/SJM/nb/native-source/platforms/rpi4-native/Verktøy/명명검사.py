#!/usr/bin/env python3
"""명명 klippe·unntak·경로를 검사한다. --시언어는 libclang erklæring 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

speile_rot = Path(__file__).resolve().parents[1]
repositorium_rot = speile_rot.parents[1]

def Kjør_2():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--C_Språk', action='store_true')
    Argumenter = parser_48ee4b1b.parse_args()
    실패들 = []
    kontraktverdi = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    Fil_ANTALL = 0
    parameter_tabell = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [repositorium_rot/'compiler/kompilator.py', repositorium_rot/'compiler/기계어미리번역.py']
    for Sti in list((speile_rot/'Verktøy').glob('*.py')) + list((speile_rot/'예제').rglob('*.py')) + 공용번역기들:
        if Sti.name.endswith(('이름반영.py', '이름분석.py')): continue
        Fil_ANTALL += 1
        나무 = ast.parse(Sti.read_text()); 나무들[Sti] = 나무
        for oppføring_VERDI in ast.walk(나무):
            if isinstance(oppføring_VERDI, ast.FunctionDef):
                parameter_tabell.setdefault(oppføring_VERDI.name, set()).update(parameter_argument.arg for parameter_argument in oppføring_VERDI.args.args + oppføring_VERDI.args.kwonlyargs)
                if oppføring_VERDI.args.kwarg: 가변매개함수.add(oppføring_VERDI.name)
            if isinstance(oppføring_VERDI, ast.ClassDef):
                for FUNKSJON_VERDI in oppføring_VERDI.body:
                    if isinstance(FUNKSJON_VERDI, ast.FunctionDef) and FUNKSJON_VERDI.name == '__init__':
                        parameter_tabell.setdefault(oppføring_VERDI.name, set()).update(parameter_argument.arg for parameter_argument in FUNKSJON_VERDI.args.args + FUNKSJON_VERDI.args.kwonlyargs)
            Navn = ''
            if isinstance(oppføring_VERDI, (ast.FunctionDef, ast.ClassDef)): Navn = oppføring_VERDI.name
            elif isinstance(oppføring_VERDI, ast.Name) and isinstance(oppføring_VERDI.ctx, ast.Store): Navn = oppføring_VERDI.id
            elif isinstance(oppføring_VERDI, ast.arg): Navn = oppføring_VERDI.arg
            if Navn and Navn not in kontraktverdi and all(ord(tegn_VERDI)<128 for tegn_VERDI in Navn):
                실패들.append('{}:{}: {}'.format(Sti.relative_to(repositorium_rot), oppføring_VERDI.lineno, Navn))
    for Sti, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Navn = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Navn not in parameter_tabell or Navn in 가변매개함수 or not any(ord(tegn_VERDI)>127 for tegn_VERDI in Navn): continue
            for parameter_argument in 호출.keywords:
                if parameter_argument.arg and parameter_argument.arg not in parameter_tabell[Navn]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(Sti.relative_to(repositorium_rot), 호출.lineno, Navn, parameter_argument.arg))
    for Linje in (speile_rot/'명명/filnavn_tildeling.tsv').read_text().splitlines()[1:]:
        Forrige_vare, betalt_vare, Prosess_VERDI_oppføring = Linje.split('\t')
        if not (speile_rot/betalt_vare).is_file(): 실패들.append('flytte_VERDI_83b651b8 Fil 없음: '+betalt_vare)
        if Prosess_VERDI_oppføring == '호환진입점유지' and not (speile_rot/Forrige_vare).is_file(): 실패들.append('호환 inngangspunkt 없음: '+Forrige_vare)
    예제 = (speile_rot.parents[1]/'example/java/Nettverkseksempel.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for Sti in sorted((speile_rot.parents[1]/'example/java').glob('*.java')):
        KILDE = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Sti.read_text())
        for Navn in re.findall(r'\b[^\W\d]\w*\b', KILDE, re.UNICODE):
            if Navn not in 예약어 and all(ord(tegn_VERDI)<128 for tegn_VERDI in Navn):
                실패들.append('{}: 예제의 영어 identifikator_VERDI {}'.format(Sti.name, Navn))
    for Navn in ('Vindu', 'Knapp', 'Etikett', 'tekstfelt', 'skjermbilde_element', 'hendelse_kø', 'arbeider', '실행할일', '동작받이', 'Gjøremål_notice', '작업'):
        KILDE = (speile_rot/'한국어자바/norsk/eget'/(Navn+'.java')).read_text()
        KILDE = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', KILDE)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', KILDE):
            실패들.append(Navn+': norsk 직접 구현에 표준 objekt_VERDI 래퍼가 남았습니다.')
    시언어예제 = (speile_rot.parents[1]/'example/c/Nettverkseksempel.c').read_text()
    for Navn in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Navn in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Navn: '+Navn)
    파이썬예제 = (speile_rot.parents[1]/'example/python/Nettverkseksempel.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 unntak 직접 bruk_VERDI')
    머리 = (speile_rot.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Navn in ('sky_serie', 'datagramsocket', 'datagram_protokoll', 'socket_e_post', 'sky_socket_e_post', 'åpne_deltaker', 'sende_datagram_data'):
        if re.search(r'^#define\s+'+Navn+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 makro_VERDI bruk_VERDI: '+Navn)
    자바파일수 = 0
    for rot_VERDI in ('KILDE', 'bruker/자바', '한국어자바'):
        for Sti in (speile_rot/rot_VERDI).rglob('*.java'):
            자바파일수 += 1
            KILDE = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Sti.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', KILDE):
                실패들.append('{}: 한국어화되지 않은 erklæring {}'.format(Sti.relative_to(speile_rot), 맞음[1]))
            if rot_VERDI == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', KILDE):
                실패들.append('{}: 공개 unntak erklæring'.format(Sti.relative_to(speile_rot)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for Sti in sorted((repositorium_rot/'os/KILDE').glob('*.java')):
        x86자바파일수 += 1
        KILDE = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Sti.read_text())
        for Navn in re.findall(r'\b[^\W\d]\w*\b', KILDE, re.UNICODE):
            if Navn not in 예약어 | 표준자바이름 and all(ord(tegn_VERDI)<128 for tegn_VERDI in Navn):
                실패들.append('{}: eget 영어 identifikator_VERDI {}'.format(Sti.relative_to(repositorium_rot), Navn))
    LOG_POST = {'passed': False, 'python_files': Fil_ANTALL, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if Argumenter.C_Språk:
        subprocess.check_call(['python3', str(speile_rot/'Verktøy/시언어이름분석.py')])
        Analyser_VERDI = json.loads((speile_rot/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(feil) for feil in Analyser_VERDI['feil'])
        공개규약 = set(json.loads((speile_rot/'명명/규격이름.json').read_text()))
        for oppføring_VERDI in Analyser_VERDI['erklæring'].values():
            Navn = oppføring_VERDI['Navn']; Sti = Path(oppføring_VERDI['Fil'])
            KILDE = Sti.read_bytes()
            # norsk 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if KILDE[oppføring_VERDI['FORSKYVNING_VERDI']:oppføring_VERDI['FORSKYVNING_VERDI']+len(Navn)] == Navn.encode() and Navn not in 공개규약:
                실패들.append('{}:{}: {}'.format(Sti.relative_to(speile_rot), oppføring_VERDI['Linje'], Navn))
        LOG_POST['c_semantic_checked'] = True
        LOG_POST['c_source_sha256'] = {str(Path(Fil).relative_to(speile_rot)):hash_Fil for Fil,hash_Fil in Analyser_VERDI['원문해시'].items()}
    LOG_POST['passed'] = not 실패들; LOG_POST['failures'] = 실패들
    mål_VERDI = speile_rot/'build/verification/naming'; mål_VERDI.mkdir(parents=True, exist_ok=True)
    (mål_VERDI/'report.json').write_text(json.dumps(LOG_POST, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: norsk erklæring·Fil Sti·호환 inngangspunkt·통신 예제')

if __name__ == '__main__': Kjør_2()
