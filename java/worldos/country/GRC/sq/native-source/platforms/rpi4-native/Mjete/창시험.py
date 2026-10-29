#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from zbatoj_komandë import Project_rrënjë,Komanda

def Ekzekuto():
    vendmbërritje_VALUE_pozicioni=Project_rrënjë/'build/verification/windows';vendmbërritje_VALUE_pozicioni.mkdir(parents=True,exist_ok=True)
    miratim_raport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_rrënjë/'build/kernel8.img').read_bytes()).hexdigest()};LOG_RECORD=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        të_dhëna_pozicioni=subprocess.Popen(Komanda()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        përzgjedhësi_a916db4e=selectors.DefaultSelector();përzgjedhësi_a916db4e.register(të_dhëna_pozicioni.stdout,selectors.EVENT_READ)
        def dorezë_ngjarje(초단위=.1):
            for 누름값,_ in përzgjedhësi_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_RECORD.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_RECORD and b'HALTED' not in LOG_RECORD,LOG_RECORD[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            mbaroj_OFFSET=time.monotonic()+초단위
            while 확인표시 not in LOG_RECORD[현재위치:]:
                if time.monotonic()>mbaroj_OFFSET or të_dhëna_pozicioni.poll() is not None:raise AssertionError(LOG_RECORD[현재위치:].decode('utf-8','replace'))
                dorezë_ngjarje()
            return bytes(LOG_RECORD[현재위치:])
        def dërgoj(SECOND_VALUE,확인표시=b'jkoros-native> '):
            현재위치=len(LOG_RECORD);të_dhëna_pozicioni.stdin.write(SECOND_VALUE);të_dhëna_pozicioni.stdin.flush();return 기다리기(확인표시,현재위치)
        def pasues(varg_të_dhëna):return dërgoj((varg_të_dhëna+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def shkurtore_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def klik_buton(koordinata_x,Y_koordinatë):return bytes([30,1,1,koordinata_x&255,koordinata_x>>8,Y_koordinatë&255,Y_koordinatë>>8,30,1,0,koordinata_x&255,koordinata_x>>8,Y_koordinatë&255,Y_koordinatë>>8])
        def komandë_MODE():
            të_dhëna_pozicioni.stdin.write(b'\x1b');të_dhëna_pozicioni.stdin.flush();mbaroj_OFFSET=time.monotonic()+.2
            while time.monotonic()<mbaroj_OFFSET:dorezë_ngjarje(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            pasues('terminal');dorezë_ngjarje(.3)
            pasues('mkdir first; cd first; export NAME=one')
            dërgoj('vi 첫째.py\n'.encode(),b'NORMAL')
            dërgoj('i값 = 21\nprint(VALUE * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            mbaroj_OFFSET=time.monotonic()+3
            while time.monotonic()<mbaroj_OFFSET:dorezë_ngjarje(.1)
            dërgoj(shkurtore_VALUE(1),b'TERMINAL FOCUS 2');dorezë_ngjarje(.2)
            assert b'/\r\n' in pasues('pwd')
            pasues('export NAME=two')
            dërgoj('vi 둘째.txt\n'.encode(),b'NORMAL')
            dërgoj('i두 번째 Dritare\n'.encode(),b'INSERT')
            dërgoj(klik_buton(180,12),b'TERMINAL FOCUS 1');dorezë_ngjarje(.2)
            komandë_MODE();dërgoj(b':wq\r')
            assert b'one:/first' in pasues('echo "$NAME:$PWD"')
            assert 'VALUE = 21\r\nprint(VALUE * 2)'.encode() in pasues('cat 첫째.py')
            llogaritje=pasues('python 첫째.py');assert b'42\r\n' in llogaritje,llogaritje
            # Close the first shell with its actual title-bar X; second editor resumes.
            dërgoj(klik_buton(560,63),b'TERMINAL FOCUS 2');dorezë_ngjarje(.2)
            komandë_MODE();dërgoj(b':wq\r')
            assert b'two:/' in pasues('echo "$NAME:$PWD"')
            assert '두 번째 Dritare'.encode() in pasues('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            dërgoj('vi 둘째.txt\n'.encode(),b'NORMAL');dërgoj(b'xu',b'NORMAL')
            dërgoj(b'iX',b'INSERT');komandë_MODE();dërgoj(b':q\r',b'Unsaved')
            dërgoj(b':q!\r');assert '두 번째 Dritare'.encode() in pasues('cat 둘째.txt')
            dërgoj(shkurtore_VALUE(1),b'TERMINAL FOCUS 1');dorezë_ngjarje(.2)
            dërgoj(shkurtore_VALUE(1),b'TERMINAL FOCUS 3');dorezë_ngjarje(.2)
            dërgoj(shkurtore_VALUE(1),b'TERMINAL FOCUS 4');dorezë_ngjarje(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            të_dhëna_pozicioni.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));të_dhëna_pozicioni.stdin.flush()
            pasues('echo DRAGGED_OK')
            dërgoj('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            dërgoj('i저장하지 않은 të_dhëna'.encode(),b'INSERT')
            dërgoj(klik_buton(578,97),b'TERMINAL FOCUS 3');dorezë_ngjarje(.2)
            assert '버릴문서.txt'.encode() not in pasues('ls')
            dërgoj(shkurtore_VALUE(1),b'TERMINAL FOCUS 4');dorezë_ngjarje(.2)
            pasues('echo REUSED_WINDOW_OK')
            완료량=LOG_RECORD.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            mbaroj_OFFSET=time.monotonic()+.3
            while time.monotonic()<mbaroj_OFFSET:dorezë_ngjarje(.05)
            with socket.socket(socket.AF_UNIX) as kodi_i_karakterit:
                kodi_i_karakterit.settimeout(10);kodi_i_karakterit.connect(str(모의제어접속))
                with kodi_i_karakterit.makefile('rwb') as skedar_futje:
                    json.loads(skedar_futje.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(vendmbërritje_VALUE_pozicioni/'four-terminals.png'),'format':'png'}}):
                        skedar_futje.write((json.dumps(요청값)+'\n').encode());skedar_futje.flush()
                        while True:
                            반환값=json.loads(skedar_futje.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(vendmbërritje_VALUE_pozicioni/'four-terminals.png')).convert('RGB')
            for çifti_i_koordinatave,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(çifti_i_koordinatave)==색상,(çifti_i_koordinatave,화소들.getpixel(çifti_i_koordinatave))
            pasues('echo FOUR_WINDOWS_OK')
            miratim_raport.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if të_dhëna_pozicioni.poll() is None:të_dhëna_pozicioni.terminate()
            try:të_dhëna_pozicioni.wait(timeout=5)
            except subprocess.TimeoutExpired:të_dhëna_pozicioni.kill();të_dhëna_pozicioni.wait()
            përzgjedhësi_a916db4e.close();të_dhëna_pozicioni.stdin.close();të_dhëna_pozicioni.stdout.close();(vendmbërritje_VALUE_pozicioni/'serial.log').write_bytes(LOG_RECORD);(vendmbërritje_VALUE_pozicioni/'report.json').write_text(json.dumps(miratim_raport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Ekzekuto()
