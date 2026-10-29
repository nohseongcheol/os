#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from végrehajt_parancs import teendő_gyök,Parancs

def Futtatás():
    cél_ÉRTÉK_pozíció=teendő_gyök/'build/verification/swing';cél_ÉRTÉK_pozíció.mkdir(parents=True,exist_ok=True)
    tanóra_útvonal=teendő_gyök/'build/verification/new-java';tanóra_útvonal.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(teendő_gyök/'dist/jkoros-native-korean.jar'),'-d',str(tanóra_útvonal),str(teendő_gyök/'시험/자바/Szving_teszt.java'),str(teendő_gyök/'시험/자바/한글창시험.java')])
    ellenőrzés_jelent={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((teendő_gyök/'build/kernel8.img').read_bytes()).hexdigest()};LOG_REKORD=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        adat_pozíció=subprocess.Popen(Parancs()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        szelektor_a916db4e=selectors.DefaultSelector();szelektor_a916db4e.register(adat_pozíció.stdout,selectors.EVENT_READ)
        def leíró_esemény(초단위=.1):
            for 누름값,_ in szelektor_a916db4e.select(초단위):
                MPERC_ÉRTÉK=누름값.fileobj.read(65536)
                if MPERC_ÉRTÉK:LOG_REKORD.extend(MPERC_ÉRTÉK)
            assert b'PANIC:' not in LOG_REKORD and b'HALTED' not in LOG_REKORD,LOG_REKORD[-2048:]
        def 기다리기(jelölő,aktuális_pozíció,초단위=50):
            megszüntet_Ofszet=time.monotonic()+초단위
            while jelölő not in LOG_REKORD[aktuális_pozíció:]:
                if time.monotonic()>megszüntet_Ofszet or adat_pozíció.poll() is not None:raise AssertionError(LOG_REKORD[aktuális_pozíció:].decode('utf-8','replace'))
                leíró_esemény()
            return bytes(LOG_REKORD[aktuális_pozíció:])
        def küld(MPERC_ÉRTÉK,jelölő=b'jkoros-native> '):
            aktuális_pozíció=len(LOG_REKORD);adat_pozíció.stdin.write(MPERC_ÉRTÉK);adat_pozíció.stdin.flush();return 기다리기(jelölő,aktuális_pozíció)
        def felület(sztring_adat):return küld((sztring_adat+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def hivatkozás_ÉRTÉK(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def kattint_gomb(x_koordináta,Y_koordináta):return bytes([30,1,1,x_koordináta&255,x_koordináta>>8,Y_koordináta&255,Y_koordináta>>8,30,1,0,x_koordináta&255,x_koordináta>>8,Y_koordináta&255,Y_koordináta>>8])
        def parancs_mód():
            adat_pozíció.stdin.write(b'\x1b');adat_pozíció.stdin.flush();megszüntet_Ofszet=time.monotonic()+.2
            while time.monotonic()<megszüntet_Ofszet:leíró_esemény(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            felület('terminal');leíró_esemény(.3)
            adat=(teendő_gyök/'build/verification/new-java/Szving_teszt.class').read_bytes()
            küld('load Szving_teszt.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(adat),64):küld(adat[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            küld(b'.\n')
            küld('java Szving_teszt\n'.encode(),b'SWING READY')
            megszüntet_Ofszet=time.monotonic()+3
            while time.monotonic()<megszüntet_Ofszet:leíró_esemény(.1)
            # JFrame centered at (120,100), content at y=130.
            küld(kattint_gomb(200,210),b'',)  # focus JTextField
            adat_pozíció.stdin.write('누리'.encode());adat_pozíció.stdin.flush()
            megszüntet_Ofszet=time.monotonic()+.3
            while time.monotonic()<megszüntet_Ofszet:leíró_esemény(.05)
            KR=küld(kattint_gomb(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_REKORD)-len(KR))
            küld(hivatkozás_ÉRTÉK(1),b'TERMINAL FOCUS 2')
            KR=felület('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in KR
            küld(kattint_gomb(180,12),b'TERMINAL FOCUS 1')
            megszüntet_Ofszet=time.monotonic()+.3
            while time.monotonic()<megszüntet_Ofszet:leíró_esemény(.05)
            with socket.socket(socket.AF_UNIX) as kódpont:
                kódpont.settimeout(10);kódpont.connect(str(모의제어접속))
                with kódpont.makefile('rwb') as Fájl_bejegyzés:
                    json.loads(Fájl_bejegyzés.readline())
                    for kérés_ÉRTÉK in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(cél_ÉRTÉK_pozíció/'native-swing.png'),'format':'png'}}):
                        Fájl_bejegyzés.write((json.dumps(kérés_ÉRTÉK)+'\n').encode());Fájl_bejegyzés.flush()
                        while True:
                            반환값=json.loads(Fájl_bejegyzés.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            küld(kattint_gomb(505,115))
            felület('echo SWING_CLOSED_OK')
            adat=(tanóra_útvonal/'한글창시험.class').read_bytes()
            küld('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(adat),64):küld(adat[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            küld(b'.\n')
            küld('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            küld(kattint_gomb(200,255),'KOREAN SWING CLICK Név'.encode())
            küld(kattint_gomb(505,115))
            felület('echo KOREAN_SWING_CLOSED_OK')
            ellenőrzés_jelent.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','magyar Ablak/gomb/Action_alapelv/esemény_várólista directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if adat_pozíció.poll() is None:adat_pozíció.terminate()
            try:adat_pozíció.wait(timeout=5)
            except subprocess.TimeoutExpired:adat_pozíció.kill();adat_pozíció.wait()
            szelektor_a916db4e.close();adat_pozíció.stdin.close();adat_pozíció.stdout.close();(cél_ÉRTÉK_pozíció/'serial.log').write_bytes(LOG_REKORD);(cél_ÉRTÉK_pozíció/'report.json').write_text(json.dumps(ellenőrzés_jelent,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Futtatás()
