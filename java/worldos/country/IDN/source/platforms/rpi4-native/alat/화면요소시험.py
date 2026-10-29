#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Jalankan_perintah import Tugas_akar,perintah

def jalankan():
    tujuan_VALUE_posisi=Tugas_akar/'build/verification/swing';tujuan_VALUE_posisi.mkdir(parents=True,exist_ok=True)
    Kelas_jalur=Tugas_akar/'build/verification/new-java';Kelas_jalur.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(Tugas_akar/'dist/jkoros-native-korean.jar'),'-d',str(Kelas_jalur),str(Tugas_akar/'pengujian/자바/스윙시험.java'),str(Tugas_akar/'pengujian/자바/한글창시험.java')])
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
            data=(Tugas_akar/'build/verification/new-java/스윙시험.class').read_bytes()
            kirim('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(data),64):kirim(data[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            kirim(b'.\n')
            kirim('java 스윙시험\n'.encode(),b'SWING READY')
            mengakhiri_OFFSET=time.monotonic()+3
            while time.monotonic()<mengakhiri_OFFSET:handel_acara(.1)
            # JFrame centered at (120,100), content at y=130.
            kirim(klik_tombol(200,210),b'',)  # focus JTextField
            data_posisi.stdin.write('누리'.encode());data_posisi.stdin.flush()
            mengakhiri_OFFSET=time.monotonic()+.3
            while time.monotonic()<mengakhiri_OFFSET:handel_acara(.05)
            hasil=kirim(klik_tombol(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_baris)-len(hasil))
            kirim(pintasan_VALUE(1),b'TERMINAL FOCUS 2')
            hasil=shell('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in hasil
            kirim(klik_tombol(180,12),b'TERMINAL FOCUS 1')
            mengakhiri_OFFSET=time.monotonic()+.3
            while time.monotonic()<mengakhiri_OFFSET:handel_acara(.05)
            with socket.socket(socket.AF_UNIX) as kode_karakter:
                kode_karakter.settimeout(10);kode_karakter.connect(str(모의제어접속))
                with kode_karakter.makefile('rwb') as file_entri:
                    json.loads(file_entri.readline())
                    for permintaan_VALUE in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(tujuan_VALUE_posisi/'native-swing.png'),'format':'png'}}):
                        file_entri.write((json.dumps(permintaan_VALUE)+'\n').encode());file_entri.flush()
                        while True:
                            반환값=json.loads(file_entri.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            kirim(klik_tombol(505,115))
            shell('echo SWING_CLOSED_OK')
            data=(Kelas_jalur/'한글창시험.class').read_bytes()
            kirim('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(data),64):kirim(data[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            kirim(b'.\n')
            kirim('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            kirim(klik_tombol(200,255),'KOREAN SWING CLICK Nama_2'.encode())
            kirim(klik_tombol(505,115))
            shell('echo KOREAN_SWING_CLOSED_OK')
            validasi_lapor.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','Indonesia Jendela/tombol/동작알림/acara_antrean directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if data_posisi.poll() is None:data_posisi.terminate()
            try:data_posisi.wait(timeout=5)
            except subprocess.TimeoutExpired:data_posisi.kill();data_posisi.wait()
            pemilih_a916db4e.close();data_posisi.stdin.close();data_posisi.stdout.close();(tujuan_VALUE_posisi/'serial.log').write_bytes(LOG_baris);(tujuan_VALUE_posisi/'report.json').write_text(json.dumps(validasi_lapor,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':jalankan()
