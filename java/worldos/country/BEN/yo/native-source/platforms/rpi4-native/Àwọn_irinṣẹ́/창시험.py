#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from ṣiṣẹ́_àṣẹ import 기준,Àṣẹ

def Rọ́ọ̀nù():
    목적위치=기준/'build/verification/windows';목적위치.mkdir(parents=True,exist_ok=True)
    Àfọwọ́sí_ìjábọ̀={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};àkọsílẹ̀_ìṣe_ìlà_ìbú=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(Àṣẹ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        olùyàn_a916db4e=selectors.DefaultSelector();olùyàn_a916db4e.register(자료위치.stdout,selectors.EVENT_READ)
        def èkù_ìgbéṣẹ̀(초단위=.1):
            for 누름값,_ in olùyàn_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:àkọsílẹ̀_ìṣe_ìlà_ìbú.extend(둘째값)
            assert b'PANIC:' not in àkọsílẹ̀_ìṣe_ìlà_ìbú and b'HALTED' not in àkọsílẹ̀_ìṣe_ìlà_ìbú,àkọsílẹ̀_ìṣe_ìlà_ìbú[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            parí_Ìtayọ=time.monotonic()+초단위
            while 확인표시 not in àkọsílẹ̀_ìṣe_ìlà_ìbú[현재위치:]:
                if time.monotonic()>parí_Ìtayọ or 자료위치.poll() is not None:raise AssertionError(àkọsílẹ̀_ìṣe_ìlà_ìbú[현재위치:].decode('utf-8','replace'))
                èkù_ìgbéṣẹ̀()
            return bytes(àkọsílẹ̀_ìṣe_ìlà_ìbú[현재위치:])
        def í_meèlì(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(àkọsílẹ̀_ìṣe_ìlà_ìbú);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def ṣẹ́ẹ̀lì(fọ́nrán_détà):return í_meèlì((fọ́nrán_détà+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def àbùjá_iye(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def ṣíra_tẹ_bọ́tìnnì(ibi_ìtọ́kasí_x,세로좌표):return bytes([30,1,1,ibi_ìtọ́kasí_x&255,ibi_ìtọ́kasí_x>>8,세로좌표&255,세로좌표>>8,30,1,0,ibi_ìtọ́kasí_x&255,ibi_ìtọ́kasí_x>>8,세로좌표&255,세로좌표>>8])
        def àṣẹ_móòdù():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();parí_Ìtayọ=time.monotonic()+.2
            while time.monotonic()<parí_Ìtayọ:èkù_ìgbéṣẹ̀(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            ṣẹ́ẹ̀lì('terminal');èkù_ìgbéṣẹ̀(.3)
            ṣẹ́ẹ̀lì('mkdir first; cd first; export NAME=one')
            í_meèlì('vi 첫째.py\n'.encode(),b'NORMAL')
            í_meèlì('i값 = 21\nprint(iye * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            parí_Ìtayọ=time.monotonic()+3
            while time.monotonic()<parí_Ìtayọ:èkù_ìgbéṣẹ̀(.1)
            í_meèlì(àbùjá_iye(1),b'TERMINAL FOCUS 2');èkù_ìgbéṣẹ̀(.2)
            assert b'/\r\n' in ṣẹ́ẹ̀lì('pwd')
            ṣẹ́ẹ̀lì('export NAME=two')
            í_meèlì('vi 둘째.txt\n'.encode(),b'NORMAL')
            í_meèlì('i두 번째 wínńdò\n'.encode(),b'INSERT')
            í_meèlì(ṣíra_tẹ_bọ́tìnnì(180,12),b'TERMINAL FOCUS 1');èkù_ìgbéṣẹ̀(.2)
            àṣẹ_móòdù();í_meèlì(b':wq\r')
            assert b'one:/first' in ṣẹ́ẹ̀lì('echo "$NAME:$PWD"')
            assert 'iye = 21\r\nprint(iye * 2)'.encode() in ṣẹ́ẹ̀lì('cat 첫째.py')
            결과=ṣẹ́ẹ̀lì('python 첫째.py');assert b'42\r\n' in 결과,결과
            # Close the first shell with its actual title-bar X; second editor resumes.
            í_meèlì(ṣíra_tẹ_bọ́tìnnì(560,63),b'TERMINAL FOCUS 2');èkù_ìgbéṣẹ̀(.2)
            àṣẹ_móòdù();í_meèlì(b':wq\r')
            assert b'two:/' in ṣẹ́ẹ̀lì('echo "$NAME:$PWD"')
            assert '두 번째 wínńdò'.encode() in ṣẹ́ẹ̀lì('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            í_meèlì('vi 둘째.txt\n'.encode(),b'NORMAL');í_meèlì(b'xu',b'NORMAL')
            í_meèlì(b'iX',b'INSERT');àṣẹ_móòdù();í_meèlì(b':q\r',b'Unsaved')
            í_meèlì(b':q!\r');assert '두 번째 wínńdò'.encode() in ṣẹ́ẹ̀lì('cat 둘째.txt')
            í_meèlì(àbùjá_iye(1),b'TERMINAL FOCUS 1');èkù_ìgbéṣẹ̀(.2)
            í_meèlì(àbùjá_iye(1),b'TERMINAL FOCUS 3');èkù_ìgbéṣẹ̀(.2)
            í_meèlì(àbùjá_iye(1),b'TERMINAL FOCUS 4');èkù_ìgbéṣẹ̀(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            자료위치.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));자료위치.stdin.flush()
            ṣẹ́ẹ̀lì('echo DRAGGED_OK')
            í_meèlì('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            í_meèlì('i저장하지 않은 détà'.encode(),b'INSERT')
            í_meèlì(ṣíra_tẹ_bọ́tìnnì(578,97),b'TERMINAL FOCUS 3');èkù_ìgbéṣẹ̀(.2)
            assert '버릴문서.txt'.encode() not in ṣẹ́ẹ̀lì('ls')
            í_meèlì(àbùjá_iye(1),b'TERMINAL FOCUS 4');èkù_ìgbéṣẹ̀(.2)
            ṣẹ́ẹ̀lì('echo REUSED_WINDOW_OK')
            완료량=àkọsílẹ̀_ìṣe_ìlà_ìbú.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            parí_Ìtayọ=time.monotonic()+.3
            while time.monotonic()<parí_Ìtayọ:èkù_ìgbéṣẹ̀(.05)
            with socket.socket(socket.AF_UNIX) as kóòdù_ẹyọ_ọ̀rọ̀:
                kóòdù_ẹyọ_ọ̀rọ̀.settimeout(10);kóòdù_ẹyọ_ọ̀rọ̀.connect(str(모의제어접속))
                with kóòdù_ẹyọ_ọ̀rọ̀.makefile('rwb') as fáìlì_ìgbéwọlé:
                    json.loads(fáìlì_ìgbéwọlé.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'four-terminals.png'),'format':'png'}}):
                        fáìlì_ìgbéwọlé.write((json.dumps(요청값)+'\n').encode());fáìlì_ìgbéwọlé.flush()
                        while True:
                            반환값=json.loads(fáìlì_ìgbéwọlé.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(목적위치/'four-terminals.png')).convert('RGB')
            for ohun_aṣàpèjúwe_adálérí_ọ̀pọ̀_ẹ̀yà_abèjì,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(ohun_aṣàpèjúwe_adálérí_ọ̀pọ̀_ẹ̀yà_abèjì)==색상,(ohun_aṣàpèjúwe_adálérí_ọ̀pọ̀_ẹ̀yà_abèjì,화소들.getpixel(ohun_aṣàpèjúwe_adálérí_ọ̀pọ̀_ẹ̀yà_abèjì))
            ṣẹ́ẹ̀lì('echo FOUR_WINDOWS_OK')
            Àfọwọ́sí_ìjábọ̀.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            olùyàn_a916db4e.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(àkọsílẹ̀_ìṣe_ìlà_ìbú);(목적위치/'report.json').write_text(json.dumps(Àfọwọ́sí_ìjábọ̀,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Rọ́ọ̀nù()
