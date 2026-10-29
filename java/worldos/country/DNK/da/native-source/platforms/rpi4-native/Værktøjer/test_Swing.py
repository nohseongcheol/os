#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Udfør_kommando import To_do_rod,Kommando

def Kør_2():
    destination_VÆRDI_placere=To_do_rod/'build/verification/swing';destination_VÆRDI_placere.mkdir(parents=True,exist_ok=True)
    Hold_sti=To_do_rod/'build/verification/new-java';Hold_sti.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(To_do_rod/'dist/jkoros-native-korean.jar'),'-d',str(Hold_sti),str(To_do_rod/'시험/자바/Swing_test.java'),str(To_do_rod/'시험/자바/한글창시험.java')])
    validering_rapport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((To_do_rod/'build/kernel8.img').read_bytes()).hexdigest()};LOG_post=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        data_placere=subprocess.Popen(Kommando()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        selektor_a916db4e=selectors.DefaultSelector();selektor_a916db4e.register(data_placere.stdout,selectors.EVENT_READ)
        def handle_hændelse(초단위=.1):
            for 누름값,_ in selektor_a916db4e.select(초단위):
                SEKUND_VÆRDI=누름값.fileobj.read(65536)
                if SEKUND_VÆRDI:LOG_post.extend(SEKUND_VÆRDI)
            assert b'PANIC:' not in LOG_post and b'HALTED' not in LOG_post,LOG_post[-2048:]
        def 기다리기(mærke,aktuel_placere,초단위=50):
            afslutte_et_opkald_FORSKYDNING=time.monotonic()+초단위
            while mærke not in LOG_post[aktuel_placere:]:
                if time.monotonic()>afslutte_et_opkald_FORSKYDNING or data_placere.poll() is not None:raise AssertionError(LOG_post[aktuel_placere:].decode('utf-8','replace'))
                handle_hændelse()
            return bytes(LOG_post[aktuel_placere:])
        def maile(SEKUND_VÆRDI,mærke=b'jkoros-native> '):
            aktuel_placere=len(LOG_post);data_placere.stdin.write(SEKUND_VÆRDI);data_placere.stdin.flush();return 기다리기(mærke,aktuel_placere)
        def Shell(streng_data):return maile((streng_data+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def alias_VÆRDI(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def klik_knap(X_koordinat,Y_koordinat):return bytes([30,1,1,X_koordinat&255,X_koordinat>>8,Y_koordinat&255,Y_koordinat>>8,30,1,0,X_koordinat&255,X_koordinat>>8,Y_koordinat&255,Y_koordinat>>8])
        def kommando_HYPPIGST():
            data_placere.stdin.write(b'\x1b');data_placere.stdin.flush();afslutte_et_opkald_FORSKYDNING=time.monotonic()+.2
            while time.monotonic()<afslutte_et_opkald_FORSKYDNING:handle_hændelse(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            Shell('terminal');handle_hændelse(.3)
            data=(To_do_rod/'build/verification/new-java/Swing_test.class').read_bytes()
            maile('load Swing_test.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(data),64):maile(data[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            maile(b'.\n')
            maile('java Swing_test\n'.encode(),b'SWING READY')
            afslutte_et_opkald_FORSKYDNING=time.monotonic()+3
            while time.monotonic()<afslutte_et_opkald_FORSKYDNING:handle_hændelse(.1)
            # JFrame centered at (120,100), content at y=130.
            maile(klik_knap(200,210),b'',)  # focus JTextField
            data_placere.stdin.write('누리'.encode());data_placere.stdin.flush()
            afslutte_et_opkald_FORSKYDNING=time.monotonic()+.3
            while time.monotonic()<afslutte_et_opkald_FORSKYDNING:handle_hændelse(.05)
            KR=maile(klik_knap(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_post)-len(KR))
            maile(alias_VÆRDI(1),b'TERMINAL FOCUS 2')
            KR=Shell('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in KR
            maile(klik_knap(180,12),b'TERMINAL FOCUS 1')
            afslutte_et_opkald_FORSKYDNING=time.monotonic()+.3
            while time.monotonic()<afslutte_et_opkald_FORSKYDNING:handle_hændelse(.05)
            with socket.socket(socket.AF_UNIX) as tegnkode:
                tegnkode.settimeout(10);tegnkode.connect(str(모의제어접속))
                with tegnkode.makefile('rwb') as fil_post:
                    json.loads(fil_post.readline())
                    for anmodning_VÆRDI in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(destination_VÆRDI_placere/'native-swing.png'),'format':'png'}}):
                        fil_post.write((json.dumps(anmodning_VÆRDI)+'\n').encode());fil_post.flush()
                        while True:
                            반환값=json.loads(fil_post.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            maile(klik_knap(505,115))
            Shell('echo SWING_CLOSED_OK')
            data=(Hold_sti/'한글창시험.class').read_bytes()
            maile('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(data),64):maile(data[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            maile(b'.\n')
            maile('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            maile(klik_knap(200,255),'KOREAN SWING CLICK Navn'.encode())
            maile(klik_knap(505,115))
            Shell('echo KOREAN_SWING_CLOSED_OK')
            validering_rapport.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','Dansk Vindue/knap/동작알림/hændelse_kø directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if data_placere.poll() is None:data_placere.terminate()
            try:data_placere.wait(timeout=5)
            except subprocess.TimeoutExpired:data_placere.kill();data_placere.wait()
            selektor_a916db4e.close();data_placere.stdin.close();data_placere.stdout.close();(destination_VÆRDI_placere/'serial.log').write_bytes(LOG_post);(destination_VÆRDI_placere/'report.json').write_text(json.dumps(validering_rapport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Kør_2()
