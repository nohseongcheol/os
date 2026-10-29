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
from stasjonær_vise import EXACT_VALUE
from 예제되돌림서버 import 되돌림서버
from Utfør_kommando import spegle_rot


def test_언어(Språk,되돌림서버항목,forretningsmål_data):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));fil_Overfør_portnummer=임시자원.getsockname()[1]
    Prosess=subprocess.Popen(['python3',str(spegle_rot/'Verktøy/Utfør_kommando.py'),'--desktop','--network','--port','0','--ftp-port',str(fil_Overfør_portnummer)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    veljar=selectors.DefaultSelector();veljar.register(Prosess.stdout,selectors.EVENT_READ)
    대화기록=bytearray();klient=None;fil_Overfør_kontakt=None
    def 수신하기(확인표시,Køyr_2=0):
        avslutte_OFFSET=time.monotonic()+60
        while 확인표시 not in 대화기록[Køyr_2:]:
            if time.monotonic()>avslutte_OFFSET or Prosess.poll() is not None:raise AssertionError(대화기록[Køyr_2:].decode('utf-8','replace'))
            for 누름값,_ in veljar.select(.1):
                data=누름값.fileobj.read(65536)
                if data:대화기록.extend(data)
        return 대화기록[Køyr_2:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(symbol_VALUE,누르는중=True):klient.sendall(struct.pack('>BBHI',4,int(누르는중),0,symbol_VALUE))
    def START_OFFSET(linje):
        Køyr_2=len(대화기록)
        for teiknkode in linje+'\n':
            symbol_VALUE=0xff0d if teiknkode=='\n' else ord(teiknkode) if ord(teiknkode)<256 else 0x1000000|ord(teiknkode)
            누름값(symbol_VALUE);누름값(symbol_VALUE,False)
        return Køyr_2
    def grensesnitt(linje):return 수신하기(b'jkoros-native> ',START_OFFSET(linje))
    def Utfør_kommando(linje,예상결과):
        Tekst=grensesnitt(linje);assert 예상결과 in Tekst and 'exit 0' in Tekst,(linje,Tekst)
        return Tekst
    def 화소들():
        klient.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            kategori_VALUE=EXACT_VALUE(klient,1)[0]
            if kategori_VALUE==2:continue
            if kategori_VALUE==3:
                vare_COUNT=struct.unpack('>I',EXACT_VALUE(klient,7)[3:])[0];EXACT_VALUE(klient,vare_COUNT);continue
            assert kategori_VALUE==0,kategori_VALUE
            oppføring_COUNT=struct.unpack('>H',EXACT_VALUE(klient,3)[1:])[0]
            for _ in range(oppføring_COUNT):
                x_koordinat,Y_koordinat,너비값,높이값,teiknsett=struct.unpack('>HHHHi',EXACT_VALUE(klient,12));assert teiknsett==0,teiknsett
                data=EXACT_VALUE(klient,너비값*높이값*4)
                for ROW_plassere in range(높이값):
                    for COLUMN_plassere in range(너비값):
                        원본자료=(ROW_plassere*너비값+COLUMN_plassere)*4;mål=((Y_koordinat+ROW_plassere)*640+x_koordinat+COLUMN_plassere)*3
                        빛삼원색[mål:mål+3]=bytes((data[원본자료+2],data[원본자료+1],data[원본자료]))
            if oppføring_COUNT:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        portnummer=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        klient=socket.create_connection(('127.0.0.1',portnummer),timeout=10)
        assert EXACT_VALUE(klient,12)==b'RFB 003.008\n';klient.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(klient,EXACT_VALUE(klient,1)[0]);klient.sendall(b'\x01');assert EXACT_VALUE(klient,4)==b'\0'*4
        klient.sendall(b'\x01');초기값=EXACT_VALUE(klient,24);EXACT_VALUE(klient,struct.unpack('>I',초기값[20:])[0])
        klient.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        klient.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in grensesnitt('ftpd start')
        fil_Overfør_kontakt=ftplib.FTP();fil_Overfør_kontakt.encoding='utf-8';fil_Overfør_kontakt.connect('127.0.0.1',fil_Overfør_portnummer,timeout=20);fil_Overfør_kontakt.login()
        nyttelast_data=('GUI와 FTP 동시 사용 '+Språk+' 😀\n').encode()
        fil_Overfør_kontakt.storbinary('STOR 함께.txt',io.BytesIO(nyttelast_data))
        assert nyttelast_data.decode().strip() in grensesnitt('cat /함께.txt')
        RECEIVED_COUNT=bytearray();fil_Overfør_kontakt.retrbinary('RETR 함께.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==nyttelast_data;fil_Overfør_kontakt.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        sende_Liste=grensesnitt('ls /example')
        assert all(Namn in sende_Liste for Namn in ('java/','c/','python/','README.md')),sende_Liste
        if Språk=='java':
            꾸러미명세=json.loads((spegle_rot/'build/examples/manifest.json').read_text())
            for STIGE,oppføring_p in 꾸러미명세.items():
                grensesnitt('cp '+STIGE+' /example-check.bin')
                Innhald_VALUE=bytearray();fil_Overfør_kontakt.retrbinary('RETR example-check.bin',Innhald_VALUE.extend)
                assert len(Innhald_VALUE)==oppføring_p['bytes'] and hashlib.sha256(Innhald_VALUE).hexdigest()==oppføring_p['sha256'],STIGE
            fil_Overfør_kontakt.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            binær=bytes(range(256))*64
            fil_Overfør_kontakt.storbinary('STOR boundary.bin',io.BytesIO(binær))
            Innhald_VALUE=bytearray();fil_Overfør_kontakt.retrbinary('RETR boundary.bin',Innhald_VALUE.extend)
            assert Innhald_VALUE==binær and 'boundary.bin' in fil_Overfør_kontakt.nlst()
            grensesnitt('cp /boundary.bin /boundary-copy.bin')
            Innhald_VALUE=bytearray();fil_Overfør_kontakt.retrbinary('RETR boundary-copy.bin',Innhald_VALUE.extend)
            assert Innhald_VALUE==binær
            fil_Overfør_kontakt.delete('boundary.bin');fil_Overfør_kontakt.delete('boundary-copy.bin')
        assert '출력예제' in grensesnitt('ls /example/'+Språk)
        grensesnitt('cd /example/'+Språk)
        namn_tabell={'java':'JAVA','c':'C','python':'PYTHON'}[Språk]
        예상파일=namn_tabell+' Fil: 한글 data 😀\n'
        if Språk=='java':
            Utfør_kommando('javac 출력예제.java','Compiled:');Utfør_kommando('java 출력예제','JAVA Utdata: 안녕하세요 😀')
            Utfør_kommando('javac 파일예제.java','Compiled:');Utfør_kommando('java 파일예제',예상파일)
            Utfør_kommando('java 네트워크예제 {} {}'.format(되돌림서버항목.TCP_port,되돌림서버항목.전문접속번호),'JAVA 네트워크 stadfeste: TCP UDP 한글')
            grafikk_kommando='java 그래픽예제'
        elif Språk=='c':
            for Namn,전달값,예상결과 in [('Utdata','', 'C Utdata: 안녕하세요 😀'),('Fil','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 stadfeste: UDP 한글')]:
                Utfør_kommando('cc '+Namn+'예제.c -o Utfør_kommando','Compiled native ARM64 ELF:')
                Utfør_kommando('./Utfør_kommando'+전달값,예상결과)
            Utfør_kommando('cc 그래픽예제.c -o Utfør_kommando','Compiled native ARM64 ELF:');grafikk_kommando='./Utfør_kommando'
        else:
            for Namn,전달값,예상결과 in [('Utdata','','PYTHON Utdata: 안녕하세요 😀'),('Fil','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 stadfeste: UDP 한글')]:
                Utfør_kommando('python '+Namn+'예제.py'+전달값,예상결과)
            grafikk_kommando='python 그래픽예제.py'
        START_teikning=START_OFFSET(grafikk_kommando)
        Tekst=수신하기('그림을 확인한 TILBAKE_VALUE Enter를 누르세요.\r\n'.encode(),START_teikning)
        assert namn_tabell+' 그래픽: 빨강 초록 파랑' in Tekst and 'exit 0' not in Tekst,Tekst
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        fil_Overfør_kontakt.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        RECEIVED_COUNT=bytearray();fil_Overfør_kontakt.retrbinary('RETR 도중.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==b'FTP DURING GRAPHICS';fil_Overfør_kontakt.delete('도중.txt')
        빛삼원색=화소들()
        for Y_koordinat,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            OFFSET_VALUE=(Y_koordinat*640+610)*3;assert tuple(빛삼원색[OFFSET_VALUE:OFFSET_VALUE+3])==색상,(Språk,Y_koordinat,tuple(빛삼원색[OFFSET_VALUE:OFFSET_VALUE+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(forretningsmål_data/(Språk+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',START_teikning)
        if Språk=='java':
            START_vindauge=START_OFFSET('java 창예제')
            수신하기('GUI 예제 Klargjer: 창예제'.encode(),START_vindauge)
            def klikk_VALUE(가로,vertikalvising_plassere):
                for knapp in (1,0):klient.sendall(struct.pack('>BBHH',5,knapp,가로,vertikalvising_plassere))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            klikk_VALUE(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for teikn_VALUE in '한글':누름값(0x1000000|ord(teikn_VALUE));누름값(0x1000000|ord(teikn_VALUE),False)
            for 횟수 in (1,2):
                Køyr_2=len(대화기록);klikk_VALUE(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Køyr_2)
            time.sleep(.3)
            vindauge_teikning=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=vindauge_teikning.crop((110,272,530,300)).tobytes()
            vindauge_teikning.save(str(forretningsmål_data/'java-swing.png'))
            Køyr_2=len(대화기록);klikk_VALUE(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',Køyr_2)
        # Download the guest-created bytes through FTP in the same GUI VM.
        fil_oppføring_namn={'java':'java.txt','c':'c.txt','python':'python.txt'}[Språk]
        grensesnitt('cp '+fil_oppføring_namn+' /bekrefte.txt')
        RECEIVED_COUNT=bytearray();fil_Overfør_kontakt.retrbinary('RETR bekrefte.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==예상파일.encode()
        grensesnitt('echo preserved > 출력예제.'+('py' if Språk=='python' else Språk))
        assert 'EXAMPLES READY' in grensesnitt('example '+Språk)
        assert '\npreserved\n' in grensesnitt('cat 출력예제.'+('py' if Språk=='python' else Språk))
        assert '한/영 tast_VALUE, Shift+Space 또는 F9' in grensesnitt('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in grensesnitt('echo GUI NETWORK TOGETHER')
        fil_Overfør_kontakt.quit();fil_Overfør_kontakt=None;assert 'FTP stopped' in grensesnitt('ftpd stop')
        print('PASS '+Språk+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if fil_Overfør_kontakt:
            try:fil_Overfør_kontakt.close()
            except OSError:pass
        if klient:klient.close()
        Prosess.terminate()
        try:Prosess.wait(timeout=8)
        except subprocess.TimeoutExpired:Prosess.kill();Prosess.wait()
        veljar.close();Prosess.stdout.close();(forretningsmål_data/(Språk+'-serial.log')).write_bytes(대화기록)


def Køyr_2():
    forretningsmål_data=spegle_rot/'build/verification/examples';forretningsmål_data.mkdir(parents=True,exist_ok=True)
    validering_rapport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((spegle_rot/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for Språk in ('java','c','python'):
                test_언어(Språk,되돌림서버항목,forretningsmål_data);validering_rapport['languages'].append(Språk)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(kategori_VALUE,data.encode()) for kategori_VALUE,data in 예상결과],되돌림서버항목.수신됨
            validering_rapport['host_network_payloads']=[{'protocol':kategori_VALUE,'text':data.decode()} for kategori_VALUE,data in 되돌림서버항목.수신됨]
        validering_rapport.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(forretningsmål_data/'report.json').write_text(json.dumps(validering_rapport,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Køyr_2()
