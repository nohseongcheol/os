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
from desktop_Prikaz import EXACT_VALUE
from 예제되돌림서버 import 되돌림서버
from Izvrši_komanda import projicirati_koijen


def test_언어(Jezik,되돌림서버항목,mjera_podaci):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));fajl_prijenos_broj_priključka=임시자원.getsockname()[1]
    proces=subprocess.Popen(['python3',str(projicirati_koijen/'Alati/Izvrši_komanda.py'),'--desktop','--network','--port','0','--ftp-port',str(fajl_prijenos_broj_priključka)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    birač=selectors.DefaultSelector();birač.register(proces.stdout,selectors.EVENT_READ)
    대화기록=bytearray();klijent=None;fajl_prijenos_veza=None
    def 수신하기(확인표시,Pokreni=0):
        završiti_Pomak=time.monotonic()+60
        while 확인표시 not in 대화기록[Pokreni:]:
            if time.monotonic()>završiti_Pomak or proces.poll() is not None:raise AssertionError(대화기록[Pokreni:].decode('utf-8','replace'))
            for 누름값,_ in birač.select(.1):
                podaci=누름값.fileobj.read(65536)
                if podaci:대화기록.extend(podaci)
        return 대화기록[Pokreni:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(simbol_VALUE,누르는중=True):klijent.sendall(struct.pack('>BBHI',4,int(누르는중),0,simbol_VALUE))
    def START_Pomak(Linija):
        Pokreni=len(대화기록)
        for kôd_znaka in Linija+'\n':
            simbol_VALUE=0xff0d if kôd_znaka=='\n' else ord(kôd_znaka) if ord(kôd_znaka)<256 else 0x1000000|ord(kôd_znaka)
            누름값(simbol_VALUE);누름값(simbol_VALUE,False)
        return Pokreni
    def ljuska(Linija):return 수신하기(b'jkoros-native> ',START_Pomak(Linija))
    def Izvrši_komanda(Linija,예상결과):
        Tekst=ljuska(Linija);assert 예상결과 in Tekst and 'exit 0' in Tekst,(Linija,Tekst)
        return Tekst
    def 화소들():
        klijent.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            oblast_VALUE=EXACT_VALUE(klijent,1)[0]
            if oblast_VALUE==2:continue
            if oblast_VALUE==3:
                stavka_COUNT=struct.unpack('>I',EXACT_VALUE(klijent,7)[3:])[0];EXACT_VALUE(klijent,stavka_COUNT);continue
            assert oblast_VALUE==0,oblast_VALUE
            unos_COUNT=struct.unpack('>H',EXACT_VALUE(klijent,3)[1:])[0]
            for _ in range(unos_COUNT):
                koordinata_x,Y_koordinata,너비값,높이값,skup_znakova=struct.unpack('>HHHHi',EXACT_VALUE(klijent,12));assert skup_znakova==0,skup_znakova
                podaci=EXACT_VALUE(klijent,너비값*높이값*4)
                for ROW_položaj in range(높이값):
                    for COLUMN_položaj in range(너비값):
                        원본자료=(ROW_položaj*너비값+COLUMN_položaj)*4;cilj=((Y_koordinata+ROW_položaj)*640+koordinata_x+COLUMN_položaj)*3
                        빛삼원색[cilj:cilj+3]=bytes((podaci[원본자료+2],podaci[원본자료+1],podaci[원본자료]))
            if unos_COUNT:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        broj_priključka=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        klijent=socket.create_connection(('127.0.0.1',broj_priključka),timeout=10)
        assert EXACT_VALUE(klijent,12)==b'RFB 003.008\n';klijent.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(klijent,EXACT_VALUE(klijent,1)[0]);klijent.sendall(b'\x01');assert EXACT_VALUE(klijent,4)==b'\0'*4
        klijent.sendall(b'\x01');초기값=EXACT_VALUE(klijent,24);EXACT_VALUE(klijent,struct.unpack('>I',초기값[20:])[0])
        klijent.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        klijent.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in ljuska('ftpd start')
        fajl_prijenos_veza=ftplib.FTP();fajl_prijenos_veza.encoding='utf-8';fajl_prijenos_veza.connect('127.0.0.1',fajl_prijenos_broj_priključka,timeout=20);fajl_prijenos_veza.login()
        korisni_sadržaj_podaci=('GUI와 FTP 동시 사용 '+Jezik+' 😀\n').encode()
        fajl_prijenos_veza.storbinary('STOR 함께.txt',io.BytesIO(korisni_sadržaj_podaci))
        assert korisni_sadržaj_podaci.decode().strip() in ljuska('cat /함께.txt')
        RECEIVED_COUNT=bytearray();fajl_prijenos_veza.retrbinary('RETR 함께.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==korisni_sadržaj_podaci;fajl_prijenos_veza.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        poslati_spisak=ljuska('ls /example')
        assert all(Naziv in poslati_spisak for Naziv in ('java/','c/','python/','README.md')),poslati_spisak
        if Jezik=='java':
            꾸러미명세=json.loads((projicirati_koijen/'build/examples/manifest.json').read_text())
            for Putanja,unos_p in 꾸러미명세.items():
                ljuska('cp '+Putanja+' /example-check.bin')
                Sadržaj_VALUE=bytearray();fajl_prijenos_veza.retrbinary('RETR example-check.bin',Sadržaj_VALUE.extend)
                assert len(Sadržaj_VALUE)==unos_p['bytes'] and hashlib.sha256(Sadržaj_VALUE).hexdigest()==unos_p['sha256'],Putanja
            fajl_prijenos_veza.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            binarno=bytes(range(256))*64
            fajl_prijenos_veza.storbinary('STOR boundary.bin',io.BytesIO(binarno))
            Sadržaj_VALUE=bytearray();fajl_prijenos_veza.retrbinary('RETR boundary.bin',Sadržaj_VALUE.extend)
            assert Sadržaj_VALUE==binarno and 'boundary.bin' in fajl_prijenos_veza.nlst()
            ljuska('cp /boundary.bin /boundary-copy.bin')
            Sadržaj_VALUE=bytearray();fajl_prijenos_veza.retrbinary('RETR boundary-copy.bin',Sadržaj_VALUE.extend)
            assert Sadržaj_VALUE==binarno
            fajl_prijenos_veza.delete('boundary.bin');fajl_prijenos_veza.delete('boundary-copy.bin')
        assert '출력예제' in ljuska('ls /example/'+Jezik)
        ljuska('cd /example/'+Jezik)
        naziv_tabela={'java':'JAVA','c':'C','python':'PYTHON'}[Jezik]
        예상파일=naziv_tabela+' Fajl: 한글 podaci 😀\n'
        if Jezik=='java':
            Izvrši_komanda('javac 출력예제.java','Compiled:');Izvrši_komanda('java 출력예제','JAVA Ispis: 안녕하세요 😀')
            Izvrši_komanda('javac 파일예제.java','Compiled:');Izvrši_komanda('java 파일예제',예상파일)
            Izvrši_komanda('java 네트워크예제 {} {}'.format(되돌림서버항목.TCP_port,되돌림서버항목.UDP_port),'JAVA 네트워크 potvrditi: TCP UDP 한글')
            grafika_komanda='java 그래픽예제'
        elif Jezik=='c':
            for Naziv,전달값,예상결과 in [('Ispis','', 'C Ispis: 안녕하세요 😀'),('Fajl','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.UDP_port),'C 네트워크 potvrditi: UDP 한글')]:
                Izvrši_komanda('cc '+Naziv+'예제.c -o Izvrši_komanda','Compiled native ARM64 ELF:')
                Izvrši_komanda('./Izvrši_komanda'+전달값,예상결과)
            Izvrši_komanda('cc 그래픽예제.c -o Izvrši_komanda','Compiled native ARM64 ELF:');grafika_komanda='./Izvrši_komanda'
        else:
            for Naziv,전달값,예상결과 in [('Ispis','','PYTHON Ispis: 안녕하세요 😀'),('Fajl','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.UDP_port),'PYTHON 네트워크 potvrditi: UDP 한글')]:
                Izvrši_komanda('python '+Naziv+'예제.py'+전달값,예상결과)
            grafika_komanda='python 그래픽예제.py'
        START_ucrtavanje=START_Pomak(grafika_komanda)
        Tekst=수신하기('그림을 확인한 ZAD_VALUE Enter를 누르세요.\r\n'.encode(),START_ucrtavanje)
        assert naziv_tabela+' 그래픽: 빨강 초록 파랑' in Tekst and 'exit 0' not in Tekst,Tekst
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        fajl_prijenos_veza.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        RECEIVED_COUNT=bytearray();fajl_prijenos_veza.retrbinary('RETR 도중.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==b'FTP DURING GRAPHICS';fajl_prijenos_veza.delete('도중.txt')
        빛삼원색=화소들()
        for Y_koordinata,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            Pomak_VALUE=(Y_koordinata*640+610)*3;assert tuple(빛삼원색[Pomak_VALUE:Pomak_VALUE+3])==색상,(Jezik,Y_koordinata,tuple(빛삼원색[Pomak_VALUE:Pomak_VALUE+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(mjera_podaci/(Jezik+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',START_ucrtavanje)
        if Jezik=='java':
            START_prozor=START_Pomak('java 창예제')
            수신하기('GUI 예제 Pripremiti: 창예제'.encode(),START_prozor)
            def klik_VALUE(가로,Vertikalno_položaj):
                for dugme in (1,0):klijent.sendall(struct.pack('>BBHH',5,dugme,가로,Vertikalno_položaj))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            klik_VALUE(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for znak_VALUE in '한글':누름값(0x1000000|ord(znak_VALUE));누름값(0x1000000|ord(znak_VALUE),False)
            for 횟수 in (1,2):
                Pokreni=len(대화기록);klik_VALUE(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Pokreni)
            time.sleep(.3)
            prozor_ucrtavanje=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=prozor_ucrtavanje.crop((110,272,530,300)).tobytes()
            prozor_ucrtavanje.save(str(mjera_podaci/'java-swing.png'))
            Pokreni=len(대화기록);klik_VALUE(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',Pokreni)
        # Download the guest-created bytes through FTP in the same GUI VM.
        fajl_unos_naziv={'java':'java.txt','c':'c.txt','python':'python.txt'}[Jezik]
        ljuska('cp '+fajl_unos_naziv+' /ovjeriti.txt')
        RECEIVED_COUNT=bytearray();fajl_prijenos_veza.retrbinary('RETR ovjeriti.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==예상파일.encode()
        ljuska('echo preserved > 출력예제.'+('py' if Jezik=='python' else Jezik))
        assert 'EXAMPLES READY' in ljuska('example '+Jezik)
        assert '\npreserved\n' in ljuska('cat 출력예제.'+('py' if Jezik=='python' else Jezik))
        assert '한/영 ključ_VALUE, Shift+Space 또는 F9' in ljuska('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in ljuska('echo GUI NETWORK TOGETHER')
        fajl_prijenos_veza.quit();fajl_prijenos_veza=None;assert 'FTP stopped' in ljuska('ftpd stop')
        print('PASS '+Jezik+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if fajl_prijenos_veza:
            try:fajl_prijenos_veza.close()
            except OSError:pass
        if klijent:klijent.close()
        proces.terminate()
        try:proces.wait(timeout=8)
        except subprocess.TimeoutExpired:proces.kill();proces.wait()
        birač.close();proces.stdout.close();(mjera_podaci/(Jezik+'-serial.log')).write_bytes(대화기록)


def Pokreni():
    mjera_podaci=projicirati_koijen/'build/verification/examples';mjera_podaci.mkdir(parents=True,exist_ok=True)
    provjera_izvještaj={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((projicirati_koijen/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for Jezik in ('java','c','python'):
                test_언어(Jezik,되돌림서버항목,mjera_podaci);provjera_izvještaj['languages'].append(Jezik)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(oblast_VALUE,podaci.encode()) for oblast_VALUE,podaci in 예상결과],되돌림서버항목.수신됨
            provjera_izvještaj['host_network_payloads']=[{'protocol':oblast_VALUE,'text':podaci.decode()} for oblast_VALUE,podaci in 되돌림서버항목.수신됨]
        provjera_izvještaj.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(mjera_podaci/'report.json').write_text(json.dumps(provjera_izvještaj,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Pokreni()
