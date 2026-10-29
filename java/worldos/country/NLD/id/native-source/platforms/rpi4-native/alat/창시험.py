#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Jalankan_perintah import Tugas_akar,perintah

def jalankan():
    tujuan_VALUE_posisi=Tugas_akar/'build/verification/windows';tujuan_VALUE_posisi.mkdir(parents=True,exist_ok=True)
    validasi_lapor={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Tugas_akar/'build/kernel8.img').read_bytes()).hexdigest()};LOG_baris=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        data_posisi=subprocess.Popen(perintah()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        pemilih_a916db4e=selectors.DefaultSelector();pemilih_a916db4e.register(data_posisi.stdout,selectors.EVENT_READ)
        def handel_acara(초단위=.1):
            for 누름값,_ in pemilih_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_baris.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_baris and b'HALTED' not in LOG_baris,LOG_baris[-2048:]
        def 기다리기(확인표시,saat_ini_posisi,초단위=50):
            mengakhiri_OFFSET=time.monotonic()+초단위
            while 확인표시 not in LOG_baris[saat_ini_posisi:]:
                if time.monotonic()>mengakhiri_OFFSET or data_posisi.poll() is not None:raise AssertionError(LOG_baris[saat_ini_posisi:].decode('utf-8','replace'))
                handel_acara()
            return bytes(LOG_baris[saat_ini_posisi:])
        def kirim(SECOND_VALUE,확인표시=b'jkoros-native> '):
            saat_ini_posisi=len(LOG_baris);data_posisi.stdin.write(SECOND_VALUE);data_posisi.stdin.flush();return 기다리기(확인표시,saat_ini_posisi)
        def shell(string_data):return kirim((string_data+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def pintasan_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def klik_tombol(koordinat_x,Y_koordinat):return bytes([30,1,1,koordinat_x&255,koordinat_x>>8,Y_koordinat&255,Y_koordinat>>8,30,1,0,koordinat_x&255,koordinat_x>>8,Y_koordinat&255,Y_koordinat>>8])
        def perintah_MODE():
            data_posisi.stdin.write(b'\x1b');data_posisi.stdin.flush();mengakhiri_OFFSET=time.monotonic()+.2
            while time.monotonic()<mengakhiri_OFFSET:handel_acara(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            shell('terminal');handel_acara(.3)
            shell('mkdir first; cd first; export NAME=one')
            kirim('vi 첫째.py\n'.encode(),b'NORMAL')
            kirim('i값 = 21\nprint(VALUE * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            mengakhiri_OFFSET=time.monotonic()+3
            while time.monotonic()<mengakhiri_OFFSET:handel_acara(.1)
            kirim(pintasan_VALUE(1),b'TERMINAL FOCUS 2');handel_acara(.2)
            assert b'/\r\n' in shell('pwd')
            shell('export NAME=two')
            kirim('vi 둘째.txt\n'.encode(),b'NORMAL')
            kirim('i두 번째 Jendela\n'.encode(),b'INSERT')
            kirim(klik_tombol(180,12),b'TERMINAL FOCUS 1');handel_acara(.2)
            perintah_MODE();kirim(b':wq\r')
            assert b'one:/first' in shell('echo "$NAME:$PWD"')
            assert 'VALUE = 21\r\nprint(VALUE * 2)'.encode() in shell('cat 첫째.py')
            hasil=shell('python 첫째.py');assert b'42\r\n' in hasil,hasil
            # Close the first shell with its actual title-bar X; second editor resumes.
            kirim(klik_tombol(560,63),b'TERMINAL FOCUS 2');handel_acara(.2)
            perintah_MODE();kirim(b':wq\r')
            assert b'two:/' in shell('echo "$NAME:$PWD"')
            assert '두 번째 Jendela'.encode() in shell('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            kirim('vi 둘째.txt\n'.encode(),b'NORMAL');kirim(b'xu',b'NORMAL')
            kirim(b'iX',b'INSERT');perintah_MODE();kirim(b':q\r',b'Unsaved')
            kirim(b':q!\r');assert '두 번째 Jendela'.encode() in shell('cat 둘째.txt')
            kirim(pintasan_VALUE(1),b'TERMINAL FOCUS 1');handel_acara(.2)
            kirim(pintasan_VALUE(1),b'TERMINAL FOCUS 3');handel_acara(.2)
            kirim(pintasan_VALUE(1),b'TERMINAL FOCUS 4');handel_acara(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            data_posisi.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));data_posisi.stdin.flush()
            shell('echo DRAGGED_OK')
            kirim('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            kirim('i저장하지 않은 data'.encode(),b'INSERT')
            kirim(klik_tombol(578,97),b'TERMINAL FOCUS 3');handel_acara(.2)
            assert '버릴문서.txt'.encode() not in shell('ls')
            kirim(pintasan_VALUE(1),b'TERMINAL FOCUS 4');handel_acara(.2)
            shell('echo REUSED_WINDOW_OK')
            Selesai_jumlah=LOG_baris.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',Selesai_jumlah)
            # UART completion precedes the next QEMU display refresh.
            mengakhiri_OFFSET=time.monotonic()+.3
            while time.monotonic()<mengakhiri_OFFSET:handel_acara(.05)
            with socket.socket(socket.AF_UNIX) as kode_karakter:
                kode_karakter.settimeout(10);kode_karakter.connect(str(모의제어접속))
                with kode_karakter.makefile('rwb') as file_entri:
                    json.loads(file_entri.readline())
                    for permintaan_VALUE in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(tujuan_VALUE_posisi/'four-terminals.png'),'format':'png'}}):
                        file_entri.write((json.dumps(permintaan_VALUE)+'\n').encode());file_entri.flush()
                        while True:
                            반환값=json.loads(file_entri.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(tujuan_VALUE_posisi/'four-terminals.png')).convert('RGB')
            for pasangan_koordinat,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(pasangan_koordinat)==색상,(pasangan_koordinat,화소들.getpixel(pasangan_koordinat))
            shell('echo FOUR_WINDOWS_OK')
            validasi_lapor.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if data_posisi.poll() is None:data_posisi.terminate()
            try:data_posisi.wait(timeout=5)
            except subprocess.TimeoutExpired:data_posisi.kill();data_posisi.wait()
            pemilih_a916db4e.close();data_posisi.stdin.close();data_posisi.stdout.close();(tujuan_VALUE_posisi/'serial.log').write_bytes(LOG_baris);(tujuan_VALUE_posisi/'report.json').write_text(json.dumps(validasi_lapor,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':jalankan()
