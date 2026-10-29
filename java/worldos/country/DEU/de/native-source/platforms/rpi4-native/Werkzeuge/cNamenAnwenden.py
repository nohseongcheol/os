#!/usr/bin/env python3
"""Deklarationen 고유번호와 UTF-8 byteWert 위치로 eigen C 이름을 옮기는 일회성 이행 Werkzeuge.

externWert 구조체의 멤버, Zeichenkette, C 표준 Funktion, Portierung 규약은 보존한다.
입력은 wertÄndern davorWert 소스에 대한 cNamenUntersuchenWert.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

projektWurzel = Path(__file__).resolve().parents[1]

def befehlAusführen():
    wertUntersuchenWert = json.loads((projektWurzel/'build/한국어화/시언어분석.json').read_text())
    if wertUntersuchenWert['fehler']: raise SystemExit('wertUntersuchenWert 오류를 먼저 해결해야 합니다.')
    nameTabelle = json.loads((projektWurzel/'benennung/cNamen.json').read_text())
    standardDefinition = set(json.loads((projektWurzel/'benennung/standardNamen.json').read_text()))
    deklarationTabelle = wertUntersuchenWert['Deklarationen']
    deklarationNachErsetzen = {eindeutigWert:nameTabelle[eintragWert['Name']] for eindeutigWert,eintragWert in deklarationTabelle.items()
                if eintragWert['Name'] in nameTabelle and eintragWert['Name'] not in standardDefinition}
    verbindungTabelle = {eintragWert['Name']:nameTabelle[eintragWert['Name']] for eintragWert in deklarationTabelle.values()
              if eintragWert.get('verbinden')==4 and eintragWert['artWert'] in (8,9)
              and eintragWert['Name'] in nameTabelle and eintragWert['Name'] not in standardDefinition}
    # generieren AOT C·어셈블리·공개 SDK가 공유하는 바이너리 verbinden 이름만 유지한다.
    kopfWert = ['/* Deutsch quelltextBaum 이름과 기존 maschine verbinden vertragWert. 자동 generieren: benennung/cNamen.json */',
           '#ifndef systemnahMaschineBindenNamenKopf', '#define systemnahMaschineBindenNamenKopf']
    kopfWert += ['#define '+neuName+' '+altName for altName,neuName in sorted(verbindungTabelle.items())]
    kopfWert += ['#endif','']
    (projektWurzel/'benennung/maschineBindenNamen.h').write_text('\n'.join(kopfWert))
    änderungslisteListe = defaultdict(dict)
    for Datei,versatzwertWert,Name,eindeutigWert in wertUntersuchenWert['verweis']:
        if eindeutigWert in deklarationNachErsetzen:
            änderungslisteListe[Datei][versatzwertWert] = (Name,deklarationNachErsetzen[eindeutigWert])
    protokolldateiAufzeichnung = ['Datei\t원래바이트위치\t이전이름\t한국어이름']
    wertIgnorieren = []
    for Datei,wertÄndern in änderungslisteListe.items():
        pfad = Path(Datei); ursprünglich = pfad.read_bytes(); Daten = ursprünglich
        for versatzwertWert,(altName,neuName) in sorted(wertÄndern.items(),reverse=True):
            endung = versatzwertWert+len(altName.encode())
            if ursprünglich[versatzwertWert:endung] != altName.encode():
                wertIgnorieren.append((str(pfad.relative_to(projektWurzel)),versatzwertWert,altName));continue
            Daten = Daten[:versatzwertWert]+neuName.encode()+Daten[endung:]
            protokolldateiAufzeichnung.append('{}\t{}\t{}\t{}'.format(pfad.relative_to(projektWurzel),versatzwertWert,altName,neuName))
        pfad.write_bytes(Daten)
    # vorverarbeitenQuelltext 매개변수는 AST의 선언으로 나타나지 않는다. vorverarbeitenQuelltext 줄만 보완한다.
    lexikalischMaschinenwort = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    makroWert = {eintragWert['Name']:nameTabelle[eintragWert['Name']] for eintragWert in deklarationTabelle.values()
              if eintragWert['artWert']==501 and eintragWert['Name'] in nameTabelle and eintragWert['Name'] not in standardDefinition}
    for pfad in sorted({Path(eintragWert['Datei']) for eintragWert in deklarationTabelle.values()}):
        zeileListe = pfad.read_text().splitlines(True); istFortsetzung = False
        for Nummer,zeile in enumerate(zeileListe):
            vorverarbeitenQuelltext = istFortsetzung or bool(re.match(r'\s*#',zeile))
            istFortsetzung = vorverarbeitenQuelltext and zeile.rstrip().endswith('\\')
            if vorverarbeitenQuelltext:
                Tabelle = nameTabelle if re.match(r'\s*#\s*define\b',zeile) or istFortsetzung else makroWert
                zeileListe[Nummer] = lexikalischMaschinenwort.sub(lambda istÜbereinstimmend: Tabelle.get(istÜbereinstimmend[0],istÜbereinstimmend[0]) if istÜbereinstimmend[0] not in standardDefinition else istÜbereinstimmend[0],zeile)
        pfad.write_text(''.join(zeileListe))
    # 각 eigen quelltextÜbersetzenText 단위에만 연결표를 넣는다. externWert 배포본에는 전파하지 않는다.
    for pfad in sorted({Path(eintragWert['Datei']) for eintragWert in deklarationTabelle.values()}):
        if pfad.suffix not in ('.c','.cpp'):continue
        gegenstelleWert = '../' * len(pfad.relative_to(projektWurzel).parts[:-1]) + 'benennung/maschineBindenNamen.h'
        pfad.write_text('#include "'+gegenstelleWert+'"\n'+pfad.read_text())
    (projektWurzel/'benennung/cNameZuordnung.tsv').write_text('\n'.join(protokolldateiAufzeichnung)+'\n')
    (projektWurzel/'build/한국어화/전처리참조.json').write_text(json.dumps(wertIgnorieren,ensure_ascii=False,indent=2)+'\n')
    print('wertÄndern',len(protokolldateiAufzeichnung)-1,'vorverarbeitenQuelltext 재검토',len(wertIgnorieren),'maschine verbinden',len(verbindungTabelle))

if __name__=='__main__': befehlAusführen()
