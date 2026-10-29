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
from desktop_Pamja import EXACT_VALUE
from 예제되돌림서버 import 되돌림서버
from zbatoj_komandë import Project_rrënjë


def test_언어(Gjuha,되돌림서버항목,llogaritje_të_dhëna):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));skedar_transferim_numri_i_portës=임시자원.getsockname()[1]
    Proçes=subprocess.Popen(['python3',str(Project_rrënjë/'Mjete/zbatoj_komandë.py'),'--desktop','--network','--port','0','--ftp-port',str(skedar_transferim_numri_i_portës)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    përzgjedhësi=selectors.DefaultSelector();përzgjedhësi.register(Proçes.stdout,selectors.EVENT_READ)
    대화기록=bytearray();klient=None;skedar_transferim_lidhje=None
    def 수신하기(확인표시,Ekzekuto=0):
        mbaroj_OFFSET=time.monotonic()+60
        while 확인표시 not in 대화기록[Ekzekuto:]:
            if time.monotonic()>mbaroj_OFFSET or Proçes.poll() is not None:raise AssertionError(대화기록[Ekzekuto:].decode('utf-8','replace'))
            for 누름값,_ in përzgjedhësi.select(.1):
                të_dhëna=누름값.fileobj.read(65536)
                if të_dhëna:대화기록.extend(të_dhëna)
        return 대화기록[Ekzekuto:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(simbol_VALUE,누르는중=True):klient.sendall(struct.pack('>BBHI',4,int(누르는중),0,simbol_VALUE))
    def nis_OFFSET(linjë):
        Ekzekuto=len(대화기록)
        for kodi_i_karakterit in linjë+'\n':
            simbol_VALUE=0xff0d if kodi_i_karakterit=='\n' else ord(kodi_i_karakterit) if ord(kodi_i_karakterit)<256 else 0x1000000|ord(kodi_i_karakterit)
            누름값(simbol_VALUE);누름값(simbol_VALUE,False)
        return Ekzekuto
    def pasues(linjë):return 수신하기(b'jkoros-native> ',nis_OFFSET(linjë))
    def zbatoj_komandë(linjë,예상결과):
        Teksti=pasues(linjë);assert 예상결과 in Teksti and 'exit 0' in Teksti,(linjë,Teksti)
        return Teksti
    def 화소들():
        klient.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            kategori_VALUE=EXACT_VALUE(klient,1)[0]
            if kategori_VALUE==2:continue
            if kategori_VALUE==3:
                njësi_COUNT=struct.unpack('>I',EXACT_VALUE(klient,7)[3:])[0];EXACT_VALUE(klient,njësi_COUNT);continue
            assert kategori_VALUE==0,kategori_VALUE
            futje_COUNT=struct.unpack('>H',EXACT_VALUE(klient,3)[1:])[0]
            for _ in range(futje_COUNT):
                koordinata_x,Y_koordinatë,너비값,높이값,bashkësia_e_karaktereve=struct.unpack('>HHHHi',EXACT_VALUE(klient,12));assert bashkësia_e_karaktereve==0,bashkësia_e_karaktereve
                të_dhëna=EXACT_VALUE(klient,너비값*높이값*4)
                for ROW_pozicioni in range(높이값):
                    for COLUMN_pozicioni in range(너비값):
                        원본자료=(ROW_pozicioni*너비값+COLUMN_pozicioni)*4;objektiv=((Y_koordinatë+ROW_pozicioni)*640+koordinata_x+COLUMN_pozicioni)*3
                        빛삼원색[objektiv:objektiv+3]=bytes((të_dhëna[원본자료+2],të_dhëna[원본자료+1],të_dhëna[원본자료]))
            if futje_COUNT:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        numri_i_portës=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        klient=socket.create_connection(('127.0.0.1',numri_i_portës),timeout=10)
        assert EXACT_VALUE(klient,12)==b'RFB 003.008\n';klient.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(klient,EXACT_VALUE(klient,1)[0]);klient.sendall(b'\x01');assert EXACT_VALUE(klient,4)==b'\0'*4
        klient.sendall(b'\x01');초기값=EXACT_VALUE(klient,24);EXACT_VALUE(klient,struct.unpack('>I',초기값[20:])[0])
        klient.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        klient.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in pasues('ftpd start')
        skedar_transferim_lidhje=ftplib.FTP();skedar_transferim_lidhje.encoding='utf-8';skedar_transferim_lidhje.connect('127.0.0.1',skedar_transferim_numri_i_portës,timeout=20);skedar_transferim_lidhje.login()
        ngarkesë_e_dobishme_të_dhëna=('GUI와 FTP 동시 사용 '+Gjuha+' 😀\n').encode()
        skedar_transferim_lidhje.storbinary('STOR 함께.txt',io.BytesIO(ngarkesë_e_dobishme_të_dhëna))
        assert ngarkesë_e_dobishme_të_dhëna.decode().strip() in pasues('cat /함께.txt')
        RECEIVED_COUNT=bytearray();skedar_transferim_lidhje.retrbinary('RETR 함께.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==ngarkesë_e_dobishme_të_dhëna;skedar_transferim_lidhje.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        dërgoj_Listë=pasues('ls /example')
        assert all(Emër in dërgoj_Listë for Emër in ('java/','c/','python/','README.md')),dërgoj_Listë
        if Gjuha=='java':
            꾸러미명세=json.loads((Project_rrënjë/'build/examples/manifest.json').read_text())
            for POZICIONI,futje_p in 꾸러미명세.items():
                pasues('cp '+POZICIONI+' /example-check.bin')
                Përmbajtje_VALUE=bytearray();skedar_transferim_lidhje.retrbinary('RETR example-check.bin',Përmbajtje_VALUE.extend)
                assert len(Përmbajtje_VALUE)==futje_p['bytes'] and hashlib.sha256(Përmbajtje_VALUE).hexdigest()==futje_p['sha256'],POZICIONI
            skedar_transferim_lidhje.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            binar=bytes(range(256))*64
            skedar_transferim_lidhje.storbinary('STOR boundary.bin',io.BytesIO(binar))
            Përmbajtje_VALUE=bytearray();skedar_transferim_lidhje.retrbinary('RETR boundary.bin',Përmbajtje_VALUE.extend)
            assert Përmbajtje_VALUE==binar and 'boundary.bin' in skedar_transferim_lidhje.nlst()
            pasues('cp /boundary.bin /boundary-copy.bin')
            Përmbajtje_VALUE=bytearray();skedar_transferim_lidhje.retrbinary('RETR boundary-copy.bin',Përmbajtje_VALUE.extend)
            assert Përmbajtje_VALUE==binar
            skedar_transferim_lidhje.delete('boundary.bin');skedar_transferim_lidhje.delete('boundary-copy.bin')
        assert '출력예제' in pasues('ls /example/'+Gjuha)
        pasues('cd /example/'+Gjuha)
        emër_tabelë={'java':'JAVA','c':'C','python':'PYTHON'}[Gjuha]
        예상파일=emër_tabelë+' Kartelë: 한글 të_dhëna 😀\n'
        if Gjuha=='java':
            zbatoj_komandë('javac 출력예제.java','Compiled:');zbatoj_komandë('java 출력예제','JAVA 출력: 안녕하세요 😀')
            zbatoj_komandë('javac 파일예제.java','Compiled:');zbatoj_komandë('java 파일예제',예상파일)
            zbatoj_komandë('java 네트워크예제 {} {}'.format(되돌림서버항목.TCP_portë,되돌림서버항목.UDP_portë),'JAVA 네트워크 verifikoj: TCP UDP 한글')
            figura_komandë='java 그래픽예제'
        elif Gjuha=='c':
            for Emër,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('Kartelë','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.UDP_portë),'C 네트워크 verifikoj: UDP 한글')]:
                zbatoj_komandë('cc '+Emër+'예제.c -o zbatoj_komandë','Compiled native ARM64 ELF:')
                zbatoj_komandë('./zbatoj_komandë'+전달값,예상결과)
            zbatoj_komandë('cc 그래픽예제.c -o zbatoj_komandë','Compiled native ARM64 ELF:');figura_komandë='./zbatoj_komandë'
        else:
            for Emër,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('Kartelë','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.UDP_portë),'PYTHON 네트워크 verifikoj: UDP 한글')]:
                zbatoj_komandë('python '+Emër+'예제.py'+전달값,예상결과)
            figura_komandë='python 그래픽예제.py'
        nis_vizatim=nis_OFFSET(figura_komandë)
        Teksti=수신하기('그림을 확인한 PAS_VALUE Enter를 누르세요.\r\n'.encode(),nis_vizatim)
        assert emër_tabelë+' 그래픽: 빨강 초록 파랑' in Teksti and 'exit 0' not in Teksti,Teksti
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        skedar_transferim_lidhje.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        RECEIVED_COUNT=bytearray();skedar_transferim_lidhje.retrbinary('RETR 도중.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==b'FTP DURING GRAPHICS';skedar_transferim_lidhje.delete('도중.txt')
        빛삼원색=화소들()
        for Y_koordinatë,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            OFFSET_VALUE=(Y_koordinatë*640+610)*3;assert tuple(빛삼원색[OFFSET_VALUE:OFFSET_VALUE+3])==색상,(Gjuha,Y_koordinatë,tuple(빛삼원색[OFFSET_VALUE:OFFSET_VALUE+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(llogaritje_të_dhëna/(Gjuha+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',nis_vizatim)
        if Gjuha=='java':
            nis_dritare=nis_OFFSET('java 창예제')
            수신하기('GUI 예제 Përgatit: 창예제'.encode(),nis_dritare)
            def klik_VALUE(가로,Vertikal_pozicioni):
                for Buton in (1,0):klient.sendall(struct.pack('>BBHH',5,Buton,가로,Vertikal_pozicioni))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            klik_VALUE(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for karakter_VALUE in '한글':누름값(0x1000000|ord(karakter_VALUE));누름값(0x1000000|ord(karakter_VALUE),False)
            for 횟수 in (1,2):
                Ekzekuto=len(대화기록);klik_VALUE(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Ekzekuto)
            time.sleep(.3)
            dritare_vizatim=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=dritare_vizatim.crop((110,272,530,300)).tobytes()
            dritare_vizatim.save(str(llogaritje_të_dhëna/'java-swing.png'))
            Ekzekuto=len(대화기록);klik_VALUE(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',Ekzekuto)
        # Download the guest-created bytes through FTP in the same GUI VM.
        skedar_futje_emër={'java':'java.txt','c':'c.txt','python':'python.txt'}[Gjuha]
        pasues('cp '+skedar_futje_emër+' /vlerësoj.txt')
        RECEIVED_COUNT=bytearray();skedar_transferim_lidhje.retrbinary('RETR vlerësoj.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==예상파일.encode()
        pasues('echo preserved > 출력예제.'+('py' if Gjuha=='python' else Gjuha))
        assert 'EXAMPLES READY' in pasues('example '+Gjuha)
        assert '\npreserved\n' in pasues('cat 출력예제.'+('py' if Gjuha=='python' else Gjuha))
        assert '한/영 tast_VALUE, Shift+Space 또는 F9' in pasues('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in pasues('echo GUI NETWORK TOGETHER')
        skedar_transferim_lidhje.quit();skedar_transferim_lidhje=None;assert 'FTP stopped' in pasues('ftpd stop')
        print('PASS '+Gjuha+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if skedar_transferim_lidhje:
            try:skedar_transferim_lidhje.close()
            except OSError:pass
        if klient:klient.close()
        Proçes.terminate()
        try:Proçes.wait(timeout=8)
        except subprocess.TimeoutExpired:Proçes.kill();Proçes.wait()
        përzgjedhësi.close();Proçes.stdout.close();(llogaritje_të_dhëna/(Gjuha+'-serial.log')).write_bytes(대화기록)


def Ekzekuto():
    llogaritje_të_dhëna=Project_rrënjë/'build/verification/examples';llogaritje_të_dhëna.mkdir(parents=True,exist_ok=True)
    miratim_raport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_rrënjë/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for Gjuha in ('java','c','python'):
                test_언어(Gjuha,되돌림서버항목,llogaritje_të_dhëna);miratim_raport['languages'].append(Gjuha)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(kategori_VALUE,të_dhëna.encode()) for kategori_VALUE,të_dhëna in 예상결과],되돌림서버항목.수신됨
            miratim_raport['host_network_payloads']=[{'protocol':kategori_VALUE,'text':të_dhëna.decode()} for kategori_VALUE,të_dhëna in 되돌림서버항목.수신됨]
        miratim_raport.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(llogaritje_të_dhëna/'report.json').write_text(json.dumps(miratim_raport,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Ekzekuto()
