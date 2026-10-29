#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from ṣiṣẹ́_àṣẹ import 기준,Àṣẹ

def Rọ́ọ̀nù():
    목적위치=기준/'build/verification/swing';목적위치.mkdir(parents=True,exist_ok=True)
    ọ̀wọ́_ọ̀nà=기준/'build/verification/new-java';ọ̀wọ́_ọ̀nà.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'dist/jkoros-native-korean.jar'),'-d',str(ọ̀wọ́_ọ̀nà),str(기준/'시험/자바/스윙시험.java'),str(기준/'시험/자바/한글창시험.java')])
    Àfọwọ́sí_ìjábọ̀={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};àkọsílẹ̀_ìṣe_ìlà_ìbú=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(Àṣẹ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        olùyàn_a916db4e=selectors.DefaultSelector();olùyàn_a916db4e.register(자료위치.stdout,selectors.EVENT_READ)
        def èkù_ìgbéṣẹ̀(초단위=.1):
            for 누름값,_ in olùyàn_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:àkọsílẹ̀_ìṣe_ìlà_ìbú.extend(둘째값)
            assert b'PANIC:' not in àkọsílẹ̀_ìṣe_ìlà_ìbú and b'HALTED' not in àkọsílẹ̀_ìṣe_ìlà_ìbú,àkọsílẹ̀_ìṣe_ìlà_ìbú[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            parí_Ìtayọ=time.monotonic()+초단위
            while 확인표시 not in àkọsílẹ̀_ìṣe_ìlà_ìbú[현재위치:]:
                if time.monotonic()>parí_Ìtayọ or 자료위치.poll() is not None:raise AssertionError(àkọsílẹ̀_ìṣe_ìlà_ìbú[현재위치:].decode('utf-8','replace'))
                èkù_ìgbéṣẹ̀()
            return bytes(àkọsílẹ̀_ìṣe_ìlà_ìbú[현재위치:])
        def í_meèlì(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(àkọsílẹ̀_ìṣe_ìlà_ìbú);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def ṣẹ́ẹ̀lì(fọ́nrán_détà):return í_meèlì((fọ́nrán_détà+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def àbùjá_iye(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def ṣíra_tẹ_bọ́tìnnì(ibi_ìtọ́kasí_x,세로좌표):return bytes([30,1,1,ibi_ìtọ́kasí_x&255,ibi_ìtọ́kasí_x>>8,세로좌표&255,세로좌표>>8,30,1,0,ibi_ìtọ́kasí_x&255,ibi_ìtọ́kasí_x>>8,세로좌표&255,세로좌표>>8])
        def àṣẹ_móòdù():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();parí_Ìtayọ=time.monotonic()+.2
            while time.monotonic()<parí_Ìtayọ:èkù_ìgbéṣẹ̀(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            ṣẹ́ẹ̀lì('terminal');èkù_ìgbéṣẹ̀(.3)
            détà=(기준/'build/verification/new-java/스윙시험.class').read_bytes()
            í_meèlì('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(détà),64):í_meèlì(détà[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            í_meèlì(b'.\n')
            í_meèlì('java 스윙시험\n'.encode(),b'SWING READY')
            parí_Ìtayọ=time.monotonic()+3
            while time.monotonic()<parí_Ìtayọ:èkù_ìgbéṣẹ̀(.1)
            # JFrame centered at (120,100), content at y=130.
            í_meèlì(ṣíra_tẹ_bọ́tìnnì(200,210),b'',)  # focus JTextField
            자료위치.stdin.write('누리'.encode());자료위치.stdin.flush()
            parí_Ìtayọ=time.monotonic()+.3
            while time.monotonic()<parí_Ìtayọ:èkù_ìgbéṣẹ̀(.05)
            결과=í_meèlì(ṣíra_tẹ_bọ́tìnnì(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(àkọsílẹ̀_ìṣe_ìlà_ìbú)-len(결과))
            í_meèlì(àbùjá_iye(1),b'TERMINAL FOCUS 2')
            결과=ṣẹ́ẹ̀lì('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in 결과
            í_meèlì(ṣíra_tẹ_bọ́tìnnì(180,12),b'TERMINAL FOCUS 1')
            parí_Ìtayọ=time.monotonic()+.3
            while time.monotonic()<parí_Ìtayọ:èkù_ìgbéṣẹ̀(.05)
            with socket.socket(socket.AF_UNIX) as kóòdù_ẹyọ_ọ̀rọ̀:
                kóòdù_ẹyọ_ọ̀rọ̀.settimeout(10);kóòdù_ẹyọ_ọ̀rọ̀.connect(str(모의제어접속))
                with kóòdù_ẹyọ_ọ̀rọ̀.makefile('rwb') as fáìlì_ìgbéwọlé:
                    json.loads(fáìlì_ìgbéwọlé.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'native-swing.png'),'format':'png'}}):
                        fáìlì_ìgbéwọlé.write((json.dumps(요청값)+'\n').encode());fáìlì_ìgbéwọlé.flush()
                        while True:
                            반환값=json.loads(fáìlì_ìgbéwọlé.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            í_meèlì(ṣíra_tẹ_bọ́tìnnì(505,115))
            ṣẹ́ẹ̀lì('echo SWING_CLOSED_OK')
            détà=(ọ̀wọ́_ọ̀nà/'한글창시험.class').read_bytes()
            í_meèlì('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(détà),64):í_meèlì(détà[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            í_meèlì(b'.\n')
            í_meèlì('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            í_meèlì(ṣíra_tẹ_bọ́tìnnì(200,255),'KOREAN SWING CLICK Orúkọ'.encode())
            í_meèlì(ṣíra_tẹ_bọ́tìnnì(505,115))
            ṣẹ́ẹ̀lì('echo KOREAN_SWING_CLOSED_OK')
            Àfọwọ́sí_ìjábọ̀.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 wínńdò/bọ́tìnnì/동작알림/ìgbéṣẹ̀_ìtòléra directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            olùyàn_a916db4e.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(àkọsílẹ̀_ìṣe_ìlà_ìbú);(목적위치/'report.json').write_text(json.dumps(Àfọwọ́sí_ìjábọ̀,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Rọ́ọ̀nù()
