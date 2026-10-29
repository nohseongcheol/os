#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Izpildīt_komanda import Project_sakne,Komanda

def Palaist():
    mērķis_VALUE_amats=Project_sakne/'build/verification/windows';mērķis_VALUE_amats.mkdir(parents=True,exist_ok=True)
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
            čaula('mkdir first; cd first; export NAME=one')
            sūtīt('vi 첫째.py\n'.encode(),b'NORMAL')
            sūtīt('i값 = 21\nprint(VALUE * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            beigt_zvanu_Nobīde=time.monotonic()+3
            while time.monotonic()<beigt_zvanu_Nobīde:turis_notikums(.1)
            sūtīt(saīsne_VALUE(1),b'TERMINAL FOCUS 2');turis_notikums(.2)
            assert b'/\r\n' in čaula('pwd')
            čaula('export NAME=two')
            sūtīt('vi 둘째.txt\n'.encode(),b'NORMAL')
            sūtīt('i두 번째 Logs\n'.encode(),b'INSERT')
            sūtīt(klikšķis_poga(180,12),b'TERMINAL FOCUS 1');turis_notikums(.2)
            komanda_MODE();sūtīt(b':wq\r')
            assert b'one:/first' in čaula('echo "$NAME:$PWD"')
            assert 'VALUE = 21\r\nprint(VALUE * 2)'.encode() in čaula('cat 첫째.py')
            mērs=čaula('python 첫째.py');assert b'42\r\n' in mērs,mērs
            # Close the first shell with its actual title-bar X; second editor resumes.
            sūtīt(klikšķis_poga(560,63),b'TERMINAL FOCUS 2');turis_notikums(.2)
            komanda_MODE();sūtīt(b':wq\r')
            assert b'two:/' in čaula('echo "$NAME:$PWD"')
            assert '두 번째 Logs'.encode() in čaula('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            sūtīt('vi 둘째.txt\n'.encode(),b'NORMAL');sūtīt(b'xu',b'NORMAL')
            sūtīt(b'iX',b'INSERT');komanda_MODE();sūtīt(b':q\r',b'Unsaved')
            sūtīt(b':q!\r');assert '두 번째 Logs'.encode() in čaula('cat 둘째.txt')
            sūtīt(saīsne_VALUE(1),b'TERMINAL FOCUS 1');turis_notikums(.2)
            sūtīt(saīsne_VALUE(1),b'TERMINAL FOCUS 3');turis_notikums(.2)
            sūtīt(saīsne_VALUE(1),b'TERMINAL FOCUS 4');turis_notikums(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            dati_amats.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));dati_amats.stdin.flush()
            čaula('echo DRAGGED_OK')
            sūtīt('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            sūtīt('i저장하지 않은 dati'.encode(),b'INSERT')
            sūtīt(klikšķis_poga(578,97),b'TERMINAL FOCUS 3');turis_notikums(.2)
            assert '버릴문서.txt'.encode() not in čaula('ls')
            sūtīt(saīsne_VALUE(1),b'TERMINAL FOCUS 4');turis_notikums(.2)
            čaula('echo REUSED_WINDOW_OK')
            Pabeigti_summa=LOG_RECORD.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',Pabeigti_summa)
            # UART completion precedes the next QEMU display refresh.
            beigt_zvanu_Nobīde=time.monotonic()+.3
            while time.monotonic()<beigt_zvanu_Nobīde:turis_notikums(.05)
            with socket.socket(socket.AF_UNIX) as koda_punkts:
                koda_punkts.settimeout(10);koda_punkts.connect(str(모의제어접속))
                with koda_punkts.makefile('rwb') as Fails_ievade:
                    json.loads(Fails_ievade.readline())
                    for pieprasījums_VALUE in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(mērķis_VALUE_amats/'four-terminals.png'),'format':'png'}}):
                        Fails_ievade.write((json.dumps(pieprasījums_VALUE)+'\n').encode());Fails_ievade.flush()
                        while True:
                            반환값=json.loads(Fails_ievade.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(mērķis_VALUE_amats/'four-terminals.png')).convert('RGB')
            for koordinātu_pāris,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(koordinātu_pāris)==색상,(koordinātu_pāris,화소들.getpixel(koordinātu_pāris))
            čaula('echo FOUR_WINDOWS_OK')
            validācija_ziņot.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if dati_amats.poll() is None:dati_amats.terminate()
            try:dati_amats.wait(timeout=5)
            except subprocess.TimeoutExpired:dati_amats.kill();dati_amats.wait()
            atlasītājs_a916db4e.close();dati_amats.stdin.close();dati_amats.stdout.close();(mērķis_VALUE_amats/'serial.log').write_bytes(LOG_RECORD);(mērķis_VALUE_amats/'report.json').write_text(json.dumps(validācija_ziņot,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Palaist()
