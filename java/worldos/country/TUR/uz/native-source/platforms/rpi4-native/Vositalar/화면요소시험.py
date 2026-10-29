#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from bajarmoq_buyruq import Project_ildiz,Buyruq

def Bajarish():
    ko_chirish_joyi_VALUE_holat=Project_ildiz/'build/verification/swing';ko_chirish_joyi_VALUE_holat.mkdir(parents=True,exist_ok=True)
    Sinf_yo_l=Project_ildiz/'build/verification/new-java';Sinf_yo_l.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(Project_ildiz/'dist/jkoros-native-korean.jar'),'-d',str(Sinf_yo_l),str(Project_ildiz/'시험/자바/스윙시험.java'),str(Project_ildiz/'시험/자바/한글창시험.java')])
    tasdiq_hisobot={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_ildiz/'build/kernel8.img').read_bytes()).hexdigest()};LOG_satr=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        ma_lumotlar_holat=subprocess.Popen(Buyruq()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        tanlagich_a916db4e=selectors.DefaultSelector();tanlagich_a916db4e.register(ma_lumotlar_holat.stdout,selectors.EVENT_READ)
        def deskriptor_hodisa(초단위=.1):
            for 누름값,_ in tanlagich_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_satr.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_satr and b'HALTED' not in LOG_satr,LOG_satr[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            to_xtatmoq_OFFSET=time.monotonic()+초단위
            while 확인표시 not in LOG_satr[현재위치:]:
                if time.monotonic()>to_xtatmoq_OFFSET or ma_lumotlar_holat.poll() is not None:raise AssertionError(LOG_satr[현재위치:].decode('utf-8','replace'))
                deskriptor_hodisa()
            return bytes(LOG_satr[현재위치:])
        def yuborish(SECOND_VALUE,확인표시=b'jkoros-native> '):
            현재위치=len(LOG_satr);ma_lumotlar_holat.stdin.write(SECOND_VALUE);ma_lumotlar_holat.stdin.flush();return 기다리기(확인표시,현재위치)
        def qobiq(satr_ma_lumotlar):return yuborish((satr_ma_lumotlar+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def yorliq_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def chertmoq_tugma(x_koordinata,Y_tugmasi_koordinat):return bytes([30,1,1,x_koordinata&255,x_koordinata>>8,Y_tugmasi_koordinat&255,Y_tugmasi_koordinat>>8,30,1,0,x_koordinata&255,x_koordinata>>8,Y_tugmasi_koordinat&255,Y_tugmasi_koordinat>>8])
        def buyruq_MODE():
            ma_lumotlar_holat.stdin.write(b'\x1b');ma_lumotlar_holat.stdin.flush();to_xtatmoq_OFFSET=time.monotonic()+.2
            while time.monotonic()<to_xtatmoq_OFFSET:deskriptor_hodisa(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            qobiq('terminal');deskriptor_hodisa(.3)
            ma_lumotlar=(Project_ildiz/'build/verification/new-java/스윙시험.class').read_bytes()
            yuborish('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(ma_lumotlar),64):yuborish(ma_lumotlar[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            yuborish(b'.\n')
            yuborish('java 스윙시험\n'.encode(),b'SWING READY')
            to_xtatmoq_OFFSET=time.monotonic()+3
            while time.monotonic()<to_xtatmoq_OFFSET:deskriptor_hodisa(.1)
            # JFrame centered at (120,100), content at y=130.
            yuborish(chertmoq_tugma(200,210),b'',)  # focus JTextField
            ma_lumotlar_holat.stdin.write('누리'.encode());ma_lumotlar_holat.stdin.flush()
            to_xtatmoq_OFFSET=time.monotonic()+.3
            while time.monotonic()<to_xtatmoq_OFFSET:deskriptor_hodisa(.05)
            o_lchov=yuborish(chertmoq_tugma(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_satr)-len(o_lchov))
            yuborish(yorliq_VALUE(1),b'TERMINAL FOCUS 2')
            o_lchov=qobiq('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in o_lchov
            yuborish(chertmoq_tugma(180,12),b'TERMINAL FOCUS 1')
            to_xtatmoq_OFFSET=time.monotonic()+.3
            while time.monotonic()<to_xtatmoq_OFFSET:deskriptor_hodisa(.05)
            with socket.socket(socket.AF_UNIX) as belgi_kodi:
                belgi_kodi.settimeout(10);belgi_kodi.connect(str(모의제어접속))
                with belgi_kodi.makefile('rwb') as fayl_kiritish:
                    json.loads(fayl_kiritish.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(ko_chirish_joyi_VALUE_holat/'native-swing.png'),'format':'png'}}):
                        fayl_kiritish.write((json.dumps(요청값)+'\n').encode());fayl_kiritish.flush()
                        while True:
                            반환값=json.loads(fayl_kiritish.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            yuborish(chertmoq_tugma(505,115))
            qobiq('echo SWING_CLOSED_OK')
            ma_lumotlar=(Sinf_yo_l/'한글창시험.class').read_bytes()
            yuborish('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(ma_lumotlar),64):yuborish(ma_lumotlar[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            yuborish(b'.\n')
            yuborish('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            yuborish(chertmoq_tugma(200,255),'KOREAN SWING CLICK Nomi'.encode())
            yuborish(chertmoq_tugma(505,115))
            qobiq('echo KOREAN_SWING_CLOSED_OK')
            tasdiq_hisobot.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 oyna/tugma/동작알림/hodisa_navbat directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if ma_lumotlar_holat.poll() is None:ma_lumotlar_holat.terminate()
            try:ma_lumotlar_holat.wait(timeout=5)
            except subprocess.TimeoutExpired:ma_lumotlar_holat.kill();ma_lumotlar_holat.wait()
            tanlagich_a916db4e.close();ma_lumotlar_holat.stdin.close();ma_lumotlar_holat.stdout.close();(ko_chirish_joyi_VALUE_holat/'serial.log').write_bytes(LOG_satr);(ko_chirish_joyi_VALUE_holat/'report.json').write_text(json.dumps(tasdiq_hisobot,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Bajarish()
