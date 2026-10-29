#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from შესრულება_ბრძანება import პროეცირება_ფესვი,ბრძანება

def გაშვება():
    მიმართულება_მნიშვნელობა_პოზიცია=პროეცირება_ფესვი/'build/verification/windows';მიმართულება_მნიშვნელობა_პოზიცია.mkdir(parents=True,exist_ok=True)
    გადამოწმება_ანგარიში={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((პროეცირება_ფესვი/'build/kernel8.img').read_bytes()).hexdigest()};ჟურნალი_ჩაწერა=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        მონაცემები_პოზიცია=subprocess.Popen(ბრძანება()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        სელექტორი_a916db4e=selectors.DefaultSelector();სელექტორი_a916db4e.register(მონაცემები_პოზიცია.stdout,selectors.EVENT_READ)
        def სახელური_მოვლენა(초단위=.1):
            for 누름값,_ in სელექტორი_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:ჟურნალი_ჩაწერა.extend(둘째값)
            assert b'PANIC:' not in ჟურნალი_ჩაწერა and b'HALTED' not in ჟურნალი_ჩაწერა,ჟურნალი_ჩაწერა[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            დასასრული_ოფსეტი=time.monotonic()+초단위
            while 확인표시 not in ჟურნალი_ჩაწერა[현재위치:]:
                if time.monotonic()>დასასრული_ოფსეტი or მონაცემები_პოზიცია.poll() is not None:raise AssertionError(ჟურნალი_ჩაწერა[현재위치:].decode('utf-8','replace'))
                სახელური_მოვლენა()
            return bytes(ჟურნალი_ჩაწერა[현재위치:])
        def გაგზავნა(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(ჟურნალი_ჩაწერა);მონაცემები_პოზიცია.stdin.write(둘째값);მონაცემები_პოზიცია.stdin.flush();return 기다리기(확인표시,현재위치)
        def გარემო(სტრიქონი_მონაცემები):return გაგზავნა((სტრიქონი_მონაცემები+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def მალსახმობი_მნიშვნელობა(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def დაწკაპუნება_ღილაკი(x_კოორდინატა,Y_ღილაკი_კოორდინატი):return bytes([30,1,1,x_კოორდინატა&255,x_კოორდინატა>>8,Y_ღილაკი_კოორდინატი&255,Y_ღილაკი_კოორდინატი>>8,30,1,0,x_კოორდინატა&255,x_კოორდინატა>>8,Y_ღილაკი_კოორდინატი&255,Y_ღილაკი_კოორდინატი>>8])
        def ბრძანება_რეჟიმი():
            მონაცემები_პოზიცია.stdin.write(b'\x1b');მონაცემები_პოზიცია.stdin.flush();დასასრული_ოფსეტი=time.monotonic()+.2
            while time.monotonic()<დასასრული_ოფსეტი:სახელური_მოვლენა(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            გარემო('terminal');სახელური_მოვლენა(.3)
            გარემო('mkdir first; cd first; export NAME=one')
            გაგზავნა('vi 첫째.py\n'.encode(),b'NORMAL')
            გაგზავნა('i값 = 21\nprint(მნიშვნელობა * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            დასასრული_ოფსეტი=time.monotonic()+3
            while time.monotonic()<დასასრული_ოფსეტი:სახელური_მოვლენა(.1)
            გაგზავნა(მალსახმობი_მნიშვნელობა(1),b'TERMINAL FOCUS 2');სახელური_მოვლენა(.2)
            assert b'/\r\n' in გარემო('pwd')
            გარემო('export NAME=two')
            გაგზავნა('vi 둘째.txt\n'.encode(),b'NORMAL')
            გაგზავნა('i두 번째 ფანჯარა\n'.encode(),b'INSERT')
            გაგზავნა(დაწკაპუნება_ღილაკი(180,12),b'TERMINAL FOCUS 1');სახელური_მოვლენა(.2)
            ბრძანება_რეჟიმი();გაგზავნა(b':wq\r')
            assert b'one:/first' in გარემო('echo "$NAME:$PWD"')
            assert 'მნიშვნელობა = 21\r\nprint(მნიშვნელობა * 2)'.encode() in გარემო('cat 첫째.py')
            გაზომვა=გარემო('python 첫째.py');assert b'42\r\n' in გაზომვა,გაზომვა
            # Close the first shell with its actual title-bar X; second editor resumes.
            გაგზავნა(დაწკაპუნება_ღილაკი(560,63),b'TERMINAL FOCUS 2');სახელური_მოვლენა(.2)
            ბრძანება_რეჟიმი();გაგზავნა(b':wq\r')
            assert b'two:/' in გარემო('echo "$NAME:$PWD"')
            assert '두 번째 ფანჯარა'.encode() in გარემო('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            გაგზავნა('vi 둘째.txt\n'.encode(),b'NORMAL');გაგზავნა(b'xu',b'NORMAL')
            გაგზავნა(b'iX',b'INSERT');ბრძანება_რეჟიმი();გაგზავნა(b':q\r',b'Unsaved')
            გაგზავნა(b':q!\r');assert '두 번째 ფანჯარა'.encode() in გარემო('cat 둘째.txt')
            გაგზავნა(მალსახმობი_მნიშვნელობა(1),b'TERMINAL FOCUS 1');სახელური_მოვლენა(.2)
            გაგზავნა(მალსახმობი_მნიშვნელობა(1),b'TERMINAL FOCUS 3');სახელური_მოვლენა(.2)
            გაგზავნა(მალსახმობი_მნიშვნელობა(1),b'TERMINAL FOCUS 4');სახელური_მოვლენა(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            მონაცემები_პოზიცია.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));მონაცემები_პოზიცია.stdin.flush()
            გარემო('echo DRAGGED_OK')
            გაგზავნა('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            გაგზავნა('i저장하지 않은 მონაცემები'.encode(),b'INSERT')
            გაგზავნა(დაწკაპუნება_ღილაკი(578,97),b'TERMINAL FOCUS 3');სახელური_მოვლენა(.2)
            assert '버릴문서.txt'.encode() not in გარემო('ls')
            გაგზავნა(მალსახმობი_მნიშვნელობა(1),b'TERMINAL FOCUS 4');სახელური_მოვლენა(.2)
            გარემო('echo REUSED_WINDOW_OK')
            완료량=ჟურნალი_ჩაწერა.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            დასასრული_ოფსეტი=time.monotonic()+.3
            while time.monotonic()<დასასრული_ოფსეტი:სახელური_მოვლენა(.05)
            with socket.socket(socket.AF_UNIX) as სიმბოლოს_კოდი:
                სიმბოლოს_კოდი.settimeout(10);სიმბოლოს_კოდი.connect(str(모의제어접속))
                with სიმბოლოს_კოდი.makefile('rwb') as ფაილი_შენატანი:
                    json.loads(ფაილი_შენატანი.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(მიმართულება_მნიშვნელობა_პოზიცია/'four-terminals.png'),'format':'png'}}):
                        ფაილი_შენატანი.write((json.dumps(요청값)+'\n').encode());ფაილი_შენატანი.flush()
                        while True:
                            반환값=json.loads(ფაილი_შენატანი.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(მიმართულება_მნიშვნელობა_პოზიცია/'four-terminals.png')).convert('RGB')
            for კოორდინატთა_წყვილი,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(კოორდინატთა_წყვილი)==색상,(კოორდინატთა_წყვილი,화소들.getpixel(კოორდინატთა_წყვილი))
            გარემო('echo FOUR_WINDOWS_OK')
            გადამოწმება_ანგარიში.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if მონაცემები_პოზიცია.poll() is None:მონაცემები_პოზიცია.terminate()
            try:მონაცემები_პოზიცია.wait(timeout=5)
            except subprocess.TimeoutExpired:მონაცემები_პოზიცია.kill();მონაცემები_პოზიცია.wait()
            სელექტორი_a916db4e.close();მონაცემები_პოზიცია.stdin.close();მონაცემები_პოზიცია.stdout.close();(მიმართულება_მნიშვნელობა_პოზიცია/'serial.log').write_bytes(ჟურნალი_ჩაწერა);(მიმართულება_მნიშვნელობა_პოზიცია/'report.json').write_text(json.dumps(გადამოწმება_ანგარიში,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':გაშვება()
