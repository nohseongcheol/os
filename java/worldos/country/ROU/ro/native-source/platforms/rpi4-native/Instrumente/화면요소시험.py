#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from executa_comandă import Project_rădăcină,Comandă

def Pornește():
    destinație_VALUE_poziție=Project_rădăcină/'build/verification/swing';destinație_VALUE_poziție.mkdir(parents=True,exist_ok=True)
    Clasă_cale=Project_rădăcină/'build/verification/new-java';Clasă_cale.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(Project_rădăcină/'dist/jkoros-native-korean.jar'),'-d',str(Clasă_cale),str(Project_rădăcină/'시험/자바/스윙시험.java'),str(Project_rădăcină/'시험/자바/한글창시험.java')])
    validare_raport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_rădăcină/'build/kernel8.img').read_bytes()).hexdigest()};LOG_RECORD=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        date_poziție=subprocess.Popen(Comandă()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        selector_a916db4e=selectors.DefaultSelector();selector_a916db4e.register(date_poziție.stdout,selectors.EVENT_READ)
        def handle_eveniment(초단위=.1):
            for 누름값,_ in selector_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_RECORD.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_RECORD and b'HALTED' not in LOG_RECORD,LOG_RECORD[-2048:]
        def 기다리기(marcaj,curent_poziție,초단위=50):
            termina_un_apel_OFFSET=time.monotonic()+초단위
            while marcaj not in LOG_RECORD[curent_poziție:]:
                if time.monotonic()>termina_un_apel_OFFSET or date_poziție.poll() is not None:raise AssertionError(LOG_RECORD[curent_poziție:].decode('utf-8','replace'))
                handle_eveniment()
            return bytes(LOG_RECORD[curent_poziție:])
        def trimite(SECOND_VALUE,marcaj=b'jkoros-native> '):
            curent_poziție=len(LOG_RECORD);date_poziție.stdin.write(SECOND_VALUE);date_poziție.stdin.flush();return 기다리기(marcaj,curent_poziție)
        def shell(șir_date):return trimite((șir_date+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def comandă_rapidă_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def clic_buton(coordonata_X,세로좌표):return bytes([30,1,1,coordonata_X&255,coordonata_X>>8,세로좌표&255,세로좌표>>8,30,1,0,coordonata_X&255,coordonata_X>>8,세로좌표&255,세로좌표>>8])
        def comandă_mod():
            date_poziție.stdin.write(b'\x1b');date_poziție.stdin.flush();termina_un_apel_OFFSET=time.monotonic()+.2
            while time.monotonic()<termina_un_apel_OFFSET:handle_eveniment(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            shell('terminal');handle_eveniment(.3)
            date=(Project_rădăcină/'build/verification/new-java/스윙시험.class').read_bytes()
            trimite('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(date),64):trimite(date[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            trimite(b'.\n')
            trimite('java 스윙시험\n'.encode(),b'SWING READY')
            termina_un_apel_OFFSET=time.monotonic()+3
            while time.monotonic()<termina_un_apel_OFFSET:handle_eveniment(.1)
            # JFrame centered at (120,100), content at y=130.
            trimite(clic_buton(200,210),b'',)  # focus JTextField
            date_poziție.stdin.write('누리'.encode());date_poziție.stdin.flush()
            termina_un_apel_OFFSET=time.monotonic()+.3
            while time.monotonic()<termina_un_apel_OFFSET:handle_eveniment(.05)
            KR=trimite(clic_buton(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_RECORD)-len(KR))
            trimite(comandă_rapidă_VALUE(1),b'TERMINAL FOCUS 2')
            KR=shell('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in KR
            trimite(clic_buton(180,12),b'TERMINAL FOCUS 1')
            termina_un_apel_OFFSET=time.monotonic()+.3
            while time.monotonic()<termina_un_apel_OFFSET:handle_eveniment(.05)
            with socket.socket(socket.AF_UNIX) as cod_caracter:
                cod_caracter.settimeout(10);cod_caracter.connect(str(모의제어접속))
                with cod_caracter.makefile('rwb') as Fișier_intrare:
                    json.loads(Fișier_intrare.readline())
                    for cerere_VALUE in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(destinație_VALUE_poziție/'native-swing.png'),'format':'png'}}):
                        Fișier_intrare.write((json.dumps(cerere_VALUE)+'\n').encode());Fișier_intrare.flush()
                        while True:
                            반환값=json.loads(Fișier_intrare.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            trimite(clic_buton(505,115))
            shell('echo SWING_CLOSED_OK')
            date=(Clasă_cale/'한글창시험.class').read_bytes()
            trimite('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(date),64):trimite(date[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            trimite(b'.\n')
            trimite('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            trimite(clic_buton(200,255),'KOREAN SWING CLICK Nume'.encode())
            trimite(clic_buton(505,115))
            shell('echo KOREAN_SWING_CLOSED_OK')
            validare_raport.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','Română Fereastră/buton/Acțiune_înștiințare/eveniment_coadă directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if date_poziție.poll() is None:date_poziție.terminate()
            try:date_poziție.wait(timeout=5)
            except subprocess.TimeoutExpired:date_poziție.kill();date_poziție.wait()
            selector_a916db4e.close();date_poziție.stdin.close();date_poziție.stdout.close();(destinație_VALUE_poziție/'serial.log').write_bytes(LOG_RECORD);(destinație_VALUE_poziție/'report.json').write_text(json.dumps(validare_raport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Pornește()
