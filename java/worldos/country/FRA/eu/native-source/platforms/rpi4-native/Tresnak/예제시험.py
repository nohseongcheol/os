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
from mahaigain_ikusi import BERDIN_balio
from 예제되돌림서버 import atzeko_planoko_eguneratze_Zerbitzariak
from exekutatu_komando import Project_erro


def test_언어(Hizkuntza,atzeko_planoko_eguneratze_zerbitzari_sarrera,neurria_datuak):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));fitxategi_transferitu_ataka_zenbaki=임시자원.getsockname()[1]
    Prozesua=subprocess.Popen(['python3',str(Project_erro/'Tresnak/exekutatu_komando.py'),'--desktop','--network','--port','0','--ftp-port',str(fitxategi_transferitu_ataka_zenbaki)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비선택기=selectors.DefaultSelector();준비선택기.register(Prozesua.stdout,selectors.EVENT_READ)
    대화기록=bytearray();bezero=None;fitxategi_transferitu_konexio=None
    def 수신하기(확인표시,Exekutatu_2=0):
        amaitu_Geruzak=time.monotonic()+60
        while 확인표시 not in 대화기록[Exekutatu_2:]:
            if time.monotonic()>amaitu_Geruzak or Prozesua.poll() is not None:raise AssertionError(대화기록[Exekutatu_2:].decode('utf-8','replace'))
            for 누름값,_ in 준비선택기.select(.1):
                datuak=누름값.fileobj.read(65536)
                if datuak:대화기록.extend(datuak)
        return 대화기록[Exekutatu_2:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(ikur_balio,누르는중=True):bezero.sendall(struct.pack('>BBHI',4,int(누르는중),0,ikur_balio))
    def HASI_Geruzak(Marra):
        Exekutatu_2=len(대화기록)
        for karaktere_kode in Marra+'\n':
            ikur_balio=0xff0d if karaktere_kode=='\n' else ord(karaktere_kode) if ord(karaktere_kode)<256 else 0x1000000|ord(karaktere_kode)
            누름값(ikur_balio);누름값(ikur_balio,False)
        return Exekutatu_2
    def shell(Marra):return 수신하기(b'jkoros-native> ',HASI_Geruzak(Marra))
    def exekutatu_komando(Marra,예상결과):
        Testua=shell(Marra);assert 예상결과 in Testua and 'exit 0' in Testua,(Marra,Testua)
        return Testua
    def 화소들():
        bezero.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            Kategoria_balio=BERDIN_balio(bezero,1)[0]
            if Kategoria_balio==2:continue
            if Kategoria_balio==3:
                elementu_ZENBATU=struct.unpack('>I',BERDIN_balio(bezero,7)[3:])[0];BERDIN_balio(bezero,elementu_ZENBATU);continue
            assert Kategoria_balio==0,Kategoria_balio
            sarrera_ZENBATU=struct.unpack('>H',BERDIN_balio(bezero,3)[1:])[0]
            for _ in range(sarrera_ZENBATU):
                X_koordenatu,Y_koordenatu,너비값,높이값,karaktere_joko=struct.unpack('>HHHHi',BERDIN_balio(bezero,12));assert karaktere_joko==0,karaktere_joko
                datuak=BERDIN_balio(bezero,너비값*높이값*4)
                for ERRENKADA_kargu in range(높이값):
                    for zutabe_kargu in range(너비값):
                        원본자료=(ERRENKADA_kargu*너비값+zutabe_kargu)*4;helburu_balio=((Y_koordenatu+ERRENKADA_kargu)*640+X_koordenatu+zutabe_kargu)*3
                        빛삼원색[helburu_balio:helburu_balio+3]=bytes((datuak[원본자료+2],datuak[원본자료+1],datuak[원본자료]))
            if sarrera_ZENBATU:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        ataka_zenbaki=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        bezero=socket.create_connection(('127.0.0.1',ataka_zenbaki),timeout=10)
        assert BERDIN_balio(bezero,12)==b'RFB 003.008\n';bezero.sendall(b'RFB 003.008\n')
        assert 1 in BERDIN_balio(bezero,BERDIN_balio(bezero,1)[0]);bezero.sendall(b'\x01');assert BERDIN_balio(bezero,4)==b'\0'*4
        bezero.sendall(b'\x01');초기값=BERDIN_balio(bezero,24);BERDIN_balio(bezero,struct.unpack('>I',초기값[20:])[0])
        bezero.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        bezero.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in shell('ftpd start')
        fitxategi_transferitu_konexio=ftplib.FTP();fitxategi_transferitu_konexio.encoding='utf-8';fitxategi_transferitu_konexio.connect('127.0.0.1',fitxategi_transferitu_ataka_zenbaki,timeout=20);fitxategi_transferitu_konexio.login()
        karga_datuak=('GUI와 FTP 동시 사용 '+Hizkuntza+' 😀\n').encode()
        fitxategi_transferitu_konexio.storbinary('STOR 함께.txt',io.BytesIO(karga_datuak))
        assert karga_datuak.decode().strip() in shell('cat /함께.txt')
        RECEIVED_ZENBATU=bytearray();fitxategi_transferitu_konexio.retrbinary('RETR 함께.txt',RECEIVED_ZENBATU.extend);assert RECEIVED_ZENBATU==karga_datuak;fitxategi_transferitu_konexio.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        bidali_Zerrenda=shell('ls /example')
        assert all(Izena in bidali_Zerrenda for Izena in ('java/','c/','python/','README.md')),bidali_Zerrenda
        if Hizkuntza=='java':
            꾸러미명세=json.loads((Project_erro/'build/examples/manifest.json').read_text())
            for Bide_izena,sarrera_p in 꾸러미명세.items():
                shell('cp '+Bide_izena+' /example-check.bin')
                eduki_balio=bytearray();fitxategi_transferitu_konexio.retrbinary('RETR example-check.bin',eduki_balio.extend)
                assert len(eduki_balio)==sarrera_p['bytes'] and hashlib.sha256(eduki_balio).hexdigest()==sarrera_p['sha256'],Bide_izena
            fitxategi_transferitu_konexio.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            bitar=bytes(range(256))*64
            fitxategi_transferitu_konexio.storbinary('STOR boundary.bin',io.BytesIO(bitar))
            eduki_balio=bytearray();fitxategi_transferitu_konexio.retrbinary('RETR boundary.bin',eduki_balio.extend)
            assert eduki_balio==bitar and 'boundary.bin' in fitxategi_transferitu_konexio.nlst()
            shell('cp /boundary.bin /boundary-copy.bin')
            eduki_balio=bytearray();fitxategi_transferitu_konexio.retrbinary('RETR boundary-copy.bin',eduki_balio.extend)
            assert eduki_balio==bitar
            fitxategi_transferitu_konexio.delete('boundary.bin');fitxategi_transferitu_konexio.delete('boundary-copy.bin')
        assert '출력예제' in shell('ls /example/'+Hizkuntza)
        shell('cd /example/'+Hizkuntza)
        izen_taula={'java':'JAVA','c':'C','python':'PYTHON'}[Hizkuntza]
        예상파일=izen_taula+' Fitxategia: 한글 datuak 😀\n'
        if Hizkuntza=='java':
            exekutatu_komando('javac 출력예제.java','Compiled:');exekutatu_komando('java 출력예제','JAVA Irteera: 안녕하세요 😀')
            exekutatu_komando('javac 파일예제.java','Compiled:');exekutatu_komando('java 파일예제',예상파일)
            exekutatu_komando('java 네트워크예제 {} {}'.format(atzeko_planoko_eguneratze_zerbitzari_sarrera.TCP_ataka,atzeko_planoko_eguneratze_zerbitzari_sarrera.UDP_ataka),'JAVA 네트워크 egiaztatu: TCP UDP 한글')
            grafikoak_komando='java 그래픽예제'
        elif Hizkuntza=='c':
            for Izena,전달값,예상결과 in [('Irteera','', 'C Irteera: 안녕하세요 😀'),('Fitxategia','',예상파일),
                    ('네트워크',' '+str(atzeko_planoko_eguneratze_zerbitzari_sarrera.UDP_ataka),'C 네트워크 egiaztatu: UDP 한글')]:
                exekutatu_komando('cc '+Izena+'예제.c -o exekutatu_komando','Compiled native ARM64 ELF:')
                exekutatu_komando('./exekutatu_komando'+전달값,예상결과)
            exekutatu_komando('cc 그래픽예제.c -o exekutatu_komando','Compiled native ARM64 ELF:');grafikoak_komando='./exekutatu_komando'
        else:
            for Izena,전달값,예상결과 in [('Irteera','','PYTHON Irteera: 안녕하세요 😀'),('Fitxategia','',예상파일),
                    ('네트워크',' '+str(atzeko_planoko_eguneratze_zerbitzari_sarrera.UDP_ataka),'PYTHON 네트워크 egiaztatu: UDP 한글')]:
                exekutatu_komando('python '+Izena+'예제.py'+전달값,예상결과)
            grafikoak_komando='python 그래픽예제.py'
        그림시작=HASI_Geruzak(grafikoak_komando)
        Testua=수신하기('그림을 확인한 ATZERA_balio Enter를 누르세요.\r\n'.encode(),그림시작)
        assert izen_taula+' 그래픽: 빨강 초록 파랑' in Testua and 'exit 0' not in Testua,Testua
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        fitxategi_transferitu_konexio.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        RECEIVED_ZENBATU=bytearray();fitxategi_transferitu_konexio.retrbinary('RETR 도중.txt',RECEIVED_ZENBATU.extend);assert RECEIVED_ZENBATU==b'FTP DURING GRAPHICS';fitxategi_transferitu_konexio.delete('도중.txt')
        빛삼원색=화소들()
        for Y_koordenatu,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            Geruzak_balio=(Y_koordenatu*640+610)*3;assert tuple(빛삼원색[Geruzak_balio:Geruzak_balio+3])==색상,(Hizkuntza,Y_koordenatu,tuple(빛삼원색[Geruzak_balio:Geruzak_balio+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(neurria_datuak/(Hizkuntza+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',그림시작)
        if Hizkuntza=='java':
            HASI_leiho=HASI_Geruzak('java 창예제')
            수신하기('GUI 예제 준비: 창예제'.encode(),HASI_leiho)
            def klik_balio(가로,Bertikala_kargu):
                for botoia in (1,0):bezero.sendall(struct.pack('>BBHH',5,botoia,가로,Bertikala_kargu))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            klik_balio(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for karaktere_balio in '한글':누름값(0x1000000|ord(karaktere_balio));누름값(0x1000000|ord(karaktere_balio),False)
            for 횟수 in (1,2):
                Exekutatu_2=len(대화기록);klik_balio(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Exekutatu_2)
            time.sleep(.3)
            창그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=창그림.crop((110,272,530,300)).tobytes()
            창그림.save(str(neurria_datuak/'java-swing.png'))
            Exekutatu_2=len(대화기록);klik_balio(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',Exekutatu_2)
        # Download the guest-created bytes through FTP in the same GUI VM.
        fitxategi_sarrera_izen={'java':'java.txt','c':'c.txt','python':'python.txt'}[Hizkuntza]
        shell('cp '+fitxategi_sarrera_izen+' /baliozkotu.txt')
        RECEIVED_ZENBATU=bytearray();fitxategi_transferitu_konexio.retrbinary('RETR baliozkotu.txt',RECEIVED_ZENBATU.extend);assert RECEIVED_ZENBATU==예상파일.encode()
        shell('echo preserved > 출력예제.'+('py' if Hizkuntza=='python' else Hizkuntza))
        assert 'EXAMPLES READY' in shell('example '+Hizkuntza)
        assert '\npreserved\n' in shell('cat 출력예제.'+('py' if Hizkuntza=='python' else Hizkuntza))
        assert '한/영 gako_balio, Shift+Space 또는 F9' in shell('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in shell('echo GUI NETWORK TOGETHER')
        fitxategi_transferitu_konexio.quit();fitxategi_transferitu_konexio=None;assert 'FTP stopped' in shell('ftpd stop')
        print('PASS '+Hizkuntza+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if fitxategi_transferitu_konexio:
            try:fitxategi_transferitu_konexio.close()
            except OSError:pass
        if bezero:bezero.close()
        Prozesua.terminate()
        try:Prozesua.wait(timeout=8)
        except subprocess.TimeoutExpired:Prozesua.kill();Prozesua.wait()
        준비선택기.close();Prozesua.stdout.close();(neurria_datuak/(Hizkuntza+'-serial.log')).write_bytes(대화기록)


def Exekutatu_2():
    neurria_datuak=Project_erro/'build/verification/examples';neurria_datuak.mkdir(parents=True,exist_ok=True)
    balidazio_txosten={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_erro/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with atzeko_planoko_eguneratze_Zerbitzariak() as atzeko_planoko_eguneratze_zerbitzari_sarrera:
            for Hizkuntza in ('java','c','python'):
                test_언어(Hizkuntza,atzeko_planoko_eguneratze_zerbitzari_sarrera,neurria_datuak);balidazio_txosten['languages'].append(Hizkuntza)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert atzeko_planoko_eguneratze_zerbitzari_sarrera.수신됨==[(Kategoria_balio,datuak.encode()) for Kategoria_balio,datuak in 예상결과],atzeko_planoko_eguneratze_zerbitzari_sarrera.수신됨
            balidazio_txosten['host_network_payloads']=[{'protocol':Kategoria_balio,'text':datuak.decode()} for Kategoria_balio,datuak in atzeko_planoko_eguneratze_zerbitzari_sarrera.수신됨]
        balidazio_txosten.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(neurria_datuak/'report.json').write_text(json.dumps(balidazio_txosten,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Exekutatu_2()
