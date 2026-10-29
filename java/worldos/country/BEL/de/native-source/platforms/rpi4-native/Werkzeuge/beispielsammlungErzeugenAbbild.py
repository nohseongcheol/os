"""Embed boot-installed guest examples; canonical sources live in jkoros/example."""
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ip_config import read_config, configure_guest_text
from javaBibliothekErzeugenAbbild import javaBibliothekErstellen


def beispielsammlungErstellen(wurzelPfad, ablagePfad, befehlAusführen):
    ursprünglichDaten=ablagePfad/'example';ergebnisDaten=wurzelPfad/'build/examples';ergebnisDaten.mkdir(parents=True,exist_ok=True)
    klassePfad=ergebnisDaten/'classes';klassePfad.mkdir(exist_ok=True)
    javaBibliothekErstellen(wurzelPfad,befehlAusführen)
    ip_settings = read_config(wurzelPfad)
    def guest_bytes(path):
        data = path.read_bytes()
        return configure_guest_text(data.decode('utf-8'), ip_settings).encode('utf-8') if path.suffix in ('.java','.py','.c','.h','.md') else data
    java_sources = ergebnisDaten/'java-source'; java_sources.mkdir(exist_ok=True)
    javaAusführen=[]
    for path in sorted((ursprünglichDaten/'java').glob('*.java')):
        target = java_sources/path.name; target.write_bytes(guest_bytes(path)); javaAusführen.append(target)
    befehlAusführen(['javac','--release','8','-encoding','UTF-8','-cp',wurzelPfad/'build/java-library/classes','-d',klassePfad]+javaAusführen)
    befehlswortFolge=['public final class BeispielBündel { public static int wertEinrichten(int Sprache) { int verarbeitetWert;',
          'verarbeitetWert=Befehlsinterpreter.beispielVerzeichnis("/example"); if(verarbeitetWert<0)return verarbeitetWert;']
    bündelInhaltsverzeichnis={}
    liesmich=guest_bytes(ursprünglichDaten/'README.md')
    if len(liesmich)>16384: raise ValueError('example README exceeds native VFS limit')
    befehlswortFolge.append('verarbeitetWert=Befehlsinterpreter.beispielDatei("/example/README.md","%s"); if(verarbeitetWert<0)return verarbeitetWert;'%liesmich.hex())
    bündelInhaltsverzeichnis['/example/README.md']={'bytes':len(liesmich),'sha256':hashlib.sha256(liesmich).hexdigest()}
    befehlswortFolge.append('if(Sprache==0){verarbeitetWert=Befehlsinterpreter.beispielVerzeichnis("/lib"); if(verarbeitetWert<0)return verarbeitetWert;')
    for pfad in [ursprünglichDaten/'python/Deutsch.py'] + sorted((wurzelPfad/'pythonBrücke/bibliothek').glob('*.py')):
        inhaltswertWert=guest_bytes(pfad);zielobjektWert='/lib/'+pfad.name
        if len(inhaltswertWert)>16384 or len(zielobjektWert.encode('utf-8'))>63: raise ValueError('Python library exceeds native VFS limit: '+zielobjektWert)
        befehlswortFolge.append('verarbeitetWert=Befehlsinterpreter.beispielDatei(%s,"%s"); if(verarbeitetWert<0)return verarbeitetWert;'%(json.dumps(zielobjektWert,ensure_ascii=True),inhaltswertWert.hex()))
        bündelInhaltsverzeichnis[zielobjektWert]={'bytes':len(inhaltswertWert),'sha256':hashlib.sha256(inhaltswertWert).hexdigest()}
    befehlswortFolge.append('}')
    for nachschlagenIndex,Sprache in enumerate(('java','c','python')):
        dateiListe=[(datenPosition.name,datenPosition) for datenPosition in sorted((ursprünglichDaten/Sprache).iterdir()) if datenPosition.is_file()]
        if Sprache=='java':dateiListe += [(datenPosition.stem+'.class',klassePfad/(datenPosition.stem+'.class')) for datenPosition in javaAusführen]
        befehlswortFolge += ['if(Sprache==%d){'%nachschlagenIndex,'verarbeitetWert=Befehlsinterpreter.beispielVerzeichnis("/example/%s"); if(verarbeitetWert<0)return verarbeitetWert;'%Sprache]
        for Name,pfad in dateiListe:
            inhaltswertWert=guest_bytes(pfad);zielobjektWert='/example/'+Sprache+'/'+Name
            if len(inhaltswertWert)>16384 or len(zielobjektWert.encode('utf-8'))>63:raise ValueError('example exceeds native VFS limit: '+zielobjektWert)
            befehlswortFolge.append('verarbeitetWert=Befehlsinterpreter.beispielDatei(%s,"%s"); if(verarbeitetWert<0)return verarbeitetWert;'%(json.dumps(zielobjektWert,ensure_ascii=True),inhaltswertWert.hex()))
            bündelInhaltsverzeichnis[zielobjektWert]={'bytes':len(inhaltswertWert),'sha256':hashlib.sha256(inhaltswertWert).hexdigest()}
        befehlswortFolge += ['return 0;}']
    befehlswortFolge += ['return -22;}}']
    (wurzelPfad/'build/BeispielBündel.java').write_text('\n'.join(befehlswortFolge)+'\n')
    (ergebnisDaten/'manifest.json').write_text(json.dumps(bündelInhaltsverzeichnis,ensure_ascii=False,indent=2)+'\n')
