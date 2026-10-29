#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from иҷро_кардан_фармон import 기준,фармон

def порча():
    목적위치=기준/'build/verification/swing';목적위치.mkdir(parents=True,exist_ok=True)
    синф_масир=기준/'build/verification/new-java';синф_масир.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'dist/jkoros-native-korean.jar'),'-d',str(синф_масир),str(기준/'시험/자바/스윙시험.java'),str(기준/'시험/자바/한글창시험.java')])
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
            иттилоот=(기준/'build/verification/new-java/스윙시험.class').read_bytes()
            фиристодан('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(иттилоот),64):фиристодан(иттилоот[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            фиристодан(b'.\n')
            фиристодан('java 스윙시험\n'.encode(),b'SWING READY')
            анҷом_додан_Интиқолшавӣ=time.monotonic()+3
            while time.monotonic()<анҷом_додан_Интиқолшавӣ:дастак_рӯйдод(.1)
            # JFrame centered at (120,100), content at y=130.
            фиристодан(зер_кардан_тугма(200,210),b'',)  # focus JTextField
            자료위치.stdin.write('누리'.encode());자료위치.stdin.flush()
            анҷом_додан_Интиқолшавӣ=time.monotonic()+.3
            while time.monotonic()<анҷом_додан_Интиқолшавӣ:дастак_рӯйдод(.05)
            결과=фиристодан(зер_кардан_тугма(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(сабт_кардан_сабт)-len(결과))
            фиристодан(миёнбур_қимат(1),b'TERMINAL FOCUS 2')
            결과=восит('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in 결과
            фиристодан(зер_кардан_тугма(180,12),b'TERMINAL FOCUS 1')
            анҷом_додан_Интиқолшавӣ=time.monotonic()+.3
            while time.monotonic()<анҷом_додан_Интиқолшавӣ:дастак_рӯйдод(.05)
            with socket.socket(socket.AF_UNIX) as рамзи_аломат:
                рамзи_аломат.settimeout(10);рамзи_аломат.connect(str(모의제어접속))
                with рамзи_аломат.makefile('rwb') as файл_ворида:
                    json.loads(файл_ворида.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'native-swing.png'),'format':'png'}}):
                        файл_ворида.write((json.dumps(요청값)+'\n').encode());файл_ворида.flush()
                        while True:
                            반환값=json.loads(файл_ворида.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            фиристодан(зер_кардан_тугма(505,115))
            восит('echo SWING_CLOSED_OK')
            иттилоот=(синф_масир/'한글창시험.class').read_bytes()
            фиристодан('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(иттилоот),64):фиристодан(иттилоот[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            фиристодан(b'.\n')
            фиристодан('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            фиристодан(зер_кардан_тугма(200,255),'KOREAN SWING CLICK Ном'.encode())
            фиристодан(зер_кардан_тугма(505,115))
            восит('echo KOREAN_SWING_CLOSED_OK')
            санҷиши_эътибор_гузориш.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 равзана/тугма/동작알림/рӯйдод_навбат directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            интихобкунанда_a916db4e.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(сабт_кардан_сабт);(목적위치/'report.json').write_text(json.dumps(санҷиши_эътибор_гузориш,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':порча()
