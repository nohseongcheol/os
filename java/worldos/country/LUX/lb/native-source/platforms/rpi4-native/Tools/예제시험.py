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
from Desktop_Vue import EXACT_VALUE
from 예제되돌림서버 import 되돌림서버
from ausféieren_Befeel import projezéieren_Racinn


def test_언어(Sprooch,되돌림서버항목,Mooss_Daten):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    Prozess=subprocess.Popen(['python3',str(projezéieren_Racinn/'Tools/ausféieren_Befeel.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    Selekteur=selectors.DefaultSelector();Selekteur.register(Prozess.stdout,selectors.EVENT_READ)
    대화기록=bytearray();Client=None;Fichier_Transfer_Verbindung=None
    def 수신하기(Markéierung,Laf=0):
        bëennegen_OFFSET=time.monotonic()+60
        while Markéierung not in 대화기록[Laf:]:
            if time.monotonic()>bëennegen_OFFSET or Prozess.poll() is not None:raise AssertionError(대화기록[Laf:].decode('utf-8','replace'))
            for 누름값,_ in Selekteur.select(.1):
                Daten=누름값.fileobj.read(65536)
                if Daten:대화기록.extend(Daten)
        return 대화기록[Laf:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(Symbol_VALUE,누르는중=True):Client.sendall(struct.pack('>BBHI',4,int(누르는중),0,Symbol_VALUE))
    def Start_OFFSET(Zeil):
        Laf=len(대화기록)
        for Zeechecode in Zeil+'\n':
            Symbol_VALUE=0xff0d if Zeechecode=='\n' else ord(Zeechecode) if ord(Zeechecode)<256 else 0x1000000|ord(Zeechecode)
            누름값(Symbol_VALUE);누름값(Symbol_VALUE,False)
        return Laf
    def Shell(Zeil):return 수신하기(b'jkoros-native> ',Start_OFFSET(Zeil))
    def ausféieren_Befeel(Zeil,예상결과):
        SMS=Shell(Zeil);assert 예상결과 in SMS and 'exit 0' in SMS,(Zeil,SMS)
        return SMS
    def 화소들():
        Client.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            Kategorie_VALUE=EXACT_VALUE(Client,1)[0]
            if Kategorie_VALUE==2:continue
            if Kategorie_VALUE==3:
                Element_COUNT=struct.unpack('>I',EXACT_VALUE(Client,7)[3:])[0];EXACT_VALUE(Client,Element_COUNT);continue
            assert Kategorie_VALUE==0,Kategorie_VALUE
            Agab_COUNT=struct.unpack('>H',EXACT_VALUE(Client,3)[1:])[0]
            for _ in range(Agab_COUNT):
                X_Koordinat,세로좌표,너비값,높이값,Zeechesaz=struct.unpack('>HHHHi',EXACT_VALUE(Client,12));assert Zeechesaz==0,Zeechesaz
                Daten=EXACT_VALUE(Client,너비값*높이값*4)
                for ROW_positionéieren in range(높이값):
                    for COLUMN_positionéieren in range(너비값):
                        원본자료=(ROW_positionéieren*너비값+COLUMN_positionéieren)*4;Zil=((세로좌표+ROW_positionéieren)*640+X_Koordinat+COLUMN_positionéieren)*3
                        빛삼원색[Zil:Zil+3]=bytes((Daten[원본자료+2],Daten[원본자료+1],Daten[원본자료]))
            if Agab_COUNT:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        Client=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert EXACT_VALUE(Client,12)==b'RFB 003.008\n';Client.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(Client,EXACT_VALUE(Client,1)[0]);Client.sendall(b'\x01');assert EXACT_VALUE(Client,4)==b'\0'*4
        Client.sendall(b'\x01');초기값=EXACT_VALUE(Client,24);EXACT_VALUE(Client,struct.unpack('>I',초기값[20:])[0])
        Client.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        Client.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in Shell('ftpd start')
        Fichier_Transfer_Verbindung=ftplib.FTP();Fichier_Transfer_Verbindung.encoding='utf-8';Fichier_Transfer_Verbindung.connect('127.0.0.1',파일전송접속번호,timeout=20);Fichier_Transfer_Verbindung.login()
        nëtzlech_Charge_Daten=('GUI와 FTP 동시 사용 '+Sprooch+' 😀\n').encode()
        Fichier_Transfer_Verbindung.storbinary('STOR 함께.txt',io.BytesIO(nëtzlech_Charge_Daten))
        assert nëtzlech_Charge_Daten.decode().strip() in Shell('cat /함께.txt')
        RECEIVED_COUNT=bytearray();Fichier_Transfer_Verbindung.retrbinary('RETR 함께.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==nëtzlech_Charge_Daten;Fichier_Transfer_Verbindung.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        mailen_Lëscht=Shell('ls /example')
        assert all(Numm in mailen_Lëscht for Numm in ('java/','c/','python/','README.md')),mailen_Lëscht
        if Sprooch=='java':
            꾸러미명세=json.loads((projezéieren_Racinn/'build/examples/manifest.json').read_text())
            for Wee,Agab_Punkt in 꾸러미명세.items():
                Shell('cp '+Wee+' /example-check.bin')
                Inhalt_VALUE=bytearray();Fichier_Transfer_Verbindung.retrbinary('RETR example-check.bin',Inhalt_VALUE.extend)
                assert len(Inhalt_VALUE)==Agab_Punkt['bytes'] and hashlib.sha256(Inhalt_VALUE).hexdigest()==Agab_Punkt['sha256'],Wee
            Fichier_Transfer_Verbindung.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            Binär=bytes(range(256))*64
            Fichier_Transfer_Verbindung.storbinary('STOR boundary.bin',io.BytesIO(Binär))
            Inhalt_VALUE=bytearray();Fichier_Transfer_Verbindung.retrbinary('RETR boundary.bin',Inhalt_VALUE.extend)
            assert Inhalt_VALUE==Binär and 'boundary.bin' in Fichier_Transfer_Verbindung.nlst()
            Shell('cp /boundary.bin /boundary-copy.bin')
            Inhalt_VALUE=bytearray();Fichier_Transfer_Verbindung.retrbinary('RETR boundary-copy.bin',Inhalt_VALUE.extend)
            assert Inhalt_VALUE==Binär
            Fichier_Transfer_Verbindung.delete('boundary.bin');Fichier_Transfer_Verbindung.delete('boundary-copy.bin')
        assert '출력예제' in Shell('ls /example/'+Sprooch)
        Shell('cd /example/'+Sprooch)
        Numm_Tabell={'java':'JAVA','c':'C','python':'PYTHON'}[Sprooch]
        예상파일=Numm_Tabell+' Fichier: 한글 Daten 😀\n'
        if Sprooch=='java':
            ausféieren_Befeel('javac 출력예제.java','Compiled:');ausféieren_Befeel('java 출력예제','JAVA 출력: 안녕하세요 😀')
            ausféieren_Befeel('javac 파일예제.java','Compiled:');ausféieren_Befeel('java 파일예제',예상파일)
            ausféieren_Befeel('java 네트워크예제 {} {}'.format(되돌림서버항목.TCP_Port,되돌림서버항목.UDP_Port),'JAVA 네트워크 verifizéieren: TCP UDP 한글')
            Grafiken_Befeel='java 그래픽예제'
        elif Sprooch=='c':
            for Numm,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('Fichier','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.UDP_Port),'C 네트워크 verifizéieren: UDP 한글')]:
                ausféieren_Befeel('cc '+Numm+'예제.c -o ausféieren_Befeel','Compiled native ARM64 ELF:')
                ausféieren_Befeel('./ausféieren_Befeel'+전달값,예상결과)
            ausféieren_Befeel('cc 그래픽예제.c -o ausféieren_Befeel','Compiled native ARM64 ELF:');Grafiken_Befeel='./ausféieren_Befeel'
        else:
            for Numm,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('Fichier','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.UDP_Port),'PYTHON 네트워크 verifizéieren: UDP 한글')]:
                ausféieren_Befeel('python '+Numm+'예제.py'+전달값,예상결과)
            Grafiken_Befeel='python 그래픽예제.py'
        Start_Zeechnung=Start_OFFSET(Grafiken_Befeel)
        SMS=수신하기('그림을 확인한 Zeréck_VALUE Enter를 누르세요.\r\n'.encode(),Start_Zeechnung)
        assert Numm_Tabell+' 그래픽: 빨강 초록 파랑' in SMS and 'exit 0' not in SMS,SMS
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        Fichier_Transfer_Verbindung.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        RECEIVED_COUNT=bytearray();Fichier_Transfer_Verbindung.retrbinary('RETR 도중.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==b'FTP DURING GRAPHICS';Fichier_Transfer_Verbindung.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            OFFSET_VALUE=(세로좌표*640+610)*3;assert tuple(빛삼원색[OFFSET_VALUE:OFFSET_VALUE+3])==색상,(Sprooch,세로좌표,tuple(빛삼원색[OFFSET_VALUE:OFFSET_VALUE+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(Mooss_Daten/(Sprooch+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',Start_Zeechnung)
        if Sprooch=='java':
            Start_Fënster=Start_OFFSET('java 창예제')
            수신하기('GUI 예제 Préparéieren: 창예제'.encode(),Start_Fënster)
            def klicken_VALUE(가로,Vertikal_positionéieren):
                for Tast in (1,0):Client.sendall(struct.pack('>BBHH',5,Tast,가로,Vertikal_positionéieren))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            klicken_VALUE(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for Zeechen_VALUE in '한글':누름값(0x1000000|ord(Zeechen_VALUE));누름값(0x1000000|ord(Zeechen_VALUE),False)
            for 횟수 in (1,2):
                Laf=len(대화기록);klicken_VALUE(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Laf)
            time.sleep(.3)
            Fënster_Zeechnung=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=Fënster_Zeechnung.crop((110,272,530,300)).tobytes()
            Fënster_Zeechnung.save(str(Mooss_Daten/'java-swing.png'))
            Laf=len(대화기록);klicken_VALUE(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',Laf)
        # Download the guest-created bytes through FTP in the same GUI VM.
        Fichier_Agab_Numm={'java':'java.txt','c':'c.txt','python':'python.txt'}[Sprooch]
        Shell('cp '+Fichier_Agab_Numm+' /validéieren.txt')
        RECEIVED_COUNT=bytearray();Fichier_Transfer_Verbindung.retrbinary('RETR validéieren.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==예상파일.encode()
        Shell('echo preserved > 출력예제.'+('py' if Sprooch=='python' else Sprooch))
        assert 'EXAMPLES READY' in Shell('example '+Sprooch)
        assert '\npreserved\n' in Shell('cat 출력예제.'+('py' if Sprooch=='python' else Sprooch))
        assert '한/영 Tast_VALUE, Shift+Space 또는 F9' in Shell('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in Shell('echo GUI NETWORK TOGETHER')
        Fichier_Transfer_Verbindung.quit();Fichier_Transfer_Verbindung=None;assert 'FTP stopped' in Shell('ftpd stop')
        print('PASS '+Sprooch+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if Fichier_Transfer_Verbindung:
            try:Fichier_Transfer_Verbindung.close()
            except OSError:pass
        if Client:Client.close()
        Prozess.terminate()
        try:Prozess.wait(timeout=8)
        except subprocess.TimeoutExpired:Prozess.kill();Prozess.wait()
        Selekteur.close();Prozess.stdout.close();(Mooss_Daten/(Sprooch+'-serial.log')).write_bytes(대화기록)


def Laf():
    Mooss_Daten=projezéieren_Racinn/'build/verification/examples';Mooss_Daten.mkdir(parents=True,exist_ok=True)
    Validatioun_mellen={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((projezéieren_Racinn/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for Sprooch in ('java','c','python'):
                test_언어(Sprooch,되돌림서버항목,Mooss_Daten);Validatioun_mellen['languages'].append(Sprooch)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(Kategorie_VALUE,Daten.encode()) for Kategorie_VALUE,Daten in 예상결과],되돌림서버항목.수신됨
            Validatioun_mellen['host_network_payloads']=[{'protocol':Kategorie_VALUE,'text':Daten.decode()} for Kategorie_VALUE,Daten in 되돌림서버항목.수신됨]
        Validatioun_mellen.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(Mooss_Daten/'report.json').write_text(json.dumps(Validatioun_mellen,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Laf()
