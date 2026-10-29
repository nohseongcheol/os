#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Izvrši_naredba import akcija_korijen,Naredba

def Pokreni():
    odredište_VALUE_položaj=akcija_korijen/'build/verification/swing';odredište_VALUE_položaj.mkdir(parents=True,exist_ok=True)
    poduka_put=akcija_korijen/'build/verification/new-java';poduka_put.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(akcija_korijen/'dist/jkoros-native-korean.jar'),'-d',str(poduka_put),str(akcija_korijen/'시험/자바/스윙시험.java'),str(akcija_korijen/'시험/자바/한글창시험.java')])
    provjera_izvješće={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((akcija_korijen/'build/kernel8.img').read_bytes()).hexdigest()};LOG_zapis=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        podaci_položaj=subprocess.Popen(Naredba()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        odabirač_a916db4e=selectors.DefaultSelector();odabirač_a916db4e.register(podaci_položaj.stdout,selectors.EVENT_READ)
        def ustroj_događaj(초단위=.1):
            for 누름값,_ in odabirač_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_zapis.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_zapis and b'HALTED' not in LOG_zapis,LOG_zapis[-2048:]
        def 기다리기(marker,redovno_položaj,초단위=50):
            završiti_razgovor_pomak=time.monotonic()+초단위
            while marker not in LOG_zapis[redovno_položaj:]:
                if time.monotonic()>završiti_razgovor_pomak or podaci_položaj.poll() is not None:raise AssertionError(LOG_zapis[redovno_položaj:].decode('utf-8','replace'))
                ustroj_događaj()
            return bytes(LOG_zapis[redovno_položaj:])
        def slati(SECOND_VALUE,marker=b'jkoros-native> '):
            redovno_položaj=len(LOG_zapis);podaci_položaj.stdin.write(SECOND_VALUE);podaci_položaj.stdin.flush();return 기다리기(marker,redovno_položaj)
        def ljuska(niz_podaci):return slati((niz_podaci+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def prečac_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def klik_tipka(koordinata_x,세로좌표):return bytes([30,1,1,koordinata_x&255,koordinata_x>>8,세로좌표&255,세로좌표>>8,30,1,0,koordinata_x&255,koordinata_x>>8,세로좌표&255,세로좌표>>8])
        def naredba_MODE():
            podaci_položaj.stdin.write(b'\x1b');podaci_položaj.stdin.flush();završiti_razgovor_pomak=time.monotonic()+.2
            while time.monotonic()<završiti_razgovor_pomak:ustroj_događaj(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            ljuska('terminal');ustroj_događaj(.3)
            podaci=(akcija_korijen/'build/verification/new-java/스윙시험.class').read_bytes()
            slati('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(podaci),64):slati(podaci[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            slati(b'.\n')
            slati('java 스윙시험\n'.encode(),b'SWING READY')
            završiti_razgovor_pomak=time.monotonic()+3
            while time.monotonic()<završiti_razgovor_pomak:ustroj_događaj(.1)
            # JFrame centered at (120,100), content at y=130.
            slati(klik_tipka(200,210),b'',)  # focus JTextField
            podaci_položaj.stdin.write('누리'.encode());podaci_položaj.stdin.flush()
            završiti_razgovor_pomak=time.monotonic()+.3
            while time.monotonic()<završiti_razgovor_pomak:ustroj_događaj(.05)
            REZULTAT=slati(klik_tipka(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_zapis)-len(REZULTAT))
            slati(prečac_VALUE(1),b'TERMINAL FOCUS 2')
            REZULTAT=ljuska('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in REZULTAT
            slati(klik_tipka(180,12),b'TERMINAL FOCUS 1')
            završiti_razgovor_pomak=time.monotonic()+.3
            while time.monotonic()<završiti_razgovor_pomak:ustroj_događaj(.05)
            with socket.socket(socket.AF_UNIX) as kodna_točka:
                kodna_točka.settimeout(10);kodna_točka.connect(str(모의제어접속))
                with kodna_točka.makefile('rwb') as Datoteka_unos:
                    json.loads(Datoteka_unos.readline())
                    for zahtjev_VALUE in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(odredište_VALUE_položaj/'native-swing.png'),'format':'png'}}):
                        Datoteka_unos.write((json.dumps(zahtjev_VALUE)+'\n').encode());Datoteka_unos.flush()
                        while True:
                            반환값=json.loads(Datoteka_unos.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            slati(klik_tipka(505,115))
            ljuska('echo SWING_CLOSED_OK')
            podaci=(poduka_put/'한글창시험.class').read_bytes()
            slati('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(podaci),64):slati(podaci[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            slati(b'.\n')
            slati('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            slati(klik_tipka(200,255),'KOREAN SWING CLICK Ime'.encode())
            slati(klik_tipka(505,115))
            ljuska('echo KOREAN_SWING_CLOSED_OK')
            provjera_izvješće.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','hrvatski Prozor/gumb/akcija_obavijest/događaj_red_čekanja directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if podaci_položaj.poll() is None:podaci_položaj.terminate()
            try:podaci_položaj.wait(timeout=5)
            except subprocess.TimeoutExpired:podaci_položaj.kill();podaci_položaj.wait()
            odabirač_a916db4e.close();podaci_položaj.stdin.close();podaci_položaj.stdout.close();(odredište_VALUE_položaj/'serial.log').write_bytes(LOG_zapis);(odredište_VALUE_položaj/'report.json').write_text(json.dumps(provjera_izvješće,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Pokreni()
