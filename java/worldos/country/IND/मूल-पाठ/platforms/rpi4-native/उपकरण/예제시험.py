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
from डेस्कटॉप_दृश्य import 정확한값
from 예제되돌림서버 import प्रतिध्वनि_सर्वर
from निष्पादित_करें_आदेश import प्रोजेक्ट_करें_मूल


def test_언어(भाषा,되돌림서버항목,परिणाम_डेटा):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));फ़ाइल_स्थानांतरण_पोर्ट_संख्या=임시자원.getsockname()[1]
    प्रक्रिया=subprocess.Popen(['python3',str(प्रोजेक्ट_करें_मूल/'उपकरण/निष्पादित_करें_आदेश.py'),'--desktop','--network','--port','0','--ftp-port',str(फ़ाइल_स्थानांतरण_पोर्ट_संख्या)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    सिलेक्टर=selectors.DefaultSelector();सिलेक्टर.register(प्रक्रिया.stdout,selectors.EVENT_READ)
    बोला_गया_पाठ=bytearray();क्लायंट=None;फ़ाइल_स्थानांतरण_कनेक्शन=None
    def 수신하기(मार्कर,चलाएँ=0):
        समाप्त_करें_ऑफ़सेट=time.monotonic()+60
        while मार्कर not in बोला_गया_पाठ[चलाएँ:]:
            if time.monotonic()>समाप्त_करें_ऑफ़सेट or प्रक्रिया.poll() is not None:raise AssertionError(बोला_गया_पाठ[चलाएँ:].decode('utf-8','replace'))
            for 누름값,_ in सिलेक्टर.select(.1):
                आँकड़े=누름값.fileobj.read(65536)
                if आँकड़े:बोला_गया_पाठ.extend(आँकड़े)
        return बोला_गया_पाठ[चलाएँ:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(प्रतीक_मान,누르는중=True):क्लायंट.sendall(struct.pack('>BBHI',4,int(누르는중),0,प्रतीक_मान))
    def प्रारंभ_ऑफ़सेट(पंक्ति):
        चलाएँ=len(बोला_गया_पाठ)
        for वर्ण_कोड in पंक्ति+'\n':
            प्रतीक_मान=0xff0d if वर्ण_कोड=='\n' else ord(वर्ण_कोड) if ord(वर्ण_कोड)<256 else 0x1000000|ord(वर्ण_कोड)
            누름값(प्रतीक_मान);누름값(प्रतीक_मान,False)
        return चलाएँ
    def शेल(पंक्ति):return 수신하기(b'jkoros-native> ',प्रारंभ_ऑफ़सेट(पंक्ति))
    def निष्पादित_करें_आदेश(पंक्ति,예상결과):
        पाठ=शेल(पंक्ति);assert 예상결과 in पाठ and 'exit 0' in पाठ,(पंक्ति,पाठ)
        return पाठ
    def 화소들():
        क्लायंट.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            श्रेणी_मान=정확한값(क्लायंट,1)[0]
            if श्रेणी_मान==2:continue
            if श्रेणी_मान==3:
                개수=struct.unpack('>I',정확한값(क्लायंट,7)[3:])[0];정확한값(क्लायंट,개수);continue
            assert श्रेणी_मान==0,श्रेणी_मान
            항목수=struct.unpack('>H',정확한값(क्लायंट,3)[1:])[0]
            for _ in range(항목수):
                x_निर्देशांक,세로좌표,너비값,높이값,वर्ण_सेट=struct.unpack('>HHHHi',정확한값(क्लायंट,12));assert वर्ण_सेट==0,वर्ण_सेट
                आँकड़े=정확한값(क्लायंट,너비값*높이값*4)
                for पंक्ति_पद in range(높이값):
                    for कालम_पद in range(너비값):
                        원본자료=(पंक्ति_पद*너비값+कालम_पद)*4;लक्ष्य=((세로좌표+पंक्ति_पद)*640+x_निर्देशांक+कालम_पद)*3
                        빛삼원색[लक्ष्य:लक्ष्य+3]=bytes((आँकड़े[원본자료+2],आँकड़े[원본자료+1],आँकड़े[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',बोला_गया_पाठ.rfind(b'TERMINAL READY'))
        पोर्ट_संख्या=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',बोला_गया_पाठ).group(1))
        क्लायंट=socket.create_connection(('127.0.0.1',पोर्ट_संख्या),timeout=10)
        assert 정확한값(क्लायंट,12)==b'RFB 003.008\n';क्लायंट.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(क्लायंट,정확한값(क्लायंट,1)[0]);क्लायंट.sendall(b'\x01');assert 정확한값(क्लायंट,4)==b'\0'*4
        क्लायंट.sendall(b'\x01');초기값=정확한값(क्लायंट,24);정확한값(क्लायंट,struct.unpack('>I',초기값[20:])[0])
        क्लायंट.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        क्लायंट.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in शेल('ftpd start')
        फ़ाइल_स्थानांतरण_कनेक्शन=ftplib.FTP();फ़ाइल_स्थानांतरण_कनेक्शन.encoding='utf-8';फ़ाइल_स्थानांतरण_कनेक्शन.connect('127.0.0.1',फ़ाइल_स्थानांतरण_पोर्ट_संख्या,timeout=20);फ़ाइल_स्थानांतरण_कनेक्शन.login()
        पेलोड_डेटा=('GUI와 FTP 동시 사용 '+भाषा+' 😀\n').encode()
        फ़ाइल_स्थानांतरण_कनेक्शन.storbinary('STOR 함께.txt',io.BytesIO(पेलोड_डेटा))
        assert पेलोड_डेटा.decode().strip() in शेल('cat /함께.txt')
        받은수=bytearray();फ़ाइल_स्थानांतरण_कनेक्शन.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==पेलोड_डेटा;फ़ाइल_स्थानांतरण_कनेक्शन.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        भेजें_सूची=शेल('ls /example')
        assert all(नाम in भेजें_सूची for नाम in ('java/','c/','python/','README.md')),भेजें_सूची
        if भाषा=='java':
            बंडल_सूची=json.loads((प्रोजेक्ट_करें_मूल/'build/examples/manifest.json').read_text())
            for पथ,प्रवेश_बिदुं in बंडल_सूची.items():
                शेल('cp '+पथ+' /example-check.bin')
                सामग्री_मान=bytearray();फ़ाइल_स्थानांतरण_कनेक्शन.retrbinary('RETR example-check.bin',सामग्री_मान.extend)
                assert len(सामग्री_मान)==प्रवेश_बिदुं['bytes'] and hashlib.sha256(सामग्री_मान).hexdigest()==प्रवेश_बिदुं['sha256'],पथ
            फ़ाइल_स्थानांतरण_कनेक्शन.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            बाइनरी=bytes(range(256))*64
            फ़ाइल_स्थानांतरण_कनेक्शन.storbinary('STOR boundary.bin',io.BytesIO(बाइनरी))
            सामग्री_मान=bytearray();फ़ाइल_स्थानांतरण_कनेक्शन.retrbinary('RETR boundary.bin',सामग्री_मान.extend)
            assert सामग्री_मान==बाइनरी and 'boundary.bin' in फ़ाइल_स्थानांतरण_कनेक्शन.nlst()
            शेल('cp /boundary.bin /boundary-copy.bin')
            सामग्री_मान=bytearray();फ़ाइल_स्थानांतरण_कनेक्शन.retrbinary('RETR boundary-copy.bin',सामग्री_मान.extend)
            assert सामग्री_मान==बाइनरी
            फ़ाइल_स्थानांतरण_कनेक्शन.delete('boundary.bin');फ़ाइल_स्थानांतरण_कनेक्शन.delete('boundary-copy.bin')
        assert 'लेखनउदाहरण' in शेल('ls /example/'+भाषा)
        शेल('cd /example/'+भाषा)
        नाम_तालिका={'java':'JAVA','c':'C','python':'PYTHON'}[भाषा]
        예상파일=नाम_तालिका+' संचिका: 한글 आँकड़े 😀\n'
        if भाषा=='java':
            निष्पादित_करें_आदेश('javac लेखनउदाहरण.java','Compiled:');निष्पादित_करें_आदेश('java लेखनउदाहरण','JAVA निर्गम: 안녕하세요 😀')
            निष्पादित_करें_आदेश('javac संचिकाउदाहरण.java','Compiled:');निष्पादित_करें_आदेश('java संचिकाउदाहरण',예상파일)
            निष्पादित_करें_आदेश('java जालउदाहरण {} {}'.format(되돌림서버항목.연결접속번호,되돌림서버항목.यूज़र_डेटाग्राम_प्रॉटोकॉल_पोर्ट),'JAVA 네트워크 सत्यापित_करें: TCP UDP 한글')
            ग्राफ़िक्स_आदेश='java चित्रउदाहरण'
        elif भाषा=='c':
            for नाम,전달값,예상결과 in [('निर्गम','', 'C निर्गम: 안녕하세요 😀'),('संचिका','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.यूज़र_डेटाग्राम_प्रॉटोकॉल_पोर्ट),'C 네트워크 सत्यापित_करें: UDP 한글')]:
                निष्पादित_करें_आदेश('cc '+नाम+'예제.c -o निष्पादित_करें_आदेश','Compiled native ARM64 ELF:')
                निष्पादित_करें_आदेश('./निष्पादित_करें_आदेश'+전달값,예상결과)
            निष्पादित_करें_आदेश('cc चित्रउदाहरण.c -o निष्पादित_करें_आदेश','Compiled native ARM64 ELF:');ग्राफ़िक्स_आदेश='./निष्पादित_करें_आदेश'
        else:
            for नाम,전달값,예상결과 in [('निर्गम','','PYTHON निर्गम: 안녕하세요 😀'),('संचिका','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.यूज़र_डेटाग्राम_प्रॉटोकॉल_पोर्ट),'PYTHON 네트워크 सत्यापित_करें: UDP 한글')]:
                निष्पादित_करें_आदेश('python '+नाम+'예제.py'+전달값,예상결과)
            ग्राफ़िक्स_आदेश='python चित्रउदाहरण.py'
        प्रारंभ_ड्रॉइंग=प्रारंभ_ऑफ़सेट(ग्राफ़िक्स_आदेश)
        पाठ=수신하기('그림을 확인한 वापस_मान Enter를 누르세요.\r\n'.encode(),प्रारंभ_ड्रॉइंग)
        assert नाम_तालिका+' 그래픽: 빨강 초록 파랑' in पाठ and 'exit 0' not in पाठ,पाठ
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        फ़ाइल_स्थानांतरण_कनेक्शन.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();फ़ाइल_स्थानांतरण_कनेक्शन.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';फ़ाइल_स्थानांतरण_कनेक्शन.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            ऑफ़सेट_मान=(세로좌표*640+610)*3;assert tuple(빛삼원색[ऑफ़सेट_मान:ऑफ़सेट_मान+3])==색상,(भाषा,세로좌표,tuple(빛삼원색[ऑफ़सेट_मान:ऑफ़सेट_मान+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(परिणाम_डेटा/(भाषा+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',प्रारंभ_ड्रॉइंग)
        if भाषा=='java':
            प्रारंभ_विंडो=प्रारंभ_ऑफ़सेट('java खिड़कीउदाहरण')
            수신하기('GUI 예제 준비: खिड़कीउदाहरण'.encode(),प्रारंभ_विंडो)
            def क्लिक_करना_मान(가로,अनुलंब_पद):
                for बटन in (1,0):क्लायंट.sendall(struct.pack('>BBHH',5,बटन,가로,अनुलंब_पद))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            क्लिक_करना_मान(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for कैरेक्टर_मान in '한글':누름값(0x1000000|ord(कैरेक्टर_मान));누름값(0x1000000|ord(कैरेक्टर_मान),False)
            for 횟수 in (1,2):
                चलाएँ=len(बोला_गया_पाठ);क्लिक_करना_मान(180,242)
                수신하기(('GUI अभिनन्दन_ae353e94: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),चलाएँ)
            time.sleep(.3)
            विंडो_ड्रॉइंग=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=विंडो_ड्रॉइंग.crop((110,272,530,300)).tobytes()
            विंडो_ड्रॉइंग.save(str(परिणाम_डेटा/'java-swing.png'))
            चलाएँ=len(बोला_गया_पाठ);क्लिक_करना_मान(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',चलाएँ)
        # Download the guest-created bytes through FTP in the same GUI VM.
        फ़ाइल_एन्ट्री_नाम={'java':'java.txt','c':'c.txt','python':'python.txt'}[भाषा]
        शेल('cp '+फ़ाइल_एन्ट्री_नाम+' /मान्य_करें.txt')
        받은수=bytearray();फ़ाइल_स्थानांतरण_कनेक्शन.retrbinary('RETR मान्य_करें.txt',받은수.extend);assert 받은수==예상파일.encode()
        शेल('echo preserved > लेखनउदाहरण.'+('py' if भाषा=='python' else भाषा))
        assert 'EXAMPLES READY' in शेल('example '+भाषा)
        assert '\npreserved\n' in शेल('cat लेखनउदाहरण.'+('py' if भाषा=='python' else भाषा))
        assert '한/शून्य_ऑपरेंड कुंजी_मान, Shift+Space 또는 F9' in शेल('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in शेल('echo GUI NETWORK TOGETHER')
        फ़ाइल_स्थानांतरण_कनेक्शन.quit();फ़ाइल_स्थानांतरण_कनेक्शन=None;assert 'FTP stopped' in शेल('ftpd stop')
        print('PASS '+भाषा+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if फ़ाइल_स्थानांतरण_कनेक्शन:
            try:फ़ाइल_स्थानांतरण_कनेक्शन.close()
            except OSError:pass
        if क्लायंट:क्लायंट.close()
        प्रक्रिया.terminate()
        try:प्रक्रिया.wait(timeout=8)
        except subprocess.TimeoutExpired:प्रक्रिया.kill();प्रक्रिया.wait()
        सिलेक्टर.close();प्रक्रिया.stdout.close();(परिणाम_डेटा/(भाषा+'-serial.log')).write_bytes(बोला_गया_पाठ)


def चलाएँ():
    परिणाम_डेटा=प्रोजेक्ट_करें_मूल/'build/verification/examples';परिणाम_डेटा.mkdir(parents=True,exist_ok=True)
    प्रमाणीकरण_रिपोर्ट={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((प्रोजेक्ट_करें_मूल/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with प्रतिध्वनि_सर्वर() as 되돌림서버항목:
            for भाषा in ('java','c','python'):
                test_언어(भाषा,되돌림서버항목,परिणाम_डेटा);प्रमाणीकरण_रिपोर्ट['languages'].append(भाषा)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(श्रेणी_मान,आँकड़े.encode()) for श्रेणी_मान,आँकड़े in 예상결과],되돌림서버항목.수신됨
            प्रमाणीकरण_रिपोर्ट['host_network_payloads']=[{'protocol':श्रेणी_मान,'text':आँकड़े.decode()} for श्रेणी_मान,आँकड़े in 되돌림서버항목.수신됨]
        प्रमाणीकरण_रिपोर्ट.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(परिणाम_डेटा/'report.json').write_text(json.dumps(प्रमाणीकरण_रिपोर्ट,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':चलाएँ()
