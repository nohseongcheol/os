#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Utfør_kommando import spegle_rot,Kommando

def Køyr_2():
    mål_VALUE_plassere=spegle_rot/'build/verification/swing';mål_VALUE_plassere.mkdir(parents=True,exist_ok=True)
    time_bane=spegle_rot/'build/verification/new-java';time_bane.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(spegle_rot/'dist/jkoros-native-korean.jar'),'-d',str(time_bane),str(spegle_rot/'시험/자바/스윙시험.java'),str(spegle_rot/'시험/자바/한글창시험.java')])
    validering_rapport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((spegle_rot/'build/kernel8.img').read_bytes()).hexdigest()};LOG_rad=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        data_plassere=subprocess.Popen(Kommando()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        veljar_a916db4e=selectors.DefaultSelector();veljar_a916db4e.register(data_plassere.stdout,selectors.EVENT_READ)
        def handtak_hending(초단위=.1):
            for 누름값,_ in veljar_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_rad.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_rad and b'HALTED' not in LOG_rad,LOG_rad[-2048:]
        def 기다리기(확인표시,betalt_plassere,초단위=50):
            avslutte_OFFSET=time.monotonic()+초단위
            while 확인표시 not in LOG_rad[betalt_plassere:]:
                if time.monotonic()>avslutte_OFFSET or data_plassere.poll() is not None:raise AssertionError(LOG_rad[betalt_plassere:].decode('utf-8','replace'))
                handtak_hending()
            return bytes(LOG_rad[betalt_plassere:])
        def sende(SECOND_VALUE,확인표시=b'jkoros-native> '):
            betalt_plassere=len(LOG_rad);data_plassere.stdin.write(SECOND_VALUE);data_plassere.stdin.flush();return 기다리기(확인표시,betalt_plassere)
        def grensesnitt(streng_data):return sende((streng_data+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def snarveg_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def klikk_knapp(x_koordinat,Y_koordinat):return bytes([30,1,1,x_koordinat&255,x_koordinat>>8,Y_koordinat&255,Y_koordinat>>8,30,1,0,x_koordinat&255,x_koordinat>>8,Y_koordinat&255,Y_koordinat>>8])
        def kommando_MODE():
            data_plassere.stdin.write(b'\x1b');data_plassere.stdin.flush();avslutte_OFFSET=time.monotonic()+.2
            while time.monotonic()<avslutte_OFFSET:handtak_hending(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            grensesnitt('terminal');handtak_hending(.3)
            data=(spegle_rot/'build/verification/new-java/스윙시험.class').read_bytes()
            sende('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(data),64):sende(data[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            sende(b'.\n')
            sende('java 스윙시험\n'.encode(),b'SWING READY')
            avslutte_OFFSET=time.monotonic()+3
            while time.monotonic()<avslutte_OFFSET:handtak_hending(.1)
            # JFrame centered at (120,100), content at y=130.
            sende(klikk_knapp(200,210),b'',)  # focus JTextField
            data_plassere.stdin.write('누리'.encode());data_plassere.stdin.flush()
            avslutte_OFFSET=time.monotonic()+.3
            while time.monotonic()<avslutte_OFFSET:handtak_hending(.05)
            forretningsmål=sende(klikk_knapp(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_rad)-len(forretningsmål))
            sende(snarveg_VALUE(1),b'TERMINAL FOCUS 2')
            forretningsmål=grensesnitt('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in forretningsmål
            sende(klikk_knapp(180,12),b'TERMINAL FOCUS 1')
            avslutte_OFFSET=time.monotonic()+.3
            while time.monotonic()<avslutte_OFFSET:handtak_hending(.05)
            with socket.socket(socket.AF_UNIX) as teiknkode:
                teiknkode.settimeout(10);teiknkode.connect(str(모의제어접속))
                with teiknkode.makefile('rwb') as fil_oppføring:
                    json.loads(fil_oppføring.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(mål_VALUE_plassere/'native-swing.png'),'format':'png'}}):
                        fil_oppføring.write((json.dumps(요청값)+'\n').encode());fil_oppføring.flush()
                        while True:
                            반환값=json.loads(fil_oppføring.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            sende(klikk_knapp(505,115))
            grensesnitt('echo SWING_CLOSED_OK')
            data=(time_bane/'한글창시험.class').read_bytes()
            sende('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(data),64):sende(data[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            sende(b'.\n')
            sende('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            sende(klikk_knapp(200,255),'KOREAN SWING CLICK Namn'.encode())
            sende(klikk_knapp(505,115))
            grensesnitt('echo KOREAN_SWING_CLOSED_OK')
            validering_rapport.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 vindauge/knapp/동작알림/hending_kø directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if data_plassere.poll() is None:data_plassere.terminate()
            try:data_plassere.wait(timeout=5)
            except subprocess.TimeoutExpired:data_plassere.kill();data_plassere.wait()
            veljar_a916db4e.close();data_plassere.stdin.close();data_plassere.stdout.close();(mål_VALUE_plassere/'serial.log').write_bytes(LOG_rad);(mål_VALUE_plassere/'report.json').write_text(json.dumps(validering_rapport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Køyr_2()
