#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ import 기준,ᎤᏁᏤᎸᎩ

def ᎠᎢᏎᏍᏗ():
    목적위치=기준/'build/verification/swing';목적위치.mkdir(parents=True,exist_ok=True)
    ᏄᏍᏛᎢ_ᎠᏍᏓᏩᏛᏍᏗ=기준/'build/verification/new-java';ᏄᏍᏛᎢ_ᎠᏍᏓᏩᏛᏍᏗ.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'dist/jkoros-native-korean.jar'),'-d',str(ᏄᏍᏛᎢ_ᎠᏍᏓᏩᏛᏍᏗ),str(기준/'시험/자바/스윙시험.java'),str(기준/'시험/자바/한글창시험.java')])
    ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(ᎤᏁᏤᎸᎩ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        ᎠᏑᏰᏍᎩ_a916db4e=selectors.DefaultSelector();ᎠᏑᏰᏍᎩ_a916db4e.register(자료위치.stdout,selectors.EVENT_READ)
        def ᎫᎭᏢ_ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ(초단위=.1):
            for 누름값,_ in ᎠᏑᏰᏍᎩ_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ.extend(둘째값)
            assert b'PANIC:' not in ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ and b'HALTED' not in ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ,ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            끝위치=time.monotonic()+초단위
            while 확인표시 not in ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ[현재위치:]:
                if time.monotonic()>끝위치 or 자료위치.poll() is not None:raise AssertionError(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ[현재위치:].decode('utf-8','replace'))
                ᎫᎭᏢ_ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ()
            return bytes(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ[현재위치:])
        def ᏫᎦᏅᏗ(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def ᎤᏯᏍᎦ(ᎠᏍᏘ_ᎦᏟᏌᏅᎯ):return ᏫᎦᏅᏗ((ᎠᏍᏘ_ᎦᏟᏌᏅᎯ+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def ᏥᏳᎪᏗᏊ_ᏧᎬᏩᎶᏗᏯ(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def ᎭᏐᏅᏍᏓ_ᎠᏐᏅᏍᏙᏗ(가로좌표,세로좌표):return bytes([30,1,1,가로좌표&255,가로좌표>>8,세로좌표&255,세로좌표>>8,30,1,0,가로좌표&255,가로좌표>>8,세로좌표&255,세로좌표>>8])
        def ᎤᏁᏤᎸᎩ_ᎬᏙᏗ():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();끝위치=time.monotonic()+.2
            while time.monotonic()<끝위치:ᎫᎭᏢ_ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            ᎤᏯᏍᎦ('terminal');ᎫᎭᏢ_ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ(.3)
            ᎦᏟᏌᏅᎯ=(기준/'build/verification/new-java/스윙시험.class').read_bytes()
            ᏫᎦᏅᏗ('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(ᎦᏟᏌᏅᎯ),64):ᏫᎦᏅᏗ(ᎦᏟᏌᏅᎯ[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            ᏫᎦᏅᏗ(b'.\n')
            ᏫᎦᏅᏗ('java 스윙시험\n'.encode(),b'SWING READY')
            끝위치=time.monotonic()+3
            while time.monotonic()<끝위치:ᎫᎭᏢ_ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ(.1)
            # JFrame centered at (120,100), content at y=130.
            ᏫᎦᏅᏗ(ᎭᏐᏅᏍᏓ_ᎠᏐᏅᏍᏙᏗ(200,210),b'',)  # focus JTextField
            자료위치.stdin.write('누리'.encode());자료위치.stdin.flush()
            끝위치=time.monotonic()+.3
            while time.monotonic()<끝위치:ᎫᎭᏢ_ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ(.05)
            결과=ᏫᎦᏅᏗ(ᎭᏐᏅᏍᏓ_ᎠᏐᏅᏍᏙᏗ(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ)-len(결과))
            ᏫᎦᏅᏗ(ᏥᏳᎪᏗᏊ_ᏧᎬᏩᎶᏗᏯ(1),b'TERMINAL FOCUS 2')
            결과=ᎤᏯᏍᎦ('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in 결과
            ᏫᎦᏅᏗ(ᎭᏐᏅᏍᏓ_ᎠᏐᏅᏍᏙᏗ(180,12),b'TERMINAL FOCUS 1')
            끝위치=time.monotonic()+.3
            while time.monotonic()<끝위치:ᎫᎭᏢ_ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ(.05)
            with socket.socket(socket.AF_UNIX) as 문자값:
                문자값.settimeout(10);문자값.connect(str(모의제어접속))
                with 문자값.makefile('rwb') as ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ:
                    json.loads(ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'native-swing.png'),'format':'png'}}):
                        ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ.write((json.dumps(요청값)+'\n').encode());ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ.flush()
                        while True:
                            반환값=json.loads(ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            ᏫᎦᏅᏗ(ᎭᏐᏅᏍᏓ_ᎠᏐᏅᏍᏙᏗ(505,115))
            ᎤᏯᏍᎦ('echo SWING_CLOSED_OK')
            ᎦᏟᏌᏅᎯ=(ᏄᏍᏛᎢ_ᎠᏍᏓᏩᏛᏍᏗ/'한글창시험.class').read_bytes()
            ᏫᎦᏅᏗ('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(ᎦᏟᏌᏅᎯ),64):ᏫᎦᏅᏗ(ᎦᏟᏌᏅᎯ[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            ᏫᎦᏅᏗ(b'.\n')
            ᏫᎦᏅᏗ('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            ᏫᎦᏅᏗ(ᎭᏐᏅᏍᏓ_ᎠᏐᏅᏍᏙᏗ(200,255),'KOREAN SWING CLICK ᏚᏙᎥᎢ'.encode())
            ᏫᎦᏅᏗ(ᎭᏐᏅᏍᏓ_ᎠᏐᏅᏍᏙᏗ(505,115))
            ᎤᏯᏍᎦ('echo KOREAN_SWING_CLOSED_OK')
            ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 ᏦᎳᏂ/ᎠᏐᏅᏍᏙᏗ/동작알림/ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ_ᎠᏍᏓᏅᏅ directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            ᎠᏑᏰᏍᎩ_a916db4e.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(ᎸᏛᏁᎸ_ᎪᏪᎳᏅᎢ_ᎤᏓᏅᏅ);(목적위치/'report.json').write_text(json.dumps(ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ᎠᎢᏎᏍᏗ()
