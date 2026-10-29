#!/usr/bin/env python3
"""Run all examples in the real combined VNC + SLIP/FTP native VM."""
import ftplib
import hashlib
import io
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from meja_lihat import EXACT_VALUE
from 예제되돌림서버 import 되돌림서버
from laksanakan_perintah import projek_akar


def ujian_Bahasa(Bahasa,되돌림서버항목,ukuran_data):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));pemindahan_fail_nombor_port=임시자원.getsockname()[1]
    Proses=subprocess.Popen(['python3',str(projek_akar/'alat/laksanakan_perintah.py'),'--desktop','--network','--port','0','--ftp-port',str(pemindahan_fail_nombor_port)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비선택기=selectors.DefaultSelector();준비선택기.register(Proses.stdout,selectors.EVENT_READ)
    대화기록=bytearray();klien=None;pemindahan_fail_hubungan=None
    def 수신하기(penanda,Jalan=0):
        tamat_Ofset=time.monotonic()+60
        while penanda not in 대화기록[Jalan:]:
            if time.monotonic()>tamat_Ofset or Proses.poll() is not None:raise AssertionError(대화기록[Jalan:].decode('utf-8','replace'))
            for 누름값,_ in 준비선택기.select(.1):
                data=누름값.fileobj.read(65536)
                if data:대화기록.extend(data)
        return 대화기록[Jalan:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(simbol_VALUE,누르는중=True):klien.sendall(struct.pack('>BBHI',4,int(누르는중),0,simbol_VALUE))
    def Mula_Ofset(baris):
        Jalan=len(대화기록)
        for titik_kod in baris+'\n':
            simbol_VALUE=0xff0d if titik_kod=='\n' else ord(titik_kod) if ord(titik_kod)<256 else 0x1000000|ord(titik_kod)
            누름값(simbol_VALUE);누름값(simbol_VALUE,False)
        return Jalan
    def cangkerang(baris):return 수신하기(b'jkoros-native> ',Mula_Ofset(baris))
    def laksanakan_perintah(baris,예상결과):
        Teks=cangkerang(baris);assert 예상결과 in Teks and 'exit 0' in Teks,(baris,Teks)
        return Teks
    def 화소들():
        klien.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            bidang_VALUE=EXACT_VALUE(klien,1)[0]
            if bidang_VALUE==2:continue
            if bidang_VALUE==3:
                item_COUNT=struct.unpack('>I',EXACT_VALUE(klien,7)[3:])[0];EXACT_VALUE(klien,item_COUNT);continue
            assert bidang_VALUE==0,bidang_VALUE
            pemasukan_COUNT=struct.unpack('>H',EXACT_VALUE(klien,3)[1:])[0]
            for _ in range(pemasukan_COUNT):
                koordinat_x,Y_koordinat,너비값,높이값,set_aksara=struct.unpack('>HHHHi',EXACT_VALUE(klien,12));assert set_aksara==0,set_aksara
                data=EXACT_VALUE(klien,너비값*높이값*4)
                for ROW_jawatan in range(높이값):
                    for lajur_jawatan in range(너비값):
                        원본자료=(ROW_jawatan*너비값+lajur_jawatan)*4;sasaran=((Y_koordinat+ROW_jawatan)*640+koordinat_x+lajur_jawatan)*3
                        빛삼원색[sasaran:sasaran+3]=bytes((data[원본자료+2],data[원본자료+1],data[원본자료]))
            if pemasukan_COUNT:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        nombor_port=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        klien=socket.create_connection(('127.0.0.1',nombor_port),timeout=10)
        assert EXACT_VALUE(klien,12)==b'RFB 003.008\n';klien.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(klien,EXACT_VALUE(klien,1)[0]);klien.sendall(b'\x01');assert EXACT_VALUE(klien,4)==b'\0'*4
        klien.sendall(b'\x01');초기값=EXACT_VALUE(klien,24);EXACT_VALUE(klien,struct.unpack('>I',초기값[20:])[0])
        klien.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        klien.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in cangkerang('ftpd start')
        pemindahan_fail_hubungan=ftplib.FTP();pemindahan_fail_hubungan.encoding='utf-8';pemindahan_fail_hubungan.connect('127.0.0.1',pemindahan_fail_nombor_port,timeout=20);pemindahan_fail_hubungan.login()
        muat_beban_data=('GUI와 FTP 동시 사용 '+Bahasa+' 😀\n').encode()
        pemindahan_fail_hubungan.storbinary('STOR 함께.txt',io.BytesIO(muat_beban_data))
        assert muat_beban_data.decode().strip() in cangkerang('cat /함께.txt')
        RECEIVED_COUNT=bytearray();pemindahan_fail_hubungan.retrbinary('RETR 함께.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==muat_beban_data;pemindahan_fail_hubungan.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        e_mel_Senarai=cangkerang('ls /example')
        assert all(Nama in e_mel_Senarai for Nama in ('java/','c/','python/','README.md')),e_mel_Senarai
        if Bahasa=='java':
            pakej_manifes_aplikasi=json.loads((projek_akar/'build/examples/manifest.json').read_text())
            for LALUAN,titik_permulaan in pakej_manifes_aplikasi.items():
                cangkerang('cp '+LALUAN+' /example-check.bin')
                Kandungan_VALUE=bytearray();pemindahan_fail_hubungan.retrbinary('RETR example-check.bin',Kandungan_VALUE.extend)
                assert len(Kandungan_VALUE)==titik_permulaan['bytes'] and hashlib.sha256(Kandungan_VALUE).hexdigest()==titik_permulaan['sha256'],LALUAN
            pemindahan_fail_hubungan.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            perduaan=bytes(range(256))*64
            pemindahan_fail_hubungan.storbinary('STOR boundary.bin',io.BytesIO(perduaan))
            Kandungan_VALUE=bytearray();pemindahan_fail_hubungan.retrbinary('RETR boundary.bin',Kandungan_VALUE.extend)
            assert Kandungan_VALUE==perduaan and 'boundary.bin' in pemindahan_fail_hubungan.nlst()
            cangkerang('cp /boundary.bin /boundary-copy.bin')
            Kandungan_VALUE=bytearray();pemindahan_fail_hubungan.retrbinary('RETR boundary-copy.bin',Kandungan_VALUE.extend)
            assert Kandungan_VALUE==perduaan
            pemindahan_fail_hubungan.delete('boundary.bin');pemindahan_fail_hubungan.delete('boundary-copy.bin')
        assert 'ContohKeluaran' in cangkerang('ls /example/'+Bahasa)
        cangkerang('cd /example/'+Bahasa)
        nama_jadual={'java':'JAVA','c':'C','python':'PYTHON'}[Bahasa]
        예상파일=nama_jadual+' Fail: 한글 data 😀\n'
        if Bahasa=='java':
            laksanakan_perintah('javac ContohKeluaran.java','Compiled:');laksanakan_perintah('java ContohKeluaran','JAVA 출력: 안녕하세요 😀')
            laksanakan_perintah('javac ContohFail.java','Compiled:');laksanakan_perintah('java ContohFail',예상파일)
            laksanakan_perintah('java ContohRangkaian {} {}'.format(되돌림서버항목.TCP_port,되돌림서버항목.UDP_port),'JAVA 네트워크 tentu_sahkan: TCP UDP 한글')
            grafik_perintah='java ContohLukisan'
        elif Bahasa=='c':
            for Nama,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('Fail','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.UDP_port),'C 네트워크 tentu_sahkan: UDP 한글')]:
                laksanakan_perintah('cc '+Nama+'예제.c -o laksanakan_perintah','Compiled native ARM64 ELF:')
                laksanakan_perintah('./laksanakan_perintah'+전달값,예상결과)
            laksanakan_perintah('cc ContohLukisan.c -o laksanakan_perintah','Compiled native ARM64 ELF:');grafik_perintah='./laksanakan_perintah'
        else:
            for Nama,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('Fail','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.UDP_port),'PYTHON 네트워크 tentu_sahkan: UDP 한글')]:
                laksanakan_perintah('python '+Nama+'예제.py'+전달값,예상결과)
            grafik_perintah='python ContohLukisan.py'
        Mula_lukisan=Mula_Ofset(grafik_perintah)
        Teks=수신하기('그림을 확인한 BACK_VALUE Enter를 누르세요.\r\n'.encode(),Mula_lukisan)
        assert nama_jadual+' 그래픽: 빨강 초록 파랑' in Teks and 'exit 0' not in Teks,Teks
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        pemindahan_fail_hubungan.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        RECEIVED_COUNT=bytearray();pemindahan_fail_hubungan.retrbinary('RETR 도중.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==b'FTP DURING GRAPHICS';pemindahan_fail_hubungan.delete('도중.txt')
        빛삼원색=화소들()
        for Y_koordinat,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            Ofset_VALUE=(Y_koordinat*640+610)*3;assert tuple(빛삼원색[Ofset_VALUE:Ofset_VALUE+3])==색상,(Bahasa,Y_koordinat,tuple(빛삼원색[Ofset_VALUE:Ofset_VALUE+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(ukuran_data/(Bahasa+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',Mula_lukisan)
        if Bahasa=='java':
            Mula_tetingkap=Mula_Ofset('java ContohTetingkap')
            수신하기('GUI 예제 Sediakan: ContohTetingkap'.encode(),Mula_tetingkap)
            def klik_VALUE(가로,Menegak_jawatan):
                for Butang in (1,0):klien.sendall(struct.pack('>BBHH',5,Butang,가로,Menegak_jawatan))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            klik_VALUE(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for aksara_VALUE in '한글':누름값(0x1000000|ord(aksara_VALUE));누름값(0x1000000|ord(aksara_VALUE),False)
            for 횟수 in (1,2):
                Jalan=len(대화기록);klik_VALUE(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Jalan)
            time.sleep(.3)
            tetingkap_lukisan=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=tetingkap_lukisan.crop((110,272,530,300)).tobytes()
            tetingkap_lukisan.save(str(ukuran_data/'java-swing.png'))
            Jalan=len(대화기록);klik_VALUE(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',Jalan)
        # Download the guest-created bytes through FTP in the same GUI VM.
        fail_pemasukan_nama={'java':'java.txt','c':'c.txt','python':'python.txt'}[Bahasa]
        cangkerang('cp '+fail_pemasukan_nama+' /sahkan.txt')
        RECEIVED_COUNT=bytearray();pemindahan_fail_hubungan.retrbinary('RETR sahkan.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==예상파일.encode()
        cangkerang('echo preserved > ContohKeluaran.'+('py' if Bahasa=='python' else Bahasa))
        assert 'EXAMPLES READY' in cangkerang('example '+Bahasa)
        assert '\npreserved\n' in cangkerang('cat ContohKeluaran.'+('py' if Bahasa=='python' else Bahasa))
        assert '한/영 Kunci_VALUE, Shift+Space 또는 F9' in cangkerang('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in cangkerang('echo GUI NETWORK TOGETHER')
        pemindahan_fail_hubungan.quit();pemindahan_fail_hubungan=None;assert 'FTP stopped' in cangkerang('ftpd stop')
        print('PASS '+Bahasa+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if pemindahan_fail_hubungan:
            try:pemindahan_fail_hubungan.close()
            except OSError:pass
        if klien:klien.close()
        Proses.terminate()
        try:Proses.wait(timeout=8)
        except subprocess.TimeoutExpired:Proses.kill();Proses.wait()
        준비선택기.close();Proses.stdout.close();(ukuran_data/(Bahasa+'-serial.log')).write_bytes(대화기록)


def Jalan():
    ukuran_data=projek_akar/'build/verification/examples';ukuran_data.mkdir(parents=True,exist_ok=True)
    pensahihan_lapor={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((projek_akar/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for Bahasa in ('java','c','python'):
                ujian_Bahasa(Bahasa,되돌림서버항목,ukuran_data);pensahihan_lapor['languages'].append(Bahasa)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(bidang_VALUE,data.encode()) for bidang_VALUE,data in 예상결과],되돌림서버항목.수신됨
            pensahihan_lapor['host_network_payloads']=[{'protocol':bidang_VALUE,'text':data.decode()} for bidang_VALUE,data in 되돌림서버항목.수신됨]
        pensahihan_lapor.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(ukuran_data/'report.json').write_text(json.dumps(pensahihan_lapor,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Jalan()
