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
from डेस्कटॉप_दृश्य import तंतोतंत_मूल्य
from उदाहरण_प्रतिध्वनी import प्रतिध्वनी_सर्व्हर्स
from आज्ञा_कार्यवाही_करा import प्रोजेक्ट_मूळ


def भाषा_चाचणी(भाषा,प्रतिध्वनी_सर्व्हर_प्रविष्टी,मोजमाप_डेटा):
    with socket.socket() as तात्पुरते:
        तात्पुरते.bind(('127.0.0.1',0));संचिका_स्थानांतर_पोर्ट_नंबर=तात्पुरते.getsockname()[1]
    प्रक्रिया=subprocess.Popen(['python3',str(प्रोजेक्ट_मूळ/'साधने/आज्ञा_कार्यवाही_करा.py'),'--desktop','--network','--port','0','--ftp-port',str(संचिका_स्थानांतर_पोर्ट_नंबर)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    निवडक=selectors.DefaultSelector();निवडक.register(प्रक्रिया.stdout,selectors.EVENT_READ)
    सत्रलेख=bytearray();क्लायंट=None;संचिका_स्थानांतर_कनेक्शन=None
    def संदेश_स्वीकारा(खूण,सुरू_करा=0):
        शेवट_करा_ऑफसेट=time.monotonic()+60
        while खूण not in सत्रलेख[सुरू_करा:]:
            if time.monotonic()>शेवट_करा_ऑफसेट or प्रक्रिया.poll() is not None:raise AssertionError(सत्रलेख[सुरू_करा:].decode('utf-8','replace'))
            for दाबलेले_मूल्य,_ in निवडक.select(.1):
                डेटा=दाबलेले_मूल्य.fileobj.read(65536)
                if डेटा:सत्रलेख.extend(डेटा)
        return सत्रलेख[सुरू_करा:].decode('utf-8','replace').replace('\r\n','\n')
    def दाबलेले_मूल्य(चिन्ह_मूल्य,आहे_दाबणे=True):क्लायंट.sendall(struct.pack('>BBHI',4,int(आहे_दाबणे),0,चिन्ह_मूल्य))
    def प्रारंभ_ऑफसेट(ओळ):
        सुरू_करा=len(सत्रलेख)
        for वर्ण_कोड in ओळ+'\n':
            चिन्ह_मूल्य=0xff0d if वर्ण_कोड=='\n' else ord(वर्ण_कोड) if ord(वर्ण_कोड)<256 else 0x1000000|ord(वर्ण_कोड)
            दाबलेले_मूल्य(चिन्ह_मूल्य);दाबलेले_मूल्य(चिन्ह_मूल्य,False)
        return सुरू_करा
    def शेल(ओळ):return संदेश_स्वीकारा(b'jkoros-native> ',प्रारंभ_ऑफसेट(ओळ))
    def आज्ञा_कार्यवाही_करा(ओळ,अपेक्षित):
        पाठ्य=शेल(ओळ);assert अपेक्षित in पाठ्य and 'exit 0' in पाठ्य,(ओळ,पाठ्य)
        return पाठ्य
    def चित्रबिंदू_यादी():
        क्लायंट.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        रेड_ग्रीन_ब्ल्यू_रंग=bytearray(640*480*3)
        while True:
            वर्गवारी_मूल्य=तंतोतंत_मूल्य(क्लायंट,1)[0]
            if वर्गवारी_मूल्य==2:continue
            if वर्गवारी_मूल्य==3:
                आयटम_संख्या=struct.unpack('>I',तंतोतंत_मूल्य(क्लायंट,7)[3:])[0];तंतोतंत_मूल्य(क्लायंट,आयटम_संख्या);continue
            assert वर्गवारी_मूल्य==0,वर्गवारी_मूल्य
            प्रविष्टी_संख्या=struct.unpack('>H',तंतोतंत_मूल्य(क्लायंट,3)[1:])[0]
            for _ in range(प्रविष्टी_संख्या):
                आडवे_समन्वयीत,उभे_समन्वयीत,मागितलेले_रुंदी_मूल्य,मागितलेले_उंची_मूल्य,वर्ण_संच=struct.unpack('>HHHHi',तंतोतंत_मूल्य(क्लायंट,12));assert वर्ण_संच==0,वर्ण_संच
                डेटा=तंतोतंत_मूल्य(क्लायंट,मागितलेले_रुंदी_मूल्य*मागितलेले_उंची_मूल्य*4)
                for ओळ_स्थान in range(मागितलेले_उंची_मूल्य):
                    for स्तंभ_स्थान in range(मागितलेले_रुंदी_मूल्य):
                        मूळ_डेटा=(ओळ_स्थान*मागितलेले_रुंदी_मूल्य+स्तंभ_स्थान)*4;लक्ष्य=((उभे_समन्वयीत+ओळ_स्थान)*640+आडवे_समन्वयीत+स्तंभ_स्थान)*3
                        रेड_ग्रीन_ब्ल्यू_रंग[लक्ष्य:लक्ष्य+3]=bytes((डेटा[मूळ_डेटा+2],डेटा[मूळ_डेटा+1],डेटा[मूळ_डेटा]))
            if प्रविष्टी_संख्या:return रेड_ग्रीन_ब्ल्यू_रंग
    try:
        संदेश_स्वीकारा(b'TERMINAL READY');संदेश_स्वीकारा(b'jkoros-native> ',सत्रलेख.rfind(b'TERMINAL READY'))
        पोर्ट_नंबर=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',सत्रलेख).group(1))
        क्लायंट=socket.create_connection(('127.0.0.1',पोर्ट_नंबर),timeout=10)
        assert तंतोतंत_मूल्य(क्लायंट,12)==b'RFB 003.008\n';क्लायंट.sendall(b'RFB 003.008\n')
        assert 1 in तंतोतंत_मूल्य(क्लायंट,तंतोतंत_मूल्य(क्लायंट,1)[0]);क्लायंट.sendall(b'\x01');assert तंतोतंत_मूल्य(क्लायंट,4)==b'\0'*4
        क्लायंट.sendall(b'\x01');प्रारंभिक_मूल्य=तंतोतंत_मूल्य(क्लायंट,24);तंतोतंत_मूल्य(क्लायंट,struct.unpack('>I',प्रारंभिक_मूल्य[20:])[0])
        क्लायंट.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        क्लायंट.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in शेल('ftpd start')
        संचिका_स्थानांतर_कनेक्शन=ftplib.FTP();संचिका_स्थानांतर_कनेक्शन.encoding='utf-8';संचिका_स्थानांतर_कनेक्शन.connect('127.0.0.1',संचिका_स्थानांतर_पोर्ट_नंबर,timeout=20);संचिका_स्थानांतर_कनेक्शन.login()
        पेलोड_डेटा=('GUI와 FTP 동시 वापर_मूल्य '+भाषा+' 😀\n').encode()
        संचिका_स्थानांतर_कनेक्शन.storbinary('STOR 함께.txt',io.BytesIO(पेलोड_डेटा))
        assert पेलोड_डेटा.decode().strip() in शेल('cat /함께.txt')
        स्वीकारलेले_संख्या=bytearray();संचिका_स्थानांतर_कनेक्शन.retrbinary('RETR 함께.txt',स्वीकारलेले_संख्या.extend);assert स्वीकारलेले_संख्या==पेलोड_डेटा;संचिका_स्थानांतर_कनेक्शन.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        यादी_पाठवा=शेल('ls /example')
        assert all(नाव in यादी_पाठवा for नाव in ('java/','c/','python/','README.md')),यादी_पाठवा
        if भाषा=='java':
            बंडल_सूचीलेख=json.loads((प्रोजेक्ट_मूळ/'build/examples/manifest.json').read_text())
            for मार्ग,प्रविष्टी_गुण in बंडल_सूचीलेख.items():
                शेल('cp '+मार्ग+' /example-check.bin')
                सामुग्री_मूल्य=bytearray();संचिका_स्थानांतर_कनेक्शन.retrbinary('RETR example-check.bin',सामुग्री_मूल्य.extend)
                assert len(सामुग्री_मूल्य)==प्रविष्टी_गुण['bytes'] and hashlib.sha256(सामुग्री_मूल्य).hexdigest()==प्रविष्टी_गुण['sha256'],मार्ग
            संचिका_स्थानांतर_कनेक्शन.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            बायनरी=bytes(range(256))*64
            संचिका_स्थानांतर_कनेक्शन.storbinary('STOR boundary.bin',io.BytesIO(बायनरी))
            सामुग्री_मूल्य=bytearray();संचिका_स्थानांतर_कनेक्शन.retrbinary('RETR boundary.bin',सामुग्री_मूल्य.extend)
            assert सामुग्री_मूल्य==बायनरी and 'boundary.bin' in संचिका_स्थानांतर_कनेक्शन.nlst()
            शेल('cp /boundary.bin /boundary-copy.bin')
            सामुग्री_मूल्य=bytearray();संचिका_स्थानांतर_कनेक्शन.retrbinary('RETR boundary-copy.bin',सामुग्री_मूल्य.extend)
            assert सामुग्री_मूल्य==बायनरी
            संचिका_स्थानांतर_कनेक्शन.delete('boundary.bin');संचिका_स्थानांतर_कनेक्शन.delete('boundary-copy.bin')
        assert 'प्रदान_उदाहरण' in शेल('ls /example/'+भाषा)
        शेल('cd /example/'+भाषा)
        नाव_सारणी={'java':'JAVA','c':'C','python':'PYTHON'}[भाषा]
        अपेक्षित_संचिका=नाव_सारणी+' फाइल: 한글 डेटा 😀\n'
        if भाषा=='java':
            आज्ञा_कार्यवाही_करा('javac प्रदान_उदाहरण.java','Compiled:');आज्ञा_कार्यवाही_करा('java प्रदान_उदाहरण','JAVA आउटपुट: 안녕하세요 😀')
            आज्ञा_कार्यवाही_करा('javac संचिका_उदाहरण.java','Compiled:');आज्ञा_कार्यवाही_करा('java संचिका_उदाहरण',अपेक्षित_संचिका)
            आज्ञा_कार्यवाही_करा('java जाळेउदाहरण {} {}'.format(प्रतिध्वनी_सर्व्हर_प्रविष्टी.ट्रान्समिशन_कंट्रोल_प्रोटोकॉल_पॉर्ट,प्रतिध्वनी_सर्व्हर_प्रविष्टी.स्वतंत्रसंदेशसंचार_पॉर्ट),'JAVA 네트워크 पडताळा: TCP UDP 한글')
            ग्राफिक्स_आज्ञा='java चित्रउदाहरण'
        elif भाषा=='c':
            for नाव,अग्रेषित_मूल्य,अपेक्षित in [('आउटपुट','', 'C आउटपुट: 안녕하세요 😀'),('फाइल','',अपेक्षित_संचिका),
                    ('네트워크',' '+str(प्रतिध्वनी_सर्व्हर_प्रविष्टी.स्वतंत्रसंदेशसंचार_पॉर्ट),'C 네트워크 पडताळा: UDP 한글')]:
                आज्ञा_कार्यवाही_करा('cc '+नाव+'उदाहरणे.c -o आज्ञा_कार्यवाही_करा','Compiled native ARM64 ELF:')
                आज्ञा_कार्यवाही_करा('./आज्ञा_कार्यवाही_करा'+अग्रेषित_मूल्य,अपेक्षित)
            आज्ञा_कार्यवाही_करा('cc चित्रउदाहरण.c -o आज्ञा_कार्यवाही_करा','Compiled native ARM64 ELF:');ग्राफिक्स_आज्ञा='./आज्ञा_कार्यवाही_करा'
        else:
            for नाव,अग्रेषित_मूल्य,अपेक्षित in [('आउटपुट','','PYTHON आउटपुट: 안녕하세요 😀'),('फाइल','',अपेक्षित_संचिका),
                    ('네트워크',' '+str(प्रतिध्वनी_सर्व्हर_प्रविष्टी.स्वतंत्रसंदेशसंचार_पॉर्ट),'PYTHON 네트워크 पडताळा: UDP 한글')]:
                आज्ञा_कार्यवाही_करा('python '+नाव+'उदाहरणे.py'+अग्रेषित_मूल्य,अपेक्षित)
            ग्राफिक्स_आज्ञा='python चित्रउदाहरण.py'
        प्रारंभ_रेखांकन=प्रारंभ_ऑफसेट(ग्राफिक्स_आज्ञा)
        पाठ्य=संदेश_स्वीकारा('그림을 확인한 मागे_मूल्य Enter를 누르세요.\r\n'.encode(),प्रारंभ_रेखांकन)
        assert नाव_सारणी+' 그래픽: 빨강 초록 파랑' in पाठ्य and 'exit 0' not in पाठ्य,पाठ्य
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        संचिका_स्थानांतर_कनेक्शन.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        स्वीकारलेले_संख्या=bytearray();संचिका_स्थानांतर_कनेक्शन.retrbinary('RETR 도중.txt',स्वीकारलेले_संख्या.extend);assert स्वीकारलेले_संख्या==b'FTP DURING GRAPHICS';संचिका_स्थानांतर_कनेक्शन.delete('도중.txt')
        रेड_ग्रीन_ब्ल्यू_रंग=चित्रबिंदू_यादी()
        for उभे_समन्वयीत,पिक्सेल_रंग in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            ऑफसेट_मूल्य=(उभे_समन्वयीत*640+610)*3;assert tuple(रेड_ग्रीन_ब्ल्यू_रंग[ऑफसेट_मूल्य:ऑफसेट_मूल्य+3])==पिक्सेल_रंग,(भाषा,उभे_समन्वयीत,tuple(रेड_ग्रीन_ब्ल्यू_रंग[ऑफसेट_मूल्य:ऑफसेट_मूल्य+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(रेड_ग्रीन_ब्ल्यू_रंग)).save(str(मोजमाप_डेटा/(भाषा+'-graphics.png')))
        दाबलेले_मूल्य(0xff0d);दाबलेले_मूल्य(0xff0d,False)
        assert 'exit 0' in संदेश_स्वीकारा(b'jkoros-native> ',प्रारंभ_रेखांकन)
        if भाषा=='java':
            प्रारंभ_विंडो=प्रारंभ_ऑफसेट('java खिडकीउदाहरण')
            संदेश_स्वीकारा('GUI उदाहरणे तयार_करणे: खिडकीउदाहरण'.encode(),प्रारंभ_विंडो)
            def क्लिक_करा_मूल्य(आडवे_स्थान,अनुलंब_स्थान):
                for बटण in (1,0):क्लायंट.sendall(struct.pack('>BBHH',5,बटण,आडवे_स्थान,अनुलंब_स्थान))
            time.sleep(.3)
            मागील_चित्र=Image.frombytes('RGB',(640,480),bytes(चित्रबिंदू_यादी()))
            क्लिक_करा_मूल्य(160,196)
            for _ in range(2):दाबलेले_मूल्य(0xff08);दाबलेले_मूल्य(0xff08,False)
            for वर्ण_मूल्य in '한글':दाबलेले_मूल्य(0x1000000|ord(वर्ण_मूल्य));दाबलेले_मूल्य(0x1000000|ord(वर्ण_मूल्य),False)
            for पुनरावृत्ती_संख्या in (1,2):
                सुरू_करा=len(सत्रलेख);क्लिक_करा_मूल्य(180,242)
                संदेश_स्वीकारा(('GUI अभिवादन_ae353e94: 안녕하세요, 한글님! ('+str(पुनरावृत्ती_संख्या)+')').encode(),सुरू_करा)
            time.sleep(.3)
            विंडो_रेखांकन=Image.frombytes('RGB',(640,480),bytes(चित्रबिंदू_यादी()))
            assert मागील_चित्र.crop((110,272,530,300)).tobytes()!=विंडो_रेखांकन.crop((110,272,530,300)).tobytes()
            विंडो_रेखांकन.save(str(मोजमाप_डेटा/'java-swing.png'))
            सुरू_करा=len(सत्रलेख);क्लिक_करा_मूल्य(535,105)
            assert 'exit 0' in संदेश_स्वीकारा(b'jkoros-native> ',सुरू_करा)
        # Download the guest-created bytes through FTP in the same GUI VM.
        संचिका_प्रविष्टी_नाव={'java':'java.txt','c':'c.txt','python':'python.txt'}[भाषा]
        शेल('cp '+संचिका_प्रविष्टी_नाव+' /प्रमाणित.txt')
        स्वीकारलेले_संख्या=bytearray();संचिका_स्थानांतर_कनेक्शन.retrbinary('RETR प्रमाणित.txt',स्वीकारलेले_संख्या.extend);assert स्वीकारलेले_संख्या==अपेक्षित_संचिका.encode()
        शेल('echo preserved > प्रदान_उदाहरण.'+('py' if भाषा=='python' else भाषा))
        assert 'EXAMPLES READY' in शेल('example '+भाषा)
        assert '\npreserved\n' in शेल('cat प्रदान_उदाहरण.'+('py' if भाषा=='python' else भाषा))
        assert '한/शून्य_संकार्य कळ_मूल्य, Shift+Space 또는 F9' in शेल('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in शेल('echo GUI NETWORK TOGETHER')
        संचिका_स्थानांतर_कनेक्शन.quit();संचिका_स्थानांतर_कनेक्शन=None;assert 'FTP stopped' in शेल('ftpd stop')
        print('PASS '+भाषा+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if संचिका_स्थानांतर_कनेक्शन:
            try:संचिका_स्थानांतर_कनेक्शन.close()
            except OSError:pass
        if क्लायंट:क्लायंट.close()
        प्रक्रिया.terminate()
        try:प्रक्रिया.wait(timeout=8)
        except subprocess.TimeoutExpired:प्रक्रिया.kill();प्रक्रिया.wait()
        निवडक.close();प्रक्रिया.stdout.close();(मोजमाप_डेटा/(भाषा+'-serial.log')).write_bytes(सत्रलेख)


def सुरू_करा():
    मोजमाप_डेटा=प्रोजेक्ट_मूळ/'build/verification/examples';मोजमाप_डेटा.mkdir(parents=True,exist_ok=True)
    पडताळणी_अहवाल={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((प्रोजेक्ट_मूळ/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with प्रतिध्वनी_सर्व्हर्स() as प्रतिध्वनी_सर्व्हर_प्रविष्टी:
            for भाषा in ('java','c','python'):
                भाषा_चाचणी(भाषा,प्रतिध्वनी_सर्व्हर_प्रविष्टी,मोजमाप_डेटा);पडताळणी_अहवाल['languages'].append(भाषा)
            अपेक्षित=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert प्रतिध्वनी_सर्व्हर_प्रविष्टी.आहे_स्वीकारलेले==[(वर्गवारी_मूल्य,डेटा.encode()) for वर्गवारी_मूल्य,डेटा in अपेक्षित],प्रतिध्वनी_सर्व्हर_प्रविष्टी.आहे_स्वीकारलेले
            पडताळणी_अहवाल['host_network_payloads']=[{'protocol':वर्गवारी_मूल्य,'text':डेटा.decode()} for वर्गवारी_मूल्य,डेटा in प्रतिध्वनी_सर्व्हर_प्रविष्टी.आहे_स्वीकारलेले]
        पडताळणी_अहवाल.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(मोजमाप_डेटा/'report.json').write_text(json.dumps(पडताळणी_अहवाल,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':सुरू_करा()
