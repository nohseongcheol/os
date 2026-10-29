#!/usr/bin/env python3
"""명명 obcinać·wyjątek·경로를 검사한다. --시언어는 libclang deklaracja 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

Project_korzeń = Path(__file__).resolve().parents[1]
repozytorium_korzeń = Project_korzeń.parents[1]

def Uruchom_2():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--C_Język', action='store_true')
    argumenty = parser_48ee4b1b.parse_args()
    실패들 = []
    wartość_kontraktu = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    Plik_ILE_LICZB = 0
    parametr_tabela = {}
    ze_zmienną_liczbą_argumentów_FUNKCJA = set()
    나무들 = {}
    공용번역기들 = [repozytorium_korzeń/'compiler/kompilator.py', repozytorium_korzeń/'compiler/기계어미리번역.py']
    for ścieżka_2 in list((Project_korzeń/'narzędzia').glob('*.py')) + list((Project_korzeń/'예제').rglob('*.py')) + 공용번역기들:
        if ścieżka_2.name.endswith(('이름반영.py', '이름분석.py')): continue
        Plik_ILE_LICZB += 1
        나무 = ast.parse(ścieżka_2.read_text()); 나무들[ścieżka_2] = 나무
        for wpis_WARTOŚĆ in ast.walk(나무):
            if isinstance(wpis_WARTOŚĆ, ast.FunctionDef):
                parametr_tabela.setdefault(wpis_WARTOŚĆ.name, set()).update(parametr_argument.arg for parametr_argument in wpis_WARTOŚĆ.args.args + wpis_WARTOŚĆ.args.kwonlyargs)
                if wpis_WARTOŚĆ.args.kwarg: ze_zmienną_liczbą_argumentów_FUNKCJA.add(wpis_WARTOŚĆ.name)
            if isinstance(wpis_WARTOŚĆ, ast.ClassDef):
                for FUNKCJA_WARTOŚĆ in wpis_WARTOŚĆ.body:
                    if isinstance(FUNKCJA_WARTOŚĆ, ast.FunctionDef) and FUNKCJA_WARTOŚĆ.name == '__init__':
                        parametr_tabela.setdefault(wpis_WARTOŚĆ.name, set()).update(parametr_argument.arg for parametr_argument in FUNKCJA_WARTOŚĆ.args.args + FUNKCJA_WARTOŚĆ.args.kwonlyargs)
            Nazwa = ''
            if isinstance(wpis_WARTOŚĆ, (ast.FunctionDef, ast.ClassDef)): Nazwa = wpis_WARTOŚĆ.name
            elif isinstance(wpis_WARTOŚĆ, ast.Name) and isinstance(wpis_WARTOŚĆ.ctx, ast.Store): Nazwa = wpis_WARTOŚĆ.id
            elif isinstance(wpis_WARTOŚĆ, ast.arg): Nazwa = wpis_WARTOŚĆ.arg
            if Nazwa and Nazwa not in wartość_kontraktu and all(ord(znak_WARTOŚĆ)<128 for znak_WARTOŚĆ in Nazwa):
                실패들.append('{}:{}: {}'.format(ścieżka_2.relative_to(repozytorium_korzeń), wpis_WARTOŚĆ.lineno, Nazwa))
    for ścieżka_2, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Nazwa = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Nazwa not in parametr_tabela or Nazwa in ze_zmienną_liczbą_argumentów_FUNKCJA or not any(ord(znak_WARTOŚĆ)>127 for znak_WARTOŚĆ in Nazwa): continue
            for parametr_argument in 호출.keywords:
                if parametr_argument.arg and parametr_argument.arg not in parametr_tabela[Nazwa]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(ścieżka_2.relative_to(repozytorium_korzeń), 호출.lineno, Nazwa, parametr_argument.arg))
    for wiersz_wejścia in (Project_korzeń/'명명/nazwa_pliku_mapowanie.tsv').read_text().splitlines()[1:]:
        Wstecz_towar, bieżący_towar, Proces_WARTOŚĆ_wpis = wiersz_wejścia.split('\t')
        if not (Project_korzeń/bieżący_towar).is_file(): 실패들.append('przenosić_WARTOŚĆ nazwa_pliku 없음: '+bieżący_towar)
        if Proces_WARTOŚĆ_wpis == '호환진입점유지' and not (Project_korzeń/Wstecz_towar).is_file(): 실패들.append('호환 punkt_wejścia 없음: '+Wstecz_towar)
    예제 = (Project_korzeń.parents[1]/'example/java/PrzykładSieci.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for ścieżka_2 in sorted((Project_korzeń.parents[1]/'example/java').glob('*.java')):
        plik_źródłowy = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ścieżka_2.read_text())
        for Nazwa in re.findall(r'\b[^\W\d]\w*\b', plik_źródłowy, re.UNICODE):
            if Nazwa not in 예약어 and all(ord(znak_WARTOŚĆ)<128 for znak_WARTOŚĆ in Nazwa):
                실패들.append('{}: 예제의 영어 identyfikator_WARTOŚĆ {}'.format(ścieżka_2.name, Nazwa))
    for Nazwa in ('Okno', 'przycisk', 'Etykieta', 'pole_tekstowe', '화면구성요소', 'konkurs_kolejka', 'pracownik', '실행할일', '동작받이', 'akcja_powiadomienie', '작업'):
        plik_źródłowy = (Project_korzeń/'한국어자바/polski/własny'/(Nazwa+'.java')).read_text()
        plik_źródłowy = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', plik_źródłowy)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', plik_źródłowy):
            실패들.append(Nazwa+': polski 직접 구현에 표준 obiekt_WARTOŚĆ 래퍼가 남았습니다.')
    시언어예제 = (Project_korzeń.parents[1]/'example/c/PrzykładSieci.c').read_text()
    for Nazwa in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Nazwa in 시언어예제: 실패들.append('C komunikacja 예제에 남은 표준 Nazwa: '+Nazwa)
    파이썬예제 = (Project_korzeń.parents[1]/'example/python/PrzykładSieci.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python komunikacja 예제에 남은 표준 wyjątek 직접 używać_WARTOŚĆ')
    머리 = (Project_korzeń.parents[1]/'posix-kor/arm64-native/deklaracje/sieć_ABI.h').read_text()
    for Nazwa in ('chmura_Rodzina', 'gniazdo_do_przesyłania_datagramów', 'datagram_protokół', 'gniazdo_ADRES', 'chmura_gniazdo_ADRES', 'Twórca_uczestnik', 'wysłać_datagram_dane'):
        if re.search(r'^#define\s+'+Nazwa+r'\b', 머리, re.M): 실패들.append('C 직접 implementacja 대신 makro_WARTOŚĆ używać_WARTOŚĆ: '+Nazwa)
    자바파일수 = 0
    for korzeń_WARTOŚĆ in ('plik_źródłowy', 'przestrzeń_użytkownika/자바', '한국어자바'):
        for ścieżka_2 in (Project_korzeń/korzeń_WARTOŚĆ).rglob('*.java'):
            자바파일수 += 1
            plik_źródłowy = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ścieżka_2.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', plik_źródłowy):
                실패들.append('{}: 한국어화되지 않은 deklaracja {}'.format(ścieżka_2.relative_to(Project_korzeń), 맞음[1]))
            if korzeń_WARTOŚĆ == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', plik_źródłowy):
                실패들.append('{}: 공개 wyjątek deklaracja'.format(ścieżka_2.relative_to(Project_korzeń)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for ścieżka_2 in sorted((repozytorium_korzeń/'os/plik_źródłowy').glob('*.java')):
        x86자바파일수 += 1
        plik_źródłowy = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ścieżka_2.read_text())
        for Nazwa in re.findall(r'\b[^\W\d]\w*\b', plik_źródłowy, re.UNICODE):
            if Nazwa not in 예약어 | 표준자바이름 and all(ord(znak_WARTOŚĆ)<128 for znak_WARTOŚĆ in Nazwa):
                실패들.append('{}: własny 영어 identyfikator_WARTOŚĆ {}'.format(ścieżka_2.relative_to(repozytorium_korzeń), Nazwa))
    LOG_zapis = {'passed': False, 'python_files': Plik_ILE_LICZB, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if argumenty.C_Język:
        subprocess.check_call(['python3', str(Project_korzeń/'narzędzia/시언어이름분석.py')])
        Analiza_WARTOŚĆ = json.loads((Project_korzeń/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(błąd) for błąd in Analiza_WARTOŚĆ['błąd'])
        eksportować_ABI = set(json.loads((Project_korzeń/'명명/규격이름.json').read_text()))
        for wpis_WARTOŚĆ in Analiza_WARTOŚĆ['deklaracja'].values():
            Nazwa = wpis_WARTOŚĆ['Nazwa']; ścieżka_2 = Path(wpis_WARTOŚĆ['nazwa_pliku'])
            plik_źródłowy = ścieżka_2.read_bytes()
            # polski 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if plik_źródłowy[wpis_WARTOŚĆ['przesunąć_WARTOŚĆ_450fc799']:wpis_WARTOŚĆ['przesunąć_WARTOŚĆ_450fc799']+len(Nazwa)] == Nazwa.encode() and Nazwa not in eksportować_ABI:
                실패들.append('{}:{}: {}'.format(ścieżka_2.relative_to(Project_korzeń), wpis_WARTOŚĆ['wiersz_wejścia'], Nazwa))
        LOG_zapis['c_semantic_checked'] = True
        LOG_zapis['c_source_sha256'] = {str(Path(nazwa_pliku).relative_to(Project_korzeń)):skrót_Plik for nazwa_pliku,skrót_Plik in Analiza_WARTOŚĆ['원문해시'].items()}
    LOG_zapis['passed'] = not 실패들; LOG_zapis['failures'] = 실패들
    cel_WARTOŚĆ = Project_korzeń/'build/verification/naming'; cel_WARTOŚĆ.mkdir(parents=True, exist_ok=True)
    (cel_WARTOŚĆ/'report.json').write_text(json.dumps(LOG_zapis, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: polski deklaracja·nazwa_pliku ścieżka_2·호환 punkt_wejścia·komunikacja 예제')

if __name__ == '__main__': Uruchom_2()
