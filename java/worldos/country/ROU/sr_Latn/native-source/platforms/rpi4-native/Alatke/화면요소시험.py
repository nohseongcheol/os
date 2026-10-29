#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Izvrši_komanda import radnja_koren,komanda

def koristiti():
    odredište_VALUE_pozicija=radnja_koren/'build/verification/swing';odredište_VALUE_pozicija.mkdir(parents=True,exist_ok=True)
    Razred_putanja=radnja_koren/'build/verification/new-java';Razred_putanja.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(radnja_koren/'dist/jkoros-native-korean.jar'),'-d',str(Razred_putanja),str(radnja_koren/'시험/자바/스윙시험.java'),str(radnja_koren/'시험/자바/한글창시험.java')])
    provera_valjanosti_izveštaj={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((radnja_koren/'build/kernel8.img').read_bytes()).hexdigest()};LOG_snimi=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        podaci_pozicija=subprocess.Popen(komanda()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        birač_a916db4e=selectors.DefaultSelector();birač_a916db4e.register(podaci_pozicija.stdout,selectors.EVENT_READ)
        def pokazivač_događaj(초단위=.1):
            for 누름값,_ in birač_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_snimi.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_snimi and b'HALTED' not in LOG_snimi,LOG_snimi[-2048:]
        def 기다리기(označivač,aktuelno_pozicija,초단위=50):
            završiti_razgovor_Pomak=time.monotonic()+초단위
            while označivač not in LOG_snimi[aktuelno_pozicija:]:
                if time.monotonic()>završiti_razgovor_Pomak or podaci_pozicija.poll() is not None:raise AssertionError(LOG_snimi[aktuelno_pozicija:].decode('utf-8','replace'))
                pokazivač_događaj()
            return bytes(LOG_snimi[aktuelno_pozicija:])
        def poslati(SECOND_VALUE,označivač=b'jkoros-native> '):
            aktuelno_pozicija=len(LOG_snimi);podaci_pozicija.stdin.write(SECOND_VALUE);podaci_pozicija.stdin.flush();return 기다리기(označivač,aktuelno_pozicija)
        def ljuska(niska_podaci):return poslati((niska_podaci+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def prečica_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def klik_taster(x_koordinata,세로좌표):return bytes([30,1,1,x_koordinata&255,x_koordinata>>8,세로좌표&255,세로좌표>>8,30,1,0,x_koordinata&255,x_koordinata>>8,세로좌표&255,세로좌표>>8])
        def komanda_MODE():
            podaci_pozicija.stdin.write(b'\x1b');podaci_pozicija.stdin.flush();završiti_razgovor_Pomak=time.monotonic()+.2
            while time.monotonic()<završiti_razgovor_Pomak:pokazivač_događaj(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            ljuska('terminal');pokazivač_događaj(.3)
            podaci=(radnja_koren/'build/verification/new-java/스윙시험.class').read_bytes()
            poslati('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(podaci),64):poslati(podaci[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            poslati(b'.\n')
            poslati('java 스윙시험\n'.encode(),b'SWING READY')
            završiti_razgovor_Pomak=time.monotonic()+3
            while time.monotonic()<završiti_razgovor_Pomak:pokazivač_događaj(.1)
            # JFrame centered at (120,100), content at y=130.
            poslati(klik_taster(200,210),b'',)  # focus JTextField
            podaci_pozicija.stdin.write('누리'.encode());podaci_pozicija.stdin.flush()
            završiti_razgovor_Pomak=time.monotonic()+.3
            while time.monotonic()<završiti_razgovor_Pomak:pokazivač_događaj(.05)
            KR=poslati(klik_taster(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_snimi)-len(KR))
            poslati(prečica_VALUE(1),b'TERMINAL FOCUS 2')
            KR=ljuska('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in KR
            poslati(klik_taster(180,12),b'TERMINAL FOCUS 1')
            završiti_razgovor_Pomak=time.monotonic()+.3
            while time.monotonic()<završiti_razgovor_Pomak:pokazivač_događaj(.05)
            with socket.socket(socket.AF_UNIX) as kôd_znaka:
                kôd_znaka.settimeout(10);kôd_znaka.connect(str(모의제어접속))
                with kôd_znaka.makefile('rwb') as Datoteka_stavka:
                    json.loads(Datoteka_stavka.readline())
                    for zahtev_VALUE_625fa62c in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(odredište_VALUE_pozicija/'native-swing.png'),'format':'png'}}):
                        Datoteka_stavka.write((json.dumps(zahtev_VALUE_625fa62c)+'\n').encode());Datoteka_stavka.flush()
                        while True:
                            반환값=json.loads(Datoteka_stavka.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            poslati(klik_taster(505,115))
            ljuska('echo SWING_CLOSED_OK')
            podaci=(Razred_putanja/'한글창시험.class').read_bytes()
            poslati('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(podaci),64):poslati(podaci[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            poslati(b'.\n')
            poslati('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            poslati(klik_taster(200,255),'KOREAN SWING CLICK ime'.encode())
            poslati(klik_taster(505,115))
            ljuska('echo KOREAN_SWING_CLOSED_OK')
            provera_valjanosti_izveštaj.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 prozor/taster/radnja_obaveštavanje/događaj_red directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if podaci_pozicija.poll() is None:podaci_pozicija.terminate()
            try:podaci_pozicija.wait(timeout=5)
            except subprocess.TimeoutExpired:podaci_pozicija.kill();podaci_pozicija.wait()
            birač_a916db4e.close();podaci_pozicija.stdin.close();podaci_pozicija.stdout.close();(odredište_VALUE_pozicija/'serial.log').write_bytes(LOG_snimi);(odredište_VALUE_pozicija/'report.json').write_text(json.dumps(provera_valjanosti_izveštaj,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':koristiti()
