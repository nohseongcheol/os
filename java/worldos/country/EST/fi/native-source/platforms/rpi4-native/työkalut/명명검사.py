#!/usr/bin/env python3
"""명명 leikata·poikkeus·경로를 검사한다. --시언어는 libclang esittely 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

aloite_juuri = Path(__file__).resolve().parents[1]
säilö_juuri = aloite_juuri.parents[1]

def Suorita_2():
    jäsennin_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    jäsennin_48ee4b1b.add_argument('--C_Kieli', action='store_true')
    argumentit = jäsennin_48ee4b1b.parse_args()
    실패들 = []
    sopimuksen_arvo = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    Tiedosto_LASKE = 0
    parametri_taulukko = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [säilö_juuri/'compiler/kääntäjä.py', säilö_juuri/'compiler/기계어미리번역.py']
    for polku_2 in list((aloite_juuri/'työkalut').glob('*.py')) + list((aloite_juuri/'예제').rglob('*.py')) + 공용번역기들:
        if polku_2.name.endswith(('이름반영.py', '이름분석.py')): continue
        Tiedosto_LASKE += 1
        나무 = ast.parse(polku_2.read_text()); 나무들[polku_2] = 나무
        for merkintä_ARVO_962f286b in ast.walk(나무):
            if isinstance(merkintä_ARVO_962f286b, ast.FunctionDef):
                parametri_taulukko.setdefault(merkintä_ARVO_962f286b.name, set()).update(parametri_argumentti.arg for parametri_argumentti in merkintä_ARVO_962f286b.args.args + merkintä_ARVO_962f286b.args.kwonlyargs)
                if merkintä_ARVO_962f286b.args.kwarg: 가변매개함수.add(merkintä_ARVO_962f286b.name)
            if isinstance(merkintä_ARVO_962f286b, ast.ClassDef):
                for funktio_ARVO in merkintä_ARVO_962f286b.body:
                    if isinstance(funktio_ARVO, ast.FunctionDef) and funktio_ARVO.name == '__init__':
                        parametri_taulukko.setdefault(merkintä_ARVO_962f286b.name, set()).update(parametri_argumentti.arg for parametri_argumentti in funktio_ARVO.args.args + funktio_ARVO.args.kwonlyargs)
            Nimi = ''
            if isinstance(merkintä_ARVO_962f286b, (ast.FunctionDef, ast.ClassDef)): Nimi = merkintä_ARVO_962f286b.name
            elif isinstance(merkintä_ARVO_962f286b, ast.Name) and isinstance(merkintä_ARVO_962f286b.ctx, ast.Store): Nimi = merkintä_ARVO_962f286b.id
            elif isinstance(merkintä_ARVO_962f286b, ast.arg): Nimi = merkintä_ARVO_962f286b.arg
            if Nimi and Nimi not in sopimuksen_arvo and all(ord(merkki_ARVO)<128 for merkki_ARVO in Nimi):
                실패들.append('{}:{}: {}'.format(polku_2.relative_to(säilö_juuri), merkintä_ARVO_962f286b.lineno, Nimi))
    for polku_2, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Nimi = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Nimi not in parametri_taulukko or Nimi in 가변매개함수 or not any(ord(merkki_ARVO)>127 for merkki_ARVO in Nimi): continue
            for parametri_argumentti in 호출.keywords:
                if parametri_argumentti.arg and parametri_argumentti.arg not in parametri_taulukko[Nimi]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(polku_2.relative_to(säilö_juuri), 호출.lineno, Nimi, parametri_argumentti.arg))
    for syöterivi in (aloite_juuri/'명명/tiedostonimi_yhdistämismääritys.tsv').read_text().splitlines()[1:]:
        Edellinen_kohde, nykyinen_kohde, prosessi_ARVO_merkintä = syöterivi.split('\t')
        if not (aloite_juuri/nykyinen_kohde).is_file(): 실패들.append('siirrä_ARVO_83b651b8 tiedoston_nimi 없음: '+nykyinen_kohde)
        if prosessi_ARVO_merkintä == '호환진입점유지' and not (aloite_juuri/Edellinen_kohde).is_file(): 실패들.append('호환 aloituskohta 없음: '+Edellinen_kohde)
    예제 = (aloite_juuri.parents[1]/'example/java/Verkkoesimerkki.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for polku_2 in sorted((aloite_juuri.parents[1]/'example/java').glob('*.java')):
        lähdetiedosto = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', polku_2.read_text())
        for Nimi in re.findall(r'\b[^\W\d]\w*\b', lähdetiedosto, re.UNICODE):
            if Nimi not in 예약어 and all(ord(merkki_ARVO)<128 for merkki_ARVO in Nimi):
                실패들.append('{}: 예제의 영어 tunniste_ARVO {}'.format(polku_2.name, Nimi))
    for Nimi in ('Ikkuna', 'painike', 'Nimike', 'tekstikenttä', '화면구성요소', 'tapahtuma_jono', 'työntekijä', '실행할일', '동작받이', '동작알림', '작업'):
        lähdetiedosto = (aloite_juuri/'한국어자바/suomi/oma'/(Nimi+'.java')).read_text()
        lähdetiedosto = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', lähdetiedosto)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', lähdetiedosto):
            실패들.append(Nimi+': suomi 직접 구현에 표준 objekti_ARVO 래퍼가 남았습니다.')
    시언어예제 = (aloite_juuri.parents[1]/'example/c/Verkkoesimerkki.c').read_text()
    for Nimi in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Nimi in 시언어예제: 실패들.append('C 통신 예제에 남은 표준 Nimi: '+Nimi)
    파이썬예제 = (aloite_juuri.parents[1]/'example/python/Verkkoesimerkki.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python 통신 예제에 남은 표준 poikkeus 직접 käyttö_ARVO')
    머리 = (aloite_juuri.parents[1]/'posix-kor/arm64-native/esittelyt/통신규약.h').read_text()
    for Nimi in ('pilvi_Perhe', 'datagrammivastake', 'datagrammi_protokolla', 'vastake_OSOITE', 'pilvi_vastake_OSOITE', 'Luo_päätepiste', 'lähettää_datagrammi_data'):
        if re.search(r'^#define\s+'+Nimi+r'\b', 머리, re.M): 실패들.append('C 직접 toteutus 대신 makro_ARVO käyttö_ARVO: '+Nimi)
    자바파일수 = 0
    for juuri_ARVO in ('lähdetiedosto', 'käyttäjätila/자바', '한국어자바'):
        for polku_2 in (aloite_juuri/juuri_ARVO).rglob('*.java'):
            자바파일수 += 1
            lähdetiedosto = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', polku_2.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', lähdetiedosto):
                실패들.append('{}: 한국어화되지 않은 esittely {}'.format(polku_2.relative_to(aloite_juuri), 맞음[1]))
            if juuri_ARVO == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', lähdetiedosto):
                실패들.append('{}: 공개 poikkeus esittely'.format(polku_2.relative_to(aloite_juuri)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for polku_2 in sorted((säilö_juuri/'os/lähdetiedosto').glob('*.java')):
        x86자바파일수 += 1
        lähdetiedosto = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', polku_2.read_text())
        for Nimi in re.findall(r'\b[^\W\d]\w*\b', lähdetiedosto, re.UNICODE):
            if Nimi not in 예약어 | 표준자바이름 and all(ord(merkki_ARVO)<128 for merkki_ARVO in Nimi):
                실패들.append('{}: oma 영어 tunniste_ARVO {}'.format(polku_2.relative_to(säilö_juuri), Nimi))
    LOG_TIETUE = {'passed': False, 'python_files': Tiedosto_LASKE, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if argumentit.C_Kieli:
        subprocess.check_call(['python3', str(aloite_juuri/'työkalut/시언어이름분석.py')])
        Analysoi_ARVO = json.loads((aloite_juuri/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(VIRHE) for VIRHE in Analysoi_ARVO['VIRHE'])
        공개규약 = set(json.loads((aloite_juuri/'명명/규격이름.json').read_text()))
        for merkintä_ARVO_962f286b in Analysoi_ARVO['esittely'].values():
            Nimi = merkintä_ARVO_962f286b['Nimi']; polku_2 = Path(merkintä_ARVO_962f286b['tiedoston_nimi'])
            lähdetiedosto = polku_2.read_bytes()
            # suomi 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if lähdetiedosto[merkintä_ARVO_962f286b['SIIRTYMÄ_ARVO']:merkintä_ARVO_962f286b['SIIRTYMÄ_ARVO']+len(Nimi)] == Nimi.encode() and Nimi not in 공개규약:
                실패들.append('{}:{}: {}'.format(polku_2.relative_to(aloite_juuri), merkintä_ARVO_962f286b['syöterivi'], Nimi))
        LOG_TIETUE['c_semantic_checked'] = True
        LOG_TIETUE['c_source_sha256'] = {str(Path(tiedoston_nimi).relative_to(aloite_juuri)):hajautusarvo_Tiedosto for tiedoston_nimi,hajautusarvo_Tiedosto in Analysoi_ARVO['원문해시'].items()}
    LOG_TIETUE['passed'] = not 실패들; LOG_TIETUE['failures'] = 실패들
    kohde_ARVO = aloite_juuri/'build/verification/naming'; kohde_ARVO.mkdir(parents=True, exist_ok=True)
    (kohde_ARVO/'report.json').write_text(json.dumps(LOG_TIETUE, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: suomi esittely·tiedoston_nimi polku_2·호환 aloituskohta·통신 예제')

if __name__ == '__main__': Suorita_2()
