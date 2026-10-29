#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from def_ndigel import 기준,ndigel

def daw():
    목적위치=기준/'build/verification/windows';목적위치.mkdir(parents=True,exist_ok=True)
    wéral_tënk={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};làq_Dënk=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(ndigel()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        tànnkat_a916db4e=selectors.DefaultSelector();tànnkat_a916db4e.register(자료위치.stdout,selectors.EVENT_READ)
        def yombal_xewxew(초단위=.1):
            for 누름값,_ in tànnkat_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:làq_Dënk.extend(둘째값)
            assert b'PANIC:' not in làq_Dënk and b'HALTED' not in làq_Dënk,làq_Dënk[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            jeexal_Randal=time.monotonic()+초단위
            while 확인표시 not in làq_Dënk[현재위치:]:
                if time.monotonic()>jeexal_Randal or 자료위치.poll() is not None:raise AssertionError(làq_Dënk[현재위치:].decode('utf-8','replace'))
                yombal_xewxew()
            return bytes(làq_Dënk[현재위치:])
        def Yónnee(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(làq_Dënk);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def Wëreef(araf_yu_bennoo_mbir):return Yónnee((araf_yu_bennoo_mbir+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def Teggi_xëyma(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def bës_butoñ(rëddu_iks_yi,세로좌표):return bytes([30,1,1,rëddu_iks_yi&255,rëddu_iks_yi>>8,세로좌표&255,세로좌표>>8,30,1,0,rëddu_iks_yi&255,rëddu_iks_yi>>8,세로좌표&255,세로좌표>>8])
        def ndigel_anam():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();jeexal_Randal=time.monotonic()+.2
            while time.monotonic()<jeexal_Randal:yombal_xewxew(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            Wëreef('terminal');yombal_xewxew(.3)
            Wëreef('mkdir first; cd first; export NAME=one')
            Yónnee('vi 첫째.py\n'.encode(),b'NORMAL')
            Yónnee('i값 = 21\nprint(xëyma * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            jeexal_Randal=time.monotonic()+3
            while time.monotonic()<jeexal_Randal:yombal_xewxew(.1)
            Yónnee(Teggi_xëyma(1),b'TERMINAL FOCUS 2');yombal_xewxew(.2)
            assert b'/\r\n' in Wëreef('pwd')
            Wëreef('export NAME=two')
            Yónnee('vi 둘째.txt\n'.encode(),b'NORMAL')
            Yónnee('i두 번째 palanteer\n'.encode(),b'INSERT')
            Yónnee(bës_butoñ(180,12),b'TERMINAL FOCUS 1');yombal_xewxew(.2)
            ndigel_anam();Yónnee(b':wq\r')
            assert b'one:/first' in Wëreef('echo "$NAME:$PWD"')
            assert 'xëyma = 21\r\nprint(xëyma * 2)'.encode() in Wëreef('cat 첫째.py')
            결과=Wëreef('python 첫째.py');assert b'42\r\n' in 결과,결과
            # Close the first shell with its actual title-bar X; second editor resumes.
            Yónnee(bës_butoñ(560,63),b'TERMINAL FOCUS 2');yombal_xewxew(.2)
            ndigel_anam();Yónnee(b':wq\r')
            assert b'two:/' in Wëreef('echo "$NAME:$PWD"')
            assert '두 번째 palanteer'.encode() in Wëreef('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            Yónnee('vi 둘째.txt\n'.encode(),b'NORMAL');Yónnee(b'xu',b'NORMAL')
            Yónnee(b'iX',b'INSERT');ndigel_anam();Yónnee(b':q\r',b'Unsaved')
            Yónnee(b':q!\r');assert '두 번째 palanteer'.encode() in Wëreef('cat 둘째.txt')
            Yónnee(Teggi_xëyma(1),b'TERMINAL FOCUS 1');yombal_xewxew(.2)
            Yónnee(Teggi_xëyma(1),b'TERMINAL FOCUS 3');yombal_xewxew(.2)
            Yónnee(Teggi_xëyma(1),b'TERMINAL FOCUS 4');yombal_xewxew(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            자료위치.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));자료위치.stdin.flush()
            Wëreef('echo DRAGGED_OK')
            Yónnee('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            Yónnee('i저장하지 않은 mbir'.encode(),b'INSERT')
            Yónnee(bës_butoñ(578,97),b'TERMINAL FOCUS 3');yombal_xewxew(.2)
            assert '버릴문서.txt'.encode() not in Wëreef('ls')
            Yónnee(Teggi_xëyma(1),b'TERMINAL FOCUS 4');yombal_xewxew(.2)
            Wëreef('echo REUSED_WINDOW_OK')
            완료량=làq_Dënk.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            jeexal_Randal=time.monotonic()+.3
            while time.monotonic()<jeexal_Randal:yombal_xewxew(.05)
            with socket.socket(socket.AF_UNIX) as kotu_araf:
                kotu_araf.settimeout(10);kotu_araf.connect(str(모의제어접속))
                with kotu_araf.makefile('rwb') as bara_denc_dugal_xabaar:
                    json.loads(bara_denc_dugal_xabaar.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'four-terminals.png'),'format':'png'}}):
                        bara_denc_dugal_xabaar.write((json.dumps(요청값)+'\n').encode());bara_denc_dugal_xabaar.flush()
                        while True:
                            반환값=json.loads(bara_denc_dugal_xabaar.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(목적위치/'four-terminals.png')).convert('RGB')
            for tëralinu_tëggin,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(tëralinu_tëggin)==색상,(tëralinu_tëggin,화소들.getpixel(tëralinu_tëggin))
            Wëreef('echo FOUR_WINDOWS_OK')
            wéral_tënk.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            tànnkat_a916db4e.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(làq_Dënk);(목적위치/'report.json').write_text(json.dumps(wéral_tënk,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':daw()
