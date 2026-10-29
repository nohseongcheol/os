#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Udfør_kommando import To_do_rod,Kommando

def Kør_2():
    destination_VÆRDI_placere=To_do_rod/'build/verification/windows';destination_VÆRDI_placere.mkdir(parents=True,exist_ok=True)
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
            Shell('mkdir first; cd first; export NAME=one')
            maile('vi 첫째.py\n'.encode(),b'NORMAL')
            maile('i값 = 21\nprint(VÆRDI * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            afslutte_et_opkald_FORSKYDNING=time.monotonic()+3
            while time.monotonic()<afslutte_et_opkald_FORSKYDNING:handle_hændelse(.1)
            maile(alias_VÆRDI(1),b'TERMINAL FOCUS 2');handle_hændelse(.2)
            assert b'/\r\n' in Shell('pwd')
            Shell('export NAME=two')
            maile('vi 둘째.txt\n'.encode(),b'NORMAL')
            maile('i두 번째 Vindue\n'.encode(),b'INSERT')
            maile(klik_knap(180,12),b'TERMINAL FOCUS 1');handle_hændelse(.2)
            kommando_HYPPIGST();maile(b':wq\r')
            assert b'one:/first' in Shell('echo "$NAME:$PWD"')
            assert 'VÆRDI = 21\r\nprint(VÆRDI * 2)'.encode() in Shell('cat 첫째.py')
            KR=Shell('python 첫째.py');assert b'42\r\n' in KR,KR
            # Close the first shell with its actual title-bar X; second editor resumes.
            maile(klik_knap(560,63),b'TERMINAL FOCUS 2');handle_hændelse(.2)
            kommando_HYPPIGST();maile(b':wq\r')
            assert b'two:/' in Shell('echo "$NAME:$PWD"')
            assert '두 번째 Vindue'.encode() in Shell('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            maile('vi 둘째.txt\n'.encode(),b'NORMAL');maile(b'xu',b'NORMAL')
            maile(b'iX',b'INSERT');kommando_HYPPIGST();maile(b':q\r',b'Unsaved')
            maile(b':q!\r');assert '두 번째 Vindue'.encode() in Shell('cat 둘째.txt')
            maile(alias_VÆRDI(1),b'TERMINAL FOCUS 1');handle_hændelse(.2)
            maile(alias_VÆRDI(1),b'TERMINAL FOCUS 3');handle_hændelse(.2)
            maile(alias_VÆRDI(1),b'TERMINAL FOCUS 4');handle_hændelse(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            data_placere.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));data_placere.stdin.flush()
            Shell('echo DRAGGED_OK')
            maile('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            maile('i저장하지 않은 data'.encode(),b'INSERT')
            maile(klik_knap(578,97),b'TERMINAL FOCUS 3');handle_hændelse(.2)
            assert '버릴문서.txt'.encode() not in Shell('ls')
            maile(alias_VÆRDI(1),b'TERMINAL FOCUS 4');handle_hændelse(.2)
            Shell('echo REUSED_WINDOW_OK')
            fuldført_sum=LOG_post.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',fuldført_sum)
            # UART completion precedes the next QEMU display refresh.
            afslutte_et_opkald_FORSKYDNING=time.monotonic()+.3
            while time.monotonic()<afslutte_et_opkald_FORSKYDNING:handle_hændelse(.05)
            with socket.socket(socket.AF_UNIX) as tegnkode:
                tegnkode.settimeout(10);tegnkode.connect(str(모의제어접속))
                with tegnkode.makefile('rwb') as fil_post:
                    json.loads(fil_post.readline())
                    for anmodning_VÆRDI in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(destination_VÆRDI_placere/'four-terminals.png'),'format':'png'}}):
                        fil_post.write((json.dumps(anmodning_VÆRDI)+'\n').encode());fil_post.flush()
                        while True:
                            반환값=json.loads(fil_post.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(destination_VÆRDI_placere/'four-terminals.png')).convert('RGB')
            for koordinatpar,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(koordinatpar)==색상,(koordinatpar,화소들.getpixel(koordinatpar))
            Shell('echo FOUR_WINDOWS_OK')
            validering_rapport.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if data_placere.poll() is None:data_placere.terminate()
            try:data_placere.wait(timeout=5)
            except subprocess.TimeoutExpired:data_placere.kill();data_placere.wait()
            selektor_a916db4e.close();data_placere.stdin.close();data_placere.stdout.close();(destination_VÆRDI_placere/'serial.log').write_bytes(LOG_post);(destination_VÆRDI_placere/'report.json').write_text(json.dumps(validering_rapport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Kør_2()
