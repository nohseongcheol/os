#!/usr/bin/env python3
"""명명 klip·kivétel·경로를 검사한다. --시언어는 libclang bevallás 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

teendő_gyök = Path(__file__).resolve().parents[1]
adattár_gyök = teendő_gyök.parents[1]

def Futtatás():
    elemző_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    elemző_48ee4b1b.add_argument('--C_Nyelv', action='store_true')
    Argumentumok = elemző_48ee4b1b.parse_args()
    실패들 = []
    szerződés_értéke = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    Fájl_DARAB = 0
    paraméter_tábla = {}
    가변매개함수 = set()
    나무들 = {}
    공용번역기들 = [adattár_gyök/'compiler/fordítóprogram.py', adattár_gyök/'compiler/기계어미리번역.py']
    for ÚTVONAL in list((teendő_gyök/'Eszközök').glob('*.py')) + list((teendő_gyök/'예제').rglob('*.py')) + 공용번역기들:
        if ÚTVONAL.name.endswith(('이름반영.py', '이름분석.py')): continue
        Fájl_DARAB += 1
        나무 = ast.parse(ÚTVONAL.read_text()); 나무들[ÚTVONAL] = 나무
        for bejegyzés_ÉRTÉK in ast.walk(나무):
            if isinstance(bejegyzés_ÉRTÉK, ast.FunctionDef):
                paraméter_tábla.setdefault(bejegyzés_ÉRTÉK.name, set()).update(paraméter_argumentum.arg for paraméter_argumentum in bejegyzés_ÉRTÉK.args.args + bejegyzés_ÉRTÉK.args.kwonlyargs)
                if bejegyzés_ÉRTÉK.args.kwarg: 가변매개함수.add(bejegyzés_ÉRTÉK.name)
            if isinstance(bejegyzés_ÉRTÉK, ast.ClassDef):
                for FÜGGVÉNY_ÉRTÉK in bejegyzés_ÉRTÉK.body:
                    if isinstance(FÜGGVÉNY_ÉRTÉK, ast.FunctionDef) and FÜGGVÉNY_ÉRTÉK.name == '__init__':
                        paraméter_tábla.setdefault(bejegyzés_ÉRTÉK.name, set()).update(paraméter_argumentum.arg for paraméter_argumentum in FÜGGVÉNY_ÉRTÉK.args.args + FÜGGVÉNY_ÉRTÉK.args.kwonlyargs)
            Név = ''
            if isinstance(bejegyzés_ÉRTÉK, (ast.FunctionDef, ast.ClassDef)): Név = bejegyzés_ÉRTÉK.name
            elif isinstance(bejegyzés_ÉRTÉK, ast.Name) and isinstance(bejegyzés_ÉRTÉK.ctx, ast.Store): Név = bejegyzés_ÉRTÉK.id
            elif isinstance(bejegyzés_ÉRTÉK, ast.arg): Név = bejegyzés_ÉRTÉK.arg
            if Név and Név not in szerződés_értéke and all(ord(karakter_ÉRTÉK)<128 for karakter_ÉRTÉK in Név):
                실패들.append('{}:{}: {}'.format(ÚTVONAL.relative_to(adattár_gyök), bejegyzés_ÉRTÉK.lineno, Név))
    for ÚTVONAL, 나무 in 나무들.items():
        for 호출 in ast.walk(나무):
            if not isinstance(호출, ast.Call): continue
            Név = 호출.func.id if isinstance(호출.func, ast.Name) else 호출.func.attr if isinstance(호출.func, ast.Attribute) else ''
            if Név not in paraméter_tábla or Név in 가변매개함수 or not any(ord(karakter_ÉRTÉK)>127 for karakter_ÉRTÉK in Név): continue
            for paraméter_argumentum in 호출.keywords:
                if paraméter_argumentum.arg and paraméter_argumentum.arg not in paraméter_tábla[Név]:
                    실패들.append('{}:{}: {}의 매개변수 {}'.format(ÚTVONAL.relative_to(adattár_gyök), 호출.lineno, Név, paraméter_argumentum.arg))
    for Vonal in (teendő_gyök/'명명/fájlnév_leképezés.tsv').read_text().splitlines()[1:]:
        Előző_cikk, aktuális_cikk, folyamat_ÉRTÉK_bejegyzés = Vonal.split('\t')
        if not (teendő_gyök/aktuális_cikk).is_file(): 실패들.append('áthelyez_ÉRTÉK Fájl 없음: '+aktuális_cikk)
        if folyamat_ÉRTÉK_bejegyzés == '호환진입점유지' and not (teendő_gyök/Előző_cikk).is_file(): 실패들.append('호환 belépési_pont 없음: '+Előző_cikk)
    예제 = (teendő_gyök.parents[1]/'example/java/HálózatiPélda.java').read_text()
    for 금지호출 in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if 금지호출 in 예제: 실패들.append('네트워크 예제에 남은 표준 직접 호출: '+금지호출)
    # 사용자가 읽는 Java 예제는 예약어/리터럴을 제외한 식별자도 모두 한국어다.
    예약어 = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for ÚTVONAL in sorted((teendő_gyök.parents[1]/'example/java').glob('*.java')):
        FORRÁS = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ÚTVONAL.read_text())
        for Név in re.findall(r'\b[^\W\d]\w*\b', FORRÁS, re.UNICODE):
            if Név not in 예약어 and all(ord(karakter_ÉRTÉK)<128 for karakter_ÉRTÉK in Név):
                실패들.append('{}: 예제의 영어 azonosító_ÉRTÉK {}'.format(ÚTVONAL.name, Név))
    for Név in ('Ablak', 'gomb', 'Címke', 'szövegmező', '화면구성요소', 'esemény_várólista', 'dolgozó', '실행할일', '동작받이', 'Action_alapelv', '작업'):
        FORRÁS = (teendő_gyök/'한국어자바/magyar/saját'/(Név+'.java')).read_text()
        FORRÁS = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', FORRÁS)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', FORRÁS):
            실패들.append(Név+': magyar 직접 구현에 표준 objektum_ÉRTÉK 래퍼가 남았습니다.')
    시언어예제 = (teendő_gyök.parents[1]/'example/c/HálózatiPélda.c').read_text()
    for Név in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Név in 시언어예제: 실패들.append('C kommunikáció 예제에 남은 표준 Név: '+Név)
    파이썬예제 = (teendő_gyök.parents[1]/'example/python/HálózatiPélda.py').read_text()
    if 'OSError' in 파이썬예제 or '.args' in 파이썬예제: 실패들.append('Python kommunikáció 예제에 남은 표준 kivétel 직접 használ_ÉRTÉK')
    머리 = (teendő_gyök.parents[1]/'posix-kor/arm64-native/포함/통신규약.h').read_text()
    for Név in ('háló_Család', 'datagram_szoftvercsatorna', 'datagram_protokoll', 'szoftvercsatorna_CÍM', 'háló_szoftvercsatorna_CÍM', 'készít_végpont', 'küld_datagram_adat'):
        if re.search(r'^#define\s+'+Név+r'\b', 머리, re.M): 실패들.append('C 직접 구현 대신 makró_ÉRTÉK használ_ÉRTÉK: '+Név)
    자바파일수 = 0
    for gyök_ÉRTÉK in ('FORRÁS', 'felhasználó/자바', '한국어자바'):
        for ÚTVONAL in (teendő_gyök/gyök_ÉRTÉK).rglob('*.java'):
            자바파일수 += 1
            FORRÁS = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ÚTVONAL.read_text())
            for 맞음 in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', FORRÁS):
                실패들.append('{}: 한국어화되지 않은 bevallás {}'.format(ÚTVONAL.relative_to(teendő_gyök), 맞음[1]))
            if gyök_ÉRTÉK == '한국어자바' and re.search(r'\bthrows\s+[A-Za-z]', FORRÁS):
                실패들.append('{}: 공개 kivétel bevallás'.format(ÚTVONAL.relative_to(teendő_gyök)))
    x86자바파일수 = 0
    표준자바이름 = {'String', 'length', 'charAt'}
    for ÚTVONAL in sorted((adattár_gyök/'os/FORRÁS').glob('*.java')):
        x86자바파일수 += 1
        FORRÁS = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', ÚTVONAL.read_text())
        for Név in re.findall(r'\b[^\W\d]\w*\b', FORRÁS, re.UNICODE):
            if Név not in 예약어 | 표준자바이름 and all(ord(karakter_ÉRTÉK)<128 for karakter_ÉRTÉK in Név):
                실패들.append('{}: saját 영어 azonosító_ÉRTÉK {}'.format(ÚTVONAL.relative_to(adattár_gyök), Név))
    LOG_REKORD = {'passed': False, 'python_files': Fájl_DARAB, 'java_files': 자바파일수,
          'x86_java_files': x86자바파일수, 'host_compiler_python_files': len(공용번역기들), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if Argumentumok.C_Nyelv:
        subprocess.check_call(['python3', str(teendő_gyök/'Eszközök/시언어이름분석.py')])
        Elemzés_ÉRTÉK = json.loads((teendő_gyök/'build/한국어화/시언어분석.json').read_text())
        실패들.extend(str(HIBA) for HIBA in Elemzés_ÉRTÉK['HIBA'])
        공개규약 = set(json.loads((teendő_gyök/'명명/규격이름.json').read_text()))
        for bejegyzés_ÉRTÉK in Elemzés_ÉRTÉK['bevallás'].values():
            Név = bejegyzés_ÉRTÉK['Név']; ÚTVONAL = Path(bejegyzés_ÉRTÉK['Fájl'])
            FORRÁS = ÚTVONAL.read_bytes()
            # magyar 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if FORRÁS[bejegyzés_ÉRTÉK['Ofszet_ÉRTÉK']:bejegyzés_ÉRTÉK['Ofszet_ÉRTÉK']+len(Név)] == Név.encode() and Név not in 공개규약:
                실패들.append('{}:{}: {}'.format(ÚTVONAL.relative_to(teendő_gyök), bejegyzés_ÉRTÉK['Vonal'], Név))
        LOG_REKORD['c_semantic_checked'] = True
        LOG_REKORD['c_source_sha256'] = {str(Path(Fájl).relative_to(teendő_gyök)):kivonat_Fájl for Fájl,kivonat_Fájl in Elemzés_ÉRTÉK['원문해시'].items()}
    LOG_REKORD['passed'] = not 실패들; LOG_REKORD['failures'] = 실패들
    cél_ÉRTÉK = teendő_gyök/'build/verification/naming'; cél_ÉRTÉK.mkdir(parents=True, exist_ok=True)
    (cél_ÉRTÉK/'report.json').write_text(json.dumps(LOG_REKORD, ensure_ascii=False, indent=2)+'\n')
    if 실패들: raise SystemExit('\n'.join(실패들))
    print('PASS: magyar bevallás·Fájl ÚTVONAL·호환 belépési_pont·kommunikáció 예제')

if __name__ == '__main__': Futtatás()
