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
from dators_Skats import EXACT_VALUE
from 예제되돌림서버 import atbalss_Serveri
from Izpildīt_komanda import Project_sakne


def test_언어(Valodas,atbalss_serveris_ievade,mērs_dati):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));faila_pārsūtīšana_porta_numurs=임시자원.getsockname()[1]
    Process=subprocess.Popen(['python3',str(Project_sakne/'Rīki/Izpildīt_komanda.py'),'--desktop','--network','--port','0','--ftp-port',str(faila_pārsūtīšana_porta_numurs)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    atlasītājs=selectors.DefaultSelector();atlasītājs.register(Process.stdout,selectors.EVENT_READ)
    transkripcija=bytearray();klients=None;faila_pārsūtīšana_paziņa=None
    def saņemt_ziņa(marķieris,Palaist=0):
        beigt_zvanu_Nobīde=time.monotonic()+60
        while marķieris not in transkripcija[Palaist:]:
            if time.monotonic()>beigt_zvanu_Nobīde or Process.poll() is not None:raise AssertionError(transkripcija[Palaist:].decode('utf-8','replace'))
            for 누름값,_ in atlasītājs.select(.1):
                dati=누름값.fileobj.read(65536)
                if dati:transkripcija.extend(dati)
        return transkripcija[Palaist:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(simbols_VALUE,누르는중=True):klients.sendall(struct.pack('>BBHI',4,int(누르는중),0,simbols_VALUE))
    def Sākt_Nobīde(Līniju):
        Palaist=len(transkripcija)
        for koda_punkts in Līniju+'\n':
            simbols_VALUE=0xff0d if koda_punkts=='\n' else ord(koda_punkts) if ord(koda_punkts)<256 else 0x1000000|ord(koda_punkts)
            누름값(simbols_VALUE);누름값(simbols_VALUE,False)
        return Palaist
    def čaula(Līniju):return saņemt_ziņa(b'jkoros-native> ',Sākt_Nobīde(Līniju))
    def Izpildīt_komanda(Līniju,예상결과):
        Teksts=čaula(Līniju);assert 예상결과 in Teksts and 'exit 0' in Teksts,(Līniju,Teksts)
        return Teksts
    def 화소들():
        klients.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            joma_VALUE=EXACT_VALUE(klients,1)[0]
            if joma_VALUE==2:continue
            if joma_VALUE==3:
                krājums_COUNT=struct.unpack('>I',EXACT_VALUE(klients,7)[3:])[0];EXACT_VALUE(klients,krājums_COUNT);continue
            assert joma_VALUE==0,joma_VALUE
            ievade_COUNT=struct.unpack('>H',EXACT_VALUE(klients,3)[1:])[0]
            for _ in range(ievade_COUNT):
                x_koordināta,세로좌표,너비값,높이값,rakstzīmju_kopa=struct.unpack('>HHHHi',EXACT_VALUE(klients,12));assert rakstzīmju_kopa==0,rakstzīmju_kopa
                dati=EXACT_VALUE(klients,너비값*높이값*4)
                for ROW_amats in range(높이값):
                    for COLUMN_amats in range(너비값):
                        원본자료=(ROW_amats*너비값+COLUMN_amats)*4;mērķis=((세로좌표+ROW_amats)*640+x_koordināta+COLUMN_amats)*3
                        빛삼원색[mērķis:mērķis+3]=bytes((dati[원본자료+2],dati[원본자료+1],dati[원본자료]))
            if ievade_COUNT:return 빛삼원색
    try:
        saņemt_ziņa(b'TERMINAL READY');saņemt_ziņa(b'jkoros-native> ',transkripcija.rfind(b'TERMINAL READY'))
        porta_numurs=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',transkripcija).group(1))
        klients=socket.create_connection(('127.0.0.1',porta_numurs),timeout=10)
        assert EXACT_VALUE(klients,12)==b'RFB 003.008\n';klients.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(klients,EXACT_VALUE(klients,1)[0]);klients.sendall(b'\x01');assert EXACT_VALUE(klients,4)==b'\0'*4
        klients.sendall(b'\x01');초기값=EXACT_VALUE(klients,24);EXACT_VALUE(klients,struct.unpack('>I',초기값[20:])[0])
        klients.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        klients.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in čaula('ftpd start')
        faila_pārsūtīšana_paziņa=ftplib.FTP();faila_pārsūtīšana_paziņa.encoding='utf-8';faila_pārsūtīšana_paziņa.connect('127.0.0.1',faila_pārsūtīšana_porta_numurs,timeout=20);faila_pārsūtīšana_paziņa.login()
        vērtums_dati=('GUI와 FTP 동시 lietot_VALUE '+Valodas+' 😀\n').encode()
        faila_pārsūtīšana_paziņa.storbinary('STOR 함께.txt',io.BytesIO(vērtums_dati))
        assert vērtums_dati.decode().strip() in čaula('cat /함께.txt')
        RECEIVED_COUNT=bytearray();faila_pārsūtīšana_paziņa.retrbinary('RETR 함께.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==vērtums_dati;faila_pārsūtīšana_paziņa.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        sūtīt_Saraksts=čaula('ls /example')
        assert all(Nosaukums in sūtīt_Saraksts for Nosaukums in ('java/','c/','python/','README.md')),sūtīt_Saraksts
        if Valodas=='java':
            꾸러미명세=json.loads((Project_sakne/'build/examples/manifest.json').read_text())
            for CEĻŠ,ieejas_punkts in 꾸러미명세.items():
                čaula('cp '+CEĻŠ+' /example-check.bin')
                Saturs_VALUE=bytearray();faila_pārsūtīšana_paziņa.retrbinary('RETR example-check.bin',Saturs_VALUE.extend)
                assert len(Saturs_VALUE)==ieejas_punkts['bytes'] and hashlib.sha256(Saturs_VALUE).hexdigest()==ieejas_punkts['sha256'],CEĻŠ
            faila_pārsūtīšana_paziņa.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            binary=bytes(range(256))*64
            faila_pārsūtīšana_paziņa.storbinary('STOR boundary.bin',io.BytesIO(binary))
            Saturs_VALUE=bytearray();faila_pārsūtīšana_paziņa.retrbinary('RETR boundary.bin',Saturs_VALUE.extend)
            assert Saturs_VALUE==binary and 'boundary.bin' in faila_pārsūtīšana_paziņa.nlst()
            čaula('cp /boundary.bin /boundary-copy.bin')
            Saturs_VALUE=bytearray();faila_pārsūtīšana_paziņa.retrbinary('RETR boundary-copy.bin',Saturs_VALUE.extend)
            assert Saturs_VALUE==binary
            faila_pārsūtīšana_paziņa.delete('boundary.bin');faila_pārsūtīšana_paziņa.delete('boundary-copy.bin')
        assert 'IzvadesPiemērs' in čaula('ls /example/'+Valodas)
        čaula('cd /example/'+Valodas)
        nosaukums_tabula={'java':'JAVA','c':'C','python':'PYTHON'}[Valodas]
        예상파일=nosaukums_tabula+' Fails: 한글 dati 😀\n'
        if Valodas=='java':
            Izpildīt_komanda('javac IzvadesPiemērs.java','Compiled:');Izpildīt_komanda('java IzvadesPiemērs','JAVA Izvade: 안녕하세요 😀')
            Izpildīt_komanda('javac DatnesPiemērs.java','Compiled:');Izpildīt_komanda('java DatnesPiemērs',예상파일)
            Izpildīt_komanda('java TīklaPiemērs {} {}'.format(atbalss_serveris_ievade.TCP_ports,atbalss_serveris_ievade.UDP_ports),'JAVA 네트워크 verificēt: TCP UDP 한글')
            grafika_komanda='java ZīmējumaPiemērs'
        elif Valodas=='c':
            for Nosaukums,전달값,예상결과 in [('Izvade','', 'C Izvade: 안녕하세요 😀'),('Fails','',예상파일),
                    ('네트워크',' '+str(atbalss_serveris_ievade.UDP_ports),'C 네트워크 verificēt: UDP 한글')]:
                Izpildīt_komanda('cc '+Nosaukums+'예제.c -o Izpildīt_komanda','Compiled native ARM64 ELF:')
                Izpildīt_komanda('./Izpildīt_komanda'+전달값,예상결과)
            Izpildīt_komanda('cc ZīmējumaPiemērs.c -o Izpildīt_komanda','Compiled native ARM64 ELF:');grafika_komanda='./Izpildīt_komanda'
        else:
            for Nosaukums,전달값,예상결과 in [('Izvade','','PYTHON Izvade: 안녕하세요 😀'),('Fails','',예상파일),
                    ('네트워크',' '+str(atbalss_serveris_ievade.UDP_ports),'PYTHON 네트워크 verificēt: UDP 한글')]:
                Izpildīt_komanda('python '+Nosaukums+'예제.py'+전달값,예상결과)
            grafika_komanda='python ZīmējumaPiemērs.py'
        Sākt_zīmējums=Sākt_Nobīde(grafika_komanda)
        Teksts=saņemt_ziņa('그림을 확인한 ATPAKAĻ_VALUE Enter를 누르세요.\r\n'.encode(),Sākt_zīmējums)
        assert nosaukums_tabula+' 그래픽: 빨강 초록 파랑' in Teksts and 'exit 0' not in Teksts,Teksts
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        faila_pārsūtīšana_paziņa.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        RECEIVED_COUNT=bytearray();faila_pārsūtīšana_paziņa.retrbinary('RETR 도중.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==b'FTP DURING GRAPHICS';faila_pārsūtīšana_paziņa.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            Nobīde_VALUE=(세로좌표*640+610)*3;assert tuple(빛삼원색[Nobīde_VALUE:Nobīde_VALUE+3])==색상,(Valodas,세로좌표,tuple(빛삼원색[Nobīde_VALUE:Nobīde_VALUE+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(mērs_dati/(Valodas+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in saņemt_ziņa(b'jkoros-native> ',Sākt_zīmējums)
        if Valodas=='java':
            Sākt_logs=Sākt_Nobīde('java LogaPiemērs')
            saņemt_ziņa('GUI 예제 Sagatavot: LogaPiemērs'.encode(),Sākt_logs)
            def klikšķis_VALUE(가로,vertikāle_amats):
                for Pogas in (1,0):klients.sendall(struct.pack('>BBHH',5,Pogas,가로,vertikāle_amats))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            klikšķis_VALUE(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for rakstzīme_VALUE in '한글':누름값(0x1000000|ord(rakstzīme_VALUE));누름값(0x1000000|ord(rakstzīme_VALUE),False)
            for 횟수 in (1,2):
                Palaist=len(transkripcija);klikšķis_VALUE(180,242)
                saņemt_ziņa(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Palaist)
            time.sleep(.3)
            logs_zīmējums=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=logs_zīmējums.crop((110,272,530,300)).tobytes()
            logs_zīmējums.save(str(mērs_dati/'java-swing.png'))
            Palaist=len(transkripcija);klikšķis_VALUE(535,105)
            assert 'exit 0' in saņemt_ziņa(b'jkoros-native> ',Palaist)
        # Download the guest-created bytes through FTP in the same GUI VM.
        Fails_ievade_nosaukums={'java':'java.txt','c':'c.txt','python':'python.txt'}[Valodas]
        čaula('cp '+Fails_ievade_nosaukums+' /validēt.txt')
        RECEIVED_COUNT=bytearray();faila_pārsūtīšana_paziņa.retrbinary('RETR validēt.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==예상파일.encode()
        čaula('echo preserved > IzvadesPiemērs.'+('py' if Valodas=='python' else Valodas))
        assert 'EXAMPLES READY' in čaula('example '+Valodas)
        assert '\npreserved\n' in čaula('cat IzvadesPiemērs.'+('py' if Valodas=='python' else Valodas))
        assert '한/nulle_operands Atslēga_VALUE, Shift+Space 또는 F9' in čaula('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in čaula('echo GUI NETWORK TOGETHER')
        faila_pārsūtīšana_paziņa.quit();faila_pārsūtīšana_paziņa=None;assert 'FTP stopped' in čaula('ftpd stop')
        print('PASS '+Valodas+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if faila_pārsūtīšana_paziņa:
            try:faila_pārsūtīšana_paziņa.close()
            except OSError:pass
        if klients:klients.close()
        Process.terminate()
        try:Process.wait(timeout=8)
        except subprocess.TimeoutExpired:Process.kill();Process.wait()
        atlasītājs.close();Process.stdout.close();(mērs_dati/(Valodas+'-serial.log')).write_bytes(transkripcija)


def Palaist():
    mērs_dati=Project_sakne/'build/verification/examples';mērs_dati.mkdir(parents=True,exist_ok=True)
    validācija_ziņot={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_sakne/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with atbalss_Serveri() as atbalss_serveris_ievade:
            for Valodas in ('java','c','python'):
                test_언어(Valodas,atbalss_serveris_ievade,mērs_dati);validācija_ziņot['languages'].append(Valodas)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert atbalss_serveris_ievade.수신됨==[(joma_VALUE,dati.encode()) for joma_VALUE,dati in 예상결과],atbalss_serveris_ievade.수신됨
            validācija_ziņot['host_network_payloads']=[{'protocol':joma_VALUE,'text':dati.decode()} for joma_VALUE,dati in atbalss_serveris_ievade.수신됨]
        validācija_ziņot.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(mērs_dati/'report.json').write_text(json.dumps(validācija_ziņot,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Palaist()
