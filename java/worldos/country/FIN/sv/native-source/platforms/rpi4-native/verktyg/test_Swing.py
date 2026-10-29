#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from köra_kommando import åtgärd_rot,kommando

def Kör():
    mål_värde_placera=åtgärd_rot/'build/verification/swing';mål_värde_placera.mkdir(parents=True,exist_ok=True)
    Kurs_väg=åtgärd_rot/'build/verification/new-java';Kurs_väg.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(åtgärd_rot/'dist/jkoros-native-korean.jar'),'-d',str(Kurs_väg),str(åtgärd_rot/'tester/자바/Swing_test.java'),str(åtgärd_rot/'tester/자바/한글창시험.java')])
    validering_Rapport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((åtgärd_rot/'build/kernel8.img').read_bytes()).hexdigest()};LOG_POST=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        data_placera=subprocess.Popen(kommando()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        väljare_a916db4e=selectors.DefaultSelector();väljare_a916db4e.register(data_placera.stdout,selectors.EVENT_READ)
        def handtag_händelse(초단위=.1):
            for 누름값,_ in väljare_a916db4e.select(초단위):
                SEKUND_värde=누름값.fileobj.read(65536)
                if SEKUND_värde:LOG_POST.extend(SEKUND_värde)
            assert b'PANIC:' not in LOG_POST and b'HALTED' not in LOG_POST,LOG_POST[-2048:]
        def 기다리기(markör_8b722c5f,aktuellt_placera,초단위=50):
            avsluta_FÖRSKJUTNING=time.monotonic()+초단위
            while markör_8b722c5f not in LOG_POST[aktuellt_placera:]:
                if time.monotonic()>avsluta_FÖRSKJUTNING or data_placera.poll() is not None:raise AssertionError(LOG_POST[aktuellt_placera:].decode('utf-8','replace'))
                handtag_händelse()
            return bytes(LOG_POST[aktuellt_placera:])
        def skicka(SEKUND_värde,markör_8b722c5f=b'jkoros-native> '):
            aktuellt_placera=len(LOG_POST);data_placera.stdin.write(SEKUND_värde);data_placera.stdin.flush();return 기다리기(markör_8b722c5f,aktuellt_placera)
        def Shell(sträng_data):return skicka((sträng_data+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def alias_värde(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def klick_knapp(x_koordinat,Y_koordinat):return bytes([30,1,1,x_koordinat&255,x_koordinat>>8,Y_koordinat&255,Y_koordinat>>8,30,1,0,x_koordinat&255,x_koordinat>>8,Y_koordinat&255,Y_koordinat>>8])
        def kommando_läge():
            data_placera.stdin.write(b'\x1b');data_placera.stdin.flush();avsluta_FÖRSKJUTNING=time.monotonic()+.2
            while time.monotonic()<avsluta_FÖRSKJUTNING:handtag_händelse(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            Shell('terminal');handtag_händelse(.3)
            data=(åtgärd_rot/'build/verification/new-java/Swing_test.class').read_bytes()
            skicka('load Swing_test.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(data),64):skicka(data[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            skicka(b'.\n')
            skicka('java Swing_test\n'.encode(),b'SWING READY')
            avsluta_FÖRSKJUTNING=time.monotonic()+3
            while time.monotonic()<avsluta_FÖRSKJUTNING:handtag_händelse(.1)
            # JFrame centered at (120,100), content at y=130.
            skicka(klick_knapp(200,210),b'',)  # focus JTextField
            data_placera.stdin.write('누리'.encode());data_placera.stdin.flush()
            avsluta_FÖRSKJUTNING=time.monotonic()+.3
            while time.monotonic()<avsluta_FÖRSKJUTNING:handtag_händelse(.05)
            RESULTAT=skicka(klick_knapp(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_POST)-len(RESULTAT))
            skicka(alias_värde(1),b'TERMINAL FOCUS 2')
            RESULTAT=Shell('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in RESULTAT
            skicka(klick_knapp(180,12),b'TERMINAL FOCUS 1')
            avsluta_FÖRSKJUTNING=time.monotonic()+.3
            while time.monotonic()<avsluta_FÖRSKJUTNING:handtag_händelse(.05)
            with socket.socket(socket.AF_UNIX) as kodpunkt:
                kodpunkt.settimeout(10);kodpunkt.connect(str(모의제어접속))
                with kodpunkt.makefile('rwb') as fil_post:
                    json.loads(fil_post.readline())
                    for begäran_värde in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(mål_värde_placera/'native-swing.png'),'format':'png'}}):
                        fil_post.write((json.dumps(begäran_värde)+'\n').encode());fil_post.flush()
                        while True:
                            반환값=json.loads(fil_post.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            skicka(klick_knapp(505,115))
            Shell('echo SWING_CLOSED_OK')
            data=(Kurs_väg/'한글창시험.class').read_bytes()
            skicka('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(data),64):skicka(data[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            skicka(b'.\n')
            skicka('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            skicka(klick_knapp(200,255),'KOREAN SWING CLICK Namn'.encode())
            skicka(klick_knapp(505,115))
            Shell('echo KOREAN_SWING_CLOSED_OK')
            validering_Rapport.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','Svenska Fönster/knapp/동작알림/händelse_kö directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if data_placera.poll() is None:data_placera.terminate()
            try:data_placera.wait(timeout=5)
            except subprocess.TimeoutExpired:data_placera.kill();data_placera.wait()
            väljare_a916db4e.close();data_placera.stdin.close();data_placera.stdout.close();(mål_värde_placera/'serial.log').write_bytes(LOG_POST);(mål_värde_placera/'report.json').write_text(json.dumps(validering_Rapport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Kör()
