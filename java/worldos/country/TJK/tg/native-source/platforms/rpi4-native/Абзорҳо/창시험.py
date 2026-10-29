#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from иҷро_кардан_фармон import 기준,фармон

def порча():
    목적위치=기준/'build/verification/windows';목적위치.mkdir(parents=True,exist_ok=True)
    санҷиши_эътибор_гузориш={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};сабт_кардан_сабт=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(фармон()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        интихобкунанда_a916db4e=selectors.DefaultSelector();интихобкунанда_a916db4e.register(자료위치.stdout,selectors.EVENT_READ)
        def дастак_рӯйдод(초단위=.1):
            for 누름값,_ in интихобкунанда_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:сабт_кардан_сабт.extend(둘째값)
            assert b'PANIC:' not in сабт_кардан_сабт and b'HALTED' not in сабт_кардан_сабт,сабт_кардан_сабт[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            анҷом_додан_Интиқолшавӣ=time.monotonic()+초단위
            while 확인표시 not in сабт_кардан_сабт[현재위치:]:
                if time.monotonic()>анҷом_додан_Интиқолшавӣ or 자료위치.poll() is not None:raise AssertionError(сабт_кардан_сабт[현재위치:].decode('utf-8','replace'))
                дастак_рӯйдод()
            return bytes(сабт_кардан_сабт[현재위치:])
        def фиристодан(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(сабт_кардан_сабт);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def восит(сатр_иттилоот):return фиристодан((сатр_иттилоот+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def миёнбур_қимат(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def зер_кардан_тугма(координатаи_х,세로좌표):return bytes([30,1,1,координатаи_х&255,координатаи_х>>8,세로좌표&255,세로좌표>>8,30,1,0,координатаи_х&255,координатаи_х>>8,세로좌표&255,세로좌표>>8])
        def фармон_ҳолат():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();анҷом_додан_Интиқолшавӣ=time.monotonic()+.2
            while time.monotonic()<анҷом_додан_Интиқолшавӣ:дастак_рӯйдод(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            восит('terminal');дастак_рӯйдод(.3)
            восит('mkdir first; cd first; export NAME=one')
            фиристодан('vi 첫째.py\n'.encode(),b'NORMAL')
            фиристодан('i값 = 21\nprint(қимат * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            анҷом_додан_Интиқолшавӣ=time.monotonic()+3
            while time.monotonic()<анҷом_додан_Интиқолшавӣ:дастак_рӯйдод(.1)
            фиристодан(миёнбур_қимат(1),b'TERMINAL FOCUS 2');дастак_рӯйдод(.2)
            assert b'/\r\n' in восит('pwd')
            восит('export NAME=two')
            фиристодан('vi 둘째.txt\n'.encode(),b'NORMAL')
            фиристодан('i두 번째 равзана\n'.encode(),b'INSERT')
            фиристодан(зер_кардан_тугма(180,12),b'TERMINAL FOCUS 1');дастак_рӯйдод(.2)
            фармон_ҳолат();фиристодан(b':wq\r')
            assert b'one:/first' in восит('echo "$NAME:$PWD"')
            assert 'қимат = 21\r\nprint(қимат * 2)'.encode() in восит('cat 첫째.py')
            결과=восит('python 첫째.py');assert b'42\r\n' in 결과,결과
            # Close the first shell with its actual title-bar X; second editor resumes.
            фиристодан(зер_кардан_тугма(560,63),b'TERMINAL FOCUS 2');дастак_рӯйдод(.2)
            фармон_ҳолат();фиристодан(b':wq\r')
            assert b'two:/' in восит('echo "$NAME:$PWD"')
            assert '두 번째 равзана'.encode() in восит('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            фиристодан('vi 둘째.txt\n'.encode(),b'NORMAL');фиристодан(b'xu',b'NORMAL')
            фиристодан(b'iX',b'INSERT');фармон_ҳолат();фиристодан(b':q\r',b'Unsaved')
            фиристодан(b':q!\r');assert '두 번째 равзана'.encode() in восит('cat 둘째.txt')
            фиристодан(миёнбур_қимат(1),b'TERMINAL FOCUS 1');дастак_рӯйдод(.2)
            фиристодан(миёнбур_қимат(1),b'TERMINAL FOCUS 3');дастак_рӯйдод(.2)
            фиристодан(миёнбур_қимат(1),b'TERMINAL FOCUS 4');дастак_рӯйдод(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            자료위치.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));자료위치.stdin.flush()
            восит('echo DRAGGED_OK')
            фиристодан('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            фиристодан('i저장하지 않은 иттилоот'.encode(),b'INSERT')
            фиристодан(зер_кардан_тугма(578,97),b'TERMINAL FOCUS 3');дастак_рӯйдод(.2)
            assert '버릴문서.txt'.encode() not in восит('ls')
            фиристодан(миёнбур_қимат(1),b'TERMINAL FOCUS 4');дастак_рӯйдод(.2)
            восит('echo REUSED_WINDOW_OK')
            완료량=сабт_кардан_сабт.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            анҷом_додан_Интиқолшавӣ=time.monotonic()+.3
            while time.monotonic()<анҷом_додан_Интиқолшавӣ:дастак_рӯйдод(.05)
            with socket.socket(socket.AF_UNIX) as рамзи_аломат:
                рамзи_аломат.settimeout(10);рамзи_аломат.connect(str(모의제어접속))
                with рамзи_аломат.makefile('rwb') as файл_ворида:
                    json.loads(файл_ворида.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'four-terminals.png'),'format':'png'}}):
                        файл_ворида.write((json.dumps(요청값)+'\n').encode());файл_ворида.flush()
                        while True:
                            반환값=json.loads(файл_ворида.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(목적위치/'four-terminals.png')).convert('RGB')
            for ҷуфти_координат,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(ҷуфти_координат)==색상,(ҷуфти_координат,화소들.getpixel(ҷуфти_координат))
            восит('echo FOUR_WINDOWS_OK')
            санҷиши_эътибор_гузориш.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            интихобкунанда_a916db4e.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(сабт_кардан_сабт);(목적위치/'report.json').write_text(json.dumps(санҷиши_эътибор_гузориш,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':порча()
