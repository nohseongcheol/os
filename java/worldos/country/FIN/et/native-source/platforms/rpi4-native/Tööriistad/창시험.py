#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Täida_käsk import Project_juur,Käsk

def Käivita_2():
    sihtkoht_VALUE_ametikoht=Project_juur/'build/verification/windows';sihtkoht_VALUE_ametikoht.mkdir(parents=True,exist_ok=True)
    kinnitamine_aruanne={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_juur/'build/kernel8.img').read_bytes()).hexdigest()};LOG_kirje=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        andmed_ametikoht=subprocess.Popen(Käsk()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        valija_a916db4e=selectors.DefaultSelector();valija_a916db4e.register(andmed_ametikoht.stdout,selectors.EVENT_READ)
        def pide_sündmus(초단위=.1):
            for 누름값,_ in valija_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_kirje.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_kirje and b'HALTED' not in LOG_kirje,LOG_kirje[-2048:]
        def 기다리기(marker,tähtaja_piires_ametikoht,초단위=50):
            lõpeta_kõne_nihe=time.monotonic()+초단위
            while marker not in LOG_kirje[tähtaja_piires_ametikoht:]:
                if time.monotonic()>lõpeta_kõne_nihe or andmed_ametikoht.poll() is not None:raise AssertionError(LOG_kirje[tähtaja_piires_ametikoht:].decode('utf-8','replace'))
                pide_sündmus()
            return bytes(LOG_kirje[tähtaja_piires_ametikoht:])
        def saatma(SECOND_VALUE,marker=b'jkoros-native> '):
            tähtaja_piires_ametikoht=len(LOG_kirje);andmed_ametikoht.stdin.write(SECOND_VALUE);andmed_ametikoht.stdin.flush();return 기다리기(marker,tähtaja_piires_ametikoht)
        def kest(string_andmed):return saatma((string_andmed+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def otsetee_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def klõps_nupp(가로좌표,세로좌표):return bytes([30,1,1,가로좌표&255,가로좌표>>8,세로좌표&255,세로좌표>>8,30,1,0,가로좌표&255,가로좌표>>8,세로좌표&255,세로좌표>>8])
        def käsk_MODE():
            andmed_ametikoht.stdin.write(b'\x1b');andmed_ametikoht.stdin.flush();lõpeta_kõne_nihe=time.monotonic()+.2
            while time.monotonic()<lõpeta_kõne_nihe:pide_sündmus(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            kest('terminal');pide_sündmus(.3)
            kest('mkdir first; cd first; export NAME=one')
            saatma('vi 첫째.py\n'.encode(),b'NORMAL')
            saatma('i값 = 21\nprint(VALUE * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            lõpeta_kõne_nihe=time.monotonic()+3
            while time.monotonic()<lõpeta_kõne_nihe:pide_sündmus(.1)
            saatma(otsetee_VALUE(1),b'TERMINAL FOCUS 2');pide_sündmus(.2)
            assert b'/\r\n' in kest('pwd')
            kest('export NAME=two')
            saatma('vi 둘째.txt\n'.encode(),b'NORMAL')
            saatma('i두 번째 aken\n'.encode(),b'INSERT')
            saatma(klõps_nupp(180,12),b'TERMINAL FOCUS 1');pide_sündmus(.2)
            käsk_MODE();saatma(b':wq\r')
            assert b'one:/first' in kest('echo "$NAME:$PWD"')
            assert 'VALUE = 21\r\nprint(VALUE * 2)'.encode() in kest('cat 첫째.py')
            TULEMUS=kest('python 첫째.py');assert b'42\r\n' in TULEMUS,TULEMUS
            # Close the first shell with its actual title-bar X; second editor resumes.
            saatma(klõps_nupp(560,63),b'TERMINAL FOCUS 2');pide_sündmus(.2)
            käsk_MODE();saatma(b':wq\r')
            assert b'two:/' in kest('echo "$NAME:$PWD"')
            assert '두 번째 aken'.encode() in kest('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            saatma('vi 둘째.txt\n'.encode(),b'NORMAL');saatma(b'xu',b'NORMAL')
            saatma(b'iX',b'INSERT');käsk_MODE();saatma(b':q\r',b'Unsaved')
            saatma(b':q!\r');assert '두 번째 aken'.encode() in kest('cat 둘째.txt')
            saatma(otsetee_VALUE(1),b'TERMINAL FOCUS 1');pide_sündmus(.2)
            saatma(otsetee_VALUE(1),b'TERMINAL FOCUS 3');pide_sündmus(.2)
            saatma(otsetee_VALUE(1),b'TERMINAL FOCUS 4');pide_sündmus(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            andmed_ametikoht.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));andmed_ametikoht.stdin.flush()
            kest('echo DRAGGED_OK')
            saatma('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            saatma('i저장하지 않은 andmed'.encode(),b'INSERT')
            saatma(klõps_nupp(578,97),b'TERMINAL FOCUS 3');pide_sündmus(.2)
            assert '버릴문서.txt'.encode() not in kest('ls')
            saatma(otsetee_VALUE(1),b'TERMINAL FOCUS 4');pide_sündmus(.2)
            kest('echo REUSED_WINDOW_OK')
            Lõpetatud_kogus=LOG_kirje.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',Lõpetatud_kogus)
            # UART completion precedes the next QEMU display refresh.
            lõpeta_kõne_nihe=time.monotonic()+.3
            while time.monotonic()<lõpeta_kõne_nihe:pide_sündmus(.05)
            with socket.socket(socket.AF_UNIX) as koodipunkt:
                koodipunkt.settimeout(10);koodipunkt.connect(str(모의제어접속))
                with koodipunkt.makefile('rwb') as Fail_kirje:
                    json.loads(Fail_kirje.readline())
                    for päring_VALUE_625fa62c in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(sihtkoht_VALUE_ametikoht/'four-terminals.png'),'format':'png'}}):
                        Fail_kirje.write((json.dumps(päring_VALUE_625fa62c)+'\n').encode());Fail_kirje.flush()
                        while True:
                            반환값=json.loads(Fail_kirje.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(sihtkoht_VALUE_ametikoht/'four-terminals.png')).convert('RGB')
            for 좌표쌍,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(좌표쌍)==색상,(좌표쌍,화소들.getpixel(좌표쌍))
            kest('echo FOUR_WINDOWS_OK')
            kinnitamine_aruanne.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if andmed_ametikoht.poll() is None:andmed_ametikoht.terminate()
            try:andmed_ametikoht.wait(timeout=5)
            except subprocess.TimeoutExpired:andmed_ametikoht.kill();andmed_ametikoht.wait()
            valija_a916db4e.close();andmed_ametikoht.stdin.close();andmed_ametikoht.stdout.close();(sihtkoht_VALUE_ametikoht/'serial.log').write_bytes(LOG_kirje);(sihtkoht_VALUE_ametikoht/'report.json').write_text(json.dumps(kinnitamine_aruanne,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Käivita_2()
