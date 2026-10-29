#!/usr/bin/env python3
import hashlib,json,subprocess,tarfile
from pathlib import Path
from befehlAusführen import projektWurzel

def ausführenVorgang():
    ergebnisDaten=projektWurzel/'build/verification/coding';ergebnisDaten.mkdir(parents=True,exist_ok=True)
    validierungBericht={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((projektWurzel/'build/kernel8.img').read_bytes()).hexdigest(),'checks':[]}
    try:
        subprocess.check_call(['python3',str(projektWurzel/'Werkzeuge/exportierenSDK.py')])
        with tarfile.open(str(projektWurzel/'dist/jkoros-native-aarch64-sdk.tar.gz')) as komprimiertBündel:komprimiertBündel.extractall(str(ergebnisDaten))
        entwicklungWerkzeugsatz=ergebnisDaten/'jkoros-native-sdk'
        symboleListe=subprocess.check_output(['aarch64-linux-gnu-nm','--defined-only',str(entwicklungWerkzeugsatz/'lib/libposix-kor-user.a')]).decode()
        for Name in ('endpunktErstellen','adresseZuordnen','datagrammDatenSenden','datagrammDatenEmpfangen','dateiÖffnen','dateiDatenLesen','dateiDatenSchreiben'):
            assert ' T '+Name+'\n' in symboleListe, Name
        (ergebnisDaten/'korean-function-symbols.txt').write_text(symboleListe)
        validierungBericht['checks'].append('real-korean-c-function-symbols')
        def befehlAusführen(Name,pfad,argumentDatenfeld,erwartet):
            datenPosition=subprocess.run(['python3',str(projektWurzel/'Werkzeuge/dateiAusführen.py'),str(pfad)]+argumentDatenfeld,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (ergebnisDaten/(Name+'.log')).write_bytes(datenPosition.stdout);assert datenPosition.returncode==0,datenPosition.stdout.decode('utf-8','replace')
            assert erwartet.encode() in datenPosition.stdout,datenPosition.stdout;validierungBericht['checks'].append(Name)
        for nachsilbeWert in ('c','cpp'):
            ausführdateiDatei=ergebnisDaten/('Gruß-'+nachsilbeWert+'.elf')
            subprocess.check_call(['python3',str(entwicklungWerkzeugsatz/'compile.py'),str(entwicklungWerkzeugsatz/'examples'/('Gruß.'+nachsilbeWert)),'-o',str(ausführdateiDatei)])
            befehlAusführen('korean-'+nachsilbeWert,ausführdateiDatei,[],'posix-kor aufrufen')
        ausführdateiDatei=ergebnisDaten/'datenstromWert.elf'
        subprocess.check_call(['python3',str(entwicklungWerkzeugsatz/'compile.py'),str(entwicklungWerkzeugsatz/'examples/datenstromWert.c'),'-o',str(ausführdateiDatei)])
        befehlAusführen('c-stream-queues',ausführdateiDatei,[],'C posix-kor 연결형 Kommunikation PASS')
        befehlAusführen('korean-python',projektWurzel/'Beispiele/HangulKodierweise/Gruß.py',['--include',str(projektWurzel/'Beispiele/HangulKodierweise/Deutsch.py')],'안녕하세요 누리')
        befehlAusführen('guest-korean-javac',projektWurzel/'Beispiele/HangulKodierweise/Gruß.java',[],'안녕하세요 · gesamtwertWert=42')
        validierungBericht['passed']=True;print('PASS: Korean C/C++ identifiers and posix-kor SDK; Korean Python module; guest javac')
    finally:(ergebnisDaten/'report.json').write_text(json.dumps(validierungBericht,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ausführenVorgang()
