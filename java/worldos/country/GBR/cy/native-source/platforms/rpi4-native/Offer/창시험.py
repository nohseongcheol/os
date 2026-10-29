#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Gweithredu_gorchymyn import prosiect_gwraidd,Gorchymyn

def Gweithredu_2():
    cyrchfan_VALUE_safle=prosiect_gwraidd/'build/verification/windows';cyrchfan_VALUE_safle.mkdir(parents=True,exist_ok=True)
    dilysu_adrodd={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((prosiect_gwraidd/'build/kernel8.img').read_bytes()).hexdigest()};LOG_rhes=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        data_safle=subprocess.Popen(Gorchymyn()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        dewisydd_a916db4e=selectors.DefaultSelector();dewisydd_a916db4e.register(data_safle.stdout,selectors.EVENT_READ)
        def dolen_digwyddiad(초단위=.1):
            for 누름값,_ in dewisydd_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_rhes.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_rhes and b'HALTED' not in LOG_rhes,LOG_rhes[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            gorffen_OFFSET=time.monotonic()+초단위
            while 확인표시 not in LOG_rhes[현재위치:]:
                if time.monotonic()>gorffen_OFFSET or data_safle.poll() is not None:raise AssertionError(LOG_rhes[현재위치:].decode('utf-8','replace'))
                dolen_digwyddiad()
            return bytes(LOG_rhes[현재위치:])
        def anfon(SECOND_VALUE,확인표시=b'jkoros-native> '):
            현재위치=len(LOG_rhes);data_safle.stdin.write(SECOND_VALUE);data_safle.stdin.flush();return 기다리기(확인표시,현재위치)
        def cragen(testun_data):return anfon((testun_data+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def llwybr_byr_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def clicio_botwm(cyfesuryn_x,Y_cyfesuryn):return bytes([30,1,1,cyfesuryn_x&255,cyfesuryn_x>>8,Y_cyfesuryn&255,Y_cyfesuryn>>8,30,1,0,cyfesuryn_x&255,cyfesuryn_x>>8,Y_cyfesuryn&255,Y_cyfesuryn>>8])
        def gorchymyn_MODE():
            data_safle.stdin.write(b'\x1b');data_safle.stdin.flush();gorffen_OFFSET=time.monotonic()+.2
            while time.monotonic()<gorffen_OFFSET:dolen_digwyddiad(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            cragen('terminal');dolen_digwyddiad(.3)
            cragen('mkdir first; cd first; export NAME=one')
            anfon('vi 첫째.py\n'.encode(),b'NORMAL')
            anfon('i값 = 21\nprint(VALUE * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            gorffen_OFFSET=time.monotonic()+3
            while time.monotonic()<gorffen_OFFSET:dolen_digwyddiad(.1)
            anfon(llwybr_byr_VALUE(1),b'TERMINAL FOCUS 2');dolen_digwyddiad(.2)
            assert b'/\r\n' in cragen('pwd')
            cragen('export NAME=two')
            anfon('vi 둘째.txt\n'.encode(),b'NORMAL')
            anfon('i두 번째 ffenestr\n'.encode(),b'INSERT')
            anfon(clicio_botwm(180,12),b'TERMINAL FOCUS 1');dolen_digwyddiad(.2)
            gorchymyn_MODE();anfon(b':wq\r')
            assert b'one:/first' in cragen('echo "$NAME:$PWD"')
            assert 'VALUE = 21\r\nprint(VALUE * 2)'.encode() in cragen('cat 첫째.py')
            mesur=cragen('python 첫째.py');assert b'42\r\n' in mesur,mesur
            # Close the first shell with its actual title-bar X; second editor resumes.
            anfon(clicio_botwm(560,63),b'TERMINAL FOCUS 2');dolen_digwyddiad(.2)
            gorchymyn_MODE();anfon(b':wq\r')
            assert b'two:/' in cragen('echo "$NAME:$PWD"')
            assert '두 번째 ffenestr'.encode() in cragen('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            anfon('vi 둘째.txt\n'.encode(),b'NORMAL');anfon(b'xu',b'NORMAL')
            anfon(b'iX',b'INSERT');gorchymyn_MODE();anfon(b':q\r',b'Unsaved')
            anfon(b':q!\r');assert '두 번째 ffenestr'.encode() in cragen('cat 둘째.txt')
            anfon(llwybr_byr_VALUE(1),b'TERMINAL FOCUS 1');dolen_digwyddiad(.2)
            anfon(llwybr_byr_VALUE(1),b'TERMINAL FOCUS 3');dolen_digwyddiad(.2)
            anfon(llwybr_byr_VALUE(1),b'TERMINAL FOCUS 4');dolen_digwyddiad(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            data_safle.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));data_safle.stdin.flush()
            cragen('echo DRAGGED_OK')
            anfon('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            anfon('i저장하지 않은 data'.encode(),b'INSERT')
            anfon(clicio_botwm(578,97),b'TERMINAL FOCUS 3');dolen_digwyddiad(.2)
            assert '버릴문서.txt'.encode() not in cragen('ls')
            anfon(llwybr_byr_VALUE(1),b'TERMINAL FOCUS 4');dolen_digwyddiad(.2)
            cragen('echo REUSED_WINDOW_OK')
            완료량=LOG_rhes.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            gorffen_OFFSET=time.monotonic()+.3
            while time.monotonic()<gorffen_OFFSET:dolen_digwyddiad(.05)
            with socket.socket(socket.AF_UNIX) as cod_nod:
                cod_nod.settimeout(10);cod_nod.connect(str(모의제어접속))
                with cod_nod.makefile('rwb') as ffeil_cofnod:
                    json.loads(ffeil_cofnod.readline())
                    for cais_HTTP_VALUE in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(cyrchfan_VALUE_safle/'four-terminals.png'),'format':'png'}}):
                        ffeil_cofnod.write((json.dumps(cais_HTTP_VALUE)+'\n').encode());ffeil_cofnod.flush()
                        while True:
                            반환값=json.loads(ffeil_cofnod.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(cyrchfan_VALUE_safle/'four-terminals.png')).convert('RGB')
            for pâr_o_gyfesurynnau,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(pâr_o_gyfesurynnau)==색상,(pâr_o_gyfesurynnau,화소들.getpixel(pâr_o_gyfesurynnau))
            cragen('echo FOUR_WINDOWS_OK')
            dilysu_adrodd.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if data_safle.poll() is None:data_safle.terminate()
            try:data_safle.wait(timeout=5)
            except subprocess.TimeoutExpired:data_safle.kill();data_safle.wait()
            dewisydd_a916db4e.close();data_safle.stdin.close();data_safle.stdout.close();(cyrchfan_VALUE_safle/'serial.log').write_bytes(LOG_rhes);(cyrchfan_VALUE_safle/'report.json').write_text(json.dumps(dilysu_adrodd,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Gweithredu_2()
