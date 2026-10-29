#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Provést_příkaz import akce_kořen,příkaz

def Spustit_2():
    cíl_HODNOTA_pozice=akce_kořen/'build/verification/swing';cíl_HODNOTA_pozice.mkdir(parents=True,exist_ok=True)
    Třída_cesta=akce_kořen/'build/verification/new-java';Třída_cesta.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(akce_kořen/'dist/jkoros-native-korean.jar'),'-d',str(Třída_cesta),str(akce_kořen/'zkoušky/자바/Swing_test.java'),str(akce_kořen/'zkoušky/자바/한글창시험.java')])
    ověření_Zpráva={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((akce_kořen/'build/kernel8.img').read_bytes()).hexdigest()};LOGZ_ZÁZNAM=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        data_pozice=subprocess.Popen(příkaz()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        selektor_a916db4e=selectors.DefaultSelector();selektor_a916db4e.register(data_pozice.stdout,selectors.EVENT_READ)
        def úchyt_událost(초단위=.1):
            for 누름값,_ in selektor_a916db4e.select(초단위):
                SEKUNDA_HODNOTA=누름값.fileobj.read(65536)
                if SEKUNDA_HODNOTA:LOGZ_ZÁZNAM.extend(SEKUNDA_HODNOTA)
            assert b'PANIC:' not in LOGZ_ZÁZNAM and b'HALTED' not in LOGZ_ZÁZNAM,LOGZ_ZÁZNAM[-2048:]
        def 기다리기(značka,dobrá_pozice,초단위=50):
            konec_POSUN=time.monotonic()+초단위
            while značka not in LOGZ_ZÁZNAM[dobrá_pozice:]:
                if time.monotonic()>konec_POSUN or data_pozice.poll() is not None:raise AssertionError(LOGZ_ZÁZNAM[dobrá_pozice:].decode('utf-8','replace'))
                úchyt_událost()
            return bytes(LOGZ_ZÁZNAM[dobrá_pozice:])
        def poslat(SEKUNDA_HODNOTA,značka=b'jkoros-native> '):
            dobrá_pozice=len(LOGZ_ZÁZNAM);data_pozice.stdin.write(SEKUNDA_HODNOTA);data_pozice.stdin.flush();return 기다리기(značka,dobrá_pozice)
        def prostředí(řetězec_data):return poslat((řetězec_data+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def zkratka_HODNOTA(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def klepnout_tlačítko(souřadnice_x,Y_souřadnice):return bytes([30,1,1,souřadnice_x&255,souřadnice_x>>8,Y_souřadnice&255,Y_souřadnice>>8,30,1,0,souřadnice_x&255,souřadnice_x>>8,Y_souřadnice&255,Y_souřadnice>>8])
        def příkaz_MODE():
            data_pozice.stdin.write(b'\x1b');data_pozice.stdin.flush();konec_POSUN=time.monotonic()+.2
            while time.monotonic()<konec_POSUN:úchyt_událost(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            prostředí('terminal');úchyt_událost(.3)
            data=(akce_kořen/'build/verification/new-java/Swing_test.class').read_bytes()
            poslat('load Swing_test.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(data),64):poslat(data[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            poslat(b'.\n')
            poslat('java Swing_test\n'.encode(),b'SWING READY')
            konec_POSUN=time.monotonic()+3
            while time.monotonic()<konec_POSUN:úchyt_událost(.1)
            # JFrame centered at (120,100), content at y=130.
            poslat(klepnout_tlačítko(200,210),b'',)  # focus JTextField
            data_pozice.stdin.write('누리'.encode());data_pozice.stdin.flush()
            konec_POSUN=time.monotonic()+.3
            while time.monotonic()<konec_POSUN:úchyt_událost(.05)
            VÝSLEDEK=poslat(klepnout_tlačítko(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOGZ_ZÁZNAM)-len(VÝSLEDEK))
            poslat(zkratka_HODNOTA(1),b'TERMINAL FOCUS 2')
            VÝSLEDEK=prostředí('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in VÝSLEDEK
            poslat(klepnout_tlačítko(180,12),b'TERMINAL FOCUS 1')
            konec_POSUN=time.monotonic()+.3
            while time.monotonic()<konec_POSUN:úchyt_událost(.05)
            with socket.socket(socket.AF_UNIX) as bod_kódu:
                bod_kódu.settimeout(10);bod_kódu.connect(str(모의제어접속))
                with bod_kódu.makefile('rwb') as Soubor_položka:
                    json.loads(Soubor_položka.readline())
                    for žádost_HODNOTA in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(cíl_HODNOTA_pozice/'native-swing.png'),'format':'png'}}):
                        Soubor_položka.write((json.dumps(žádost_HODNOTA)+'\n').encode());Soubor_položka.flush()
                        while True:
                            반환값=json.loads(Soubor_položka.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            poslat(klepnout_tlačítko(505,115))
            prostředí('echo SWING_CLOSED_OK')
            data=(Třída_cesta/'한글창시험.class').read_bytes()
            poslat('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(data),64):poslat(data[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            poslat(b'.\n')
            poslat('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            poslat(klepnout_tlačítko(200,255),'KOREAN SWING CLICK Název'.encode())
            poslat(klepnout_tlačítko(505,115))
            prostředí('echo KOREAN_SWING_CLOSED_OK')
            ověření_Zpráva.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','čeština Okno/tlačítko/Akce_povinnost_zvěřejnit/událost_fronta directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if data_pozice.poll() is None:data_pozice.terminate()
            try:data_pozice.wait(timeout=5)
            except subprocess.TimeoutExpired:data_pozice.kill();data_pozice.wait()
            selektor_a916db4e.close();data_pozice.stdin.close();data_pozice.stdout.close();(cíl_HODNOTA_pozice/'serial.log').write_bytes(LOGZ_ZÁZNAM);(cíl_HODNOTA_pozice/'report.json').write_text(json.dumps(ověření_Zpráva,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Spustit_2()
