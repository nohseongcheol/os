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
from desktop_vizualiza import EXACT_VALUE
from 예제되돌림서버 import ecou_Servere
from executa_comandă import Project_rădăcină


def test_언어(Limbi_străine,ecou_server_intrare,KR_date):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));transfer_de_fișiere_număr_port=임시자원.getsockname()[1]
    Proces=subprocess.Popen(['python3',str(Project_rădăcină/'Instrumente/executa_comandă.py'),'--desktop','--network','--port','0','--ftp-port',str(transfer_de_fișiere_număr_port)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    selector=selectors.DefaultSelector();selector.register(Proces.stdout,selectors.EVENT_READ)
    transcriere=bytearray();client=None;transfer_de_fișiere_conexiune=None
    def primi_mesaj(marcaj,Pornește=0):
        termina_un_apel_OFFSET=time.monotonic()+60
        while marcaj not in transcriere[Pornește:]:
            if time.monotonic()>termina_un_apel_OFFSET or Proces.poll() is not None:raise AssertionError(transcriere[Pornește:].decode('utf-8','replace'))
            for 누름값,_ in selector.select(.1):
                date=누름값.fileobj.read(65536)
                if date:transcriere.extend(date)
        return transcriere[Pornește:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(simbol_VALUE,누르는중=True):client.sendall(struct.pack('>BBHI',4,int(누르는중),0,simbol_VALUE))
    def buta_OFFSET(Linie):
        Pornește=len(transcriere)
        for cod_caracter in Linie+'\n':
            simbol_VALUE=0xff0d if cod_caracter=='\n' else ord(cod_caracter) if ord(cod_caracter)<256 else 0x1000000|ord(cod_caracter)
            누름값(simbol_VALUE);누름값(simbol_VALUE,False)
        return Pornește
    def shell(Linie):return primi_mesaj(b'jkoros-native> ',buta_OFFSET(Linie))
    def executa_comandă(Linie,예상결과):
        SMS=shell(Linie);assert 예상결과 in SMS and 'exit 0' in SMS,(Linie,SMS)
        return SMS
    def 화소들():
        client.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            zonă_VALUE=EXACT_VALUE(client,1)[0]
            if zonă_VALUE==2:continue
            if zonă_VALUE==3:
                element_COUNT=struct.unpack('>I',EXACT_VALUE(client,7)[3:])[0];EXACT_VALUE(client,element_COUNT);continue
            assert zonă_VALUE==0,zonă_VALUE
            intrare_COUNT=struct.unpack('>H',EXACT_VALUE(client,3)[1:])[0]
            for _ in range(intrare_COUNT):
                coordonata_X,세로좌표,너비값,높이값,set_de_caractere=struct.unpack('>HHHHi',EXACT_VALUE(client,12));assert set_de_caractere==0,set_de_caractere
                date=EXACT_VALUE(client,너비값*높이값*4)
                for ROW_poziție in range(높이값):
                    for COLUMN_poziție in range(너비값):
                        원본자료=(ROW_poziție*너비값+COLUMN_poziție)*4;țintă=((세로좌표+ROW_poziție)*640+coordonata_X+COLUMN_poziție)*3
                        빛삼원색[țintă:țintă+3]=bytes((date[원본자료+2],date[원본자료+1],date[원본자료]))
            if intrare_COUNT:return 빛삼원색
    try:
        primi_mesaj(b'TERMINAL READY');primi_mesaj(b'jkoros-native> ',transcriere.rfind(b'TERMINAL READY'))
        număr_port=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',transcriere).group(1))
        client=socket.create_connection(('127.0.0.1',număr_port),timeout=10)
        assert EXACT_VALUE(client,12)==b'RFB 003.008\n';client.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(client,EXACT_VALUE(client,1)[0]);client.sendall(b'\x01');assert EXACT_VALUE(client,4)==b'\0'*4
        client.sendall(b'\x01');초기값=EXACT_VALUE(client,24);EXACT_VALUE(client,struct.unpack('>I',초기값[20:])[0])
        client.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        client.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in shell('ftpd start')
        transfer_de_fișiere_conexiune=ftplib.FTP();transfer_de_fișiere_conexiune.encoding='utf-8';transfer_de_fișiere_conexiune.connect('127.0.0.1',transfer_de_fișiere_număr_port,timeout=20);transfer_de_fișiere_conexiune.login()
        sarcină_date=('GUI와 FTP 동시 utiliza_VALUE '+Limbi_străine+' 😀\n').encode()
        transfer_de_fișiere_conexiune.storbinary('STOR 함께.txt',io.BytesIO(sarcină_date))
        assert sarcină_date.decode().strip() in shell('cat /함께.txt')
        RECEIVED_COUNT=bytearray();transfer_de_fișiere_conexiune.retrbinary('RETR 함께.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==sarcină_date;transfer_de_fișiere_conexiune.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        trimite_Listă=shell('ls /example')
        assert all(Nume in trimite_Listă for Nume in ('java/','c/','python/','README.md')),trimite_Listă
        if Limbi_străine=='java':
            꾸러미명세=json.loads((Project_rădăcină/'build/examples/manifest.json').read_text())
            for Cale,intrare_p in 꾸러미명세.items():
                shell('cp '+Cale+' /example-check.bin')
                Conținut_VALUE=bytearray();transfer_de_fișiere_conexiune.retrbinary('RETR example-check.bin',Conținut_VALUE.extend)
                assert len(Conținut_VALUE)==intrare_p['bytes'] and hashlib.sha256(Conținut_VALUE).hexdigest()==intrare_p['sha256'],Cale
            transfer_de_fișiere_conexiune.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            binar=bytes(range(256))*64
            transfer_de_fișiere_conexiune.storbinary('STOR boundary.bin',io.BytesIO(binar))
            Conținut_VALUE=bytearray();transfer_de_fișiere_conexiune.retrbinary('RETR boundary.bin',Conținut_VALUE.extend)
            assert Conținut_VALUE==binar and 'boundary.bin' in transfer_de_fișiere_conexiune.nlst()
            shell('cp /boundary.bin /boundary-copy.bin')
            Conținut_VALUE=bytearray();transfer_de_fișiere_conexiune.retrbinary('RETR boundary-copy.bin',Conținut_VALUE.extend)
            assert Conținut_VALUE==binar
            transfer_de_fișiere_conexiune.delete('boundary.bin');transfer_de_fișiere_conexiune.delete('boundary-copy.bin')
        assert 'ExempluIeșire' in shell('ls /example/'+Limbi_străine)
        shell('cd /example/'+Limbi_străine)
        nume_tabel={'java':'JAVA','c':'C','python':'PYTHON'}[Limbi_străine]
        예상파일=nume_tabel+' Fișier: 한글 date 😀\n'
        if Limbi_străine=='java':
            executa_comandă('javac ExempluIeșire.java','Compiled:');executa_comandă('java ExempluIeșire','JAVA Rezultat: 안녕하세요 😀')
            executa_comandă('javac ExempluFișier.java','Compiled:');executa_comandă('java ExempluFișier',예상파일)
            executa_comandă('java ExempluRețea {} {}'.format(ecou_server_intrare.TCP_muta,ecou_server_intrare.UDP_muta),'JAVA 네트워크 verifica: TCP UDP 한글')
            grafice_comandă='java ExempluDesen'
        elif Limbi_străine=='c':
            for Nume,전달값,예상결과 in [('Rezultat','', 'C Rezultat: 안녕하세요 😀'),('Fișier','',예상파일),
                    ('네트워크',' '+str(ecou_server_intrare.UDP_muta),'C 네트워크 verifica: UDP 한글')]:
                executa_comandă('cc '+Nume+'예제.c -o executa_comandă','Compiled native ARM64 ELF:')
                executa_comandă('./executa_comandă'+전달값,예상결과)
            executa_comandă('cc ExempluDesen.c -o executa_comandă','Compiled native ARM64 ELF:');grafice_comandă='./executa_comandă'
        else:
            for Nume,전달값,예상결과 in [('Rezultat','','PYTHON Rezultat: 안녕하세요 😀'),('Fișier','',예상파일),
                    ('네트워크',' '+str(ecou_server_intrare.UDP_muta),'PYTHON 네트워크 verifica: UDP 한글')]:
                executa_comandă('python '+Nume+'예제.py'+전달값,예상결과)
            grafice_comandă='python ExempluDesen.py'
        buta_desen=buta_OFFSET(grafice_comandă)
        SMS=primi_mesaj('그림을 확인한 ÎNAPOI_VALUE Enter를 누르세요.\r\n'.encode(),buta_desen)
        assert nume_tabel+' 그래픽: 빨강 초록 파랑' in SMS and 'exit 0' not in SMS,SMS
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        transfer_de_fișiere_conexiune.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        RECEIVED_COUNT=bytearray();transfer_de_fișiere_conexiune.retrbinary('RETR 도중.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==b'FTP DURING GRAPHICS';transfer_de_fișiere_conexiune.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            OFFSET_VALUE=(세로좌표*640+610)*3;assert tuple(빛삼원색[OFFSET_VALUE:OFFSET_VALUE+3])==색상,(Limbi_străine,세로좌표,tuple(빛삼원색[OFFSET_VALUE:OFFSET_VALUE+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(KR_date/(Limbi_străine+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in primi_mesaj(b'jkoros-native> ',buta_desen)
        if Limbi_străine=='java':
            buta_fereastră=buta_OFFSET('java ExempluFereastră')
            primi_mesaj('GUI 예제 Pregătiți: ExempluFereastră'.encode(),buta_fereastră)
            def clic_VALUE(가로,Verticală_poziție):
                for buton in (1,0):client.sendall(struct.pack('>BBHH',5,buton,가로,Verticală_poziție))
            time.sleep(.3)
            Anteriorul_IMAGE=Image.frombytes('RGB',(640,480),bytes(화소들()))
            clic_VALUE(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for caracter_VALUE in '한글':누름값(0x1000000|ord(caracter_VALUE));누름값(0x1000000|ord(caracter_VALUE),False)
            for 횟수 in (1,2):
                Pornește=len(transcriere);clic_VALUE(180,242)
                primi_mesaj(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Pornește)
            time.sleep(.3)
            fereastră_desen=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert Anteriorul_IMAGE.crop((110,272,530,300)).tobytes()!=fereastră_desen.crop((110,272,530,300)).tobytes()
            fereastră_desen.save(str(KR_date/'java-swing.png'))
            Pornește=len(transcriere);clic_VALUE(535,105)
            assert 'exit 0' in primi_mesaj(b'jkoros-native> ',Pornește)
        # Download the guest-created bytes through FTP in the same GUI VM.
        Fișier_intrare_nume={'java':'java.txt','c':'c.txt','python':'python.txt'}[Limbi_străine]
        shell('cp '+Fișier_intrare_nume+' /valida.txt')
        RECEIVED_COUNT=bytearray();transfer_de_fișiere_conexiune.retrbinary('RETR valida.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==예상파일.encode()
        shell('echo preserved > ExempluIeșire.'+('py' if Limbi_străine=='python' else Limbi_străine))
        assert 'EXAMPLES READY' in shell('example '+Limbi_străine)
        assert '\npreserved\n' in shell('cat ExempluIeșire.'+('py' if Limbi_străine=='python' else Limbi_străine))
        assert '한/zero_operand Cheie_VALUE, Shift+Space 또는 F9' in shell('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in shell('echo GUI NETWORK TOGETHER')
        transfer_de_fișiere_conexiune.quit();transfer_de_fișiere_conexiune=None;assert 'FTP stopped' in shell('ftpd stop')
        print('PASS '+Limbi_străine+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if transfer_de_fișiere_conexiune:
            try:transfer_de_fișiere_conexiune.close()
            except OSError:pass
        if client:client.close()
        Proces.terminate()
        try:Proces.wait(timeout=8)
        except subprocess.TimeoutExpired:Proces.kill();Proces.wait()
        selector.close();Proces.stdout.close();(KR_date/(Limbi_străine+'-serial.log')).write_bytes(transcriere)


def Pornește():
    KR_date=Project_rădăcină/'build/verification/examples';KR_date.mkdir(parents=True,exist_ok=True)
    validare_raport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_rădăcină/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with ecou_Servere() as ecou_server_intrare:
            for Limbi_străine in ('java','c','python'):
                test_언어(Limbi_străine,ecou_server_intrare,KR_date);validare_raport['languages'].append(Limbi_străine)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert ecou_server_intrare.수신됨==[(zonă_VALUE,date.encode()) for zonă_VALUE,date in 예상결과],ecou_server_intrare.수신됨
            validare_raport['host_network_payloads']=[{'protocol':zonă_VALUE,'text':date.decode()} for zonă_VALUE,date in ecou_server_intrare.수신됨]
        validare_raport.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(KR_date/'report.json').write_text(json.dumps(validare_raport,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Pornește()
