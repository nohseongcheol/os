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
from डेस्कटप_दृश्य import 정확한값
from 예제되돌림서버 import 되돌림서버
from कार्यान्वयन_गर्नुहोस्_आदेश import परियोजना_रूट


def test_언어(भाषा,되돌림서버항목,मापन_लगत):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    प्रक्रिया=subprocess.Popen(['python3',str(परियोजना_रूट/'उपकरणहरू/कार्यान्वयन_गर्नुहोस्_आदेश.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    चयनकर्ता=selectors.DefaultSelector();चयनकर्ता.register(प्रक्रिया.stdout,selectors.EVENT_READ)
    대화기록=bytearray();ग्राहक=None;फाइल_ट्रान्सफर_जडान=None
    def 수신하기(확인표시,चलाउनुहोस्=0):
        समाप्त_गर्नुहोस्_अफसेट=time.monotonic()+60
        while 확인표시 not in 대화기록[चलाउनुहोस्:]:
            if time.monotonic()>समाप्त_गर्नुहोस्_अफसेट or प्रक्रिया.poll() is not None:raise AssertionError(대화기록[चलाउनुहोस्:].decode('utf-8','replace'))
            for 누름값,_ in चयनकर्ता.select(.1):
                लगत=누름값.fileobj.read(65536)
                if लगत:대화기록.extend(लगत)
        return 대화기록[चलाउनुहोस्:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(चिन्ह_मान,누르는중=True):ग्राहक.sendall(struct.pack('>BBHI',4,int(누르는중),0,चिन्ह_मान))
    def सुरु_अफसेट(रेखा):
        चलाउनुहोस्=len(대화기록)
        for वर्ण_सङ्केत in रेखा+'\n':
            चिन्ह_मान=0xff0d if वर्ण_सङ्केत=='\n' else ord(वर्ण_सङ्केत) if ord(वर्ण_सङ्केत)<256 else 0x1000000|ord(वर्ण_सङ्केत)
            누름값(चिन्ह_मान);누름값(चिन्ह_मान,False)
        return चलाउनुहोस्
    def शेल(रेखा):return 수신하기(b'jkoros-native> ',सुरु_अफसेट(रेखा))
    def कार्यान्वयन_गर्नुहोस्_आदेश(रेखा,예상결과):
        पाठ=शेल(रेखा);assert 예상결과 in पाठ and 'exit 0' in पाठ,(रेखा,पाठ)
        return पाठ
    def 화소들():
        ग्राहक.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            कोटि_मान=정확한값(ग्राहक,1)[0]
            if कोटि_मान==2:continue
            if कोटि_मान==3:
                개수=struct.unpack('>I',정확한값(ग्राहक,7)[3:])[0];정확한값(ग्राहक,개수);continue
            assert कोटि_मान==0,कोटि_मान
            항목수=struct.unpack('>H',정확한값(ग्राहक,3)[1:])[0]
            for _ in range(항목수):
                x_समन्वय,세로좌표,너비값,높이값,वर्णसेट=struct.unpack('>HHHHi',정확한값(ग्राहक,12));assert वर्णसेट==0,वर्णसेट
                लगत=정확한값(ग्राहक,너비값*높이값*4)
                for रेकर्ड_राख्नुहोस् in range(높이값):
                    for स्तम्भ_राख्नुहोस् in range(너비값):
                        원본자료=(रेकर्ड_राख्नुहोस्*너비값+स्तम्भ_राख्नुहोस्)*4;लक्ष्य=((세로좌표+रेकर्ड_राख्नुहोस्)*640+x_समन्वय+स्तम्भ_राख्नुहोस्)*3
                        빛삼원색[लक्ष्य:लक्ष्य+3]=bytes((लगत[원본자료+2],लगत[원본자료+1],लगत[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        ग्राहक=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert 정확한값(ग्राहक,12)==b'RFB 003.008\n';ग्राहक.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(ग्राहक,정확한값(ग्राहक,1)[0]);ग्राहक.sendall(b'\x01');assert 정확한값(ग्राहक,4)==b'\0'*4
        ग्राहक.sendall(b'\x01');초기값=정확한값(ग्राहक,24);정확한값(ग्राहक,struct.unpack('>I',초기값[20:])[0])
        ग्राहक.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        ग्राहक.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in शेल('ftpd start')
        फाइल_ट्रान्सफर_जडान=ftplib.FTP();फाइल_ट्रान्सफर_जडान.encoding='utf-8';फाइल_ट्रान्सफर_जडान.connect('127.0.0.1',파일전송접속번호,timeout=20);फाइल_ट्रान्सफर_जडान.login()
        पेलोड_लगत=('GUI와 FTP 동시 사용 '+भाषा+' 😀\n').encode()
        फाइल_ट्रान्सफर_जडान.storbinary('STOR 함께.txt',io.BytesIO(पेलोड_लगत))
        assert पेलोड_लगत.decode().strip() in शेल('cat /함께.txt')
        받은수=bytearray();फाइल_ट्रान्सफर_जडान.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==पेलोड_लगत;फाइल_ट्रान्सफर_जडान.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        पठाउनुहोस्_सूची=शेल('ls /example')
        assert all(नाम in पठाउनुहोस्_सूची for नाम in ('java/','c/','python/','README.md')),पठाउनुहोस्_सूची
        if भाषा=='java':
            꾸러미명세=json.loads((परियोजना_रूट/'build/examples/manifest.json').read_text())
            for मार्ग,प्रविष्टि_अंक in 꾸러미명세.items():
                शेल('cp '+मार्ग+' /example-check.bin')
                सामग्री_मान=bytearray();फाइल_ट्रान्सफर_जडान.retrbinary('RETR example-check.bin',सामग्री_मान.extend)
                assert len(सामग्री_मान)==प्रविष्टि_अंक['bytes'] and hashlib.sha256(सामग्री_मान).hexdigest()==प्रविष्टि_अंक['sha256'],मार्ग
            फाइल_ट्रान्सफर_जडान.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            बाइनेरी=bytes(range(256))*64
            फाइल_ट्रान्सफर_जडान.storbinary('STOR boundary.bin',io.BytesIO(बाइनेरी))
            सामग्री_मान=bytearray();फाइल_ट्रान्सफर_जडान.retrbinary('RETR boundary.bin',सामग्री_मान.extend)
            assert सामग्री_मान==बाइनेरी and 'boundary.bin' in फाइल_ट्रान्सफर_जडान.nlst()
            शेल('cp /boundary.bin /boundary-copy.bin')
            सामग्री_मान=bytearray();फाइल_ट्रान्सफर_जडान.retrbinary('RETR boundary-copy.bin',सामग्री_मान.extend)
            assert सामग्री_मान==बाइनेरी
            फाइल_ट्रान्सफर_जडान.delete('boundary.bin');फाइल_ट्रान्सफर_जडान.delete('boundary-copy.bin')
        assert 'लेखनउदाहरण' in शेल('ls /example/'+भाषा)
        शेल('cd /example/'+भाषा)
        नाम_तालिका={'java':'JAVA','c':'C','python':'PYTHON'}[भाषा]
        예상파일=नाम_तालिका+' फाइल: 한글 लगत 😀\n'
        if भाषा=='java':
            कार्यान्वयन_गर्नुहोस्_आदेश('javac लेखनउदाहरण.java','Compiled:');कार्यान्वयन_गर्नुहोस्_आदेश('java लेखनउदाहरण','JAVA 출력: 안녕하세요 😀')
            कार्यान्वयन_गर्नुहोस्_आदेश('javac फाइलउदाहरण.java','Compiled:');कार्यान्वयन_गर्नुहोस्_आदेश('java फाइलउदाहरण',예상파일)
            कार्यान्वयन_गर्नुहोस्_आदेश('java सञ्जालउदाहरण {} {}'.format(되돌림서버항목.टिसिपी_पोर्ट,되돌림서버항목.युडिपी_पोर्ट),'JAVA 네트워크 रुजू_गर्नुहोस्: TCP UDP 한글')
            ग्राफिक्स_आदेश='java चित्रउदाहरण'
        elif भाषा=='c':
            for नाम,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('फाइल','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.युडिपी_पोर्ट),'C 네트워크 रुजू_गर्नुहोस्: UDP 한글')]:
                कार्यान्वयन_गर्नुहोस्_आदेश('cc '+नाम+'예제.c -o कार्यान्वयन_गर्नुहोस्_आदेश','Compiled native ARM64 ELF:')
                कार्यान्वयन_गर्नुहोस्_आदेश('./कार्यान्वयन_गर्नुहोस्_आदेश'+전달값,예상결과)
            कार्यान्वयन_गर्नुहोस्_आदेश('cc चित्रउदाहरण.c -o कार्यान्वयन_गर्नुहोस्_आदेश','Compiled native ARM64 ELF:');ग्राफिक्स_आदेश='./कार्यान्वयन_गर्नुहोस्_आदेश'
        else:
            for नाम,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('फाइल','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.युडिपी_पोर्ट),'PYTHON 네트워크 रुजू_गर्नुहोस्: UDP 한글')]:
                कार्यान्वयन_गर्नुहोस्_आदेश('python '+नाम+'예제.py'+전달값,예상결과)
            ग्राफिक्स_आदेश='python चित्रउदाहरण.py'
        सुरु_चित्रकारी=सुरु_अफसेट(ग्राफिक्स_आदेश)
        पाठ=수신하기('그림을 확인한 पछाडि_मान Enter를 누르세요.\r\n'.encode(),सुरु_चित्रकारी)
        assert नाम_तालिका+' 그래픽: 빨강 초록 파랑' in पाठ and 'exit 0' not in पाठ,पाठ
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        फाइल_ट्रान्सफर_जडान.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();फाइल_ट्रान्सफर_जडान.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';फाइल_ट्रान्सफर_जडान.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            अफसेट_मान=(세로좌표*640+610)*3;assert tuple(빛삼원색[अफसेट_मान:अफसेट_मान+3])==색상,(भाषा,세로좌표,tuple(빛삼원색[अफसेट_मान:अफसेट_मान+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(मापन_लगत/(भाषा+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',सुरु_चित्रकारी)
        if भाषा=='java':
            सुरु_सन्झ्याल=सुरु_अफसेट('java झ्यालउदाहरण')
            수신하기('GUI 예제 तयार_गर्नुहोस्: झ्यालउदाहरण'.encode(),सुरु_सन्झ्याल)
            def क्लिक_गर्नुहोस्_मान(가로,ठाडो_राख्नुहोस्):
                for बटन in (1,0):ग्राहक.sendall(struct.pack('>BBHH',5,बटन,가로,ठाडो_राख्नुहोस्))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            क्लिक_गर्नुहोस्_मान(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for वर्ण_मान in '한글':누름값(0x1000000|ord(वर्ण_मान));누름값(0x1000000|ord(वर्ण_मान),False)
            for 횟수 in (1,2):
                चलाउनुहोस्=len(대화기록);क्लिक_गर्नुहोस्_मान(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),चलाउनुहोस्)
            time.sleep(.3)
            सन्झ्याल_चित्रकारी=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=सन्झ्याल_चित्रकारी.crop((110,272,530,300)).tobytes()
            सन्झ्याल_चित्रकारी.save(str(मापन_लगत/'java-swing.png'))
            चलाउनुहोस्=len(대화기록);क्लिक_गर्नुहोस्_मान(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',चलाउनुहोस्)
        # Download the guest-created bytes through FTP in the same GUI VM.
        फाइल_प्रविष्टि_नाम={'java':'java.txt','c':'c.txt','python':'python.txt'}[भाषा]
        शेल('cp '+फाइल_प्रविष्टि_नाम+' /वैध_गर्नुहोस्.txt')
        받은수=bytearray();फाइल_ट्रान्सफर_जडान.retrbinary('RETR वैध_गर्नुहोस्.txt',받은수.extend);assert 받은수==예상파일.encode()
        शेल('echo preserved > लेखनउदाहरण.'+('py' if भाषा=='python' else भाषा))
        assert 'EXAMPLES READY' in शेल('example '+भाषा)
        assert '\npreserved\n' in शेल('cat लेखनउदाहरण.'+('py' if भाषा=='python' else भाषा))
        assert '한/영 कुञ्जी_मान, Shift+Space 또는 F9' in शेल('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in शेल('echo GUI NETWORK TOGETHER')
        फाइल_ट्रान्सफर_जडान.quit();फाइल_ट्रान्सफर_जडान=None;assert 'FTP stopped' in शेल('ftpd stop')
        print('PASS '+भाषा+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if फाइल_ट्रान्सफर_जडान:
            try:फाइल_ट्रान्सफर_जडान.close()
            except OSError:pass
        if ग्राहक:ग्राहक.close()
        प्रक्रिया.terminate()
        try:प्रक्रिया.wait(timeout=8)
        except subprocess.TimeoutExpired:प्रक्रिया.kill();प्रक्रिया.wait()
        चयनकर्ता.close();प्रक्रिया.stdout.close();(मापन_लगत/(भाषा+'-serial.log')).write_bytes(대화기록)


def चलाउनुहोस्():
    मापन_लगत=परियोजना_रूट/'build/verification/examples';मापन_लगत.mkdir(parents=True,exist_ok=True)
    वैधानिकता_रिपोर्ट={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((परियोजना_रूट/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for भाषा in ('java','c','python'):
                test_언어(भाषा,되돌림서버항목,मापन_लगत);वैधानिकता_रिपोर्ट['languages'].append(भाषा)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(कोटि_मान,लगत.encode()) for कोटि_मान,लगत in 예상결과],되돌림서버항목.수신됨
            वैधानिकता_रिपोर्ट['host_network_payloads']=[{'protocol':कोटि_मान,'text':लगत.decode()} for कोटि_मान,लगत in 되돌림서버항목.수신됨]
        वैधानिकता_रिपोर्ट.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(मापन_लगत/'report.json').write_text(json.dumps(वैधानिकता_रिपोर्ट,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':चलाउनुहोस्()
