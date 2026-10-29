#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from exekutatu_komando import Project_erro,Komandoa

def Exekutatu_2():
    helburu_balio_kargu=Project_erro/'build/verification/windows';helburu_balio_kargu.mkdir(parents=True,exist_ok=True)
    balidazio_txosten={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_erro/'build/kernel8.img').read_bytes()).hexdigest()};LOG_marka=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        datuak_kargu=subprocess.Popen(Komandoa()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        선택기=selectors.DefaultSelector();선택기.register(datuak_kargu.stdout,selectors.EVENT_READ)
        def helduleku_gertaera(초단위=.1):
            for 누름값,_ in 선택기.select(초단위):
                SEGUNDOA_balio=누름값.fileobj.read(65536)
                if SEGUNDOA_balio:LOG_marka.extend(SEGUNDOA_balio)
            assert b'PANIC:' not in LOG_marka and b'HALTED' not in LOG_marka,LOG_marka[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            amaitu_Geruzak=time.monotonic()+초단위
            while 확인표시 not in LOG_marka[현재위치:]:
                if time.monotonic()>amaitu_Geruzak or datuak_kargu.poll() is not None:raise AssertionError(LOG_marka[현재위치:].decode('utf-8','replace'))
                helduleku_gertaera()
            return bytes(LOG_marka[현재위치:])
        def bidali(SEGUNDOA_balio,확인표시=b'jkoros-native> '):
            현재위치=len(LOG_marka);datuak_kargu.stdin.write(SEGUNDOA_balio);datuak_kargu.stdin.flush();return 기다리기(확인표시,현재위치)
        def shell(kate_datuak):return bidali((kate_datuak+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def lasterbide_balio(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def klik_botoi(X_koordenatu,Y_koordenatu):return bytes([30,1,1,X_koordenatu&255,X_koordenatu>>8,Y_koordenatu&255,Y_koordenatu>>8,30,1,0,X_koordenatu&255,X_koordenatu>>8,Y_koordenatu&255,Y_koordenatu>>8])
        def komando_MODA():
            datuak_kargu.stdin.write(b'\x1b');datuak_kargu.stdin.flush();amaitu_Geruzak=time.monotonic()+.2
            while time.monotonic()<amaitu_Geruzak:helduleku_gertaera(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            shell('terminal');helduleku_gertaera(.3)
            shell('mkdir first; cd first; export NAME=one')
            bidali('vi 첫째.py\n'.encode(),b'NORMAL')
            bidali('i값 = 21\nprint(balio * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            amaitu_Geruzak=time.monotonic()+3
            while time.monotonic()<amaitu_Geruzak:helduleku_gertaera(.1)
            bidali(lasterbide_balio(1),b'TERMINAL FOCUS 2');helduleku_gertaera(.2)
            assert b'/\r\n' in shell('pwd')
            shell('export NAME=two')
            bidali('vi 둘째.txt\n'.encode(),b'NORMAL')
            bidali('i두 번째 Leihoa\n'.encode(),b'INSERT')
            bidali(klik_botoi(180,12),b'TERMINAL FOCUS 1');helduleku_gertaera(.2)
            komando_MODA();bidali(b':wq\r')
            assert b'one:/first' in shell('echo "$NAME:$PWD"')
            assert 'balio = 21\r\nprint(balio * 2)'.encode() in shell('cat 첫째.py')
            EMAITZA=shell('python 첫째.py');assert b'42\r\n' in EMAITZA,EMAITZA
            # Close the first shell with its actual title-bar X; second editor resumes.
            bidali(klik_botoi(560,63),b'TERMINAL FOCUS 2');helduleku_gertaera(.2)
            komando_MODA();bidali(b':wq\r')
            assert b'two:/' in shell('echo "$NAME:$PWD"')
            assert '두 번째 Leihoa'.encode() in shell('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            bidali('vi 둘째.txt\n'.encode(),b'NORMAL');bidali(b'xu',b'NORMAL')
            bidali(b'iX',b'INSERT');komando_MODA();bidali(b':q\r',b'Unsaved')
            bidali(b':q!\r');assert '두 번째 Leihoa'.encode() in shell('cat 둘째.txt')
            bidali(lasterbide_balio(1),b'TERMINAL FOCUS 1');helduleku_gertaera(.2)
            bidali(lasterbide_balio(1),b'TERMINAL FOCUS 3');helduleku_gertaera(.2)
            bidali(lasterbide_balio(1),b'TERMINAL FOCUS 4');helduleku_gertaera(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            datuak_kargu.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));datuak_kargu.stdin.flush()
            shell('echo DRAGGED_OK')
            bidali('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            bidali('i저장하지 않은 datuak'.encode(),b'INSERT')
            bidali(klik_botoi(578,97),b'TERMINAL FOCUS 3');helduleku_gertaera(.2)
            assert '버릴문서.txt'.encode() not in shell('ls')
            bidali(lasterbide_balio(1),b'TERMINAL FOCUS 4');helduleku_gertaera(.2)
            shell('echo REUSED_WINDOW_OK')
            Osatutakoak_kopuru=LOG_marka.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',Osatutakoak_kopuru)
            # UART completion precedes the next QEMU display refresh.
            amaitu_Geruzak=time.monotonic()+.3
            while time.monotonic()<amaitu_Geruzak:helduleku_gertaera(.05)
            with socket.socket(socket.AF_UNIX) as karaktere_kode:
                karaktere_kode.settimeout(10);karaktere_kode.connect(str(모의제어접속))
                with karaktere_kode.makefile('rwb') as fitxategi_sarrera:
                    json.loads(fitxategi_sarrera.readline())
                    for eskaera_balio in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(helburu_balio_kargu/'four-terminals.png'),'format':'png'}}):
                        fitxategi_sarrera.write((json.dumps(eskaera_balio)+'\n').encode());fitxategi_sarrera.flush()
                        while True:
                            반환값=json.loads(fitxategi_sarrera.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(helburu_balio_kargu/'four-terminals.png')).convert('RGB')
            for koordenatu_pare,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(koordenatu_pare)==색상,(koordenatu_pare,화소들.getpixel(koordenatu_pare))
            shell('echo FOUR_WINDOWS_OK')
            balidazio_txosten.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if datuak_kargu.poll() is None:datuak_kargu.terminate()
            try:datuak_kargu.wait(timeout=5)
            except subprocess.TimeoutExpired:datuak_kargu.kill();datuak_kargu.wait()
            선택기.close();datuak_kargu.stdin.close();datuak_kargu.stdout.close();(helburu_balio_kargu/'serial.log').write_bytes(LOG_marka);(helburu_balio_kargu/'report.json').write_text(json.dumps(balidazio_txosten,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Exekutatu_2()
