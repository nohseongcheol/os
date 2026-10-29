#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from ukwenza_umyalelo import 기준,Umyalelo

def Phumeza():
    목적위치=기준/'build/verification/windows';목적위치.mkdir(parents=True,exist_ok=True)
    uqinisekiso_ingxelo={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};ilog_umqolo=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(Umyalelo()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        umkhethi_a916db4e=selectors.DefaultSelector();umkhethi_a916db4e.register(자료위치.stdout,selectors.EVENT_READ)
        def isibambi_umcimbi(초단위=.1):
            for 누름값,_ in umkhethi_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:ilog_umqolo.extend(둘째값)
            assert b'PANIC:' not in ilog_umqolo and b'HALTED' not in ilog_umqolo,ilog_umqolo[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            phela_Ukulinganisa=time.monotonic()+초단위
            while 확인표시 not in ilog_umqolo[현재위치:]:
                if time.monotonic()>phela_Ukulinganisa or 자료위치.poll() is not None:raise AssertionError(ilog_umqolo[현재위치:].decode('utf-8','replace'))
                isibambi_umcimbi()
            return bytes(ilog_umqolo[현재위치:])
        def thumela(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(ilog_umqolo);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def isiniki_myalelo(uluhlu_lweekharektha_iingcombolo):return thumela((uluhlu_lweekharektha_iingcombolo+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def isinqumleli_ixabiso(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def cofa_iqhosha(isilungelelanisi_x,세로좌표):return bytes([30,1,1,isilungelelanisi_x&255,isilungelelanisi_x>>8,세로좌표&255,세로좌표>>8,30,1,0,isilungelelanisi_x&255,isilungelelanisi_x>>8,세로좌표&255,세로좌표>>8])
        def umyalelo_imo():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();phela_Ukulinganisa=time.monotonic()+.2
            while time.monotonic()<phela_Ukulinganisa:isibambi_umcimbi(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            isiniki_myalelo('terminal');isibambi_umcimbi(.3)
            isiniki_myalelo('mkdir first; cd first; export NAME=one')
            thumela('vi 첫째.py\n'.encode(),b'NORMAL')
            thumela('i값 = 21\nprint(ixabiso * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            phela_Ukulinganisa=time.monotonic()+3
            while time.monotonic()<phela_Ukulinganisa:isibambi_umcimbi(.1)
            thumela(isinqumleli_ixabiso(1),b'TERMINAL FOCUS 2');isibambi_umcimbi(.2)
            assert b'/\r\n' in isiniki_myalelo('pwd')
            isiniki_myalelo('export NAME=two')
            thumela('vi 둘째.txt\n'.encode(),b'NORMAL')
            thumela('i두 번째 i_window\n'.encode(),b'INSERT')
            thumela(cofa_iqhosha(180,12),b'TERMINAL FOCUS 1');isibambi_umcimbi(.2)
            umyalelo_imo();thumela(b':wq\r')
            assert b'one:/first' in isiniki_myalelo('echo "$NAME:$PWD"')
            assert 'ixabiso = 21\r\nprint(ixabiso * 2)'.encode() in isiniki_myalelo('cat 첫째.py')
            결과=isiniki_myalelo('python 첫째.py');assert b'42\r\n' in 결과,결과
            # Close the first shell with its actual title-bar X; second editor resumes.
            thumela(cofa_iqhosha(560,63),b'TERMINAL FOCUS 2');isibambi_umcimbi(.2)
            umyalelo_imo();thumela(b':wq\r')
            assert b'two:/' in isiniki_myalelo('echo "$NAME:$PWD"')
            assert '두 번째 i_window'.encode() in isiniki_myalelo('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            thumela('vi 둘째.txt\n'.encode(),b'NORMAL');thumela(b'xu',b'NORMAL')
            thumela(b'iX',b'INSERT');umyalelo_imo();thumela(b':q\r',b'Unsaved')
            thumela(b':q!\r');assert '두 번째 i_window'.encode() in isiniki_myalelo('cat 둘째.txt')
            thumela(isinqumleli_ixabiso(1),b'TERMINAL FOCUS 1');isibambi_umcimbi(.2)
            thumela(isinqumleli_ixabiso(1),b'TERMINAL FOCUS 3');isibambi_umcimbi(.2)
            thumela(isinqumleli_ixabiso(1),b'TERMINAL FOCUS 4');isibambi_umcimbi(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            자료위치.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));자료위치.stdin.flush()
            isiniki_myalelo('echo DRAGGED_OK')
            thumela('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            thumela('i저장하지 않은 iingcombolo'.encode(),b'INSERT')
            thumela(cofa_iqhosha(578,97),b'TERMINAL FOCUS 3');isibambi_umcimbi(.2)
            assert '버릴문서.txt'.encode() not in isiniki_myalelo('ls')
            thumela(isinqumleli_ixabiso(1),b'TERMINAL FOCUS 4');isibambi_umcimbi(.2)
            isiniki_myalelo('echo REUSED_WINDOW_OK')
            완료량=ilog_umqolo.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            phela_Ukulinganisa=time.monotonic()+.3
            while time.monotonic()<phela_Ukulinganisa:isibambi_umcimbi(.05)
            with socket.socket(socket.AF_UNIX) as ikhowudi_yekharakhtha:
                ikhowudi_yekharakhtha.settimeout(10);ikhowudi_yekharakhtha.connect(str(모의제어접속))
                with ikhowudi_yekharakhtha.makefile('rwb') as ifayile_ufako_nkcukacha:
                    json.loads(ifayile_ufako_nkcukacha.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'four-terminals.png'),'format':'png'}}):
                        ifayile_ufako_nkcukacha.write((json.dumps(요청값)+'\n').encode());ifayile_ufako_nkcukacha.flush()
                        while True:
                            반환값=json.loads(ifayile_ufako_nkcukacha.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(목적위치/'four-terminals.png')).convert('RGB')
            for isilungelelanisi,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(isilungelelanisi)==색상,(isilungelelanisi,화소들.getpixel(isilungelelanisi))
            isiniki_myalelo('echo FOUR_WINDOWS_OK')
            uqinisekiso_ingxelo.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            umkhethi_a916db4e.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(ilog_umqolo);(목적위치/'report.json').write_text(json.dumps(uqinisekiso_ingxelo,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Phumeza()
