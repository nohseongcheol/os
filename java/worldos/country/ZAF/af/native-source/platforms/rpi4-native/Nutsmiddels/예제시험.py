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
from werkskerm_bekyk import EXACT_VALUE
from 예제되돌림서버 import 되돌림서버
from uitvoer_bevel import Project_wortel


def test_언어(Taal,되돌림서버항목,maatreël_data):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    Proses=subprocess.Popen(['python3',str(Project_wortel/'Nutsmiddels/uitvoer_bevel.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    selekteerder=selectors.DefaultSelector();selekteerder.register(Proses.stdout,selectors.EVENT_READ)
    대화기록=bytearray();kliënt=None;lêer_oordra_verbinding=None
    def 수신하기(확인표시,Loop=0):
        beëindig_OFFSET=time.monotonic()+60
        while 확인표시 not in 대화기록[Loop:]:
            if time.monotonic()>beëindig_OFFSET or Proses.poll() is not None:raise AssertionError(대화기록[Loop:].decode('utf-8','replace'))
            for 누름값,_ in selekteerder.select(.1):
                data=누름값.fileobj.read(65536)
                if data:대화기록.extend(data)
        return 대화기록[Loop:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(simbool_VALUE,누르는중=True):kliënt.sendall(struct.pack('>BBHI',4,int(누르는중),0,simbool_VALUE))
    def BEGIN_OFFSET(lyn):
        Loop=len(대화기록)
        for karakterkode in lyn+'\n':
            simbool_VALUE=0xff0d if karakterkode=='\n' else ord(karakterkode) if ord(karakterkode)<256 else 0x1000000|ord(karakterkode)
            누름값(simbool_VALUE);누름값(simbool_VALUE,False)
        return Loop
    def dop(lyn):return 수신하기(b'jkoros-native> ',BEGIN_OFFSET(lyn))
    def uitvoer_bevel(lyn,예상결과):
        Teks=dop(lyn);assert 예상결과 in Teks and 'exit 0' in Teks,(lyn,Teks)
        return Teks
    def 화소들():
        kliënt.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            kategorie_VALUE=EXACT_VALUE(kliënt,1)[0]
            if kategorie_VALUE==2:continue
            if kategorie_VALUE==3:
                item_COUNT=struct.unpack('>I',EXACT_VALUE(kliënt,7)[3:])[0];EXACT_VALUE(kliënt,item_COUNT);continue
            assert kategorie_VALUE==0,kategorie_VALUE
            inskrywing_COUNT=struct.unpack('>H',EXACT_VALUE(kliënt,3)[1:])[0]
            for _ in range(inskrywing_COUNT):
                x_koördinaat,Y_koördinaat,너비값,높이값,karakterstel=struct.unpack('>HHHHi',EXACT_VALUE(kliënt,12));assert karakterstel==0,karakterstel
                data=EXACT_VALUE(kliënt,너비값*높이값*4)
                for ry_plaas in range(높이값):
                    for kolom_plaas in range(너비값):
                        원본자료=(ry_plaas*너비값+kolom_plaas)*4;teiken=((Y_koördinaat+ry_plaas)*640+x_koördinaat+kolom_plaas)*3
                        빛삼원색[teiken:teiken+3]=bytes((data[원본자료+2],data[원본자료+1],data[원본자료]))
            if inskrywing_COUNT:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        kliënt=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert EXACT_VALUE(kliënt,12)==b'RFB 003.008\n';kliënt.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(kliënt,EXACT_VALUE(kliënt,1)[0]);kliënt.sendall(b'\x01');assert EXACT_VALUE(kliënt,4)==b'\0'*4
        kliënt.sendall(b'\x01');초기값=EXACT_VALUE(kliënt,24);EXACT_VALUE(kliënt,struct.unpack('>I',초기값[20:])[0])
        kliënt.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        kliënt.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in dop('ftpd start')
        lêer_oordra_verbinding=ftplib.FTP();lêer_oordra_verbinding.encoding='utf-8';lêer_oordra_verbinding.connect('127.0.0.1',파일전송접속번호,timeout=20);lêer_oordra_verbinding.login()
        lading_data=('GUI와 FTP 동시 사용 '+Taal+' 😀\n').encode()
        lêer_oordra_verbinding.storbinary('STOR 함께.txt',io.BytesIO(lading_data))
        assert lading_data.decode().strip() in dop('cat /함께.txt')
        RECEIVED_COUNT=bytearray();lêer_oordra_verbinding.retrbinary('RETR 함께.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==lading_data;lêer_oordra_verbinding.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        e_pos_Lys=dop('ls /example')
        assert all(Naam in e_pos_Lys for Naam in ('java/','c/','python/','README.md')),e_pos_Lys
        if Taal=='java':
            꾸러미명세=json.loads((Project_wortel/'build/examples/manifest.json').read_text())
            for Pad,inskrywing_p in 꾸러미명세.items():
                dop('cp '+Pad+' /example-check.bin')
                Inhoud_VALUE=bytearray();lêer_oordra_verbinding.retrbinary('RETR example-check.bin',Inhoud_VALUE.extend)
                assert len(Inhoud_VALUE)==inskrywing_p['bytes'] and hashlib.sha256(Inhoud_VALUE).hexdigest()==inskrywing_p['sha256'],Pad
            lêer_oordra_verbinding.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            binêr=bytes(range(256))*64
            lêer_oordra_verbinding.storbinary('STOR boundary.bin',io.BytesIO(binêr))
            Inhoud_VALUE=bytearray();lêer_oordra_verbinding.retrbinary('RETR boundary.bin',Inhoud_VALUE.extend)
            assert Inhoud_VALUE==binêr and 'boundary.bin' in lêer_oordra_verbinding.nlst()
            dop('cp /boundary.bin /boundary-copy.bin')
            Inhoud_VALUE=bytearray();lêer_oordra_verbinding.retrbinary('RETR boundary-copy.bin',Inhoud_VALUE.extend)
            assert Inhoud_VALUE==binêr
            lêer_oordra_verbinding.delete('boundary.bin');lêer_oordra_verbinding.delete('boundary-copy.bin')
        assert '출력예제' in dop('ls /example/'+Taal)
        dop('cd /example/'+Taal)
        naam_tabel={'java':'JAVA','c':'C','python':'PYTHON'}[Taal]
        예상파일=naam_tabel+' Lêer: 한글 data 😀\n'
        if Taal=='java':
            uitvoer_bevel('javac 출력예제.java','Compiled:');uitvoer_bevel('java 출력예제','JAVA Afvoer: 안녕하세요 😀')
            uitvoer_bevel('javac 파일예제.java','Compiled:');uitvoer_bevel('java 파일예제',예상파일)
            uitvoer_bevel('java 네트워크예제 {} {}'.format(되돌림서버항목.TCP_ombou,되돌림서버항목.GDP_Gebruikersdatagramprotokol_ombou),'JAVA 네트워크 verifieer: TCP UDP 한글')
            grafika_bevel='java 그래픽예제'
        elif Taal=='c':
            for Naam,전달값,예상결과 in [('Afvoer','', 'C Afvoer: 안녕하세요 😀'),('Lêer','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.GDP_Gebruikersdatagramprotokol_ombou),'C 네트워크 verifieer: UDP 한글')]:
                uitvoer_bevel('cc '+Naam+'예제.c -o uitvoer_bevel','Compiled native ARM64 ELF:')
                uitvoer_bevel('./uitvoer_bevel'+전달값,예상결과)
            uitvoer_bevel('cc 그래픽예제.c -o uitvoer_bevel','Compiled native ARM64 ELF:');grafika_bevel='./uitvoer_bevel'
        else:
            for Naam,전달값,예상결과 in [('Afvoer','','PYTHON Afvoer: 안녕하세요 😀'),('Lêer','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.GDP_Gebruikersdatagramprotokol_ombou),'PYTHON 네트워크 verifieer: UDP 한글')]:
                uitvoer_bevel('python '+Naam+'예제.py'+전달값,예상결과)
            grafika_bevel='python 그래픽예제.py'
        BEGIN_tekening=BEGIN_OFFSET(grafika_bevel)
        Teks=수신하기('그림을 확인한 TERUG_VALUE Enter를 누르세요.\r\n'.encode(),BEGIN_tekening)
        assert naam_tabel+' 그래픽: 빨강 초록 파랑' in Teks and 'exit 0' not in Teks,Teks
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        lêer_oordra_verbinding.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        RECEIVED_COUNT=bytearray();lêer_oordra_verbinding.retrbinary('RETR 도중.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==b'FTP DURING GRAPHICS';lêer_oordra_verbinding.delete('도중.txt')
        빛삼원색=화소들()
        for Y_koördinaat,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            OFFSET_VALUE=(Y_koördinaat*640+610)*3;assert tuple(빛삼원색[OFFSET_VALUE:OFFSET_VALUE+3])==색상,(Taal,Y_koördinaat,tuple(빛삼원색[OFFSET_VALUE:OFFSET_VALUE+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(maatreël_data/(Taal+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',BEGIN_tekening)
        if Taal=='java':
            BEGIN_venster=BEGIN_OFFSET('java 창예제')
            수신하기('GUI 예제 Maak_gereed: 창예제'.encode(),BEGIN_venster)
            def klik_VALUE(가로,Vertikaal_plaas):
                for knoppie in (1,0):kliënt.sendall(struct.pack('>BBHH',5,knoppie,가로,Vertikaal_plaas))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            klik_VALUE(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for karakter_VALUE in '한글':누름값(0x1000000|ord(karakter_VALUE));누름값(0x1000000|ord(karakter_VALUE),False)
            for 횟수 in (1,2):
                Loop=len(대화기록);klik_VALUE(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Loop)
            time.sleep(.3)
            venster_tekening=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=venster_tekening.crop((110,272,530,300)).tobytes()
            venster_tekening.save(str(maatreël_data/'java-swing.png'))
            Loop=len(대화기록);klik_VALUE(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',Loop)
        # Download the guest-created bytes through FTP in the same GUI VM.
        lêer_inskrywing_naam={'java':'java.txt','c':'c.txt','python':'python.txt'}[Taal]
        dop('cp '+lêer_inskrywing_naam+' /valideer.txt')
        RECEIVED_COUNT=bytearray();lêer_oordra_verbinding.retrbinary('RETR valideer.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==예상파일.encode()
        dop('echo preserved > 출력예제.'+('py' if Taal=='python' else Taal))
        assert 'EXAMPLES READY' in dop('example '+Taal)
        assert '\npreserved\n' in dop('cat 출력예제.'+('py' if Taal=='python' else Taal))
        assert '한/영 Sleutel_VALUE, Shift+Space 또는 F9' in dop('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in dop('echo GUI NETWORK TOGETHER')
        lêer_oordra_verbinding.quit();lêer_oordra_verbinding=None;assert 'FTP stopped' in dop('ftpd stop')
        print('PASS '+Taal+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if lêer_oordra_verbinding:
            try:lêer_oordra_verbinding.close()
            except OSError:pass
        if kliënt:kliënt.close()
        Proses.terminate()
        try:Proses.wait(timeout=8)
        except subprocess.TimeoutExpired:Proses.kill();Proses.wait()
        selekteerder.close();Proses.stdout.close();(maatreël_data/(Taal+'-serial.log')).write_bytes(대화기록)


def Loop():
    maatreël_data=Project_wortel/'build/verification/examples';maatreël_data.mkdir(parents=True,exist_ok=True)
    validering_verslag={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_wortel/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for Taal in ('java','c','python'):
                test_언어(Taal,되돌림서버항목,maatreël_data);validering_verslag['languages'].append(Taal)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(kategorie_VALUE,data.encode()) for kategorie_VALUE,data in 예상결과],되돌림서버항목.수신됨
            validering_verslag['host_network_payloads']=[{'protocol':kategorie_VALUE,'text':data.decode()} for kategorie_VALUE,data in 되돌림서버항목.수신됨]
        validering_verslag.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(maatreël_data/'report.json').write_text(json.dumps(validering_verslag,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Loop()
