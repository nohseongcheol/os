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
from pc_Weergave import GELIJK_WAARDE
from 예제되돌림서버 import echo_Servers
from Uitvoeren_opdracht import Taken_wortel


def test_Taal(Taal,echo_server_invoer,HR_gegevens):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));bestandsoverdracht_poortnummer=임시자원.getsockname()[1]
    Proces=subprocess.Popen(['python3',str(Taken_wortel/'hulpmiddelen/Uitvoeren_opdracht.py'),'--desktop','--network','--port','0','--ftp-port',str(bestandsoverdracht_poortnummer)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    selector=selectors.DefaultSelector();selector.register(Proces.stdout,selectors.EVENT_READ)
    transcriptie=bytearray();client=None;bestandsoverdracht_verbinding=None
    def ontvangen_e_mail(markering,starten=0):
        beëindigen_VERSCHUIVING=time.monotonic()+60
        while markering not in transcriptie[starten:]:
            if time.monotonic()>beëindigen_VERSCHUIVING or Proces.poll() is not None:raise AssertionError(transcriptie[starten:].decode('utf-8','replace'))
            for 누름값,_ in selector.select(.1):
                gegevens=누름값.fileobj.read(65536)
                if gegevens:transcriptie.extend(gegevens)
        return transcriptie[starten:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(symbool_WAARDE,누르는중=True):client.sendall(struct.pack('>BBHI',4,int(누르는중),0,symbool_WAARDE))
    def START_VERSCHUIVING(invoerregel):
        starten=len(transcriptie)
        for codepoint in invoerregel+'\n':
            symbool_WAARDE=0xff0d if codepoint=='\n' else ord(codepoint) if ord(codepoint)<256 else 0x1000000|ord(codepoint)
            누름값(symbool_WAARDE);누름값(symbool_WAARDE,False)
        return starten
    def Shell(invoerregel):return ontvangen_e_mail(b'jkoros-native> ',START_VERSCHUIVING(invoerregel))
    def Uitvoeren_opdracht(invoerregel,예상결과):
        tekst=Shell(invoerregel);assert 예상결과 in tekst and 'exit 0' in tekst,(invoerregel,tekst)
        return tekst
    def 화소들():
        client.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            gebied_WAARDE=GELIJK_WAARDE(client,1)[0]
            if gebied_WAARDE==2:continue
            if gebied_WAARDE==3:
                item_AANTAL=struct.unpack('>I',GELIJK_WAARDE(client,7)[3:])[0];GELIJK_WAARDE(client,item_AANTAL);continue
            assert gebied_WAARDE==0,gebied_WAARDE
            invoer_AANTAL_8f7753a1=struct.unpack('>H',GELIJK_WAARDE(client,3)[1:])[0]
            for _ in range(invoer_AANTAL_8f7753a1):
                x_coördinaat,Y_coördinaat,너비값,aangevraagd_hoogte_WAARDE,tekenset=struct.unpack('>HHHHi',GELIJK_WAARDE(client,12));assert tekenset==0,tekenset
                gegevens=GELIJK_WAARDE(client,너비값*aangevraagd_hoogte_WAARDE*4)
                for RIJ_functie in range(aangevraagd_hoogte_WAARDE):
                    for KOLOM_functie in range(너비값):
                        원본자료=(RIJ_functie*너비값+KOLOM_functie)*4;doel=((Y_coördinaat+RIJ_functie)*640+x_coördinaat+KOLOM_functie)*3
                        빛삼원색[doel:doel+3]=bytes((gegevens[원본자료+2],gegevens[원본자료+1],gegevens[원본자료]))
            if invoer_AANTAL_8f7753a1:return 빛삼원색
    try:
        ontvangen_e_mail(b'TERMINAL READY');ontvangen_e_mail(b'jkoros-native> ',transcriptie.rfind(b'TERMINAL READY'))
        poortnummer=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',transcriptie).group(1))
        client=socket.create_connection(('127.0.0.1',poortnummer),timeout=10)
        assert GELIJK_WAARDE(client,12)==b'RFB 003.008\n';client.sendall(b'RFB 003.008\n')
        assert 1 in GELIJK_WAARDE(client,GELIJK_WAARDE(client,1)[0]);client.sendall(b'\x01');assert GELIJK_WAARDE(client,4)==b'\0'*4
        client.sendall(b'\x01');초기값=GELIJK_WAARDE(client,24);GELIJK_WAARDE(client,struct.unpack('>I',초기값[20:])[0])
        client.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        client.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in Shell('ftpd start')
        bestandsoverdracht_verbinding=ftplib.FTP();bestandsoverdracht_verbinding.encoding='utf-8';bestandsoverdracht_verbinding.connect('127.0.0.1',bestandsoverdracht_poortnummer,timeout=20);bestandsoverdracht_verbinding.login()
        payload_gegevens=('GUI와 FTP 동시 gebruik_WAARDE '+Taal+' 😀\n').encode()
        bestandsoverdracht_verbinding.storbinary('STOR 함께.txt',io.BytesIO(payload_gegevens))
        assert payload_gegevens.decode().strip() in Shell('cat /함께.txt')
        OPBRENGST_AANTAL=bytearray();bestandsoverdracht_verbinding.retrbinary('RETR 함께.txt',OPBRENGST_AANTAL.extend);assert OPBRENGST_AANTAL==payload_gegevens;bestandsoverdracht_verbinding.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        e_mailen_Lijst=Shell('ls /example')
        assert all(Naam in e_mailen_Lijst for Naam in ('java/','c/','python/','README.md')),e_mailen_Lijst
        if Taal=='java':
            bundel_manifest=json.loads((Taken_wortel/'build/examples/manifest.json').read_text())
            for pad,beginpunt in bundel_manifest.items():
                Shell('cp '+pad+' /example-check.bin')
                Inhoud_WAARDE=bytearray();bestandsoverdracht_verbinding.retrbinary('RETR example-check.bin',Inhoud_WAARDE.extend)
                assert len(Inhoud_WAARDE)==beginpunt['bytes'] and hashlib.sha256(Inhoud_WAARDE).hexdigest()==beginpunt['sha256'],pad
            bestandsoverdracht_verbinding.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            binair=bytes(range(256))*64
            bestandsoverdracht_verbinding.storbinary('STOR boundary.bin',io.BytesIO(binair))
            Inhoud_WAARDE=bytearray();bestandsoverdracht_verbinding.retrbinary('RETR boundary.bin',Inhoud_WAARDE.extend)
            assert Inhoud_WAARDE==binair and 'boundary.bin' in bestandsoverdracht_verbinding.nlst()
            Shell('cp /boundary.bin /boundary-copy.bin')
            Inhoud_WAARDE=bytearray();bestandsoverdracht_verbinding.retrbinary('RETR boundary-copy.bin',Inhoud_WAARDE.extend)
            assert Inhoud_WAARDE==binair
            bestandsoverdracht_verbinding.delete('boundary.bin');bestandsoverdracht_verbinding.delete('boundary-copy.bin')
        assert 'Uitvoervoorbeeld' in Shell('ls /example/'+Taal)
        Shell('cd /example/'+Taal)
        naam_tabel={'java':'JAVA','c':'C','python':'PYTHON'}[Taal]
        예상파일=naam_tabel+' bestand: 한글 gegevens 😀\n'
        if Taal=='java':
            Uitvoeren_opdracht('javac Uitvoervoorbeeld.java','Compiled:');Uitvoeren_opdracht('java Uitvoervoorbeeld','JAVA tekstuitvoer: 안녕하세요 😀')
            Uitvoeren_opdracht('javac Bestandsvoorbeeld.java','Compiled:');Uitvoeren_opdracht('java Bestandsvoorbeeld',예상파일)
            Uitvoeren_opdracht('java Netwerkvoorbeeld {} {}'.format(echo_server_invoer.TCP_poort,echo_server_invoer.UDP_poort),'JAVA 네트워크 bevestigen: TCP UDP 한글')
            graphics_opdracht='java Tekenvoorbeeld'
        elif Taal=='c':
            for Naam,전달값,예상결과 in [('tekstuitvoer','', 'C tekstuitvoer: 안녕하세요 😀'),('bestand','',예상파일),
                    ('네트워크',' '+str(echo_server_invoer.UDP_poort),'C 네트워크 bevestigen: UDP 한글')]:
                Uitvoeren_opdracht('cc '+Naam+'예제.c -o Uitvoeren_opdracht','Compiled native ARM64 ELF:')
                Uitvoeren_opdracht('./Uitvoeren_opdracht'+전달값,예상결과)
            Uitvoeren_opdracht('cc Tekenvoorbeeld.c -o Uitvoeren_opdracht','Compiled native ARM64 ELF:');graphics_opdracht='./Uitvoeren_opdracht'
        else:
            for Naam,전달값,예상결과 in [('tekstuitvoer','','PYTHON tekstuitvoer: 안녕하세요 😀'),('bestand','',예상파일),
                    ('네트워크',' '+str(echo_server_invoer.UDP_poort),'PYTHON 네트워크 bevestigen: UDP 한글')]:
                Uitvoeren_opdracht('python '+Naam+'예제.py'+전달값,예상결과)
            graphics_opdracht='python Tekenvoorbeeld.py'
        START_tekening=START_VERSCHUIVING(graphics_opdracht)
        tekst=ontvangen_e_mail('그림을 확인한 BACK_WAARDE Enter를 누르세요.\r\n'.encode(),START_tekening)
        assert naam_tabel+' 그래픽: 빨강 초록 파랑' in tekst and 'exit 0' not in tekst,tekst
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        bestandsoverdracht_verbinding.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        OPBRENGST_AANTAL=bytearray();bestandsoverdracht_verbinding.retrbinary('RETR 도중.txt',OPBRENGST_AANTAL.extend);assert OPBRENGST_AANTAL==b'FTP DURING GRAPHICS';bestandsoverdracht_verbinding.delete('도중.txt')
        빛삼원색=화소들()
        for Y_coördinaat,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            VERSCHUIVING_WAARDE=(Y_coördinaat*640+610)*3;assert tuple(빛삼원색[VERSCHUIVING_WAARDE:VERSCHUIVING_WAARDE+3])==색상,(Taal,Y_coördinaat,tuple(빛삼원색[VERSCHUIVING_WAARDE:VERSCHUIVING_WAARDE+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(HR_gegevens/(Taal+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in ontvangen_e_mail(b'jkoros-native> ',START_tekening)
        if Taal=='java':
            START_venster=START_VERSCHUIVING('java Venstervoorbeeld')
            ontvangen_e_mail('GUI 예제 Bereid_voor: Venstervoorbeeld'.encode(),START_venster)
            def click_WAARDE(가로,Verticaal_functie):
                for knop in (1,0):client.sendall(struct.pack('>BBHH',5,knop,가로,Verticaal_functie))
            time.sleep(.3)
            Vorige_kopie=Image.frombytes('RGB',(640,480),bytes(화소들()))
            click_WAARDE(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for teken_WAARDE in '한글':누름값(0x1000000|ord(teken_WAARDE));누름값(0x1000000|ord(teken_WAARDE),False)
            for herhaling_AANTAL in (1,2):
                starten=len(transcriptie);click_WAARDE(180,242)
                ontvangen_e_mail(('GUI 인사: 안녕하세요, 한글님! ('+str(herhaling_AANTAL)+')').encode(),starten)
            time.sleep(.3)
            venster_tekening=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert Vorige_kopie.crop((110,272,530,300)).tobytes()!=venster_tekening.crop((110,272,530,300)).tobytes()
            venster_tekening.save(str(HR_gegevens/'java-swing.png'))
            starten=len(transcriptie);click_WAARDE(535,105)
            assert 'exit 0' in ontvangen_e_mail(b'jkoros-native> ',starten)
        # Download the guest-created bytes through FTP in the same GUI VM.
        Bestand_invoer_naam={'java':'java.txt','c':'c.txt','python':'python.txt'}[Taal]
        Shell('cp '+Bestand_invoer_naam+' /valideren.txt')
        OPBRENGST_AANTAL=bytearray();bestandsoverdracht_verbinding.retrbinary('RETR valideren.txt',OPBRENGST_AANTAL.extend);assert OPBRENGST_AANTAL==예상파일.encode()
        Shell('echo preserved > Uitvoervoorbeeld.'+('py' if Taal=='python' else Taal))
        assert 'EXAMPLES READY' in Shell('example '+Taal)
        assert '\npreserved\n' in Shell('cat Uitvoervoorbeeld.'+('py' if Taal=='python' else Taal))
        assert '한/nul_operand toets_WAARDE, Shift+Space 또는 F9' in Shell('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in Shell('echo GUI NETWORK TOGETHER')
        bestandsoverdracht_verbinding.quit();bestandsoverdracht_verbinding=None;assert 'FTP stopped' in Shell('ftpd stop')
        print('PASS '+Taal+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if bestandsoverdracht_verbinding:
            try:bestandsoverdracht_verbinding.close()
            except OSError:pass
        if client:client.close()
        Proces.terminate()
        try:Proces.wait(timeout=8)
        except subprocess.TimeoutExpired:Proces.kill();Proces.wait()
        selector.close();Proces.stdout.close();(HR_gegevens/(Taal+'-serial.log')).write_bytes(transcriptie)


def starten():
    HR_gegevens=Taken_wortel/'build/verification/examples';HR_gegevens.mkdir(parents=True,exist_ok=True)
    validatie_Rapport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Taken_wortel/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with echo_Servers() as echo_server_invoer:
            for Taal in ('java','c','python'):
                test_Taal(Taal,echo_server_invoer,HR_gegevens);validatie_Rapport['languages'].append(Taal)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert echo_server_invoer.수신됨==[(gebied_WAARDE,gegevens.encode()) for gebied_WAARDE,gegevens in 예상결과],echo_server_invoer.수신됨
            validatie_Rapport['host_network_payloads']=[{'protocol':gebied_WAARDE,'text':gegevens.decode()} for gebied_WAARDE,gegevens in echo_server_invoer.수신됨]
        validatie_Rapport.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(HR_gegevens/'report.json').write_text(json.dumps(validatie_Rapport,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':starten()
