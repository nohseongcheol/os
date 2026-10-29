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
from 예제되돌림서버 import eho_Serveri
from Izvrši_komanda import radnja_koren


def test_언어(jezik,eho_server_stavka,KR_podaci):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));prenos_datoteka_broj_porta=임시자원.getsockname()[1]
    Proces=subprocess.Popen(['python3',str(radnja_koren/'Alatke/Izvrši_komanda.py'),'--desktop','--network','--port','0','--ftp-port',str(prenos_datoteka_broj_porta)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    birač=selectors.DefaultSelector();birač.register(Proces.stdout,selectors.EVENT_READ)
    transkript=bytearray();klijent=None;prenos_datoteka_veza=None
    def primiti_poruka(označivač,koristiti=0):
        završiti_razgovor_Pomak=time.monotonic()+60
        while označivač not in transkript[koristiti:]:
            if time.monotonic()>završiti_razgovor_Pomak or Proces.poll() is not None:raise AssertionError(transkript[koristiti:].decode('utf-8','replace'))
            for 누름값,_ in birač.select(.1):
                podaci=누름값.fileobj.read(65536)
                if podaci:transkript.extend(podaci)
        return transkript[koristiti:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(simbol_VALUE,누르는중=True):klijent.sendall(struct.pack('>BBHI',4,int(누르는중),0,simbol_VALUE))
    def START_Pomak(red):
        koristiti=len(transkript)
        for kôd_znaka in red+'\n':
            simbol_VALUE=0xff0d if kôd_znaka=='\n' else ord(kôd_znaka) if ord(kôd_znaka)<256 else 0x1000000|ord(kôd_znaka)
            누름값(simbol_VALUE);누름값(simbol_VALUE,False)
        return koristiti
    def ljuska(red):return primiti_poruka(b'jkoros-native> ',START_Pomak(red))
    def Izvrši_komanda(red,예상결과):
        SMS=ljuska(red);assert 예상결과 in SMS and 'exit 0' in SMS,(red,SMS)
        return SMS
    def 화소들():
        klijent.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            oblast_VALUE=EXACT_VALUE(klijent,1)[0]
            if oblast_VALUE==2:continue
            if oblast_VALUE==3:
                stavka_COUNT=struct.unpack('>I',EXACT_VALUE(klijent,7)[3:])[0];EXACT_VALUE(klijent,stavka_COUNT);continue
            assert oblast_VALUE==0,oblast_VALUE
            stavka_COUNT_8f7753a1=struct.unpack('>H',EXACT_VALUE(klijent,3)[1:])[0]
            for _ in range(stavka_COUNT_8f7753a1):
                x_koordinata,세로좌표,너비값,높이값,skup_znakova=struct.unpack('>HHHHi',EXACT_VALUE(klijent,12));assert skup_znakova==0,skup_znakova
                podaci=EXACT_VALUE(klijent,너비값*높이값*4)
                for ROW_pozicija in range(높이값):
                    for COLUMN_pozicija in range(너비값):
                        원본자료=(ROW_pozicija*너비값+COLUMN_pozicija)*4;cilj=((세로좌표+ROW_pozicija)*640+x_koordinata+COLUMN_pozicija)*3
                        빛삼원색[cilj:cilj+3]=bytes((podaci[원본자료+2],podaci[원본자료+1],podaci[원본자료]))
            if stavka_COUNT_8f7753a1:return 빛삼원색
    try:
        primiti_poruka(b'TERMINAL READY');primiti_poruka(b'jkoros-native> ',transkript.rfind(b'TERMINAL READY'))
        broj_porta=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',transkript).group(1))
        klijent=socket.create_connection(('127.0.0.1',broj_porta),timeout=10)
        assert EXACT_VALUE(klijent,12)==b'RFB 003.008\n';klijent.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(klijent,EXACT_VALUE(klijent,1)[0]);klijent.sendall(b'\x01');assert EXACT_VALUE(klijent,4)==b'\0'*4
        klijent.sendall(b'\x01');초기값=EXACT_VALUE(klijent,24);EXACT_VALUE(klijent,struct.unpack('>I',초기값[20:])[0])
        klijent.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        klijent.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in ljuska('ftpd start')
        prenos_datoteka_veza=ftplib.FTP();prenos_datoteka_veza.encoding='utf-8';prenos_datoteka_veza.connect('127.0.0.1',prenos_datoteka_broj_porta,timeout=20);prenos_datoteka_veza.login()
        korisni_podaci_podaci=('GUI와 FTP 동시 koristiti_VALUE '+jezik+' 😀\n').encode()
        prenos_datoteka_veza.storbinary('STOR 함께.txt',io.BytesIO(korisni_podaci_podaci))
        assert korisni_podaci_podaci.decode().strip() in ljuska('cat /함께.txt')
        RECEIVED_COUNT=bytearray();prenos_datoteka_veza.retrbinary('RETR 함께.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==korisni_podaci_podaci;prenos_datoteka_veza.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        poslati_Lista=ljuska('ls /example')
        assert all(ime in poslati_Lista for ime in ('java/','c/','python/','README.md')),poslati_Lista
        if jezik=='java':
            꾸러미명세=json.loads((radnja_koren/'build/examples/manifest.json').read_text())
            for putanja,stavka_p in 꾸러미명세.items():
                ljuska('cp '+putanja+' /example-check.bin')
                Sadržaj_VALUE=bytearray();prenos_datoteka_veza.retrbinary('RETR example-check.bin',Sadržaj_VALUE.extend)
                assert len(Sadržaj_VALUE)==stavka_p['bytes'] and hashlib.sha256(Sadržaj_VALUE).hexdigest()==stavka_p['sha256'],putanja
            prenos_datoteka_veza.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            binarni=bytes(range(256))*64
            prenos_datoteka_veza.storbinary('STOR boundary.bin',io.BytesIO(binarni))
            Sadržaj_VALUE=bytearray();prenos_datoteka_veza.retrbinary('RETR boundary.bin',Sadržaj_VALUE.extend)
            assert Sadržaj_VALUE==binarni and 'boundary.bin' in prenos_datoteka_veza.nlst()
            ljuska('cp /boundary.bin /boundary-copy.bin')
            Sadržaj_VALUE=bytearray();prenos_datoteka_veza.retrbinary('RETR boundary-copy.bin',Sadržaj_VALUE.extend)
            assert Sadržaj_VALUE==binarni
            prenos_datoteka_veza.delete('boundary.bin');prenos_datoteka_veza.delete('boundary-copy.bin')
        assert '출력예제' in ljuska('ls /example/'+jezik)
        ljuska('cd /example/'+jezik)
        ime_tabela={'java':'JAVA','c':'C','python':'PYTHON'}[jezik]
        예상파일=ime_tabela+' Datoteka: 한글 podaci 😀\n'
        if jezik=='java':
            Izvrši_komanda('javac 출력예제.java','Compiled:');Izvrši_komanda('java 출력예제','JAVA 출력: 안녕하세요 😀')
            Izvrši_komanda('javac 파일예제.java','Compiled:');Izvrši_komanda('java 파일예제',예상파일)
            Izvrši_komanda('java 네트워크예제 {} {}'.format(eho_server_stavka.TCP_port,eho_server_stavka.UDP_port),'JAVA 네트워크 verifikovati: TCP UDP 한글')
            grafika_komanda='java 그래픽예제'
        elif jezik=='c':
            for ime,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('Datoteka','',예상파일),
                    ('네트워크',' '+str(eho_server_stavka.UDP_port),'C 네트워크 verifikovati: UDP 한글')]:
                Izvrši_komanda('cc '+ime+'예제.c -o Izvrši_komanda','Compiled native ARM64 ELF:')
                Izvrši_komanda('./Izvrši_komanda'+전달값,예상결과)
            Izvrši_komanda('cc 그래픽예제.c -o Izvrši_komanda','Compiled native ARM64 ELF:');grafika_komanda='./Izvrši_komanda'
        else:
            for ime,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('Datoteka','',예상파일),
                    ('네트워크',' '+str(eho_server_stavka.UDP_port),'PYTHON 네트워크 verifikovati: UDP 한글')]:
                Izvrši_komanda('python '+ime+'예제.py'+전달값,예상결과)
            grafika_komanda='python 그래픽예제.py'
        START_crtež=START_Pomak(grafika_komanda)
        SMS=primiti_poruka('그림을 확인한 NAZAD_VALUE Enter를 누르세요.\r\n'.encode(),START_crtež)
        assert ime_tabela+' 그래픽: 빨강 초록 파랑' in SMS and 'exit 0' not in SMS,SMS
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        prenos_datoteka_veza.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        RECEIVED_COUNT=bytearray();prenos_datoteka_veza.retrbinary('RETR 도중.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==b'FTP DURING GRAPHICS';prenos_datoteka_veza.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            Pomak_VALUE=(세로좌표*640+610)*3;assert tuple(빛삼원색[Pomak_VALUE:Pomak_VALUE+3])==색상,(jezik,세로좌표,tuple(빛삼원색[Pomak_VALUE:Pomak_VALUE+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(KR_podaci/(jezik+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in primiti_poruka(b'jkoros-native> ',START_crtež)
        if jezik=='java':
            START_prozor=START_Pomak('java 창예제')
            primiti_poruka('GUI 예제 Pripremi: 창예제'.encode(),START_prozor)
            def klik_VALUE(가로,vertikala_pozicija):
                for taster in (1,0):klijent.sendall(struct.pack('>BBHH',5,taster,가로,vertikala_pozicija))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            klik_VALUE(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for znak_VALUE in '한글':누름값(0x1000000|ord(znak_VALUE));누름값(0x1000000|ord(znak_VALUE),False)
            for 횟수 in (1,2):
                koristiti=len(transkript);klik_VALUE(180,242)
                primiti_poruka(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),koristiti)
            time.sleep(.3)
            prozor_crtež=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=prozor_crtež.crop((110,272,530,300)).tobytes()
            prozor_crtež.save(str(KR_podaci/'java-swing.png'))
            koristiti=len(transkript);klik_VALUE(535,105)
            assert 'exit 0' in primiti_poruka(b'jkoros-native> ',koristiti)
        # Download the guest-created bytes through FTP in the same GUI VM.
        Datoteka_stavka_ime={'java':'java.txt','c':'c.txt','python':'python.txt'}[jezik]
        ljuska('cp '+Datoteka_stavka_ime+' /potvrditi.txt')
        RECEIVED_COUNT=bytearray();prenos_datoteka_veza.retrbinary('RETR potvrditi.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==예상파일.encode()
        ljuska('echo preserved > 출력예제.'+('py' if jezik=='python' else jezik))
        assert 'EXAMPLES READY' in ljuska('example '+jezik)
        assert '\npreserved\n' in ljuska('cat 출력예제.'+('py' if jezik=='python' else jezik))
        assert '한/nula_operand Ključ_VALUE, Shift+Space 또는 F9' in ljuska('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in ljuska('echo GUI NETWORK TOGETHER')
        prenos_datoteka_veza.quit();prenos_datoteka_veza=None;assert 'FTP stopped' in ljuska('ftpd stop')
        print('PASS '+jezik+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if prenos_datoteka_veza:
            try:prenos_datoteka_veza.close()
            except OSError:pass
        if klijent:klijent.close()
        Proces.terminate()
        try:Proces.wait(timeout=8)
        except subprocess.TimeoutExpired:Proces.kill();Proces.wait()
        birač.close();Proces.stdout.close();(KR_podaci/(jezik+'-serial.log')).write_bytes(transkript)


def koristiti():
    KR_podaci=radnja_koren/'build/verification/examples';KR_podaci.mkdir(parents=True,exist_ok=True)
    provera_valjanosti_izveštaj={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((radnja_koren/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with eho_Serveri() as eho_server_stavka:
            for jezik in ('java','c','python'):
                test_언어(jezik,eho_server_stavka,KR_podaci);provera_valjanosti_izveštaj['languages'].append(jezik)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert eho_server_stavka.수신됨==[(oblast_VALUE,podaci.encode()) for oblast_VALUE,podaci in 예상결과],eho_server_stavka.수신됨
            provera_valjanosti_izveštaj['host_network_payloads']=[{'protocol':oblast_VALUE,'text':podaci.decode()} for oblast_VALUE,podaci in eho_server_stavka.수신됨]
        provera_valjanosti_izveštaj.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(KR_podaci/'report.json').write_text(json.dumps(provera_valjanosti_izveštaj,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':koristiti()
