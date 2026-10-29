#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from tekeleza_amri import 기준,amri

def endesha():
    목적위치=기준/'build/verification/swing';목적위치.mkdir(parents=True,exist_ok=True)
    tabaka_njia=기준/'build/verification/new-java';tabaka_njia.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'dist/jkoros-native-korean.jar'),'-d',str(tabaka_njia),str(기준/'시험/자바/스윙시험.java'),str(기준/'시험/자바/한글창시험.java')])
    uhakikishi_ripoti={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};batli_REKODI=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(amri()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        kiteuzi_a916db4e=selectors.DefaultSelector();kiteuzi_a916db4e.register(자료위치.stdout,selectors.EVENT_READ)
        def kishiko_tukio(초단위=.1):
            for 누름값,_ in kiteuzi_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:batli_REKODI.extend(둘째값)
            assert b'PANIC:' not in batli_REKODI and b'HALTED' not in batli_REKODI,batli_REKODI[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            tamatia_Chipua=time.monotonic()+초단위
            while 확인표시 not in batli_REKODI[현재위치:]:
                if time.monotonic()>tamatia_Chipua or 자료위치.poll() is not None:raise AssertionError(batli_REKODI[현재위치:].decode('utf-8','replace'))
                kishiko_tukio()
            return bytes(batli_REKODI[현재위치:])
        def tuma(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(batli_REKODI);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def sheli(tungo_data):return tuma((tungo_data+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def njia_ya_mkato_thamani(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def bofya_kitufe(jira_x,Kitufe_cha_Y_kiratibu):return bytes([30,1,1,jira_x&255,jira_x>>8,Kitufe_cha_Y_kiratibu&255,Kitufe_cha_Y_kiratibu>>8,30,1,0,jira_x&255,jira_x>>8,Kitufe_cha_Y_kiratibu&255,Kitufe_cha_Y_kiratibu>>8])
        def amri_hali_tumizi():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();tamatia_Chipua=time.monotonic()+.2
            while time.monotonic()<tamatia_Chipua:kishiko_tukio(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            sheli('terminal');kishiko_tukio(.3)
            data=(기준/'build/verification/new-java/스윙시험.class').read_bytes()
            tuma('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(data),64):tuma(data[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            tuma(b'.\n')
            tuma('java 스윙시험\n'.encode(),b'SWING READY')
            tamatia_Chipua=time.monotonic()+3
            while time.monotonic()<tamatia_Chipua:kishiko_tukio(.1)
            # JFrame centered at (120,100), content at y=130.
            tuma(bofya_kitufe(200,210),b'',)  # focus JTextField
            자료위치.stdin.write('누리'.encode());자료위치.stdin.flush()
            tamatia_Chipua=time.monotonic()+.3
            while time.monotonic()<tamatia_Chipua:kishiko_tukio(.05)
            결과=tuma(bofya_kitufe(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(batli_REKODI)-len(결과))
            tuma(njia_ya_mkato_thamani(1),b'TERMINAL FOCUS 2')
            결과=sheli('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in 결과
            tuma(bofya_kitufe(180,12),b'TERMINAL FOCUS 1')
            tamatia_Chipua=time.monotonic()+.3
            while time.monotonic()<tamatia_Chipua:kishiko_tukio(.05)
            with socket.socket(socket.AF_UNIX) as msimbo_wa_kibambo:
                msimbo_wa_kibambo.settimeout(10);msimbo_wa_kibambo.connect(str(모의제어접속))
                with msimbo_wa_kibambo.makefile('rwb') as faili_ingizo:
                    json.loads(faili_ingizo.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'native-swing.png'),'format':'png'}}):
                        faili_ingizo.write((json.dumps(요청값)+'\n').encode());faili_ingizo.flush()
                        while True:
                            반환값=json.loads(faili_ingizo.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            tuma(bofya_kitufe(505,115))
            sheli('echo SWING_CLOSED_OK')
            data=(tabaka_njia/'한글창시험.class').read_bytes()
            tuma('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(data),64):tuma(data[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            tuma(b'.\n')
            tuma('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            tuma(bofya_kitufe(200,255),'KOREAN SWING CLICK Jina'.encode())
            tuma(bofya_kitufe(505,115))
            sheli('echo KOREAN_SWING_CLOSED_OK')
            uhakikishi_ripoti.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 dirisha/kitufe/동작알림/tukio_foleni directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            kiteuzi_a916db4e.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(batli_REKODI);(목적위치/'report.json').write_text(json.dumps(uhakikishi_ripoti,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':endesha()
