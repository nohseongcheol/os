#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Esegui_comando import azione_radice,comando

def avvia():
    meta_VALORE_funzione=azione_radice/'build/verification/windows';meta_VALORE_funzione.mkdir(parents=True,exist_ok=True)
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
            Shell('mkdir first; cd first; export NAME=one')
            inviare('vi 첫째.py\n'.encode(),b'NORMAL')
            inviare('i값 = 21\nprint(VALORE * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            chiudere_SCARTO=time.monotonic()+3
            while time.monotonic()<chiudere_SCARTO:handle_evento(.1)
            inviare(collegamento_VALORE(1),b'TERMINAL FOCUS 2');handle_evento(.2)
            assert b'/\r\n' in Shell('pwd')
            Shell('export NAME=two')
            inviare('vi 둘째.txt\n'.encode(),b'NORMAL')
            inviare('i두 번째 Finestra\n'.encode(),b'INSERT')
            inviare(clic_pulsante(180,12),b'TERMINAL FOCUS 1');handle_evento(.2)
            comando_MODA();inviare(b':wq\r')
            assert b'one:/first' in Shell('echo "$NAME:$PWD"')
            assert 'VALORE = 21\r\nprint(VALORE * 2)'.encode() in Shell('cat 첫째.py')
            risultato=Shell('python 첫째.py');assert b'42\r\n' in risultato,risultato
            # Close the first shell with its actual title-bar X; second editor resumes.
            inviare(clic_pulsante(560,63),b'TERMINAL FOCUS 2');handle_evento(.2)
            comando_MODA();inviare(b':wq\r')
            assert b'two:/' in Shell('echo "$NAME:$PWD"')
            assert '두 번째 Finestra'.encode() in Shell('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            inviare('vi 둘째.txt\n'.encode(),b'NORMAL');inviare(b'xu',b'NORMAL')
            inviare(b'iX',b'INSERT');comando_MODA();inviare(b':q\r',b'Unsaved')
            inviare(b':q!\r');assert '두 번째 Finestra'.encode() in Shell('cat 둘째.txt')
            inviare(collegamento_VALORE(1),b'TERMINAL FOCUS 1');handle_evento(.2)
            inviare(collegamento_VALORE(1),b'TERMINAL FOCUS 3');handle_evento(.2)
            inviare(collegamento_VALORE(1),b'TERMINAL FOCUS 4');handle_evento(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            dati_funzione.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));dati_funzione.stdin.flush()
            Shell('echo DRAGGED_OK')
            inviare('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            inviare('i저장하지 않은 dati'.encode(),b'INSERT')
            inviare(clic_pulsante(578,97),b'TERMINAL FOCUS 3');handle_evento(.2)
            assert '버릴문서.txt'.encode() not in Shell('ls')
            inviare(collegamento_VALORE(1),b'TERMINAL FOCUS 4');handle_evento(.2)
            Shell('echo REUSED_WINDOW_OK')
            Completate_importo=LOG_riga.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',Completate_importo)
            # UART completion precedes the next QEMU display refresh.
            chiudere_SCARTO=time.monotonic()+.3
            while time.monotonic()<chiudere_SCARTO:handle_evento(.05)
            with socket.socket(socket.AF_UNIX) as punto_di_codice:
                punto_di_codice.settimeout(10);punto_di_codice.connect(str(모의제어접속))
                with punto_di_codice.makefile('rwb') as File_voce:
                    json.loads(File_voce.readline())
                    for richiesta_VALORE in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(meta_VALORE_funzione/'four-terminals.png'),'format':'png'}}):
                        File_voce.write((json.dumps(richiesta_VALORE)+'\n').encode());File_voce.flush()
                        while True:
                            반환값=json.loads(File_voce.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(meta_VALORE_funzione/'four-terminals.png')).convert('RGB')
            for coordinate,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(coordinate)==색상,(coordinate,화소들.getpixel(coordinate))
            Shell('echo FOUR_WINDOWS_OK')
            convalida_Report.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if dati_funzione.poll() is None:dati_funzione.terminate()
            try:dati_funzione.wait(timeout=5)
            except subprocess.TimeoutExpired:dati_funzione.kill();dati_funzione.wait()
            selettore_a916db4e.close();dati_funzione.stdin.close();dati_funzione.stdout.close();(meta_VALORE_funzione/'serial.log').write_bytes(LOG_riga);(meta_VALORE_funzione/'report.json').write_text(json.dumps(convalida_Report,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':avvia()
