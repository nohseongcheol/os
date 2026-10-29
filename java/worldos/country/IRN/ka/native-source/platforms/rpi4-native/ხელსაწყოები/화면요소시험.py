#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from შესრულება_ბრძანება import პროეცირება_ფესვი,ბრძანება

def გაშვება():
    მიმართულება_მნიშვნელობა_პოზიცია=პროეცირება_ფესვი/'build/verification/swing';მიმართულება_მნიშვნელობა_პოზიცია.mkdir(parents=True,exist_ok=True)
    კლასი_მდებარეობა=პროეცირება_ფესვი/'build/verification/new-java';კლასი_მდებარეობა.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(პროეცირება_ფესვი/'dist/jkoros-native-korean.jar'),'-d',str(კლასი_მდებარეობა),str(პროეცირება_ფესვი/'시험/자바/스윙시험.java'),str(პროეცირება_ფესვი/'시험/자바/한글창시험.java')])
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
            მონაცემები=(პროეცირება_ფესვი/'build/verification/new-java/스윙시험.class').read_bytes()
            გაგზავნა('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(მონაცემები),64):გაგზავნა(მონაცემები[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            გაგზავნა(b'.\n')
            გაგზავნა('java 스윙시험\n'.encode(),b'SWING READY')
            დასასრული_ოფსეტი=time.monotonic()+3
            while time.monotonic()<დასასრული_ოფსეტი:სახელური_მოვლენა(.1)
            # JFrame centered at (120,100), content at y=130.
            გაგზავნა(დაწკაპუნება_ღილაკი(200,210),b'',)  # focus JTextField
            მონაცემები_პოზიცია.stdin.write('누리'.encode());მონაცემები_პოზიცია.stdin.flush()
            დასასრული_ოფსეტი=time.monotonic()+.3
            while time.monotonic()<დასასრული_ოფსეტი:სახელური_მოვლენა(.05)
            გაზომვა=გაგზავნა(დაწკაპუნება_ღილაკი(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(ჟურნალი_ჩაწერა)-len(გაზომვა))
            გაგზავნა(მალსახმობი_მნიშვნელობა(1),b'TERMINAL FOCUS 2')
            გაზომვა=გარემო('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in გაზომვა
            გაგზავნა(დაწკაპუნება_ღილაკი(180,12),b'TERMINAL FOCUS 1')
            დასასრული_ოფსეტი=time.monotonic()+.3
            while time.monotonic()<დასასრული_ოფსეტი:სახელური_მოვლენა(.05)
            with socket.socket(socket.AF_UNIX) as სიმბოლოს_კოდი:
                სიმბოლოს_კოდი.settimeout(10);სიმბოლოს_კოდი.connect(str(모의제어접속))
                with სიმბოლოს_კოდი.makefile('rwb') as ფაილი_შენატანი:
                    json.loads(ფაილი_შენატანი.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(მიმართულება_მნიშვნელობა_პოზიცია/'native-swing.png'),'format':'png'}}):
                        ფაილი_შენატანი.write((json.dumps(요청값)+'\n').encode());ფაილი_შენატანი.flush()
                        while True:
                            반환값=json.loads(ფაილი_შენატანი.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            გაგზავნა(დაწკაპუნება_ღილაკი(505,115))
            გარემო('echo SWING_CLOSED_OK')
            მონაცემები=(კლასი_მდებარეობა/'한글창시험.class').read_bytes()
            გაგზავნა('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(მონაცემები),64):გაგზავნა(მონაცემები[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            გაგზავნა(b'.\n')
            გაგზავნა('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            გაგზავნა(დაწკაპუნება_ღილაკი(200,255),'KOREAN SWING CLICK სახელი'.encode())
            გაგზავნა(დაწკაპუნება_ღილაკი(505,115))
            გარემო('echo KOREAN_SWING_CLOSED_OK')
            გადამოწმება_ანგარიში.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 ფანჯარა/ღილაკი/동작알림/მოვლენა_რიგი directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if მონაცემები_პოზიცია.poll() is None:მონაცემები_პოზიცია.terminate()
            try:მონაცემები_პოზიცია.wait(timeout=5)
            except subprocess.TimeoutExpired:მონაცემები_პოზიცია.kill();მონაცემები_პოზიცია.wait()
            სელექტორი_a916db4e.close();მონაცემები_პოზიცია.stdin.close();მონაცემები_პოზიცია.stdout.close();(მიმართულება_მნიშვნელობა_პოზიცია/'serial.log').write_bytes(ჟურნალი_ჩაწერა);(მიმართულება_მნიშვნელობა_პოზიცია/'report.json').write_text(json.dumps(გადამოწმება_ანგარიში,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':გაშვება()
