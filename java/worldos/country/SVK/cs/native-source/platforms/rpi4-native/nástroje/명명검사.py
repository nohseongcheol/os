#!/usr/bin/env python3
"""명명 oříznout·výjimka·경로를 검사한다. --시언어는 libclang deklarace_4f4f026b 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

akce_kořen = Path(__file__).resolve().parents[1]
úložiště_kořen = akce_kořen.parents[1]

def Spustit_2():
    analyzátor_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analyzátor_48ee4b1b.add_argument('--C_Jazyk', action='store_true')
    argumenty = analyzátor_48ee4b1b.parse_args()
    실패들 = []
    hodnota_smlouvy = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    Soubor_POČET = 0
    parametr_tabulka = {}
    variadický_funkce = set()
    나무들 = {}
    공용번역기들 = [úložiště_kořen/'compiler/kompilátor.py', úložiště_kořen/'compiler/기계어미리번역.py']
    for cesta_2 in list((akce_kořen/'nástroje').glob('*.py')) + list((akce_kořen/'예제').rglob('*.py')) + 공용번역기들:
        if cesta_2.name.endswith(('이름반영.py', '이름분석.py')): continue
        Soubor_POČET += 1
        나무 = ast.parse(cesta_2.read_text()); 나무들[cesta_2] = 나무
        for položka_HODNOTA in ast.walk(나무):
            if isinstance(položka_HODNOTA, ast.FunctionDef):
                parametr_tabulka.setdefault(položka_HODNOTA.name, set()).update(parametr_argument.arg for parametr_argument in položka_HODNOTA.args.args + položka_HODNOTA.args.kwonlyargs)
                if položka_HODNOTA.args.kwarg: variadický_funkce.add(položka_HODNOTA.name)
            if isinstance(položka_HODNOTA, ast.ClassDef):
                for funkce_HODNOTA in položka_HODNOTA.body:
                    if isinstance(funkce_HODNOTA, ast.FunctionDef) and funkce_HODNOTA.name == '__init__':
                        parametr_tabulka.setdefault(položka_HODNOTA.name, set()).update(parametr_argument.arg for parametr_argument in funkce_HODNOTA.args.args + funkce_HODNOTA.args.kwonlyargs)
            Název = ''
            if isinstance(položka_HODNOTA, (ast.FunctionDef, ast.ClassDef)): Název = položka_HODNOTA.name
            elif isinstance(položka_HODNOTA, ast.Name) and isinstance(položka_HODNOTA.ctx, ast.Store): Název = položka_HODNOTA.id
            elif isinstance(položka_HODNOTA, ast.arg): Název = položka_HODNOTA.arg
            if Název and Název not in hodnota_smlouvy and all(ord(znak_HODNOTA)<128 for znak_HODNOTA in Název):
                실패들.append('{}:{}: {}'.format(cesta_2.relative_to(úložiště_kořen), položka_HODNOTA.lineno, Název))
    for cesta_2, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Název = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Název not in parametr_tabulka or Název in variadický_funkce or not any(ord(znak_HODNOTA)>127 for znak_HODNOTA in Název): continue
            for parametr_argument in 호출.keywords:
                if parametr_argument.arg and parametr_argument.arg not in parametr_tabulka[Název]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(cesta_2.relative_to(úložiště_kořen), 호출.lineno, Název, parametr_argument.arg))
    for vstupní_řádek in (akce_kořen/'명명/파일이름대응.tsv').read_text().splitlines()[1:]:
        Předchozí_zboží, dobrá_zboží, Proces_HODNOTA_položka = vstupní_řádek.split('\t')
        if not (akce_kořen/dobrá_zboží).is_file(): 실패들.append('přesunout_HODNOTA název_souboru 없음: '+dobrá_zboží)
        if Proces_HODNOTA_položka == '호환진입점유지' and not (akce_kořen/Předchozí_zboží).is_file(): 실패들.append('호환 vstupní_bod 없음: '+Předchozí_zboží)
    예제 = (akce_kořen.parents[1]/'example/java/UkázkaSítě.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for cesta_2 in sorted((akce_kořen.parents[1]/'example/java').glob('*.java')):
        zdrojový_soubor = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', cesta_2.read_text())
        for Název in re.findall(r'\b[^\W\d]\w*\b', zdrojový_soubor, re.UNICODE):
            if Název not in 예약어 and all(ord(znak_HODNOTA)<128 for znak_HODNOTA in Název):
                실패들.append('{}: 예제의 영어 identifikátor_HODNOTA {}'.format(cesta_2.name, Název))
    for Název in ('Okno', 'tlačítko', 'Popisek', 'textové_pole', '화면구성요소', 'událost_fronta', 'pracovník', '실행할일', '동작받이', 'Akce_povinnost_zvěřejnit', '작업'):
        zdrojový_soubor = (akce_kořen/'한국어자바/čeština/vlastní'/(Název+'.java')).read_text()
        zdrojový_soubor = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', zdrojový_soubor)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', zdrojový_soubor):
            실패들.append(Název+': čeština 직접 구현에 표준 objekt_HODNOTA 래퍼가 남았습니다.')
    시언어예제 = (akce_kořen.parents[1]/'example/c/UkázkaSítě.c').read_text()
    for Název in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Název in 시언어예제: 실패들.append('C komunikace 예제에 남은 표준 Název: '+Název)
    파이썬예제 = (akce_kořen.parents[1]/'example/python/UkázkaSítě.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python komunikace 예제에 남은 표준 výjimka 직접 použít_HODNOTA')
    머리 = (akce_kořen.parents[1]/'posix-kor/arm64-native/deklarace/síť_ABI.h').read_text()
    for Název in ('cloud_řada', 'datagramový_soket', 'datagram_protokol', 'soket_ODKAZ', 'cloud_soket_ODKAZ', 'Create_účastník', 'poslat_datagram_data'):
        if re.search(r'^#define\s+'+Název+r'\b', 머리, re.M): 실패들.append('C 직접 implementace 대신 makro_HODNOTA použít_HODNOTA: '+Název)
    자바파일수 = 0
    for kořen_HODNOTA in ('zdrojový_soubor', 'uživatelský_prostor/자바', '한국어자바'):
        for cesta_2 in (akce_kořen/kořen_HODNOTA).rglob('*.java'):
            자바파일수 += 1
            zdrojový_soubor = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', cesta_2.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', zdrojový_soubor):
                실패들.append('{}: 한국어화되지 않은 deklarace_4f4f026b {}'.format(cesta_2.relative_to(akce_kořen), 맞음[1]))
            if kořen_HODNOTA == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', zdrojový_soubor):
                실패들.append('{}: 공개 výjimka deklarace_4f4f026b'.format(cesta_2.relative_to(akce_kořen)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for cesta_2 in sorted((úložiště_kořen/'os/zdrojový_soubor').glob('*.java')):
        x86자바파일수 += 1
        zdrojový_soubor = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', cesta_2.read_text())
        for Název in re.findall(r'\b[^\W\d]\w*\b', zdrojový_soubor, re.UNICODE):
            if Název not in 예약어 | 표준자바이름 and all(ord(znak_HODNOTA)<128 for znak_HODNOTA in Název):
                실패들.append('{}: vlastní 영어 identifikátor_HODNOTA {}'.format(cesta_2.relative_to(úložiště_kořen), Název))
    LOGZ_ZÁZNAM = {'passed': False, 'python_files': Soubor_POČET, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if argumenty.C_Jazyk:
        subprocess.check_call(['python3', str(akce_kořen/'nástroje/시언어이름분석.py')])
        Analýza_HODNOTA = json.loads((akce_kořen/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(chyba) for chyba in Analýza_HODNOTA['chyba'])
        exportovat_ABI = set(json.loads((akce_kořen/'명명/규격이름.json').read_text()))
        for položka_HODNOTA in Analýza_HODNOTA['deklarace_4f4f026b'].values():
            Název = položka_HODNOTA['Název']; cesta_2 = Path(položka_HODNOTA['název_souboru'])
            zdrojový_soubor = cesta_2.read_bytes()
            # čeština 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if zdrojový_soubor[položka_HODNOTA['POSUN_HODNOTA']:položka_HODNOTA['POSUN_HODNOTA']+len(Název)] == Název.encode() and Název not in exportovat_ABI:
                실패들.append('{}:{}: {}'.format(cesta_2.relative_to(akce_kořen), položka_HODNOTA['vstupní_řádek'], Název))
        LOGZ_ZÁZNAM['c_semantic_checked'] = True
        LOGZ_ZÁZNAM['c_source_sha256'] = {str(Path(název_souboru).relative_to(akce_kořen)):hodnota_hash_Soubor for název_souboru,hodnota_hash_Soubor in Analýza_HODNOTA['원문해시'].items()}
    LOGZ_ZÁZNAM['passed'] = not 실패들; LOGZ_ZÁZNAM['failures'] = 실패들
    cíl_HODNOTA = akce_kořen/'build/verification/naming'; cíl_HODNOTA.mkdir(parents=True, exist_ok=True)
    (cíl_HODNOTA/'report.json').write_text(json.dumps(LOGZ_ZÁZNAM, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: čeština deklarace_4f4f026b·název_souboru cesta_2·호환 vstupní_bod·komunikace 예제')

if __name__ == '__main__': Spustit_2()
