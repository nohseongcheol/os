#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from gudanar_Umarni import 기준,Umarni

def Tafiyar_da():
    목적위치=기준/'build/verification/swing';목적위치.mkdir(parents=True,exist_ok=True)
    Aji_Hanyar_shiga=기준/'build/verification/new-java';Aji_Hanyar_shiga.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'dist/jkoros-native-korean.jar'),'-d',str(Aji_Hanyar_shiga),str(기준/'시험/자바/스윙시험.java'),str(기준/'시험/자바/한글창시험.java')])
    amincewa_Rahoto={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};logu_naɗa=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(Umarni()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        mai_zabe_a916db4e=selectors.DefaultSelector();mai_zabe_a916db4e.register(자료위치.stdout,selectors.EVENT_READ)
        def Mariki_Faruwa(초단위=.1):
            for 누름값,_ in mai_zabe_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:logu_naɗa.extend(둘째값)
            assert b'PANIC:' not in logu_naɗa and b'HALTED' not in logu_naɗa,logu_naɗa[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            Ƙarshe_Sassautawa=time.monotonic()+초단위
            while 확인표시 not in logu_naɗa[현재위치:]:
                if time.monotonic()>Ƙarshe_Sassautawa or 자료위치.poll() is not None:raise AssertionError(logu_naɗa[현재위치:].decode('utf-8','replace'))
                Mariki_Faruwa()
            return bytes(logu_naɗa[현재위치:])
        def Aika(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(logu_naɗa);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def Mai_fayyace_umani(Zare_Tarin_bayani):return Aika((Zare_Tarin_bayani+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def Hada_lambobi_Daraja(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def Danna_maɓali(gamayyar_x,Maɓallin_Y_Mai_tsarawa):return bytes([30,1,1,gamayyar_x&255,gamayyar_x>>8,Maɓallin_Y_Mai_tsarawa&255,Maɓallin_Y_Mai_tsarawa>>8,30,1,0,gamayyar_x&255,gamayyar_x>>8,Maɓallin_Y_Mai_tsarawa&255,Maɓallin_Y_Mai_tsarawa>>8])
        def Umarni_yanayin_aiki():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();Ƙarshe_Sassautawa=time.monotonic()+.2
            while time.monotonic()<Ƙarshe_Sassautawa:Mariki_Faruwa(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            Mai_fayyace_umani('terminal');Mariki_Faruwa(.3)
            Tarin_bayani=(기준/'build/verification/new-java/스윙시험.class').read_bytes()
            Aika('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(Tarin_bayani),64):Aika(Tarin_bayani[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            Aika(b'.\n')
            Aika('java 스윙시험\n'.encode(),b'SWING READY')
            Ƙarshe_Sassautawa=time.monotonic()+3
            while time.monotonic()<Ƙarshe_Sassautawa:Mariki_Faruwa(.1)
            # JFrame centered at (120,100), content at y=130.
            Aika(Danna_maɓali(200,210),b'',)  # focus JTextField
            자료위치.stdin.write('누리'.encode());자료위치.stdin.flush()
            Ƙarshe_Sassautawa=time.monotonic()+.3
            while time.monotonic()<Ƙarshe_Sassautawa:Mariki_Faruwa(.05)
            결과=Aika(Danna_maɓali(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(logu_naɗa)-len(결과))
            Aika(Hada_lambobi_Daraja(1),b'TERMINAL FOCUS 2')
            결과=Mai_fayyace_umani('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in 결과
            Aika(Danna_maɓali(180,12),b'TERMINAL FOCUS 1')
            Ƙarshe_Sassautawa=time.monotonic()+.3
            while time.monotonic()<Ƙarshe_Sassautawa:Mariki_Faruwa(.05)
            with socket.socket(socket.AF_UNIX) as Lambar_sirrin_harafi:
                Lambar_sirrin_harafi.settimeout(10);Lambar_sirrin_harafi.connect(str(모의제어접속))
                with Lambar_sirrin_harafi.makefile('rwb') as Fayil_Mashigar_bayanai:
                    json.loads(Fayil_Mashigar_bayanai.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'native-swing.png'),'format':'png'}}):
                        Fayil_Mashigar_bayanai.write((json.dumps(요청값)+'\n').encode());Fayil_Mashigar_bayanai.flush()
                        while True:
                            반환값=json.loads(Fayil_Mashigar_bayanai.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            Aika(Danna_maɓali(505,115))
            Mai_fayyace_umani('echo SWING_CLOSED_OK')
            Tarin_bayani=(Aji_Hanyar_shiga/'한글창시험.class').read_bytes()
            Aika('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(Tarin_bayani),64):Aika(Tarin_bayani[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            Aika(b'.\n')
            Aika('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            Aika(Danna_maɓali(200,255),'KOREAN SWING CLICK Suna'.encode())
            Aika(Danna_maɓali(505,115))
            Mai_fayyace_umani('echo KOREAN_SWING_CLOSED_OK')
            amincewa_Rahoto.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 taga/maɓali/동작알림/Faruwa_Jerin_ayyukan_da_za_a_yi directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            mai_zabe_a916db4e.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(logu_naɗa);(목적위치/'report.json').write_text(json.dumps(amincewa_Rahoto,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Tafiyar_da()
