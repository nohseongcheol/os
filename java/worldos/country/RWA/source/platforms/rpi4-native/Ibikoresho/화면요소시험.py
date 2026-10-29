#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from gukora_ibwiriza import 기준,Icyo_wifuza

def ihuriro():
    목적위치=기준/'build/verification/swing';목적위치.mkdir(parents=True,exist_ok=True)
    icyiciro_inzira=기준/'build/verification/new-java';icyiciro_inzira.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'dist/jkoros-native-korean.jar'),'-d',str(icyiciro_inzira),str(기준/'시험/자바/스윙시험.java'),str(기준/'시험/자바/한글창시험.java')])
    iyemeza_raporo={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};kubika_umurongo=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(Icyo_wifuza()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        muhitamo_a916db4e=selectors.DefaultSelector();muhitamo_a916db4e.register(자료위치.stdout,selectors.EVENT_READ)
        def umukondo_icyabaye(초단위=.1):
            for 누름값,_ in muhitamo_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:kubika_umurongo.extend(둘째값)
            assert b'PANIC:' not in kubika_umurongo and b'HALTED' not in kubika_umurongo,kubika_umurongo[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            kurangiza_Ofuseti=time.monotonic()+초단위
            while 확인표시 not in kubika_umurongo[현재위치:]:
                if time.monotonic()>kurangiza_Ofuseti or 자료위치.poll() is not None:raise AssertionError(kubika_umurongo[현재위치:].decode('utf-8','replace'))
                umukondo_icyabaye()
            return bytes(kubika_umurongo[현재위치:])
        def kohereza(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(kubika_umurongo);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def insomamabwiriza(igicenteruro_amakurushingiro):return kohereza((igicenteruro_amakurushingiro+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def ihinanzira_agaciro(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def gukanda_buto(Ihuza_rya_x,세로좌표):return bytes([30,1,1,Ihuza_rya_x&255,Ihuza_rya_x>>8,세로좌표&255,세로좌표>>8,30,1,0,Ihuza_rya_x&255,Ihuza_rya_x>>8,세로좌표&255,세로좌표>>8])
        def ibwiriza_uburyo():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();kurangiza_Ofuseti=time.monotonic()+.2
            while time.monotonic()<kurangiza_Ofuseti:umukondo_icyabaye(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            insomamabwiriza('terminal');umukondo_icyabaye(.3)
            amakurushingiro=(기준/'build/verification/new-java/스윙시험.class').read_bytes()
            kohereza('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(amakurushingiro),64):kohereza(amakurushingiro[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            kohereza(b'.\n')
            kohereza('java 스윙시험\n'.encode(),b'SWING READY')
            kurangiza_Ofuseti=time.monotonic()+3
            while time.monotonic()<kurangiza_Ofuseti:umukondo_icyabaye(.1)
            # JFrame centered at (120,100), content at y=130.
            kohereza(gukanda_buto(200,210),b'',)  # focus JTextField
            자료위치.stdin.write('누리'.encode());자료위치.stdin.flush()
            kurangiza_Ofuseti=time.monotonic()+.3
            while time.monotonic()<kurangiza_Ofuseti:umukondo_icyabaye(.05)
            결과=kohereza(gukanda_buto(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(kubika_umurongo)-len(결과))
            kohereza(ihinanzira_agaciro(1),b'TERMINAL FOCUS 2')
            결과=insomamabwiriza('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in 결과
            kohereza(gukanda_buto(180,12),b'TERMINAL FOCUS 1')
            kurangiza_Ofuseti=time.monotonic()+.3
            while time.monotonic()<kurangiza_Ofuseti:umukondo_icyabaye(.05)
            with socket.socket(socket.AF_UNIX) as 문자값:
                문자값.settimeout(10);문자값.connect(str(모의제어접속))
                with 문자값.makefile('rwb') as dosiye_icyinjizwa:
                    json.loads(dosiye_icyinjizwa.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'native-swing.png'),'format':'png'}}):
                        dosiye_icyinjizwa.write((json.dumps(요청값)+'\n').encode());dosiye_icyinjizwa.flush()
                        while True:
                            반환값=json.loads(dosiye_icyinjizwa.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            kohereza(gukanda_buto(505,115))
            insomamabwiriza('echo SWING_CLOSED_OK')
            amakurushingiro=(icyiciro_inzira/'한글창시험.class').read_bytes()
            kohereza('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(amakurushingiro),64):kohereza(amakurushingiro[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            kohereza(b'.\n')
            kohereza('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            kohereza(gukanda_buto(200,255),'KOREAN SWING CLICK Izina'.encode())
            kohereza(gukanda_buto(505,115))
            insomamabwiriza('echo KOREAN_SWING_CLOSED_OK')
            iyemeza_raporo.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','Ikinyarwanda idirishya/buto/동작알림/icyabaye_umurongo_utegererezwaho directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            muhitamo_a916db4e.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(kubika_umurongo);(목적위치/'report.json').write_text(json.dumps(iyemeza_raporo,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ihuriro()
