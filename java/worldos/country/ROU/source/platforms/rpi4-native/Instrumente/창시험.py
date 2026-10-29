#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from executa_comandă import Project_rădăcină,Comandă

def Pornește():
    destinație_VALUE_poziție=Project_rădăcină/'build/verification/windows';destinație_VALUE_poziție.mkdir(parents=True,exist_ok=True)
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
            shell('mkdir first; cd first; export NAME=one')
            trimite('vi 첫째.py\n'.encode(),b'NORMAL')
            trimite('i값 = 21\nprint(VALUE * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            termina_un_apel_OFFSET=time.monotonic()+3
            while time.monotonic()<termina_un_apel_OFFSET:handle_eveniment(.1)
            trimite(comandă_rapidă_VALUE(1),b'TERMINAL FOCUS 2');handle_eveniment(.2)
            assert b'/\r\n' in shell('pwd')
            shell('export NAME=two')
            trimite('vi 둘째.txt\n'.encode(),b'NORMAL')
            trimite('i두 번째 Fereastră\n'.encode(),b'INSERT')
            trimite(clic_buton(180,12),b'TERMINAL FOCUS 1');handle_eveniment(.2)
            comandă_mod();trimite(b':wq\r')
            assert b'one:/first' in shell('echo "$NAME:$PWD"')
            assert 'VALUE = 21\r\nprint(VALUE * 2)'.encode() in shell('cat 첫째.py')
            KR=shell('python 첫째.py');assert b'42\r\n' in KR,KR
            # Close the first shell with its actual title-bar X; second editor resumes.
            trimite(clic_buton(560,63),b'TERMINAL FOCUS 2');handle_eveniment(.2)
            comandă_mod();trimite(b':wq\r')
            assert b'two:/' in shell('echo "$NAME:$PWD"')
            assert '두 번째 Fereastră'.encode() in shell('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            trimite('vi 둘째.txt\n'.encode(),b'NORMAL');trimite(b'xu',b'NORMAL')
            trimite(b'iX',b'INSERT');comandă_mod();trimite(b':q\r',b'Unsaved')
            trimite(b':q!\r');assert '두 번째 Fereastră'.encode() in shell('cat 둘째.txt')
            trimite(comandă_rapidă_VALUE(1),b'TERMINAL FOCUS 1');handle_eveniment(.2)
            trimite(comandă_rapidă_VALUE(1),b'TERMINAL FOCUS 3');handle_eveniment(.2)
            trimite(comandă_rapidă_VALUE(1),b'TERMINAL FOCUS 4');handle_eveniment(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            date_poziție.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));date_poziție.stdin.flush()
            shell('echo DRAGGED_OK')
            trimite('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            trimite('i저장하지 않은 date'.encode(),b'INSERT')
            trimite(clic_buton(578,97),b'TERMINAL FOCUS 3');handle_eveniment(.2)
            assert '버릴문서.txt'.encode() not in shell('ls')
            trimite(comandă_rapidă_VALUE(1),b'TERMINAL FOCUS 4');handle_eveniment(.2)
            shell('echo REUSED_WINDOW_OK')
            Finalizate_sumă=LOG_RECORD.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',Finalizate_sumă)
            # UART completion precedes the next QEMU display refresh.
            termina_un_apel_OFFSET=time.monotonic()+.3
            while time.monotonic()<termina_un_apel_OFFSET:handle_eveniment(.05)
            with socket.socket(socket.AF_UNIX) as cod_caracter:
                cod_caracter.settimeout(10);cod_caracter.connect(str(모의제어접속))
                with cod_caracter.makefile('rwb') as Fișier_intrare:
                    json.loads(Fișier_intrare.readline())
                    for cerere_VALUE in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(destinație_VALUE_poziție/'four-terminals.png'),'format':'png'}}):
                        Fișier_intrare.write((json.dumps(cerere_VALUE)+'\n').encode());Fișier_intrare.flush()
                        while True:
                            반환값=json.loads(Fișier_intrare.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(destinație_VALUE_poziție/'four-terminals.png')).convert('RGB')
            for pereche_de_coordonate,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(pereche_de_coordonate)==색상,(pereche_de_coordonate,화소들.getpixel(pereche_de_coordonate))
            shell('echo FOUR_WINDOWS_OK')
            validare_raport.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if date_poziție.poll() is None:date_poziție.terminate()
            try:date_poziție.wait(timeout=5)
            except subprocess.TimeoutExpired:date_poziție.kill();date_poziție.wait()
            selector_a916db4e.close();date_poziție.stdin.close();date_poziție.stdout.close();(destinație_VALUE_poziție/'serial.log').write_bytes(LOG_RECORD);(destinație_VALUE_poziție/'report.json').write_text(json.dumps(validare_raport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Pornește()
