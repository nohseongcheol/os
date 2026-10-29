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
from desktop_Tampilan import EXACT_VALUE
from 예제되돌림서버 import echo_Server
from Jalankan_perintah import Tugas_akar


def test_언어(Bahasa,echo_server_entri,KR_data):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));transfer_file_nomor_port=임시자원.getsockname()[1]
    Proses=subprocess.Popen(['python3',str(Tugas_akar/'alat/Jalankan_perintah.py'),'--desktop','--network','--port','0','--ftp-port',str(transfer_file_nomor_port)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    pemilih=selectors.DefaultSelector();pemilih.register(Proses.stdout,selectors.EVENT_READ)
    transkrip=bytearray();klien=None;transfer_file_koneksi=None
    def terima_email(확인표시,jalankan=0):
        mengakhiri_OFFSET=time.monotonic()+60
        while 확인표시 not in transkrip[jalankan:]:
            if time.monotonic()>mengakhiri_OFFSET or Proses.poll() is not None:raise AssertionError(transkrip[jalankan:].decode('utf-8','replace'))
            for 누름값,_ in pemilih.select(.1):
                data=누름값.fileobj.read(65536)
                if data:transkrip.extend(data)
        return transkrip[jalankan:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(simbol_VALUE,누르는중=True):klien.sendall(struct.pack('>BBHI',4,int(누르는중),0,simbol_VALUE))
    def Mulai_OFFSET(baris_masukan):
        jalankan=len(transkrip)
        for kode_karakter in baris_masukan+'\n':
            simbol_VALUE=0xff0d if kode_karakter=='\n' else ord(kode_karakter) if ord(kode_karakter)<256 else 0x1000000|ord(kode_karakter)
            누름값(simbol_VALUE);누름값(simbol_VALUE,False)
        return jalankan
    def shell(baris_masukan):return terima_email(b'jkoros-native> ',Mulai_OFFSET(baris_masukan))
    def Jalankan_perintah(baris_masukan,예상결과):
        teks=shell(baris_masukan);assert 예상결과 in teks and 'exit 0' in teks,(baris_masukan,teks)
        return teks
    def 화소들():
        klien.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            area_VALUE=EXACT_VALUE(klien,1)[0]
            if area_VALUE==2:continue
            if area_VALUE==3:
                item_COUNT=struct.unpack('>I',EXACT_VALUE(klien,7)[3:])[0];EXACT_VALUE(klien,item_COUNT);continue
            assert area_VALUE==0,area_VALUE
            entri_COUNT=struct.unpack('>H',EXACT_VALUE(klien,3)[1:])[0]
            for _ in range(entri_COUNT):
                koordinat_x,Y_koordinat,너비값,높이값,tataan_karakter=struct.unpack('>HHHHi',EXACT_VALUE(klien,12));assert tataan_karakter==0,tataan_karakter
                data=EXACT_VALUE(klien,너비값*높이값*4)
                for ROW_posisi in range(높이값):
                    for kolom_posisi in range(너비값):
                        원본자료=(ROW_posisi*너비값+kolom_posisi)*4;target=((Y_koordinat+ROW_posisi)*640+koordinat_x+kolom_posisi)*3
                        빛삼원색[target:target+3]=bytes((data[원본자료+2],data[원본자료+1],data[원본자료]))
            if entri_COUNT:return 빛삼원색
    try:
        terima_email(b'TERMINAL READY');terima_email(b'jkoros-native> ',transkrip.rfind(b'TERMINAL READY'))
        nomor_port=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',transkrip).group(1))
        klien=socket.create_connection(('127.0.0.1',nomor_port),timeout=10)
        assert EXACT_VALUE(klien,12)==b'RFB 003.008\n';klien.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(klien,EXACT_VALUE(klien,1)[0]);klien.sendall(b'\x01');assert EXACT_VALUE(klien,4)==b'\0'*4
        klien.sendall(b'\x01');초기값=EXACT_VALUE(klien,24);EXACT_VALUE(klien,struct.unpack('>I',초기값[20:])[0])
        klien.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        klien.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in shell('ftpd start')
        transfer_file_koneksi=ftplib.FTP();transfer_file_koneksi.encoding='utf-8';transfer_file_koneksi.connect('127.0.0.1',transfer_file_nomor_port,timeout=20);transfer_file_koneksi.login()
        payload_data=('GUI와 FTP 동시 gunakan_VALUE '+Bahasa+' 😀\n').encode()
        transfer_file_koneksi.storbinary('STOR 함께.txt',io.BytesIO(payload_data))
        assert payload_data.decode().strip() in shell('cat /함께.txt')
        RECEIVED_COUNT=bytearray();transfer_file_koneksi.retrbinary('RETR 함께.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==payload_data;transfer_file_koneksi.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        kirim_Daftar=shell('ls /example')
        assert all(Nama_2 in kirim_Daftar for Nama_2 in ('java/','c/','python/','README.md')),kirim_Daftar
        if Bahasa=='java':
            꾸러미명세=json.loads((Tugas_akar/'build/examples/manifest.json').read_text())
            for jalur,entri_p in 꾸러미명세.items():
                shell('cp '+jalur+' /example-check.bin')
                Isi_VALUE=bytearray();transfer_file_koneksi.retrbinary('RETR example-check.bin',Isi_VALUE.extend)
                assert len(Isi_VALUE)==entri_p['bytes'] and hashlib.sha256(Isi_VALUE).hexdigest()==entri_p['sha256'],jalur
            transfer_file_koneksi.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            biner=bytes(range(256))*64
            transfer_file_koneksi.storbinary('STOR boundary.bin',io.BytesIO(biner))
            Isi_VALUE=bytearray();transfer_file_koneksi.retrbinary('RETR boundary.bin',Isi_VALUE.extend)
            assert Isi_VALUE==biner and 'boundary.bin' in transfer_file_koneksi.nlst()
            shell('cp /boundary.bin /boundary-copy.bin')
            Isi_VALUE=bytearray();transfer_file_koneksi.retrbinary('RETR boundary-copy.bin',Isi_VALUE.extend)
            assert Isi_VALUE==biner
            transfer_file_koneksi.delete('boundary.bin');transfer_file_koneksi.delete('boundary-copy.bin')
        assert 'ContohKeluaran' in shell('ls /example/'+Bahasa)
        shell('cd /example/'+Bahasa)
        nama_tabel={'java':'JAVA','c':'C','python':'PYTHON'}[Bahasa]
        예상파일=nama_tabel+' berkas: 한글 data 😀\n'
        if Bahasa=='java':
            Jalankan_perintah('javac ContohKeluaran.java','Compiled:');Jalankan_perintah('java ContohKeluaran','JAVA keluaranTeks: 안녕하세요 😀')
            Jalankan_perintah('javac ContohBerkas.java','Compiled:');Jalankan_perintah('java ContohBerkas',예상파일)
            Jalankan_perintah('java ContohJaringan {} {}'.format(echo_server_entri.TCP_port,echo_server_entri.UDP_port),'JAVA 네트워크 periksa: TCP UDP 한글')
            grafis_perintah='java ContohGambar'
        elif Bahasa=='c':
            for Nama_2,전달값,예상결과 in [('keluaranTeks','', 'C keluaranTeks: 안녕하세요 😀'),('berkas','',예상파일),
                    ('네트워크',' '+str(echo_server_entri.UDP_port),'C 네트워크 periksa: UDP 한글')]:
                Jalankan_perintah('cc '+Nama_2+'예제.c -o Jalankan_perintah','Compiled native ARM64 ELF:')
                Jalankan_perintah('./Jalankan_perintah'+전달값,예상결과)
            Jalankan_perintah('cc ContohGambar.c -o Jalankan_perintah','Compiled native ARM64 ELF:');grafis_perintah='./Jalankan_perintah'
        else:
            for Nama_2,전달값,예상결과 in [('keluaranTeks','','PYTHON keluaranTeks: 안녕하세요 😀'),('berkas','',예상파일),
                    ('네트워크',' '+str(echo_server_entri.UDP_port),'PYTHON 네트워크 periksa: UDP 한글')]:
                Jalankan_perintah('python '+Nama_2+'예제.py'+전달값,예상결과)
            grafis_perintah='python ContohGambar.py'
        Mulai_gambar=Mulai_OFFSET(grafis_perintah)
        teks=terima_email('그림을 확인한 BACK_VALUE Enter를 누르세요.\r\n'.encode(),Mulai_gambar)
        assert nama_tabel+' 그래픽: 빨강 초록 파랑' in teks and 'exit 0' not in teks,teks
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        transfer_file_koneksi.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        RECEIVED_COUNT=bytearray();transfer_file_koneksi.retrbinary('RETR 도중.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==b'FTP DURING GRAPHICS';transfer_file_koneksi.delete('도중.txt')
        빛삼원색=화소들()
        for Y_koordinat,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            OFFSET_VALUE=(Y_koordinat*640+610)*3;assert tuple(빛삼원색[OFFSET_VALUE:OFFSET_VALUE+3])==색상,(Bahasa,Y_koordinat,tuple(빛삼원색[OFFSET_VALUE:OFFSET_VALUE+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(KR_data/(Bahasa+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in terima_email(b'jkoros-native> ',Mulai_gambar)
        if Bahasa=='java':
            Mulai_jendela=Mulai_OFFSET('java ContohJendela')
            terima_email('GUI 예제 Siapkan: ContohJendela'.encode(),Mulai_jendela)
            def klik_VALUE(가로,Vertikal_posisi):
                for tombol in (1,0):klien.sendall(struct.pack('>BBHH',5,tombol,가로,Vertikal_posisi))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            klik_VALUE(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for karakter_VALUE in '한글':누름값(0x1000000|ord(karakter_VALUE));누름값(0x1000000|ord(karakter_VALUE),False)
            for pengulangan_COUNT in (1,2):
                jalankan=len(transkrip);klik_VALUE(180,242)
                terima_email(('GUI 인사: 안녕하세요, 한글님! ('+str(pengulangan_COUNT)+')').encode(),jalankan)
            time.sleep(.3)
            jendela_gambar=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=jendela_gambar.crop((110,272,530,300)).tobytes()
            jendela_gambar.save(str(KR_data/'java-swing.png'))
            jalankan=len(transkrip);klik_VALUE(535,105)
            assert 'exit 0' in terima_email(b'jkoros-native> ',jalankan)
        # Download the guest-created bytes through FTP in the same GUI VM.
        file_entri_nama={'java':'java.txt','c':'c.txt','python':'python.txt'}[Bahasa]
        shell('cp '+file_entri_nama+' /validasi.txt')
        RECEIVED_COUNT=bytearray();transfer_file_koneksi.retrbinary('RETR validasi.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==예상파일.encode()
        shell('echo preserved > ContohKeluaran.'+('py' if Bahasa=='python' else Bahasa))
        assert 'EXAMPLES READY' in shell('example '+Bahasa)
        assert '\npreserved\n' in shell('cat ContohKeluaran.'+('py' if Bahasa=='python' else Bahasa))
        assert '한/영 Kunci_VALUE, Shift+Space 또는 F9' in shell('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in shell('echo GUI NETWORK TOGETHER')
        transfer_file_koneksi.quit();transfer_file_koneksi=None;assert 'FTP stopped' in shell('ftpd stop')
        print('PASS '+Bahasa+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if transfer_file_koneksi:
            try:transfer_file_koneksi.close()
            except OSError:pass
        if klien:klien.close()
        Proses.terminate()
        try:Proses.wait(timeout=8)
        except subprocess.TimeoutExpired:Proses.kill();Proses.wait()
        pemilih.close();Proses.stdout.close();(KR_data/(Bahasa+'-serial.log')).write_bytes(transkrip)


def jalankan():
    KR_data=Tugas_akar/'build/verification/examples';KR_data.mkdir(parents=True,exist_ok=True)
    validasi_lapor={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Tugas_akar/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with echo_Server() as echo_server_entri:
            for Bahasa in ('java','c','python'):
                test_언어(Bahasa,echo_server_entri,KR_data);validasi_lapor['languages'].append(Bahasa)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert echo_server_entri.수신됨==[(area_VALUE,data.encode()) for area_VALUE,data in 예상결과],echo_server_entri.수신됨
            validasi_lapor['host_network_payloads']=[{'protocol':area_VALUE,'text':data.decode()} for area_VALUE,data in echo_server_entri.수신됨]
        validasi_lapor.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(KR_data/'report.json').write_text(json.dumps(validasi_lapor,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':jalankan()
