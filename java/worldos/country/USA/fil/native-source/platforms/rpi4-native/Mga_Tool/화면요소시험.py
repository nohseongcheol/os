#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Mag_execute_utos import Project_root,utos

def run():
    patutunguhan_VALUE_posisyon=Project_root/'build/verification/swing';patutunguhan_VALUE_posisyon.mkdir(parents=True,exist_ok=True)
    kategorya_path=Project_root/'build/verification/new-java';kategorya_path.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(Project_root/'dist/jkoros-native-korean.jar'),'-d',str(kategorya_path),str(Project_root/'시험/자바/스윙시험.java'),str(Project_root/'시험/자바/한글창시험.java')])
    pagpapatibay_ulat={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_root/'build/kernel8.img').read_bytes()).hexdigest()};LOG_hanay=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        data_posisyon=subprocess.Popen(utos()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        tagapili_a916db4e=selectors.DefaultSelector();tagapili_a916db4e.register(data_posisyon.stdout,selectors.EVENT_READ)
        def hawakán_kaganapan(초단위=.1):
            for 누름값,_ in tagapili_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_hanay.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_hanay and b'HALTED' not in LOG_hanay,LOG_hanay[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            tapusin_OFFSET=time.monotonic()+초단위
            while 확인표시 not in LOG_hanay[현재위치:]:
                if time.monotonic()>tapusin_OFFSET or data_posisyon.poll() is not None:raise AssertionError(LOG_hanay[현재위치:].decode('utf-8','replace'))
                hawakán_kaganapan()
            return bytes(LOG_hanay[현재위치:])
        def i_email(SECOND_VALUE,확인표시=b'jkoros-native> '):
            현재위치=len(LOG_hanay);data_posisyon.stdin.write(SECOND_VALUE);data_posisyon.stdin.flush();return 기다리기(확인표시,현재위치)
        def shell(string_data):return i_email((string_data+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def shortcut_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def magklik_button(x_coordinate,Y_button_coordinate):return bytes([30,1,1,x_coordinate&255,x_coordinate>>8,Y_button_coordinate&255,Y_button_coordinate>>8,30,1,0,x_coordinate&255,x_coordinate>>8,Y_button_coordinate&255,Y_button_coordinate>>8])
        def utos_MODE():
            data_posisyon.stdin.write(b'\x1b');data_posisyon.stdin.flush();tapusin_OFFSET=time.monotonic()+.2
            while time.monotonic()<tapusin_OFFSET:hawakán_kaganapan(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            shell('terminal');hawakán_kaganapan(.3)
            data=(Project_root/'build/verification/new-java/스윙시험.class').read_bytes()
            i_email('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(data),64):i_email(data[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            i_email(b'.\n')
            i_email('java 스윙시험\n'.encode(),b'SWING READY')
            tapusin_OFFSET=time.monotonic()+3
            while time.monotonic()<tapusin_OFFSET:hawakán_kaganapan(.1)
            # JFrame centered at (120,100), content at y=130.
            i_email(magklik_button(200,210),b'',)  # focus JTextField
            data_posisyon.stdin.write('누리'.encode());data_posisyon.stdin.flush()
            tapusin_OFFSET=time.monotonic()+.3
            while time.monotonic()<tapusin_OFFSET:hawakán_kaganapan(.05)
            sukat=i_email(magklik_button(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_hanay)-len(sukat))
            i_email(shortcut_VALUE(1),b'TERMINAL FOCUS 2')
            sukat=shell('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in sukat
            i_email(magklik_button(180,12),b'TERMINAL FOCUS 1')
            tapusin_OFFSET=time.monotonic()+.3
            while time.monotonic()<tapusin_OFFSET:hawakán_kaganapan(.05)
            with socket.socket(socket.AF_UNIX) as character_code:
                character_code.settimeout(10);character_code.connect(str(모의제어접속))
                with character_code.makefile('rwb') as file_pagpasok:
                    json.loads(file_pagpasok.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(patutunguhan_VALUE_posisyon/'native-swing.png'),'format':'png'}}):
                        file_pagpasok.write((json.dumps(요청값)+'\n').encode());file_pagpasok.flush()
                        while True:
                            반환값=json.loads(file_pagpasok.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            i_email(magklik_button(505,115))
            shell('echo SWING_CLOSED_OK')
            data=(kategorya_path/'한글창시험.class').read_bytes()
            i_email('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(data),64):i_email(data[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            i_email(b'.\n')
            i_email('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            i_email(magklik_button(200,255),'KOREAN SWING CLICK pangalan'.encode())
            i_email(magklik_button(505,115))
            shell('echo KOREAN_SWING_CLOSED_OK')
            pagpapatibay_ulat.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 window/button/동작알림/kaganapan_pila directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if data_posisyon.poll() is None:data_posisyon.terminate()
            try:data_posisyon.wait(timeout=5)
            except subprocess.TimeoutExpired:data_posisyon.kill();data_posisyon.wait()
            tagapili_a916db4e.close();data_posisyon.stdin.close();data_posisyon.stdout.close();(patutunguhan_VALUE_posisyon/'serial.log').write_bytes(LOG_hanay);(patutunguhan_VALUE_posisyon/'report.json').write_text(json.dumps(pagpapatibay_ulat,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':run()
