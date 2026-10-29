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
from ಡೆಸ್ಕ್_ಟಾಪ್_ವೀಕ್ಷಣೆ import 정확한값
from 예제되돌림서버 import 되돌림서버
from ಪೂರೈಸು_ಆದೇಶ import ಬಿಂಬಿಸು_ಮೂಲ


def test_언어(ಭಾಷೆ,되돌림서버항목,ಮಾಪನ_ಡೇಟಾ):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));ಫೈಲ್_ವರ್ಗಾವಣೆ_ಪೋರ್ಟ್_ಸಂಖ್ಯೆ=임시자원.getsockname()[1]
    ಪ್ರಕ್ರಿಯೆ=subprocess.Popen(['python3',str(ಬಿಂಬಿಸು_ಮೂಲ/'ಪರಿಕರಗಳು/ಪೂರೈಸು_ಆದೇಶ.py'),'--desktop','--network','--port','0','--ftp-port',str(ಫೈಲ್_ವರ್ಗಾವಣೆ_ಪೋರ್ಟ್_ಸಂಖ್ಯೆ)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    ಸೆಲೆಕ್ಟರ್=selectors.DefaultSelector();ಸೆಲೆಕ್ಟರ್.register(ಪ್ರಕ್ರಿಯೆ.stdout,selectors.EVENT_READ)
    대화기록=bytearray();ಕ್ಲೈಂಟ್=None;ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ=None
    def 수신하기(확인표시,ಚಲಾಯಿಸು_2=0):
        ಅಂತ್ಯಗೊಳಿಸು_ಆಫ್_ಸೆಟ್=time.monotonic()+60
        while 확인표시 not in 대화기록[ಚಲಾಯಿಸು_2:]:
            if time.monotonic()>ಅಂತ್ಯಗೊಳಿಸು_ಆಫ್_ಸೆಟ್ or ಪ್ರಕ್ರಿಯೆ.poll() is not None:raise AssertionError(대화기록[ಚಲಾಯಿಸು_2:].decode('utf-8','replace'))
            for 누름값,_ in ಸೆಲೆಕ್ಟರ್.select(.1):
                ಡೇಟಾ=누름값.fileobj.read(65536)
                if ಡೇಟಾ:대화기록.extend(ಡೇಟಾ)
        return 대화기록[ಚಲಾಯಿಸು_2:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(ಚಿಹ್ನೆ_ಮೌಲ್ಯ,누르는중=True):ಕ್ಲೈಂಟ್.sendall(struct.pack('>BBHI',4,int(누르는중),0,ಚಿಹ್ನೆ_ಮೌಲ್ಯ))
    def ಆರಂಭಿಸು_ಆಫ್_ಸೆಟ್(ಸಾಲು):
        ಚಲಾಯಿಸು_2=len(대화기록)
        for ಅಕ್ಷರ_ಕೋಡ್ in ಸಾಲು+'\n':
            ಚಿಹ್ನೆ_ಮೌಲ್ಯ=0xff0d if ಅಕ್ಷರ_ಕೋಡ್=='\n' else ord(ಅಕ್ಷರ_ಕೋಡ್) if ord(ಅಕ್ಷರ_ಕೋಡ್)<256 else 0x1000000|ord(ಅಕ್ಷರ_ಕೋಡ್)
            누름값(ಚಿಹ್ನೆ_ಮೌಲ್ಯ);누름값(ಚಿಹ್ನೆ_ಮೌಲ್ಯ,False)
        return ಚಲಾಯಿಸು_2
    def ಶೆಲ್(ಸಾಲು):return 수신하기(b'jkoros-native> ',ಆರಂಭಿಸು_ಆಫ್_ಸೆಟ್(ಸಾಲು))
    def ಪೂರೈಸು_ಆದೇಶ(ಸಾಲು,예상결과):
        ಪಠ್ಯ=ಶೆಲ್(ಸಾಲು);assert 예상결과 in ಪಠ್ಯ and 'exit 0' in ಪಠ್ಯ,(ಸಾಲು,ಪಠ್ಯ)
        return ಪಠ್ಯ
    def 화소들():
        ಕ್ಲೈಂಟ್.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            ವರ್ಗ_ಮೌಲ್ಯ=정확한값(ಕ್ಲೈಂಟ್,1)[0]
            if ವರ್ಗ_ಮೌಲ್ಯ==2:continue
            if ವರ್ಗ_ಮೌಲ್ಯ==3:
                개수=struct.unpack('>I',정확한값(ಕ್ಲೈಂಟ್,7)[3:])[0];정확한값(ಕ್ಲೈಂಟ್,개수);continue
            assert ವರ್ಗ_ಮೌಲ್ಯ==0,ವರ್ಗ_ಮೌಲ್ಯ
            항목수=struct.unpack('>H',정확한값(ಕ್ಲೈಂಟ್,3)[1:])[0]
            for _ in range(항목수):
                x_ಸಮಭಾಜಕ,Y_ಬಟನ್_ಸಮನ್ವಯ,너비값,높이값,ಅಕ್ಷರ_ಸಮೂಹ=struct.unpack('>HHHHi',정확한값(ಕ್ಲೈಂಟ್,12));assert ಅಕ್ಷರ_ಸಮೂಹ==0,ಅಕ್ಷರ_ಸಮೂಹ
                ಡೇಟಾ=정확한값(ಕ್ಲೈಂಟ್,너비값*높이값*4)
                for ಅಡ್ಡಸಾಲು_ಹುದ್ದೆ in range(높이값):
                    for ಲಂಬಸಾಲು_ಹುದ್ದೆ in range(너비값):
                        원본자료=(ಅಡ್ಡಸಾಲು_ಹುದ್ದೆ*너비값+ಲಂಬಸಾಲು_ಹುದ್ದೆ)*4;ಲಕ್ಷ್ಯ=((Y_ಬಟನ್_ಸಮನ್ವಯ+ಅಡ್ಡಸಾಲು_ಹುದ್ದೆ)*640+x_ಸಮಭಾಜಕ+ಲಂಬಸಾಲು_ಹುದ್ದೆ)*3
                        빛삼원색[ಲಕ್ಷ್ಯ:ಲಕ್ಷ್ಯ+3]=bytes((ಡೇಟಾ[원본자료+2],ಡೇಟಾ[원본자료+1],ಡೇಟಾ[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        ಪೋರ್ಟ್_ಸಂಖ್ಯೆ=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        ಕ್ಲೈಂಟ್=socket.create_connection(('127.0.0.1',ಪೋರ್ಟ್_ಸಂಖ್ಯೆ),timeout=10)
        assert 정확한값(ಕ್ಲೈಂಟ್,12)==b'RFB 003.008\n';ಕ್ಲೈಂಟ್.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(ಕ್ಲೈಂಟ್,정확한값(ಕ್ಲೈಂಟ್,1)[0]);ಕ್ಲೈಂಟ್.sendall(b'\x01');assert 정확한값(ಕ್ಲೈಂಟ್,4)==b'\0'*4
        ಕ್ಲೈಂಟ್.sendall(b'\x01');초기값=정확한값(ಕ್ಲೈಂಟ್,24);정확한값(ಕ್ಲೈಂಟ್,struct.unpack('>I',초기값[20:])[0])
        ಕ್ಲೈಂಟ್.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        ಕ್ಲೈಂಟ್.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in ಶೆಲ್('ftpd start')
        ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ=ftplib.FTP();ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.encoding='utf-8';ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.connect('127.0.0.1',ಫೈಲ್_ವರ್ಗಾವಣೆ_ಪೋರ್ಟ್_ಸಂಖ್ಯೆ,timeout=20);ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.login()
        ಪೇಲೋಡ್_ಡೇಟಾ=('GUI와 FTP 동시 사용 '+ಭಾಷೆ+' 😀\n').encode()
        ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.storbinary('STOR 함께.txt',io.BytesIO(ಪೇಲೋಡ್_ಡೇಟಾ))
        assert ಪೇಲೋಡ್_ಡೇಟಾ.decode().strip() in ಶೆಲ್('cat /함께.txt')
        받은수=bytearray();ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==ಪೇಲೋಡ್_ಡೇಟಾ;ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        ಕಳುಹಿಸಿ_ಪಟ್ಟಿ=ಶೆಲ್('ls /example')
        assert all(ಹೆಸರು in ಕಳುಹಿಸಿ_ಪಟ್ಟಿ for ಹೆಸರು in ('java/','c/','python/','README.md')),ಕಳುಹಿಸಿ_ಪಟ್ಟಿ
        if ಭಾಷೆ=='java':
            꾸러미명세=json.loads((ಬಿಂಬಿಸು_ಮೂಲ/'build/examples/manifest.json').read_text())
            for ಮಾರ್ಗ,ನಮೂದು_ಬಿಂದು in 꾸러미명세.items():
                ಶೆಲ್('cp '+ಮಾರ್ಗ+' /example-check.bin')
                ವಿಷಯ_ಮೌಲ್ಯ=bytearray();ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.retrbinary('RETR example-check.bin',ವಿಷಯ_ಮೌಲ್ಯ.extend)
                assert len(ವಿಷಯ_ಮೌಲ್ಯ)==ನಮೂದು_ಬಿಂದು['bytes'] and hashlib.sha256(ವಿಷಯ_ಮೌಲ್ಯ).hexdigest()==ನಮೂದು_ಬಿಂದು['sha256'],ಮಾರ್ಗ
            ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            ದ್ವಿಮಾನ=bytes(range(256))*64
            ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.storbinary('STOR boundary.bin',io.BytesIO(ದ್ವಿಮಾನ))
            ವಿಷಯ_ಮೌಲ್ಯ=bytearray();ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.retrbinary('RETR boundary.bin',ವಿಷಯ_ಮೌಲ್ಯ.extend)
            assert ವಿಷಯ_ಮೌಲ್ಯ==ದ್ವಿಮಾನ and 'boundary.bin' in ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.nlst()
            ಶೆಲ್('cp /boundary.bin /boundary-copy.bin')
            ವಿಷಯ_ಮೌಲ್ಯ=bytearray();ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.retrbinary('RETR boundary-copy.bin',ವಿಷಯ_ಮೌಲ್ಯ.extend)
            assert ವಿಷಯ_ಮೌಲ್ಯ==ದ್ವಿಮಾನ
            ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.delete('boundary.bin');ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.delete('boundary-copy.bin')
        assert '출력예제' in ಶೆಲ್('ls /example/'+ಭಾಷೆ)
        ಶೆಲ್('cd /example/'+ಭಾಷೆ)
        ಹೆಸರು_ಕೋಷ್ಟಕ={'java':'JAVA','c':'C','python':'PYTHON'}[ಭಾಷೆ]
        예상파일=ಹೆಸರು_ಕೋಷ್ಟಕ+' ಕಡತ: 한글 ಡೇಟಾ 😀\n'
        if ಭಾಷೆ=='java':
            ಪೂರೈಸು_ಆದೇಶ('javac 출력예제.java','Compiled:');ಪೂರೈಸು_ಆದೇಶ('java 출력예제','JAVA ಔಟ್_ಪುಟ್: 안녕하세요 😀')
            ಪೂರೈಸು_ಆದೇಶ('javac 파일예제.java','Compiled:');ಪೂರೈಸು_ಆದೇಶ('java 파일예제',예상파일)
            ಪೂರೈಸು_ಆದೇಶ('java 네트워크예제 {} {}'.format(되돌림서버항목.ಪ್ರಸಾರ_ನಿಯಂತ್ರಣ_ಪ್ರೊಟೋಕಾಲ್_ಪೋರ್ಟ್,되돌림서버항목.전문접속번호),'JAVA 네트워크 ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು: TCP UDP 한글')
            ಗ್ರ್ಯಾಫಿಕ್ಸ್_ಆದೇಶ='java 그래픽예제'
        elif ಭಾಷೆ=='c':
            for ಹೆಸರು,전달값,예상결과 in [('ಔಟ್_ಪುಟ್','', 'C ಔಟ್_ಪುಟ್: 안녕하세요 😀'),('ಕಡತ','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು: UDP 한글')]:
                ಪೂರೈಸು_ಆದೇಶ('cc '+ಹೆಸರು+'예제.c -o ಪೂರೈಸು_ಆದೇಶ','Compiled native ARM64 ELF:')
                ಪೂರೈಸು_ಆದೇಶ('./ಪೂರೈಸು_ಆದೇಶ'+전달값,예상결과)
            ಪೂರೈಸು_ಆದೇಶ('cc 그래픽예제.c -o ಪೂರೈಸು_ಆದೇಶ','Compiled native ARM64 ELF:');ಗ್ರ್ಯಾಫಿಕ್ಸ್_ಆದೇಶ='./ಪೂರೈಸು_ಆದೇಶ'
        else:
            for ಹೆಸರು,전달값,예상결과 in [('ಔಟ್_ಪುಟ್','','PYTHON ಔಟ್_ಪುಟ್: 안녕하세요 😀'),('ಕಡತ','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು: UDP 한글')]:
                ಪೂರೈಸು_ಆದೇಶ('python '+ಹೆಸರು+'예제.py'+전달값,예상결과)
            ಗ್ರ್ಯಾಫಿಕ್ಸ್_ಆದೇಶ='python 그래픽예제.py'
        ಆರಂಭಿಸು_ಚಿತ್ರರಚನೆ=ಆರಂಭಿಸು_ಆಫ್_ಸೆಟ್(ಗ್ರ್ಯಾಫಿಕ್ಸ್_ಆದೇಶ)
        ಪಠ್ಯ=수신하기('그림을 확인한 ಹಿಂದೆ_ಮೌಲ್ಯ Enter를 누르세요.\r\n'.encode(),ಆರಂಭಿಸು_ಚಿತ್ರರಚನೆ)
        assert ಹೆಸರು_ಕೋಷ್ಟಕ+' 그래픽: 빨강 초록 파랑' in ಪಠ್ಯ and 'exit 0' not in ಪಠ್ಯ,ಪಠ್ಯ
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.delete('도중.txt')
        빛삼원색=화소들()
        for Y_ಬಟನ್_ಸಮನ್ವಯ,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ=(Y_ಬಟನ್_ಸಮನ್ವಯ*640+610)*3;assert tuple(빛삼원색[ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ:ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ+3])==색상,(ಭಾಷೆ,Y_ಬಟನ್_ಸಮನ್ವಯ,tuple(빛삼원색[ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ:ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(ಮಾಪನ_ಡೇಟಾ/(ಭಾಷೆ+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',ಆರಂಭಿಸು_ಚಿತ್ರರಚನೆ)
        if ಭಾಷೆ=='java':
            ಆರಂಭಿಸು_ವಿಂಡೋ=ಆರಂಭಿಸು_ಆಫ್_ಸೆಟ್('java 창예제')
            수신하기('GUI 예제 ಸಿದ್ಧಪಡಿಸು: 창예제'.encode(),ಆರಂಭಿಸು_ವಿಂಡೋ)
            def ಕ್ಲಿಕ್_ಮಾಡಿ_ಮೌಲ್ಯ(가로,ಲಂಬ_ಹುದ್ದೆ):
                for ಬಟನ್ in (1,0):ಕ್ಲೈಂಟ್.sendall(struct.pack('>BBHH',5,ಬಟನ್,가로,ಲಂಬ_ಹುದ್ದೆ))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            ಕ್ಲಿಕ್_ಮಾಡಿ_ಮೌಲ್ಯ(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for ಅಕ್ಷರ_ಮೌಲ್ಯ in '한글':누름값(0x1000000|ord(ಅಕ್ಷರ_ಮೌಲ್ಯ));누름값(0x1000000|ord(ಅಕ್ಷರ_ಮೌಲ್ಯ),False)
            for 횟수 in (1,2):
                ಚಲಾಯಿಸು_2=len(대화기록);ಕ್ಲಿಕ್_ಮಾಡಿ_ಮೌಲ್ಯ(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),ಚಲಾಯಿಸು_2)
            time.sleep(.3)
            ವಿಂಡೋ_ಚಿತ್ರರಚನೆ=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=ವಿಂಡೋ_ಚಿತ್ರರಚನೆ.crop((110,272,530,300)).tobytes()
            ವಿಂಡೋ_ಚಿತ್ರರಚನೆ.save(str(ಮಾಪನ_ಡೇಟಾ/'java-swing.png'))
            ಚಲಾಯಿಸು_2=len(대화기록);ಕ್ಲಿಕ್_ಮಾಡಿ_ಮೌಲ್ಯ(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',ಚಲಾಯಿಸು_2)
        # Download the guest-created bytes through FTP in the same GUI VM.
        ಫೈಲ್_ನಮೂದು_ಹೆಸರು={'java':'java.txt','c':'c.txt','python':'python.txt'}[ಭಾಷೆ]
        ಶೆಲ್('cp '+ಫೈಲ್_ನಮೂದು_ಹೆಸರು+' /ಸಕ್ರಮೀಕರಿಸು.txt')
        받은수=bytearray();ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.retrbinary('RETR ಸಕ್ರಮೀಕರಿಸು.txt',받은수.extend);assert 받은수==예상파일.encode()
        ಶೆಲ್('echo preserved > 출력예제.'+('py' if ಭಾಷೆ=='python' else ಭಾಷೆ))
        assert 'EXAMPLES READY' in ಶೆಲ್('example '+ಭಾಷೆ)
        assert '\npreserved\n' in ಶೆಲ್('cat 출력예제.'+('py' if ಭಾಷೆ=='python' else ಭಾಷೆ))
        assert '한/영 ಕೀ_ಮೌಲ್ಯ, Shift+Space 또는 F9' in ಶೆಲ್('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in ಶೆಲ್('echo GUI NETWORK TOGETHER')
        ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.quit();ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ=None;assert 'FTP stopped' in ಶೆಲ್('ftpd stop')
        print('PASS '+ಭಾಷೆ+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ:
            try:ಫೈಲ್_ವರ್ಗಾವಣೆ_ಸಂಪರ್ಕ.close()
            except OSError:pass
        if ಕ್ಲೈಂಟ್:ಕ್ಲೈಂಟ್.close()
        ಪ್ರಕ್ರಿಯೆ.terminate()
        try:ಪ್ರಕ್ರಿಯೆ.wait(timeout=8)
        except subprocess.TimeoutExpired:ಪ್ರಕ್ರಿಯೆ.kill();ಪ್ರಕ್ರಿಯೆ.wait()
        ಸೆಲೆಕ್ಟರ್.close();ಪ್ರಕ್ರಿಯೆ.stdout.close();(ಮಾಪನ_ಡೇಟಾ/(ಭಾಷೆ+'-serial.log')).write_bytes(대화기록)


def ಚಲಾಯಿಸು_2():
    ಮಾಪನ_ಡೇಟಾ=ಬಿಂಬಿಸು_ಮೂಲ/'build/verification/examples';ಮಾಪನ_ಡೇಟಾ.mkdir(parents=True,exist_ok=True)
    ದೃಢೀಕರಣ_ವರದಿ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ಬಿಂಬಿಸು_ಮೂಲ/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for ಭಾಷೆ in ('java','c','python'):
                test_언어(ಭಾಷೆ,되돌림서버항목,ಮಾಪನ_ಡೇಟಾ);ದೃಢೀಕರಣ_ವರದಿ['languages'].append(ಭಾಷೆ)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(ವರ್ಗ_ಮೌಲ್ಯ,ಡೇಟಾ.encode()) for ವರ್ಗ_ಮೌಲ್ಯ,ಡೇಟಾ in 예상결과],되돌림서버항목.수신됨
            ದೃಢೀಕರಣ_ವರದಿ['host_network_payloads']=[{'protocol':ವರ್ಗ_ಮೌಲ್ಯ,'text':ಡೇಟಾ.decode()} for ವರ್ಗ_ಮೌಲ್ಯ,ಡೇಟಾ in 되돌림서버항목.수신됨]
        ದೃಢೀಕರಣ_ವರದಿ.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(ಮಾಪನ_ಡೇಟಾ/'report.json').write_text(json.dumps(ದೃಢೀಕರಣ_ವರದಿ,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':ಚಲಾಯಿಸು_2()
