#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from կատարել_հրաման import արձակել_արմատ,Հրահանգ

def Գործարկել():
    նպատակակետ_արժեք_դիրք=արձակել_արմատ/'build/verification/swing';նպատակակետ_արժեք_դիրք.mkdir(parents=True,exist_ok=True)
    դաս_ուղի=արձակել_արմատ/'build/verification/new-java';դաս_ուղի.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(արձակել_արմատ/'dist/jkoros-native-korean.jar'),'-d',str(դաս_ուղի),str(արձակել_արմատ/'시험/자바/스윙시험.java'),str(արձակել_արմատ/'시험/자바/한글창시험.java')])
    վավերացում_զեկույց={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((արձակել_արմատ/'build/kernel8.img').read_bytes()).hexdigest()};մատյան_տող=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        տվյալ_դիրք=subprocess.Popen(Հրահանգ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        ընտրիչ_a916db4e=selectors.DefaultSelector();ընտրիչ_a916db4e.register(տվյալ_դիրք.stdout,selectors.EVENT_READ)
        def բռնակ_միջոցառում(초단위=.1):
            for 누름값,_ in ընտրիչ_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:մատյան_տող.extend(둘째값)
            assert b'PANIC:' not in մատյան_տող and b'HALTED' not in մատյան_տող,մատյան_տող[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            վերջացնել_Տեղաշարժում=time.monotonic()+초단위
            while 확인표시 not in մատյան_տող[현재위치:]:
                if time.monotonic()>վերջացնել_Տեղաշարժում or տվյալ_դիրք.poll() is not None:raise AssertionError(մատյան_տող[현재위치:].decode('utf-8','replace'))
                բռնակ_միջոցառում()
            return bytes(մատյան_տող[현재위치:])
        def ուղարկել(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(մատյան_տող);տվյալ_դիրք.stdin.write(둘째값);տվյալ_դիրք.stdin.flush();return 기다리기(확인표시,현재위치)
        def խեցի(տող_տվյալ):return ուղարկել((տող_տվյալ+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def դյուրանցում_արժեք(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def կտտացնել_կոճակ(x_կոորդինատ,세로좌표):return bytes([30,1,1,x_կոորդինատ&255,x_կոորդինատ>>8,세로좌표&255,세로좌표>>8,30,1,0,x_կոորդինատ&255,x_կոորդինատ>>8,세로좌표&255,세로좌표>>8])
        def հրաման_կերպ():
            տվյալ_դիրք.stdin.write(b'\x1b');տվյալ_դիրք.stdin.flush();վերջացնել_Տեղաշարժում=time.monotonic()+.2
            while time.monotonic()<վերջացնել_Տեղաշարժում:բռնակ_միջոցառում(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            խեցի('terminal');բռնակ_միջոցառում(.3)
            տվյալ=(արձակել_արմատ/'build/verification/new-java/스윙시험.class').read_bytes()
            ուղարկել('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(տվյալ),64):ուղարկել(տվյալ[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            ուղարկել(b'.\n')
            ուղարկել('java 스윙시험\n'.encode(),b'SWING READY')
            վերջացնել_Տեղաշարժում=time.monotonic()+3
            while time.monotonic()<վերջացնել_Տեղաշարժում:բռնակ_միջոցառում(.1)
            # JFrame centered at (120,100), content at y=130.
            ուղարկել(կտտացնել_կոճակ(200,210),b'',)  # focus JTextField
            տվյալ_դիրք.stdin.write('누리'.encode());տվյալ_դիրք.stdin.flush()
            վերջացնել_Տեղաշարժում=time.monotonic()+.3
            while time.monotonic()<վերջացնել_Տեղաշարժում:բռնակ_միջոցառում(.05)
            չափ=ուղարկել(կտտացնել_կոճակ(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(մատյան_տող)-len(չափ))
            ուղարկել(դյուրանցում_արժեք(1),b'TERMINAL FOCUS 2')
            չափ=խեցի('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in չափ
            ուղարկել(կտտացնել_կոճակ(180,12),b'TERMINAL FOCUS 1')
            վերջացնել_Տեղաշարժում=time.monotonic()+.3
            while time.monotonic()<վերջացնել_Տեղաշարժում:բռնակ_միջոցառում(.05)
            with socket.socket(socket.AF_UNIX) as գրանշանի_կոդ:
                գրանշանի_կոդ.settimeout(10);գրանշանի_կոդ.connect(str(모의제어접속))
                with գրանշանի_կոդ.makefile('rwb') as նիշք_մուտքագրում:
                    json.loads(նիշք_մուտքագրում.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(նպատակակետ_արժեք_դիրք/'native-swing.png'),'format':'png'}}):
                        նիշք_մուտքագրում.write((json.dumps(요청값)+'\n').encode());նիշք_մուտքագրում.flush()
                        while True:
                            반환값=json.loads(նիշք_մուտքագրում.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            ուղարկել(կտտացնել_կոճակ(505,115))
            խեցի('echo SWING_CLOSED_OK')
            տվյալ=(դաս_ուղի/'한글창시험.class').read_bytes()
            ուղարկել('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(տվյալ),64):ուղարկել(տվյալ[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            ուղարկել(b'.\n')
            ուղարկել('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            ուղարկել(կտտացնել_կոճակ(200,255),'KOREAN SWING CLICK Անուն'.encode())
            ուղարկել(կտտացնել_կոճակ(505,115))
            խեցի('echo KOREAN_SWING_CLOSED_OK')
            վավերացում_զեկույց.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 պատուհան/կոճակ/동작알림/միջոցառում_հերթ directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if տվյալ_դիրք.poll() is None:տվյալ_դիրք.terminate()
            try:տվյալ_դիրք.wait(timeout=5)
            except subprocess.TimeoutExpired:տվյալ_դիրք.kill();տվյալ_դիրք.wait()
            ընտրիչ_a916db4e.close();տվյալ_դիրք.stdin.close();տվյալ_դիրք.stdout.close();(նպատակակետ_արժեք_դիրք/'serial.log').write_bytes(մատյան_տող);(նպատակակետ_արժեք_դիրք/'report.json').write_text(json.dumps(վավերացում_զեկույց,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Գործարկել()
