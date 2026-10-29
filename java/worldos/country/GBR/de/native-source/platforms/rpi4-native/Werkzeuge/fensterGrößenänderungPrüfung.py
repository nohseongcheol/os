#!/usr/bin/env python3
"""tatsächlichDaten QEMU/VNC에서 terminal eckeWert ziehenWert·zeiger·동적 zeichenWert platzEintrag·bearbeitenWert inhaltswertWert 보존를 검사한다."""
import ftplib
import hashlib
import io
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from PIL import Image
from arbeitsflächeAnsicht import exaktWert
from befehlAusführen import projektWurzel


def fensterGrößenänderungPrüfung(breiteWert, höheWert, ergebnisPfad):
    with socket.socket() as vorläufigWert:
        vorläufigWert.bind(('127.0.0.1', 0)); portNummer = vorläufigWert.getsockname()[1]
    größeText = '{}x{}'.format(breiteWert, höheWert)
    prozessWert = subprocess.Popen(['python3', str(projektWurzel/'Werkzeuge/befehlAusführen.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(portNummer), '--resolution', größeText], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    Auswähler = selectors.DefaultSelector(); Auswähler.register(prozessWert.stdout, selectors.EVENT_READ)
    protokolldateiAufzeichnung = bytearray(); entferntWert = None; übertragungWert = None; zeigerVerborgen=[False]

    def abwarten(wertAnzeigen, ausführenVorgang=0):
        fristWert = time.monotonic() + 60
        while wertAnzeigen not in protokolldateiAufzeichnung[ausführenVorgang:]:
            if time.monotonic() > fristWert or prozessWert.poll() is not None or b'HALTED' in protokolldateiAufzeichnung or b'PANIC:' in protokolldateiAufzeichnung:
                raise AssertionError(protokolldateiAufzeichnung[ausführenVorgang:].decode('utf-8', 'replace'))
            for ereignis, _ in Auswähler.select(.1):
                Daten = ereignis.fileobj.read(65536)
                if Daten: protokolldateiAufzeichnung.extend(Daten)
        return protokolldateiAufzeichnung[ausführenVorgang:].decode('utf-8', 'replace')

    def klickenSchaltfläche(symbol, istGedrückt=True): entferntWert.sendall(struct.pack('>BBHI', 4, int(istGedrückt), 0, symbol))

    def textSenden(Text):
        ausführenVorgang = len(protokolldateiAufzeichnung)
        for zeichenWert in Text:
            symbol = 0xff0d if zeichenWert == '\n' else ord(zeichenWert) if ord(zeichenWert) < 256 else 0x1000000 | ord(zeichenWert)
            klickenSchaltfläche(symbol); klickenSchaltfläche(symbol, False)
        return ausführenVorgang

    def befehlshülle(Text): return abwarten(b'\r\n__RESIZE_DONE__\r\n', textSenden(Text+'; echo __RESIZE_DONE__\n'))

    def punktAnStelle(waagerechtPosition, senkrechtPosition, istGedrückt): entferntWert.sendall(struct.pack('>BBHH', 5, istGedrückt, waagerechtPosition, senkrechtPosition))

    def klickenWert(waagerechtPosition, senkrechtPosition): punktAnStelle(waagerechtPosition, senkrechtPosition, 1); punktAnStelle(waagerechtPosition, senkrechtPosition, 0)

    def bitkarteAbbild():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 tatsächlichDaten 너비를 쓴다.
        entferntWert.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, breiteWert, höheWert))
        Zeichnung = Image.new('RGB', (breiteWert, höheWert)); flächeWert = 0
        while True:
            artWert = exaktWert(entferntWert, 1)[0]
            if artWert == 2: continue
            if artWert == 3:
                Länge = struct.unpack('>I', exaktWert(entferntWert, 7)[3:])[0]; exaktWert(entferntWert, Länge); continue
            assert artWert == 0, artWert
            elementeintragAnzahl = struct.unpack('>H', exaktWert(entferntWert, 3)[1:])[0]
            for _ in range(elementeintragAnzahl):
                waagerechtPosition, senkrechtPosition, breiteSpannweite, Länge, kodierungWert = struct.unpack('>HHHHi', exaktWert(entferntWert, 12))
                if kodierungWert == -239:
                    assert breiteSpannweite==0 and Länge==0, 'remote cursor must be hidden'
                    zeigerVerborgen[0]=True
                    continue
                assert kodierungWert == 0 and waagerechtPosition+breiteSpannweite <= breiteWert and senkrechtPosition+Länge <= höheWert
                Zeichnung.paste(Image.frombytes('RGB', (breiteSpannweite, Länge), exaktWert(entferntWert, breiteSpannweite*Länge*4), 'raw', 'BGRX'), (waagerechtPosition, senkrechtPosition))
                flächeWert += breiteSpannweite*Länge
            if flächeWert:
                assert flächeWert == breiteWert*höheWert, flächeWert
                return Zeichnung

    def bildpunktPrüfen(koordinateWert, farbeWert):
        fristWert = time.monotonic()+10
        while True:
            Zeichnung = bitkarteAbbild()
            if Zeichnung.getpixel(koordinateWert) == farbeWert: return Zeichnung
            if time.monotonic() > fristWert: raise AssertionError((koordinateWert, Zeichnung.getpixel(koordinateWert), farbeWert))

    def hochladenDateien(Name, Daten): übertragungWert.storbinary('STOR '+Name, io.BytesIO(Daten))

    try:
        abwarten(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+größeText+' RGB32').encode() in protokolldateiAufzeichnung
        print('BOOT:', größeText, flush=True)
        entferntNummer = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', protokolldateiAufzeichnung).group(1))
        entferntWert = socket.create_connection(('127.0.0.1', entferntNummer), timeout=20)
        assert exaktWert(entferntWert, 12) == b'RFB 003.008\n'; entferntWert.sendall(b'RFB 003.008\n')
        assert 1 in exaktWert(entferntWert, exaktWert(entferntWert, 1)[0]); entferntWert.sendall(b'\x01')
        assert exaktWert(entferntWert, 4) == b'\0'*4; entferntWert.sendall(b'\x01')
        anfänglichStatuswert = exaktWert(entferntWert, 24); assert struct.unpack('>HH', anfänglichStatuswert[:4]) == (breiteWert, höheWert)
        exaktWert(entferntWert, struct.unpack('>I', anfänglichStatuswert[20:])[0])
        entferntWert.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        entferntWert.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        bildpunktPrüfen((breiteWert-1, höheWert-1), (24, 32, 48))
        def pausierenKurzzeitigTun(sekundenWert=.25):
            endung=time.monotonic()+sekundenWert
            while time.monotonic()<endung:
                for ereignis,_ in Auswähler.select(.02):
                    Daten=ereignis.fileobj.read(65536)
                    if Daten:protokolldateiAufzeichnung.extend(Daten)
        fenster=[12,48,568,360]
        def größeÜberprüfen():
            spalteWert,zeilennummerWert=(fenster[2]-24)//8,(fenster[3]-56)//16
            Text=befehlshülle('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(spalteWert,zeilennummerWert) in Text,Text
            # tatsächlichDaten fenster 테두리: 단지 größe abfragenWert 값만 바뀐 것이 아닌지 확인한다.
            punktAnStelle(breiteWert-1,10,0);pausierenKurzzeitigTun()
            bildpunktPrüfen((fenster[0],fenster[1]),(32,80,144))
            Zeichnung=bildpunktPrüfen((fenster[0]+fenster[2]-1,fenster[1]+fenster[3]-1),(39,49,64))
            return Zeichnung
        def eckeWert(richtung):
            return (fenster[0]+(3 if richtung in (1,3) else fenster[2]-4),fenster[1]+(3 if richtung<=2 else fenster[3]-4))
        def größeÄndernZiehen(richtung,unterschiedWert,schaltfläche=1):
            ersterOperand,dreiWert=eckeWert(richtung);punktAnStelle(ersterOperand,dreiWert,0);pausierenKurzzeitigTun()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            weißBildpunkt=(ersterOperand-7 if richtung in (1,4) else ersterOperand+7,dreiWert-7)
            bildpunktPrüfen(weißBildpunkt,(255,255,255))
            punktAnStelle(ersterOperand,dreiWert,schaltfläche)
            endeWaagerecht=max(0,min(breiteWert-1,ersterOperand+unterschiedWert[0]));endeSenkrecht=max(0,min(höheWert-1,dreiWert+unterschiedWert[1]))
            punktAnStelle(endeWaagerecht,endeSenkrecht,schaltfläche);punktAnStelle(endeWaagerecht,endeSenkrecht,0);pausierenKurzzeitigTun()
            if schaltfläche==1:
                linksWert,oberkanteWert,breiteSpannweite,Länge=fenster;rechtsWert,unterkanteWert=linksWert+breiteSpannweite,oberkanteWert+Länge
                if richtung in (1,3):linksWert=max(0,min(rechtsWert-360,linksWert+endeWaagerecht-ersterOperand))
                else:rechtsWert=max(linksWert+360,min(breiteWert,rechtsWert+endeWaagerecht-ersterOperand))
                if richtung<=2:oberkanteWert=max(34,min(unterkanteWert-216,oberkanteWert+endeSenkrecht-dreiWert))
                else:unterkanteWert=max(oberkanteWert+216,min(höheWert,unterkanteWert+endeSenkrecht-dreiWert))
                fenster[:]=[linksWert,oberkanteWert,rechtsWert-linksWert,unterkanteWert-oberkanteWert]
        größeÜberprüfen();assert zeigerVerborgen[0]
        größeÄndernZiehen(4,(-100,-60),4);größeÜberprüfen() # rechts 버튼은 크기를 바꾸지 않는다.
        for richtung,unterschiedWert in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            größeÄndernZiehen(richtung,unterschiedWert);größeÜberprüfen()
        # Eingabewert 중인 긴 HangulText 명령은 zeilenumbruch/waagerechtPosition 스크롤과 무관하게 그대로 실행된다.
        langText='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        textSenden("echo '"+langText+"'");pausierenKurzzeitigTun()
        größeÄndernZiehen(4,(-1000,-1000));assert fenster[2:]==[360,216]
        größeÄndernZiehen(4,(breiteWert,höheWert))
        ausführenVorgang=textSenden('\n');abwarten(('\r\n'+langText+'\r\n').encode(),ausführenVorgang);größeÜberprüfen()
        # vi가 bearbeitenWert 중에 Bildschirm 크기를 erneutVersuchenWert 읽고, 저장하지 않은 한글도 유지한다.
        befehlshülle('ftpd start')
        übertragungWert=ftplib.FTP();übertragungWert.encoding='utf-8';übertragungWert.connect('127.0.0.1',portNummer,timeout=20);übertragungWert.login()
        abwarten(b'NORMAL',textSenden('vi /크기자료.txt\n'))
        abwarten(b'INSERT',textSenden('i미저장 한글 Daten\n'));pausierenKurzzeitigTun()
        größeÄndernZiehen(4,(-breiteWert,-höheWert))
        # ANSI zeilennummerWert 이동에 새 zeilennummerWert 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((fenster[3]-56)//16)).encode() in protokolldateiAufzeichnung[-4096:]
        textSenden('작은 창에서도 fortsetzungWert schreiben\n');pausierenKurzzeitigTun()
        größeÄndernZiehen(4,(breiteWert,höheWert))
        textSenden('큰 창에서도 fortsetzungWert schreiben\n');pausierenKurzzeitigTun()
        klickenSchaltfläche(0xff1b);klickenSchaltfläche(0xff1b,False);pausierenKurzzeitigTun()
        abwarten(b'jkoros-native> ',textSenden(':wq\n'))
        inhaltswertWert=bytearray();übertragungWert.retrbinary('RETR 크기자료.txt',inhaltswertWert.extend)
        assert inhaltswertWert=='미저장 한글 Daten\n작은 창에서도 fortsetzungWert schreiben\n큰 창에서도 fortsetzungWert schreiben\n'.encode(),inhaltswertWert
        größeÜberprüfen().save(str(ergebnisPfad/(größeText+'-large.png')))
        # 두 번째 창은 standardwertWert größe, erneutVersuchenWert ersterElementeintrag 창을 고르면 앞에서 바꾼 크기가 유지된다.
        ausführenVorgang=len(protokolldateiAufzeichnung);klickenWert(70,16);abwarten(b'TERMINAL FOCUS 2',ausführenVorgang)
        assert 'TERMINAL SIZE 68x19' in befehlshülle('terminal size')
        ausführenVorgang=len(protokolldateiAufzeichnung);klickenWert(180,16);abwarten(b'TERMINAL FOCUS 1',ausführenVorgang);größeÜberprüfen()
        größeÄndernZiehen(4,(-breiteWert,-höheWert));größeÜberprüfen().save(str(ergebnisPfad/(größeText+'-small.png')))
        # größe wertÄndern rückseiteWert X 닫기도 새로운 rechts 가장자리를 사용한다.
        ausführenVorgang=len(protokolldateiAufzeichnung);klickenWert(fenster[0]+fenster[2]-20,fenster[1]+15);abwarten(b'TERMINAL FOCUS 2',ausführenVorgang)
        assert 'RESIZE CLOSED' in befehlshülle('echo RESIZE CLOSED')
        print('PASS:',größeText,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if übertragungWert:übertragungWert.close()
        if entferntWert:entferntWert.close()
        if prozessWert.poll() is None:
            prozessWert.terminate()
            try:prozessWert.wait(timeout=8)
            except subprocess.TimeoutExpired:prozessWert.kill();prozessWert.wait()
        Auswähler.close();prozessWert.stdout.close();(ergebnisPfad/(größeText+'.log')).write_bytes(protokolldateiAufzeichnung)


def ausführenVorgang():
    ergebnisPfad=projektWurzel/'build/verification/resize';ergebnisPfad.mkdir(parents=True,exist_ok=True)
    protokolldateiAufzeichnung={'passed':False,'kernel_sha256':hashlib.sha256((projektWurzel/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for breiteWert,höheWert in ((640,480),(1920,1080)):
            fensterGrößenänderungPrüfung(breiteWert,höheWert,ergebnisPfad);protokolldateiAufzeichnung['resolutions'].append([breiteWert,höheWert])
        protokolldateiAufzeichnung.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(ergebnisPfad/'report.json').write_text(json.dumps(protokolldateiAufzeichnung,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':ausführenVorgang()
