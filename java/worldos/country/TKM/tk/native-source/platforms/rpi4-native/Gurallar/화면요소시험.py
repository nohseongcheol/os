#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from ýerine_ýetir_buýruk import 기준,buýruk

def Bitir():
    목적위치=기준/'build/verification/swing';목적위치.mkdir(parents=True,exist_ok=True)
    klas_ýol=기준/'build/verification/new-java';klas_ýol.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'dist/jkoros-native-korean.jar'),'-d',str(klas_ýol),str(기준/'시험/자바/스윙시험.java'),str(기준/'시험/자바/한글창시험.java')])
    barlag_hasabat={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};hasaba_alyş_setir=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(buýruk()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        saýlaýjy_a916db4e=selectors.DefaultSelector();saýlaýjy_a916db4e.register(자료위치.stdout,selectors.EVENT_READ)
        def ryçag_waka(초단위=.1):
            for 누름값,_ in saýlaýjy_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:hasaba_alyş_setir.extend(둘째값)
            assert b'PANIC:' not in hasaba_alyş_setir and b'HALTED' not in hasaba_alyş_setir,hasaba_alyş_setir[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            tamamla_Süýşüriş=time.monotonic()+초단위
            while 확인표시 not in hasaba_alyş_setir[현재위치:]:
                if time.monotonic()>tamamla_Süýşüriş or 자료위치.poll() is not None:raise AssertionError(hasaba_alyş_setir[현재위치:].decode('utf-8','replace'))
                ryçag_waka()
            return bytes(hasaba_alyş_setir[현재위치:])
        def iber(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(hasaba_alyş_setir);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def gabyjak(setir_maglumat):return iber((setir_maglumat+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def ýarlyk_baha(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def bas_düwme(x_koordinatasy,세로좌표):return bytes([30,1,1,x_koordinatasy&255,x_koordinatasy>>8,세로좌표&255,세로좌표>>8,30,1,0,x_koordinatasy&255,x_koordinatasy>>8,세로좌표&255,세로좌표>>8])
        def buýruk_reje():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();tamamla_Süýşüriş=time.monotonic()+.2
            while time.monotonic()<tamamla_Süýşüriş:ryçag_waka(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            gabyjak('terminal');ryçag_waka(.3)
            maglumat=(기준/'build/verification/new-java/스윙시험.class').read_bytes()
            iber('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(maglumat),64):iber(maglumat[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            iber(b'.\n')
            iber('java 스윙시험\n'.encode(),b'SWING READY')
            tamamla_Süýşüriş=time.monotonic()+3
            while time.monotonic()<tamamla_Süýşüriş:ryçag_waka(.1)
            # JFrame centered at (120,100), content at y=130.
            iber(bas_düwme(200,210),b'',)  # focus JTextField
            자료위치.stdin.write('누리'.encode());자료위치.stdin.flush()
            tamamla_Süýşüriş=time.monotonic()+.3
            while time.monotonic()<tamamla_Süýşüriş:ryçag_waka(.05)
            결과=iber(bas_düwme(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(hasaba_alyş_setir)-len(결과))
            iber(ýarlyk_baha(1),b'TERMINAL FOCUS 2')
            결과=gabyjak('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in 결과
            iber(bas_düwme(180,12),b'TERMINAL FOCUS 1')
            tamamla_Süýşüriş=time.monotonic()+.3
            while time.monotonic()<tamamla_Süýşüriş:ryçag_waka(.05)
            with socket.socket(socket.AF_UNIX) as nyşanyň_kody:
                nyşanyň_kody.settimeout(10);nyşanyň_kody.connect(str(모의제어접속))
                with nyşanyň_kody.makefile('rwb') as faýl_girizmeklik:
                    json.loads(faýl_girizmeklik.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'native-swing.png'),'format':'png'}}):
                        faýl_girizmeklik.write((json.dumps(요청값)+'\n').encode());faýl_girizmeklik.flush()
                        while True:
                            반환값=json.loads(faýl_girizmeklik.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            iber(bas_düwme(505,115))
            gabyjak('echo SWING_CLOSED_OK')
            maglumat=(klas_ýol/'한글창시험.class').read_bytes()
            iber('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(maglumat),64):iber(maglumat[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            iber(b'.\n')
            iber('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            iber(bas_düwme(200,255),'KOREAN SWING CLICK Ad'.encode())
            iber(bas_düwme(505,115))
            gabyjak('echo KOREAN_SWING_CLOSED_OK')
            barlag_hasabat.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 penjire/düwme/동작알림/waka_nobat directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            saýlaýjy_a916db4e.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(hasaba_alyş_setir);(목적위치/'report.json').write_text(json.dumps(barlag_hasabat,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Bitir()
