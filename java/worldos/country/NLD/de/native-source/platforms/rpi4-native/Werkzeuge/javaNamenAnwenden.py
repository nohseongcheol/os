#!/usr/bin/env python3
"""eigen Java lokalGültigkeitsbereich 이름을 바꾼다. Zeichenkette·주석·externWert 멤버 이름은 보존한다."""
import json
import re
from pathlib import Path

projektWurzel = Path(__file__).resolve().parents[1]
zuordnungWert = json.loads((projektWurzel / 'benennung/javaNamen.json').read_text())
teilblockAusdruck = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[\w$]+|[^\w\s]', re.UNICODE)
protokolldateiAufzeichnung = []
for verzeichnisWert in ('Quelltext', 'Benutzer/Java', 'DeutschJava'):
    for pfad in sorted((projektWurzel / verzeichnisWert).rglob('*.java')):
        Quelltext = pfad.read_text()
        teilblöckeListe = list(teilblockAusdruck.finditer(Quelltext))
        benutztName = {teilblockEintrag.group() for teilblockEintrag in teilblöckeListe if re.search('[ersterOperand-힣]', teilblockEintrag.group())}
        dateiZuordnung = {}
        for vorherigElementeintrag, danachWert in zuordnungWert.items():
            # A pre-existing Korean binding must never be shadowed by renaming.
            neuName = danachWert
            while neuName in benutztName: neuName = 'lokalGültigkeitsbereich' + neuName
            dateiZuordnung[vorherigElementeintrag] = neuName
        wertVerändern = []
        vorherigTeilblock = ''
        for teilblockEintrag in teilblöckeListe:
            lexikalischMaschinenwort = teilblockEintrag.group()
            if lexikalischMaschinenwort.startswith(('//', '/*', '"', "'")): continue
            if lexikalischMaschinenwort in dateiZuordnung and vorherigTeilblock != '.':
                wertVerändern.append((teilblockEintrag.start(), teilblockEintrag.end(), dateiZuordnung[lexikalischMaschinenwort]))
                protokolldateiAufzeichnung.append((str(pfad.relative_to(projektWurzel)), lexikalischMaschinenwort, dateiZuordnung[lexikalischMaschinenwort]))
            vorherigTeilblock = lexikalischMaschinenwort
        for ausführenVorgang, endung, neuName in reversed(wertVerändern): Quelltext = Quelltext[:ausführenVorgang] + neuName + Quelltext[endung:]
        if wertVerändern: pfad.write_text(Quelltext)
(projektWurzel / 'benennung/javaNameZuordnung.tsv').write_text('Datei\t이전\t이후\n' + ''.join('\t'.join(eintragWert)+'\n' for eintragWert in sorted(set(protokolldateiAufzeichnung))))
print('Java Name verweis wertÄndern:', len(protokolldateiAufzeichnung))
