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
from desktop_View import EXACT_VALUE
from 예제되돌림서버 import 되돌림서버
from Mag_execute_utos import Project_root


def test_언어(Wika,되돌림서버항목,sukat_data):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));file_lipat_numero_ng_port=임시자원.getsockname()[1]
    Proseso=subprocess.Popen(['python3',str(Project_root/'Mga_Tool/Mag_execute_utos.py'),'--desktop','--network','--port','0','--ftp-port',str(file_lipat_numero_ng_port)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    tagapili=selectors.DefaultSelector();tagapili.register(Proseso.stdout,selectors.EVENT_READ)
    대화기록=bytearray();client=None;file_lipat_koneksyon=None
    def 수신하기(확인표시,run=0):
        tapusin_OFFSET=time.monotonic()+60
        while 확인표시 not in 대화기록[run:]:
            if time.monotonic()>tapusin_OFFSET or Proseso.poll() is not None:raise AssertionError(대화기록[run:].decode('utf-8','replace'))
            for 누름값,_ in tagapili.select(.1):
                data=누름값.fileobj.read(65536)
                if data:대화기록.extend(data)
        return 대화기록[run:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(simbolo_VALUE,누르는중=True):client.sendall(struct.pack('>BBHI',4,int(누르는중),0,simbolo_VALUE))
    def Start_OFFSET(linya):
        run=len(대화기록)
        for character_code in linya+'\n':
            simbolo_VALUE=0xff0d if character_code=='\n' else ord(character_code) if ord(character_code)<256 else 0x1000000|ord(character_code)
            누름값(simbolo_VALUE);누름값(simbolo_VALUE,False)
        return run
    def shell(linya):return 수신하기(b'jkoros-native> ',Start_OFFSET(linya))
    def Mag_execute_utos(linya,예상결과):
        SMS=shell(linya);assert 예상결과 in SMS and 'exit 0' in SMS,(linya,SMS)
        return SMS
    def 화소들():
        client.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            kategorya_VALUE=EXACT_VALUE(client,1)[0]
            if kategorya_VALUE==2:continue
            if kategorya_VALUE==3:
                item_COUNT=struct.unpack('>I',EXACT_VALUE(client,7)[3:])[0];EXACT_VALUE(client,item_COUNT);continue
            assert kategorya_VALUE==0,kategorya_VALUE
            pagpasok_COUNT=struct.unpack('>H',EXACT_VALUE(client,3)[1:])[0]
            for _ in range(pagpasok_COUNT):
                x_coordinate,Y_button_coordinate,너비값,높이값,set_ng_karakter=struct.unpack('>HHHHi',EXACT_VALUE(client,12));assert set_ng_karakter==0,set_ng_karakter
                data=EXACT_VALUE(client,너비값*높이값*4)
                for ROW_posisyon in range(높이값):
                    for kolum_posisyon in range(너비값):
                        원본자료=(ROW_posisyon*너비값+kolum_posisyon)*4;layunin=((Y_button_coordinate+ROW_posisyon)*640+x_coordinate+kolum_posisyon)*3
                        빛삼원색[layunin:layunin+3]=bytes((data[원본자료+2],data[원본자료+1],data[원본자료]))
            if pagpasok_COUNT:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        numero_ng_port=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        client=socket.create_connection(('127.0.0.1',numero_ng_port),timeout=10)
        assert EXACT_VALUE(client,12)==b'RFB 003.008\n';client.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(client,EXACT_VALUE(client,1)[0]);client.sendall(b'\x01');assert EXACT_VALUE(client,4)==b'\0'*4
        client.sendall(b'\x01');초기값=EXACT_VALUE(client,24);EXACT_VALUE(client,struct.unpack('>I',초기값[20:])[0])
        client.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        client.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in shell('ftpd start')
        file_lipat_koneksyon=ftplib.FTP();file_lipat_koneksyon.encoding='utf-8';file_lipat_koneksyon.connect('127.0.0.1',file_lipat_numero_ng_port,timeout=20);file_lipat_koneksyon.login()
        payload_data=('GUI와 FTP 동시 사용 '+Wika+' 😀\n').encode()
        file_lipat_koneksyon.storbinary('STOR 함께.txt',io.BytesIO(payload_data))
        assert payload_data.decode().strip() in shell('cat /함께.txt')
        RECEIVED_COUNT=bytearray();file_lipat_koneksyon.retrbinary('RETR 함께.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==payload_data;file_lipat_koneksyon.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        i_email_list=shell('ls /example')
        assert all(pangalan in i_email_list for pangalan in ('java/','c/','python/','README.md')),i_email_list
        if Wika=='java':
            꾸러미명세=json.loads((Project_root/'build/examples/manifest.json').read_text())
            for path,pagpasok_point in 꾸러미명세.items():
                shell('cp '+path+' /example-check.bin')
                Nilalaman_VALUE=bytearray();file_lipat_koneksyon.retrbinary('RETR example-check.bin',Nilalaman_VALUE.extend)
                assert len(Nilalaman_VALUE)==pagpasok_point['bytes'] and hashlib.sha256(Nilalaman_VALUE).hexdigest()==pagpasok_point['sha256'],path
            file_lipat_koneksyon.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            binary=bytes(range(256))*64
            file_lipat_koneksyon.storbinary('STOR boundary.bin',io.BytesIO(binary))
            Nilalaman_VALUE=bytearray();file_lipat_koneksyon.retrbinary('RETR boundary.bin',Nilalaman_VALUE.extend)
            assert Nilalaman_VALUE==binary and 'boundary.bin' in file_lipat_koneksyon.nlst()
            shell('cp /boundary.bin /boundary-copy.bin')
            Nilalaman_VALUE=bytearray();file_lipat_koneksyon.retrbinary('RETR boundary-copy.bin',Nilalaman_VALUE.extend)
            assert Nilalaman_VALUE==binary
            file_lipat_koneksyon.delete('boundary.bin');file_lipat_koneksyon.delete('boundary-copy.bin')
        assert '출력예제' in shell('ls /example/'+Wika)
        shell('cd /example/'+Wika)
        pangalan_talahanayan={'java':'JAVA','c':'C','python':'PYTHON'}[Wika]
        예상파일=pangalan_talahanayan+' file: 한글 data 😀\n'
        if Wika=='java':
            Mag_execute_utos('javac 출력예제.java','Compiled:');Mag_execute_utos('java 출력예제','JAVA 출력: 안녕하세요 😀')
            Mag_execute_utos('javac 파일예제.java','Compiled:');Mag_execute_utos('java 파일예제',예상파일)
            Mag_execute_utos('java 네트워크예제 {} {}'.format(되돌림서버항목.TCP_port,되돌림서버항목.UDP_port),'JAVA 네트워크 tiyakin_kumpirmahin: TCP UDP 한글')
            graphics_utos='java 그래픽예제'
        elif Wika=='c':
            for pangalan,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('file','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.UDP_port),'C 네트워크 tiyakin_kumpirmahin: UDP 한글')]:
                Mag_execute_utos('cc '+pangalan+'예제.c -o Mag_execute_utos','Compiled native ARM64 ELF:')
                Mag_execute_utos('./Mag_execute_utos'+전달값,예상결과)
            Mag_execute_utos('cc 그래픽예제.c -o Mag_execute_utos','Compiled native ARM64 ELF:');graphics_utos='./Mag_execute_utos'
        else:
            for pangalan,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('file','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.UDP_port),'PYTHON 네트워크 tiyakin_kumpirmahin: UDP 한글')]:
                Mag_execute_utos('python '+pangalan+'예제.py'+전달값,예상결과)
            graphics_utos='python 그래픽예제.py'
        Start_iginuhit=Start_OFFSET(graphics_utos)
        SMS=수신하기('그림을 확인한 Bumalik_VALUE Enter를 누르세요.\r\n'.encode(),Start_iginuhit)
        assert pangalan_talahanayan+' 그래픽: 빨강 초록 파랑' in SMS and 'exit 0' not in SMS,SMS
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        file_lipat_koneksyon.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        RECEIVED_COUNT=bytearray();file_lipat_koneksyon.retrbinary('RETR 도중.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==b'FTP DURING GRAPHICS';file_lipat_koneksyon.delete('도중.txt')
        빛삼원색=화소들()
        for Y_button_coordinate,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            OFFSET_VALUE=(Y_button_coordinate*640+610)*3;assert tuple(빛삼원색[OFFSET_VALUE:OFFSET_VALUE+3])==색상,(Wika,Y_button_coordinate,tuple(빛삼원색[OFFSET_VALUE:OFFSET_VALUE+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(sukat_data/(Wika+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',Start_iginuhit)
        if Wika=='java':
            Start_window=Start_OFFSET('java 창예제')
            수신하기('GUI 예제 Ihanda: 창예제'.encode(),Start_window)
            def magklik_VALUE(가로,archive_posisyon):
                for button in (1,0):client.sendall(struct.pack('>BBHH',5,button,가로,archive_posisyon))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            magklik_VALUE(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for karakter_VALUE in '한글':누름값(0x1000000|ord(karakter_VALUE));누름값(0x1000000|ord(karakter_VALUE),False)
            for 횟수 in (1,2):
                run=len(대화기록);magklik_VALUE(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),run)
            time.sleep(.3)
            window_iginuhit=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=window_iginuhit.crop((110,272,530,300)).tobytes()
            window_iginuhit.save(str(sukat_data/'java-swing.png'))
            run=len(대화기록);magklik_VALUE(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',run)
        # Download the guest-created bytes through FTP in the same GUI VM.
        file_pagpasok_pangalan={'java':'java.txt','c':'c.txt','python':'python.txt'}[Wika]
        shell('cp '+file_pagpasok_pangalan+' /patunayan.txt')
        RECEIVED_COUNT=bytearray();file_lipat_koneksyon.retrbinary('RETR patunayan.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==예상파일.encode()
        shell('echo preserved > 출력예제.'+('py' if Wika=='python' else Wika))
        assert 'EXAMPLES READY' in shell('example '+Wika)
        assert '\npreserved\n' in shell('cat 출력예제.'+('py' if Wika=='python' else Wika))
        assert '한/영 key_VALUE, Shift+Space 또는 F9' in shell('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in shell('echo GUI NETWORK TOGETHER')
        file_lipat_koneksyon.quit();file_lipat_koneksyon=None;assert 'FTP stopped' in shell('ftpd stop')
        print('PASS '+Wika+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if file_lipat_koneksyon:
            try:file_lipat_koneksyon.close()
            except OSError:pass
        if client:client.close()
        Proseso.terminate()
        try:Proseso.wait(timeout=8)
        except subprocess.TimeoutExpired:Proseso.kill();Proseso.wait()
        tagapili.close();Proseso.stdout.close();(sukat_data/(Wika+'-serial.log')).write_bytes(대화기록)


def run():
    sukat_data=Project_root/'build/verification/examples';sukat_data.mkdir(parents=True,exist_ok=True)
    pagpapatibay_ulat={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_root/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for Wika in ('java','c','python'):
                test_언어(Wika,되돌림서버항목,sukat_data);pagpapatibay_ulat['languages'].append(Wika)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(kategorya_VALUE,data.encode()) for kategorya_VALUE,data in 예상결과],되돌림서버항목.수신됨
            pagpapatibay_ulat['host_network_payloads']=[{'protocol':kategorya_VALUE,'text':data.decode()} for kategorya_VALUE,data in 되돌림서버항목.수신됨]
        pagpapatibay_ulat.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(sukat_data/'report.json').write_text(json.dumps(pagpapatibay_ulat,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':run()
