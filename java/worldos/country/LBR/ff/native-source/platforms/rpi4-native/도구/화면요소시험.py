#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from 실행 import 기준,ginol

def huutoraade():
    목적위치=기준/'build/verification/swing';목적위치.mkdir(parents=True,exist_ok=True)
    fedde_laawol=기준/'build/verification/new-java';fedde_laawol.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'dist/jkoros-native-korean.jar'),'-d',str(fedde_laawol),str(기준/'시험/자바/스윙시험.java'),str(기준/'시험/자바/한글창시험.java')])
    teeŋtingol_ciimtol={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};suurnal_winndande=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(ginol()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        선택기=selectors.DefaultSelector();선택기.register(자료위치.stdout,selectors.EVENT_READ)
        def jaggoode_saɗteende(초단위=.1):
            for 누름값,_ in 선택기.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:suurnal_winndande.extend(둘째값)
            assert b'PANIC:' not in suurnal_winndande and b'HALTED' not in suurnal_winndande,suurnal_winndande[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            끝위치=time.monotonic()+초단위
            while 확인표시 not in suurnal_winndande[현재위치:]:
                if time.monotonic()>끝위치 or 자료위치.poll() is not None:raise AssertionError(suurnal_winndande[현재위치:].decode('utf-8','replace'))
                jaggoode_saɗteende()
            return bytes(suurnal_winndande[현재위치:])
        def neldude(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(suurnal_winndande);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def laalagal(ɓoggol_keɓe):return neldude((ɓoggol_keɓe+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def sodorde_njaru(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def dobaade_feɗoode(가로좌표,세로좌표):return bytes([30,1,1,가로좌표&255,가로좌표>>8,세로좌표&255,세로좌표>>8,30,1,0,가로좌표&255,가로좌표>>8,세로좌표&255,세로좌표>>8])
        def ginol_modd():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();끝위치=time.monotonic()+.2
            while time.monotonic()<끝위치:jaggoode_saɗteende(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            laalagal('terminal');jaggoode_saɗteende(.3)
            keɓe=(기준/'build/verification/new-java/스윙시험.class').read_bytes()
            neldude('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(keɓe),64):neldude(keɓe[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            neldude(b'.\n')
            neldude('java 스윙시험\n'.encode(),b'SWING READY')
            끝위치=time.monotonic()+3
            while time.monotonic()<끝위치:jaggoode_saɗteende(.1)
            # JFrame centered at (120,100), content at y=130.
            neldude(dobaade_feɗoode(200,210),b'',)  # focus JTextField
            자료위치.stdin.write('누리'.encode());자료위치.stdin.flush()
            끝위치=time.monotonic()+.3
            while time.monotonic()<끝위치:jaggoode_saɗteende(.05)
            결과=neldude(dobaade_feɗoode(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(suurnal_winndande)-len(결과))
            neldude(sodorde_njaru(1),b'TERMINAL FOCUS 2')
            결과=laalagal('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in 결과
            neldude(dobaade_feɗoode(180,12),b'TERMINAL FOCUS 1')
            끝위치=time.monotonic()+.3
            while time.monotonic()<끝위치:jaggoode_saɗteende(.05)
            with socket.socket(socket.AF_UNIX) as 문자값:
                문자값.settimeout(10);문자값.connect(str(모의제어접속))
                with 문자값.makefile('rwb') as fiilde_naatnugol:
                    json.loads(fiilde_naatnugol.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'native-swing.png'),'format':'png'}}):
                        fiilde_naatnugol.write((json.dumps(요청값)+'\n').encode());fiilde_naatnugol.flush()
                        while True:
                            반환값=json.loads(fiilde_naatnugol.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            neldude(dobaade_feɗoode(505,115))
            laalagal('echo SWING_CLOSED_OK')
            keɓe=(fedde_laawol/'한글창시험.class').read_bytes()
            neldude('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(keɓe),64):neldude(keɓe[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            neldude(b'.\n')
            neldude('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            neldude(dobaade_feɗoode(200,255),'KOREAN SWING CLICK innde'.encode())
            neldude(dobaade_feɗoode(505,115))
            laalagal('echo KOREAN_SWING_CLOSED_OK')
            teeŋtingol_ciimtol.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 falanteere/feɗoode/동작알림/saɗteende_lappol directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            선택기.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(suurnal_winndande);(목적위치/'report.json').write_text(json.dumps(teeŋtingol_ciimtol,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':huutoraade()
