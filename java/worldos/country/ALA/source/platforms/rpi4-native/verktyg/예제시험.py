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
from Dator_vy import EXAKT_värde
from 예제되돌림서버 import UppdateraSkärm_Servrar
from köra_kommando import åtgärd_rot


def test_Språk(Språk,UppdateraSkärm_server_post,KR_data):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));filöverföring_portnummer=임시자원.getsockname()[1]
    Process=subprocess.Popen(['python3',str(åtgärd_rot/'verktyg/köra_kommando.py'),'--desktop','--network','--port','0','--ftp-port',str(filöverföring_portnummer)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    väljare=selectors.DefaultSelector();väljare.register(Process.stdout,selectors.EVENT_READ)
    avskrift=bytearray();klient=None;filöverföring_kontakt=None
    def få_dokument(markör_8b722c5f,Kör=0):
        avsluta_FÖRSKJUTNING=time.monotonic()+60
        while markör_8b722c5f not in avskrift[Kör:]:
            if time.monotonic()>avsluta_FÖRSKJUTNING or Process.poll() is not None:raise AssertionError(avskrift[Kör:].decode('utf-8','replace'))
            for 누름값,_ in väljare.select(.1):
                data=누름값.fileobj.read(65536)
                if data:avskrift.extend(data)
        return avskrift[Kör:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(symbol_värde,누르는중=True):klient.sendall(struct.pack('>BBHI',4,int(누르는중),0,symbol_värde))
    def START_FÖRSKJUTNING(inmatningsrad):
        Kör=len(avskrift)
        for kodpunkt in inmatningsrad+'\n':
            symbol_värde=0xff0d if kodpunkt=='\n' else ord(kodpunkt) if ord(kodpunkt)<256 else 0x1000000|ord(kodpunkt)
            누름값(symbol_värde);누름값(symbol_värde,False)
        return Kör
    def Shell(inmatningsrad):return få_dokument(b'jkoros-native> ',START_FÖRSKJUTNING(inmatningsrad))
    def köra_kommando(inmatningsrad,예상결과):
        text=Shell(inmatningsrad);assert 예상결과 in text and 'exit 0' in text,(inmatningsrad,text)
        return text
    def 화소들():
        klient.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            område_värde=EXAKT_värde(klient,1)[0]
            if område_värde==2:continue
            if område_värde==3:
                objekt_ANTAL=struct.unpack('>I',EXAKT_värde(klient,7)[3:])[0];EXAKT_värde(klient,objekt_ANTAL);continue
            assert område_värde==0,område_värde
            post_ANTAL=struct.unpack('>H',EXAKT_värde(klient,3)[1:])[0]
            for _ in range(post_ANTAL):
                x_koordinat,Y_koordinat,너비값,높이값,teckenuppsättning=struct.unpack('>HHHHi',EXAKT_värde(klient,12));assert teckenuppsättning==0,teckenuppsättning
                data=EXAKT_värde(klient,너비값*높이값*4)
                for RAD_placera in range(높이값):
                    for spalt_placera in range(너비값):
                        원본자료=(RAD_placera*너비값+spalt_placera)*4;mål=((Y_koordinat+RAD_placera)*640+x_koordinat+spalt_placera)*3
                        빛삼원색[mål:mål+3]=bytes((data[원본자료+2],data[원본자료+1],data[원본자료]))
            if post_ANTAL:return 빛삼원색
    try:
        få_dokument(b'TERMINAL READY');få_dokument(b'jkoros-native> ',avskrift.rfind(b'TERMINAL READY'))
        portnummer=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',avskrift).group(1))
        klient=socket.create_connection(('127.0.0.1',portnummer),timeout=10)
        assert EXAKT_värde(klient,12)==b'RFB 003.008\n';klient.sendall(b'RFB 003.008\n')
        assert 1 in EXAKT_värde(klient,EXAKT_värde(klient,1)[0]);klient.sendall(b'\x01');assert EXAKT_värde(klient,4)==b'\0'*4
        klient.sendall(b'\x01');초기값=EXAKT_värde(klient,24);EXAKT_värde(klient,struct.unpack('>I',초기값[20:])[0])
        klient.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        klient.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in Shell('ftpd start')
        filöverföring_kontakt=ftplib.FTP();filöverföring_kontakt.encoding='utf-8';filöverföring_kontakt.connect('127.0.0.1',filöverföring_portnummer,timeout=20);filöverföring_kontakt.login()
        nyttolast_data=('GUI와 FTP 동시 använda_värde '+Språk+' 😀\n').encode()
        filöverföring_kontakt.storbinary('STOR 함께.txt',io.BytesIO(nyttolast_data))
        assert nyttolast_data.decode().strip() in Shell('cat /함께.txt')
        BELOPP_ANTAL=bytearray();filöverföring_kontakt.retrbinary('RETR 함께.txt',BELOPP_ANTAL.extend);assert BELOPP_ANTAL==nyttolast_data;filöverföring_kontakt.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        skicka_ange=Shell('ls /example')
        assert all(Namn in skicka_ange for Namn in ('java/','c/','python/','README.md')),skicka_ange
        if Språk=='java':
            bunt_manifest=json.loads((åtgärd_rot/'build/examples/manifest.json').read_text())
            for sökväg_2,startpunkt in bunt_manifest.items():
                Shell('cp '+sökväg_2+' /example-check.bin')
                Innehåll_värde=bytearray();filöverföring_kontakt.retrbinary('RETR example-check.bin',Innehåll_värde.extend)
                assert len(Innehåll_värde)==startpunkt['bytes'] and hashlib.sha256(Innehåll_värde).hexdigest()==startpunkt['sha256'],sökväg_2
            filöverföring_kontakt.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            binär=bytes(range(256))*64
            filöverföring_kontakt.storbinary('STOR boundary.bin',io.BytesIO(binär))
            Innehåll_värde=bytearray();filöverföring_kontakt.retrbinary('RETR boundary.bin',Innehåll_värde.extend)
            assert Innehåll_värde==binär and 'boundary.bin' in filöverföring_kontakt.nlst()
            Shell('cp /boundary.bin /boundary-copy.bin')
            Innehåll_värde=bytearray();filöverföring_kontakt.retrbinary('RETR boundary-copy.bin',Innehåll_värde.extend)
            assert Innehåll_värde==binär
            filöverföring_kontakt.delete('boundary.bin');filöverföring_kontakt.delete('boundary-copy.bin')
        assert 'Utdataexempel' in Shell('ls /example/'+Språk)
        Shell('cd /example/'+Språk)
        namn_tabell={'java':'JAVA','c':'C','python':'PYTHON'}[Språk]
        예상파일=namn_tabell+' filnamn: 한글 data 😀\n'
        if Språk=='java':
            köra_kommando('javac Utdataexempel.java','Compiled:');köra_kommando('java Utdataexempel','JAVA utmatningsposition: 안녕하세요 😀')
            köra_kommando('javac Filexempel.java','Compiled:');köra_kommando('java Filexempel',예상파일)
            köra_kommando('java Nätverksexempel {} {}'.format(UppdateraSkärm_server_post.TCP_port,UppdateraSkärm_server_post.UDP_port),'JAVA 네트워크 verifiera: TCP UDP 한글')
            grafik_kommando='java Ritexempel'
        elif Språk=='c':
            for Namn,전달값,예상결과 in [('utmatningsposition','', 'C utmatningsposition: 안녕하세요 😀'),('filnamn','',예상파일),
                    ('네트워크',' '+str(UppdateraSkärm_server_post.UDP_port),'C 네트워크 verifiera: UDP 한글')]:
                köra_kommando('cc '+Namn+'예제.c -o köra_kommando','Compiled native ARM64 ELF:')
                köra_kommando('./köra_kommando'+전달값,예상결과)
            köra_kommando('cc Ritexempel.c -o köra_kommando','Compiled native ARM64 ELF:');grafik_kommando='./köra_kommando'
        else:
            for Namn,전달값,예상결과 in [('utmatningsposition','','PYTHON utmatningsposition: 안녕하세요 😀'),('filnamn','',예상파일),
                    ('네트워크',' '+str(UppdateraSkärm_server_post.UDP_port),'PYTHON 네트워크 verifiera: UDP 한글')]:
                köra_kommando('python '+Namn+'예제.py'+전달값,예상결과)
            grafik_kommando='python Ritexempel.py'
        START_ritning=START_FÖRSKJUTNING(grafik_kommando)
        text=få_dokument('그림을 확인한 BACK_värde Enter를 누르세요.\r\n'.encode(),START_ritning)
        assert namn_tabell+' 그래픽: 빨강 초록 파랑' in text and 'exit 0' not in text,text
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        filöverföring_kontakt.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        BELOPP_ANTAL=bytearray();filöverföring_kontakt.retrbinary('RETR 도중.txt',BELOPP_ANTAL.extend);assert BELOPP_ANTAL==b'FTP DURING GRAPHICS';filöverföring_kontakt.delete('도중.txt')
        빛삼원색=화소들()
        for Y_koordinat,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            FÖRSKJUTNING_värde=(Y_koordinat*640+610)*3;assert tuple(빛삼원색[FÖRSKJUTNING_värde:FÖRSKJUTNING_värde+3])==색상,(Språk,Y_koordinat,tuple(빛삼원색[FÖRSKJUTNING_värde:FÖRSKJUTNING_värde+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(KR_data/(Språk+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in få_dokument(b'jkoros-native> ',START_ritning)
        if Språk=='java':
            START_fönster=START_FÖRSKJUTNING('java Fönsterexempel')
            få_dokument('GUI 예제 Förbereda: Fönsterexempel'.encode(),START_fönster)
            def klick_värde(가로,bransch_placera):
                for knapp in (1,0):klient.sendall(struct.pack('>BBHH',5,knapp,가로,bransch_placera))
            time.sleep(.3)
            Föregående_BILD=Image.frombytes('RGB',(640,480),bytes(화소들()))
            klick_värde(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for tecken_värde in '한글':누름값(0x1000000|ord(tecken_värde));누름값(0x1000000|ord(tecken_värde),False)
            for repetition_ANTAL in (1,2):
                Kör=len(avskrift);klick_värde(180,242)
                få_dokument(('GUI 인사: 안녕하세요, 한글님! ('+str(repetition_ANTAL)+')').encode(),Kör)
            time.sleep(.3)
            fönster_ritning=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert Föregående_BILD.crop((110,272,530,300)).tobytes()!=fönster_ritning.crop((110,272,530,300)).tobytes()
            fönster_ritning.save(str(KR_data/'java-swing.png'))
            Kör=len(avskrift);klick_värde(535,105)
            assert 'exit 0' in få_dokument(b'jkoros-native> ',Kör)
        # Download the guest-created bytes through FTP in the same GUI VM.
        fil_post_namn={'java':'java.txt','c':'c.txt','python':'python.txt'}[Språk]
        Shell('cp '+fil_post_namn+' /validera.txt')
        BELOPP_ANTAL=bytearray();filöverföring_kontakt.retrbinary('RETR validera.txt',BELOPP_ANTAL.extend);assert BELOPP_ANTAL==예상파일.encode()
        Shell('echo preserved > Utdataexempel.'+('py' if Språk=='python' else Språk))
        assert 'EXAMPLES READY' in Shell('example '+Språk)
        assert '\npreserved\n' in Shell('cat Utdataexempel.'+('py' if Språk=='python' else Språk))
        assert '한/noll_operand Nyckel_värde, Shift+Space 또는 F9' in Shell('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in Shell('echo GUI NETWORK TOGETHER')
        filöverföring_kontakt.quit();filöverföring_kontakt=None;assert 'FTP stopped' in Shell('ftpd stop')
        print('PASS '+Språk+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if filöverföring_kontakt:
            try:filöverföring_kontakt.close()
            except OSError:pass
        if klient:klient.close()
        Process.terminate()
        try:Process.wait(timeout=8)
        except subprocess.TimeoutExpired:Process.kill();Process.wait()
        väljare.close();Process.stdout.close();(KR_data/(Språk+'-serial.log')).write_bytes(avskrift)


def Kör():
    KR_data=åtgärd_rot/'build/verification/examples';KR_data.mkdir(parents=True,exist_ok=True)
    validering_Rapport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((åtgärd_rot/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with UppdateraSkärm_Servrar() as UppdateraSkärm_server_post:
            for Språk in ('java','c','python'):
                test_Språk(Språk,UppdateraSkärm_server_post,KR_data);validering_Rapport['languages'].append(Språk)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert UppdateraSkärm_server_post.수신됨==[(område_värde,data.encode()) for område_värde,data in 예상결과],UppdateraSkärm_server_post.수신됨
            validering_Rapport['host_network_payloads']=[{'protocol':område_värde,'text':data.decode()} for område_värde,data in UppdateraSkärm_server_post.수신됨]
        validering_Rapport.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(KR_data/'report.json').write_text(json.dumps(validering_Rapport,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Kör()
