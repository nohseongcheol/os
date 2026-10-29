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
from Masaüstü_Görünüm import ÖZDEŞ_değer
from 예제되돌림서버 import yankı_Sunucular
from yürütmek_komut import işlem_kök


def test_Dil(Dil,yankı_sunucu_girdi,KR_veri):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));dosya_aktarımı_bağlantı_noktası_numarası=임시자원.getsockname()[1]
    Süreç=subprocess.Popen(['python3',str(işlem_kök/'araçlar/yürütmek_komut.py'),'--desktop','--network','--port','0','--ftp-port',str(dosya_aktarımı_bağlantı_noktası_numarası)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    seçici=selectors.DefaultSelector();seçici.register(Süreç.stdout,selectors.EVENT_READ)
    döküm=bytearray();istemci=None;dosya_aktarımı_cxn=None
    def almak_belge(işaret,çalıştır=0):
        Bitiş_Ofset=time.monotonic()+60
        while işaret not in döküm[çalıştır:]:
            if time.monotonic()>Bitiş_Ofset or Süreç.poll() is not None:raise AssertionError(döküm[çalıştır:].decode('utf-8','replace'))
            for 누름값,_ in seçici.select(.1):
                veri=누름값.fileobj.read(65536)
                if veri:döküm.extend(veri)
        return döküm[çalıştır:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(simge_değer,누르는중=True):istemci.sendall(struct.pack('>BBHI',4,int(누르는중),0,simge_değer))
    def Start_Ofset(girdi_satırı):
        çalıştır=len(döküm)
        for kod_noktası in girdi_satırı+'\n':
            simge_değer=0xff0d if kod_noktası=='\n' else ord(kod_noktası) if ord(kod_noktası)<256 else 0x1000000|ord(kod_noktası)
            누름값(simge_değer);누름값(simge_değer,False)
        return çalıştır
    def kabuk(girdi_satırı):return almak_belge(b'jkoros-native> ',Start_Ofset(girdi_satırı))
    def yürütmek_komut(girdi_satırı,예상결과):
        metin=kabuk(girdi_satırı);assert 예상결과 in metin and 'exit 0' in metin,(girdi_satırı,metin)
        return metin
    def 화소들():
        istemci.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            alan_değer=ÖZDEŞ_değer(istemci,1)[0]
            if alan_değer==2:continue
            if alan_değer==3:
                öğe_BAĞ_DEĞ_SAY=struct.unpack('>I',ÖZDEŞ_değer(istemci,7)[3:])[0];ÖZDEŞ_değer(istemci,öğe_BAĞ_DEĞ_SAY);continue
            assert alan_değer==0,alan_değer
            girdi_BAĞ_DEĞ_SAY=struct.unpack('>H',ÖZDEŞ_değer(istemci,3)[1:])[0]
            for _ in range(girdi_BAĞ_DEĞ_SAY):
                x_koordinatı,Y_koordinat,너비값,높이값,karakter_kümesi=struct.unpack('>HHHHi',ÖZDEŞ_değer(istemci,12));assert karakter_kümesi==0,karakter_kümesi
                veri=ÖZDEŞ_değer(istemci,너비값*높이값*4)
                for SATIR_konum in range(높이값):
                    for SÜTUN_konum in range(너비값):
                        원본자료=(SATIR_konum*너비값+SÜTUN_konum)*4;hedef=((Y_koordinat+SATIR_konum)*640+x_koordinatı+SÜTUN_konum)*3
                        빛삼원색[hedef:hedef+3]=bytes((veri[원본자료+2],veri[원본자료+1],veri[원본자료]))
            if girdi_BAĞ_DEĞ_SAY:return 빛삼원색
    try:
        almak_belge(b'TERMINAL READY');almak_belge(b'jkoros-native> ',döküm.rfind(b'TERMINAL READY'))
        bağlantı_noktası_numarası=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',döküm).group(1))
        istemci=socket.create_connection(('127.0.0.1',bağlantı_noktası_numarası),timeout=10)
        assert ÖZDEŞ_değer(istemci,12)==b'RFB 003.008\n';istemci.sendall(b'RFB 003.008\n')
        assert 1 in ÖZDEŞ_değer(istemci,ÖZDEŞ_değer(istemci,1)[0]);istemci.sendall(b'\x01');assert ÖZDEŞ_değer(istemci,4)==b'\0'*4
        istemci.sendall(b'\x01');초기값=ÖZDEŞ_değer(istemci,24);ÖZDEŞ_değer(istemci,struct.unpack('>I',초기값[20:])[0])
        istemci.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        istemci.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in kabuk('ftpd start')
        dosya_aktarımı_cxn=ftplib.FTP();dosya_aktarımı_cxn.encoding='utf-8';dosya_aktarımı_cxn.connect('127.0.0.1',dosya_aktarımı_bağlantı_noktası_numarası,timeout=20);dosya_aktarımı_cxn.login()
        yük_veri=('GUI와 FTP 동시 kullanmak_değer '+Dil+' 😀\n').encode()
        dosya_aktarımı_cxn.storbinary('STOR 함께.txt',io.BytesIO(yük_veri))
        assert yük_veri.decode().strip() in kabuk('cat /함께.txt')
        GETİRİ_BAĞ_DEĞ_SAY=bytearray();dosya_aktarımı_cxn.retrbinary('RETR 함께.txt',GETİRİ_BAĞ_DEĞ_SAY.extend);assert GETİRİ_BAĞ_DEĞ_SAY==yük_veri;dosya_aktarımı_cxn.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        göndermek_Liste=kabuk('ls /example')
        assert all(İsim in göndermek_Liste for İsim in ('java/','c/','python/','README.md')),göndermek_Liste
        if Dil=='java':
            paket_iş_bildirim=json.loads((işlem_kök/'build/examples/manifest.json').read_text())
            for yol,giriş_noktası in paket_iş_bildirim.items():
                kabuk('cp '+yol+' /example-check.bin')
                içerik_değer=bytearray();dosya_aktarımı_cxn.retrbinary('RETR example-check.bin',içerik_değer.extend)
                assert len(içerik_değer)==giriş_noktası['bytes'] and hashlib.sha256(içerik_değer).hexdigest()==giriş_noktası['sha256'],yol
            dosya_aktarımı_cxn.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            ikili=bytes(range(256))*64
            dosya_aktarımı_cxn.storbinary('STOR boundary.bin',io.BytesIO(ikili))
            içerik_değer=bytearray();dosya_aktarımı_cxn.retrbinary('RETR boundary.bin',içerik_değer.extend)
            assert içerik_değer==ikili and 'boundary.bin' in dosya_aktarımı_cxn.nlst()
            kabuk('cp /boundary.bin /boundary-copy.bin')
            içerik_değer=bytearray();dosya_aktarımı_cxn.retrbinary('RETR boundary-copy.bin',içerik_değer.extend)
            assert içerik_değer==ikili
            dosya_aktarımı_cxn.delete('boundary.bin');dosya_aktarımı_cxn.delete('boundary-copy.bin')
        assert 'ÇıktıÖrneği' in kabuk('ls /example/'+Dil)
        kabuk('cd /example/'+Dil)
        ad_tablo={'java':'JAVA','c':'C','python':'PYTHON'}[Dil]
        예상파일=ad_tablo+' dosya: 한글 veri 😀\n'
        if Dil=='java':
            yürütmek_komut('javac ÇıktıÖrneği.java','Compiled:');yürütmek_komut('java ÇıktıÖrneği','JAVA metinÇıktısı: 안녕하세요 😀')
            yürütmek_komut('javac DosyaÖrneği.java','Compiled:');yürütmek_komut('java DosyaÖrneği',예상파일)
            yürütmek_komut('java AğÖrneği {} {}'.format(yankı_sunucu_girdi.TCP_bağlantı_noktası,yankı_sunucu_girdi.UDP_taşımak),'JAVA 네트워크 doğrulamak: TCP UDP 한글')
            grafik_komut='java ÇizimÖrneği'
        elif Dil=='c':
            for İsim,전달값,예상결과 in [('metinÇıktısı','', 'C metinÇıktısı: 안녕하세요 😀'),('dosya','',예상파일),
                    ('네트워크',' '+str(yankı_sunucu_girdi.UDP_taşımak),'C 네트워크 doğrulamak: UDP 한글')]:
                yürütmek_komut('cc '+İsim+'예제.c -o yürütmek_komut','Compiled native ARM64 ELF:')
                yürütmek_komut('./yürütmek_komut'+전달값,예상결과)
            yürütmek_komut('cc ÇizimÖrneği.c -o yürütmek_komut','Compiled native ARM64 ELF:');grafik_komut='./yürütmek_komut'
        else:
            for İsim,전달값,예상결과 in [('metinÇıktısı','','PYTHON metinÇıktısı: 안녕하세요 😀'),('dosya','',예상파일),
                    ('네트워크',' '+str(yankı_sunucu_girdi.UDP_taşımak),'PYTHON 네트워크 doğrulamak: UDP 한글')]:
                yürütmek_komut('python '+İsim+'예제.py'+전달값,예상결과)
            grafik_komut='python ÇizimÖrneği.py'
        Start_çizim=Start_Ofset(grafik_komut)
        metin=almak_belge('그림을 확인한 BACK_değer Enter를 누르세요.\r\n'.encode(),Start_çizim)
        assert ad_tablo+' 그래픽: 빨강 초록 파랑' in metin and 'exit 0' not in metin,metin
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        dosya_aktarımı_cxn.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        GETİRİ_BAĞ_DEĞ_SAY=bytearray();dosya_aktarımı_cxn.retrbinary('RETR 도중.txt',GETİRİ_BAĞ_DEĞ_SAY.extend);assert GETİRİ_BAĞ_DEĞ_SAY==b'FTP DURING GRAPHICS';dosya_aktarımı_cxn.delete('도중.txt')
        빛삼원색=화소들()
        for Y_koordinat,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            Ofset_değer=(Y_koordinat*640+610)*3;assert tuple(빛삼원색[Ofset_değer:Ofset_değer+3])==색상,(Dil,Y_koordinat,tuple(빛삼원색[Ofset_değer:Ofset_değer+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(KR_veri/(Dil+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in almak_belge(b'jkoros-native> ',Start_çizim)
        if Dil=='java':
            Start_pencere=Start_Ofset('java PencereÖrneği')
            almak_belge('GUI 예제 Hazırlan: PencereÖrneği'.encode(),Start_pencere)
            def tık_değer(가로,Dikey_konum):
                for düğme in (1,0):istemci.sendall(struct.pack('>BBHH',5,düğme,가로,Dikey_konum))
            time.sleep(.3)
            Önceki_RESİM=Image.frombytes('RGB',(640,480),bytes(화소들()))
            tık_değer(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for karakter_değer in '한글':누름값(0x1000000|ord(karakter_değer));누름값(0x1000000|ord(karakter_değer),False)
            for 횟수 in (1,2):
                çalıştır=len(döküm);tık_değer(180,242)
                almak_belge(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),çalıştır)
            time.sleep(.3)
            pencere_çizim=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert Önceki_RESİM.crop((110,272,530,300)).tobytes()!=pencere_çizim.crop((110,272,530,300)).tobytes()
            pencere_çizim.save(str(KR_veri/'java-swing.png'))
            çalıştır=len(döküm);tık_değer(535,105)
            assert 'exit 0' in almak_belge(b'jkoros-native> ',çalıştır)
        # Download the guest-created bytes through FTP in the same GUI VM.
        Dosya_girdi_ad={'java':'java.txt','c':'c.txt','python':'python.txt'}[Dil]
        kabuk('cp '+Dosya_girdi_ad+' /doğrulamak_5fb2b747.txt')
        GETİRİ_BAĞ_DEĞ_SAY=bytearray();dosya_aktarımı_cxn.retrbinary('RETR doğrulamak_5fb2b747.txt',GETİRİ_BAĞ_DEĞ_SAY.extend);assert GETİRİ_BAĞ_DEĞ_SAY==예상파일.encode()
        kabuk('echo preserved > ÇıktıÖrneği.'+('py' if Dil=='python' else Dil))
        assert 'EXAMPLES READY' in kabuk('example '+Dil)
        assert '\npreserved\n' in kabuk('cat ÇıktıÖrneği.'+('py' if Dil=='python' else Dil))
        assert '한/sıfır_işlenen tuş_değer, Shift+Space 또는 F9' in kabuk('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in kabuk('echo GUI NETWORK TOGETHER')
        dosya_aktarımı_cxn.quit();dosya_aktarımı_cxn=None;assert 'FTP stopped' in kabuk('ftpd stop')
        print('PASS '+Dil+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if dosya_aktarımı_cxn:
            try:dosya_aktarımı_cxn.close()
            except OSError:pass
        if istemci:istemci.close()
        Süreç.terminate()
        try:Süreç.wait(timeout=8)
        except subprocess.TimeoutExpired:Süreç.kill();Süreç.wait()
        seçici.close();Süreç.stdout.close();(KR_veri/(Dil+'-serial.log')).write_bytes(döküm)


def çalıştır():
    KR_veri=işlem_kök/'build/verification/examples';KR_veri.mkdir(parents=True,exist_ok=True)
    doğrulama_Rapor={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((işlem_kök/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with yankı_Sunucular() as yankı_sunucu_girdi:
            for Dil in ('java','c','python'):
                test_Dil(Dil,yankı_sunucu_girdi,KR_veri);doğrulama_Rapor['languages'].append(Dil)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert yankı_sunucu_girdi.수신됨==[(alan_değer,veri.encode()) for alan_değer,veri in 예상결과],yankı_sunucu_girdi.수신됨
            doğrulama_Rapor['host_network_payloads']=[{'protocol':alan_değer,'text':veri.decode()} for alan_değer,veri in yankı_sunucu_girdi.수신됨]
        doğrulama_Rapor.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(KR_veri/'report.json').write_text(json.dumps(doğrulama_Rapor,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':çalıştır()
