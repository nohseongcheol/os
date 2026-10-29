#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from అమలు_చేయి_ఆదేశం import ప్రొజెక్ట్_మూలం,ఆదేశము

def నడుపుము():
    గమ్యం_మూల్యం_స్థాయి=ప్రొజెక్ట్_మూలం/'build/verification/swing';గమ్యం_మూల్యం_స్థాయి.mkdir(parents=True,exist_ok=True)
    తరగతి_పథం=ప్రొజెక్ట్_మూలం/'build/verification/new-java';తరగతి_పథం.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(ప్రొజెక్ట్_మూలం/'dist/jkoros-native-korean.jar'),'-d',str(తరగతి_పథం),str(ప్రొజెక్ట్_మూలం/'시험/자바/스윙시험.java'),str(ప్రొజెక్ట్_మూలం/'시험/자바/한글창시험.java')])
    నిర్ధారణ_నివేదిక={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ప్రొజెక్ట్_మూలం/'build/kernel8.img').read_bytes()).hexdigest()};లాగ్_వరుస=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        డేటా_స్థాయి=subprocess.Popen(ఆదేశము()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        సెలక్టర్_a916db4e=selectors.DefaultSelector();సెలక్టర్_a916db4e.register(డేటా_స్థాయి.stdout,selectors.EVENT_READ)
        def నిర్వాహకం_ఈవెంట్(초단위=.1):
            for 누름값,_ in సెలక్టర్_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:లాగ్_వరుస.extend(둘째값)
            assert b'PANIC:' not in లాగ్_వరుస and b'HALTED' not in లాగ్_వరుస,లాగ్_వరుస[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            ముగించు_ఆఫ్_సెట్=time.monotonic()+초단위
            while 확인표시 not in లాగ్_వరుస[현재위치:]:
                if time.monotonic()>ముగించు_ఆఫ్_సెట్ or డేటా_స్థాయి.poll() is not None:raise AssertionError(లాగ్_వరుస[현재위치:].decode('utf-8','replace'))
                నిర్వాహకం_ఈవెంట్()
            return bytes(లాగ్_వరుస[현재위치:])
        def పంపు(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(లాగ్_వరుస);డేటా_స్థాయి.stdin.write(둘째값);డేటా_స్థాయి.stdin.flush();return 기다리기(확인표시,현재위치)
        def షెల్(అక్షరసరం_డేటా):return పంపు((అక్షరసరం_డేటా+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def సత్వరమార్గం_మూల్యం(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def క్లిక్_చెయండి_బటన్(x_నిర్దేశాంకం,Y_బటన్_సమన్వయపరుచు):return bytes([30,1,1,x_నిర్దేశాంకం&255,x_నిర్దేశాంకం>>8,Y_బటన్_సమన్వయపరుచు&255,Y_బటన్_సమన్వయపరుచు>>8,30,1,0,x_నిర్దేశాంకం&255,x_నిర్దేశాంకం>>8,Y_బటన్_సమన్వయపరుచు&255,Y_బటన్_సమన్వయపరుచు>>8])
        def ఆదేశం_మోడ్():
            డేటా_స్థాయి.stdin.write(b'\x1b');డేటా_స్థాయి.stdin.flush();ముగించు_ఆఫ్_సెట్=time.monotonic()+.2
            while time.monotonic()<ముగించు_ఆఫ్_సెట్:నిర్వాహకం_ఈవెంట్(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            షెల్('terminal');నిర్వాహకం_ఈవెంట్(.3)
            డేటా=(ప్రొజెక్ట్_మూలం/'build/verification/new-java/스윙시험.class').read_bytes()
            పంపు('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(డేటా),64):పంపు(డేటా[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            పంపు(b'.\n')
            పంపు('java 스윙시험\n'.encode(),b'SWING READY')
            ముగించు_ఆఫ్_సెట్=time.monotonic()+3
            while time.monotonic()<ముగించు_ఆఫ్_సెట్:నిర్వాహకం_ఈవెంట్(.1)
            # JFrame centered at (120,100), content at y=130.
            పంపు(క్లిక్_చెయండి_బటన్(200,210),b'',)  # focus JTextField
            డేటా_స్థాయి.stdin.write('누리'.encode());డేటా_స్థాయి.stdin.flush()
            ముగించు_ఆఫ్_సెట్=time.monotonic()+.3
            while time.monotonic()<ముగించు_ఆఫ్_సెట్:నిర్వాహకం_ఈవెంట్(.05)
            ప్రమాణం=పంపు(క్లిక్_చెయండి_బటన్(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(లాగ్_వరుస)-len(ప్రమాణం))
            పంపు(సత్వరమార్గం_మూల్యం(1),b'TERMINAL FOCUS 2')
            ప్రమాణం=షెల్('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in ప్రమాణం
            పంపు(క్లిక్_చెయండి_బటన్(180,12),b'TERMINAL FOCUS 1')
            ముగించు_ఆఫ్_సెట్=time.monotonic()+.3
            while time.monotonic()<ముగించు_ఆఫ్_సెట్:నిర్వాహకం_ఈవెంట్(.05)
            with socket.socket(socket.AF_UNIX) as అక్షర_కోడ్:
                అక్షర_కోడ్.settimeout(10);అక్షర_కోడ్.connect(str(모의제어접속))
                with అక్షర_కోడ్.makefile('rwb') as ఫైలు_ప్రవేశం:
                    json.loads(ఫైలు_ప్రవేశం.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(గమ్యం_మూల్యం_స్థాయి/'native-swing.png'),'format':'png'}}):
                        ఫైలు_ప్రవేశం.write((json.dumps(요청값)+'\n').encode());ఫైలు_ప్రవేశం.flush()
                        while True:
                            반환값=json.loads(ఫైలు_ప్రవేశం.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            పంపు(క్లిక్_చెయండి_బటన్(505,115))
            షెల్('echo SWING_CLOSED_OK')
            డేటా=(తరగతి_పథం/'한글창시험.class').read_bytes()
            పంపు('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(డేటా),64):పంపు(డేటా[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            పంపు(b'.\n')
            పంపు('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            పంపు(క్లిక్_చెయండి_బటన్(200,255),'KOREAN SWING CLICK పేరు'.encode())
            పంపు(క్లిక్_చెయండి_బటన్(505,115))
            షెల్('echo KOREAN_SWING_CLOSED_OK')
            నిర్ధారణ_నివేదిక.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 విండో/బటన్/동작알림/ఈవెంట్_నిరీక్షణ_క్రమం directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if డేటా_స్థాయి.poll() is None:డేటా_స్థాయి.terminate()
            try:డేటా_స్థాయి.wait(timeout=5)
            except subprocess.TimeoutExpired:డేటా_స్థాయి.kill();డేటా_స్థాయి.wait()
            సెలక్టర్_a916db4e.close();డేటా_స్థాయి.stdin.close();డేటా_స్థాయి.stdout.close();(గమ్యం_మూల్యం_స్థాయి/'serial.log').write_bytes(లాగ్_వరుస);(గమ్యం_మూల్యం_స్థాయి/'report.json').write_text(json.dumps(నిర్ధారణ_నివేదిక,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':నడుపుము()
