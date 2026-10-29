#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from icra_etmək_əmr import Project_kök,Əmr

def İcra_Et():
    təyinat_VALUE_yerinə_qoymaq=Project_kök/'build/verification/windows';təyinat_VALUE_yerinə_qoymaq.mkdir(parents=True,exist_ok=True)
    yoxlama_hesabat={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_kök/'build/kernel8.img').read_bytes()).hexdigest()};LOG_yaz=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        verilənlər_yerinə_qoymaq=subprocess.Popen(Əmr()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        seçici_a916db4e=selectors.DefaultSelector();seçici_a916db4e.register(verilənlər_yerinə_qoymaq.stdout,selectors.EVENT_READ)
        def tutacaq_hadisə(초단위=.1):
            for 누름값,_ in seçici_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_yaz.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_yaz and b'HALTED' not in LOG_yaz,LOG_yaz[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            bitirmək_OFFSET=time.monotonic()+초단위
            while 확인표시 not in LOG_yaz[현재위치:]:
                if time.monotonic()>bitirmək_OFFSET or verilənlər_yerinə_qoymaq.poll() is not None:raise AssertionError(LOG_yaz[현재위치:].decode('utf-8','replace'))
                tutacaq_hadisə()
            return bytes(LOG_yaz[현재위치:])
        def göndərmək(SECOND_VALUE,확인표시=b'jkoros-native> '):
            현재위치=len(LOG_yaz);verilənlər_yerinə_qoymaq.stdin.write(SECOND_VALUE);verilənlər_yerinə_qoymaq.stdin.flush();return 기다리기(확인표시,현재위치)
        def örtük(sətir_verilənlər):return göndərmək((sətir_verilənlər+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def qısayol_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def klikləmə_düymə(x_koordinatı,Y_koordinat):return bytes([30,1,1,x_koordinatı&255,x_koordinatı>>8,Y_koordinat&255,Y_koordinat>>8,30,1,0,x_koordinatı&255,x_koordinatı>>8,Y_koordinat&255,Y_koordinat>>8])
        def əmr_MODE():
            verilənlər_yerinə_qoymaq.stdin.write(b'\x1b');verilənlər_yerinə_qoymaq.stdin.flush();bitirmək_OFFSET=time.monotonic()+.2
            while time.monotonic()<bitirmək_OFFSET:tutacaq_hadisə(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            örtük('terminal');tutacaq_hadisə(.3)
            örtük('mkdir first; cd first; export NAME=one')
            göndərmək('vi 첫째.py\n'.encode(),b'NORMAL')
            göndərmək('i값 = 21\nprint(VALUE * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            bitirmək_OFFSET=time.monotonic()+3
            while time.monotonic()<bitirmək_OFFSET:tutacaq_hadisə(.1)
            göndərmək(qısayol_VALUE(1),b'TERMINAL FOCUS 2');tutacaq_hadisə(.2)
            assert b'/\r\n' in örtük('pwd')
            örtük('export NAME=two')
            göndərmək('vi 둘째.txt\n'.encode(),b'NORMAL')
            göndərmək('i두 번째 pəncərə\n'.encode(),b'INSERT')
            göndərmək(klikləmə_düymə(180,12),b'TERMINAL FOCUS 1');tutacaq_hadisə(.2)
            əmr_MODE();göndərmək(b':wq\r')
            assert b'one:/first' in örtük('echo "$NAME:$PWD"')
            assert 'VALUE = 21\r\nprint(VALUE * 2)'.encode() in örtük('cat 첫째.py')
            ölçü=örtük('python 첫째.py');assert b'42\r\n' in ölçü,ölçü
            # Close the first shell with its actual title-bar X; second editor resumes.
            göndərmək(klikləmə_düymə(560,63),b'TERMINAL FOCUS 2');tutacaq_hadisə(.2)
            əmr_MODE();göndərmək(b':wq\r')
            assert b'two:/' in örtük('echo "$NAME:$PWD"')
            assert '두 번째 pəncərə'.encode() in örtük('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            göndərmək('vi 둘째.txt\n'.encode(),b'NORMAL');göndərmək(b'xu',b'NORMAL')
            göndərmək(b'iX',b'INSERT');əmr_MODE();göndərmək(b':q\r',b'Unsaved')
            göndərmək(b':q!\r');assert '두 번째 pəncərə'.encode() in örtük('cat 둘째.txt')
            göndərmək(qısayol_VALUE(1),b'TERMINAL FOCUS 1');tutacaq_hadisə(.2)
            göndərmək(qısayol_VALUE(1),b'TERMINAL FOCUS 3');tutacaq_hadisə(.2)
            göndərmək(qısayol_VALUE(1),b'TERMINAL FOCUS 4');tutacaq_hadisə(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            verilənlər_yerinə_qoymaq.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));verilənlər_yerinə_qoymaq.stdin.flush()
            örtük('echo DRAGGED_OK')
            göndərmək('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            göndərmək('i저장하지 않은 verilənlər'.encode(),b'INSERT')
            göndərmək(klikləmə_düymə(578,97),b'TERMINAL FOCUS 3');tutacaq_hadisə(.2)
            assert '버릴문서.txt'.encode() not in örtük('ls')
            göndərmək(qısayol_VALUE(1),b'TERMINAL FOCUS 4');tutacaq_hadisə(.2)
            örtük('echo REUSED_WINDOW_OK')
            완료량=LOG_yaz.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            bitirmək_OFFSET=time.monotonic()+.3
            while time.monotonic()<bitirmək_OFFSET:tutacaq_hadisə(.05)
            with socket.socket(socket.AF_UNIX) as simvol_kodu:
                simvol_kodu.settimeout(10);simvol_kodu.connect(str(모의제어접속))
                with simvol_kodu.makefile('rwb') as fayl_daxiletmə:
                    json.loads(fayl_daxiletmə.readline())
                    for HTTP_sorğusu_VALUE in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(təyinat_VALUE_yerinə_qoymaq/'four-terminals.png'),'format':'png'}}):
                        fayl_daxiletmə.write((json.dumps(HTTP_sorğusu_VALUE)+'\n').encode());fayl_daxiletmə.flush()
                        while True:
                            반환값=json.loads(fayl_daxiletmə.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(təyinat_VALUE_yerinə_qoymaq/'four-terminals.png')).convert('RGB')
            for koordinat_cütü,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(koordinat_cütü)==색상,(koordinat_cütü,화소들.getpixel(koordinat_cütü))
            örtük('echo FOUR_WINDOWS_OK')
            yoxlama_hesabat.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if verilənlər_yerinə_qoymaq.poll() is None:verilənlər_yerinə_qoymaq.terminate()
            try:verilənlər_yerinə_qoymaq.wait(timeout=5)
            except subprocess.TimeoutExpired:verilənlər_yerinə_qoymaq.kill();verilənlər_yerinə_qoymaq.wait()
            seçici_a916db4e.close();verilənlər_yerinə_qoymaq.stdin.close();verilənlər_yerinə_qoymaq.stdout.close();(təyinat_VALUE_yerinə_qoymaq/'serial.log').write_bytes(LOG_yaz);(təyinat_VALUE_yerinə_qoymaq/'report.json').write_text(json.dumps(yoxlama_hesabat,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':İcra_Et()
