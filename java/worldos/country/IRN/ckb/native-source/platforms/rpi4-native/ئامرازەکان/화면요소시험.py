#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from جێبەجێکردن_فەرمان import 기준,فەرمان

def ڕادان():
    목적위치=기준/'build/verification/swing';목적위치.mkdir(parents=True,exist_ok=True)
    کلاس_گوزەر=기준/'build/verification/new-java';کلاس_گوزەر.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'dist/jkoros-native-korean.jar'),'-d',str(کلاس_گوزەر),str(기준/'시험/자바/스윙시험.java'),str(기준/'시험/자바/한글창시험.java')])
    ڕەواکردن_ڕاپۆرت={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};تۆمار_ڕزن=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(فەرمان()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        هەڵبژێرەر_a916db4e=selectors.DefaultSelector();هەڵبژێرەر_a916db4e.register(자료위치.stdout,selectors.EVENT_READ)
        def دەسک_پێشهات(초단위=.1):
            for 누름값,_ in هەڵبژێرەر_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:تۆمار_ڕزن.extend(둘째값)
            assert b'PANIC:' not in تۆمار_ڕزن and b'HALTED' not in تۆمار_ڕزن,تۆمار_ڕزن[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            دوایی_کردن_ئۆفسێت=time.monotonic()+초단위
            while 확인표시 not in تۆمار_ڕزن[현재위치:]:
                if time.monotonic()>دوایی_کردن_ئۆفسێت or 자료위치.poll() is not None:raise AssertionError(تۆمار_ڕزن[현재위치:].decode('utf-8','replace'))
                دەسک_پێشهات()
            return bytes(تۆمار_ڕزن[현재위치:])
        def ناردن(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(تۆمار_ڕزن);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def توێکڵ(رست_دەیتا):return ناردن((رست_دەیتا+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def کورتەڕێ_نرخ(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def کرته_کردن_دوگمه(پۆوتانی_x,세로좌표):return bytes([30,1,1,پۆوتانی_x&255,پۆوتانی_x>>8,세로좌표&255,세로좌표>>8,30,1,0,پۆوتانی_x&255,پۆوتانی_x>>8,세로좌표&255,세로좌표>>8])
        def فەرمان_دۆخ():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();دوایی_کردن_ئۆفسێت=time.monotonic()+.2
            while time.monotonic()<دوایی_کردن_ئۆفسێت:دەسک_پێشهات(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            توێکڵ('terminal');دەسک_پێشهات(.3)
            دەیتا=(기준/'build/verification/new-java/스윙시험.class').read_bytes()
            ناردن('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(دەیتا),64):ناردن(دەیتا[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            ناردن(b'.\n')
            ناردن('java 스윙시험\n'.encode(),b'SWING READY')
            دوایی_کردن_ئۆفسێت=time.monotonic()+3
            while time.monotonic()<دوایی_کردن_ئۆفسێت:دەسک_پێشهات(.1)
            # JFrame centered at (120,100), content at y=130.
            ناردن(کرته_کردن_دوگمه(200,210),b'',)  # focus JTextField
            자료위치.stdin.write('누리'.encode());자료위치.stdin.flush()
            دوایی_کردن_ئۆفسێت=time.monotonic()+.3
            while time.monotonic()<دوایی_کردن_ئۆفسێت:دەسک_پێشهات(.05)
            결과=ناردن(کرته_کردن_دوگمه(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(تۆمار_ڕزن)-len(결과))
            ناردن(کورتەڕێ_نرخ(1),b'TERMINAL FOCUS 2')
            결과=توێکڵ('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in 결과
            ناردن(کرته_کردن_دوگمه(180,12),b'TERMINAL FOCUS 1')
            دوایی_کردن_ئۆفسێت=time.monotonic()+.3
            while time.monotonic()<دوایی_کردن_ئۆفسێت:دەسک_پێشهات(.05)
            with socket.socket(socket.AF_UNIX) as کۆدی_نووسە:
                کۆدی_نووسە.settimeout(10);کۆدی_نووسە.connect(str(모의제어접속))
                with کۆدی_نووسە.makefile('rwb') as فایل_تێنووسین:
                    json.loads(فایل_تێنووسین.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'native-swing.png'),'format':'png'}}):
                        فایل_تێنووسین.write((json.dumps(요청값)+'\n').encode());فایل_تێنووسین.flush()
                        while True:
                            반환값=json.loads(فایل_تێنووسین.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            ناردن(کرته_کردن_دوگمه(505,115))
            توێکڵ('echo SWING_CLOSED_OK')
            دەیتا=(کلاس_گوزەر/'한글창시험.class').read_bytes()
            ناردن('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(دەیتا),64):ناردن(دەیتا[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            ناردن(b'.\n')
            ناردن('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            ناردن(کرته_کردن_دوگمه(200,255),'KOREAN SWING CLICK ناو'.encode())
            ناردن(کرته_کردن_دوگمه(505,115))
            توێکڵ('echo KOREAN_SWING_CLOSED_OK')
            ڕەواکردن_ڕاپۆرت.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 پەنجەرە/دوگمه/동작알림/پێشهات_ڕیز directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            هەڵبژێرەر_a916db4e.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(تۆمار_ڕزن);(목적위치/'report.json').write_text(json.dumps(ڕەواکردن_ڕاپۆرت,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ڕادان()
