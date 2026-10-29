#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from орындау_пәрмен import жоба_түбір,Команда

def Орындау_2():
    тағайындау_мән_лауазым=жоба_түбір/'build/verification/swing';тағайындау_мән_лауазым.mkdir(parents=True,exist_ok=True)
    оқу_жол=жоба_түбір/'build/verification/new-java';оқу_жол.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(жоба_түбір/'dist/jkoros-native-korean.jar'),'-d',str(оқу_жол),str(жоба_түбір/'시험/자바/스윙시험.java'),str(жоба_түбір/'시험/자바/한글창시험.java')])
    тексерім_есеп={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((жоба_түбір/'build/kernel8.img').read_bytes()).hexdigest()};журнал_жол=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        деректер_лауазым=subprocess.Popen(Команда()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        селектор_a916db4e=selectors.DefaultSelector();селектор_a916db4e.register(деректер_лауазым.stdout,selectors.EVENT_READ)
        def дескриптор_оқиға(초단위=.1):
            for 누름값,_ in селектор_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:журнал_жол.extend(둘째값)
            assert b'PANIC:' not in журнал_жол and b'HALTED' not in журнал_жол,журнал_жол[-2048:]
        def 기다리기(확인표시,ток_лауазым,초단위=50):
            тоқтату_жылжыту=time.monotonic()+초단위
            while 확인표시 not in журнал_жол[ток_лауазым:]:
                if time.monotonic()>тоқтату_жылжыту or деректер_лауазым.poll() is not None:raise AssertionError(журнал_жол[ток_лауазым:].decode('utf-8','replace'))
                дескриптор_оқиға()
            return bytes(журнал_жол[ток_лауазым:])
        def жіберу(둘째값,확인표시=b'jkoros-native> '):
            ток_лауазым=len(журнал_жол);деректер_лауазым.stdin.write(둘째값);деректер_лауазым.stdin.flush();return 기다리기(확인표시,ток_лауазым)
        def қоршам(жол_деректер):return жіберу((жол_деректер+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def таңбаша_мән(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def басу_түйме(x_координатасы,Y_түймешігі_координата):return bytes([30,1,1,x_координатасы&255,x_координатасы>>8,Y_түймешігі_координата&255,Y_түймешігі_координата>>8,30,1,0,x_координатасы&255,x_координатасы>>8,Y_түймешігі_координата&255,Y_түймешігі_координата>>8])
        def пәрмен_режим():
            деректер_лауазым.stdin.write(b'\x1b');деректер_лауазым.stdin.flush();тоқтату_жылжыту=time.monotonic()+.2
            while time.monotonic()<тоқтату_жылжыту:дескриптор_оқиға(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            қоршам('terminal');дескриптор_оқиға(.3)
            деректер=(жоба_түбір/'build/verification/new-java/스윙시험.class').read_bytes()
            жіберу('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(деректер),64):жіберу(деректер[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            жіберу(b'.\n')
            жіберу('java 스윙시험\n'.encode(),b'SWING READY')
            тоқтату_жылжыту=time.monotonic()+3
            while time.monotonic()<тоқтату_жылжыту:дескриптор_оқиға(.1)
            # JFrame centered at (120,100), content at y=130.
            жіберу(басу_түйме(200,210),b'',)  # focus JTextField
            деректер_лауазым.stdin.write('누리'.encode());деректер_лауазым.stdin.flush()
            тоқтату_жылжыту=time.monotonic()+.3
            while time.monotonic()<тоқтату_жылжыту:дескриптор_оқиға(.05)
            НӘТИЖЕ=жіберу(басу_түйме(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(журнал_жол)-len(НӘТИЖЕ))
            жіберу(таңбаша_мән(1),b'TERMINAL FOCUS 2')
            НӘТИЖЕ=қоршам('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in НӘТИЖЕ
            жіберу(басу_түйме(180,12),b'TERMINAL FOCUS 1')
            тоқтату_жылжыту=time.monotonic()+.3
            while time.monotonic()<тоқтату_жылжыту:дескриптор_оқиға(.05)
            with socket.socket(socket.AF_UNIX) as таңба_коды:
                таңба_коды.settimeout(10);таңба_коды.connect(str(모의제어접속))
                with таңба_коды.makefile('rwb') as файл_енгізу:
                    json.loads(файл_енгізу.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(тағайындау_мән_лауазым/'native-swing.png'),'format':'png'}}):
                        файл_енгізу.write((json.dumps(요청값)+'\n').encode());файл_енгізу.flush()
                        while True:
                            반환값=json.loads(файл_енгізу.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            жіберу(басу_түйме(505,115))
            қоршам('echo SWING_CLOSED_OK')
            деректер=(оқу_жол/'한글창시험.class').read_bytes()
            жіберу('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(деректер),64):жіберу(деректер[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            жіберу(b'.\n')
            жіберу('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            жіберу(басу_түйме(200,255),'KOREAN SWING CLICK Аты'.encode())
            жіберу(басу_түйме(505,115))
            қоршам('echo KOREAN_SWING_CLOSED_OK')
            тексерім_есеп.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 Терезе/батырма/동작알림/оқиға_кезек directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if деректер_лауазым.poll() is None:деректер_лауазым.terminate()
            try:деректер_лауазым.wait(timeout=5)
            except subprocess.TimeoutExpired:деректер_лауазым.kill();деректер_лауазым.wait()
            селектор_a916db4e.close();деректер_лауазым.stdin.close();деректер_лауазым.stdout.close();(тағайындау_мән_лауазым/'serial.log').write_bytes(журнал_жол);(тағайындау_мән_лауазым/'report.json').write_text(json.dumps(тексерім_есеп,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Орындау_2()
