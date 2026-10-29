#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Gweithredu_gorchymyn import prosiect_gwraidd,Gorchymyn

def Gweithredu_2():
    cyrchfan_VALUE_safle=prosiect_gwraidd/'build/verification/swing';cyrchfan_VALUE_safle.mkdir(parents=True,exist_ok=True)
    Dosbarth_llwybr=prosiect_gwraidd/'build/verification/new-java';Dosbarth_llwybr.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(prosiect_gwraidd/'dist/jkoros-native-korean.jar'),'-d',str(Dosbarth_llwybr),str(prosiect_gwraidd/'시험/자바/스윙시험.java'),str(prosiect_gwraidd/'시험/자바/한글창시험.java')])
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
            data=(prosiect_gwraidd/'build/verification/new-java/스윙시험.class').read_bytes()
            anfon('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(data),64):anfon(data[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            anfon(b'.\n')
            anfon('java 스윙시험\n'.encode(),b'SWING READY')
            gorffen_OFFSET=time.monotonic()+3
            while time.monotonic()<gorffen_OFFSET:dolen_digwyddiad(.1)
            # JFrame centered at (120,100), content at y=130.
            anfon(clicio_botwm(200,210),b'',)  # focus JTextField
            data_safle.stdin.write('누리'.encode());data_safle.stdin.flush()
            gorffen_OFFSET=time.monotonic()+.3
            while time.monotonic()<gorffen_OFFSET:dolen_digwyddiad(.05)
            mesur=anfon(clicio_botwm(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_rhes)-len(mesur))
            anfon(llwybr_byr_VALUE(1),b'TERMINAL FOCUS 2')
            mesur=cragen('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in mesur
            anfon(clicio_botwm(180,12),b'TERMINAL FOCUS 1')
            gorffen_OFFSET=time.monotonic()+.3
            while time.monotonic()<gorffen_OFFSET:dolen_digwyddiad(.05)
            with socket.socket(socket.AF_UNIX) as cod_nod:
                cod_nod.settimeout(10);cod_nod.connect(str(모의제어접속))
                with cod_nod.makefile('rwb') as ffeil_cofnod:
                    json.loads(ffeil_cofnod.readline())
                    for cais_HTTP_VALUE in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(cyrchfan_VALUE_safle/'native-swing.png'),'format':'png'}}):
                        ffeil_cofnod.write((json.dumps(cais_HTTP_VALUE)+'\n').encode());ffeil_cofnod.flush()
                        while True:
                            반환값=json.loads(ffeil_cofnod.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            anfon(clicio_botwm(505,115))
            cragen('echo SWING_CLOSED_OK')
            data=(Dosbarth_llwybr/'한글창시험.class').read_bytes()
            anfon('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(data),64):anfon(data[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            anfon(b'.\n')
            anfon('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            anfon(clicio_botwm(200,255),'KOREAN SWING CLICK Enw'.encode())
            anfon(clicio_botwm(505,115))
            cragen('echo KOREAN_SWING_CLOSED_OK')
            dilysu_adrodd.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','Cymraeg ffenestr/botwm/동작알림/digwyddiad_ciw directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if data_safle.poll() is None:data_safle.terminate()
            try:data_safle.wait(timeout=5)
            except subprocess.TimeoutExpired:data_safle.kill();data_safle.wait()
            dewisydd_a916db4e.close();data_safle.stdin.close();data_safle.stdout.close();(cyrchfan_VALUE_safle/'serial.log').write_bytes(LOG_rhes);(cyrchfan_VALUE_safle/'report.json').write_text(json.dumps(dilysu_adrodd,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Gweithredu_2()
