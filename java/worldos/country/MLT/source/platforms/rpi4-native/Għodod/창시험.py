#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from eżegwixxa_kmand import pprojetta_għerq,kmand

def serje():
    destinazzjoni_VALUE_pożizzjoni=pprojetta_għerq/'build/verification/windows';destinazzjoni_VALUE_pożizzjoni.mkdir(parents=True,exist_ok=True)
    validazzjoni_rapport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((pprojetta_għerq/'build/kernel8.img').read_bytes()).hexdigest()};LOG_RECORD=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        data_pożizzjoni=subprocess.Popen(kmand()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        selettur_a916db4e=selectors.DefaultSelector();selettur_a916db4e.register(data_pożizzjoni.stdout,selectors.EVENT_READ)
        def handle_avveniment(초단위=.1):
            for 누름값,_ in selettur_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_RECORD.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_RECORD and b'HALTED' not in LOG_RECORD,LOG_RECORD[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            ttermina_OFFSET=time.monotonic()+초단위
            while 확인표시 not in LOG_RECORD[현재위치:]:
                if time.monotonic()>ttermina_OFFSET or data_pożizzjoni.poll() is not None:raise AssertionError(LOG_RECORD[현재위치:].decode('utf-8','replace'))
                handle_avveniment()
            return bytes(LOG_RECORD[현재위치:])
        def bagħat(SECOND_VALUE,확인표시=b'jkoros-native> '):
            현재위치=len(LOG_RECORD);data_pożizzjoni.stdin.write(SECOND_VALUE);data_pożizzjoni.stdin.flush();return 기다리기(확인표시,현재위치)
        def shell(string_data):return bagħat((string_data+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def shortcut_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def klikkja_buttuna(koordinat_x,세로좌표):return bytes([30,1,1,koordinat_x&255,koordinat_x>>8,세로좌표&255,세로좌표>>8,30,1,0,koordinat_x&255,koordinat_x>>8,세로좌표&255,세로좌표>>8])
        def kmand_MODE():
            data_pożizzjoni.stdin.write(b'\x1b');data_pożizzjoni.stdin.flush();ttermina_OFFSET=time.monotonic()+.2
            while time.monotonic()<ttermina_OFFSET:handle_avveniment(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            shell('terminal');handle_avveniment(.3)
            shell('mkdir first; cd first; export NAME=one')
            bagħat('vi 첫째.py\n'.encode(),b'NORMAL')
            bagħat('i값 = 21\nprint(VALUE * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            ttermina_OFFSET=time.monotonic()+3
            while time.monotonic()<ttermina_OFFSET:handle_avveniment(.1)
            bagħat(shortcut_VALUE(1),b'TERMINAL FOCUS 2');handle_avveniment(.2)
            assert b'/\r\n' in shell('pwd')
            shell('export NAME=two')
            bagħat('vi 둘째.txt\n'.encode(),b'NORMAL')
            bagħat('i두 번째 tieqa\n'.encode(),b'INSERT')
            bagħat(klikkja_buttuna(180,12),b'TERMINAL FOCUS 1');handle_avveniment(.2)
            kmand_MODE();bagħat(b':wq\r')
            assert b'one:/first' in shell('echo "$NAME:$PWD"')
            assert 'VALUE = 21\r\nprint(VALUE * 2)'.encode() in shell('cat 첫째.py')
            miżura=shell('python 첫째.py');assert b'42\r\n' in miżura,miżura
            # Close the first shell with its actual title-bar X; second editor resumes.
            bagħat(klikkja_buttuna(560,63),b'TERMINAL FOCUS 2');handle_avveniment(.2)
            kmand_MODE();bagħat(b':wq\r')
            assert b'two:/' in shell('echo "$NAME:$PWD"')
            assert '두 번째 tieqa'.encode() in shell('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            bagħat('vi 둘째.txt\n'.encode(),b'NORMAL');bagħat(b'xu',b'NORMAL')
            bagħat(b'iX',b'INSERT');kmand_MODE();bagħat(b':q\r',b'Unsaved')
            bagħat(b':q!\r');assert '두 번째 tieqa'.encode() in shell('cat 둘째.txt')
            bagħat(shortcut_VALUE(1),b'TERMINAL FOCUS 1');handle_avveniment(.2)
            bagħat(shortcut_VALUE(1),b'TERMINAL FOCUS 3');handle_avveniment(.2)
            bagħat(shortcut_VALUE(1),b'TERMINAL FOCUS 4');handle_avveniment(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            data_pożizzjoni.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));data_pożizzjoni.stdin.flush()
            shell('echo DRAGGED_OK')
            bagħat('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            bagħat('i저장하지 않은 data'.encode(),b'INSERT')
            bagħat(klikkja_buttuna(578,97),b'TERMINAL FOCUS 3');handle_avveniment(.2)
            assert '버릴문서.txt'.encode() not in shell('ls')
            bagħat(shortcut_VALUE(1),b'TERMINAL FOCUS 4');handle_avveniment(.2)
            shell('echo REUSED_WINDOW_OK')
            완료량=LOG_RECORD.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            ttermina_OFFSET=time.monotonic()+.3
            while time.monotonic()<ttermina_OFFSET:handle_avveniment(.05)
            with socket.socket(socket.AF_UNIX) as kodiċi_tal_karattru:
                kodiċi_tal_karattru.settimeout(10);kodiċi_tal_karattru.connect(str(모의제어접속))
                with kodiċi_tal_karattru.makefile('rwb') as fajl_entrata:
                    json.loads(fajl_entrata.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(destinazzjoni_VALUE_pożizzjoni/'four-terminals.png'),'format':'png'}}):
                        fajl_entrata.write((json.dumps(요청값)+'\n').encode());fajl_entrata.flush()
                        while True:
                            반환값=json.loads(fajl_entrata.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(destinazzjoni_VALUE_pożizzjoni/'four-terminals.png')).convert('RGB')
            for par_koordinati,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(par_koordinati)==색상,(par_koordinati,화소들.getpixel(par_koordinati))
            shell('echo FOUR_WINDOWS_OK')
            validazzjoni_rapport.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if data_pożizzjoni.poll() is None:data_pożizzjoni.terminate()
            try:data_pożizzjoni.wait(timeout=5)
            except subprocess.TimeoutExpired:data_pożizzjoni.kill();data_pożizzjoni.wait()
            selettur_a916db4e.close();data_pożizzjoni.stdin.close();data_pożizzjoni.stdout.close();(destinazzjoni_VALUE_pożizzjoni/'serial.log').write_bytes(LOG_RECORD);(destinazzjoni_VALUE_pożizzjoni/'report.json').write_text(json.dumps(validazzjoni_rapport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':serje()
