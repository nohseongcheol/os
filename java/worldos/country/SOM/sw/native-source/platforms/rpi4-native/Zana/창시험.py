#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from tekeleza_amri import 기준,amri

def endesha():
    목적위치=기준/'build/verification/windows';목적위치.mkdir(parents=True,exist_ok=True)
    uhakikishi_ripoti={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};batli_REKODI=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(amri()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        kiteuzi_a916db4e=selectors.DefaultSelector();kiteuzi_a916db4e.register(자료위치.stdout,selectors.EVENT_READ)
        def kishiko_tukio(초단위=.1):
            for 누름값,_ in kiteuzi_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:batli_REKODI.extend(둘째값)
            assert b'PANIC:' not in batli_REKODI and b'HALTED' not in batli_REKODI,batli_REKODI[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            tamatia_Chipua=time.monotonic()+초단위
            while 확인표시 not in batli_REKODI[현재위치:]:
                if time.monotonic()>tamatia_Chipua or 자료위치.poll() is not None:raise AssertionError(batli_REKODI[현재위치:].decode('utf-8','replace'))
                kishiko_tukio()
            return bytes(batli_REKODI[현재위치:])
        def tuma(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(batli_REKODI);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def sheli(tungo_data):return tuma((tungo_data+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def njia_ya_mkato_thamani(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def bofya_kitufe(jira_x,Kitufe_cha_Y_kiratibu):return bytes([30,1,1,jira_x&255,jira_x>>8,Kitufe_cha_Y_kiratibu&255,Kitufe_cha_Y_kiratibu>>8,30,1,0,jira_x&255,jira_x>>8,Kitufe_cha_Y_kiratibu&255,Kitufe_cha_Y_kiratibu>>8])
        def amri_hali_tumizi():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();tamatia_Chipua=time.monotonic()+.2
            while time.monotonic()<tamatia_Chipua:kishiko_tukio(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            sheli('terminal');kishiko_tukio(.3)
            sheli('mkdir first; cd first; export NAME=one')
            tuma('vi 첫째.py\n'.encode(),b'NORMAL')
            tuma('i값 = 21\nprint(thamani * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            tamatia_Chipua=time.monotonic()+3
            while time.monotonic()<tamatia_Chipua:kishiko_tukio(.1)
            tuma(njia_ya_mkato_thamani(1),b'TERMINAL FOCUS 2');kishiko_tukio(.2)
            assert b'/\r\n' in sheli('pwd')
            sheli('export NAME=two')
            tuma('vi 둘째.txt\n'.encode(),b'NORMAL')
            tuma('i두 번째 dirisha\n'.encode(),b'INSERT')
            tuma(bofya_kitufe(180,12),b'TERMINAL FOCUS 1');kishiko_tukio(.2)
            amri_hali_tumizi();tuma(b':wq\r')
            assert b'one:/first' in sheli('echo "$NAME:$PWD"')
            assert 'thamani = 21\r\nprint(thamani * 2)'.encode() in sheli('cat 첫째.py')
            결과=sheli('python 첫째.py');assert b'42\r\n' in 결과,결과
            # Close the first shell with its actual title-bar X; second editor resumes.
            tuma(bofya_kitufe(560,63),b'TERMINAL FOCUS 2');kishiko_tukio(.2)
            amri_hali_tumizi();tuma(b':wq\r')
            assert b'two:/' in sheli('echo "$NAME:$PWD"')
            assert '두 번째 dirisha'.encode() in sheli('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            tuma('vi 둘째.txt\n'.encode(),b'NORMAL');tuma(b'xu',b'NORMAL')
            tuma(b'iX',b'INSERT');amri_hali_tumizi();tuma(b':q\r',b'Unsaved')
            tuma(b':q!\r');assert '두 번째 dirisha'.encode() in sheli('cat 둘째.txt')
            tuma(njia_ya_mkato_thamani(1),b'TERMINAL FOCUS 1');kishiko_tukio(.2)
            tuma(njia_ya_mkato_thamani(1),b'TERMINAL FOCUS 3');kishiko_tukio(.2)
            tuma(njia_ya_mkato_thamani(1),b'TERMINAL FOCUS 4');kishiko_tukio(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            자료위치.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));자료위치.stdin.flush()
            sheli('echo DRAGGED_OK')
            tuma('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            tuma('i저장하지 않은 data'.encode(),b'INSERT')
            tuma(bofya_kitufe(578,97),b'TERMINAL FOCUS 3');kishiko_tukio(.2)
            assert '버릴문서.txt'.encode() not in sheli('ls')
            tuma(njia_ya_mkato_thamani(1),b'TERMINAL FOCUS 4');kishiko_tukio(.2)
            sheli('echo REUSED_WINDOW_OK')
            완료량=batli_REKODI.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            tamatia_Chipua=time.monotonic()+.3
            while time.monotonic()<tamatia_Chipua:kishiko_tukio(.05)
            with socket.socket(socket.AF_UNIX) as msimbo_wa_kibambo:
                msimbo_wa_kibambo.settimeout(10);msimbo_wa_kibambo.connect(str(모의제어접속))
                with msimbo_wa_kibambo.makefile('rwb') as faili_ingizo:
                    json.loads(faili_ingizo.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'four-terminals.png'),'format':'png'}}):
                        faili_ingizo.write((json.dumps(요청값)+'\n').encode());faili_ingizo.flush()
                        while True:
                            반환값=json.loads(faili_ingizo.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(목적위치/'four-terminals.png')).convert('RGB')
            for Jozi_ratibu,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(Jozi_ratibu)==색상,(Jozi_ratibu,화소들.getpixel(Jozi_ratibu))
            sheli('echo FOUR_WINDOWS_OK')
            uhakikishi_ripoti.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            kiteuzi_a916db4e.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(batli_REKODI);(목적위치/'report.json').write_text(json.dumps(uhakikishi_ripoti,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':endesha()
