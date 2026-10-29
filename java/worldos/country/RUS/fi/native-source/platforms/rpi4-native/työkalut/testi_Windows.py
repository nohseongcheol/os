#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Suorita_komento import aloite_juuri,komento

def Suorita_2():
    kohde_ARVO_toimi=aloite_juuri/'build/verification/windows';kohde_ARVO_toimi.mkdir(parents=True,exist_ok=True)
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
            liittymä('mkdir first; cd first; export NAME=one')
            lähettää('vi 첫째.py\n'.encode(),b'NORMAL')
            lähettää('i값 = 21\nprint(ARVO * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            lopettaa_puhelu_SIIRTYMÄ=time.monotonic()+3
            while time.monotonic()<lopettaa_puhelu_SIIRTYMÄ:kahva_tapahtuma(.1)
            lähettää(pikakuvake_ARVO(1),b'TERMINAL FOCUS 2');kahva_tapahtuma(.2)
            assert b'/\r\n' in liittymä('pwd')
            liittymä('export NAME=two')
            lähettää('vi 둘째.txt\n'.encode(),b'NORMAL')
            lähettää('i두 번째 Ikkuna\n'.encode(),b'INSERT')
            lähettää(osoittaa_painike(180,12),b'TERMINAL FOCUS 1');kahva_tapahtuma(.2)
            komento_tila();lähettää(b':wq\r')
            assert b'one:/first' in liittymä('echo "$NAME:$PWD"')
            assert 'ARVO = 21\r\nprint(ARVO * 2)'.encode() in liittymä('cat 첫째.py')
            TULOS=liittymä('python 첫째.py');assert b'42\r\n' in TULOS,TULOS
            # Close the first shell with its actual title-bar X; second editor resumes.
            lähettää(osoittaa_painike(560,63),b'TERMINAL FOCUS 2');kahva_tapahtuma(.2)
            komento_tila();lähettää(b':wq\r')
            assert b'two:/' in liittymä('echo "$NAME:$PWD"')
            assert '두 번째 Ikkuna'.encode() in liittymä('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            lähettää('vi 둘째.txt\n'.encode(),b'NORMAL');lähettää(b'xu',b'NORMAL')
            lähettää(b'iX',b'INSERT');komento_tila();lähettää(b':q\r',b'Unsaved')
            lähettää(b':q!\r');assert '두 번째 Ikkuna'.encode() in liittymä('cat 둘째.txt')
            lähettää(pikakuvake_ARVO(1),b'TERMINAL FOCUS 1');kahva_tapahtuma(.2)
            lähettää(pikakuvake_ARVO(1),b'TERMINAL FOCUS 3');kahva_tapahtuma(.2)
            lähettää(pikakuvake_ARVO(1),b'TERMINAL FOCUS 4');kahva_tapahtuma(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            data_toimi.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));data_toimi.stdin.flush()
            liittymä('echo DRAGGED_OK')
            lähettää('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            lähettää('i저장하지 않은 data'.encode(),b'INSERT')
            lähettää(osoittaa_painike(578,97),b'TERMINAL FOCUS 3');kahva_tapahtuma(.2)
            assert '버릴문서.txt'.encode() not in liittymä('ls')
            lähettää(pikakuvake_ARVO(1),b'TERMINAL FOCUS 4');kahva_tapahtuma(.2)
            liittymä('echo REUSED_WINDOW_OK')
            valmis_määrä=LOG_TIETUE.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',valmis_määrä)
            # UART completion precedes the next QEMU display refresh.
            lopettaa_puhelu_SIIRTYMÄ=time.monotonic()+.3
            while time.monotonic()<lopettaa_puhelu_SIIRTYMÄ:kahva_tapahtuma(.05)
            with socket.socket(socket.AF_UNIX) as merkkikoodi:
                merkkikoodi.settimeout(10);merkkikoodi.connect(str(모의제어접속))
                with merkkikoodi.makefile('rwb') as Tiedosto_merkintä:
                    json.loads(Tiedosto_merkintä.readline())
                    for pyyntö_ARVO in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(kohde_ARVO_toimi/'four-terminals.png'),'format':'png'}}):
                        Tiedosto_merkintä.write((json.dumps(pyyntö_ARVO)+'\n').encode());Tiedosto_merkintä.flush()
                        while True:
                            반환값=json.loads(Tiedosto_merkintä.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(kohde_ARVO_toimi/'four-terminals.png')).convert('RGB')
            for koordinaattipari,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(koordinaattipari)==색상,(koordinaattipari,화소들.getpixel(koordinaattipari))
            liittymä('echo FOUR_WINDOWS_OK')
            vahvistus_raportti.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if data_toimi.poll() is None:data_toimi.terminate()
            try:data_toimi.wait(timeout=5)
            except subprocess.TimeoutExpired:data_toimi.kill();data_toimi.wait()
            valitsin_a916db4e.close();data_toimi.stdin.close();data_toimi.stdout.close();(kohde_ARVO_toimi/'serial.log').write_bytes(LOG_TIETUE);(kohde_ARVO_toimi/'report.json').write_text(json.dumps(vahvistus_raportti,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Suorita_2()
