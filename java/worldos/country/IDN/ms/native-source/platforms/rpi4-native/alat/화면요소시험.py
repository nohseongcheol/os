#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from laksanakan_perintah import projek_akar,Perintah

def Jalan():
    destinasi_VALUE_jawatan=projek_akar/'build/verification/swing';destinasi_VALUE_jawatan.mkdir(parents=True,exist_ok=True)
    Kelas_laluan=projek_akar/'build/verification/new-java';Kelas_laluan.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(projek_akar/'dist/jkoros-native-korean.jar'),'-d',str(Kelas_laluan),str(projek_akar/'ujian/자바/스윙시험.java'),str(projek_akar/'ujian/자바/한글창시험.java')])
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
            data=(projek_akar/'build/verification/new-java/스윙시험.class').read_bytes()
            e_mel_9aee63bd('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(data),64):e_mel_9aee63bd(data[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            e_mel_9aee63bd(b'.\n')
            e_mel_9aee63bd('java 스윙시험\n'.encode(),b'SWING READY')
            tamat_Ofset=time.monotonic()+3
            while time.monotonic()<tamat_Ofset:pemegang_acara(.1)
            # JFrame centered at (120,100), content at y=130.
            e_mel_9aee63bd(klik_butang(200,210),b'',)  # focus JTextField
            data_jawatan.stdin.write('누리'.encode());data_jawatan.stdin.flush()
            tamat_Ofset=time.monotonic()+.3
            while time.monotonic()<tamat_Ofset:pemegang_acara(.05)
            ukuran=e_mel_9aee63bd(klik_butang(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_baris)-len(ukuran))
            e_mel_9aee63bd(pintasan_VALUE(1),b'TERMINAL FOCUS 2')
            ukuran=cangkerang('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in ukuran
            e_mel_9aee63bd(klik_butang(180,12),b'TERMINAL FOCUS 1')
            tamat_Ofset=time.monotonic()+.3
            while time.monotonic()<tamat_Ofset:pemegang_acara(.05)
            with socket.socket(socket.AF_UNIX) as titik_kod:
                titik_kod.settimeout(10);titik_kod.connect(str(모의제어접속))
                with titik_kod.makefile('rwb') as fail_pemasukan:
                    json.loads(fail_pemasukan.readline())
                    for permintaan_VALUE in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(destinasi_VALUE_jawatan/'native-swing.png'),'format':'png'}}):
                        fail_pemasukan.write((json.dumps(permintaan_VALUE)+'\n').encode());fail_pemasukan.flush()
                        while True:
                            반환값=json.loads(fail_pemasukan.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            e_mel_9aee63bd(klik_butang(505,115))
            cangkerang('echo SWING_CLOSED_OK')
            data=(Kelas_laluan/'한글창시험.class').read_bytes()
            e_mel_9aee63bd('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(data),64):e_mel_9aee63bd(data[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            e_mel_9aee63bd(b'.\n')
            e_mel_9aee63bd('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            e_mel_9aee63bd(klik_butang(200,255),'KOREAN SWING CLICK Nama'.encode())
            e_mel_9aee63bd(klik_butang(505,115))
            cangkerang('echo KOREAN_SWING_CLOSED_OK')
            pensahihan_lapor.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','Melayu Tetingkap/Butang/동작알림/acara_baris directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if data_jawatan.poll() is None:data_jawatan.terminate()
            try:data_jawatan.wait(timeout=5)
            except subprocess.TimeoutExpired:data_jawatan.kill();data_jawatan.wait()
            선택기.close();data_jawatan.stdin.close();data_jawatan.stdout.close();(destinasi_VALUE_jawatan/'serial.log').write_bytes(LOG_baris);(destinasi_VALUE_jawatan/'report.json').write_text(json.dumps(pensahihan_lapor,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Jalan()
