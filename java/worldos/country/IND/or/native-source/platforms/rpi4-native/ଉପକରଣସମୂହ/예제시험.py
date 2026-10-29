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
from ଡେସ୍କଟପ୍_ଭିୟୁ import 정확한값
from 예제되돌림서버 import 되돌림서버
from ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ import ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍


def test_언어(ଭାଷା,되돌림서버항목,ମାପ_ଡାଟା):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ପୋର୍ଟ୍_ନମ୍ଵର୍=임시자원.getsockname()[1]
    ପ୍ରକ୍ରିୟା=subprocess.Popen(['python3',str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'ଉପକରଣସମୂହ/ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ.py'),'--desktop','--network','--port','0','--ftp-port',str(ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ପୋର୍ଟ୍_ନମ୍ଵର୍)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    ଚୟନକାରୀ=selectors.DefaultSelector();ଚୟନକାରୀ.register(ପ୍ରକ୍ରିୟା.stdout,selectors.EVENT_READ)
    대화기록=bytearray();କ୍ଲାଏଣ୍ଟ=None;ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ=None
    def 수신하기(확인표시,ଚଳାନ୍ତୁ=0):
        ଶେଷ_କରନ୍ତୁ_ଅଫ୍_ସେଟ୍=time.monotonic()+60
        while 확인표시 not in 대화기록[ଚଳାନ୍ତୁ:]:
            if time.monotonic()>ଶେଷ_କରନ୍ତୁ_ଅଫ୍_ସେଟ୍ or ପ୍ରକ୍ରିୟା.poll() is not None:raise AssertionError(대화기록[ଚଳାନ୍ତୁ:].decode('utf-8','replace'))
            for 누름값,_ in ଚୟନକାରୀ.select(.1):
                ଡାଟା=누름값.fileobj.read(65536)
                if ଡାଟା:대화기록.extend(ଡାଟା)
        return 대화기록[ଚଳାନ୍ତୁ:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(ସଙ୍କେତ_ମୂଲ୍ୟ,누르는중=True):କ୍ଲାଏଣ୍ଟ.sendall(struct.pack('>BBHI',4,int(누르는중),0,ସଙ୍କେତ_ମୂଲ୍ୟ))
    def ଆରମ୍ଭ_ଅଫ୍_ସେଟ୍(ରେଖା):
        ଚଳାନ୍ତୁ=len(대화기록)
        for ବର୍ଣ୍ଣ_କୋଡ଼୍ in ରେଖା+'\n':
            ସଙ୍କେତ_ମୂଲ୍ୟ=0xff0d if ବର୍ଣ୍ଣ_କୋଡ଼୍=='\n' else ord(ବର୍ଣ୍ଣ_କୋଡ଼୍) if ord(ବର୍ଣ୍ଣ_କୋଡ଼୍)<256 else 0x1000000|ord(ବର୍ଣ୍ଣ_କୋଡ଼୍)
            누름값(ସଙ୍କେତ_ମୂଲ୍ୟ);누름값(ସଙ୍କେତ_ମୂଲ୍ୟ,False)
        return ଚଳାନ୍ତୁ
    def ଖୋଳ(ରେଖା):return 수신하기(b'jkoros-native> ',ଆରମ୍ଭ_ଅଫ୍_ସେଟ୍(ରେଖା))
    def ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ(ରେଖା,예상결과):
        ପାଠ୍ଯ=ଖୋଳ(ରେଖା);assert 예상결과 in ପାଠ୍ଯ and 'exit 0' in ପାଠ୍ଯ,(ରେଖା,ପାଠ୍ଯ)
        return ପାଠ୍ଯ
    def 화소들():
        କ୍ଲାଏଣ୍ଟ.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            ବର୍ଗ_ମୂଲ୍ୟ=정확한값(କ୍ଲାଏଣ୍ଟ,1)[0]
            if ବର୍ଗ_ମୂଲ୍ୟ==2:continue
            if ବର୍ଗ_ମୂଲ୍ୟ==3:
                개수=struct.unpack('>I',정확한값(କ୍ଲାଏଣ୍ଟ,7)[3:])[0];정확한값(କ୍ଲାଏଣ୍ଟ,개수);continue
            assert ବର୍ଗ_ମୂଲ୍ୟ==0,ବର୍ଗ_ମୂଲ୍ୟ
            항목수=struct.unpack('>H',정확한값(କ୍ଲାଏଣ୍ଟ,3)[1:])[0]
            for _ in range(항목수):
                x_ସଂଯୋଜନ,세로좌표,너비값,높이값,ବର୍ଣ୍ଣ_ସେଟ୍=struct.unpack('>HHHHi',정확한값(କ୍ଲାଏଣ୍ଟ,12));assert ବର୍ଣ୍ଣ_ସେଟ୍==0,ବର୍ଣ୍ଣ_ସେଟ୍
                ଡାଟା=정확한값(କ୍ଲାଏଣ୍ଟ,너비값*높이값*4)
                for ଧାଡ଼ି_ସ୍ଥିତି in range(높이값):
                    for ସ୍ତମ୍ଭ_ସ୍ଥିତି in range(너비값):
                        원본자료=(ଧାଡ଼ି_ସ୍ଥିତି*너비값+ସ୍ତମ୍ଭ_ସ୍ଥିତି)*4;ଲକ୍ଷ୍ୟସ୍ଥଳ=((세로좌표+ଧାଡ଼ି_ସ୍ଥିତି)*640+x_ସଂଯୋଜନ+ସ୍ତମ୍ଭ_ସ୍ଥିତି)*3
                        빛삼원색[ଲକ୍ଷ୍ୟସ୍ଥଳ:ଲକ୍ଷ୍ୟସ୍ଥଳ+3]=bytes((ଡାଟା[원본자료+2],ଡାଟା[원본자료+1],ଡାଟା[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        ପୋର୍ଟ୍_ନମ୍ଵର୍=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        କ୍ଲାଏଣ୍ଟ=socket.create_connection(('127.0.0.1',ପୋର୍ଟ୍_ନମ୍ଵର୍),timeout=10)
        assert 정확한값(କ୍ଲାଏଣ୍ଟ,12)==b'RFB 003.008\n';କ୍ଲାଏଣ୍ଟ.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(କ୍ଲାଏଣ୍ଟ,정확한값(କ୍ଲାଏଣ୍ଟ,1)[0]);କ୍ଲାଏଣ୍ଟ.sendall(b'\x01');assert 정확한값(କ୍ଲାଏଣ୍ଟ,4)==b'\0'*4
        କ୍ଲାଏଣ୍ଟ.sendall(b'\x01');초기값=정확한값(କ୍ଲାଏଣ୍ଟ,24);정확한값(କ୍ଲାଏଣ୍ଟ,struct.unpack('>I',초기값[20:])[0])
        କ୍ଲାଏଣ୍ଟ.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        କ୍ଲାଏଣ୍ଟ.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in ଖୋଳ('ftpd start')
        ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ=ftplib.FTP();ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.encoding='utf-8';ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.connect('127.0.0.1',ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ପୋର୍ଟ୍_ନମ୍ଵର୍,timeout=20);ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.login()
        ପେଲୋଡ୍_ଡାଟା=('GUI와 FTP 동시 사용 '+ଭାଷା+' 😀\n').encode()
        ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.storbinary('STOR 함께.txt',io.BytesIO(ପେଲୋଡ୍_ଡାଟା))
        assert ପେଲୋଡ୍_ଡାଟା.decode().strip() in ଖୋଳ('cat /함께.txt')
        받은수=bytearray();ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==ପେଲୋଡ୍_ଡାଟା;ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        ପଠାନ୍ତୁ_ତାଲିକା=ଖୋଳ('ls /example')
        assert all(ନାମ in ପଠାନ୍ତୁ_ତାଲିକା for ନାମ in ('java/','c/','python/','README.md')),ପଠାନ୍ତୁ_ତାଲିକା
        if ଭାଷା=='java':
            꾸러미명세=json.loads((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/examples/manifest.json').read_text())
            for ପଥ,ଏଣ୍ଟ୍ରି_ପଏଣ୍ଟ୍ in 꾸러미명세.items():
                ଖୋଳ('cp '+ପଥ+' /example-check.bin')
                ବିଷୟ_ମୂଲ୍ୟ=bytearray();ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.retrbinary('RETR example-check.bin',ବିଷୟ_ମୂଲ୍ୟ.extend)
                assert len(ବିଷୟ_ମୂଲ୍ୟ)==ଏଣ୍ଟ୍ରି_ପଏଣ୍ଟ୍['bytes'] and hashlib.sha256(ବିଷୟ_ମୂଲ୍ୟ).hexdigest()==ଏଣ୍ଟ୍ରି_ପଏଣ୍ଟ୍['sha256'],ପଥ
            ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            ବାଇନାରୀ=bytes(range(256))*64
            ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.storbinary('STOR boundary.bin',io.BytesIO(ବାଇନାରୀ))
            ବିଷୟ_ମୂଲ୍ୟ=bytearray();ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.retrbinary('RETR boundary.bin',ବିଷୟ_ମୂଲ୍ୟ.extend)
            assert ବିଷୟ_ମୂଲ୍ୟ==ବାଇନାରୀ and 'boundary.bin' in ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.nlst()
            ଖୋଳ('cp /boundary.bin /boundary-copy.bin')
            ବିଷୟ_ମୂଲ୍ୟ=bytearray();ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.retrbinary('RETR boundary-copy.bin',ବିଷୟ_ମୂଲ୍ୟ.extend)
            assert ବିଷୟ_ମୂଲ୍ୟ==ବାଇନାରୀ
            ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.delete('boundary.bin');ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.delete('boundary-copy.bin')
        assert '출력예제' in ଖୋଳ('ls /example/'+ଭାଷା)
        ଖୋଳ('cd /example/'+ଭାଷା)
        ନାମ_ସାରଣୀ={'java':'JAVA','c':'C','python':'PYTHON'}[ଭାଷା]
        예상파일=ନାମ_ସାରଣୀ+' ଫାଇଲ: 한글 ଡାଟା 😀\n'
        if ଭାଷା=='java':
            ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ('javac 출력예제.java','Compiled:');ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ('java 출력예제','JAVA ନିର୍ଗମ: 안녕하세요 😀')
            ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ('javac 파일예제.java','Compiled:');ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ('java 파일예제',예상파일)
            ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ('java 네트워크예제 {} {}'.format(되돌림서버항목.ପ୍ରେରଣ_ନିୟନ୍ତ୍ରଣ_ପ୍ରୋଟୋକଲ୍_ପୋର୍ଟ,되돌림서버항목.전문접속번호),'JAVA 네트워크 ଯାଞ୍ଚ୍_କରିବା: TCP UDP 한글')
            ଗ୍ରାଫିକ୍ସ_ନିର୍ଦ୍ଦେଶ='java 그래픽예제'
        elif ଭାଷା=='c':
            for ନାମ,전달값,예상결과 in [('ନିର୍ଗମ','', 'C ନିର୍ଗମ: 안녕하세요 😀'),('ଫାଇଲ','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 ଯାଞ୍ଚ୍_କରିବା: UDP 한글')]:
                ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ('cc '+ନାମ+'예제.c -o ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ','Compiled native ARM64 ELF:')
                ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ('./ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ'+전달값,예상결과)
            ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ('cc 그래픽예제.c -o ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ','Compiled native ARM64 ELF:');ଗ୍ରାଫିକ୍ସ_ନିର୍ଦ୍ଦେଶ='./ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ'
        else:
            for ନାମ,전달값,예상결과 in [('ନିର୍ଗମ','','PYTHON ନିର୍ଗମ: 안녕하세요 😀'),('ଫାଇଲ','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 ଯାଞ୍ଚ୍_କରିବା: UDP 한글')]:
                ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ('python '+ନାମ+'예제.py'+전달값,예상결과)
            ଗ୍ରାଫିକ୍ସ_ନିର୍ଦ୍ଦେଶ='python 그래픽예제.py'
        ଆରମ୍ଭ_ଅଙ୍କନ=ଆରମ୍ଭ_ଅଫ୍_ସେଟ୍(ଗ୍ରାଫିକ୍ସ_ନିର୍ଦ୍ଦେଶ)
        ପାଠ୍ଯ=수신하기('그림을 확인한 ପଛ_ମୂଲ୍ୟ Enter를 누르세요.\r\n'.encode(),ଆରମ୍ଭ_ଅଙ୍କନ)
        assert ନାମ_ସାରଣୀ+' 그래픽: 빨강 초록 파랑' in ପାଠ୍ଯ and 'exit 0' not in ପାଠ୍ଯ,ପାଠ୍ଯ
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ=(세로좌표*640+610)*3;assert tuple(빛삼원색[ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ:ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ+3])==색상,(ଭାଷା,세로좌표,tuple(빛삼원색[ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ:ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(ମାପ_ଡାଟା/(ଭାଷା+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',ଆରମ୍ଭ_ଅଙ୍କନ)
        if ଭାଷା=='java':
            ଆରମ୍ଭ_ଓ୍ୱିଣ୍ଡୋ=ଆରମ୍ଭ_ଅଫ୍_ସେଟ୍('java 창예제')
            수신하기('GUI 예제 ପ୍ରସ୍ତୁତ: 창예제'.encode(),ଆରମ୍ଭ_ଓ୍ୱିଣ୍ଡୋ)
            def କ୍ଲିକ୍_କରିବା_ମୂଲ୍ୟ(가로,ଅନୁଲମ୍ବ_ସ୍ଥିତି):
                for ବଟନ୍ in (1,0):କ୍ଲାଏଣ୍ଟ.sendall(struct.pack('>BBHH',5,ବଟନ୍,가로,ଅନୁଲମ୍ବ_ସ୍ଥିତି))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            କ୍ଲିକ୍_କରିବା_ମୂଲ୍ୟ(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for ବର୍ଣ୍ଣ_ମୂଲ୍ୟ in '한글':누름값(0x1000000|ord(ବର୍ଣ୍ଣ_ମୂଲ୍ୟ));누름값(0x1000000|ord(ବର୍ଣ୍ଣ_ମୂଲ୍ୟ),False)
            for 횟수 in (1,2):
                ଚଳାନ୍ତୁ=len(대화기록);କ୍ଲିକ୍_କରିବା_ମୂଲ୍ୟ(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),ଚଳାନ୍ତୁ)
            time.sleep(.3)
            ଓ୍ୱିଣ୍ଡୋ_ଅଙ୍କନ=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=ଓ୍ୱିଣ୍ଡୋ_ଅଙ୍କନ.crop((110,272,530,300)).tobytes()
            ଓ୍ୱିଣ୍ଡୋ_ଅଙ୍କନ.save(str(ମାପ_ଡାଟା/'java-swing.png'))
            ଚଳାନ୍ତୁ=len(대화기록);କ୍ଲିକ୍_କରିବା_ମୂଲ୍ୟ(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',ଚଳାନ୍ତୁ)
        # Download the guest-created bytes through FTP in the same GUI VM.
        ଫାଇଲ୍_ଏଣ୍ଟ୍ରି_ନାମ={'java':'java.txt','c':'c.txt','python':'python.txt'}[ଭାଷା]
        ଖୋଳ('cp '+ଫାଇଲ୍_ଏଣ୍ଟ୍ରି_ନାମ+' /ବୈଧକରଣ.txt')
        받은수=bytearray();ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.retrbinary('RETR ବୈଧକରଣ.txt',받은수.extend);assert 받은수==예상파일.encode()
        ଖୋଳ('echo preserved > 출력예제.'+('py' if ଭାଷା=='python' else ଭାଷା))
        assert 'EXAMPLES READY' in ଖୋଳ('example '+ଭାଷା)
        assert '\npreserved\n' in ଖୋଳ('cat 출력예제.'+('py' if ଭାଷା=='python' else ଭାଷା))
        assert '한/영 କୀ_ମୂଲ୍ୟ, Shift+Space 또는 F9' in ଖୋଳ('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in ଖୋଳ('echo GUI NETWORK TOGETHER')
        ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.quit();ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ=None;assert 'FTP stopped' in ଖୋଳ('ftpd stop')
        print('PASS '+ଭାଷା+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ:
            try:ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.close()
            except OSError:pass
        if କ୍ଲାଏଣ୍ଟ:କ୍ଲାଏଣ୍ଟ.close()
        ପ୍ରକ୍ରିୟା.terminate()
        try:ପ୍ରକ୍ରିୟା.wait(timeout=8)
        except subprocess.TimeoutExpired:ପ୍ରକ୍ରିୟା.kill();ପ୍ରକ୍ରିୟା.wait()
        ଚୟନକାରୀ.close();ପ୍ରକ୍ରିୟା.stdout.close();(ମାପ_ଡାଟା/(ଭାଷା+'-serial.log')).write_bytes(대화기록)


def ଚଳାନ୍ତୁ():
    ମାପ_ଡାଟା=ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/verification/examples';ମାପ_ଡାଟା.mkdir(parents=True,exist_ok=True)
    ବୈଧକରଣ_ରିପୋର୍ଟ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for ଭାଷା in ('java','c','python'):
                test_언어(ଭାଷା,되돌림서버항목,ମାପ_ଡାଟା);ବୈଧକରଣ_ରିପୋର୍ଟ['languages'].append(ଭାଷା)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(ବର୍ଗ_ମୂଲ୍ୟ,ଡାଟା.encode()) for ବର୍ଗ_ମୂଲ୍ୟ,ଡାଟା in 예상결과],되돌림서버항목.수신됨
            ବୈଧକରଣ_ରିପୋର୍ଟ['host_network_payloads']=[{'protocol':ବର୍ଗ_ମୂଲ୍ୟ,'text':ଡାଟା.decode()} for ବର୍ଗ_ମୂଲ୍ୟ,ଡାଟା in 되돌림서버항목.수신됨]
        ବୈଧକରଣ_ରିପୋର୍ଟ.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(ମାପ_ଡାଟା/'report.json').write_text(json.dumps(ବୈଧକରଣ_ରିପୋର୍ଟ,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':ଚଳାନ୍ତୁ()
