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
from stolni_Prikaz import EXACT_VALUE
from 예제되돌림서버 import eho_Poslužitelji
from Izvrši_naredba import akcija_korijen


def test_언어(Jezik,eho_server_unos,KR_podaci):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));prijenos_datoteka_broj_priključka=임시자원.getsockname()[1]
    Proces=subprocess.Popen(['python3',str(akcija_korijen/'Alati/Izvrši_naredba.py'),'--desktop','--network','--port','0','--ftp-port',str(prijenos_datoteka_broj_priključka)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    odabirač=selectors.DefaultSelector();odabirač.register(Proces.stdout,selectors.EVENT_READ)
    transkript=bytearray();klijent=None;prijenos_datoteka_veza=None
    def primiti_poruka(marker,Pokreni=0):
        završiti_razgovor_pomak=time.monotonic()+60
        while marker not in transkript[Pokreni:]:
            if time.monotonic()>završiti_razgovor_pomak or Proces.poll() is not None:raise AssertionError(transkript[Pokreni:].decode('utf-8','replace'))
            for 누름값,_ in odabirač.select(.1):
                podaci=누름값.fileobj.read(65536)
                if podaci:transkript.extend(podaci)
        return transkript[Pokreni:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(simbol_VALUE,누르는중=True):klijent.sendall(struct.pack('>BBHI',4,int(누르는중),0,simbol_VALUE))
    def START_pomak(red):
        Pokreni=len(transkript)
        for kodna_točka in red+'\n':
            simbol_VALUE=0xff0d if kodna_točka=='\n' else ord(kodna_točka) if ord(kodna_točka)<256 else 0x1000000|ord(kodna_točka)
            누름값(simbol_VALUE);누름값(simbol_VALUE,False)
        return Pokreni
    def ljuska(red):return primiti_poruka(b'jkoros-native> ',START_pomak(red))
    def Izvrši_naredba(red,예상결과):
        Tekst=ljuska(red);assert 예상결과 in Tekst and 'exit 0' in Tekst,(red,Tekst)
        return Tekst
    def 화소들():
        klijent.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            područje_VALUE=EXACT_VALUE(klijent,1)[0]
            if područje_VALUE==2:continue
            if područje_VALUE==3:
                artikl_COUNT=struct.unpack('>I',EXACT_VALUE(klijent,7)[3:])[0];EXACT_VALUE(klijent,artikl_COUNT);continue
            assert područje_VALUE==0,područje_VALUE
            unos_COUNT=struct.unpack('>H',EXACT_VALUE(klijent,3)[1:])[0]
            for _ in range(unos_COUNT):
                koordinata_x,세로좌표,너비값,높이값,skup_znakova=struct.unpack('>HHHHi',EXACT_VALUE(klijent,12));assert skup_znakova==0,skup_znakova
                podaci=EXACT_VALUE(klijent,너비값*높이값*4)
                for ROW_položaj in range(높이값):
                    for COLUMN_položaj in range(너비값):
                        원본자료=(ROW_položaj*너비값+COLUMN_položaj)*4;cilj=((세로좌표+ROW_položaj)*640+koordinata_x+COLUMN_položaj)*3
                        빛삼원색[cilj:cilj+3]=bytes((podaci[원본자료+2],podaci[원본자료+1],podaci[원본자료]))
            if unos_COUNT:return 빛삼원색
    try:
        primiti_poruka(b'TERMINAL READY');primiti_poruka(b'jkoros-native> ',transkript.rfind(b'TERMINAL READY'))
        broj_priključka=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',transkript).group(1))
        klijent=socket.create_connection(('127.0.0.1',broj_priključka),timeout=10)
        assert EXACT_VALUE(klijent,12)==b'RFB 003.008\n';klijent.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(klijent,EXACT_VALUE(klijent,1)[0]);klijent.sendall(b'\x01');assert EXACT_VALUE(klijent,4)==b'\0'*4
        klijent.sendall(b'\x01');초기값=EXACT_VALUE(klijent,24);EXACT_VALUE(klijent,struct.unpack('>I',초기값[20:])[0])
        klijent.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        klijent.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in ljuska('ftpd start')
        prijenos_datoteka_veza=ftplib.FTP();prijenos_datoteka_veza.encoding='utf-8';prijenos_datoteka_veza.connect('127.0.0.1',prijenos_datoteka_broj_priključka,timeout=20);prijenos_datoteka_veza.login()
        korisni_podaci_podaci=('GUI와 FTP 동시 uporaba_VALUE '+Jezik+' 😀\n').encode()
        prijenos_datoteka_veza.storbinary('STOR 함께.txt',io.BytesIO(korisni_podaci_podaci))
        assert korisni_podaci_podaci.decode().strip() in ljuska('cat /함께.txt')
        RECEIVED_COUNT=bytearray();prijenos_datoteka_veza.retrbinary('RETR 함께.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==korisni_podaci_podaci;prijenos_datoteka_veza.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        slati_Popis=ljuska('ls /example')
        assert all(Ime in slati_Popis for Ime in ('java/','c/','python/','README.md')),slati_Popis
        if Jezik=='java':
            꾸러미명세=json.loads((akcija_korijen/'build/examples/manifest.json').read_text())
            for PUTANJA,unos_p in 꾸러미명세.items():
                ljuska('cp '+PUTANJA+' /example-check.bin')
                Sadržaj_VALUE=bytearray();prijenos_datoteka_veza.retrbinary('RETR example-check.bin',Sadržaj_VALUE.extend)
                assert len(Sadržaj_VALUE)==unos_p['bytes'] and hashlib.sha256(Sadržaj_VALUE).hexdigest()==unos_p['sha256'],PUTANJA
            prijenos_datoteka_veza.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            binarni_podaci=bytes(range(256))*64
            prijenos_datoteka_veza.storbinary('STOR boundary.bin',io.BytesIO(binarni_podaci))
            Sadržaj_VALUE=bytearray();prijenos_datoteka_veza.retrbinary('RETR boundary.bin',Sadržaj_VALUE.extend)
            assert Sadržaj_VALUE==binarni_podaci and 'boundary.bin' in prijenos_datoteka_veza.nlst()
            ljuska('cp /boundary.bin /boundary-copy.bin')
            Sadržaj_VALUE=bytearray();prijenos_datoteka_veza.retrbinary('RETR boundary-copy.bin',Sadržaj_VALUE.extend)
            assert Sadržaj_VALUE==binarni_podaci
            prijenos_datoteka_veza.delete('boundary.bin');prijenos_datoteka_veza.delete('boundary-copy.bin')
        assert 'PrimjerIspisa' in ljuska('ls /example/'+Jezik)
        ljuska('cd /example/'+Jezik)
        naziv_tablica={'java':'JAVA','c':'C','python':'PYTHON'}[Jezik]
        예상파일=naziv_tablica+' Datoteka: 한글 podaci 😀\n'
        if Jezik=='java':
            Izvrši_naredba('javac PrimjerIspisa.java','Compiled:');Izvrši_naredba('java PrimjerIspisa','JAVA Izlaz: 안녕하세요 😀')
            Izvrši_naredba('javac PrimjerDatoteke.java','Compiled:');Izvrši_naredba('java PrimjerDatoteke',예상파일)
            Izvrši_naredba('java PrimjerMreže {} {}'.format(eho_server_unos.TCP_prebaciti,eho_server_unos.UDP_prebaciti),'JAVA 네트워크 provjeriti: TCP UDP 한글')
            grafika_naredba='java PrimjerCrtanja'
        elif Jezik=='c':
            for Ime,전달값,예상결과 in [('Izlaz','', 'C Izlaz: 안녕하세요 😀'),('Datoteka','',예상파일),
                    ('네트워크',' '+str(eho_server_unos.UDP_prebaciti),'C 네트워크 provjeriti: UDP 한글')]:
                Izvrši_naredba('cc '+Ime+'예제.c -o Izvrši_naredba','Compiled native ARM64 ELF:')
                Izvrši_naredba('./Izvrši_naredba'+전달값,예상결과)
            Izvrši_naredba('cc PrimjerCrtanja.c -o Izvrši_naredba','Compiled native ARM64 ELF:');grafika_naredba='./Izvrši_naredba'
        else:
            for Ime,전달값,예상결과 in [('Izlaz','','PYTHON Izlaz: 안녕하세요 😀'),('Datoteka','',예상파일),
                    ('네트워크',' '+str(eho_server_unos.UDP_prebaciti),'PYTHON 네트워크 provjeriti: UDP 한글')]:
                Izvrši_naredba('python '+Ime+'예제.py'+전달값,예상결과)
            grafika_naredba='python PrimjerCrtanja.py'
        START_crtež=START_pomak(grafika_naredba)
        Tekst=primiti_poruka('그림을 확인한 TRAG_VALUE Enter를 누르세요.\r\n'.encode(),START_crtež)
        assert naziv_tablica+' 그래픽: 빨강 초록 파랑' in Tekst and 'exit 0' not in Tekst,Tekst
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        prijenos_datoteka_veza.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        RECEIVED_COUNT=bytearray();prijenos_datoteka_veza.retrbinary('RETR 도중.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==b'FTP DURING GRAPHICS';prijenos_datoteka_veza.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            pomak_VALUE=(세로좌표*640+610)*3;assert tuple(빛삼원색[pomak_VALUE:pomak_VALUE+3])==색상,(Jezik,세로좌표,tuple(빛삼원색[pomak_VALUE:pomak_VALUE+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(KR_podaci/(Jezik+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in primiti_poruka(b'jkoros-native> ',START_crtež)
        if Jezik=='java':
            START_prozor=START_pomak('java PrimjerProzora')
            primiti_poruka('GUI 예제 Pripremi: PrimjerProzora'.encode(),START_prozor)
            def klik_VALUE(가로,Okomito_položaj):
                for gumb in (1,0):klijent.sendall(struct.pack('>BBHH',5,gumb,가로,Okomito_položaj))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            klik_VALUE(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for znak_VALUE in '한글':누름값(0x1000000|ord(znak_VALUE));누름값(0x1000000|ord(znak_VALUE),False)
            for 횟수 in (1,2):
                Pokreni=len(transkript);klik_VALUE(180,242)
                primiti_poruka(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Pokreni)
            time.sleep(.3)
            prozor_crtež=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=prozor_crtež.crop((110,272,530,300)).tobytes()
            prozor_crtež.save(str(KR_podaci/'java-swing.png'))
            Pokreni=len(transkript);klik_VALUE(535,105)
            assert 'exit 0' in primiti_poruka(b'jkoros-native> ',Pokreni)
        # Download the guest-created bytes through FTP in the same GUI VM.
        Datoteka_unos_naziv={'java':'java.txt','c':'c.txt','python':'python.txt'}[Jezik]
        ljuska('cp '+Datoteka_unos_naziv+' /potvrditi.txt')
        RECEIVED_COUNT=bytearray();prijenos_datoteka_veza.retrbinary('RETR potvrditi.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==예상파일.encode()
        ljuska('echo preserved > PrimjerIspisa.'+('py' if Jezik=='python' else Jezik))
        assert 'EXAMPLES READY' in ljuska('example '+Jezik)
        assert '\npreserved\n' in ljuska('cat PrimjerIspisa.'+('py' if Jezik=='python' else Jezik))
        assert '한/nula_operand Ključ_VALUE, Shift+Space 또는 F9' in ljuska('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in ljuska('echo GUI NETWORK TOGETHER')
        prijenos_datoteka_veza.quit();prijenos_datoteka_veza=None;assert 'FTP stopped' in ljuska('ftpd stop')
        print('PASS '+Jezik+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if prijenos_datoteka_veza:
            try:prijenos_datoteka_veza.close()
            except OSError:pass
        if klijent:klijent.close()
        Proces.terminate()
        try:Proces.wait(timeout=8)
        except subprocess.TimeoutExpired:Proces.kill();Proces.wait()
        odabirač.close();Proces.stdout.close();(KR_podaci/(Jezik+'-serial.log')).write_bytes(transkript)


def Pokreni():
    KR_podaci=akcija_korijen/'build/verification/examples';KR_podaci.mkdir(parents=True,exist_ok=True)
    provjera_izvješće={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((akcija_korijen/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with eho_Poslužitelji() as eho_server_unos:
            for Jezik in ('java','c','python'):
                test_언어(Jezik,eho_server_unos,KR_podaci);provjera_izvješće['languages'].append(Jezik)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert eho_server_unos.수신됨==[(područje_VALUE,podaci.encode()) for područje_VALUE,podaci in 예상결과],eho_server_unos.수신됨
            provjera_izvješće['host_network_payloads']=[{'protocol':područje_VALUE,'text':podaci.decode()} for područje_VALUE,podaci in eho_server_unos.수신됨]
        provjera_izvješće.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(KR_podaci/'report.json').write_text(json.dumps(provjera_izvješće,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Pokreni()
