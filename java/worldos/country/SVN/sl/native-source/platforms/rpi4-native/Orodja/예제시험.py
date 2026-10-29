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
from namizje_Pogled import EXACT_VALUE
from 예제되돌림서버 import odmev_Strežniki
from Izvedi_ukaz import pobuda_koren


def preskusiti_jezik(jezik,odmev_strežnik_vnos,KR_podatki):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));prenos_datotek_številka_vrat=임시자원.getsockname()[1]
    Opravilo=subprocess.Popen(['python3',str(pobuda_koren/'Orodja/Izvedi_ukaz.py'),'--desktop','--network','--port','0','--ftp-port',str(prenos_datotek_številka_vrat)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    izbirnik=selectors.DefaultSelector();izbirnik.register(Opravilo.stdout,selectors.EVENT_READ)
    prepis=bytearray();odjemalec=None;prenos_datotek_povezava=None
    def sprejeti_sprejemati_prejeti_prejemati_e_pošta(oznaka,Zaženi=0):
        končati_klic_odmik=time.monotonic()+60
        while oznaka not in prepis[Zaženi:]:
            if time.monotonic()>končati_klic_odmik or Opravilo.poll() is not None:raise AssertionError(prepis[Zaženi:].decode('utf-8','replace'))
            for 누름값,_ in izbirnik.select(.1):
                podatki=누름값.fileobj.read(65536)
                if podatki:prepis.extend(podatki)
        return prepis[Zaženi:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(simbol_VALUE,누르는중=True):odjemalec.sendall(struct.pack('>BBHI',4,int(누르는중),0,simbol_VALUE))
    def Start_odmik(Črtni):
        Zaženi=len(prepis)
        for koda_znaka in Črtni+'\n':
            simbol_VALUE=0xff0d if koda_znaka=='\n' else ord(koda_znaka) if ord(koda_znaka)<256 else 0x1000000|ord(koda_znaka)
            누름값(simbol_VALUE);누름값(simbol_VALUE,False)
        return Zaženi
    def lupina(Črtni):return sprejeti_sprejemati_prejeti_prejemati_e_pošta(b'jkoros-native> ',Start_odmik(Črtni))
    def Izvedi_ukaz(Črtni,예상결과):
        Besedilo=lupina(Črtni);assert 예상결과 in Besedilo and 'exit 0' in Besedilo,(Črtni,Besedilo)
        return Besedilo
    def 화소들():
        odjemalec.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            območje_VALUE=EXACT_VALUE(odjemalec,1)[0]
            if območje_VALUE==2:continue
            if območje_VALUE==3:
                element_COUNT=struct.unpack('>I',EXACT_VALUE(odjemalec,7)[3:])[0];EXACT_VALUE(odjemalec,element_COUNT);continue
            assert območje_VALUE==0,območje_VALUE
            vnos_COUNT=struct.unpack('>H',EXACT_VALUE(odjemalec,3)[1:])[0]
            for _ in range(vnos_COUNT):
                koordinata_x,세로좌표,너비값,높이값,nabor_znakov=struct.unpack('>HHHHi',EXACT_VALUE(odjemalec,12));assert nabor_znakov==0,nabor_znakov
                podatki=EXACT_VALUE(odjemalec,너비값*높이값*4)
                for ROW_položaj in range(높이값):
                    for COLUMN_položaj in range(너비값):
                        원본자료=(ROW_položaj*너비값+COLUMN_položaj)*4;tarča=((세로좌표+ROW_položaj)*640+koordinata_x+COLUMN_položaj)*3
                        빛삼원색[tarča:tarča+3]=bytes((podatki[원본자료+2],podatki[원본자료+1],podatki[원본자료]))
            if vnos_COUNT:return 빛삼원색
    try:
        sprejeti_sprejemati_prejeti_prejemati_e_pošta(b'TERMINAL READY');sprejeti_sprejemati_prejeti_prejemati_e_pošta(b'jkoros-native> ',prepis.rfind(b'TERMINAL READY'))
        številka_vrat=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',prepis).group(1))
        odjemalec=socket.create_connection(('127.0.0.1',številka_vrat),timeout=10)
        assert EXACT_VALUE(odjemalec,12)==b'RFB 003.008\n';odjemalec.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(odjemalec,EXACT_VALUE(odjemalec,1)[0]);odjemalec.sendall(b'\x01');assert EXACT_VALUE(odjemalec,4)==b'\0'*4
        odjemalec.sendall(b'\x01');초기값=EXACT_VALUE(odjemalec,24);EXACT_VALUE(odjemalec,struct.unpack('>I',초기값[20:])[0])
        odjemalec.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        odjemalec.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in lupina('ftpd start')
        prenos_datotek_povezava=ftplib.FTP();prenos_datotek_povezava.encoding='utf-8';prenos_datotek_povezava.connect('127.0.0.1',prenos_datotek_številka_vrat,timeout=20);prenos_datotek_povezava.login()
        koristna_vsebina_podatki=('GUI와 FTP 동시 uporaba_VALUE '+jezik+' 😀\n').encode()
        prenos_datotek_povezava.storbinary('STOR 함께.txt',io.BytesIO(koristna_vsebina_podatki))
        assert koristna_vsebina_podatki.decode().strip() in lupina('cat /함께.txt')
        RECEIVED_COUNT=bytearray();prenos_datotek_povezava.retrbinary('RETR 함께.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==koristna_vsebina_podatki;prenos_datotek_povezava.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        poslati_Seznam=lupina('ls /example')
        assert all(Ime in poslati_Seznam for Ime in ('java/','c/','python/','README.md')),poslati_Seznam
        if jezik=='java':
            꾸러미명세=json.loads((pobuda_koren/'build/examples/manifest.json').read_text())
            for POT,vnos_p in 꾸러미명세.items():
                lupina('cp '+POT+' /example-check.bin')
                vsebina_VALUE=bytearray();prenos_datotek_povezava.retrbinary('RETR example-check.bin',vsebina_VALUE.extend)
                assert len(vsebina_VALUE)==vnos_p['bytes'] and hashlib.sha256(vsebina_VALUE).hexdigest()==vnos_p['sha256'],POT
            prenos_datotek_povezava.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            binary=bytes(range(256))*64
            prenos_datotek_povezava.storbinary('STOR boundary.bin',io.BytesIO(binary))
            vsebina_VALUE=bytearray();prenos_datotek_povezava.retrbinary('RETR boundary.bin',vsebina_VALUE.extend)
            assert vsebina_VALUE==binary and 'boundary.bin' in prenos_datotek_povezava.nlst()
            lupina('cp /boundary.bin /boundary-copy.bin')
            vsebina_VALUE=bytearray();prenos_datotek_povezava.retrbinary('RETR boundary-copy.bin',vsebina_VALUE.extend)
            assert vsebina_VALUE==binary
            prenos_datotek_povezava.delete('boundary.bin');prenos_datotek_povezava.delete('boundary-copy.bin')
        assert 'PrimerIzpisa' in lupina('ls /example/'+jezik)
        lupina('cd /example/'+jezik)
        ime_tabela={'java':'JAVA','c':'C','python':'PYTHON'}[jezik]
        예상파일=ime_tabela+' Datoteka: 한글 podatki 😀\n'
        if jezik=='java':
            Izvedi_ukaz('javac PrimerIzpisa.java','Compiled:');Izvedi_ukaz('java PrimerIzpisa','JAVA Izpis: 안녕하세요 😀')
            Izvedi_ukaz('javac PrimerDatoteke.java','Compiled:');Izvedi_ukaz('java PrimerDatoteke',예상파일)
            Izvedi_ukaz('java PrimerOmrežja {} {}'.format(odmev_strežnik_vnos.TCP_vrata,odmev_strežnik_vnos.UDP_vrata),'JAVA 네트워크 확인: TCP UDP 한글')
            grafični_elementi_ukaz='java PrimerRisanja'
        elif jezik=='c':
            for Ime,전달값,예상결과 in [('Izpis','', 'C Izpis: 안녕하세요 😀'),('Datoteka','',예상파일),
                    ('네트워크',' '+str(odmev_strežnik_vnos.UDP_vrata),'C 네트워크 확인: UDP 한글')]:
                Izvedi_ukaz('cc '+Ime+'예제.c -o Izvedi_ukaz','Compiled native ARM64 ELF:')
                Izvedi_ukaz('./Izvedi_ukaz'+전달값,예상결과)
            Izvedi_ukaz('cc PrimerRisanja.c -o Izvedi_ukaz','Compiled native ARM64 ELF:');grafični_elementi_ukaz='./Izvedi_ukaz'
        else:
            for Ime,전달값,예상결과 in [('Izpis','','PYTHON Izpis: 안녕하세요 😀'),('Datoteka','',예상파일),
                    ('네트워크',' '+str(odmev_strežnik_vnos.UDP_vrata),'PYTHON 네트워크 확인: UDP 한글')]:
                Izvedi_ukaz('python '+Ime+'예제.py'+전달값,예상결과)
            grafični_elementi_ukaz='python PrimerRisanja.py'
        Start_risba=Start_odmik(grafični_elementi_ukaz)
        Besedilo=sprejeti_sprejemati_prejeti_prejemati_e_pošta('그림을 확인한 ZAJ_VALUE Enter를 누르세요.\r\n'.encode(),Start_risba)
        assert ime_tabela+' 그래픽: 빨강 초록 파랑' in Besedilo and 'exit 0' not in Besedilo,Besedilo
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        prenos_datotek_povezava.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        RECEIVED_COUNT=bytearray();prenos_datotek_povezava.retrbinary('RETR 도중.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==b'FTP DURING GRAPHICS';prenos_datotek_povezava.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            odmik_VALUE=(세로좌표*640+610)*3;assert tuple(빛삼원색[odmik_VALUE:odmik_VALUE+3])==색상,(jezik,세로좌표,tuple(빛삼원색[odmik_VALUE:odmik_VALUE+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(KR_podatki/(jezik+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in sprejeti_sprejemati_prejeti_prejemati_e_pošta(b'jkoros-native> ',Start_risba)
        if jezik=='java':
            Start_okno=Start_odmik('java PrimerOkna')
            sprejeti_sprejemati_prejeti_prejemati_e_pošta('GUI 예제 Pripravi: PrimerOkna'.encode(),Start_okno)
            def klik_VALUE(가로,Navpično_položaj):
                for Gumb in (1,0):odjemalec.sendall(struct.pack('>BBHH',5,Gumb,가로,Navpično_položaj))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            klik_VALUE(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for znak_VALUE in '한글':누름값(0x1000000|ord(znak_VALUE));누름값(0x1000000|ord(znak_VALUE),False)
            for 횟수 in (1,2):
                Zaženi=len(prepis);klik_VALUE(180,242)
                sprejeti_sprejemati_prejeti_prejemati_e_pošta(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Zaženi)
            time.sleep(.3)
            okno_risba=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=okno_risba.crop((110,272,530,300)).tobytes()
            okno_risba.save(str(KR_podatki/'java-swing.png'))
            Zaženi=len(prepis);klik_VALUE(535,105)
            assert 'exit 0' in sprejeti_sprejemati_prejeti_prejemati_e_pošta(b'jkoros-native> ',Zaženi)
        # Download the guest-created bytes through FTP in the same GUI VM.
        Datoteka_vnos_ime={'java':'java.txt','c':'c.txt','python':'python.txt'}[jezik]
        lupina('cp '+Datoteka_vnos_ime+' /preveriti_veljavnost.txt')
        RECEIVED_COUNT=bytearray();prenos_datotek_povezava.retrbinary('RETR preveriti_veljavnost.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==예상파일.encode()
        lupina('echo preserved > PrimerIzpisa.'+('py' if jezik=='python' else jezik))
        assert 'EXAMPLES READY' in lupina('example '+jezik)
        assert '\npreserved\n' in lupina('cat PrimerIzpisa.'+('py' if jezik=='python' else jezik))
        assert '한/nič_operand Ključ_VALUE, Shift+Space 또는 F9' in lupina('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in lupina('echo GUI NETWORK TOGETHER')
        prenos_datotek_povezava.quit();prenos_datotek_povezava=None;assert 'FTP stopped' in lupina('ftpd stop')
        print('PASS '+jezik+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if prenos_datotek_povezava:
            try:prenos_datotek_povezava.close()
            except OSError:pass
        if odjemalec:odjemalec.close()
        Opravilo.terminate()
        try:Opravilo.wait(timeout=8)
        except subprocess.TimeoutExpired:Opravilo.kill();Opravilo.wait()
        izbirnik.close();Opravilo.stdout.close();(KR_podatki/(jezik+'-serial.log')).write_bytes(prepis)


def Zaženi():
    KR_podatki=pobuda_koren/'build/verification/examples';KR_podatki.mkdir(parents=True,exist_ok=True)
    preverjanje_veljavnosti_prijavi={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((pobuda_koren/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with odmev_Strežniki() as odmev_strežnik_vnos:
            for jezik in ('java','c','python'):
                preskusiti_jezik(jezik,odmev_strežnik_vnos,KR_podatki);preverjanje_veljavnosti_prijavi['languages'].append(jezik)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert odmev_strežnik_vnos.수신됨==[(območje_VALUE,podatki.encode()) for območje_VALUE,podatki in 예상결과],odmev_strežnik_vnos.수신됨
            preverjanje_veljavnosti_prijavi['host_network_payloads']=[{'protocol':območje_VALUE,'text':podatki.decode()} for območje_VALUE,podatki in odmev_strežnik_vnos.수신됨]
        preverjanje_veljavnosti_prijavi.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(KR_podatki/'report.json').write_text(json.dumps(preverjanje_veljavnosti_prijavi,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Zaženi()
