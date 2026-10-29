#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from gudanar_Umarni import 기준,Umarni

def Tafiyar_da():
    목적위치=기준/'build/verification/windows';목적위치.mkdir(parents=True,exist_ok=True)
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
            Mai_fayyace_umani('mkdir first; cd first; export NAME=one')
            Aika('vi 첫째.py\n'.encode(),b'NORMAL')
            Aika('i값 = 21\nprint(Daraja * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            Ƙarshe_Sassautawa=time.monotonic()+3
            while time.monotonic()<Ƙarshe_Sassautawa:Mariki_Faruwa(.1)
            Aika(Hada_lambobi_Daraja(1),b'TERMINAL FOCUS 2');Mariki_Faruwa(.2)
            assert b'/\r\n' in Mai_fayyace_umani('pwd')
            Mai_fayyace_umani('export NAME=two')
            Aika('vi 둘째.txt\n'.encode(),b'NORMAL')
            Aika('i두 번째 taga\n'.encode(),b'INSERT')
            Aika(Danna_maɓali(180,12),b'TERMINAL FOCUS 1');Mariki_Faruwa(.2)
            Umarni_yanayin_aiki();Aika(b':wq\r')
            assert b'one:/first' in Mai_fayyace_umani('echo "$NAME:$PWD"')
            assert 'Daraja = 21\r\nprint(Daraja * 2)'.encode() in Mai_fayyace_umani('cat 첫째.py')
            결과=Mai_fayyace_umani('python 첫째.py');assert b'42\r\n' in 결과,결과
            # Close the first shell with its actual title-bar X; second editor resumes.
            Aika(Danna_maɓali(560,63),b'TERMINAL FOCUS 2');Mariki_Faruwa(.2)
            Umarni_yanayin_aiki();Aika(b':wq\r')
            assert b'two:/' in Mai_fayyace_umani('echo "$NAME:$PWD"')
            assert '두 번째 taga'.encode() in Mai_fayyace_umani('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            Aika('vi 둘째.txt\n'.encode(),b'NORMAL');Aika(b'xu',b'NORMAL')
            Aika(b'iX',b'INSERT');Umarni_yanayin_aiki();Aika(b':q\r',b'Unsaved')
            Aika(b':q!\r');assert '두 번째 taga'.encode() in Mai_fayyace_umani('cat 둘째.txt')
            Aika(Hada_lambobi_Daraja(1),b'TERMINAL FOCUS 1');Mariki_Faruwa(.2)
            Aika(Hada_lambobi_Daraja(1),b'TERMINAL FOCUS 3');Mariki_Faruwa(.2)
            Aika(Hada_lambobi_Daraja(1),b'TERMINAL FOCUS 4');Mariki_Faruwa(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            자료위치.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));자료위치.stdin.flush()
            Mai_fayyace_umani('echo DRAGGED_OK')
            Aika('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            Aika('i저장하지 않은 Tarin_bayani'.encode(),b'INSERT')
            Aika(Danna_maɓali(578,97),b'TERMINAL FOCUS 3');Mariki_Faruwa(.2)
            assert '버릴문서.txt'.encode() not in Mai_fayyace_umani('ls')
            Aika(Hada_lambobi_Daraja(1),b'TERMINAL FOCUS 4');Mariki_Faruwa(.2)
            Mai_fayyace_umani('echo REUSED_WINDOW_OK')
            완료량=logu_naɗa.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            Ƙarshe_Sassautawa=time.monotonic()+.3
            while time.monotonic()<Ƙarshe_Sassautawa:Mariki_Faruwa(.05)
            with socket.socket(socket.AF_UNIX) as Lambar_sirrin_harafi:
                Lambar_sirrin_harafi.settimeout(10);Lambar_sirrin_harafi.connect(str(모의제어접속))
                with Lambar_sirrin_harafi.makefile('rwb') as Fayil_Mashigar_bayanai:
                    json.loads(Fayil_Mashigar_bayanai.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'four-terminals.png'),'format':'png'}}):
                        Fayil_Mashigar_bayanai.write((json.dumps(요청값)+'\n').encode());Fayil_Mashigar_bayanai.flush()
                        while True:
                            반환값=json.loads(Fayil_Mashigar_bayanai.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(목적위치/'four-terminals.png')).convert('RGB')
            for Dangantakar_tagwai,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(Dangantakar_tagwai)==색상,(Dangantakar_tagwai,화소들.getpixel(Dangantakar_tagwai))
            Mai_fayyace_umani('echo FOUR_WINDOWS_OK')
            amincewa_Rahoto.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            mai_zabe_a916db4e.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(logu_naɗa);(목적위치/'report.json').write_text(json.dumps(amincewa_Rahoto,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Tafiyar_da()
