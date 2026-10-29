#!/usr/bin/env python3
"""tatsächlichDaten RFB 클라이언트로 QEMU 창의 한글/tasteWert/클립보드/마우스와 Bildschirm 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from arbeitsflächeAnsicht import exaktWert
from befehlAusführen import projektWurzel


def ausführenVorgang():
    ausgabe=projektWurzel/'build/verification/desktop'; ausgabe.mkdir(parents=True,exist_ok=True)
    prozess=subprocess.Popen(['python3',str(projektWurzel/'Werkzeuge/arbeitsflächeAnsicht.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    bereitschaftÜberwacher=selectors.DefaultSelector(); bereitschaftÜberwacher.register(prozess.stdout,selectors.EVENT_READ)
    ablaufprotokoll=bytearray(); validierungBericht={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((projektWurzel/'build/kernel8.img').read_bytes()).hexdigest()}
    def bis(markierung,ausführenVorgang=0):
        fristZeit=time.monotonic()+45
        while markierung not in ablaufprotokoll[ausführenVorgang:]:
            if time.monotonic()>fristZeit or prozess.poll() is not None: raise AssertionError(ablaufprotokoll[ausführenVorgang:].decode('utf-8','replace'))
            for gedrücktWert,_ in bereitschaftÜberwacher.select(.1):
                Daten=gedrücktWert.fileobj.read(4096)
                if Daten: ablaufprotokoll.extend(Daten)
        return bytes(ablaufprotokoll[ausführenVorgang:])
    try:
        bis(b'TERMINAL READY')
        portNummer=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',ablaufprotokoll).group(1))
        with socket.create_connection(('127.0.0.1',portNummer),timeout=10) as anfragestelle:
            assert exaktWert(anfragestelle,12)==b'RFB 003.008\n'; anfragestelle.sendall(b'RFB 003.008\n')
            assert 1 in exaktWert(anfragestelle,exaktWert(anfragestelle,1)[0]); anfragestelle.sendall(b'\x01'); assert exaktWert(anfragestelle,4)==b'\0'*4
            anfragestelle.sendall(b'\x01'); anfänglichWert=exaktWert(anfragestelle,24); assert struct.unpack('>HH',anfänglichWert[:4])==(640,480); exaktWert(anfragestelle,struct.unpack('>I',anfänglichWert[20:])[0])
            anfragestelle.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            anfragestelle.sendall(struct.pack('>BBHi',2,0,1,0))
            def gedrücktWert(symbolWert,istDrückend=True): anfragestelle.sendall(struct.pack('>BBHI',4,int(istDrückend),0,symbolWert))
            def eingegebenZeichen(Text):
                for zeichenDaten in Text:
                    symbol=0xff0d if zeichenDaten=='\n' else ord(zeichenDaten) if ord(zeichenDaten)<256 else 0x01000000|ord(zeichenDaten)
                    gedrücktWert(symbol); gedrücktWert(symbol,False)
            def drückenTaste(symbolWert): gedrücktWert(symbolWert); gedrücktWert(symbolWert,False)
            # Start with English keys only, as delivered without a host IME.
            versatzwertWert=len(ablaufprotokoll); eingegebenZeichen('echo '); drückenTaste(0xffc6)
            eingegebenZeichen('dkssudgktpdy gksrmf'); drückenTaste(0xffc6); eingegebenZeichen('\n')
            bis('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),versatzwertWert)
            versatzwertWert=len(ablaufprotokoll); eingegebenZeichen('echo ')
            gedrücktWert(0xffe1); drückenTaste(32); gedrücktWert(0xffe1,False)
            eingegebenZeichen('dlfr'); drückenTaste(0xff08); drückenTaste(0xff08); eingegebenZeichen('fr')
            drückenTaste(0xff31); eingegebenZeichen(' EN\n')
            bis('\r\n읽 EN\r\njkoros-native> '.encode(),versatzwertWert)
            versatzwertWert=len(ablaufprotokoll); eingegebenZeichen('echo '); drückenTaste(0xff31)
            eingegebenZeichen('rhk rkqtk RkRnd'); drückenTaste(0xff31); eingegebenZeichen('\n')
            bis('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),versatzwertWert)
            # The same composition edits UTF-8 text in the native vi editor.
            versatzwertWert=len(ablaufprotokoll); eingegebenZeichen('vi hangulEingabe.txt\n'); bis(b'NORMAL',versatzwertWert)
            eingegebenZeichen('i'); drückenTaste(0xffc6); eingegebenZeichen('gksrmf dlfr'); drückenTaste(0xffc6)
            drückenTaste(0xff1b); eingegebenZeichen(':wq\n'); bis(b'jkoros-native> ',versatzwertWert)
            versatzwertWert=len(ablaufprotokoll); eingegebenZeichen('cat hangulEingabe.txt\n')
            bis('한글 읽'.encode(),versatzwertWert); bis(b'jkoros-native> ',versatzwertWert)
            versatzwertWert=len(ablaufprotokoll); eingegebenZeichen('help ko\n')
            bis('한/nullwertOperand tasteWert, Shift+Space 또는 F9'.encode(),versatzwertWert); bis(b'jkoros-native> ',versatzwertWert)
            versatzwertWert=len(ablaufprotokoll); eingegebenZeichen('clear\necho "VNC 한글 Eingabewert 😀"\n'); bis('VNC 한글 Eingabewert 😀\r\n'.encode(),versatzwertWert)
            versatzwertWert=len(ablaufprotokoll); gedrücktWert(0xffe3); gedrücktWert(ord('u')); gedrücktWert(ord('u'),False); gedrücktWert(0xffe3,False); eingegebenZeichen('echo CONTROL_OK\n'); bis(b'\r\nCONTROL_OK\r\n',versatzwertWert)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            zwischenablageWert='echo "einsetzenWert istFertig"\n'.encode(); versatzwertWert=len(ablaufprotokoll)
            anfragestelle.sendall(struct.pack('>B3xI',6,len(zwischenablageWert))+zwischenablageWert)
            for ereignis,_ in bereitschaftÜberwacher.select(.15):
                datenBlock=ereignis.fileobj.read(4096)
                if datenBlock: ablaufprotokoll.extend(datenBlock)
            assert 'einsetzenWert istFertig'.encode() not in ablaufprotokoll[versatzwertWert:]
            gedrücktWert(0xffe3); gedrücktWert(0xffe1); gedrücktWert(ord('v')); gedrücktWert(ord('v'),False); gedrücktWert(0xffe1,False); gedrücktWert(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            bis('\r\n붙여넣기 istFertig\r\njkoros-native> '.encode(),versatzwertWert)
            anfragestelle.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            rGBFarbe=bytearray(640*480*3); gesehenEinträge=False
            while not gesehenEinträge:
                mitteilungText=exaktWert(anfragestelle,1)[0]
                if mitteilungText==2: continue
                if mitteilungText==3:
                    größe=struct.unpack('>I',exaktWert(anfragestelle,7)[3:])[0]; exaktWert(anfragestelle,größe); continue
                assert mitteilungText==0,mitteilungText
                rechtecklisteListe=struct.unpack('>H',exaktWert(anfragestelle,3)[1:])[0]
                for _ in range(rechtecklisteListe):
                    waagerechteKoordinateKoordinate,senkrechteKoordinateKoordinate,angefordertBreiteWert,angefordertHöheWert,Zeichensatz=struct.unpack('>HHHHi',exaktWert(anfragestelle,12)); assert Zeichensatz==0,Zeichensatz
                    bildpunkteListe=exaktWert(anfragestelle,angefordertBreiteWert*angefordertHöheWert*4)
                    for innerlichOrdnungszahl in range(angefordertHöheWert):
                        for ordnungszahlIndex in range(angefordertBreiteWert):
                            ursprünglichAdresse=(innerlichOrdnungszahl*angefordertBreiteWert+ordnungszahlIndex)*4; zielAdresse=((senkrechteKoordinateKoordinate+innerlichOrdnungszahl)*640+waagerechteKoordinateKoordinate+ordnungszahlIndex)*3
                            rGBFarbe[zielAdresse:zielAdresse+3]=bytes((bildpunkteListe[ursprünglichAdresse+2],bildpunkteListe[ursprünglichAdresse+1],bildpunkteListe[ursprünglichAdresse]))
                    gesehenEinträge=True
            assert rGBFarbe[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (ausgabe/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+rGBFarbe)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(rGBFarbe)).save(str(ausgabe/'vnc-terminal.png'))
            versatzwertWert=len(ablaufprotokoll)
            gedrücktWert(0xffe3); gedrücktWert(0xffe1); gedrücktWert(ord('t')); gedrücktWert(ord('t'),False); gedrücktWert(0xffe1,False); gedrücktWert(0xffe3,False)
            bis(b'TERMINAL FOCUS 2',versatzwertWert)
            versatzwertWert=len(ablaufprotokoll); eingegebenZeichen('echo SECOND_VNC_WINDOW\n'); bis(b'\r\nSECOND_VNC_WINDOW\r\n',versatzwertWert)
            versatzwertWert=len(ablaufprotokoll); anfragestelle.sendall(struct.pack('>BBHH',5,1,576,81)); anfragestelle.sendall(struct.pack('>BBHH',5,0,576,81)); bis(b'TERMINAL FOCUS 1',versatzwertWert)
            versatzwertWert=len(ablaufprotokoll); eingegebenZeichen('python -c \'print("x"*9000)\'\n'); bis(b'\r\njkoros-native> ',versatzwertWert)
            assert len(ablaufprotokoll)-versatzwertWert>8192,'exercise output longer than bridge status buffer'
            versatzwertWert=len(ablaufprotokoll); anfragestelle.sendall(struct.pack('>BBHH',5,1,560,63)); anfragestelle.sendall(struct.pack('>BBHH',5,0,560,63)); bis(b'TERMINAL FOCUS 1',versatzwertWert)
            versatzwertWert=len(ablaufprotokoll); anfragestelle.sendall(struct.pack('>BBHH',5,1,80,16)); anfragestelle.sendall(struct.pack('>BBHH',5,0,80,16)); bis(b'TERMINAL FOCUS 1',versatzwertWert)
            versatzwertWert=len(ablaufprotokoll); eingegebenZeichen('echo REOPENED_VNC_WINDOW\n'); bis(b'\r\nREOPENED_VNC_WINDOW\r\n',versatzwertWert)
            versatzwertWert=len(ablaufprotokoll); eingegebenZeichen('gui\n'); bis(b'GUI READY:',versatzwertWert)
            versatzwertWert=len(ablaufprotokoll); anfragestelle.sendall(struct.pack('>BBHH',5,1,80,332)); anfragestelle.sendall(struct.pack('>BBHH',5,0,80,332)); bis(b'TERMINAL READY',versatzwertWert)
            validierungBericht.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if prozess.poll() is None:
            prozess.terminate()
            try: prozess.wait(timeout=8)
            except subprocess.TimeoutExpired: prozess.kill(); prozess.wait()
        bereitschaftÜberwacher.close(); prozess.stdout.close()
        (ausgabe/'serial.log').write_bytes(ablaufprotokoll)
        (ausgabe/'report.json').write_text(json.dumps(validierungBericht,indent=2)+'\n')


if __name__=='__main__': ausführenVorgang()
