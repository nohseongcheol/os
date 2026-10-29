#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Esegui_comando import azione_radice,comando

def avvia():
    meta_VALORE_funzione=azione_radice/'build/verification/swing';meta_VALORE_funzione.mkdir(parents=True,exist_ok=True)
    Corso_percorso=azione_radice/'build/verification/new-java';Corso_percorso.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(azione_radice/'dist/jkoros-native-korean.jar'),'-d',str(Corso_percorso),str(azione_radice/'prove/자바/Swing_test.java'),str(azione_radice/'prove/자바/한글창시험.java')])
    convalida_Report={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((azione_radice/'build/kernel8.img').read_bytes()).hexdigest()};LOG_riga=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        dati_funzione=subprocess.Popen(comando()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        selettore_a916db4e=selectors.DefaultSelector();selettore_a916db4e.register(dati_funzione.stdout,selectors.EVENT_READ)
        def handle_evento(초단위=.1):
            for 누름값,_ in selettore_a916db4e.select(초단위):
                SECONDO_VALORE=누름값.fileobj.read(65536)
                if SECONDO_VALORE:LOG_riga.extend(SECONDO_VALORE)
            assert b'PANIC:' not in LOG_riga and b'HALTED' not in LOG_riga,LOG_riga[-2048:]
        def 기다리기(marcatore,Regolari_funzione,초단위=50):
            chiudere_SCARTO=time.monotonic()+초단위
            while marcatore not in LOG_riga[Regolari_funzione:]:
                if time.monotonic()>chiudere_SCARTO or dati_funzione.poll() is not None:raise AssertionError(LOG_riga[Regolari_funzione:].decode('utf-8','replace'))
                handle_evento()
            return bytes(LOG_riga[Regolari_funzione:])
        def inviare(SECONDO_VALORE,marcatore=b'jkoros-native> '):
            Regolari_funzione=len(LOG_riga);dati_funzione.stdin.write(SECONDO_VALORE);dati_funzione.stdin.flush();return 기다리기(marcatore,Regolari_funzione)
        def Shell(stringa_dati):return inviare((stringa_dati+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def collegamento_VALORE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def clic_pulsante(coordinata_x,Y_coordinata):return bytes([30,1,1,coordinata_x&255,coordinata_x>>8,Y_coordinata&255,Y_coordinata>>8,30,1,0,coordinata_x&255,coordinata_x>>8,Y_coordinata&255,Y_coordinata>>8])
        def comando_MODA():
            dati_funzione.stdin.write(b'\x1b');dati_funzione.stdin.flush();chiudere_SCARTO=time.monotonic()+.2
            while time.monotonic()<chiudere_SCARTO:handle_evento(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            Shell('terminal');handle_evento(.3)
            dati=(azione_radice/'build/verification/new-java/Swing_test.class').read_bytes()
            inviare('load Swing_test.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(dati),64):inviare(dati[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            inviare(b'.\n')
            inviare('java Swing_test\n'.encode(),b'SWING READY')
            chiudere_SCARTO=time.monotonic()+3
            while time.monotonic()<chiudere_SCARTO:handle_evento(.1)
            # JFrame centered at (120,100), content at y=130.
            inviare(clic_pulsante(200,210),b'',)  # focus JTextField
            dati_funzione.stdin.write('누리'.encode());dati_funzione.stdin.flush()
            chiudere_SCARTO=time.monotonic()+.3
            while time.monotonic()<chiudere_SCARTO:handle_evento(.05)
            risultato=inviare(clic_pulsante(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_riga)-len(risultato))
            inviare(collegamento_VALORE(1),b'TERMINAL FOCUS 2')
            risultato=Shell('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in risultato
            inviare(clic_pulsante(180,12),b'TERMINAL FOCUS 1')
            chiudere_SCARTO=time.monotonic()+.3
            while time.monotonic()<chiudere_SCARTO:handle_evento(.05)
            with socket.socket(socket.AF_UNIX) as punto_di_codice:
                punto_di_codice.settimeout(10);punto_di_codice.connect(str(모의제어접속))
                with punto_di_codice.makefile('rwb') as File_voce:
                    json.loads(File_voce.readline())
                    for richiesta_VALORE in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(meta_VALORE_funzione/'native-swing.png'),'format':'png'}}):
                        File_voce.write((json.dumps(richiesta_VALORE)+'\n').encode());File_voce.flush()
                        while True:
                            반환값=json.loads(File_voce.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            inviare(clic_pulsante(505,115))
            Shell('echo SWING_CLOSED_OK')
            dati=(Corso_percorso/'한글창시험.class').read_bytes()
            inviare('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(dati),64):inviare(dati[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            inviare(b'.\n')
            inviare('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            inviare(clic_pulsante(200,255),'KOREAN SWING CLICK Nome'.encode())
            inviare(clic_pulsante(505,115))
            Shell('echo KOREAN_SWING_CLOSED_OK')
            convalida_Report.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','Italiano Finestra/pulsante/Action_informativa/evento_coda directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if dati_funzione.poll() is None:dati_funzione.terminate()
            try:dati_funzione.wait(timeout=5)
            except subprocess.TimeoutExpired:dati_funzione.kill();dati_funzione.wait()
            selettore_a916db4e.close();dati_funzione.stdin.close();dati_funzione.stdout.close();(meta_VALORE_funzione/'serial.log').write_bytes(LOG_riga);(meta_VALORE_funzione/'report.json').write_text(json.dumps(convalida_Report,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':avvia()
