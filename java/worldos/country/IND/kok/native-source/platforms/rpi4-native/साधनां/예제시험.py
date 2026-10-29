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
from डॅस्कटॉप_दृश्य import EXACT_मोल
from 예제되돌림서버 import 되돌림서버
from पाळो_दिवचो_आदेश import प्रॉजॅक्ट_रूट


def test_언어(भास,되돌림서버항목,मेजप_डेटा):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    प्रक्रिया=subprocess.Popen(['python3',str(प्रॉजॅक्ट_रूट/'साधनां/पाळो_दिवचो_आदेश.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    वेंचक=selectors.DefaultSelector();वेंचक.register(प्रक्रिया.stdout,selectors.EVENT_READ)
    대화기록=bytearray();क्लायंट=None;फायल_ट्रान्सफर_कनॅक्शन=None
    def 수신하기(확인표시,चलोवप=0):
        सोपोवचें_ऑफसॅट=time.monotonic()+60
        while 확인표시 not in 대화기록[चलोवप:]:
            if time.monotonic()>सोपोवचें_ऑफसॅट or प्रक्रिया.poll() is not None:raise AssertionError(대화기록[चलोवप:].decode('utf-8','replace'))
            for 누름값,_ in वेंचक.select(.1):
                डेटा=누름값.fileobj.read(65536)
                if डेटा:대화기록.extend(डेटा)
        return 대화기록[चलोवप:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(चिन्न_मोल,누르는중=True):क्लायंट.sendall(struct.pack('>BBHI',4,int(누르는중),0,चिन्न_मोल))
    def Start_ऑफसॅट(रेग):
        चलोवप=len(대화기록)
        for वर्ण_कोड in रेग+'\n':
            चिन्न_मोल=0xff0d if वर्ण_कोड=='\n' else ord(वर्ण_कोड) if ord(वर्ण_कोड)<256 else 0x1000000|ord(वर्ण_कोड)
            누름값(चिन्न_मोल);누름값(चिन्न_मोल,False)
        return चलोवप
    def शॅल(रेग):return 수신하기(b'jkoros-native> ',Start_ऑफसॅट(रेग))
    def पाळो_दिवचो_आदेश(रेग,예상결과):
        SMS=शॅल(रेग);assert 예상결과 in SMS and 'exit 0' in SMS,(रेग,SMS)
        return SMS
    def 화소들():
        क्लायंट.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            वर्ग_मोल=EXACT_मोल(क्लायंट,1)[0]
            if वर्ग_मोल==2:continue
            if वर्ग_मोल==3:
                आयटम_COUNT=struct.unpack('>I',EXACT_मोल(क्लायंट,7)[3:])[0];EXACT_मोल(क्लायंट,आयटम_COUNT);continue
            assert वर्ग_मोल==0,वर्ग_मोल
            प्रवेश_COUNT=struct.unpack('>H',EXACT_मोल(क्लायंट,3)[1:])[0]
            for _ in range(प्रवेश_COUNT):
                x_coordinate,세로좌표,너비값,높이값,वर्ण_संच=struct.unpack('>HHHHi',EXACT_मोल(क्लायंट,12));assert वर्ण_संच==0,वर्ण_संच
                डेटा=EXACT_मोल(क्लायंट,너비값*높이값*4)
                for ROW_स्थिती in range(높이값):
                    for स्तंभ_स्थिती in range(너비값):
                        원본자료=(ROW_स्थिती*너비값+स्तंभ_स्थिती)*4;लक्ष्य=((세로좌표+ROW_स्थिती)*640+x_coordinate+स्तंभ_स्थिती)*3
                        빛삼원색[लक्ष्य:लक्ष्य+3]=bytes((डेटा[원본자료+2],डेटा[원본자료+1],डेटा[원본자료]))
            if प्रवेश_COUNT:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        क्लायंट=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert EXACT_मोल(क्लायंट,12)==b'RFB 003.008\n';क्लायंट.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_मोल(क्लायंट,EXACT_मोल(क्लायंट,1)[0]);क्लायंट.sendall(b'\x01');assert EXACT_मोल(क्लायंट,4)==b'\0'*4
        क्लायंट.sendall(b'\x01');초기값=EXACT_मोल(क्लायंट,24);EXACT_मोल(क्लायंट,struct.unpack('>I',초기값[20:])[0])
        क्लायंट.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        क्लायंट.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in शॅल('ftpd start')
        फायल_ट्रान्सफर_कनॅक्शन=ftplib.FTP();फायल_ट्रान्सफर_कनॅक्शन.encoding='utf-8';फायल_ट्रान्सफर_कनॅक्शन.connect('127.0.0.1',파일전송접속번호,timeout=20);फायल_ट्रान्सफर_कनॅक्शन.login()
        पेलोड_डेटा=('GUI와 FTP 동시 사용 '+भास+' 😀\n').encode()
        फायल_ट्रान्सफर_कनॅक्शन.storbinary('STOR 함께.txt',io.BytesIO(पेलोड_डेटा))
        assert पेलोड_डेटा.decode().strip() in शॅल('cat /함께.txt')
        RECEIVED_COUNT=bytearray();फायल_ट्रान्सफर_कनॅक्शन.retrbinary('RETR 함께.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==पेलोड_डेटा;फायल_ट्रान्सफर_कनॅक्शन.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        धाडचें_सुची=शॅल('ls /example')
        assert all(नांव in धाडचें_सुची for नांव in ('java/','c/','python/','README.md')),धाडचें_सुची
        if भास=='java':
            꾸러미명세=json.loads((प्रॉजॅक्ट_रूट/'build/examples/manifest.json').read_text())
            for पाथ,प्रवेश_पॉयंट in 꾸러미명세.items():
                शॅल('cp '+पाथ+' /example-check.bin')
                अनुक्रमणिका_मोल=bytearray();फायल_ट्रान्सफर_कनॅक्शन.retrbinary('RETR example-check.bin',अनुक्रमणिका_मोल.extend)
                assert len(अनुक्रमणिका_मोल)==प्रवेश_पॉयंट['bytes'] and hashlib.sha256(अनुक्रमणिका_मोल).hexdigest()==प्रवेश_पॉयंट['sha256'],पाथ
            फायल_ट्रान्सफर_कनॅक्शन.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            बायनरी=bytes(range(256))*64
            फायल_ट्रान्सफर_कनॅक्शन.storbinary('STOR boundary.bin',io.BytesIO(बायनरी))
            अनुक्रमणिका_मोल=bytearray();फायल_ट्रान्सफर_कनॅक्शन.retrbinary('RETR boundary.bin',अनुक्रमणिका_मोल.extend)
            assert अनुक्रमणिका_मोल==बायनरी and 'boundary.bin' in फायल_ट्रान्सफर_कनॅक्शन.nlst()
            शॅल('cp /boundary.bin /boundary-copy.bin')
            अनुक्रमणिका_मोल=bytearray();फायल_ट्रान्सफर_कनॅक्शन.retrbinary('RETR boundary-copy.bin',अनुक्रमणिका_मोल.extend)
            assert अनुक्रमणिका_मोल==बायनरी
            फायल_ट्रान्सफर_कनॅक्शन.delete('boundary.bin');फायल_ट्रान्सफर_कनॅक्शन.delete('boundary-copy.bin')
        assert '출력예제' in शॅल('ls /example/'+भास)
        शॅल('cd /example/'+भास)
        नांव_तकटो={'java':'JAVA','c':'C','python':'PYTHON'}[भास]
        예상파일=नांव_तकटो+' फायल: 한글 डेटा 😀\n'
        if भास=='java':
            पाळो_दिवचो_आदेश('javac 출력예제.java','Compiled:');पाळो_दिवचो_आदेश('java 출력예제','JAVA 출력: 안녕하세요 😀')
            पाळो_दिवचो_आदेश('javac 파일예제.java','Compiled:');पाळो_दिवचो_आदेश('java 파일예제',예상파일)
            पाळो_दिवचो_आदेश('java 네트워크예제 {} {}'.format(되돌림서버항목.TCP_पोर्ट,되돌림서버항목.UDP_पोर्ट),'JAVA 네트워크 पुनर्तपासणी_करची: TCP UDP 한글')
            ग्राफिक्स_आदेश='java 그래픽예제'
        elif भास=='c':
            for नांव,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('फायल','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.UDP_पोर्ट),'C 네트워크 पुनर्तपासणी_करची: UDP 한글')]:
                पाळो_दिवचो_आदेश('cc '+नांव+'예제.c -o पाळो_दिवचो_आदेश','Compiled native ARM64 ELF:')
                पाळो_दिवचो_आदेश('./पाळो_दिवचो_आदेश'+전달값,예상결과)
            पाळो_दिवचो_आदेश('cc 그래픽예제.c -o पाळो_दिवचो_आदेश','Compiled native ARM64 ELF:');ग्राफिक्स_आदेश='./पाळो_दिवचो_आदेश'
        else:
            for नांव,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('फायल','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.UDP_पोर्ट),'PYTHON 네트워크 पुनर्तपासणी_करची: UDP 한글')]:
                पाळो_दिवचो_आदेश('python '+नांव+'예제.py'+전달값,예상결과)
            ग्राफिक्स_आदेश='python 그래픽예제.py'
        Start_रेखाटन=Start_ऑफसॅट(ग्राफिक्स_आदेश)
        SMS=수신하기('그림을 확인한 फाटीं_मोल Enter를 누르세요.\r\n'.encode(),Start_रेखाटन)
        assert नांव_तकटो+' 그래픽: 빨강 초록 파랑' in SMS and 'exit 0' not in SMS,SMS
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        फायल_ट्रान्सफर_कनॅक्शन.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        RECEIVED_COUNT=bytearray();फायल_ट्रान्सफर_कनॅक्शन.retrbinary('RETR 도중.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==b'FTP DURING GRAPHICS';फायल_ट्रान्सफर_कनॅक्शन.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            ऑफसॅट_मोल=(세로좌표*640+610)*3;assert tuple(빛삼원색[ऑफसॅट_मोल:ऑफसॅट_मोल+3])==색상,(भास,세로좌표,tuple(빛삼원색[ऑफसॅट_मोल:ऑफसॅट_मोल+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(मेजप_डेटा/(भास+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',Start_रेखाटन)
        if भास=='java':
            Start_विंडो=Start_ऑफसॅट('java 창예제')
            수신하기('GUI 예제 तयार_करचें_9ce364fc: 창예제'.encode(),Start_विंडो)
            def क्लिक_करचें_मोल(가로,उबें_स्थिती):
                for बटन in (1,0):क्लायंट.sendall(struct.pack('>BBHH',5,बटन,가로,उबें_स्थिती))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            क्लिक_करचें_मोल(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for वर्ण_मोल in '한글':누름값(0x1000000|ord(वर्ण_मोल));누름값(0x1000000|ord(वर्ण_मोल),False)
            for 횟수 in (1,2):
                चलोवप=len(대화기록);क्लिक_करचें_मोल(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),चलोवप)
            time.sleep(.3)
            विंडो_रेखाटन=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=विंडो_रेखाटन.crop((110,272,530,300)).tobytes()
            विंडो_रेखाटन.save(str(मेजप_डेटा/'java-swing.png'))
            चलोवप=len(대화기록);क्लिक_करचें_मोल(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',चलोवप)
        # Download the guest-created bytes through FTP in the same GUI VM.
        फायल_प्रवेश_नांव={'java':'java.txt','c':'c.txt','python':'python.txt'}[भास]
        शॅल('cp '+फायल_प्रवेश_नांव+' /पुनर्तपासणी_करची_5fb2b747.txt')
        RECEIVED_COUNT=bytearray();फायल_ट्रान्सफर_कनॅक्शन.retrbinary('RETR पुनर्तपासणी_करची_5fb2b747.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==예상파일.encode()
        शॅल('echo preserved > 출력예제.'+('py' if भास=='python' else भास))
        assert 'EXAMPLES READY' in शॅल('example '+भास)
        assert '\npreserved\n' in शॅल('cat 출력예제.'+('py' if भास=='python' else भास))
        assert '한/영 की_मोल, Shift+Space 또는 F9' in शॅल('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in शॅल('echo GUI NETWORK TOGETHER')
        फायल_ट्रान्सफर_कनॅक्शन.quit();फायल_ट्रान्सफर_कनॅक्शन=None;assert 'FTP stopped' in शॅल('ftpd stop')
        print('PASS '+भास+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if फायल_ट्रान्सफर_कनॅक्शन:
            try:फायल_ट्रान्सफर_कनॅक्शन.close()
            except OSError:pass
        if क्लायंट:क्लायंट.close()
        प्रक्रिया.terminate()
        try:प्रक्रिया.wait(timeout=8)
        except subprocess.TimeoutExpired:प्रक्रिया.kill();प्रक्रिया.wait()
        वेंचक.close();प्रक्रिया.stdout.close();(मेजप_डेटा/(भास+'-serial.log')).write_bytes(대화기록)


def चलोवप():
    मेजप_डेटा=प्रॉजॅक्ट_रूट/'build/verification/examples';मेजप_डेटा.mkdir(parents=True,exist_ok=True)
    वैधताय_अहवाल={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((प्रॉजॅक्ट_रूट/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for भास in ('java','c','python'):
                test_언어(भास,되돌림서버항목,मेजप_डेटा);वैधताय_अहवाल['languages'].append(भास)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(वर्ग_मोल,डेटा.encode()) for वर्ग_मोल,डेटा in 예상결과],되돌림서버항목.수신됨
            वैधताय_अहवाल['host_network_payloads']=[{'protocol':वर्ग_मोल,'text':डेटा.decode()} for वर्ग_मोल,डेटा in 되돌림서버항목.수신됨]
        वैधताय_अहवाल.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(मेजप_डेटा/'report.json').write_text(json.dumps(वैधताय_अहवाल,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':चलोवप()
