#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from mee_nnyemiwu import 기준,Ntiiwu

def Bido():
    목적위치=기준/'build/verification/windows';목적위치.mkdir(parents=True,exist_ok=True)
    nkwèputaonòdù_akụkọ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};ndekọ_NDEKỌ=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(Ntiiwu()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        ihe_nhọpụta_a916db4e=selectors.DefaultSelector();ihe_nhọpụta_a916db4e.register(자료위치.stdout,selectors.EVENT_READ)
        def ebenjìaka_mmèrème(초단위=.1):
            for 누름값,_ in ihe_nhọpụta_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:ndekọ_NDEKỌ.extend(둘째값)
            assert b'PANIC:' not in ndekọ_NDEKỌ and b'HALTED' not in ndekọ_NDEKỌ,ndekọ_NDEKỌ[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            mèdebe_Nnokwata=time.monotonic()+초단위
            while 확인표시 not in ndekọ_NDEKỌ[현재위치:]:
                if time.monotonic()>mèdebe_Nnokwata or 자료위치.poll() is not None:raise AssertionError(ndekọ_NDEKỌ[현재위치:].decode('utf-8','replace'))
                ebenjìaka_mmèrème()
            return bytes(ndekọ_NDEKỌ[현재위치:])
        def zìga(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(ndekọ_NDEKỌ);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def nkọwannyemiwu(ùsòròokwū_datà):return zìga((ùsòròokwū_datà+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def ụzọnsō_valuu(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def pịkịnye_ọdụmbi(ngakọrịta_x,세로좌표):return bytes([30,1,1,ngakọrịta_x&255,ngakọrịta_x>>8,세로좌표&255,세로좌표>>8,30,1,0,ngakọrịta_x&255,ngakọrịta_x>>8,세로좌표&255,세로좌표>>8])
        def nnyemiwu_moòdù():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();mèdebe_Nnokwata=time.monotonic()+.2
            while time.monotonic()<mèdebe_Nnokwata:ebenjìaka_mmèrème(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            nkọwannyemiwu('terminal');ebenjìaka_mmèrème(.3)
            nkọwannyemiwu('mkdir first; cd first; export NAME=one')
            zìga('vi 첫째.py\n'.encode(),b'NORMAL')
            zìga('i값 = 21\nprint(valuu * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            mèdebe_Nnokwata=time.monotonic()+3
            while time.monotonic()<mèdebe_Nnokwata:ebenjìaka_mmèrème(.1)
            zìga(ụzọnsō_valuu(1),b'TERMINAL FOCUS 2');ebenjìaka_mmèrème(.2)
            assert b'/\r\n' in nkọwannyemiwu('pwd')
            nkọwannyemiwu('export NAME=two')
            zìga('vi 둘째.txt\n'.encode(),b'NORMAL')
            zìga('i두 번째 windò\n'.encode(),b'INSERT')
            zìga(pịkịnye_ọdụmbi(180,12),b'TERMINAL FOCUS 1');ebenjìaka_mmèrème(.2)
            nnyemiwu_moòdù();zìga(b':wq\r')
            assert b'one:/first' in nkọwannyemiwu('echo "$NAME:$PWD"')
            assert 'valuu = 21\r\nprint(valuu * 2)'.encode() in nkọwannyemiwu('cat 첫째.py')
            결과=nkọwannyemiwu('python 첫째.py');assert b'42\r\n' in 결과,결과
            # Close the first shell with its actual title-bar X; second editor resumes.
            zìga(pịkịnye_ọdụmbi(560,63),b'TERMINAL FOCUS 2');ebenjìaka_mmèrème(.2)
            nnyemiwu_moòdù();zìga(b':wq\r')
            assert b'two:/' in nkọwannyemiwu('echo "$NAME:$PWD"')
            assert '두 번째 windò'.encode() in nkọwannyemiwu('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            zìga('vi 둘째.txt\n'.encode(),b'NORMAL');zìga(b'xu',b'NORMAL')
            zìga(b'iX',b'INSERT');nnyemiwu_moòdù();zìga(b':q\r',b'Unsaved')
            zìga(b':q!\r');assert '두 번째 windò'.encode() in nkọwannyemiwu('cat 둘째.txt')
            zìga(ụzọnsō_valuu(1),b'TERMINAL FOCUS 1');ebenjìaka_mmèrème(.2)
            zìga(ụzọnsō_valuu(1),b'TERMINAL FOCUS 3');ebenjìaka_mmèrème(.2)
            zìga(ụzọnsō_valuu(1),b'TERMINAL FOCUS 4');ebenjìaka_mmèrème(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            자료위치.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));자료위치.stdin.flush()
            nkọwannyemiwu('echo DRAGGED_OK')
            zìga('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            zìga('i저장하지 않은 datà'.encode(),b'INSERT')
            zìga(pịkịnye_ọdụmbi(578,97),b'TERMINAL FOCUS 3');ebenjìaka_mmèrème(.2)
            assert '버릴문서.txt'.encode() not in nkọwannyemiwu('ls')
            zìga(ụzọnsō_valuu(1),b'TERMINAL FOCUS 4');ebenjìaka_mmèrème(.2)
            nkọwannyemiwu('echo REUSED_WINDOW_OK')
            완료량=ndekọ_NDEKỌ.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            mèdebe_Nnokwata=time.monotonic()+.3
            while time.monotonic()<mèdebe_Nnokwata:ebenjìaka_mmèrème(.05)
            with socket.socket(socket.AF_UNIX) as koòdù_nkeakàrà:
                koòdù_nkeakàrà.settimeout(10);koòdù_nkeakàrà.connect(str(모의제어접속))
                with koòdù_nkeakàrà.makefile('rwb') as ọbọakwụkwọ_ndebà:
                    json.loads(ọbọakwụkwọ_ndebà.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'four-terminals.png'),'format':'png'}}):
                        ọbọakwụkwọ_ndebà.write((json.dumps(요청값)+'\n').encode());ọbọakwụkwọ_ndebà.flush()
                        while True:
                            반환값=json.loads(ọbọakwụkwọ_ndebà.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(목적위치/'four-terminals.png')).convert('RGB')
            for mkpị_nkwụgbà,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(mkpị_nkwụgbà)==색상,(mkpị_nkwụgbà,화소들.getpixel(mkpị_nkwụgbà))
            nkọwannyemiwu('echo FOUR_WINDOWS_OK')
            nkwèputaonòdù_akụkọ.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            ihe_nhọpụta_a916db4e.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(ndekọ_NDEKỌ);(목적위치/'report.json').write_text(json.dumps(nkwèputaonòdù_akụkọ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Bido()
