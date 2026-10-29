#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from yenza_umyalo import 기준,Umlayelo

def Sebenzisa():
    목적위치=기준/'build/verification/swing';목적위치.mkdir(parents=True,exist_ok=True)
    uhlobo_umzila=기준/'build/verification/new-java';uhlobo_umzila.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'dist/jkoros-native-korean.jar'),'-d',str(uhlobo_umzila),str(기준/'시험/자바/스윙시험.java'),str(기준/'시험/자바/한글창시험.java')])
    ukufakazisa_umbiko={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};loga_umugqa=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(Umlayelo()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        isiqoki_a916db4e=selectors.DefaultSelector();isiqoki_a916db4e.register(자료위치.stdout,selectors.EVENT_READ)
        def isibambo_isigameko(초단위=.1):
            for 누름값,_ in isiqoki_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:loga_umugqa.extend(둘째값)
            assert b'PANIC:' not in loga_umugqa and b'HALTED' not in loga_umugqa,loga_umugqa[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            yekisa_I_ofisethi=time.monotonic()+초단위
            while 확인표시 not in loga_umugqa[현재위치:]:
                if time.monotonic()>yekisa_I_ofisethi or 자료위치.poll() is not None:raise AssertionError(loga_umugqa[현재위치:].decode('utf-8','replace'))
                isibambo_isigameko()
            return bytes(loga_umugqa[현재위치:])
        def Thumela(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(loga_umugqa);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def isihumushi_miyalelo(uchunge_imininingwane):return Thumela((uchunge_imininingwane+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def ukunqamulela_inani(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def qhafaza_inkinobho(okuxhumanisa_u_x,세로좌표):return bytes([30,1,1,okuxhumanisa_u_x&255,okuxhumanisa_u_x>>8,세로좌표&255,세로좌표>>8,30,1,0,okuxhumanisa_u_x&255,okuxhumanisa_u_x>>8,세로좌표&255,세로좌표>>8])
        def umyalo_inqubo():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();yekisa_I_ofisethi=time.monotonic()+.2
            while time.monotonic()<yekisa_I_ofisethi:isibambo_isigameko(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            isihumushi_miyalelo('terminal');isibambo_isigameko(.3)
            imininingwane=(기준/'build/verification/new-java/스윙시험.class').read_bytes()
            Thumela('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(imininingwane),64):Thumela(imininingwane[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            Thumela(b'.\n')
            Thumela('java 스윙시험\n'.encode(),b'SWING READY')
            yekisa_I_ofisethi=time.monotonic()+3
            while time.monotonic()<yekisa_I_ofisethi:isibambo_isigameko(.1)
            # JFrame centered at (120,100), content at y=130.
            Thumela(qhafaza_inkinobho(200,210),b'',)  # focus JTextField
            자료위치.stdin.write('누리'.encode());자료위치.stdin.flush()
            yekisa_I_ofisethi=time.monotonic()+.3
            while time.monotonic()<yekisa_I_ofisethi:isibambo_isigameko(.05)
            결과=Thumela(qhafaza_inkinobho(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(loga_umugqa)-len(결과))
            Thumela(ukunqamulela_inani(1),b'TERMINAL FOCUS 2')
            결과=isihumushi_miyalelo('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in 결과
            Thumela(qhafaza_inkinobho(180,12),b'TERMINAL FOCUS 1')
            yekisa_I_ofisethi=time.monotonic()+.3
            while time.monotonic()<yekisa_I_ofisethi:isibambo_isigameko(.05)
            with socket.socket(socket.AF_UNIX) as ikhodi_yohlamvu:
                ikhodi_yohlamvu.settimeout(10);ikhodi_yohlamvu.connect(str(모의제어접속))
                with ikhodi_yohlamvu.makefile('rwb') as ifayela_okufakwayo:
                    json.loads(ifayela_okufakwayo.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'native-swing.png'),'format':'png'}}):
                        ifayela_okufakwayo.write((json.dumps(요청값)+'\n').encode());ifayela_okufakwayo.flush()
                        while True:
                            반환값=json.loads(ifayela_okufakwayo.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            Thumela(qhafaza_inkinobho(505,115))
            isihumushi_miyalelo('echo SWING_CLOSED_OK')
            imininingwane=(uhlobo_umzila/'한글창시험.class').read_bytes()
            Thumela('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(imininingwane),64):Thumela(imininingwane[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            Thumela(b'.\n')
            Thumela('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            Thumela(qhafaza_inkinobho(200,255),'KOREAN SWING CLICK Igama'.encode())
            Thumela(qhafaza_inkinobho(505,115))
            isihumushi_miyalelo('echo KOREAN_SWING_CLOSED_OK')
            ukufakazisa_umbiko.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','Isi_Zulu ifasitela/inkinobho/동작알림/isigameko_ujenge directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            isiqoki_a916db4e.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(loga_umugqa);(목적위치/'report.json').write_text(json.dumps(ukufakazisa_umbiko,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Sebenzisa()
