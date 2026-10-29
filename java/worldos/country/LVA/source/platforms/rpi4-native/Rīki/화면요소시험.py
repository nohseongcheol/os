#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Izpildīt_komanda import Project_sakne,Komanda

def Palaist():
    mērķis_VALUE_amats=Project_sakne/'build/verification/swing';mērķis_VALUE_amats.mkdir(parents=True,exist_ok=True)
    klase_ceļš=Project_sakne/'build/verification/new-java';klase_ceļš.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(Project_sakne/'dist/jkoros-native-korean.jar'),'-d',str(klase_ceļš),str(Project_sakne/'시험/자바/스윙시험.java'),str(Project_sakne/'시험/자바/한글창시험.java')])
    validācija_ziņot={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_sakne/'build/kernel8.img').read_bytes()).hexdigest()};LOG_RECORD=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        dati_amats=subprocess.Popen(Komanda()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        atlasītājs_a916db4e=selectors.DefaultSelector();atlasītājs_a916db4e.register(dati_amats.stdout,selectors.EVENT_READ)
        def turis_notikums(초단위=.1):
            for 누름값,_ in atlasītājs_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_RECORD.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_RECORD and b'HALTED' not in LOG_RECORD,LOG_RECORD[-2048:]
        def 기다리기(marķieris,pašreizējais_amats,초단위=50):
            beigt_zvanu_Nobīde=time.monotonic()+초단위
            while marķieris not in LOG_RECORD[pašreizējais_amats:]:
                if time.monotonic()>beigt_zvanu_Nobīde or dati_amats.poll() is not None:raise AssertionError(LOG_RECORD[pašreizējais_amats:].decode('utf-8','replace'))
                turis_notikums()
            return bytes(LOG_RECORD[pašreizējais_amats:])
        def sūtīt(SECOND_VALUE,marķieris=b'jkoros-native> '):
            pašreizējais_amats=len(LOG_RECORD);dati_amats.stdin.write(SECOND_VALUE);dati_amats.stdin.flush();return 기다리기(marķieris,pašreizējais_amats)
        def čaula(virkne_dati):return sūtīt((virkne_dati+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def saīsne_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def klikšķis_poga(x_koordināta,세로좌표):return bytes([30,1,1,x_koordināta&255,x_koordināta>>8,세로좌표&255,세로좌표>>8,30,1,0,x_koordināta&255,x_koordināta>>8,세로좌표&255,세로좌표>>8])
        def komanda_MODE():
            dati_amats.stdin.write(b'\x1b');dati_amats.stdin.flush();beigt_zvanu_Nobīde=time.monotonic()+.2
            while time.monotonic()<beigt_zvanu_Nobīde:turis_notikums(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            čaula('terminal');turis_notikums(.3)
            dati=(Project_sakne/'build/verification/new-java/스윙시험.class').read_bytes()
            sūtīt('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(dati),64):sūtīt(dati[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            sūtīt(b'.\n')
            sūtīt('java 스윙시험\n'.encode(),b'SWING READY')
            beigt_zvanu_Nobīde=time.monotonic()+3
            while time.monotonic()<beigt_zvanu_Nobīde:turis_notikums(.1)
            # JFrame centered at (120,100), content at y=130.
            sūtīt(klikšķis_poga(200,210),b'',)  # focus JTextField
            dati_amats.stdin.write('누리'.encode());dati_amats.stdin.flush()
            beigt_zvanu_Nobīde=time.monotonic()+.3
            while time.monotonic()<beigt_zvanu_Nobīde:turis_notikums(.05)
            mērs=sūtīt(klikšķis_poga(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_RECORD)-len(mērs))
            sūtīt(saīsne_VALUE(1),b'TERMINAL FOCUS 2')
            mērs=čaula('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in mērs
            sūtīt(klikšķis_poga(180,12),b'TERMINAL FOCUS 1')
            beigt_zvanu_Nobīde=time.monotonic()+.3
            while time.monotonic()<beigt_zvanu_Nobīde:turis_notikums(.05)
            with socket.socket(socket.AF_UNIX) as koda_punkts:
                koda_punkts.settimeout(10);koda_punkts.connect(str(모의제어접속))
                with koda_punkts.makefile('rwb') as Fails_ievade:
                    json.loads(Fails_ievade.readline())
                    for pieprasījums_VALUE in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(mērķis_VALUE_amats/'native-swing.png'),'format':'png'}}):
                        Fails_ievade.write((json.dumps(pieprasījums_VALUE)+'\n').encode());Fails_ievade.flush()
                        while True:
                            반환값=json.loads(Fails_ievade.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            sūtīt(klikšķis_poga(505,115))
            čaula('echo SWING_CLOSED_OK')
            dati=(klase_ceļš/'한글창시험.class').read_bytes()
            sūtīt('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(dati),64):sūtīt(dati[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            sūtīt(b'.\n')
            sūtīt('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            sūtīt(klikšķis_poga(200,255),'KOREAN SWING CLICK Nosaukums'.encode())
            sūtīt(klikšķis_poga(505,115))
            čaula('echo KOREAN_SWING_CLOSED_OK')
            validācija_ziņot.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','Latviešu Logs/Pogas/darbība_informēšana/notikums_rinda directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if dati_amats.poll() is None:dati_amats.terminate()
            try:dati_amats.wait(timeout=5)
            except subprocess.TimeoutExpired:dati_amats.kill();dati_amats.wait()
            atlasītājs_a916db4e.close();dati_amats.stdin.close();dati_amats.stdout.close();(mērķis_VALUE_amats/'serial.log').write_bytes(LOG_RECORD);(mērķis_VALUE_amats/'report.json').write_text(json.dumps(validācija_ziņot,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Palaist()
