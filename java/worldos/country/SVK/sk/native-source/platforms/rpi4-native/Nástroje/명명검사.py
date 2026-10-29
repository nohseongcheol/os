#!/usr/bin/env python3
"""명명 klip·výnimka·경로를 검사한다. --시언어는 libclang deklarácia 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

akcia_koreň = Path(__file__).resolve().parents[1]
odkladací_priestor_koreň = akcia_koreň.parents[1]

def Spustiť_2():
    analyzátor_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analyzátor_48ee4b1b.add_argument('--C_Jazyky', action='store_true')
    Argumenty = analyzátor_48ee4b1b.parse_args()
    실패들 = []
    prípad_VALUE = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    Súbor_COUNT = 0
    parameter_tabuľka = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [odkladací_priestor_koreň/'compiler/kompilátor.py', odkladací_priestor_koreň/'compiler/기계어미리번역.py']
    for Cesta in list((akcia_koreň/'Nástroje').glob('*.py')) + list((akcia_koreň/'예제').rglob('*.py')) + 공용번역기들:
        if Cesta.name.endswith(('이름반영.py', '이름분석.py')): continue
        Súbor_COUNT += 1
        나무 = ast.parse(Cesta.read_text()); 나무들[Cesta] = 나무
        for položka_VALUE in ast.walk(나무):
            if isinstance(položka_VALUE, ast.FunctionDef):
                parameter_tabuľka.setdefault(položka_VALUE.name, set()).update(parameter_argument.arg for parameter_argument in položka_VALUE.args.args + položka_VALUE.args.kwonlyargs)
                if položka_VALUE.args.kwarg: 가변매개함수.add(položka_VALUE.name)
            if isinstance(položka_VALUE, ast.ClassDef):
                for funkcia_VALUE in položka_VALUE.body:
                    if isinstance(funkcia_VALUE, ast.FunctionDef) and funkcia_VALUE.name == '__init__':
                        parameter_tabuľka.setdefault(položka_VALUE.name, set()).update(parameter_argument.arg for parameter_argument in funkcia_VALUE.args.args + funkcia_VALUE.args.kwonlyargs)
            Názov = ''
            if isinstance(položka_VALUE, (ast.FunctionDef, ast.ClassDef)): Názov = položka_VALUE.name
            elif isinstance(položka_VALUE, ast.Name) and isinstance(položka_VALUE.ctx, ast.Store): Názov = položka_VALUE.id
            elif isinstance(položka_VALUE, ast.arg): Názov = položka_VALUE.arg
            if Názov and Názov not in prípad_VALUE and all(ord(znak_VALUE)<128 for znak_VALUE in Názov):
                실패들.append('{}:{}: {}'.format(Cesta.relative_to(odkladací_priestor_koreň), položka_VALUE.lineno, Názov))
    for Cesta, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Názov = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Názov not in parameter_tabuľka or Názov in 가변매개함수 or not any(ord(znak_VALUE)>127 for znak_VALUE in Názov): continue
            for parameter_argument in 호출.keywords:
                if parameter_argument.arg and parameter_argument.arg not in parameter_tabuľka[Názov]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(Cesta.relative_to(odkladací_priestor_koreň), 호출.lineno, Názov, parameter_argument.arg))
    for riadok in (akcia_koreň/'명명/názov_súboru_mapovanie.tsv').read_text().splitlines()[1:]:
        이전, v_termíne_splatnosti_položka, Proces_VALUE_položka = riadok.split('\t')
        if not (akcia_koreň/v_termíne_splatnosti_položka).is_file(): 실패들.append('premiestniť_VALUE Súbor 없음: '+v_termíne_splatnosti_položka)
        if Proces_VALUE_položka == '호환진입점유지' and not (akcia_koreň/이전).is_file(): 실패들.append('호환 položka_bod 없음: '+이전)
    예제 = (akcia_koreň.parents[1]/'example/java/UkážkaSiete.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for Cesta in sorted((akcia_koreň.parents[1]/'example/java').glob('*.java')):
        ZDROJ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Cesta.read_text())
        for Názov in re.findall(r'\b[^\W\d]\w*\b', ZDROJ, re.UNICODE):
            if Názov not in 예약어 and all(ord(znak_VALUE)<128 for znak_VALUE in Názov):
                실패들.append('{}: 예제의 영어 identifikátor_VALUE {}'.format(Cesta.name, Názov))
    for Názov in ('Okno', 'Tlačidlo', 'Nápis', 'textové_pole', '화면구성요소', 'udalosť_front', '작업가닥', '실행할일', '동작받이', 'Akcia_upozornenie', '작업'):
        ZDROJ = (akcia_koreň/'한국어자바/Slovenský/vlastné'/(Názov+'.java')).read_text()
        ZDROJ = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', ZDROJ)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', ZDROJ):
            실패들.append(Názov+': Slovenský 직접 구현에 표준 objekt_VALUE 래퍼가 남았습니다.')
    시언어예제 = (akcia_koreň.parents[1]/'example/c/UkážkaSiete.c').read_text()
    for Názov in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Názov in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Názov: '+Názov)
    파이썬예제 = (akcia_koreň.parents[1]/'example/python/UkážkaSiete.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 výnimka 직접 používať_VALUE')
    머리 = (akcia_koreň.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Názov in ('cloud_séria', 'datagramový_soket', 'datagram_protokol', 'soket_adresa', 'cloud_soket_adresa', 'Create_účastník', 'odoslať_datagram_údaje'):
        if re.search(r'^#define\s+'+Názov+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 makro_VALUE používať_VALUE: '+Názov)
    자바파일수 = 0
    for koreň_VALUE in ('ZDROJ', 'používateľ/자바', '한국어자바'):
        for Cesta in (akcia_koreň/koreň_VALUE).rglob('*.java'):
            자바파일수 += 1
            ZDROJ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Cesta.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', ZDROJ):
                실패들.append('{}: 한국어화되지 않은 deklarácia {}'.format(Cesta.relative_to(akcia_koreň), 맞음[1]))
            if koreň_VALUE == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', ZDROJ):
                실패들.append('{}: 공개 výnimka deklarácia'.format(Cesta.relative_to(akcia_koreň)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for Cesta in sorted((odkladací_priestor_koreň/'os/ZDROJ').glob('*.java')):
        x86자바파일수 += 1
        ZDROJ = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', Cesta.read_text())
        for Názov in re.findall(r'\b[^\W\d]\w*\b', ZDROJ, re.UNICODE):
            if Názov not in 예약어 | 표준자바이름 and all(ord(znak_VALUE)<128 for znak_VALUE in Názov):
                실패들.append('{}: vlastné 영어 identifikátor_VALUE {}'.format(Cesta.relative_to(odkladací_priestor_koreň), Názov))
    LOG_RECORD = {'passed': False, 'python_files': Súbor_COUNT, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if Argumenty.C_Jazyky:
        subprocess.check_call(['python3', str(akcia_koreň/'Nástroje/시언어이름분석.py')])
        Analýza_VALUE = json.loads((akcia_koreň/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(chyba) for chyba in Analýza_VALUE['chyba'])
        공개규약 = set(json.loads((akcia_koreň/'명명/규격이름.json').read_text()))
        for položka_VALUE in Analýza_VALUE['deklarácia'].values():
            Názov = položka_VALUE['Názov']; Cesta = Path(položka_VALUE['Súbor'])
            ZDROJ = Cesta.read_bytes()
            # Slovenský 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if ZDROJ[položka_VALUE['Posun_VALUE']:položka_VALUE['Posun_VALUE']+len(Názov)] == Názov.encode() and Názov not in 공개규약:
                실패들.append('{}:{}: {}'.format(Cesta.relative_to(akcia_koreň), položka_VALUE['riadok'], Názov))
        LOG_RECORD['c_semantic_checked'] = True
        LOG_RECORD['c_source_sha256'] = {str(Path(Súbor).relative_to(akcia_koreň)):hodnota_hash_Súbor for Súbor,hodnota_hash_Súbor in Analýza_VALUE['원문해시'].items()}
    LOG_RECORD['passed'] = not 실패들; LOG_RECORD['failures'] = 실패들
    cieľ_VALUE = akcia_koreň/'build/verification/naming'; cieľ_VALUE.mkdir(parents=True, exist_ok=True)
    (cieľ_VALUE/'report.json').write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: Slovenský deklarácia·Súbor Cesta·호환 položka_bod·통신 예제')

if __name__ == '__main__': Spustiť_2()
