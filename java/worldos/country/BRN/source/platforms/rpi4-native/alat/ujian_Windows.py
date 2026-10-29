#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from laksanakan_perintah import projek_akar,Perintah

def Jalan():
    destinasi_VALUE_jawatan=projek_akar/'build/verification/windows';destinasi_VALUE_jawatan.mkdir(parents=True,exist_ok=True)
    pensahihan_lapor={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((projek_akar/'build/kernel8.img').read_bytes()).hexdigest()};LOG_baris=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        data_jawatan=subprocess.Popen(Perintah()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        선택기=selectors.DefaultSelector();선택기.register(data_jawatan.stdout,selectors.EVENT_READ)
        def pemegang_acara(초단위=.1):
            for 누름값,_ in 선택기.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_baris.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_baris and b'HALTED' not in LOG_baris,LOG_baris[-2048:]
        def 기다리기(penanda,현재위치,초단위=50):
            tamat_Ofset=time.monotonic()+초단위
            while penanda not in LOG_baris[현재위치:]:
                if time.monotonic()>tamat_Ofset or data_jawatan.poll() is not None:raise AssertionError(LOG_baris[현재위치:].decode('utf-8','replace'))
                pemegang_acara()
            return bytes(LOG_baris[현재위치:])
        def e_mel_9aee63bd(SECOND_VALUE,penanda=b'jkoros-native> '):
            현재위치=len(LOG_baris);data_jawatan.stdin.write(SECOND_VALUE);data_jawatan.stdin.flush();return 기다리기(penanda,현재위치)
        def cangkerang(rentetan_data):return e_mel_9aee63bd((rentetan_data+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def pintasan_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def klik_butang(koordinat_x,Y_koordinat):return bytes([30,1,1,koordinat_x&255,koordinat_x>>8,Y_koordinat&255,Y_koordinat>>8,30,1,0,koordinat_x&255,koordinat_x>>8,Y_koordinat&255,Y_koordinat>>8])
        def perintah_mod():
            data_jawatan.stdin.write(b'\x1b');data_jawatan.stdin.flush();tamat_Ofset=time.monotonic()+.2
            while time.monotonic()<tamat_Ofset:pemegang_acara(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            cangkerang('terminal');pemegang_acara(.3)
            cangkerang('mkdir first; cd first; export NAME=one')
            e_mel_9aee63bd('vi 첫째.py\n'.encode(),b'NORMAL')
            e_mel_9aee63bd('i값 = 21\nprint(VALUE * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            tamat_Ofset=time.monotonic()+3
            while time.monotonic()<tamat_Ofset:pemegang_acara(.1)
            e_mel_9aee63bd(pintasan_VALUE(1),b'TERMINAL FOCUS 2');pemegang_acara(.2)
            assert b'/\r\n' in cangkerang('pwd')
            cangkerang('export NAME=two')
            e_mel_9aee63bd('vi 둘째.txt\n'.encode(),b'NORMAL')
            e_mel_9aee63bd('i두 번째 Tetingkap\n'.encode(),b'INSERT')
            e_mel_9aee63bd(klik_butang(180,12),b'TERMINAL FOCUS 1');pemegang_acara(.2)
            perintah_mod();e_mel_9aee63bd(b':wq\r')
            assert b'one:/first' in cangkerang('echo "$NAME:$PWD"')
            assert 'VALUE = 21\r\nprint(VALUE * 2)'.encode() in cangkerang('cat 첫째.py')
            ukuran=cangkerang('python 첫째.py');assert b'42\r\n' in ukuran,ukuran
            # Close the first shell with its actual title-bar X; second editor resumes.
            e_mel_9aee63bd(klik_butang(560,63),b'TERMINAL FOCUS 2');pemegang_acara(.2)
            perintah_mod();e_mel_9aee63bd(b':wq\r')
            assert b'two:/' in cangkerang('echo "$NAME:$PWD"')
            assert '두 번째 Tetingkap'.encode() in cangkerang('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            e_mel_9aee63bd('vi 둘째.txt\n'.encode(),b'NORMAL');e_mel_9aee63bd(b'xu',b'NORMAL')
            e_mel_9aee63bd(b'iX',b'INSERT');perintah_mod();e_mel_9aee63bd(b':q\r',b'Unsaved')
            e_mel_9aee63bd(b':q!\r');assert '두 번째 Tetingkap'.encode() in cangkerang('cat 둘째.txt')
            e_mel_9aee63bd(pintasan_VALUE(1),b'TERMINAL FOCUS 1');pemegang_acara(.2)
            e_mel_9aee63bd(pintasan_VALUE(1),b'TERMINAL FOCUS 3');pemegang_acara(.2)
            e_mel_9aee63bd(pintasan_VALUE(1),b'TERMINAL FOCUS 4');pemegang_acara(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            data_jawatan.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));data_jawatan.stdin.flush()
            cangkerang('echo DRAGGED_OK')
            e_mel_9aee63bd('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            e_mel_9aee63bd('i저장하지 않은 data'.encode(),b'INSERT')
            e_mel_9aee63bd(klik_butang(578,97),b'TERMINAL FOCUS 3');pemegang_acara(.2)
            assert '버릴문서.txt'.encode() not in cangkerang('ls')
            e_mel_9aee63bd(pintasan_VALUE(1),b'TERMINAL FOCUS 4');pemegang_acara(.2)
            cangkerang('echo REUSED_WINDOW_OK')
            Selesai_amaun=LOG_baris.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',Selesai_amaun)
            # UART completion precedes the next QEMU display refresh.
            tamat_Ofset=time.monotonic()+.3
            while time.monotonic()<tamat_Ofset:pemegang_acara(.05)
            with socket.socket(socket.AF_UNIX) as titik_kod:
                titik_kod.settimeout(10);titik_kod.connect(str(모의제어접속))
                with titik_kod.makefile('rwb') as fail_pemasukan:
                    json.loads(fail_pemasukan.readline())
                    for permintaan_VALUE in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(destinasi_VALUE_jawatan/'four-terminals.png'),'format':'png'}}):
                        fail_pemasukan.write((json.dumps(permintaan_VALUE)+'\n').encode());fail_pemasukan.flush()
                        while True:
                            반환값=json.loads(fail_pemasukan.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(destinasi_VALUE_jawatan/'four-terminals.png')).convert('RGB')
            for pasangan_koordinat,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(pasangan_koordinat)==색상,(pasangan_koordinat,화소들.getpixel(pasangan_koordinat))
            cangkerang('echo FOUR_WINDOWS_OK')
            pensahihan_lapor.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if data_jawatan.poll() is None:data_jawatan.terminate()
            try:data_jawatan.wait(timeout=5)
            except subprocess.TimeoutExpired:data_jawatan.kill();data_jawatan.wait()
            선택기.close();data_jawatan.stdin.close();data_jawatan.stdout.close();(destinasi_VALUE_jawatan/'serial.log').write_bytes(LOG_baris);(destinasi_VALUE_jawatan/'report.json').write_text(json.dumps(pensahihan_lapor,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Jalan()
