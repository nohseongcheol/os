#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from keyra_skipun import verk_rót,Skipun

def Keyra_2():
    endastaður_VALUE_staða=verk_rót/'build/verification/windows';endastaður_VALUE_staða.mkdir(parents=True,exist_ok=True)
    prófun_skrá={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((verk_rót/'build/kernel8.img').read_bytes()).hexdigest()};LOG_lína=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        gögn_staða=subprocess.Popen(Skipun()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        val_a916db4e=selectors.DefaultSelector();val_a916db4e.register(gögn_staða.stdout,selectors.EVENT_READ)
        def hald_atvik(초단위=.1):
            for 누름값,_ in val_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_lína.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_lína and b'HALTED' not in LOG_lína,LOG_lína[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            ljúka_OFFSET=time.monotonic()+초단위
            while 확인표시 not in LOG_lína[현재위치:]:
                if time.monotonic()>ljúka_OFFSET or gögn_staða.poll() is not None:raise AssertionError(LOG_lína[현재위치:].decode('utf-8','replace'))
                hald_atvik()
            return bytes(LOG_lína[현재위치:])
        def senda(SECOND_VALUE,확인표시=b'jkoros-native> '):
            현재위치=len(LOG_lína);gögn_staða.stdin.write(SECOND_VALUE);gögn_staða.stdin.flush();return 기다리기(확인표시,현재위치)
        def skel(strengur_gögn):return senda((strengur_gögn+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def flýtileið_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def smella_hnappur(x_hnit,Y_hnit):return bytes([30,1,1,x_hnit&255,x_hnit>>8,Y_hnit&255,Y_hnit>>8,30,1,0,x_hnit&255,x_hnit>>8,Y_hnit&255,Y_hnit>>8])
        def skipun_MODE():
            gögn_staða.stdin.write(b'\x1b');gögn_staða.stdin.flush();ljúka_OFFSET=time.monotonic()+.2
            while time.monotonic()<ljúka_OFFSET:hald_atvik(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            skel('terminal');hald_atvik(.3)
            skel('mkdir first; cd first; export NAME=one')
            senda('vi 첫째.py\n'.encode(),b'NORMAL')
            senda('i값 = 21\nprint(VALUE * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            ljúka_OFFSET=time.monotonic()+3
            while time.monotonic()<ljúka_OFFSET:hald_atvik(.1)
            senda(flýtileið_VALUE(1),b'TERMINAL FOCUS 2');hald_atvik(.2)
            assert b'/\r\n' in skel('pwd')
            skel('export NAME=two')
            senda('vi 둘째.txt\n'.encode(),b'NORMAL')
            senda('i두 번째 Gluggi\n'.encode(),b'INSERT')
            senda(smella_hnappur(180,12),b'TERMINAL FOCUS 1');hald_atvik(.2)
            skipun_MODE();senda(b':wq\r')
            assert b'one:/first' in skel('echo "$NAME:$PWD"')
            assert 'VALUE = 21\r\nprint(VALUE * 2)'.encode() in skel('cat 첫째.py')
            NIÐURSTAÐA=skel('python 첫째.py');assert b'42\r\n' in NIÐURSTAÐA,NIÐURSTAÐA
            # Close the first shell with its actual title-bar X; second editor resumes.
            senda(smella_hnappur(560,63),b'TERMINAL FOCUS 2');hald_atvik(.2)
            skipun_MODE();senda(b':wq\r')
            assert b'two:/' in skel('echo "$NAME:$PWD"')
            assert '두 번째 Gluggi'.encode() in skel('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            senda('vi 둘째.txt\n'.encode(),b'NORMAL');senda(b'xu',b'NORMAL')
            senda(b'iX',b'INSERT');skipun_MODE();senda(b':q\r',b'Unsaved')
            senda(b':q!\r');assert '두 번째 Gluggi'.encode() in skel('cat 둘째.txt')
            senda(flýtileið_VALUE(1),b'TERMINAL FOCUS 1');hald_atvik(.2)
            senda(flýtileið_VALUE(1),b'TERMINAL FOCUS 3');hald_atvik(.2)
            senda(flýtileið_VALUE(1),b'TERMINAL FOCUS 4');hald_atvik(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            gögn_staða.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));gögn_staða.stdin.flush()
            skel('echo DRAGGED_OK')
            senda('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            senda('i저장하지 않은 gögn'.encode(),b'INSERT')
            senda(smella_hnappur(578,97),b'TERMINAL FOCUS 3');hald_atvik(.2)
            assert '버릴문서.txt'.encode() not in skel('ls')
            senda(flýtileið_VALUE(1),b'TERMINAL FOCUS 4');hald_atvik(.2)
            skel('echo REUSED_WINDOW_OK')
            lokið_upphæð=LOG_lína.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',lokið_upphæð)
            # UART completion precedes the next QEMU display refresh.
            ljúka_OFFSET=time.monotonic()+.3
            while time.monotonic()<ljúka_OFFSET:hald_atvik(.05)
            with socket.socket(socket.AF_UNIX) as stafkóði:
                stafkóði.settimeout(10);stafkóði.connect(str(모의제어접속))
                with stafkóði.makefile('rwb') as skrá_færsla_3d0c1245:
                    json.loads(skrá_færsla_3d0c1245.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(endastaður_VALUE_staða/'four-terminals.png'),'format':'png'}}):
                        skrá_færsla_3d0c1245.write((json.dumps(요청값)+'\n').encode());skrá_færsla_3d0c1245.flush()
                        while True:
                            반환값=json.loads(skrá_færsla_3d0c1245.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(endastaður_VALUE_staða/'four-terminals.png')).convert('RGB')
            for hnitapar,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(hnitapar)==색상,(hnitapar,화소들.getpixel(hnitapar))
            skel('echo FOUR_WINDOWS_OK')
            prófun_skrá.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if gögn_staða.poll() is None:gögn_staða.terminate()
            try:gögn_staða.wait(timeout=5)
            except subprocess.TimeoutExpired:gögn_staða.kill();gögn_staða.wait()
            val_a916db4e.close();gögn_staða.stdin.close();gögn_staða.stdout.close();(endastaður_VALUE_staða/'serial.log').write_bytes(LOG_lína);(endastaður_VALUE_staða/'report.json').write_text(json.dumps(prófun_skrá,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Keyra_2()
