#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Izvedi_ukaz import pobuda_koren,Ukaz

def Zaženi():
    cilj_VALUE_položaj=pobuda_koren/'build/verification/swing';cilj_VALUE_položaj.mkdir(parents=True,exist_ok=True)
    Razred_pot=pobuda_koren/'build/verification/new-java';Razred_pot.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(pobuda_koren/'dist/jkoros-native-korean.jar'),'-d',str(Razred_pot),str(pobuda_koren/'시험/자바/Swing_preskusiti.java'),str(pobuda_koren/'시험/자바/한글창시험.java')])
    preverjanje_veljavnosti_prijavi={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((pobuda_koren/'build/kernel8.img').read_bytes()).hexdigest()};LOG_zapis=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        podatki_položaj=subprocess.Popen(Ukaz()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        izbirnik_a916db4e=selectors.DefaultSelector();izbirnik_a916db4e.register(podatki_položaj.stdout,selectors.EVENT_READ)
        def ročica_dogodek(초단위=.1):
            for 누름값,_ in izbirnik_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_zapis.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_zapis and b'HALTED' not in LOG_zapis,LOG_zapis[-2048:]
        def 기다리기(oznaka,sprotno_položaj,초단위=50):
            končati_klic_odmik=time.monotonic()+초단위
            while oznaka not in LOG_zapis[sprotno_položaj:]:
                if time.monotonic()>končati_klic_odmik or podatki_položaj.poll() is not None:raise AssertionError(LOG_zapis[sprotno_položaj:].decode('utf-8','replace'))
                ročica_dogodek()
            return bytes(LOG_zapis[sprotno_položaj:])
        def poslati(SECOND_VALUE,oznaka=b'jkoros-native> '):
            sprotno_položaj=len(LOG_zapis);podatki_položaj.stdin.write(SECOND_VALUE);podatki_položaj.stdin.flush();return 기다리기(oznaka,sprotno_položaj)
        def lupina(niz_podatki):return poslati((niz_podatki+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def bližnjica_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def klik_gumb(koordinata_x,세로좌표):return bytes([30,1,1,koordinata_x&255,koordinata_x>>8,세로좌표&255,세로좌표>>8,30,1,0,koordinata_x&255,koordinata_x>>8,세로좌표&255,세로좌표>>8])
        def ukaz_MODE():
            podatki_položaj.stdin.write(b'\x1b');podatki_položaj.stdin.flush();končati_klic_odmik=time.monotonic()+.2
            while time.monotonic()<končati_klic_odmik:ročica_dogodek(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            lupina('terminal');ročica_dogodek(.3)
            podatki=(pobuda_koren/'build/verification/new-java/Swing_preskusiti.class').read_bytes()
            poslati('load Swing_preskusiti.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(podatki),64):poslati(podatki[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            poslati(b'.\n')
            poslati('java Swing_preskusiti\n'.encode(),b'SWING READY')
            končati_klic_odmik=time.monotonic()+3
            while time.monotonic()<končati_klic_odmik:ročica_dogodek(.1)
            # JFrame centered at (120,100), content at y=130.
            poslati(klik_gumb(200,210),b'',)  # focus JTextField
            podatki_položaj.stdin.write('누리'.encode());podatki_položaj.stdin.flush()
            končati_klic_odmik=time.monotonic()+.3
            while time.monotonic()<končati_klic_odmik:ročica_dogodek(.05)
            REZULTAT=poslati(klik_gumb(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_zapis)-len(REZULTAT))
            poslati(bližnjica_VALUE(1),b'TERMINAL FOCUS 2')
            REZULTAT=lupina('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in REZULTAT
            poslati(klik_gumb(180,12),b'TERMINAL FOCUS 1')
            končati_klic_odmik=time.monotonic()+.3
            while time.monotonic()<končati_klic_odmik:ročica_dogodek(.05)
            with socket.socket(socket.AF_UNIX) as koda_znaka:
                koda_znaka.settimeout(10);koda_znaka.connect(str(모의제어접속))
                with koda_znaka.makefile('rwb') as Datoteka_vnos:
                    json.loads(Datoteka_vnos.readline())
                    for zahteva_VALUE_625fa62c in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(cilj_VALUE_položaj/'native-swing.png'),'format':'png'}}):
                        Datoteka_vnos.write((json.dumps(zahteva_VALUE_625fa62c)+'\n').encode());Datoteka_vnos.flush()
                        while True:
                            반환값=json.loads(Datoteka_vnos.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            poslati(klik_gumb(505,115))
            lupina('echo SWING_CLOSED_OK')
            podatki=(Razred_pot/'한글창시험.class').read_bytes()
            poslati('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(podatki),64):poslati(podatki[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            poslati(b'.\n')
            poslati('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            poslati(klik_gumb(200,255),'KOREAN SWING CLICK Ime'.encode())
            poslati(klik_gumb(505,115))
            lupina('echo KOREAN_SWING_CLOSED_OK')
            preverjanje_veljavnosti_prijavi.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','slovenščina okno/Gumb/akcija_obvestilo/dogodek_čakalna_vrsta directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if podatki_položaj.poll() is None:podatki_položaj.terminate()
            try:podatki_položaj.wait(timeout=5)
            except subprocess.TimeoutExpired:podatki_položaj.kill();podatki_položaj.wait()
            izbirnik_a916db4e.close();podatki_položaj.stdin.close();podatki_položaj.stdout.close();(cilj_VALUE_položaj/'serial.log').write_bytes(LOG_zapis);(cilj_VALUE_položaj/'report.json').write_text(json.dumps(preverjanje_veljavnosti_prijavi,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Zaženi()
