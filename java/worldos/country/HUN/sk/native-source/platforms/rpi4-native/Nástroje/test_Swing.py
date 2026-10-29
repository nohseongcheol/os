#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Vykonať_príkaz import akcia_koreň,Príkaz

def Spustiť_2():
    cieľ_VALUE_pozícia=akcia_koreň/'build/verification/swing';cieľ_VALUE_pozícia.mkdir(parents=True,exist_ok=True)
    lekcia_cesta=akcia_koreň/'build/verification/new-java';lekcia_cesta.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(akcia_koreň/'dist/jkoros-native-korean.jar'),'-d',str(lekcia_cesta),str(akcia_koreň/'시험/자바/Swing_test.java'),str(akcia_koreň/'시험/자바/한글창시험.java')])
    overenie_správa={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((akcia_koreň/'build/kernel8.img').read_bytes()).hexdigest()};LOG_RECORD=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        údaje_pozícia=subprocess.Popen(Príkaz()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        selektor_a916db4e=selectors.DefaultSelector();selektor_a916db4e.register(údaje_pozícia.stdout,selectors.EVENT_READ)
        def rukoväť_udalosť(초단위=.1):
            for 누름값,_ in selektor_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_RECORD.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_RECORD and b'HALTED' not in LOG_RECORD,LOG_RECORD[-2048:]
        def 기다리기(fixka,v_termíne_splatnosti_pozícia,초단위=50):
            ukončiť_hovor_Posun=time.monotonic()+초단위
            while fixka not in LOG_RECORD[v_termíne_splatnosti_pozícia:]:
                if time.monotonic()>ukončiť_hovor_Posun or údaje_pozícia.poll() is not None:raise AssertionError(LOG_RECORD[v_termíne_splatnosti_pozícia:].decode('utf-8','replace'))
                rukoväť_udalosť()
            return bytes(LOG_RECORD[v_termíne_splatnosti_pozícia:])
        def odoslať(SECOND_VALUE,fixka=b'jkoros-native> '):
            v_termíne_splatnosti_pozícia=len(LOG_RECORD);údaje_pozícia.stdin.write(SECOND_VALUE);údaje_pozícia.stdin.flush();return 기다리기(fixka,v_termíne_splatnosti_pozícia)
        def 셸(reťazec_údaje):return odoslať((reťazec_údaje+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def odkaz_VALUE_910d9d5a(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def kliknúť_tlačidlo(X_súradnica,Y_súradnica):return bytes([30,1,1,X_súradnica&255,X_súradnica>>8,Y_súradnica&255,Y_súradnica>>8,30,1,0,X_súradnica&255,X_súradnica>>8,Y_súradnica&255,Y_súradnica>>8])
        def príkaz_MODE():
            údaje_pozícia.stdin.write(b'\x1b');údaje_pozícia.stdin.flush();ukončiť_hovor_Posun=time.monotonic()+.2
            while time.monotonic()<ukončiť_hovor_Posun:rukoväť_udalosť(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            셸('terminal');rukoväť_udalosť(.3)
            údaje=(akcia_koreň/'build/verification/new-java/Swing_test.class').read_bytes()
            odoslať('load Swing_test.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(údaje),64):odoslať(údaje[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            odoslať(b'.\n')
            odoslať('java Swing_test\n'.encode(),b'SWING READY')
            ukončiť_hovor_Posun=time.monotonic()+3
            while time.monotonic()<ukončiť_hovor_Posun:rukoväť_udalosť(.1)
            # JFrame centered at (120,100), content at y=130.
            odoslať(kliknúť_tlačidlo(200,210),b'',)  # focus JTextField
            údaje_pozícia.stdin.write('누리'.encode());údaje_pozícia.stdin.flush()
            ukončiť_hovor_Posun=time.monotonic()+.3
            while time.monotonic()<ukončiť_hovor_Posun:rukoväť_udalosť(.05)
            KR=odoslať(kliknúť_tlačidlo(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_RECORD)-len(KR))
            odoslať(odkaz_VALUE_910d9d5a(1),b'TERMINAL FOCUS 2')
            KR=셸('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in KR
            odoslať(kliknúť_tlačidlo(180,12),b'TERMINAL FOCUS 1')
            ukončiť_hovor_Posun=time.monotonic()+.3
            while time.monotonic()<ukončiť_hovor_Posun:rukoväť_udalosť(.05)
            with socket.socket(socket.AF_UNIX) as bod_kódu:
                bod_kódu.settimeout(10);bod_kódu.connect(str(모의제어접속))
                with bod_kódu.makefile('rwb') as Súbor_položka:
                    json.loads(Súbor_položka.readline())
                    for požiadavka_VALUE_625fa62c in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(cieľ_VALUE_pozícia/'native-swing.png'),'format':'png'}}):
                        Súbor_položka.write((json.dumps(požiadavka_VALUE_625fa62c)+'\n').encode());Súbor_položka.flush()
                        while True:
                            반환값=json.loads(Súbor_položka.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            odoslať(kliknúť_tlačidlo(505,115))
            셸('echo SWING_CLOSED_OK')
            údaje=(lekcia_cesta/'한글창시험.class').read_bytes()
            odoslať('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(údaje),64):odoslať(údaje[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            odoslať(b'.\n')
            odoslať('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            odoslať(kliknúť_tlačidlo(200,255),'KOREAN SWING CLICK Názov'.encode())
            odoslať(kliknúť_tlačidlo(505,115))
            셸('echo KOREAN_SWING_CLOSED_OK')
            overenie_správa.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','Slovenský Okno/Tlačidlo/Akcia_upozornenie/udalosť_front directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if údaje_pozícia.poll() is None:údaje_pozícia.terminate()
            try:údaje_pozícia.wait(timeout=5)
            except subprocess.TimeoutExpired:údaje_pozícia.kill();údaje_pozícia.wait()
            selektor_a916db4e.close();údaje_pozícia.stdin.close();údaje_pozícia.stdout.close();(cieľ_VALUE_pozícia/'serial.log').write_bytes(LOG_RECORD);(cieľ_VALUE_pozícia/'report.json').write_text(json.dumps(overenie_správa,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Spustiť_2()
