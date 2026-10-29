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
from ഡെസ്ക്ടോപ്പ്_കാഴ്ച import 정확한값
from 예제되돌림서버 import 되돌림서버
from നടപ്പാക്കുക_കമാന്_ഡ് import പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം


def test_언어(భాష,되돌림서버항목,അളവ്_ഡാറ്റാ):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));ഫയല്_കൈമാറുക_പോര്_ട്ട്_നമ്പര്=임시자원.getsockname()[1]
    പ്രക്രിയ=subprocess.Popen(['python3',str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'ഉപകരണങ്ങൾ/നടപ്പാക്കുക_കമാന്_ഡ്.py'),'--desktop','--network','--port','0','--ftp-port',str(ഫയല്_കൈമാറുക_പോര്_ട്ട്_നമ്പര്)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    సెలక్టర్=selectors.DefaultSelector();సెలక్టర్.register(പ്രക്രിയ.stdout,selectors.EVENT_READ)
    대화기록=bytearray();ക്ലയന്_റ്=None;ഫയല്_കൈമാറുക_കണക്ഷൻ=None
    def 수신하기(확인표시,നടപ്പിലാക്കുക=0):
        അവസാനിപ്പിക്കുക_ഓഫ്_സെറ്റ്=time.monotonic()+60
        while 확인표시 not in 대화기록[നടപ്പിലാക്കുക:]:
            if time.monotonic()>അവസാനിപ്പിക്കുക_ഓഫ്_സെറ്റ് or പ്രക്രിയ.poll() is not None:raise AssertionError(대화기록[നടപ്പിലാക്കുക:].decode('utf-8','replace'))
            for 누름값,_ in సెలక్టర్.select(.1):
                ഡാറ്റാ=누름값.fileobj.read(65536)
                if ഡാറ്റാ:대화기록.extend(ഡാറ്റാ)
        return 대화기록[നടപ്പിലാക്കുക:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(nbsp_ചിഹ്നം_മൂല്യം,누르는중=True):ക്ലയന്_റ്.sendall(struct.pack('>BBHI',4,int(누르는중),0,nbsp_ചിഹ്നം_മൂല്യം))
    def ആരംഭം_ഓഫ്_സെറ്റ്(ലൈൻ):
        നടപ്പിലാക്കുക=len(대화기록)
        for പ്രതീകകോഡ് in ലൈൻ+'\n':
            nbsp_ചിഹ്നം_മൂല്യം=0xff0d if പ്രതീകകോഡ്=='\n' else ord(പ്രതീകകോഡ്) if ord(പ്രതീകകോഡ്)<256 else 0x1000000|ord(പ്രതീകകോഡ്)
            누름값(nbsp_ചിഹ്നം_മൂല്യം);누름값(nbsp_ചിഹ്നം_മൂല്യം,False)
        return നടപ്പിലാക്കുക
    def ഷെല്(ലൈൻ):return 수신하기(b'jkoros-native> ',ആരംഭം_ഓഫ്_സെറ്റ്(ലൈൻ))
    def നടപ്പാക്കുക_കമാന്_ഡ്(ലൈൻ,예상결과):
        പദാവലി=ഷെല്(ലൈൻ);assert 예상결과 in പദാവലി and 'exit 0' in പദാവലി,(ലൈൻ,പദാവലി)
        return പദാവലി
    def 화소들():
        ക്ലയന്_റ്.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            വകുപ്പ്_മൂല്യം=정확한값(ക്ലയന്_റ്,1)[0]
            if വകുപ്പ്_മൂല്യം==2:continue
            if വകുപ്പ്_മൂല്യം==3:
                개수=struct.unpack('>I',정확한값(ക്ലയന്_റ്,7)[3:])[0];정확한값(ക്ലയന്_റ്,개수);continue
            assert വകുപ്പ്_മൂല്യം==0,വകുപ്പ്_മൂല്യം
            항목수=struct.unpack('>H',정확한값(ക്ലയന്_റ്,3)[1:])[0]
            for _ in range(항목수):
                x_ഏകോപനം,Y_ബട്ടൺ_ഏകോപനം,너비값,높이값,പ്രതീക_ഗണം=struct.unpack('>HHHHi',정확한값(ക്ലയന്_റ്,12));assert പ്രതീക_ഗണം==0,പ്രതീക_ഗണം
                ഡാറ്റാ=정확한값(ക്ലയന്_റ്,너비값*높이값*4)
                for രേഖ_പദവി in range(높이값):
                    for നിര_പദവി in range(너비값):
                        원본자료=(രേഖ_പദവി*너비값+നിര_പദവി)*4;ലക്_ഷ്യം=((Y_ബട്ടൺ_ഏകോപനം+രേഖ_പദവി)*640+x_ഏകോപനം+നിര_പദവി)*3
                        빛삼원색[ലക്_ഷ്യം:ലക്_ഷ്യം+3]=bytes((ഡാറ്റാ[원본자료+2],ഡാറ്റാ[원본자료+1],ഡാറ്റാ[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        പോര്_ട്ട്_നമ്പര്=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        ക്ലയന്_റ്=socket.create_connection(('127.0.0.1',പോര്_ട്ട്_നമ്പര്),timeout=10)
        assert 정확한값(ക്ലയന്_റ്,12)==b'RFB 003.008\n';ക്ലയന്_റ്.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(ക്ലയന്_റ്,정확한값(ക്ലയന്_റ്,1)[0]);ക്ലയന്_റ്.sendall(b'\x01');assert 정확한값(ക്ലയന്_റ്,4)==b'\0'*4
        ക്ലയന്_റ്.sendall(b'\x01');초기값=정확한값(ക്ലയന്_റ്,24);정확한값(ക്ലയന്_റ്,struct.unpack('>I',초기값[20:])[0])
        ക്ലയന്_റ്.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        ക്ലയന്_റ്.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in ഷെല്('ftpd start')
        ഫയല്_കൈമാറുക_കണക്ഷൻ=ftplib.FTP();ഫയല്_കൈമാറുക_കണക്ഷൻ.encoding='utf-8';ഫയല്_കൈമാറുക_കണക്ഷൻ.connect('127.0.0.1',ഫയല്_കൈമാറുക_പോര്_ട്ട്_നമ്പര്,timeout=20);ഫയല്_കൈമാറുക_കണക്ഷൻ.login()
        പേലോഡ്_ഡാറ്റാ=('GUI와 FTP 동시 사용 '+భాష+' 😀\n').encode()
        ഫയല്_കൈമാറുക_കണക്ഷൻ.storbinary('STOR 함께.txt',io.BytesIO(പേലോഡ്_ഡാറ്റാ))
        assert പേലോഡ്_ഡാറ്റാ.decode().strip() in ഷെല്('cat /함께.txt')
        받은수=bytearray();ഫയല്_കൈമാറുക_കണക്ഷൻ.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==പേലോഡ്_ഡാറ്റാ;ഫയല്_കൈമാറുക_കണക്ഷൻ.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        അയയ്ക്കുക_ലിസ്റ്റ്=ഷെല്('ls /example')
        assert all(പേരു് in അയയ്ക്കുക_ലിസ്റ്റ് for പേരു് in ('java/','c/','python/','README.md')),അയയ്ക്കുക_ലിസ്റ്റ്
        if భాష=='java':
            ബണ്ടിൽ_ആവിഷ്കാരം=json.loads((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/examples/manifest.json').read_text())
            for വഴി,എന്_ട്രി_പോയിന്_റ് in ബണ്ടിൽ_ആവിഷ്കാരം.items():
                ഷെല്('cp '+വഴി+' /example-check.bin')
                ഉള്ളടക്കം_മൂല്യം=bytearray();ഫയല്_കൈമാറുക_കണക്ഷൻ.retrbinary('RETR example-check.bin',ഉള്ളടക്കം_മൂല്യം.extend)
                assert len(ഉള്ളടക്കം_മൂല്യം)==എന്_ട്രി_പോയിന്_റ്['bytes'] and hashlib.sha256(ഉള്ളടക്കം_മൂല്യം).hexdigest()==എന്_ട്രി_പോയിന്_റ്['sha256'],വഴി
            ഫയല്_കൈമാറുക_കണക്ഷൻ.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            బైనరీ=bytes(range(256))*64
            ഫയല്_കൈമാറുക_കണക്ഷൻ.storbinary('STOR boundary.bin',io.BytesIO(బైనరీ))
            ഉള്ളടക്കം_മൂല്യം=bytearray();ഫയല്_കൈമാറുക_കണക്ഷൻ.retrbinary('RETR boundary.bin',ഉള്ളടക്കം_മൂല്യം.extend)
            assert ഉള്ളടക്കം_മൂല്യം==బైనరీ and 'boundary.bin' in ഫയല്_കൈമാറുക_കണക്ഷൻ.nlst()
            ഷെല്('cp /boundary.bin /boundary-copy.bin')
            ഉള്ളടക്കം_മൂല്യം=bytearray();ഫയല്_കൈമാറുക_കണക്ഷൻ.retrbinary('RETR boundary-copy.bin',ഉള്ളടക്കം_മൂല്യം.extend)
            assert ഉള്ളടക്കം_മൂല്യം==బైనరీ
            ഫയല്_കൈമാറുക_കണക്ഷൻ.delete('boundary.bin');ഫയല്_കൈമാറുക_കണക്ഷൻ.delete('boundary-copy.bin')
        assert '출력예제' in ഷെല്('ls /example/'+భాష)
        ഷെല്('cd /example/'+భాష)
        നാ_മം_పట్టిక={'java':'JAVA','c':'C','python':'PYTHON'}[భాష]
        예상파일=നാ_മം_పట్టిక+' ഫയല്: 한글 ഡാറ്റാ 😀\n'
        if భాష=='java':
            നടപ്പാക്കുക_കമാന്_ഡ്('javac 출력예제.java','Compiled:');നടപ്പാക്കുക_കമാന്_ഡ്('java 출력예제','JAVA ഫലം: 안녕하세요 😀')
            നടപ്പാക്കുക_കമാന്_ഡ്('javac 파일예제.java','Compiled:');നടപ്പാക്കുക_കമാന്_ഡ്('java 파일예제',예상파일)
            നടപ്പാക്കുക_കമാന്_ഡ്('java 네트워크예제 {} {}'.format(되돌림서버항목.ട്രാന്_സ്_മിഷന്_കണ്_ട്രോള്_പ്രോട്ടോക്കോള്_പോര്_ട്ട്,되돌림서버항목.전문접속번호),'JAVA 네트워크 പരിശോധിക്കുക: TCP UDP 한글')
            ഗ്രാഫിക്_സ്_കമാന്_ഡ്='java 그래픽예제'
        elif భాష=='c':
            for പേരു്,전달값,예상결과 in [('ഫലം','', 'C ഫലം: 안녕하세요 😀'),('ഫയല്','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 പരിശോധിക്കുക: UDP 한글')]:
                നടപ്പാക്കുക_കമാന്_ഡ്('cc '+പേരു്+'예제.c -o നടപ്പാക്കുക_കമാന്_ഡ്','Compiled native ARM64 ELF:')
                നടപ്പാക്കുക_കമാന്_ഡ്('./നടപ്പാക്കുക_കമാന്_ഡ്'+전달값,예상결과)
            നടപ്പാക്കുക_കമാന്_ഡ്('cc 그래픽예제.c -o നടപ്പാക്കുക_കമാന്_ഡ്','Compiled native ARM64 ELF:');ഗ്രാഫിക്_സ്_കമാന്_ഡ്='./നടപ്പാക്കുക_കമാന്_ഡ്'
        else:
            for പേരു്,전달값,예상결과 in [('ഫലം','','PYTHON ഫലം: 안녕하세요 😀'),('ഫയല്','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 പരിശോധിക്കുക: UDP 한글')]:
                നടപ്പാക്കുക_കമാന്_ഡ്('python '+പേരു്+'예제.py'+전달값,예상결과)
            ഗ്രാഫിക്_സ്_കമാന്_ഡ്='python 그래픽예제.py'
        ആരംഭം_ഡ്രോയിംഗ്=ആരംഭം_ഓഫ്_സെറ്റ്(ഗ്രാഫിക്_സ്_കമാന്_ഡ്)
        പദാവലി=수신하기('그림을 확인한 പിന്നിലേക്ക്_മൂല്യം Enter를 누르세요.\r\n'.encode(),ആരംഭം_ഡ്രോയിംഗ്)
        assert നാ_മം_పట్టిక+' 그래픽: 빨강 초록 파랑' in പദാവലി and 'exit 0' not in പദാവലി,പദാവലി
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        ഫയല്_കൈമാറുക_കണക്ഷൻ.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();ഫയല്_കൈമാറുക_കണക്ഷൻ.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';ഫയല്_കൈമാറുക_കണക്ഷൻ.delete('도중.txt')
        빛삼원색=화소들()
        for Y_ബട്ടൺ_ഏകോപനം,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            ഓഫ്_സെറ്റ്_മൂല്യം=(Y_ബട്ടൺ_ഏകോപനം*640+610)*3;assert tuple(빛삼원색[ഓഫ്_സെറ്റ്_മൂല്യം:ഓഫ്_സെറ്റ്_മൂല്യം+3])==색상,(భాష,Y_ബട്ടൺ_ഏകോപനം,tuple(빛삼원색[ഓഫ്_സെറ്റ്_മൂല്യം:ഓഫ്_സെറ്റ്_മൂല്യം+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(അളവ്_ഡാറ്റാ/(భాష+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',ആരംഭം_ഡ്രോയിംഗ്)
        if భాష=='java':
            ആരംഭം_ജാലകം=ആരംഭം_ഓഫ്_സെറ്റ്('java 창예제')
            수신하기('GUI 예제 തയ്യാറാക്കുക: 창예제'.encode(),ആരംഭം_ജാലകം)
            def ക്ലിക്ക്_ചെയ്യുക_മൂല്യം(가로,ലംബം_പദവി):
                for ബട്ടണ് in (1,0):ക്ലയന്_റ്.sendall(struct.pack('>BBHH',5,ബട്ടണ്,가로,ലംബം_പദവി))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            ക്ലിക്ക്_ചെയ്യുക_മൂല്യം(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for പ്രതീകം_മൂല്യം in '한글':누름값(0x1000000|ord(പ്രതീകം_മൂല്യം));누름값(0x1000000|ord(പ്രതീകം_മൂല്യം),False)
            for 횟수 in (1,2):
                നടപ്പിലാക്കുക=len(대화기록);ക്ലിക്ക്_ചെയ്യുക_മൂല്യം(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),നടപ്പിലാക്കുക)
            time.sleep(.3)
            ജാലകം_ഡ്രോയിംഗ്=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=ജാലകം_ഡ്രോയിംഗ്.crop((110,272,530,300)).tobytes()
            ജാലകം_ഡ്രോയിംഗ്.save(str(അളവ്_ഡാറ്റാ/'java-swing.png'))
            നടപ്പിലാക്കുക=len(대화기록);ക്ലിക്ക്_ചെയ്യുക_മൂല്യം(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',നടപ്പിലാക്കുക)
        # Download the guest-created bytes through FTP in the same GUI VM.
        ഫയല്_എന്_ട്രി_നാ_മം={'java':'java.txt','c':'c.txt','python':'python.txt'}[భాష]
        ഷെല്('cp '+ഫയല്_എന്_ട്രി_നാ_മം+' /സാധൂകരിക്കുക.txt')
        받은수=bytearray();ഫയല്_കൈമാറുക_കണക്ഷൻ.retrbinary('RETR സാധൂകരിക്കുക.txt',받은수.extend);assert 받은수==예상파일.encode()
        ഷെല്('echo preserved > 출력예제.'+('py' if భాష=='python' else భాష))
        assert 'EXAMPLES READY' in ഷെല്('example '+భాష)
        assert '\npreserved\n' in ഷെല്('cat 출력예제.'+('py' if భాష=='python' else భాష))
        assert '한/영 കീ_മൂല്യം, Shift+Space 또는 F9' in ഷെല്('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in ഷെല്('echo GUI NETWORK TOGETHER')
        ഫയല്_കൈമാറുക_കണക്ഷൻ.quit();ഫയല്_കൈമാറുക_കണക്ഷൻ=None;assert 'FTP stopped' in ഷെല്('ftpd stop')
        print('PASS '+భాష+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if ഫയല്_കൈമാറുക_കണക്ഷൻ:
            try:ഫയല്_കൈമാറുക_കണക്ഷൻ.close()
            except OSError:pass
        if ക്ലയന്_റ്:ക്ലയന്_റ്.close()
        പ്രക്രിയ.terminate()
        try:പ്രക്രിയ.wait(timeout=8)
        except subprocess.TimeoutExpired:പ്രക്രിയ.kill();പ്രക്രിയ.wait()
        సెలక్టర్.close();പ്രക്രിയ.stdout.close();(അളവ്_ഡാറ്റാ/(భాష+'-serial.log')).write_bytes(대화기록)


def നടപ്പിലാക്കുക():
    അളവ്_ഡാറ്റാ=പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/verification/examples';അളവ്_ഡാറ്റാ.mkdir(parents=True,exist_ok=True)
    నిర్ధారణ_నివేదిక={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for భాష in ('java','c','python'):
                test_언어(భాష,되돌림서버항목,അളവ്_ഡാറ്റാ);నిర్ధారణ_నివేదిక['languages'].append(భాష)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(വകുപ്പ്_മൂല്യം,ഡാറ്റാ.encode()) for വകുപ്പ്_മൂല്യം,ഡാറ്റാ in 예상결과],되돌림서버항목.수신됨
            నిర్ధారణ_నివేదిక['host_network_payloads']=[{'protocol':വകുപ്പ്_മൂല്യം,'text':ഡാറ്റാ.decode()} for വകുപ്പ്_മൂല്യം,ഡാറ്റാ in 되돌림서버항목.수신됨]
        నిర్ధారణ_నివేదిక.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(അളവ്_ഡാറ്റാ/'report.json').write_text(json.dumps(నిర్ధారణ_నివేదిక,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':നടപ്പിലാക്കുക()
