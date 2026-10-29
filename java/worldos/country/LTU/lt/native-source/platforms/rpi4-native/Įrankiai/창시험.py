#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Vykdyti_komanda import Project_šaknis,Komanda

def Paleisti():
    vieta_VALUE_padėtis=Project_šaknis/'build/verification/windows';vieta_VALUE_padėtis.mkdir(parents=True,exist_ok=True)
    tikrinimas_pranešti={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_šaknis/'build/kernel8.img').read_bytes()).hexdigest()};LOG_RECORD=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        duomenys_padėtis=subprocess.Popen(Komanda()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        išrinkiklis_a916db4e=selectors.DefaultSelector();išrinkiklis_a916db4e.register(duomenys_padėtis.stdout,selectors.EVENT_READ)
        def rodyklė_įvykis(초단위=.1):
            for 누름값,_ in išrinkiklis_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_RECORD.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_RECORD and b'HALTED' not in LOG_RECORD,LOG_RECORD[-2048:]
        def 기다리기(žymeklis,dabartinis_padėtis,초단위=50):
            baigti_pokalbį_OFFSET=time.monotonic()+초단위
            while žymeklis not in LOG_RECORD[dabartinis_padėtis:]:
                if time.monotonic()>baigti_pokalbį_OFFSET or duomenys_padėtis.poll() is not None:raise AssertionError(LOG_RECORD[dabartinis_padėtis:].decode('utf-8','replace'))
                rodyklė_įvykis()
            return bytes(LOG_RECORD[dabartinis_padėtis:])
        def siųsti(SECOND_VALUE,žymeklis=b'jkoros-native> '):
            dabartinis_padėtis=len(LOG_RECORD);duomenys_padėtis.stdin.write(SECOND_VALUE);duomenys_padėtis.stdin.flush();return 기다리기(žymeklis,dabartinis_padėtis)
        def apvalkalas(eilutė_duomenys):return siųsti((eilutė_duomenys+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def nuoroda_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def spustelėti_mygtukas(x_koordinatė,세로좌표):return bytes([30,1,1,x_koordinatė&255,x_koordinatė>>8,세로좌표&255,세로좌표>>8,30,1,0,x_koordinatė&255,x_koordinatė>>8,세로좌표&255,세로좌표>>8])
        def komanda_MODE():
            duomenys_padėtis.stdin.write(b'\x1b');duomenys_padėtis.stdin.flush();baigti_pokalbį_OFFSET=time.monotonic()+.2
            while time.monotonic()<baigti_pokalbį_OFFSET:rodyklė_įvykis(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            apvalkalas('terminal');rodyklė_įvykis(.3)
            apvalkalas('mkdir first; cd first; export NAME=one')
            siųsti('vi 첫째.py\n'.encode(),b'NORMAL')
            siųsti('i값 = 21\nprint(VALUE * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            baigti_pokalbį_OFFSET=time.monotonic()+3
            while time.monotonic()<baigti_pokalbį_OFFSET:rodyklė_įvykis(.1)
            siųsti(nuoroda_VALUE(1),b'TERMINAL FOCUS 2');rodyklė_įvykis(.2)
            assert b'/\r\n' in apvalkalas('pwd')
            apvalkalas('export NAME=two')
            siųsti('vi 둘째.txt\n'.encode(),b'NORMAL')
            siųsti('i두 번째 Langas\n'.encode(),b'INSERT')
            siųsti(spustelėti_mygtukas(180,12),b'TERMINAL FOCUS 1');rodyklė_įvykis(.2)
            komanda_MODE();siųsti(b':wq\r')
            assert b'one:/first' in apvalkalas('echo "$NAME:$PWD"')
            assert 'VALUE = 21\r\nprint(VALUE * 2)'.encode() in apvalkalas('cat 첫째.py')
            REZULTATAS=apvalkalas('python 첫째.py');assert b'42\r\n' in REZULTATAS,REZULTATAS
            # Close the first shell with its actual title-bar X; second editor resumes.
            siųsti(spustelėti_mygtukas(560,63),b'TERMINAL FOCUS 2');rodyklė_įvykis(.2)
            komanda_MODE();siųsti(b':wq\r')
            assert b'two:/' in apvalkalas('echo "$NAME:$PWD"')
            assert '두 번째 Langas'.encode() in apvalkalas('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            siųsti('vi 둘째.txt\n'.encode(),b'NORMAL');siųsti(b'xu',b'NORMAL')
            siųsti(b'iX',b'INSERT');komanda_MODE();siųsti(b':q\r',b'Unsaved')
            siųsti(b':q!\r');assert '두 번째 Langas'.encode() in apvalkalas('cat 둘째.txt')
            siųsti(nuoroda_VALUE(1),b'TERMINAL FOCUS 1');rodyklė_įvykis(.2)
            siųsti(nuoroda_VALUE(1),b'TERMINAL FOCUS 3');rodyklė_įvykis(.2)
            siųsti(nuoroda_VALUE(1),b'TERMINAL FOCUS 4');rodyklė_įvykis(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            duomenys_padėtis.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));duomenys_padėtis.stdin.flush()
            apvalkalas('echo DRAGGED_OK')
            siųsti('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            siųsti('i저장하지 않은 duomenys'.encode(),b'INSERT')
            siųsti(spustelėti_mygtukas(578,97),b'TERMINAL FOCUS 3');rodyklė_įvykis(.2)
            assert '버릴문서.txt'.encode() not in apvalkalas('ls')
            siųsti(nuoroda_VALUE(1),b'TERMINAL FOCUS 4');rodyklė_įvykis(.2)
            apvalkalas('echo REUSED_WINDOW_OK')
            baigta_suma=LOG_RECORD.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',baigta_suma)
            # UART completion precedes the next QEMU display refresh.
            baigti_pokalbį_OFFSET=time.monotonic()+.3
            while time.monotonic()<baigti_pokalbį_OFFSET:rodyklė_įvykis(.05)
            with socket.socket(socket.AF_UNIX) as simbolio_kodas:
                simbolio_kodas.settimeout(10);simbolio_kodas.connect(str(모의제어접속))
                with simbolio_kodas.makefile('rwb') as Failas_įrašas:
                    json.loads(Failas_įrašas.readline())
                    for užklausa_VALUE_625fa62c in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(vieta_VALUE_padėtis/'four-terminals.png'),'format':'png'}}):
                        Failas_įrašas.write((json.dumps(užklausa_VALUE_625fa62c)+'\n').encode());Failas_įrašas.flush()
                        while True:
                            반환값=json.loads(Failas_įrašas.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(vieta_VALUE_padėtis/'four-terminals.png')).convert('RGB')
            for koordinačių_pora,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(koordinačių_pora)==색상,(koordinačių_pora,화소들.getpixel(koordinačių_pora))
            apvalkalas('echo FOUR_WINDOWS_OK')
            tikrinimas_pranešti.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if duomenys_padėtis.poll() is None:duomenys_padėtis.terminate()
            try:duomenys_padėtis.wait(timeout=5)
            except subprocess.TimeoutExpired:duomenys_padėtis.kill();duomenys_padėtis.wait()
            išrinkiklis_a916db4e.close();duomenys_padėtis.stdin.close();duomenys_padėtis.stdout.close();(vieta_VALUE_padėtis/'serial.log').write_bytes(LOG_RECORD);(vieta_VALUE_padėtis/'report.json').write_text(json.dumps(tikrinimas_pranešti,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Paleisti()
