#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from ausféieren_Befeel import projezéieren_Racinn,Befeel

def Laf():
    Zil_VALUE_positionéieren=projezéieren_Racinn/'build/verification/swing';Zil_VALUE_positionéieren.mkdir(parents=True,exist_ok=True)
    Klass_Wee=projezéieren_Racinn/'build/verification/new-java';Klass_Wee.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(projezéieren_Racinn/'dist/jkoros-native-korean.jar'),'-d',str(Klass_Wee),str(projezéieren_Racinn/'시험/자바/스윙시험.java'),str(projezéieren_Racinn/'시험/자바/한글창시험.java')])
    Validatioun_mellen={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((projezéieren_Racinn/'build/kernel8.img').read_bytes()).hexdigest()};LOG_Rei=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        Daten_positionéieren=subprocess.Popen(Befeel()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        Selekteur_a916db4e=selectors.DefaultSelector();Selekteur_a916db4e.register(Daten_positionéieren.stdout,selectors.EVENT_READ)
        def Handle_Evenement(초단위=.1):
            for 누름값,_ in Selekteur_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_Rei.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_Rei and b'HALTED' not in LOG_Rei,LOG_Rei[-2048:]
        def 기다리기(Markéierung,현재위치,초단위=50):
            bëennegen_OFFSET=time.monotonic()+초단위
            while Markéierung not in LOG_Rei[현재위치:]:
                if time.monotonic()>bëennegen_OFFSET or Daten_positionéieren.poll() is not None:raise AssertionError(LOG_Rei[현재위치:].decode('utf-8','replace'))
                Handle_Evenement()
            return bytes(LOG_Rei[현재위치:])
        def mailen(SECOND_VALUE,Markéierung=b'jkoros-native> '):
            현재위치=len(LOG_Rei);Daten_positionéieren.stdin.write(SECOND_VALUE);Daten_positionéieren.stdin.flush();return 기다리기(Markéierung,현재위치)
        def Shell(Zeechefolleg_Daten):return mailen((Zeechefolleg_Daten+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def Ofkierzung_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def klicken_Tast(X_Koordinat,세로좌표):return bytes([30,1,1,X_Koordinat&255,X_Koordinat>>8,세로좌표&255,세로좌표>>8,30,1,0,X_Koordinat&255,X_Koordinat>>8,세로좌표&255,세로좌표>>8])
        def Befeel_MODE():
            Daten_positionéieren.stdin.write(b'\x1b');Daten_positionéieren.stdin.flush();bëennegen_OFFSET=time.monotonic()+.2
            while time.monotonic()<bëennegen_OFFSET:Handle_Evenement(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            Shell('terminal');Handle_Evenement(.3)
            Daten=(projezéieren_Racinn/'build/verification/new-java/스윙시험.class').read_bytes()
            mailen('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(Daten),64):mailen(Daten[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            mailen(b'.\n')
            mailen('java 스윙시험\n'.encode(),b'SWING READY')
            bëennegen_OFFSET=time.monotonic()+3
            while time.monotonic()<bëennegen_OFFSET:Handle_Evenement(.1)
            # JFrame centered at (120,100), content at y=130.
            mailen(klicken_Tast(200,210),b'',)  # focus JTextField
            Daten_positionéieren.stdin.write('누리'.encode());Daten_positionéieren.stdin.flush()
            bëennegen_OFFSET=time.monotonic()+.3
            while time.monotonic()<bëennegen_OFFSET:Handle_Evenement(.05)
            Mooss=mailen(klicken_Tast(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_Rei)-len(Mooss))
            mailen(Ofkierzung_VALUE(1),b'TERMINAL FOCUS 2')
            Mooss=Shell('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in Mooss
            mailen(klicken_Tast(180,12),b'TERMINAL FOCUS 1')
            bëennegen_OFFSET=time.monotonic()+.3
            while time.monotonic()<bëennegen_OFFSET:Handle_Evenement(.05)
            with socket.socket(socket.AF_UNIX) as Zeechecode:
                Zeechecode.settimeout(10);Zeechecode.connect(str(모의제어접속))
                with Zeechecode.makefile('rwb') as Fichier_Agab:
                    json.loads(Fichier_Agab.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(Zil_VALUE_positionéieren/'native-swing.png'),'format':'png'}}):
                        Fichier_Agab.write((json.dumps(요청값)+'\n').encode());Fichier_Agab.flush()
                        while True:
                            반환값=json.loads(Fichier_Agab.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            mailen(klicken_Tast(505,115))
            Shell('echo SWING_CLOSED_OK')
            Daten=(Klass_Wee/'한글창시험.class').read_bytes()
            mailen('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(Daten),64):mailen(Daten[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            mailen(b'.\n')
            mailen('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            mailen(klicken_Tast(200,255),'KOREAN SWING CLICK Numm'.encode())
            mailen(klicken_Tast(505,115))
            Shell('echo KOREAN_SWING_CLOSED_OK')
            Validatioun_mellen.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 Fënster/Tast/동작알림/Evenement_Schlaang directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if Daten_positionéieren.poll() is None:Daten_positionéieren.terminate()
            try:Daten_positionéieren.wait(timeout=5)
            except subprocess.TimeoutExpired:Daten_positionéieren.kill();Daten_positionéieren.wait()
            Selekteur_a916db4e.close();Daten_positionéieren.stdin.close();Daten_positionéieren.stdout.close();(Zil_VALUE_positionéieren/'serial.log').write_bytes(LOG_Rei);(Zil_VALUE_positionéieren/'report.json').write_text(json.dumps(Validatioun_mellen,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Laf()
