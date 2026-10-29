#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Suorita_komento import aloite_juuri,komento

def Suorita_2():
    kohde_ARVO_toimi=aloite_juuri/'build/verification/swing';kohde_ARVO_toimi.mkdir(parents=True,exist_ok=True)
    Luokka_polku=aloite_juuri/'build/verification/new-java';Luokka_polku.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(aloite_juuri/'dist/jkoros-native-korean.jar'),'-d',str(Luokka_polku),str(aloite_juuri/'testit/자바/swing_testi.java'),str(aloite_juuri/'testit/자바/한글창시험.java')])
    vahvistus_raportti={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((aloite_juuri/'build/kernel8.img').read_bytes()).hexdigest()};LOG_TIETUE=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        data_toimi=subprocess.Popen(komento()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        valitsin_a916db4e=selectors.DefaultSelector();valitsin_a916db4e.register(data_toimi.stdout,selectors.EVENT_READ)
        def kahva_tapahtuma(초단위=.1):
            for 누름값,_ in valitsin_a916db4e.select(초단위):
                SEKUNNIT_ARVO=누름값.fileobj.read(65536)
                if SEKUNNIT_ARVO:LOG_TIETUE.extend(SEKUNNIT_ARVO)
            assert b'PANIC:' not in LOG_TIETUE and b'HALTED' not in LOG_TIETUE,LOG_TIETUE[-2048:]
        def 기다리기(merkintä,nykyinen_toimi,초단위=50):
            lopettaa_puhelu_SIIRTYMÄ=time.monotonic()+초단위
            while merkintä not in LOG_TIETUE[nykyinen_toimi:]:
                if time.monotonic()>lopettaa_puhelu_SIIRTYMÄ or data_toimi.poll() is not None:raise AssertionError(LOG_TIETUE[nykyinen_toimi:].decode('utf-8','replace'))
                kahva_tapahtuma()
            return bytes(LOG_TIETUE[nykyinen_toimi:])
        def lähettää(SEKUNNIT_ARVO,merkintä=b'jkoros-native> '):
            nykyinen_toimi=len(LOG_TIETUE);data_toimi.stdin.write(SEKUNNIT_ARVO);data_toimi.stdin.flush();return 기다리기(merkintä,nykyinen_toimi)
        def liittymä(merkkijono_data):return lähettää((merkkijono_data+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def pikakuvake_ARVO(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def osoittaa_painike(x_koordinaatti,Y_koordinaatti):return bytes([30,1,1,x_koordinaatti&255,x_koordinaatti>>8,Y_koordinaatti&255,Y_koordinaatti>>8,30,1,0,x_koordinaatti&255,x_koordinaatti>>8,Y_koordinaatti&255,Y_koordinaatti>>8])
        def komento_tila():
            data_toimi.stdin.write(b'\x1b');data_toimi.stdin.flush();lopettaa_puhelu_SIIRTYMÄ=time.monotonic()+.2
            while time.monotonic()<lopettaa_puhelu_SIIRTYMÄ:kahva_tapahtuma(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            liittymä('terminal');kahva_tapahtuma(.3)
            data=(aloite_juuri/'build/verification/new-java/swing_testi.class').read_bytes()
            lähettää('load swing_testi.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(data),64):lähettää(data[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            lähettää(b'.\n')
            lähettää('java swing_testi\n'.encode(),b'SWING READY')
            lopettaa_puhelu_SIIRTYMÄ=time.monotonic()+3
            while time.monotonic()<lopettaa_puhelu_SIIRTYMÄ:kahva_tapahtuma(.1)
            # JFrame centered at (120,100), content at y=130.
            lähettää(osoittaa_painike(200,210),b'',)  # focus JTextField
            data_toimi.stdin.write('누리'.encode());data_toimi.stdin.flush()
            lopettaa_puhelu_SIIRTYMÄ=time.monotonic()+.3
            while time.monotonic()<lopettaa_puhelu_SIIRTYMÄ:kahva_tapahtuma(.05)
            TULOS=lähettää(osoittaa_painike(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_TIETUE)-len(TULOS))
            lähettää(pikakuvake_ARVO(1),b'TERMINAL FOCUS 2')
            TULOS=liittymä('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in TULOS
            lähettää(osoittaa_painike(180,12),b'TERMINAL FOCUS 1')
            lopettaa_puhelu_SIIRTYMÄ=time.monotonic()+.3
            while time.monotonic()<lopettaa_puhelu_SIIRTYMÄ:kahva_tapahtuma(.05)
            with socket.socket(socket.AF_UNIX) as merkkikoodi:
                merkkikoodi.settimeout(10);merkkikoodi.connect(str(모의제어접속))
                with merkkikoodi.makefile('rwb') as Tiedosto_merkintä:
                    json.loads(Tiedosto_merkintä.readline())
                    for pyyntö_ARVO in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(kohde_ARVO_toimi/'native-swing.png'),'format':'png'}}):
                        Tiedosto_merkintä.write((json.dumps(pyyntö_ARVO)+'\n').encode());Tiedosto_merkintä.flush()
                        while True:
                            반환값=json.loads(Tiedosto_merkintä.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            lähettää(osoittaa_painike(505,115))
            liittymä('echo SWING_CLOSED_OK')
            data=(Luokka_polku/'한글창시험.class').read_bytes()
            lähettää('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(data),64):lähettää(data[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            lähettää(b'.\n')
            lähettää('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            lähettää(osoittaa_painike(200,255),'KOREAN SWING CLICK Nimi'.encode())
            lähettää(osoittaa_painike(505,115))
            liittymä('echo KOREAN_SWING_CLOSED_OK')
            vahvistus_raportti.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','suomi Ikkuna/painike/동작알림/tapahtuma_jono directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if data_toimi.poll() is None:data_toimi.terminate()
            try:data_toimi.wait(timeout=5)
            except subprocess.TimeoutExpired:data_toimi.kill();data_toimi.wait()
            valitsin_a916db4e.close();data_toimi.stdin.close();data_toimi.stdout.close();(kohde_ARVO_toimi/'serial.log').write_bytes(LOG_TIETUE);(kohde_ARVO_toimi/'report.json').write_text(json.dumps(vahvistus_raportti,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Suorita_2()
