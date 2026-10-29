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
from ᎦᏍᎩᎶᎩ_ᎦᏚ_ᎯᎪᎵᏯ import 정확한값
from 예제되돌림서버 import 되돌림서버
from ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ import 기준


def ᎠᏓᎪᎵᏰᏍᎩ_ᎦᏬᏂᎯᏍᏗ(ᎦᏬᏂᎯᏍᏗ,되돌림서버항목,결과자료):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    ᎢᏯᏛᏁᎵᏓᏍᏗ=subprocess.Popen(['python3',str(기준/'도구/ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    ᎠᏑᏰᏍᎩ=selectors.DefaultSelector();ᎠᏑᏰᏍᎩ.register(ᎢᏯᏛᏁᎵᏓᏍᏗ.stdout,selectors.EVENT_READ)
    대화기록=bytearray();ᎠᏥᏍᏕᎵᏍᎩ=None;ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ=None
    def 수신하기(확인표시,ᎠᎢᏎᏍᏗ=0):
        끝위치=time.monotonic()+60
        while 확인표시 not in 대화기록[ᎠᎢᏎᏍᏗ:]:
            if time.monotonic()>끝위치 or ᎢᏯᏛᏁᎵᏓᏍᏗ.poll() is not None:raise AssertionError(대화기록[ᎠᎢᏎᏍᏗ:].decode('utf-8','replace'))
            for 누름값,_ in ᎠᏑᏰᏍᎩ.select(.1):
                ᎦᏟᏌᏅᎯ=누름값.fileobj.read(65536)
                if ᎦᏟᏌᏅᎯ:대화기록.extend(ᎦᏟᏌᏅᎯ)
        return 대화기록[ᎠᎢᏎᏍᏗ:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(심볼,누르는중=True):ᎠᏥᏍᏕᎵᏍᎩ.sendall(struct.pack('>BBHI',4,int(누르는중),0,심볼))
    def 시작위치(ᏚᏓᏅᏅᎢ):
        ᎠᎢᏎᏍᏗ=len(대화기록)
        for 문자값 in ᏚᏓᏅᏅᎢ+'\n':
            심볼=0xff0d if 문자값=='\n' else ord(문자값) if ord(문자값)<256 else 0x1000000|ord(문자값)
            누름값(심볼);누름값(심볼,False)
        return ᎠᎢᏎᏍᏗ
    def ᎤᏯᏍᎦ(ᏚᏓᏅᏅᎢ):return 수신하기(b'jkoros-native> ',시작위치(ᏚᏓᏅᏅᎢ))
    def ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ(ᏚᏓᏅᏅᎢ,예상결과):
        ᎠᎪᎵᏰᏗ=ᎤᏯᏍᎦ(ᏚᏓᏅᏅᎢ);assert 예상결과 in ᎠᎪᎵᏰᏗ and 'exit 0' in ᎠᎪᎵᏰᏗ,(ᏚᏓᏅᏅᎢ,ᎠᎪᎵᏰᏗ)
        return ᎠᎪᎵᏰᏗ
    def 화소들():
        ᎠᏥᏍᏕᎵᏍᎩ.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ=정확한값(ᎠᏥᏍᏕᎵᏍᎩ,1)[0]
            if ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ==2:continue
            if ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ==3:
                개수=struct.unpack('>I',정확한값(ᎠᏥᏍᏕᎵᏍᎩ,7)[3:])[0];정확한값(ᎠᏥᏍᏕᎵᏍᎩ,개수);continue
            assert ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ==0,ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ
            항목수=struct.unpack('>H',정확한값(ᎠᏥᏍᏕᎵᏍᎩ,3)[1:])[0]
            for _ in range(항목수):
                가로좌표,세로좌표,너비값,높이값,ᎪᏪᎸ_ᎤᎾᏓᏡᎬ=struct.unpack('>HHHHi',정확한값(ᎠᏥᏍᏕᎵᏍᎩ,12));assert ᎪᏪᎸ_ᎤᎾᏓᏡᎬ==0,ᎪᏪᎸ_ᎤᎾᏓᏡᎬ
                ᎦᏟᏌᏅᎯ=정확한값(ᎠᏥᏍᏕᎵᏍᎩ,너비값*높이값*4)
                for 행위치 in range(높이값):
                    for 열위치 in range(너비값):
                        원본자료=(행위치*너비값+열위치)*4;ᎠᏉᏅᏗᎢ=((세로좌표+행위치)*640+가로좌표+열위치)*3
                        빛삼원색[ᎠᏉᏅᏗᎢ:ᎠᏉᏅᏗᎢ+3]=bytes((ᎦᏟᏌᏅᎯ[원본자료+2],ᎦᏟᏌᏅᎯ[원본자료+1],ᎦᏟᏌᏅᎯ[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        ᎠᏥᏍᏕᎵᏍᎩ=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert 정확한값(ᎠᏥᏍᏕᎵᏍᎩ,12)==b'RFB 003.008\n';ᎠᏥᏍᏕᎵᏍᎩ.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(ᎠᏥᏍᏕᎵᏍᎩ,정확한값(ᎠᏥᏍᏕᎵᏍᎩ,1)[0]);ᎠᏥᏍᏕᎵᏍᎩ.sendall(b'\x01');assert 정확한값(ᎠᏥᏍᏕᎵᏍᎩ,4)==b'\0'*4
        ᎠᏥᏍᏕᎵᏍᎩ.sendall(b'\x01');초기값=정확한값(ᎠᏥᏍᏕᎵᏍᎩ,24);정확한값(ᎠᏥᏍᏕᎵᏍᎩ,struct.unpack('>I',초기값[20:])[0])
        ᎠᏥᏍᏕᎵᏍᎩ.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        ᎠᏥᏍᏕᎵᏍᎩ.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in ᎤᏯᏍᎦ('ftpd start')
        ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ=ftplib.FTP();ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.encoding='utf-8';ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.connect('127.0.0.1',파일전송접속번호,timeout=20);ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.login()
        ᎠᎫᏴᏗ_ᎠᎧᎵᎢ_ᎦᏟᏌᏅᎯ=('GUI와 FTP 동시 사용 '+ᎦᏬᏂᎯᏍᏗ+' 😀\n').encode()
        ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.storbinary('STOR 함께.txt',io.BytesIO(ᎠᎫᏴᏗ_ᎠᎧᎵᎢ_ᎦᏟᏌᏅᎯ))
        assert ᎠᎫᏴᏗ_ᎠᎧᎵᎢ_ᎦᏟᏌᏅᎯ.decode().strip() in ᎤᏯᏍᎦ('cat /함께.txt')
        받은수=bytearray();ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==ᎠᎫᏴᏗ_ᎠᎧᎵᎢ_ᎦᏟᏌᏅᎯ;ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        ᏫᎦᏅᏗ_ᏕᎦᏅᏅᏛ=ᎤᏯᏍᎦ('ls /example')
        assert all(ᏚᏙᎥᎢ in ᏫᎦᏅᏗ_ᏕᎦᏅᏅᏛ for ᏚᏙᎥᎢ in ('java/','c/','python/','README.md')),ᏫᎦᏅᏗ_ᏕᎦᏅᏅᏛ
        if ᎦᏬᏂᎯᏍᏗ=='java':
            꾸러미명세=json.loads((기준/'build/examples/manifest.json').read_text())
            for ᎠᏍᏓᏩᏛᏍᏗ,Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᎤᏓᏓᏟ in 꾸러미명세.items():
                ᎤᏯᏍᎦ('cp '+ᎠᏍᏓᏩᏛᏍᏗ+' /example-check.bin')
                ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ=bytearray();ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.retrbinary('RETR example-check.bin',ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ.extend)
                assert len(ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ)==Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᎤᏓᏓᏟ['bytes'] and hashlib.sha256(ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ).hexdigest()==Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᎤᏓᏓᏟ['sha256'],ᎠᏍᏓᏩᏛᏍᏗ
            ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            binary=bytes(range(256))*64
            ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.storbinary('STOR boundary.bin',io.BytesIO(binary))
            ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ=bytearray();ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.retrbinary('RETR boundary.bin',ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ.extend)
            assert ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ==binary and 'boundary.bin' in ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.nlst()
            ᎤᏯᏍᎦ('cp /boundary.bin /boundary-copy.bin')
            ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ=bytearray();ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.retrbinary('RETR boundary-copy.bin',ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ.extend)
            assert ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ==binary
            ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.delete('boundary.bin');ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.delete('boundary-copy.bin')
        assert '출력예제' in ᎤᏯᏍᎦ('ls /example/'+ᎦᏬᏂᎯᏍᏗ)
        ᎤᏯᏍᎦ('cd /example/'+ᎦᏬᏂᎯᏍᏗ)
        ᏚᏙᎥᎢ_ᏧᎾᎶᎢᏓ={'java':'JAVA','c':'C','python':'PYTHON'}[ᎦᏬᏂᎯᏍᏗ]
        예상파일=ᏚᏙᎥᎢ_ᏧᎾᎶᎢᏓ+' ᎠᏍᏆᏂᎪᏙᏗ: 한글 ᎦᏟᏌᏅᎯ 😀\n'
        if ᎦᏬᏂᎯᏍᏗ=='java':
            ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ('javac 출력예제.java','Compiled:');ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ('java 출력예제','JAVA 출력: 안녕하세요 😀')
            ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ('javac 파일예제.java','Compiled:');ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ('java 파일예제',예상파일)
            ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ('java 네트워크예제 {} {}'.format(되돌림서버항목.TCP_ᎫᏓᎸᏗ,되돌림서버항목.전문접속번호),'JAVA 네트워크 ᎰᎯᏳᏓ: TCP UDP 한글')
            그림명령='java 그래픽예제'
        elif ᎦᏬᏂᎯᏍᏗ=='c':
            for ᏚᏙᎥᎢ,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('ᎠᏍᏆᏂᎪᏙᏗ','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 ᎰᎯᏳᏓ: UDP 한글')]:
                ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ('cc '+ᏚᏙᎥᎢ+'예제.c -o ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ','Compiled native ARM64 ELF:')
                ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ('./ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ'+전달값,예상결과)
            ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ('cc 그래픽예제.c -o ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ','Compiled native ARM64 ELF:');그림명령='./ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ'
        else:
            for ᏚᏙᎥᎢ,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('ᎠᏍᏆᏂᎪᏙᏗ','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 ᎰᎯᏳᏓ: UDP 한글')]:
                ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ('python '+ᏚᏙᎥᎢ+'예제.py'+전달값,예상결과)
            그림명령='python 그래픽예제.py'
        ᎭᏂᎩᏍᏓ_ᎠᏍᏓᏅᎿᏂᏙᎸ=시작위치(그림명령)
        ᎠᎪᎵᏰᏗ=수신하기('그림을 확인한 ᎠᎰᏂ_ᏧᎬᏩᎶᏗᏯ Enter를 누르세요.\r\n'.encode(),ᎭᏂᎩᏍᏓ_ᎠᏍᏓᏅᎿᏂᏙᎸ)
        assert ᏚᏙᎥᎢ_ᏧᎾᎶᎢᏓ+' 그래픽: 빨강 초록 파랑' in ᎠᎪᎵᏰᏗ and 'exit 0' not in ᎠᎪᎵᏰᏗ,ᎠᎪᎵᏰᏗ
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            변위=(세로좌표*640+610)*3;assert tuple(빛삼원색[변위:변위+3])==색상,(ᎦᏬᏂᎯᏍᏗ,세로좌표,tuple(빛삼원색[변위:변위+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(결과자료/(ᎦᏬᏂᎯᏍᏗ+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',ᎭᏂᎩᏍᏓ_ᎠᏍᏓᏅᎿᏂᏙᎸ)
        if ᎦᏬᏂᎯᏍᏗ=='java':
            ᎭᏂᎩᏍᏓ_ᏦᎳᏂ=시작위치('java 창예제')
            수신하기('GUI 예제 ᎭᏛᏅᎢᏍᏓ: 창예제'.encode(),ᎭᏂᎩᏍᏓ_ᏦᎳᏂ)
            def ᎭᏐᏅᏍᏓ_ᏧᎬᏩᎶᏗᏯ(가로,세로):
                for ᎠᏐᏅᏍᏙᏗ in (1,0):ᎠᏥᏍᏕᎵᏍᎩ.sendall(struct.pack('>BBHH',5,ᎠᏐᏅᏍᏙᏗ,가로,세로))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            ᎭᏐᏅᏍᏓ_ᏧᎬᏩᎶᏗᏯ(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ in '한글':누름값(0x1000000|ord(ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ));누름값(0x1000000|ord(ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ),False)
            for 횟수 in (1,2):
                ᎠᎢᏎᏍᏗ=len(대화기록);ᎭᏐᏅᏍᏓ_ᏧᎬᏩᎶᏗᏯ(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),ᎠᎢᏎᏍᏗ)
            time.sleep(.3)
            ᏦᎳᏂ_ᎠᏍᏓᏅᎿᏂᏙᎸ=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=ᏦᎳᏂ_ᎠᏍᏓᏅᎿᏂᏙᎸ.crop((110,272,530,300)).tobytes()
            ᏦᎳᏂ_ᎠᏍᏓᏅᎿᏂᏙᎸ.save(str(결과자료/'java-swing.png'))
            ᎠᎢᏎᏍᏗ=len(대화기록);ᎭᏐᏅᏍᏓ_ᏧᎬᏩᎶᏗᏯ(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',ᎠᎢᏎᏍᏗ)
        # Download the guest-created bytes through FTP in the same GUI VM.
        ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏚᏙᎥᎢ={'java':'java.txt','c':'c.txt','python':'python.txt'}[ᎦᏬᏂᎯᏍᏗ]
        ᎤᏯᏍᎦ('cp '+ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏚᏙᎥᎢ+' /ᎪᎯᏳᏙᏗ.txt')
        받은수=bytearray();ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.retrbinary('RETR ᎪᎯᏳᏙᏗ.txt',받은수.extend);assert 받은수==예상파일.encode()
        ᎤᏯᏍᎦ('echo preserved > 출력예제.'+('py' if ᎦᏬᏂᎯᏍᏗ=='python' else ᎦᏬᏂᎯᏍᏗ))
        assert 'EXAMPLES READY' in ᎤᏯᏍᎦ('example '+ᎦᏬᏂᎯᏍᏗ)
        assert '\npreserved\n' in ᎤᏯᏍᎦ('cat 출력예제.'+('py' if ᎦᏬᏂᎯᏍᏗ=='python' else ᎦᏬᏂᎯᏍᏗ))
        assert '한/영 ᏍᏚᎢᏍᏗ_ᏧᎬᏩᎶᏗᏯ, Shift+Space 또는 F9' in ᎤᏯᏍᎦ('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in ᎤᏯᏍᎦ('echo GUI NETWORK TOGETHER')
        ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.quit();ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ=None;assert 'FTP stopped' in ᎤᏯᏍᎦ('ftpd stop')
        print('PASS '+ᎦᏬᏂᎯᏍᏗ+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ:
            try:ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.close()
            except OSError:pass
        if ᎠᏥᏍᏕᎵᏍᎩ:ᎠᏥᏍᏕᎵᏍᎩ.close()
        ᎢᏯᏛᏁᎵᏓᏍᏗ.terminate()
        try:ᎢᏯᏛᏁᎵᏓᏍᏗ.wait(timeout=8)
        except subprocess.TimeoutExpired:ᎢᏯᏛᏁᎵᏓᏍᏗ.kill();ᎢᏯᏛᏁᎵᏓᏍᏗ.wait()
        ᎠᏑᏰᏍᎩ.close();ᎢᏯᏛᏁᎵᏓᏍᏗ.stdout.close();(결과자료/(ᎦᏬᏂᎯᏍᏗ+'-serial.log')).write_bytes(대화기록)


def ᎠᎢᏎᏍᏗ():
    결과자료=기준/'build/verification/examples';결과자료.mkdir(parents=True,exist_ok=True)
    ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for ᎦᏬᏂᎯᏍᏗ in ('java','c','python'):
                ᎠᏓᎪᎵᏰᏍᎩ_ᎦᏬᏂᎯᏍᏗ(ᎦᏬᏂᎯᏍᏗ,되돌림서버항목,결과자료);ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ['languages'].append(ᎦᏬᏂᎯᏍᏗ)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ,ᎦᏟᏌᏅᎯ.encode()) for ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ,ᎦᏟᏌᏅᎯ in 예상결과],되돌림서버항목.수신됨
            ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ['host_network_payloads']=[{'protocol':ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ,'text':ᎦᏟᏌᏅᎯ.decode()} for ᎦᏟᏌᏅᎯ_ᏧᎬᏩᎶᏗᏯ,ᎦᏟᏌᏅᎯ in 되돌림서버항목.수신됨]
        ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(결과자료/'report.json').write_text(json.dumps(ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':ᎠᎢᏎᏍᏗ()
