#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from köra_kommando import åtgärd_rot,kommando

def Kör():
    mål_värde_placera=åtgärd_rot/'build/verification/windows';mål_värde_placera.mkdir(parents=True,exist_ok=True)
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
            Shell('mkdir first; cd first; export NAME=one')
            skicka('vi 첫째.py\n'.encode(),b'NORMAL')
            skicka('i값 = 21\nprint(värde * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            avsluta_FÖRSKJUTNING=time.monotonic()+3
            while time.monotonic()<avsluta_FÖRSKJUTNING:handtag_händelse(.1)
            skicka(alias_värde(1),b'TERMINAL FOCUS 2');handtag_händelse(.2)
            assert b'/\r\n' in Shell('pwd')
            Shell('export NAME=two')
            skicka('vi 둘째.txt\n'.encode(),b'NORMAL')
            skicka('i두 번째 Fönster\n'.encode(),b'INSERT')
            skicka(klick_knapp(180,12),b'TERMINAL FOCUS 1');handtag_händelse(.2)
            kommando_läge();skicka(b':wq\r')
            assert b'one:/first' in Shell('echo "$NAME:$PWD"')
            assert 'värde = 21\r\nprint(värde * 2)'.encode() in Shell('cat 첫째.py')
            RESULTAT=Shell('python 첫째.py');assert b'42\r\n' in RESULTAT,RESULTAT
            # Close the first shell with its actual title-bar X; second editor resumes.
            skicka(klick_knapp(560,63),b'TERMINAL FOCUS 2');handtag_händelse(.2)
            kommando_läge();skicka(b':wq\r')
            assert b'two:/' in Shell('echo "$NAME:$PWD"')
            assert '두 번째 Fönster'.encode() in Shell('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            skicka('vi 둘째.txt\n'.encode(),b'NORMAL');skicka(b'xu',b'NORMAL')
            skicka(b'iX',b'INSERT');kommando_läge();skicka(b':q\r',b'Unsaved')
            skicka(b':q!\r');assert '두 번째 Fönster'.encode() in Shell('cat 둘째.txt')
            skicka(alias_värde(1),b'TERMINAL FOCUS 1');handtag_händelse(.2)
            skicka(alias_värde(1),b'TERMINAL FOCUS 3');handtag_händelse(.2)
            skicka(alias_värde(1),b'TERMINAL FOCUS 4');handtag_händelse(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            data_placera.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));data_placera.stdin.flush()
            Shell('echo DRAGGED_OK')
            skicka('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            skicka('i저장하지 않은 data'.encode(),b'INSERT')
            skicka(klick_knapp(578,97),b'TERMINAL FOCUS 3');handtag_händelse(.2)
            assert '버릴문서.txt'.encode() not in Shell('ls')
            skicka(alias_värde(1),b'TERMINAL FOCUS 4');handtag_händelse(.2)
            Shell('echo REUSED_WINDOW_OK')
            Slutfört_belopp=LOG_POST.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',Slutfört_belopp)
            # UART completion precedes the next QEMU display refresh.
            avsluta_FÖRSKJUTNING=time.monotonic()+.3
            while time.monotonic()<avsluta_FÖRSKJUTNING:handtag_händelse(.05)
            with socket.socket(socket.AF_UNIX) as kodpunkt:
                kodpunkt.settimeout(10);kodpunkt.connect(str(모의제어접속))
                with kodpunkt.makefile('rwb') as fil_post:
                    json.loads(fil_post.readline())
                    for begäran_värde in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(mål_värde_placera/'four-terminals.png'),'format':'png'}}):
                        fil_post.write((json.dumps(begäran_värde)+'\n').encode());fil_post.flush()
                        while True:
                            반환값=json.loads(fil_post.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(mål_värde_placera/'four-terminals.png')).convert('RGB')
            for koordinatpar,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(koordinatpar)==색상,(koordinatpar,화소들.getpixel(koordinatpar))
            Shell('echo FOUR_WINDOWS_OK')
            validering_Rapport.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if data_placera.poll() is None:data_placera.terminate()
            try:data_placera.wait(timeout=5)
            except subprocess.TimeoutExpired:data_placera.kill();data_placera.wait()
            väljare_a916db4e.close();data_placera.stdin.close();data_placera.stdout.close();(mål_värde_placera/'serial.log').write_bytes(LOG_POST);(mål_värde_placera/'report.json').write_text(json.dumps(validering_Rapport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Kör()
