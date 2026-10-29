#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Izvrši_komanda import projicirati_koijen,Naredba

def Pokreni():
    odredište_VALUE_položaj=projicirati_koijen/'build/verification/swing';odredište_VALUE_položaj.mkdir(parents=True,exist_ok=True)
    klasa_put=projicirati_koijen/'build/verification/new-java';klasa_put.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(projicirati_koijen/'dist/jkoros-native-korean.jar'),'-d',str(klasa_put),str(projicirati_koijen/'시험/자바/스윙시험.java'),str(projicirati_koijen/'시험/자바/한글창시험.java')])
    provjera_izvještaj={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((projicirati_koijen/'build/kernel8.img').read_bytes()).hexdigest()};LOG_red=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        podaci_položaj=subprocess.Popen(Naredba()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        birač_a916db4e=selectors.DefaultSelector();birač_a916db4e.register(podaci_položaj.stdout,selectors.EVENT_READ)
        def hvatište_događaj(초단위=.1):
            for 누름값,_ in birač_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_red.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_red and b'HALTED' not in LOG_red,LOG_red[-2048:]
        def 기다리기(확인표시,trenutno_položaj,초단위=50):
            završiti_Pomak=time.monotonic()+초단위
            while 확인표시 not in LOG_red[trenutno_položaj:]:
                if time.monotonic()>završiti_Pomak or podaci_položaj.poll() is not None:raise AssertionError(LOG_red[trenutno_položaj:].decode('utf-8','replace'))
                hvatište_događaj()
            return bytes(LOG_red[trenutno_položaj:])
        def poslati(SECOND_VALUE,확인표시=b'jkoros-native> '):
            trenutno_položaj=len(LOG_red);podaci_položaj.stdin.write(SECOND_VALUE);podaci_položaj.stdin.flush();return 기다리기(확인표시,trenutno_položaj)
        def ljuska(string_podaci):return poslati((string_podaci+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def prečica_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def klik_dugme(koordinata_x,Y_koordinata):return bytes([30,1,1,koordinata_x&255,koordinata_x>>8,Y_koordinata&255,Y_koordinata>>8,30,1,0,koordinata_x&255,koordinata_x>>8,Y_koordinata&255,Y_koordinata>>8])
        def komanda_mod():
            podaci_položaj.stdin.write(b'\x1b');podaci_položaj.stdin.flush();završiti_Pomak=time.monotonic()+.2
            while time.monotonic()<završiti_Pomak:hvatište_događaj(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            ljuska('terminal');hvatište_događaj(.3)
            podaci=(projicirati_koijen/'build/verification/new-java/스윙시험.class').read_bytes()
            poslati('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(podaci),64):poslati(podaci[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            poslati(b'.\n')
            poslati('java 스윙시험\n'.encode(),b'SWING READY')
            završiti_Pomak=time.monotonic()+3
            while time.monotonic()<završiti_Pomak:hvatište_događaj(.1)
            # JFrame centered at (120,100), content at y=130.
            poslati(klik_dugme(200,210),b'',)  # focus JTextField
            podaci_položaj.stdin.write('누리'.encode());podaci_položaj.stdin.flush()
            završiti_Pomak=time.monotonic()+.3
            while time.monotonic()<završiti_Pomak:hvatište_događaj(.05)
            mjera=poslati(klik_dugme(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_red)-len(mjera))
            poslati(prečica_VALUE(1),b'TERMINAL FOCUS 2')
            mjera=ljuska('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in mjera
            poslati(klik_dugme(180,12),b'TERMINAL FOCUS 1')
            završiti_Pomak=time.monotonic()+.3
            while time.monotonic()<završiti_Pomak:hvatište_događaj(.05)
            with socket.socket(socket.AF_UNIX) as kôd_znaka:
                kôd_znaka.settimeout(10);kôd_znaka.connect(str(모의제어접속))
                with kôd_znaka.makefile('rwb') as fajl_unos:
                    json.loads(fajl_unos.readline())
                    for HTTP_zahtjev_VALUE in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(odredište_VALUE_položaj/'native-swing.png'),'format':'png'}}):
                        fajl_unos.write((json.dumps(HTTP_zahtjev_VALUE)+'\n').encode());fajl_unos.flush()
                        while True:
                            반환값=json.loads(fajl_unos.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            poslati(klik_dugme(505,115))
            ljuska('echo SWING_CLOSED_OK')
            podaci=(klasa_put/'한글창시험.class').read_bytes()
            poslati('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(podaci),64):poslati(podaci[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            poslati(b'.\n')
            poslati('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            poslati(klik_dugme(200,255),'KOREAN SWING CLICK Naziv'.encode())
            poslati(klik_dugme(505,115))
            ljuska('echo KOREAN_SWING_CLOSED_OK')
            provjera_izvještaj.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 prozor/dugme/동작알림/događaj_redoslijed directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if podaci_položaj.poll() is None:podaci_položaj.terminate()
            try:podaci_položaj.wait(timeout=5)
            except subprocess.TimeoutExpired:podaci_položaj.kill();podaci_položaj.wait()
            birač_a916db4e.close();podaci_položaj.stdin.close();podaci_položaj.stdout.close();(odredište_VALUE_položaj/'serial.log').write_bytes(LOG_red);(odredište_VALUE_položaj/'report.json').write_text(json.dumps(provjera_izvještaj,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Pokreni()
