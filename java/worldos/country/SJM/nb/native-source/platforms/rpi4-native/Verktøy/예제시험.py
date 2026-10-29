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
from stasjonær_vise import EKSAKT_VERDI
from 예제되돌림서버 import oppdatere_skjerm_Servere
from Utfør_kommando import speile_rot


def test_Språk(Språk,oppdatere_skjerm_server_oppføring,KR_data):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));filoverføring_portnummer=임시자원.getsockname()[1]
    Prosess=subprocess.Popen(['python3',str(speile_rot/'Verktøy/Utfør_kommando.py'),'--desktop','--network','--port','0','--ftp-port',str(filoverføring_portnummer)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    velger=selectors.DefaultSelector();velger.register(Prosess.stdout,selectors.EVENT_READ)
    utskrift=bytearray();klient=None;filoverføring_kontakt=None
    def motta_e_post(tusj,Kjør_2=0):
        avslutte_en_samtale_FORSKYVNING=time.monotonic()+60
        while tusj not in utskrift[Kjør_2:]:
            if time.monotonic()>avslutte_en_samtale_FORSKYVNING or Prosess.poll() is not None:raise AssertionError(utskrift[Kjør_2:].decode('utf-8','replace'))
            for 누름값,_ in velger.select(.1):
                data=누름값.fileobj.read(65536)
                if data:utskrift.extend(data)
        return utskrift[Kjør_2:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(symbol_VERDI,누르는중=True):klient.sendall(struct.pack('>BBHI',4,int(누르는중),0,symbol_VERDI))
    def START_FORSKYVNING(Linje):
        Kjør_2=len(utskrift)
        for tegnkode in Linje+'\n':
            symbol_VERDI=0xff0d if tegnkode=='\n' else ord(tegnkode) if ord(tegnkode)<256 else 0x1000000|ord(tegnkode)
            누름값(symbol_VERDI);누름값(symbol_VERDI,False)
        return Kjør_2
    def Shell(Linje):return motta_e_post(b'jkoros-native> ',START_FORSKYVNING(Linje))
    def Utfør_kommando(Linje,예상결과):
        Tekst=Shell(Linje);assert 예상결과 in Tekst and 'exit 0' in Tekst,(Linje,Tekst)
        return Tekst
    def 화소들():
        klient.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            område_VERDI=EKSAKT_VERDI(klient,1)[0]
            if område_VERDI==2:continue
            if område_VERDI==3:
                vare_ANTALL=struct.unpack('>I',EKSAKT_VERDI(klient,7)[3:])[0];EKSAKT_VERDI(klient,vare_ANTALL);continue
            assert område_VERDI==0,område_VERDI
            oppføring_ANTALL=struct.unpack('>H',EKSAKT_VERDI(klient,3)[1:])[0]
            for _ in range(oppføring_ANTALL):
                x_koordinat,Y_koordinat,너비값,높이값,tegnsett=struct.unpack('>HHHHi',EKSAKT_VERDI(klient,12));assert tegnsett==0,tegnsett
                data=EKSAKT_VERDI(klient,너비값*높이값*4)
                for RAD_plassere in range(높이값):
                    for spalte_plassere in range(너비값):
                        원본자료=(RAD_plassere*너비값+spalte_plassere)*4;mål=((Y_koordinat+RAD_plassere)*640+x_koordinat+spalte_plassere)*3
                        빛삼원색[mål:mål+3]=bytes((data[원본자료+2],data[원본자료+1],data[원본자료]))
            if oppføring_ANTALL:return 빛삼원색
    try:
        motta_e_post(b'TERMINAL READY');motta_e_post(b'jkoros-native> ',utskrift.rfind(b'TERMINAL READY'))
        portnummer=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',utskrift).group(1))
        klient=socket.create_connection(('127.0.0.1',portnummer),timeout=10)
        assert EKSAKT_VERDI(klient,12)==b'RFB 003.008\n';klient.sendall(b'RFB 003.008\n')
        assert 1 in EKSAKT_VERDI(klient,EKSAKT_VERDI(klient,1)[0]);klient.sendall(b'\x01');assert EKSAKT_VERDI(klient,4)==b'\0'*4
        klient.sendall(b'\x01');초기값=EKSAKT_VERDI(klient,24);EKSAKT_VERDI(klient,struct.unpack('>I',초기값[20:])[0])
        klient.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        klient.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in Shell('ftpd start')
        filoverføring_kontakt=ftplib.FTP();filoverføring_kontakt.encoding='utf-8';filoverføring_kontakt.connect('127.0.0.1',filoverføring_portnummer,timeout=20);filoverføring_kontakt.login()
        nyttelast_data=('GUI와 FTP 동시 bruk_VERDI '+Språk+' 😀\n').encode()
        filoverføring_kontakt.storbinary('STOR 함께.txt',io.BytesIO(nyttelast_data))
        assert nyttelast_data.decode().strip() in Shell('cat /함께.txt')
        MOTTATT_AVKAST_ANTALL=bytearray();filoverføring_kontakt.retrbinary('RETR 함께.txt',MOTTATT_AVKAST_ANTALL.extend);assert MOTTATT_AVKAST_ANTALL==nyttelast_data;filoverføring_kontakt.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        sende_Liste=Shell('ls /example')
        assert all(Navn in sende_Liste for Navn in ('java/','c/','python/','README.md')),sende_Liste
        if Språk=='java':
            bunt_manifest=json.loads((speile_rot/'build/examples/manifest.json').read_text())
            for Sti,inngangspunkt in bunt_manifest.items():
                Shell('cp '+Sti+' /example-check.bin')
                Innhold_VERDI=bytearray();filoverføring_kontakt.retrbinary('RETR example-check.bin',Innhold_VERDI.extend)
                assert len(Innhold_VERDI)==inngangspunkt['bytes'] and hashlib.sha256(Innhold_VERDI).hexdigest()==inngangspunkt['sha256'],Sti
            filoverføring_kontakt.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            binær=bytes(range(256))*64
            filoverføring_kontakt.storbinary('STOR boundary.bin',io.BytesIO(binær))
            Innhold_VERDI=bytearray();filoverføring_kontakt.retrbinary('RETR boundary.bin',Innhold_VERDI.extend)
            assert Innhold_VERDI==binær and 'boundary.bin' in filoverføring_kontakt.nlst()
            Shell('cp /boundary.bin /boundary-copy.bin')
            Innhold_VERDI=bytearray();filoverføring_kontakt.retrbinary('RETR boundary-copy.bin',Innhold_VERDI.extend)
            assert Innhold_VERDI==binær
            filoverføring_kontakt.delete('boundary.bin');filoverføring_kontakt.delete('boundary-copy.bin')
        assert 'Utdataeksempel' in Shell('ls /example/'+Språk)
        Shell('cd /example/'+Språk)
        navn_tabell={'java':'JAVA','c':'C','python':'PYTHON'}[Språk]
        예상파일=navn_tabell+' Fil: 한글 data 😀\n'
        if Språk=='java':
            Utfør_kommando('javac Utdataeksempel.java','Compiled:');Utfør_kommando('java Utdataeksempel','JAVA Utgang: 안녕하세요 😀')
            Utfør_kommando('javac Fileksempel.java','Compiled:');Utfør_kommando('java Fileksempel',예상파일)
            Utfør_kommando('java Nettverkseksempel {} {}'.format(oppdatere_skjerm_server_oppføring.TCP_port,oppdatere_skjerm_server_oppføring.UDP_port),'JAVA 네트워크 bekrefte: TCP UDP 한글')
            grafikk_kommando='java Tegneeksempel'
        elif Språk=='c':
            for Navn,전달값,예상결과 in [('Utgang','', 'C Utgang: 안녕하세요 😀'),('Fil','',예상파일),
                    ('네트워크',' '+str(oppdatere_skjerm_server_oppføring.UDP_port),'C 네트워크 bekrefte: UDP 한글')]:
                Utfør_kommando('cc '+Navn+'예제.c -o Utfør_kommando','Compiled native ARM64 ELF:')
                Utfør_kommando('./Utfør_kommando'+전달값,예상결과)
            Utfør_kommando('cc Tegneeksempel.c -o Utfør_kommando','Compiled native ARM64 ELF:');grafikk_kommando='./Utfør_kommando'
        else:
            for Navn,전달값,예상결과 in [('Utgang','','PYTHON Utgang: 안녕하세요 😀'),('Fil','',예상파일),
                    ('네트워크',' '+str(oppdatere_skjerm_server_oppføring.UDP_port),'PYTHON 네트워크 bekrefte: UDP 한글')]:
                Utfør_kommando('python '+Navn+'예제.py'+전달값,예상결과)
            grafikk_kommando='python Tegneeksempel.py'
        START_tegning=START_FORSKYVNING(grafikk_kommando)
        Tekst=motta_e_post('그림을 확인한 TILBAKE_VERDI Enter를 누르세요.\r\n'.encode(),START_tegning)
        assert navn_tabell+' 그래픽: 빨강 초록 파랑' in Tekst and 'exit 0' not in Tekst,Tekst
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        filoverføring_kontakt.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        MOTTATT_AVKAST_ANTALL=bytearray();filoverføring_kontakt.retrbinary('RETR 도중.txt',MOTTATT_AVKAST_ANTALL.extend);assert MOTTATT_AVKAST_ANTALL==b'FTP DURING GRAPHICS';filoverføring_kontakt.delete('도중.txt')
        빛삼원색=화소들()
        for Y_koordinat,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            FORSKYVNING_VERDI=(Y_koordinat*640+610)*3;assert tuple(빛삼원색[FORSKYVNING_VERDI:FORSKYVNING_VERDI+3])==색상,(Språk,Y_koordinat,tuple(빛삼원색[FORSKYVNING_VERDI:FORSKYVNING_VERDI+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(KR_data/(Språk+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in motta_e_post(b'jkoros-native> ',START_tegning)
        if Språk=='java':
            START_vindu=START_FORSKYVNING('java Vinduseksempel')
            motta_e_post('GUI 예제 Forbered: Vinduseksempel'.encode(),START_vindu)
            def klikk_VERDI(가로,vertikal_plassere):
                for Knapp in (1,0):klient.sendall(struct.pack('>BBHH',5,Knapp,가로,vertikal_plassere))
            time.sleep(.3)
            Forrige_BILDE=Image.frombytes('RGB',(640,480),bytes(화소들()))
            klikk_VERDI(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for tegn_VERDI in '한글':누름값(0x1000000|ord(tegn_VERDI));누름값(0x1000000|ord(tegn_VERDI),False)
            for 횟수 in (1,2):
                Kjør_2=len(utskrift);klikk_VERDI(180,242)
                motta_e_post(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Kjør_2)
            time.sleep(.3)
            vindu_tegning=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert Forrige_BILDE.crop((110,272,530,300)).tobytes()!=vindu_tegning.crop((110,272,530,300)).tobytes()
            vindu_tegning.save(str(KR_data/'java-swing.png'))
            Kjør_2=len(utskrift);klikk_VERDI(535,105)
            assert 'exit 0' in motta_e_post(b'jkoros-native> ',Kjør_2)
        # Download the guest-created bytes through FTP in the same GUI VM.
        Fil_oppføring_navn={'java':'java.txt','c':'c.txt','python':'python.txt'}[Språk]
        Shell('cp '+Fil_oppføring_navn+' /bekrefte_5fb2b747.txt')
        MOTTATT_AVKAST_ANTALL=bytearray();filoverføring_kontakt.retrbinary('RETR bekrefte_5fb2b747.txt',MOTTATT_AVKAST_ANTALL.extend);assert MOTTATT_AVKAST_ANTALL==예상파일.encode()
        Shell('echo preserved > Utdataeksempel.'+('py' if Språk=='python' else Språk))
        assert 'EXAMPLES READY' in Shell('example '+Språk)
        assert '\npreserved\n' in Shell('cat Utdataeksempel.'+('py' if Språk=='python' else Språk))
        assert '한/null_operand tast_VERDI, Shift+Space 또는 F9' in Shell('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in Shell('echo GUI NETWORK TOGETHER')
        filoverføring_kontakt.quit();filoverføring_kontakt=None;assert 'FTP stopped' in Shell('ftpd stop')
        print('PASS '+Språk+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if filoverføring_kontakt:
            try:filoverføring_kontakt.close()
            except OSError:pass
        if klient:klient.close()
        Prosess.terminate()
        try:Prosess.wait(timeout=8)
        except subprocess.TimeoutExpired:Prosess.kill();Prosess.wait()
        velger.close();Prosess.stdout.close();(KR_data/(Språk+'-serial.log')).write_bytes(utskrift)


def Kjør_2():
    KR_data=speile_rot/'build/verification/examples';KR_data.mkdir(parents=True,exist_ok=True)
    validering_rapport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((speile_rot/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with oppdatere_skjerm_Servere() as oppdatere_skjerm_server_oppføring:
            for Språk in ('java','c','python'):
                test_Språk(Språk,oppdatere_skjerm_server_oppføring,KR_data);validering_rapport['languages'].append(Språk)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert oppdatere_skjerm_server_oppføring.수신됨==[(område_VERDI,data.encode()) for område_VERDI,data in 예상결과],oppdatere_skjerm_server_oppføring.수신됨
            validering_rapport['host_network_payloads']=[{'protocol':område_VERDI,'text':data.decode()} for område_VERDI,data in oppdatere_skjerm_server_oppføring.수신됨]
        validering_rapport.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(KR_data/'report.json').write_text(json.dumps(validering_rapport,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Kjør_2()
