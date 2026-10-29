#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from kawe_tono import whakaatu_pūtake,tono

def whakahaere():
    ūnga_uara_tūranga=whakaatu_pūtake/'build/verification/windows';ūnga_uara_tūranga.mkdir(parents=True,exist_ok=True)
    whakamana_pūrongo={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((whakaatu_pūtake/'build/kernel8.img').read_bytes()).hexdigest()};LOG_RECORD=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        raraunga_tūranga=subprocess.Popen(tono()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        pūtīpako_a916db4e=selectors.DefaultSelector();pūtīpako_a916db4e.register(raraunga_tūranga.stdout,selectors.EVENT_READ)
        def raweke_hui(초단위=.1):
            for 누름값,_ in pūtīpako_a916db4e.select(초단위):
                SECOND_uara=누름값.fileobj.read(65536)
                if SECOND_uara:LOG_RECORD.extend(SECOND_uara)
            assert b'PANIC:' not in LOG_RECORD and b'HALTED' not in LOG_RECORD,LOG_RECORD[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            mutu_OFFSET=time.monotonic()+초단위
            while 확인표시 not in LOG_RECORD[현재위치:]:
                if time.monotonic()>mutu_OFFSET or raraunga_tūranga.poll() is not None:raise AssertionError(LOG_RECORD[현재위치:].decode('utf-8','replace'))
                raweke_hui()
            return bytes(LOG_RECORD[현재위치:])
        def tuku(SECOND_uara,확인표시=b'jkoros-native> '):
            현재위치=len(LOG_RECORD);raraunga_tūranga.stdin.write(SECOND_uara);raraunga_tūranga.stdin.flush();return 기다리기(확인표시,현재위치)
        def anga(aho_raraunga):return tuku((aho_raraunga+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def pokatata_uara(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def pāwhiri_pātene(taunga_x,세로좌표):return bytes([30,1,1,taunga_x&255,taunga_x>>8,세로좌표&255,세로좌표>>8,30,1,0,taunga_x&255,taunga_x>>8,세로좌표&255,세로좌표>>8])
        def tono_MODE():
            raraunga_tūranga.stdin.write(b'\x1b');raraunga_tūranga.stdin.flush();mutu_OFFSET=time.monotonic()+.2
            while time.monotonic()<mutu_OFFSET:raweke_hui(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            anga('terminal');raweke_hui(.3)
            anga('mkdir first; cd first; export NAME=one')
            tuku('vi 첫째.py\n'.encode(),b'NORMAL')
            tuku('i값 = 21\nprint(uara * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            mutu_OFFSET=time.monotonic()+3
            while time.monotonic()<mutu_OFFSET:raweke_hui(.1)
            tuku(pokatata_uara(1),b'TERMINAL FOCUS 2');raweke_hui(.2)
            assert b'/\r\n' in anga('pwd')
            anga('export NAME=two')
            tuku('vi 둘째.txt\n'.encode(),b'NORMAL')
            tuku('i두 번째 matapihi\n'.encode(),b'INSERT')
            tuku(pāwhiri_pātene(180,12),b'TERMINAL FOCUS 1');raweke_hui(.2)
            tono_MODE();tuku(b':wq\r')
            assert b'one:/first' in anga('echo "$NAME:$PWD"')
            assert 'uara = 21\r\nprint(uara * 2)'.encode() in anga('cat 첫째.py')
            mēhua=anga('python 첫째.py');assert b'42\r\n' in mēhua,mēhua
            # Close the first shell with its actual title-bar X; second editor resumes.
            tuku(pāwhiri_pātene(560,63),b'TERMINAL FOCUS 2');raweke_hui(.2)
            tono_MODE();tuku(b':wq\r')
            assert b'two:/' in anga('echo "$NAME:$PWD"')
            assert '두 번째 matapihi'.encode() in anga('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            tuku('vi 둘째.txt\n'.encode(),b'NORMAL');tuku(b'xu',b'NORMAL')
            tuku(b'iX',b'INSERT');tono_MODE();tuku(b':q\r',b'Unsaved')
            tuku(b':q!\r');assert '두 번째 matapihi'.encode() in anga('cat 둘째.txt')
            tuku(pokatata_uara(1),b'TERMINAL FOCUS 1');raweke_hui(.2)
            tuku(pokatata_uara(1),b'TERMINAL FOCUS 3');raweke_hui(.2)
            tuku(pokatata_uara(1),b'TERMINAL FOCUS 4');raweke_hui(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            raraunga_tūranga.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));raraunga_tūranga.stdin.flush()
            anga('echo DRAGGED_OK')
            tuku('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            tuku('i저장하지 않은 raraunga'.encode(),b'INSERT')
            tuku(pāwhiri_pātene(578,97),b'TERMINAL FOCUS 3');raweke_hui(.2)
            assert '버릴문서.txt'.encode() not in anga('ls')
            tuku(pokatata_uara(1),b'TERMINAL FOCUS 4');raweke_hui(.2)
            anga('echo REUSED_WINDOW_OK')
            완료량=LOG_RECORD.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            mutu_OFFSET=time.monotonic()+.3
            while time.monotonic()<mutu_OFFSET:raweke_hui(.05)
            with socket.socket(socket.AF_UNIX) as waehere_pūāhua:
                waehere_pūāhua.settimeout(10);waehere_pūāhua.connect(str(모의제어접속))
                with waehere_pūāhua.makefile('rwb') as kōnae_tāurunga:
                    json.loads(kōnae_tāurunga.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(ūnga_uara_tūranga/'four-terminals.png'),'format':'png'}}):
                        kōnae_tāurunga.write((json.dumps(요청값)+'\n').encode());kōnae_tāurunga.flush()
                        while True:
                            반환값=json.loads(kōnae_tāurunga.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(ūnga_uara_tūranga/'four-terminals.png')).convert('RGB')
            for takirua_taururuku,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(takirua_taururuku)==색상,(takirua_taururuku,화소들.getpixel(takirua_taururuku))
            anga('echo FOUR_WINDOWS_OK')
            whakamana_pūrongo.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if raraunga_tūranga.poll() is None:raraunga_tūranga.terminate()
            try:raraunga_tūranga.wait(timeout=5)
            except subprocess.TimeoutExpired:raraunga_tūranga.kill();raraunga_tūranga.wait()
            pūtīpako_a916db4e.close();raraunga_tūranga.stdin.close();raraunga_tūranga.stdout.close();(ūnga_uara_tūranga/'serial.log').write_bytes(LOG_RECORD);(ūnga_uara_tūranga/'report.json').write_text(json.dumps(whakamana_pūrongo,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':whakahaere()
