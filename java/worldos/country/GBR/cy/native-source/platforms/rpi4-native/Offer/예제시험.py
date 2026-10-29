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
from bwrdd_gwaith_Gwedd import EXACT_VALUE
from 예제되돌림서버 import 되돌림서버
from Gweithredu_gorchymyn import prosiect_gwraidd


def test_언어(Iaith,되돌림서버항목,mesur_data):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));ffeil_trosglwyddo_rhif_porth=임시자원.getsockname()[1]
    Proses=subprocess.Popen(['python3',str(prosiect_gwraidd/'Offer/Gweithredu_gorchymyn.py'),'--desktop','--network','--port','0','--ftp-port',str(ffeil_trosglwyddo_rhif_porth)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    dewisydd=selectors.DefaultSelector();dewisydd.register(Proses.stdout,selectors.EVENT_READ)
    대화기록=bytearray();cleient=None;ffeil_trosglwyddo_cyswllt=None
    def 수신하기(확인표시,Gweithredu_2=0):
        gorffen_OFFSET=time.monotonic()+60
        while 확인표시 not in 대화기록[Gweithredu_2:]:
            if time.monotonic()>gorffen_OFFSET or Proses.poll() is not None:raise AssertionError(대화기록[Gweithredu_2:].decode('utf-8','replace'))
            for 누름값,_ in dewisydd.select(.1):
                data=누름값.fileobj.read(65536)
                if data:대화기록.extend(data)
        return 대화기록[Gweithredu_2:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(symbol_VALUE,누르는중=True):cleient.sendall(struct.pack('>BBHI',4,int(누르는중),0,symbol_VALUE))
    def START_OFFSET(llinell):
        Gweithredu_2=len(대화기록)
        for cod_nod in llinell+'\n':
            symbol_VALUE=0xff0d if cod_nod=='\n' else ord(cod_nod) if ord(cod_nod)<256 else 0x1000000|ord(cod_nod)
            누름값(symbol_VALUE);누름값(symbol_VALUE,False)
        return Gweithredu_2
    def cragen(llinell):return 수신하기(b'jkoros-native> ',START_OFFSET(llinell))
    def Gweithredu_gorchymyn(llinell,예상결과):
        Testun=cragen(llinell);assert 예상결과 in Testun and 'exit 0' in Testun,(llinell,Testun)
        return Testun
    def 화소들():
        cleient.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            ardal_VALUE=EXACT_VALUE(cleient,1)[0]
            if ardal_VALUE==2:continue
            if ardal_VALUE==3:
                eitem_COUNT=struct.unpack('>I',EXACT_VALUE(cleient,7)[3:])[0];EXACT_VALUE(cleient,eitem_COUNT);continue
            assert ardal_VALUE==0,ardal_VALUE
            cofnod_COUNT=struct.unpack('>H',EXACT_VALUE(cleient,3)[1:])[0]
            for _ in range(cofnod_COUNT):
                cyfesuryn_x,Y_cyfesuryn,너비값,높이값,set_nodau=struct.unpack('>HHHHi',EXACT_VALUE(cleient,12));assert set_nodau==0,set_nodau
                data=EXACT_VALUE(cleient,너비값*높이값*4)
                for ROW_safle in range(높이값):
                    for COLUMN_safle in range(너비값):
                        원본자료=(ROW_safle*너비값+COLUMN_safle)*4;targed=((Y_cyfesuryn+ROW_safle)*640+cyfesuryn_x+COLUMN_safle)*3
                        빛삼원색[targed:targed+3]=bytes((data[원본자료+2],data[원본자료+1],data[원본자료]))
            if cofnod_COUNT:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        rhif_porth=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        cleient=socket.create_connection(('127.0.0.1',rhif_porth),timeout=10)
        assert EXACT_VALUE(cleient,12)==b'RFB 003.008\n';cleient.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(cleient,EXACT_VALUE(cleient,1)[0]);cleient.sendall(b'\x01');assert EXACT_VALUE(cleient,4)==b'\0'*4
        cleient.sendall(b'\x01');초기값=EXACT_VALUE(cleient,24);EXACT_VALUE(cleient,struct.unpack('>I',초기값[20:])[0])
        cleient.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        cleient.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in cragen('ftpd start')
        ffeil_trosglwyddo_cyswllt=ftplib.FTP();ffeil_trosglwyddo_cyswllt.encoding='utf-8';ffeil_trosglwyddo_cyswllt.connect('127.0.0.1',ffeil_trosglwyddo_rhif_porth,timeout=20);ffeil_trosglwyddo_cyswllt.login()
        llwyth_uchaf_data=('GUI와 FTP 동시 사용 '+Iaith+' 😀\n').encode()
        ffeil_trosglwyddo_cyswllt.storbinary('STOR 함께.txt',io.BytesIO(llwyth_uchaf_data))
        assert llwyth_uchaf_data.decode().strip() in cragen('cat /함께.txt')
        RECEIVED_COUNT=bytearray();ffeil_trosglwyddo_cyswllt.retrbinary('RETR 함께.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==llwyth_uchaf_data;ffeil_trosglwyddo_cyswllt.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        anfon_Rhestr=cragen('ls /example')
        assert all(Enw in anfon_Rhestr for Enw in ('java/','c/','python/','README.md')),anfon_Rhestr
        if Iaith=='java':
            꾸러미명세=json.loads((prosiect_gwraidd/'build/examples/manifest.json').read_text())
            for LLWYBR,cofnod_p in 꾸러미명세.items():
                cragen('cp '+LLWYBR+' /example-check.bin')
                Cynnwys_VALUE=bytearray();ffeil_trosglwyddo_cyswllt.retrbinary('RETR example-check.bin',Cynnwys_VALUE.extend)
                assert len(Cynnwys_VALUE)==cofnod_p['bytes'] and hashlib.sha256(Cynnwys_VALUE).hexdigest()==cofnod_p['sha256'],LLWYBR
            ffeil_trosglwyddo_cyswllt.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            deuaidd=bytes(range(256))*64
            ffeil_trosglwyddo_cyswllt.storbinary('STOR boundary.bin',io.BytesIO(deuaidd))
            Cynnwys_VALUE=bytearray();ffeil_trosglwyddo_cyswllt.retrbinary('RETR boundary.bin',Cynnwys_VALUE.extend)
            assert Cynnwys_VALUE==deuaidd and 'boundary.bin' in ffeil_trosglwyddo_cyswllt.nlst()
            cragen('cp /boundary.bin /boundary-copy.bin')
            Cynnwys_VALUE=bytearray();ffeil_trosglwyddo_cyswllt.retrbinary('RETR boundary-copy.bin',Cynnwys_VALUE.extend)
            assert Cynnwys_VALUE==deuaidd
            ffeil_trosglwyddo_cyswllt.delete('boundary.bin');ffeil_trosglwyddo_cyswllt.delete('boundary-copy.bin')
        assert '출력예제' in cragen('ls /example/'+Iaith)
        cragen('cd /example/'+Iaith)
        enw_tabl={'java':'JAVA','c':'C','python':'PYTHON'}[Iaith]
        예상파일=enw_tabl+' Ffeil: 한글 data 😀\n'
        if Iaith=='java':
            Gweithredu_gorchymyn('javac 출력예제.java','Compiled:');Gweithredu_gorchymyn('java 출력예제','JAVA Allbwn: 안녕하세요 😀')
            Gweithredu_gorchymyn('javac 파일예제.java','Compiled:');Gweithredu_gorchymyn('java 파일예제',예상파일)
            Gweithredu_gorchymyn('java 네트워크예제 {} {}'.format(되돌림서버항목.TCP_porth,되돌림서버항목.UDP_porth),'JAVA 네트워크 dilysu: TCP UDP 한글')
            graffeg_gorchymyn='java 그래픽예제'
        elif Iaith=='c':
            for Enw,전달값,예상결과 in [('Allbwn','', 'C Allbwn: 안녕하세요 😀'),('Ffeil','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.UDP_porth),'C 네트워크 dilysu: UDP 한글')]:
                Gweithredu_gorchymyn('cc '+Enw+'예제.c -o Gweithredu_gorchymyn','Compiled native ARM64 ELF:')
                Gweithredu_gorchymyn('./Gweithredu_gorchymyn'+전달값,예상결과)
            Gweithredu_gorchymyn('cc 그래픽예제.c -o Gweithredu_gorchymyn','Compiled native ARM64 ELF:');graffeg_gorchymyn='./Gweithredu_gorchymyn'
        else:
            for Enw,전달값,예상결과 in [('Allbwn','','PYTHON Allbwn: 안녕하세요 😀'),('Ffeil','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.UDP_porth),'PYTHON 네트워크 dilysu: UDP 한글')]:
                Gweithredu_gorchymyn('python '+Enw+'예제.py'+전달값,예상결과)
            graffeg_gorchymyn='python 그래픽예제.py'
        START_lluniad=START_OFFSET(graffeg_gorchymyn)
        Testun=수신하기('그림을 확인한 BACK_VALUE Enter를 누르세요.\r\n'.encode(),START_lluniad)
        assert enw_tabl+' 그래픽: 빨강 초록 파랑' in Testun and 'exit 0' not in Testun,Testun
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        ffeil_trosglwyddo_cyswllt.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        RECEIVED_COUNT=bytearray();ffeil_trosglwyddo_cyswllt.retrbinary('RETR 도중.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==b'FTP DURING GRAPHICS';ffeil_trosglwyddo_cyswllt.delete('도중.txt')
        빛삼원색=화소들()
        for Y_cyfesuryn,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            OFFSET_VALUE=(Y_cyfesuryn*640+610)*3;assert tuple(빛삼원색[OFFSET_VALUE:OFFSET_VALUE+3])==색상,(Iaith,Y_cyfesuryn,tuple(빛삼원색[OFFSET_VALUE:OFFSET_VALUE+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(mesur_data/(Iaith+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',START_lluniad)
        if Iaith=='java':
            START_ffenestr=START_OFFSET('java 창예제')
            수신하기('GUI 예제 Paratoi: 창예제'.encode(),START_ffenestr)
            def clicio_VALUE(가로,Ar_i_fyny_safle):
                for botwm in (1,0):cleient.sendall(struct.pack('>BBHH',5,botwm,가로,Ar_i_fyny_safle))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            clicio_VALUE(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for nod_VALUE in '한글':누름값(0x1000000|ord(nod_VALUE));누름값(0x1000000|ord(nod_VALUE),False)
            for 횟수 in (1,2):
                Gweithredu_2=len(대화기록);clicio_VALUE(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Gweithredu_2)
            time.sleep(.3)
            ffenestr_lluniad=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=ffenestr_lluniad.crop((110,272,530,300)).tobytes()
            ffenestr_lluniad.save(str(mesur_data/'java-swing.png'))
            Gweithredu_2=len(대화기록);clicio_VALUE(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',Gweithredu_2)
        # Download the guest-created bytes through FTP in the same GUI VM.
        ffeil_cofnod_enw={'java':'java.txt','c':'c.txt','python':'python.txt'}[Iaith]
        cragen('cp '+ffeil_cofnod_enw+' /dilysu_5fb2b747.txt')
        RECEIVED_COUNT=bytearray();ffeil_trosglwyddo_cyswllt.retrbinary('RETR dilysu_5fb2b747.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==예상파일.encode()
        cragen('echo preserved > 출력예제.'+('py' if Iaith=='python' else Iaith))
        assert 'EXAMPLES READY' in cragen('example '+Iaith)
        assert '\npreserved\n' in cragen('cat 출력예제.'+('py' if Iaith=='python' else Iaith))
        assert '한/영 bysell_VALUE, Shift+Space 또는 F9' in cragen('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in cragen('echo GUI NETWORK TOGETHER')
        ffeil_trosglwyddo_cyswllt.quit();ffeil_trosglwyddo_cyswllt=None;assert 'FTP stopped' in cragen('ftpd stop')
        print('PASS '+Iaith+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if ffeil_trosglwyddo_cyswllt:
            try:ffeil_trosglwyddo_cyswllt.close()
            except OSError:pass
        if cleient:cleient.close()
        Proses.terminate()
        try:Proses.wait(timeout=8)
        except subprocess.TimeoutExpired:Proses.kill();Proses.wait()
        dewisydd.close();Proses.stdout.close();(mesur_data/(Iaith+'-serial.log')).write_bytes(대화기록)


def Gweithredu_2():
    mesur_data=prosiect_gwraidd/'build/verification/examples';mesur_data.mkdir(parents=True,exist_ok=True)
    dilysu_adrodd={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((prosiect_gwraidd/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for Iaith in ('java','c','python'):
                test_언어(Iaith,되돌림서버항목,mesur_data);dilysu_adrodd['languages'].append(Iaith)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(ardal_VALUE,data.encode()) for ardal_VALUE,data in 예상결과],되돌림서버항목.수신됨
            dilysu_adrodd['host_network_payloads']=[{'protocol':ardal_VALUE,'text':data.decode()} for ardal_VALUE,data in 되돌림서버항목.수신됨]
        dilysu_adrodd.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(mesur_data/'report.json').write_text(json.dumps(dilysu_adrodd,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Gweithredu_2()
