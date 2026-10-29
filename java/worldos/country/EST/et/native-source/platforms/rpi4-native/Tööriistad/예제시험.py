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
from töölaud_Kuva import EXACT_VALUE
from 예제되돌림서버 import kaja_Serverid
from Täida_käsk import Project_juur


def test_언어(Keeled,kaja_server_kirje,näitaja_andmed):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));failiedastus_pordinumber=임시자원.getsockname()[1]
    Protsess=subprocess.Popen(['python3',str(Project_juur/'Tööriistad/Täida_käsk.py'),'--desktop','--network','--port','0','--ftp-port',str(failiedastus_pordinumber)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    valija=selectors.DefaultSelector();valija.register(Protsess.stdout,selectors.EVENT_READ)
    transkriptsioon=bytearray();klient=None;failiedastus_ühendus=None
    def saama_meil(marker,Käivita_2=0):
        lõpeta_kõne_nihe=time.monotonic()+60
        while marker not in transkriptsioon[Käivita_2:]:
            if time.monotonic()>lõpeta_kõne_nihe or Protsess.poll() is not None:raise AssertionError(transkriptsioon[Käivita_2:].decode('utf-8','replace'))
            for 누름값,_ in valija.select(.1):
                andmed=누름값.fileobj.read(65536)
                if andmed:transkriptsioon.extend(andmed)
        return transkriptsioon[Käivita_2:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(sümbol_VALUE,누르는중=True):klient.sendall(struct.pack('>BBHI',4,int(누르는중),0,sümbol_VALUE))
    def START_nihe(Joon):
        Käivita_2=len(transkriptsioon)
        for koodipunkt in Joon+'\n':
            sümbol_VALUE=0xff0d if koodipunkt=='\n' else ord(koodipunkt) if ord(koodipunkt)<256 else 0x1000000|ord(koodipunkt)
            누름값(sümbol_VALUE);누름값(sümbol_VALUE,False)
        return Käivita_2
    def kest(Joon):return saama_meil(b'jkoros-native> ',START_nihe(Joon))
    def Täida_käsk(Joon,예상결과):
        Tekst=kest(Joon);assert 예상결과 in Tekst and 'exit 0' in Tekst,(Joon,Tekst)
        return Tekst
    def 화소들():
        klient.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            ala_VALUE=EXACT_VALUE(klient,1)[0]
            if ala_VALUE==2:continue
            if ala_VALUE==3:
                kaup_COUNT=struct.unpack('>I',EXACT_VALUE(klient,7)[3:])[0];EXACT_VALUE(klient,kaup_COUNT);continue
            assert ala_VALUE==0,ala_VALUE
            kirje_COUNT=struct.unpack('>H',EXACT_VALUE(klient,3)[1:])[0]
            for _ in range(kirje_COUNT):
                가로좌표,세로좌표,너비값,높이값,märgistik=struct.unpack('>HHHHi',EXACT_VALUE(klient,12));assert märgistik==0,märgistik
                andmed=EXACT_VALUE(klient,너비값*높이값*4)
                for ROW_ametikoht in range(높이값):
                    for veerg_ametikoht in range(너비값):
                        원본자료=(ROW_ametikoht*너비값+veerg_ametikoht)*4;siht=((세로좌표+ROW_ametikoht)*640+가로좌표+veerg_ametikoht)*3
                        빛삼원색[siht:siht+3]=bytes((andmed[원본자료+2],andmed[원본자료+1],andmed[원본자료]))
            if kirje_COUNT:return 빛삼원색
    try:
        saama_meil(b'TERMINAL READY');saama_meil(b'jkoros-native> ',transkriptsioon.rfind(b'TERMINAL READY'))
        pordinumber=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',transkriptsioon).group(1))
        klient=socket.create_connection(('127.0.0.1',pordinumber),timeout=10)
        assert EXACT_VALUE(klient,12)==b'RFB 003.008\n';klient.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(klient,EXACT_VALUE(klient,1)[0]);klient.sendall(b'\x01');assert EXACT_VALUE(klient,4)==b'\0'*4
        klient.sendall(b'\x01');초기값=EXACT_VALUE(klient,24);EXACT_VALUE(klient,struct.unpack('>I',초기값[20:])[0])
        klient.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        klient.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in kest('ftpd start')
        failiedastus_ühendus=ftplib.FTP();failiedastus_ühendus.encoding='utf-8';failiedastus_ühendus.connect('127.0.0.1',failiedastus_pordinumber,timeout=20);failiedastus_ühendus.login()
        last_andmed=('GUI와 FTP 동시 kasutus_VALUE '+Keeled+' 😀\n').encode()
        failiedastus_ühendus.storbinary('STOR 함께.txt',io.BytesIO(last_andmed))
        assert last_andmed.decode().strip() in kest('cat /함께.txt')
        RECEIVED_COUNT=bytearray();failiedastus_ühendus.retrbinary('RETR 함께.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==last_andmed;failiedastus_ühendus.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        saatma_Loend=kest('ls /example')
        assert all(Nimi_2 in saatma_Loend for Nimi_2 in ('java/','c/','python/','README.md')),saatma_Loend
        if Keeled=='java':
            꾸러미명세=json.loads((Project_juur/'build/examples/manifest.json').read_text())
            for RADA,kirje_p in 꾸러미명세.items():
                kest('cp '+RADA+' /example-check.bin')
                Sisu_VALUE=bytearray();failiedastus_ühendus.retrbinary('RETR example-check.bin',Sisu_VALUE.extend)
                assert len(Sisu_VALUE)==kirje_p['bytes'] and hashlib.sha256(Sisu_VALUE).hexdigest()==kirje_p['sha256'],RADA
            failiedastus_ühendus.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            binaarne=bytes(range(256))*64
            failiedastus_ühendus.storbinary('STOR boundary.bin',io.BytesIO(binaarne))
            Sisu_VALUE=bytearray();failiedastus_ühendus.retrbinary('RETR boundary.bin',Sisu_VALUE.extend)
            assert Sisu_VALUE==binaarne and 'boundary.bin' in failiedastus_ühendus.nlst()
            kest('cp /boundary.bin /boundary-copy.bin')
            Sisu_VALUE=bytearray();failiedastus_ühendus.retrbinary('RETR boundary-copy.bin',Sisu_VALUE.extend)
            assert Sisu_VALUE==binaarne
            failiedastus_ühendus.delete('boundary.bin');failiedastus_ühendus.delete('boundary-copy.bin')
        assert 'VäljundiNäide' in kest('ls /example/'+Keeled)
        kest('cd /example/'+Keeled)
        nimetus_tabel={'java':'JAVA','c':'C','python':'PYTHON'}[Keeled]
        예상파일=nimetus_tabel+' Fail: 한글 andmed 😀\n'
        if Keeled=='java':
            Täida_käsk('javac VäljundiNäide.java','Compiled:');Täida_käsk('java VäljundiNäide','JAVA Väljund: 안녕하세요 😀')
            Täida_käsk('javac FailiNäide.java','Compiled:');Täida_käsk('java FailiNäide',예상파일)
            Täida_käsk('java VõrguNäide {} {}'.format(kaja_server_kirje.TCP_port,kaja_server_kirje.UDP_port),'JAVA 네트워크 kinnitama: TCP UDP 한글')
            graafika_käsk='java JooniseNäide'
        elif Keeled=='c':
            for Nimi_2,전달값,예상결과 in [('Väljund','', 'C Väljund: 안녕하세요 😀'),('Fail','',예상파일),
                    ('네트워크',' '+str(kaja_server_kirje.UDP_port),'C 네트워크 kinnitama: UDP 한글')]:
                Täida_käsk('cc '+Nimi_2+'예제.c -o Täida_käsk','Compiled native ARM64 ELF:')
                Täida_käsk('./Täida_käsk'+전달값,예상결과)
            Täida_käsk('cc JooniseNäide.c -o Täida_käsk','Compiled native ARM64 ELF:');graafika_käsk='./Täida_käsk'
        else:
            for Nimi_2,전달값,예상결과 in [('Väljund','','PYTHON Väljund: 안녕하세요 😀'),('Fail','',예상파일),
                    ('네트워크',' '+str(kaja_server_kirje.UDP_port),'PYTHON 네트워크 kinnitama: UDP 한글')]:
                Täida_käsk('python '+Nimi_2+'예제.py'+전달값,예상결과)
            graafika_käsk='python JooniseNäide.py'
        START_joonis=START_nihe(graafika_käsk)
        Tekst=saama_meil('그림을 확인한 Tagasi_VALUE Enter를 누르세요.\r\n'.encode(),START_joonis)
        assert nimetus_tabel+' 그래픽: 빨강 초록 파랑' in Tekst and 'exit 0' not in Tekst,Tekst
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        failiedastus_ühendus.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        RECEIVED_COUNT=bytearray();failiedastus_ühendus.retrbinary('RETR 도중.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==b'FTP DURING GRAPHICS';failiedastus_ühendus.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            nihe_VALUE=(세로좌표*640+610)*3;assert tuple(빛삼원색[nihe_VALUE:nihe_VALUE+3])==색상,(Keeled,세로좌표,tuple(빛삼원색[nihe_VALUE:nihe_VALUE+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(näitaja_andmed/(Keeled+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in saama_meil(b'jkoros-native> ',START_joonis)
        if Keeled=='java':
            START_aken=START_nihe('java AknaNäide')
            saama_meil('GUI 예제 Ettevalmistamine: AknaNäide'.encode(),START_aken)
            def klõps_VALUE(가로,vertikaal_ametikoht):
                for nupp in (1,0):klient.sendall(struct.pack('>BBHH',5,nupp,가로,vertikaal_ametikoht))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            klõps_VALUE(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for märk_VALUE in '한글':누름값(0x1000000|ord(märk_VALUE));누름값(0x1000000|ord(märk_VALUE),False)
            for 횟수 in (1,2):
                Käivita_2=len(transkriptsioon);klõps_VALUE(180,242)
                saama_meil(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Käivita_2)
            time.sleep(.3)
            aken_joonis=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=aken_joonis.crop((110,272,530,300)).tobytes()
            aken_joonis.save(str(näitaja_andmed/'java-swing.png'))
            Käivita_2=len(transkriptsioon);klõps_VALUE(535,105)
            assert 'exit 0' in saama_meil(b'jkoros-native> ',Käivita_2)
        # Download the guest-created bytes through FTP in the same GUI VM.
        Fail_kirje_nimetus={'java':'java.txt','c':'c.txt','python':'python.txt'}[Keeled]
        kest('cp '+Fail_kirje_nimetus+' /valideerima.txt')
        RECEIVED_COUNT=bytearray();failiedastus_ühendus.retrbinary('RETR valideerima.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==예상파일.encode()
        kest('echo preserved > VäljundiNäide.'+('py' if Keeled=='python' else Keeled))
        assert 'EXAMPLES READY' in kest('example '+Keeled)
        assert '\npreserved\n' in kest('cat VäljundiNäide.'+('py' if Keeled=='python' else Keeled))
        assert '한/null_operand Võti_VALUE, Shift+Space 또는 F9' in kest('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in kest('echo GUI NETWORK TOGETHER')
        failiedastus_ühendus.quit();failiedastus_ühendus=None;assert 'FTP stopped' in kest('ftpd stop')
        print('PASS '+Keeled+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if failiedastus_ühendus:
            try:failiedastus_ühendus.close()
            except OSError:pass
        if klient:klient.close()
        Protsess.terminate()
        try:Protsess.wait(timeout=8)
        except subprocess.TimeoutExpired:Protsess.kill();Protsess.wait()
        valija.close();Protsess.stdout.close();(näitaja_andmed/(Keeled+'-serial.log')).write_bytes(transkriptsioon)


def Käivita_2():
    näitaja_andmed=Project_juur/'build/verification/examples';näitaja_andmed.mkdir(parents=True,exist_ok=True)
    kinnitamine_aruanne={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_juur/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with kaja_Serverid() as kaja_server_kirje:
            for Keeled in ('java','c','python'):
                test_언어(Keeled,kaja_server_kirje,näitaja_andmed);kinnitamine_aruanne['languages'].append(Keeled)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert kaja_server_kirje.수신됨==[(ala_VALUE,andmed.encode()) for ala_VALUE,andmed in 예상결과],kaja_server_kirje.수신됨
            kinnitamine_aruanne['host_network_payloads']=[{'protocol':ala_VALUE,'text':andmed.decode()} for ala_VALUE,andmed in kaja_server_kirje.수신됨]
        kinnitamine_aruanne.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(näitaja_andmed/'report.json').write_text(json.dumps(kinnitamine_aruanne,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Käivita_2()
