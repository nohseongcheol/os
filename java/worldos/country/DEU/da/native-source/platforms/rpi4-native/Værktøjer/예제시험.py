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
from desktop_Visning import EKSAKT_VÆRDI
from 예제되돌림서버 import ekko_Servere
from Udfør_kommando import To_do_rod


def test_Sprog(Sprog,ekko_server_post,KR_data):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));filoverførsel_portnummer=임시자원.getsockname()[1]
    Proces=subprocess.Popen(['python3',str(To_do_rod/'Værktøjer/Udfør_kommando.py'),'--desktop','--network','--port','0','--ftp-port',str(filoverførsel_portnummer)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    selektor=selectors.DefaultSelector();selektor.register(Proces.stdout,selectors.EVENT_READ)
    afskrift=bytearray();klient=None;filoverførsel_forbindelse=None
    def modtage_mail(mærke,Kør_2=0):
        afslutte_et_opkald_FORSKYDNING=time.monotonic()+60
        while mærke not in afskrift[Kør_2:]:
            if time.monotonic()>afslutte_et_opkald_FORSKYDNING or Proces.poll() is not None:raise AssertionError(afskrift[Kør_2:].decode('utf-8','replace'))
            for 누름값,_ in selektor.select(.1):
                data=누름값.fileobj.read(65536)
                if data:afskrift.extend(data)
        return afskrift[Kør_2:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(symbol_VÆRDI,누르는중=True):klient.sendall(struct.pack('>BBHI',4,int(누르는중),0,symbol_VÆRDI))
    def START_FORSKYDNING(Linje):
        Kør_2=len(afskrift)
        for tegnkode in Linje+'\n':
            symbol_VÆRDI=0xff0d if tegnkode=='\n' else ord(tegnkode) if ord(tegnkode)<256 else 0x1000000|ord(tegnkode)
            누름값(symbol_VÆRDI);누름값(symbol_VÆRDI,False)
        return Kør_2
    def Shell(Linje):return modtage_mail(b'jkoros-native> ',START_FORSKYDNING(Linje))
    def Udfør_kommando(Linje,예상결과):
        Tekst=Shell(Linje);assert 예상결과 in Tekst and 'exit 0' in Tekst,(Linje,Tekst)
        return Tekst
    def 화소들():
        klient.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            område_VÆRDI=EKSAKT_VÆRDI(klient,1)[0]
            if område_VÆRDI==2:continue
            if område_VÆRDI==3:
                vare_TÆL=struct.unpack('>I',EKSAKT_VÆRDI(klient,7)[3:])[0];EKSAKT_VÆRDI(klient,vare_TÆL);continue
            assert område_VÆRDI==0,område_VÆRDI
            post_TÆL_8f7753a1=struct.unpack('>H',EKSAKT_VÆRDI(klient,3)[1:])[0]
            for _ in range(post_TÆL_8f7753a1):
                X_koordinat,Y_koordinat,너비값,높이값,tegnsæt=struct.unpack('>HHHHi',EKSAKT_VÆRDI(klient,12));assert tegnsæt==0,tegnsæt
                data=EKSAKT_VÆRDI(klient,너비값*높이값*4)
                for post_placere in range(높이값):
                    for KOLONNE_placere in range(너비값):
                        원본자료=(post_placere*너비값+KOLONNE_placere)*4;mål=((Y_koordinat+post_placere)*640+X_koordinat+KOLONNE_placere)*3
                        빛삼원색[mål:mål+3]=bytes((data[원본자료+2],data[원본자료+1],data[원본자료]))
            if post_TÆL_8f7753a1:return 빛삼원색
    try:
        modtage_mail(b'TERMINAL READY');modtage_mail(b'jkoros-native> ',afskrift.rfind(b'TERMINAL READY'))
        portnummer=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',afskrift).group(1))
        klient=socket.create_connection(('127.0.0.1',portnummer),timeout=10)
        assert EKSAKT_VÆRDI(klient,12)==b'RFB 003.008\n';klient.sendall(b'RFB 003.008\n')
        assert 1 in EKSAKT_VÆRDI(klient,EKSAKT_VÆRDI(klient,1)[0]);klient.sendall(b'\x01');assert EKSAKT_VÆRDI(klient,4)==b'\0'*4
        klient.sendall(b'\x01');초기값=EKSAKT_VÆRDI(klient,24);EKSAKT_VÆRDI(klient,struct.unpack('>I',초기값[20:])[0])
        klient.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        klient.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in Shell('ftpd start')
        filoverførsel_forbindelse=ftplib.FTP();filoverførsel_forbindelse.encoding='utf-8';filoverførsel_forbindelse.connect('127.0.0.1',filoverførsel_portnummer,timeout=20);filoverførsel_forbindelse.login()
        nyttedata_data=('GUI와 FTP 동시 brug_VÆRDI '+Sprog+' 😀\n').encode()
        filoverførsel_forbindelse.storbinary('STOR 함께.txt',io.BytesIO(nyttedata_data))
        assert nyttedata_data.decode().strip() in Shell('cat /함께.txt')
        MODTAGET_VED_UDLØB_TÆL=bytearray();filoverførsel_forbindelse.retrbinary('RETR 함께.txt',MODTAGET_VED_UDLØB_TÆL.extend);assert MODTAGET_VED_UDLØB_TÆL==nyttedata_data;filoverførsel_forbindelse.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        maile_Liste=Shell('ls /example')
        assert all(Navn in maile_Liste for Navn in ('java/','c/','python/','README.md')),maile_Liste
        if Sprog=='java':
            bundt_manifest=json.loads((To_do_rod/'build/examples/manifest.json').read_text())
            for Sti,indgangspunkt in bundt_manifest.items():
                Shell('cp '+Sti+' /example-check.bin')
                Indhold_VÆRDI=bytearray();filoverførsel_forbindelse.retrbinary('RETR example-check.bin',Indhold_VÆRDI.extend)
                assert len(Indhold_VÆRDI)==indgangspunkt['bytes'] and hashlib.sha256(Indhold_VÆRDI).hexdigest()==indgangspunkt['sha256'],Sti
            filoverførsel_forbindelse.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            binær=bytes(range(256))*64
            filoverførsel_forbindelse.storbinary('STOR boundary.bin',io.BytesIO(binær))
            Indhold_VÆRDI=bytearray();filoverførsel_forbindelse.retrbinary('RETR boundary.bin',Indhold_VÆRDI.extend)
            assert Indhold_VÆRDI==binær and 'boundary.bin' in filoverførsel_forbindelse.nlst()
            Shell('cp /boundary.bin /boundary-copy.bin')
            Indhold_VÆRDI=bytearray();filoverførsel_forbindelse.retrbinary('RETR boundary-copy.bin',Indhold_VÆRDI.extend)
            assert Indhold_VÆRDI==binær
            filoverførsel_forbindelse.delete('boundary.bin');filoverførsel_forbindelse.delete('boundary-copy.bin')
        assert 'Uddataeksempel' in Shell('ls /example/'+Sprog)
        Shell('cd /example/'+Sprog)
        navn_tabel={'java':'JAVA','c':'C','python':'PYTHON'}[Sprog]
        예상파일=navn_tabel+' Fil: 한글 data 😀\n'
        if Sprog=='java':
            Udfør_kommando('javac Uddataeksempel.java','Compiled:');Udfør_kommando('java Uddataeksempel','JAVA Udgang: 안녕하세요 😀')
            Udfør_kommando('javac Fileksempel.java','Compiled:');Udfør_kommando('java Fileksempel',예상파일)
            Udfør_kommando('java Netværkseksempel {} {}'.format(ekko_server_post.TCP_port,ekko_server_post.UDP_port),'JAVA 네트워크 bekræfte: TCP UDP 한글')
            grafik_kommando='java Tegneeksempel'
        elif Sprog=='c':
            for Navn,전달값,예상결과 in [('Udgang','', 'C Udgang: 안녕하세요 😀'),('Fil','',예상파일),
                    ('네트워크',' '+str(ekko_server_post.UDP_port),'C 네트워크 bekræfte: UDP 한글')]:
                Udfør_kommando('cc '+Navn+'예제.c -o Udfør_kommando','Compiled native ARM64 ELF:')
                Udfør_kommando('./Udfør_kommando'+전달값,예상결과)
            Udfør_kommando('cc Tegneeksempel.c -o Udfør_kommando','Compiled native ARM64 ELF:');grafik_kommando='./Udfør_kommando'
        else:
            for Navn,전달값,예상결과 in [('Udgang','','PYTHON Udgang: 안녕하세요 😀'),('Fil','',예상파일),
                    ('네트워크',' '+str(ekko_server_post.UDP_port),'PYTHON 네트워크 bekræfte: UDP 한글')]:
                Udfør_kommando('python '+Navn+'예제.py'+전달값,예상결과)
            grafik_kommando='python Tegneeksempel.py'
        START_tegning=START_FORSKYDNING(grafik_kommando)
        Tekst=modtage_mail('그림을 확인한 BACK_VÆRDI Enter를 누르세요.\r\n'.encode(),START_tegning)
        assert navn_tabel+' 그래픽: 빨강 초록 파랑' in Tekst and 'exit 0' not in Tekst,Tekst
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        filoverførsel_forbindelse.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        MODTAGET_VED_UDLØB_TÆL=bytearray();filoverførsel_forbindelse.retrbinary('RETR 도중.txt',MODTAGET_VED_UDLØB_TÆL.extend);assert MODTAGET_VED_UDLØB_TÆL==b'FTP DURING GRAPHICS';filoverførsel_forbindelse.delete('도중.txt')
        빛삼원색=화소들()
        for Y_koordinat,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            FORSKYDNING_VÆRDI=(Y_koordinat*640+610)*3;assert tuple(빛삼원색[FORSKYDNING_VÆRDI:FORSKYDNING_VÆRDI+3])==색상,(Sprog,Y_koordinat,tuple(빛삼원색[FORSKYDNING_VÆRDI:FORSKYDNING_VÆRDI+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(KR_data/(Sprog+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in modtage_mail(b'jkoros-native> ',START_tegning)
        if Sprog=='java':
            START_vindue=START_FORSKYDNING('java Vindueseksempel')
            modtage_mail('GUI 예제 Tilrettelæg: Vindueseksempel'.encode(),START_vindue)
            def klik_VÆRDI(가로,Lodret_placere):
                for knap in (1,0):klient.sendall(struct.pack('>BBHH',5,knap,가로,Lodret_placere))
            time.sleep(.3)
            Forrige_Image=Image.frombytes('RGB',(640,480),bytes(화소들()))
            klik_VÆRDI(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for tegn_VÆRDI in '한글':누름값(0x1000000|ord(tegn_VÆRDI));누름값(0x1000000|ord(tegn_VÆRDI),False)
            for gentagelse_TÆL in (1,2):
                Kør_2=len(afskrift);klik_VÆRDI(180,242)
                modtage_mail(('GUI 인사: 안녕하세요, 한글님! ('+str(gentagelse_TÆL)+')').encode(),Kør_2)
            time.sleep(.3)
            vindue_tegning=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert Forrige_Image.crop((110,272,530,300)).tobytes()!=vindue_tegning.crop((110,272,530,300)).tobytes()
            vindue_tegning.save(str(KR_data/'java-swing.png'))
            Kør_2=len(afskrift);klik_VÆRDI(535,105)
            assert 'exit 0' in modtage_mail(b'jkoros-native> ',Kør_2)
        # Download the guest-created bytes through FTP in the same GUI VM.
        fil_post_navn={'java':'java.txt','c':'c.txt','python':'python.txt'}[Sprog]
        Shell('cp '+fil_post_navn+' /bekræfte_5fb2b747.txt')
        MODTAGET_VED_UDLØB_TÆL=bytearray();filoverførsel_forbindelse.retrbinary('RETR bekræfte_5fb2b747.txt',MODTAGET_VED_UDLØB_TÆL.extend);assert MODTAGET_VED_UDLØB_TÆL==예상파일.encode()
        Shell('echo preserved > Uddataeksempel.'+('py' if Sprog=='python' else Sprog))
        assert 'EXAMPLES READY' in Shell('example '+Sprog)
        assert '\npreserved\n' in Shell('cat Uddataeksempel.'+('py' if Sprog=='python' else Sprog))
        assert '한/nul_operand tast_VÆRDI, Shift+Space 또는 F9' in Shell('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in Shell('echo GUI NETWORK TOGETHER')
        filoverførsel_forbindelse.quit();filoverførsel_forbindelse=None;assert 'FTP stopped' in Shell('ftpd stop')
        print('PASS '+Sprog+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if filoverførsel_forbindelse:
            try:filoverførsel_forbindelse.close()
            except OSError:pass
        if klient:klient.close()
        Proces.terminate()
        try:Proces.wait(timeout=8)
        except subprocess.TimeoutExpired:Proces.kill();Proces.wait()
        selektor.close();Proces.stdout.close();(KR_data/(Sprog+'-serial.log')).write_bytes(afskrift)


def Kør_2():
    KR_data=To_do_rod/'build/verification/examples';KR_data.mkdir(parents=True,exist_ok=True)
    validering_rapport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((To_do_rod/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with ekko_Servere() as ekko_server_post:
            for Sprog in ('java','c','python'):
                test_Sprog(Sprog,ekko_server_post,KR_data);validering_rapport['languages'].append(Sprog)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert ekko_server_post.수신됨==[(område_VÆRDI,data.encode()) for område_VÆRDI,data in 예상결과],ekko_server_post.수신됨
            validering_rapport['host_network_payloads']=[{'protocol':område_VÆRDI,'text':data.decode()} for område_VÆRDI,data in ekko_server_post.수신됨]
        validering_rapport.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(KR_data/'report.json').write_text(json.dumps(validering_rapport,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Kør_2()
