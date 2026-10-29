#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from gnìomhaich_àithne import tilg_freumh,àithne

def ruith():
    ceann_uidhe_VALUE_suidhich=tilg_freumh/'build/verification/swing';ceann_uidhe_VALUE_suidhich.mkdir(parents=True,exist_ok=True)
    clas_slighe=tilg_freumh/'build/verification/new-java';clas_slighe.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(tilg_freumh/'dist/jkoros-native-korean.jar'),'-d',str(clas_slighe),str(tilg_freumh/'시험/자바/스윙시험.java'),str(tilg_freumh/'시험/자바/한글창시험.java')])
    dearbhadh_aithisg={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((tilg_freumh/'build/kernel8.img').read_bytes()).hexdigest()};LOG_ràgh=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        dàta_suidhich=subprocess.Popen(àithne()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        roghnaichear_a916db4e=selectors.DefaultSelector();roghnaichear_a916db4e.register(dàta_suidhich.stdout,selectors.EVENT_READ)
        def làmhrachan_tachartas(초단위=.1):
            for 누름값,_ in roghnaichear_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_ràgh.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_ràgh and b'HALTED' not in LOG_ràgh,LOG_ràgh[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            crìochnaich_OFFSET=time.monotonic()+초단위
            while 확인표시 not in LOG_ràgh[현재위치:]:
                if time.monotonic()>crìochnaich_OFFSET or dàta_suidhich.poll() is not None:raise AssertionError(LOG_ràgh[현재위치:].decode('utf-8','replace'))
                làmhrachan_tachartas()
            return bytes(LOG_ràgh[현재위치:])
        def cuir(SECOND_VALUE,확인표시=b'jkoros-native> '):
            현재위치=len(LOG_ràgh);dàta_suidhich.stdin.write(SECOND_VALUE);dàta_suidhich.stdin.flush();return 기다리기(확인표시,현재위치)
        def slige(sreang_dàta):return cuir((sreang_dàta+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def ath_ghoirid_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def briog_putan(co_chomharra_x,세로좌표):return bytes([30,1,1,co_chomharra_x&255,co_chomharra_x>>8,세로좌표&255,세로좌표>>8,30,1,0,co_chomharra_x&255,co_chomharra_x>>8,세로좌표&255,세로좌표>>8])
        def àithne_MODE():
            dàta_suidhich.stdin.write(b'\x1b');dàta_suidhich.stdin.flush();crìochnaich_OFFSET=time.monotonic()+.2
            while time.monotonic()<crìochnaich_OFFSET:làmhrachan_tachartas(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            slige('terminal');làmhrachan_tachartas(.3)
            dàta=(tilg_freumh/'build/verification/new-java/스윙시험.class').read_bytes()
            cuir('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(dàta),64):cuir(dàta[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            cuir(b'.\n')
            cuir('java 스윙시험\n'.encode(),b'SWING READY')
            crìochnaich_OFFSET=time.monotonic()+3
            while time.monotonic()<crìochnaich_OFFSET:làmhrachan_tachartas(.1)
            # JFrame centered at (120,100), content at y=130.
            cuir(briog_putan(200,210),b'',)  # focus JTextField
            dàta_suidhich.stdin.write('누리'.encode());dàta_suidhich.stdin.flush()
            crìochnaich_OFFSET=time.monotonic()+.3
            while time.monotonic()<crìochnaich_OFFSET:làmhrachan_tachartas(.05)
            tomhas=cuir(briog_putan(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_ràgh)-len(tomhas))
            cuir(ath_ghoirid_VALUE(1),b'TERMINAL FOCUS 2')
            tomhas=slige('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in tomhas
            cuir(briog_putan(180,12),b'TERMINAL FOCUS 1')
            crìochnaich_OFFSET=time.monotonic()+.3
            while time.monotonic()<crìochnaich_OFFSET:làmhrachan_tachartas(.05)
            with socket.socket(socket.AF_UNIX) as còd_a_charactair:
                còd_a_charactair.settimeout(10);còd_a_charactair.connect(str(모의제어접속))
                with còd_a_charactair.makefile('rwb') as faidhle_cur_a_steach:
                    json.loads(faidhle_cur_a_steach.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(ceann_uidhe_VALUE_suidhich/'native-swing.png'),'format':'png'}}):
                        faidhle_cur_a_steach.write((json.dumps(요청값)+'\n').encode());faidhle_cur_a_steach.flush()
                        while True:
                            반환값=json.loads(faidhle_cur_a_steach.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            cuir(briog_putan(505,115))
            slige('echo SWING_CLOSED_OK')
            dàta=(clas_slighe/'한글창시험.class').read_bytes()
            cuir('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(dàta),64):cuir(dàta[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            cuir(b'.\n')
            cuir('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            cuir(briog_putan(200,255),'KOREAN SWING CLICK Ainm'.encode())
            cuir(briog_putan(505,115))
            slige('echo KOREAN_SWING_CLOSED_OK')
            dearbhadh_aithisg.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 uinneag/putan/동작알림/tachartas_ciutha directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if dàta_suidhich.poll() is None:dàta_suidhich.terminate()
            try:dàta_suidhich.wait(timeout=5)
            except subprocess.TimeoutExpired:dàta_suidhich.kill();dàta_suidhich.wait()
            roghnaichear_a916db4e.close();dàta_suidhich.stdin.close();dàta_suidhich.stdout.close();(ceann_uidhe_VALUE_suidhich/'serial.log').write_bytes(LOG_ràgh);(ceann_uidhe_VALUE_suidhich/'report.json').write_text(json.dumps(dearbhadh_aithisg,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ruith()
