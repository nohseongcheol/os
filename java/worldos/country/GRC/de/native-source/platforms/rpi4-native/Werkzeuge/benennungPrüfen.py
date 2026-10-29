#!/usr/bin/env python3
"""benennung beschneiden·ausnahme·경로를 검사한다. --시언어는 libclang Deklarationen 분석도 수행한다."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

projektWurzel = Path(__file__).resolve().parents[1]
ablageWurzel = projektWurzel.parents[1]

def ausführenVorgang():
    Strukturanalysierer = argparse.ArgumentParser(description=__doc__)
    Strukturanalysierer.add_argument('--cSprache', action='store_true')
    argumente = Strukturanalysierer.parse_args()
    fehlschläge = []
    vertragWert = {'_', '__init__', '__enter__', '__exit__', 'setUp', 'handle'}
    dateiAnzahl = 0
    parameterTabelle = {}
    variableArgumenteFunktion = set()
    aSTKnotenliste = {}
    geteiltÜbersetzerListe = [ablageWurzel/'compiler/Übersetzer.py', ablageWurzel/'compiler/Vorabübersetzung.py']
    for pfad in list((projektWurzel/'Werkzeuge').glob('*.py')) + list((projektWurzel/'Beispiele').rglob('*.py')) + geteiltÜbersetzerListe:
        if pfad.name.endswith(('이름반영.py', '이름분석.py')): continue
        dateiAnzahl += 1
        aSTKnoten = ast.parse(pfad.read_text()); aSTKnotenliste[pfad] = aSTKnoten
        for eintragWert in ast.walk(aSTKnoten):
            if isinstance(eintragWert, ast.FunctionDef):
                parameterTabelle.setdefault(eintragWert.name, set()).update(parameterArgument.arg for parameterArgument in eintragWert.args.args + eintragWert.args.kwonlyargs)
                if eintragWert.args.kwarg: variableArgumenteFunktion.add(eintragWert.name)
            if isinstance(eintragWert, ast.ClassDef):
                for Funktion in eintragWert.body:
                    if isinstance(Funktion, ast.FunctionDef) and Funktion.name == '__init__':
                        parameterTabelle.setdefault(eintragWert.name, set()).update(parameterArgument.arg for parameterArgument in Funktion.args.args + Funktion.args.kwonlyargs)
            Name = ''
            if isinstance(eintragWert, (ast.FunctionDef, ast.ClassDef)): Name = eintragWert.name
            elif isinstance(eintragWert, ast.Name) and isinstance(eintragWert.ctx, ast.Store): Name = eintragWert.id
            elif isinstance(eintragWert, ast.arg): Name = eintragWert.arg
            if Name and Name not in vertragWert and all(ord(zeichenWert)<128 for zeichenWert in Name):
                fehlschläge.append('{}:{}: {}'.format(pfad.relative_to(ablageWurzel), eintragWert.lineno, Name))
    for pfad, aSTKnoten in aSTKnotenliste.items():
        for aufrufen in ast.walk(aSTKnoten):
            if not isinstance(aufrufen, ast.Call): continue
            Name = aufrufen.func.id if isinstance(aufrufen.func, ast.Name) else aufrufen.func.attr if isinstance(aufrufen.func, ast.Attribute) else ''
            if Name not in parameterTabelle or Name in variableArgumenteFunktion or not any(ord(zeichenWert)>127 for zeichenWert in Name): continue
            for parameterArgument in aufrufen.keywords:
                if parameterArgument.arg and parameterArgument.arg not in parameterTabelle[Name]:
                    fehlschläge.append('{}:{}: {}의 매개변수 {}'.format(pfad.relative_to(ablageWurzel), aufrufen.lineno, Name, parameterArgument.arg))
    for zeile in (projektWurzel/'benennung/dateiNameZuordnung.tsv').read_text().splitlines()[1:]:
        vorherigElementeintrag, aktuellElementeintrag, prozessWertEintrag = zeile.split('\t')
        if not (projektWurzel/aktuellElementeintrag).is_file(): fehlschläge.append('bewegenWert Datei fehlendMethode: '+aktuellElementeintrag)
        if prozessWertEintrag == '호환진입점유지' and not (projektWurzel/vorherigElementeintrag).is_file(): fehlschläge.append('호환 eintragPunkt fehlendMethode: '+vorherigElementeintrag)
    Beispiele = (projektWurzel.parents[1]/'example/java/Netzbeispiel.java').read_text()
    for verbotenAufrufliste in ('java.net.', '.getOutputStream(', '.getInputStream(', '.write(', '.read(', '.close('):
        if verbotenAufrufliste in Beispiele: fehlschläge.append('네트워크 예제에 남은 표준 직접 aufrufen: '+verbotenAufrufliste)
    # 사용자가 읽는 Java 예제는 reserviertWörter/리터럴을 제외한 식별자도 alleErzeugenAbbild 한국어다.
    reserviertWörter = set('abstract assert boolean break byte case catch char class const continue default do double else enum extends final finally float for goto if implements import instanceof int interface long native new package private protected public return short static strictfp super switch synchronized this throw throws transient try void volatile while true false null'.split())
    for pfad in sorted((projektWurzel.parents[1]/'example/java').glob('*.java')):
        Quelltext = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', pfad.read_text())
        for Name in re.findall(r'\b[^\W\d]\w*\b', Quelltext, re.UNICODE):
            if Name not in reserviertWörter and all(ord(zeichenWert)<128 for zeichenWert in Name):
                fehlschläge.append('{}: 예제의 영어 bezeichnerWert {}'.format(pfad.name, Name))
    for Name in ('fenster', 'schaltfläche', 'beschriftung', 'TextFeld', 'BildschirmElement', 'EreignisWarteschlange', 'hintergrundarbeiter', 'AusführbarAufgabe', 'AktionEmpfänger', 'AktionMitteilung', 'Aufgabe'):
        Quelltext = (projektWurzel/'DeutschJava/Deutsch/eigen'/(Name+'.java')).read_text()
        Quelltext = re.sub(r'//[^\n]*|/\*[\s\S]*?\*/', '', Quelltext)
        if re.search(r'\b(?:Runnable|Thread|JButton|SwingUtilities|ActionListener|ActionEvent)\b|javax\.swing|java\.awt', Quelltext):
            fehlschläge.append(Name+': Deutsch 직접 구현에 표준 objektWert 래퍼가 남았습니다.')
    cBeispiel = (projektWurzel.parents[1]/'example/c/Netzbeispiel.c').read_text()
    for Name in ('AF_INET', 'SOCK_DGRAM', 'IPPROTO_UDP', 'pk_sockaddr', 'sin_family', 'sin_port', 'sin_addr', 's_addr'):
        if Name in cBeispiel: fehlschläge.append('C Kommunikation 예제에 남은 표준 Name: '+Name)
    pythonBeispiel = (projektWurzel.parents[1]/'example/python/Netzbeispiel.py').read_text()
    if 'OSError' in pythonBeispiel or '.args' in pythonBeispiel: fehlschläge.append('Python Kommunikation 예제에 남은 표준 ausnahme 직접 benutzenWert')
    kopfWert = (projektWurzel.parents[1]/'posix-kor/arm64-native/Kopfdateien/NetzwerkABI.h').read_text()
    for Name in ('InternetFamilie', 'DatagrammNetzbuchse', 'DatagrammProtokoll', 'NetzbuchseAdresse', 'InternetNetzbuchseAdresse', 'endpunktErstellen', 'datagrammDatenSenden'):
        if re.search(r'^#define\s+'+Name+r'\b', kopfWert, re.M): fehlschläge.append('C 직접 umsetzung 대신 makroWert benutzenWert: '+Name)
    javaDateiAnzahl = 0
    for wurzelWert in ('Quelltext', 'Benutzer/Java', 'DeutschJava'):
        for pfad in (projektWurzel/wurzelWert).rglob('*.java'):
            javaDateiAnzahl += 1
            Quelltext = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', pfad.read_text())
            for istÜbereinstimmend in re.finditer(r'\b(?:int|long|boolean|byte|char|short|String)(?:\s*\[\s*\])*\s+([A-Za-z_$][A-Za-z_$0-9]*)\b', Quelltext):
                fehlschläge.append('{}: 한국어화되지 않은 Deklarationen {}'.format(pfad.relative_to(projektWurzel), istÜbereinstimmend[1]))
            if wurzelWert == 'DeutschJava' and re.search(r'\bthrows\s+[A-Za-z]', Quelltext):
                fehlschläge.append('{}: 공개 ausnahme Deklarationen'.format(pfad.relative_to(projektWurzel)))
    x86JavaDateianzahl = 0
    standardJavaNamen = {'String', 'length', 'charAt'}
    for pfad in sorted((ablageWurzel/'os/Quelltext').glob('*.java')):
        x86JavaDateianzahl += 1
        Quelltext = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/', ' ', pfad.read_text())
        for Name in re.findall(r'\b[^\W\d]\w*\b', Quelltext, re.UNICODE):
            if Name not in reserviertWörter | standardJavaNamen and all(ord(zeichenWert)<128 for zeichenWert in Name):
                fehlschläge.append('{}: eigen 영어 bezeichnerWert {}'.format(pfad.relative_to(ablageWurzel), Name))
    protokolldateiAufzeichnung = {'passed': False, 'python_files': dateiAnzahl, 'java_files': javaDateiAnzahl,
          'x86_java_files': x86JavaDateianzahl, 'host_compiler_python_files': len(geteiltÜbersetzerListe), 'c_semantic_checked': False,
          'java_examples_korean_identifiers': True, 'direct_korean_gui_thread_without_standard_wrappers': True}
    if argumente.cSprache:
        subprocess.check_call(['python3', str(projektWurzel/'Werkzeuge/cNamenUntersuchenWert.py')])
        wertUntersuchenWert = json.loads((projektWurzel/'build/한국어화/시언어분석.json').read_text())
        fehlschläge.extend(str(fehler) for fehler in wertUntersuchenWert['fehler'])
        exportierenABI = set(json.loads((projektWurzel/'benennung/standardNamen.json').read_text()))
        for eintragWert in wertUntersuchenWert['Deklarationen'].values():
            Name = eintragWert['Name']; pfad = Path(eintragWert['Datei'])
            Quelltext = pfad.read_bytes()
            # Deutsch 소스가 공개 ABI 매크로를 거쳐 영어 심볼이 된 경우는 허용한다.
            if Quelltext[eintragWert['versatzwertWert']:eintragWert['versatzwertWert']+len(Name)] == Name.encode() and Name not in exportierenABI:
                fehlschläge.append('{}:{}: {}'.format(pfad.relative_to(projektWurzel), eintragWert['zeile'], Name))
        protokolldateiAufzeichnung['c_semantic_checked'] = True
        protokolldateiAufzeichnung['c_source_sha256'] = {str(Path(Datei).relative_to(projektWurzel)):prüfsummeDatei for Datei,prüfsummeDatei in wertUntersuchenWert['원문해시'].items()}
    protokolldateiAufzeichnung['passed'] = not fehlschläge; protokolldateiAufzeichnung['failures'] = fehlschläge
    zielWert = projektWurzel/'build/verification/naming'; zielWert.mkdir(parents=True, exist_ok=True)
    (zielWert/'report.json').write_text(json.dumps(protokolldateiAufzeichnung, ensure_ascii=False, indent=2)+'\n')
    if fehlschläge: raise SystemExit('\n'.join(fehlschläge))
    print('PASS: Deutsch Deklarationen·Datei pfad·호환 eintragPunkt·Kommunikation Beispiele')

if __name__ == '__main__': ausführenVorgang()
