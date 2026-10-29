#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Vykonať_príkaz import akcia_koreň,Príkaz

def Spustiť_2():
    cieľ_VALUE_pozícia=akcia_koreň/'build/verification/windows';cieľ_VALUE_pozícia.mkdir(parents=True,exist_ok=True)
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
            셸('mkdir first; cd first; export NAME=one')
            odoslať('vi 첫째.py\n'.encode(),b'NORMAL')
            odoslať('i값 = 21\nprint(VALUE * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            ukončiť_hovor_Posun=time.monotonic()+3
            while time.monotonic()<ukončiť_hovor_Posun:rukoväť_udalosť(.1)
            odoslať(odkaz_VALUE_910d9d5a(1),b'TERMINAL FOCUS 2');rukoväť_udalosť(.2)
            assert b'/\r\n' in 셸('pwd')
            셸('export NAME=two')
            odoslať('vi 둘째.txt\n'.encode(),b'NORMAL')
            odoslať('i두 번째 Okno\n'.encode(),b'INSERT')
            odoslať(kliknúť_tlačidlo(180,12),b'TERMINAL FOCUS 1');rukoväť_udalosť(.2)
            príkaz_MODE();odoslať(b':wq\r')
            assert b'one:/first' in 셸('echo "$NAME:$PWD"')
            assert 'VALUE = 21\r\nprint(VALUE * 2)'.encode() in 셸('cat 첫째.py')
            KR=셸('python 첫째.py');assert b'42\r\n' in KR,KR
            # Close the first shell with its actual title-bar X; second editor resumes.
            odoslať(kliknúť_tlačidlo(560,63),b'TERMINAL FOCUS 2');rukoväť_udalosť(.2)
            príkaz_MODE();odoslať(b':wq\r')
            assert b'two:/' in 셸('echo "$NAME:$PWD"')
            assert '두 번째 Okno'.encode() in 셸('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            odoslať('vi 둘째.txt\n'.encode(),b'NORMAL');odoslať(b'xu',b'NORMAL')
            odoslať(b'iX',b'INSERT');príkaz_MODE();odoslať(b':q\r',b'Unsaved')
            odoslať(b':q!\r');assert '두 번째 Okno'.encode() in 셸('cat 둘째.txt')
            odoslať(odkaz_VALUE_910d9d5a(1),b'TERMINAL FOCUS 1');rukoväť_udalosť(.2)
            odoslať(odkaz_VALUE_910d9d5a(1),b'TERMINAL FOCUS 3');rukoväť_udalosť(.2)
            odoslať(odkaz_VALUE_910d9d5a(1),b'TERMINAL FOCUS 4');rukoväť_udalosť(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            údaje_pozícia.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));údaje_pozícia.stdin.flush()
            셸('echo DRAGGED_OK')
            odoslať('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            odoslať('i저장하지 않은 údaje'.encode(),b'INSERT')
            odoslať(kliknúť_tlačidlo(578,97),b'TERMINAL FOCUS 3');rukoväť_udalosť(.2)
            assert '버릴문서.txt'.encode() not in 셸('ls')
            odoslať(odkaz_VALUE_910d9d5a(1),b'TERMINAL FOCUS 4');rukoväť_udalosť(.2)
            셸('echo REUSED_WINDOW_OK')
            Dokončené_úlohy_suma=LOG_RECORD.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',Dokončené_úlohy_suma)
            # UART completion precedes the next QEMU display refresh.
            ukončiť_hovor_Posun=time.monotonic()+.3
            while time.monotonic()<ukončiť_hovor_Posun:rukoväť_udalosť(.05)
            with socket.socket(socket.AF_UNIX) as bod_kódu:
                bod_kódu.settimeout(10);bod_kódu.connect(str(모의제어접속))
                with bod_kódu.makefile('rwb') as Súbor_položka:
                    json.loads(Súbor_položka.readline())
                    for požiadavka_VALUE_625fa62c in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(cieľ_VALUE_pozícia/'four-terminals.png'),'format':'png'}}):
                        Súbor_položka.write((json.dumps(požiadavka_VALUE_625fa62c)+'\n').encode());Súbor_položka.flush()
                        while True:
                            반환값=json.loads(Súbor_položka.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(cieľ_VALUE_pozícia/'four-terminals.png')).convert('RGB')
            for súradnice,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(súradnice)==색상,(súradnice,화소들.getpixel(súradnice))
            셸('echo FOUR_WINDOWS_OK')
            overenie_správa.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if údaje_pozícia.poll() is None:údaje_pozícia.terminate()
            try:údaje_pozícia.wait(timeout=5)
            except subprocess.TimeoutExpired:údaje_pozícia.kill();údaje_pozícia.wait()
            selektor_a916db4e.close();údaje_pozícia.stdin.close();údaje_pozícia.stdout.close();(cieľ_VALUE_pozícia/'serial.log').write_bytes(LOG_RECORD);(cieľ_VALUE_pozícia/'report.json').write_text(json.dumps(overenie_správa,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Spustiť_2()
