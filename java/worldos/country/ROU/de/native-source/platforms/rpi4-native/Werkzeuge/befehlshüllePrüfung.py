#!/usr/bin/env python3
"""eigen 커널의 befehlshülle, 프로세스 eingabeAusgabe, Unicode GUI 터미널을 tatsächlichDaten raspi4b에서 Prüfungen."""
import hashlib
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time
from befehlAusführen import projektWurzel, befehl


def ausführenVorgang():
    ausgabe = projektWurzel / 'build/verification/shell'; ausgabe.mkdir(parents=True, exist_ok=True)
    validierungBericht = {'passed': False, 'linux_loaded': False, 'checks': [], 'kernel_sha256': hashlib.sha256((projektWurzel / 'build/kernel8.img').read_bytes()).hexdigest()}
    ablaufprotokoll = bytearray()
    with tempfile.TemporaryDirectory(prefix='native-shell-') as arbeitendPfad:
        attrappeSteuerungVerbindung = Path(arbeitendPfad) / 'qmp.sock'
        prozess = subprocess.Popen(befehl()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(attrappeSteuerungVerbindung)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        bereitschaftÜberwacher=selectors.DefaultSelector(); bereitschaftÜberwacher.register(prozess.stdout,selectors.EVENT_READ)
        def nachrichtEmpfangen(markierung, ausführungZeitüberschreitung=45):
            Daten=bytearray(); endeVersatzwert=time.monotonic()+ausführungZeitüberschreitung
            while markierung not in Daten:
                if time.monotonic()>endeVersatzwert or prozess.poll() is not None: raise AssertionError('UART timeout/exit: '+Daten.decode('utf-8','replace'))
                for gedrücktWert,_ in bereitschaftÜberwacher.select(.1):
                    fragmentWert=gedrücktWert.fileobj.read(4096)
                    if fragmentWert: Daten.extend(fragmentWert); ablaufprotokoll.extend(fragmentWert)
                if b'PANIC:' in Daten or b'FAIL ' in Daten: raise AssertionError(Daten)
            return Daten.decode('utf-8','replace').replace('\r\n','\n')
        def senden(Daten, markierung=b'jkoros-native> '):
            prozess.stdin.write(Daten); prozess.stdin.flush(); return nachrichtEmpfangen(markierung)
        def befehlshülle(zeile, *erwartet):
            ergebnis=senden(zeile.encode()+b'\n')
            for Wert in erwartet: assert Wert in ergebnis, (zeile,Wert,ergebnis)
            return ergebnis
        def Datei(Name):
            Text=befehlshülle('hex '+Name,'HEX BEGIN','HEX END'); ergebnisSuchen=re.search(r'HEX BEGIN (\d+)\n(.*?)HEX END',Text,re.S)
            Daten=bytes.fromhex(''.join(ergebnisSuchen.group(2).split())); assert len(Daten)==int(ergebnisSuchen.group(1)); return Daten
        try:
            nachrichtEmpfangen(b'jkoros-native> ')
            befehlshülle('mkdir Aufgabe; cd Aufgabe; pwd','/Aufgabe')
            befehlshülle('mkdir 하위; echo "한글 Daten 😀" > Gruß.txt')
            assert Datei('Gruß.txt')=='한글 Daten 😀\n'.encode()
            befehlshülle('cp Gruß.txt wertKopieren.txt; mv wertKopieren.txt 하위/옮김.txt; cat 하위/옮김.txt','한글 Daten 😀')
            befehlshülle('cd 하위; cat ../Gruß.txt; cat /Aufgabe/Gruß.txt; pwd','한글 Daten 😀','/Aufgabe/하위')
            befehlshülle('cd ..; rmdir 하위; echo $?','1\n')
            befehlshülle('rm 하위/옮김.txt; rmdir 하위; touch 빈파일; wc -c 빈파일','0\n')
            befehlshülle('cp Gruß.txt Gruß.txt; echo $?','1\n'); assert Datei('Gruß.txt')=='한글 Daten 😀\n'.encode()
            befehlshülle('export Gruß=누리; echo "$인사:${PWD}"; false && echo BAD || echo GOOD','누리:/Aufgabe','GOOD')
            assert b'BAD\n' not in Datei('Gruß.txt')
            befehlshülle("echo '$인사' > 리터럴; echo $인사 >> 리터럴")
            assert Datei('리터럴')=='$인사\n누리\n'.encode()
            befehlshülle('echo one > anweisungWert; echo two >> anweisungWert; echo three >> anweisungWert')
            befehlshülle('cat < anweisungWert | grep t | tee 추림 | wc -l','2\n'); assert Datei('추림')==b'two\nthree\n'
            befehlshülle('head -n 1 anweisungWert > vorderseiteWert; tail -n 1 anweisungWert > rückseiteWert'); assert Datei('앞')==b'one\n'; assert Datei('뒤')==b'three\n'
            befehlshülle('grep absent anweisungWert; echo $?','1\n')
            befehlshülle('echo untouched > wertSchützen')
            befehlshülle('echo destroyed > wertSchützen |','명령이 빠졌습니다'); assert Datei('wertSchützen')==b'untouched\n'
            befehlshülle('echo "oops','따옴표가 닫히지 않았습니다')
            befehlshülle('echo bad &','뒤에서 실행하는 작업은 지원하지 않습니다')
            befehlshülle('echo bad 2> wertSchützen','번호를 지정한 Datei deskriptorEintrag eingabeAusgabe umschaltenBetriebsart'); assert Datei('wertSchützen')==b'untouched\n'
            befehlshülle('rm 빈파일 리터럴 anweisungWert 추림 vorderseiteWert rückseiteWert wertSchützen')
            validierungBericht['checks'].append('directories/relative and absolute paths/cp/mv/unlink/rmdir/variables/conditions/redirects/pipes/filters/errors')
            # EL0 stdout reaches pipeline, without the shell exit marker leaking into data.
            befehlshülle("python -c 'print(123)' | wc -c",'4\n')
            befehlshülle("python -c 'print(456)' > Programm.txt"); assert Datei('Programm.txt')==b'456\n'
            befehlshülle("echo input | python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))'", "b'input\\n'", "b''")
            befehlshülle("python -c 'import jkoros; print(jkoros.stdin(64)); print(jkoros.stdin(64))' < Programm.txt", "b'456\\n'", "b''")
            befehlshülle("python -c 'print(\"x\"*17000)' | wc -c", 'fehler -28')
            befehlshülle('echo recovered | wc -c','10\n')
            befehlshülle("python -c 'import jkoros; print(jkoros.read("+'"/Aufgabe/Programm.txt"'+"))'",'456','exit 0')
            befehlshülle('cd /; javac Hello.java','Compiled:','exit 0')
            befehlshülle('java Hello > /Aufgabe/Java.txt'); assert '안녕하세요'.encode() in Datei('/Aufgabe/Java.txt')
            befehlshülle('cd Aufgabe; echo "echo script > ausführungErgebnis" > befehl.sh; echo "false || echo recovered >> ausführungErgebnis" >> befehl.sh; sh befehl.sh')
            assert Datei('ausführungErgebnis')==b'script\nrecovered\n'
            befehlshülle('rm ausführungErgebnis; echo "exit 7" > verlassenProzessProgramm.sh; sh verlassenProzessProgramm.sh; echo $?','7\n')
            befehlshülle('rm verlassenProzessProgramm.sh befehl.sh Programm.txt Java.txt Gruß.txt; cd /; rmdir Aufgabe')
            validierungBericht['checks'].append('EL0 Python/Java stdout routing and absolute VFS paths; script execution and exit status')
            befehlshülle('echo history-proof','history-proof')
            ergebnis=senden(b'\x1b[A\n',b'\r\nhistory-proof\r\njkoros-native> '); assert ergebnis.count('history-proof')>=2, ergebnis
            senden(b'echo eraseX\x7f\n',b'\r\nerase\r\njkoros-native> ')
            ergebnis=senden(b'echo ac\x1b[Db\n',b'\r\nabc\r\njkoros-native> '); assert '\nabc\n' in ergebnis, ergebnis
            ergebnis=senden(b'ec\tcomplete\n',b'\r\ncomplete\r\njkoros-native> '); assert '\ncomplete\n' in ergebnis,ergebnis
            ergebnis=senden('echo 한글X'.encode()+b'\x7f\n', '\r\n한글\r\njkoros-native> '.encode()); assert '\n한글\n' in ergebnis,ergebnis
            langText='한글'*50
            ergebnis=senden(('echo '+langText+'X').encode()+b'\x7f\x01\x05\n', ('\r\n'+langText+'\r\njkoros-native> ').encode()); assert '\n'+langText+'\n' in ergebnis
            befehlshülle('terminal','TERMINAL READY')
            befehlshülle('clear')
            befehlshülle('echo "한글 terminal ABC xyz 012 😀"','한글 terminal ABC xyz 012 😀')
            with socket.socket(socket.AF_UNIX) as anfragestelle:
                anfragestelle.settimeout(10); anfragestelle.connect(str(attrappeSteuerungVerbindung))
                with anfragestelle.makefile('rwb') as datenstromWert:
                    json.loads(datenstromWert.readline())
                    def aufrufen(Name,argumentDatenfeld=None):
                        netzwerkNachricht={'execute':Name}
                        if argumentDatenfeld: netzwerkNachricht['arguments']=argumentDatenfeld
                        datenstromWert.write((json.dumps(netzwerkNachricht)+'\n').encode()); datenstromWert.flush()
                        while True:
                            antwort=json.loads(datenstromWert.readline())
                            if 'error' in antwort: raise AssertionError(antwort)
                            if 'return' in antwort: return antwort['return']
                    aufrufen('qmp_capabilities')
                    abbild=ausgabe/'terminal.ppm'; aufrufen('screendump',{'filename':str(abbild),'format':'ppm'})
                    aufrufen('screendump',{'filename':str(ausgabe/'terminal.png'),'format':'png'})
                    Daten=abbild.read_bytes().split(b'\n',3)[3]
                    def bildpunkt(waagerechteKoordinateKoordinate,senkrechteKoordinateKoordinate): return tuple(Daten[(senkrechteKoordinateKoordinate*640+waagerechteKoordinateKoordinate)*3:(senkrechteKoordinateKoordinate*640+waagerechteKoordinateKoordinate)*3+3])
                    assert bildpunkt(12,48)==(32,80,144),bildpunkt(12,48)
                    assert len(set(bildpunkt(waagerechteKoordinateKoordinate,senkrechteKoordinateKoordinate) for senkrechteKoordinateKoordinate in range(100,116) for waagerechteKoordinateKoordinate in range(24,56)))>1,'Hangul glyphs missing'
                    befehlshülle('python -c \'print("GUI PROCESS OUTPUT")\'','GUI PROCESS OUTPUT','exit 0')
                    befehlshülle("python -c 'import jkoros; jkoros.rect(0,0,640,480,0)'", 'exit 0')
                    aufrufen('screendump',{'filename':str(abbild),'format':'ppm'})
                    wiederhergestelltDaten=abbild.read_bytes().split(b'\n',3)[3]
                    assert tuple(wiederhergestelltDaten[(48*640+12)*3:(48*640+12)*3+3])==(32,80,144),'terminal frame not restored after graphics program'
                    befehlshülle('echo test > visible.txt; cat visible.txt','test')
                    for ordnungszahlIndex in range(27): befehlshülle('echo scroll-'+str(ordnungszahlIndex),'scroll-'+str(ordnungszahlIndex))
                    senden(b'\x1b[5~\x1b[6~\n')
                    aufrufen('screendump',{'filename':str(ausgabe/'terminal-scroll.png'),'format':'png'})
                    ergebnis=senden(b'\x1b[24~\n',b'jkoros-native> '); assert 'TERMINAL CLOSED' in ergebnis,ergebnis
                    befehlshülle('rm visible.txt')
                    aufrufen('quit')
            prozess.wait(timeout=5)
            validierungBericht['checks'].append('history/arrows/UTF-8 deletion/completion/terminal open/close/scrollback/Hangul framebuffer pixels/EL0 GUI output')
            validierungBericht['passed']=True; print('PASS: native shell, directories, redirects/pipelines, scripts, editor, Unicode terminal')
        finally:
            if prozess.poll() is None:
                prozess.terminate()
                try: prozess.wait(timeout=5)
                except subprocess.TimeoutExpired: prozess.kill(); prozess.wait()
            bereitschaftÜberwacher.close(); prozess.stdin.close(); prozess.stdout.close()
            (ausgabe/'serial.log').write_bytes(ablaufprotokoll)
            (ausgabe/'report.json').write_text(json.dumps(validierungBericht,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__': ausführenVorgang()
