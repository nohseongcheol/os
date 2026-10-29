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
from ਡੈਸਕਟੌਪ_ਦ੍ਰਿਸ਼ import 정확한값
from 예제되돌림서버 import 되돌림서버
from ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ import ਪ੍ਰੋਜੈਕਟ_ਰੂਟ


def test_언어(ਭਾਸ਼ਾ,되돌림서버항목,ਮਾਪ_ਸਮੱਗਰੀ):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    ਪਰੋਸੈੱਸ=subprocess.Popen(['python3',str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'ਸਾਧਨ/ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    ਚੋਣਕਰਤਾ=selectors.DefaultSelector();ਚੋਣਕਰਤਾ.register(ਪਰੋਸੈੱਸ.stdout,selectors.EVENT_READ)
    대화기록=bytearray();ਗਾਹਕ=None;ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ=None
    def 수신하기(확인표시,ਚਲਾਓ_2=0):
        ਅੰਤ_ਔਫਸੈਟ=time.monotonic()+60
        while 확인표시 not in 대화기록[ਚਲਾਓ_2:]:
            if time.monotonic()>ਅੰਤ_ਔਫਸੈਟ or ਪਰੋਸੈੱਸ.poll() is not None:raise AssertionError(대화기록[ਚਲਾਓ_2:].decode('utf-8','replace'))
            for 누름값,_ in ਚੋਣਕਰਤਾ.select(.1):
                ਸਮੱਗਰੀ=누름값.fileobj.read(65536)
                if ਸਮੱਗਰੀ:대화기록.extend(ਸਮੱਗਰੀ)
        return 대화기록[ਚਲਾਓ_2:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(ਪ੍ਰਤੀਕ_ਕੀਮਤ,누르는중=True):ਗਾਹਕ.sendall(struct.pack('>BBHI',4,int(누르는중),0,ਪ੍ਰਤੀਕ_ਕੀਮਤ))
    def ਸੁਰੂ_ਔਫਸੈਟ(ਲਾਈਨ):
        ਚਲਾਓ_2=len(대화기록)
        for ਵਰਣ_ਕੋਡ in ਲਾਈਨ+'\n':
            ਪ੍ਰਤੀਕ_ਕੀਮਤ=0xff0d if ਵਰਣ_ਕੋਡ=='\n' else ord(ਵਰਣ_ਕੋਡ) if ord(ਵਰਣ_ਕੋਡ)<256 else 0x1000000|ord(ਵਰਣ_ਕੋਡ)
            누름값(ਪ੍ਰਤੀਕ_ਕੀਮਤ);누름값(ਪ੍ਰਤੀਕ_ਕੀਮਤ,False)
        return ਚਲਾਓ_2
    def ਸ਼ੈਲ(ਲਾਈਨ):return 수신하기(b'jkoros-native> ',ਸੁਰੂ_ਔਫਸੈਟ(ਲਾਈਨ))
    def ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼(ਲਾਈਨ,예상결과):
        ਟੈਕਸਟ=ਸ਼ੈਲ(ਲਾਈਨ);assert 예상결과 in ਟੈਕਸਟ and 'exit 0' in ਟੈਕਸਟ,(ਲਾਈਨ,ਟੈਕਸਟ)
        return ਟੈਕਸਟ
    def 화소들():
        ਗਾਹਕ.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            ਸ਼੍ਰੇਣੀ_ਕੀਮਤ=정확한값(ਗਾਹਕ,1)[0]
            if ਸ਼੍ਰੇਣੀ_ਕੀਮਤ==2:continue
            if ਸ਼੍ਰੇਣੀ_ਕੀਮਤ==3:
                개수=struct.unpack('>I',정확한값(ਗਾਹਕ,7)[3:])[0];정확한값(ਗਾਹਕ,개수);continue
            assert ਸ਼੍ਰੇਣੀ_ਕੀਮਤ==0,ਸ਼੍ਰੇਣੀ_ਕੀਮਤ
            항목수=struct.unpack('>H',정확한값(ਗਾਹਕ,3)[1:])[0]
            for _ in range(항목수):
                x_ਕੌਔਰਡੀਨੇਟ,세로좌표,너비값,높이값,ਵਰਣ_ਸੈਟ=struct.unpack('>HHHHi',정확한값(ਗਾਹਕ,12));assert ਵਰਣ_ਸੈਟ==0,ਵਰਣ_ਸੈਟ
                ਸਮੱਗਰੀ=정확한값(ਗਾਹਕ,너비값*높이값*4)
                for ਕਤਾਰ_ਸਥਿਤੀ_ਬਦਲੋ in range(높이값):
                    for ਕੋਲਮ_ਸਥਿਤੀ_ਬਦਲੋ in range(너비값):
                        원본자료=(ਕਤਾਰ_ਸਥਿਤੀ_ਬਦਲੋ*너비값+ਕੋਲਮ_ਸਥਿਤੀ_ਬਦਲੋ)*4;ਟੀਚਾ=((세로좌표+ਕਤਾਰ_ਸਥਿਤੀ_ਬਦਲੋ)*640+x_ਕੌਔਰਡੀਨੇਟ+ਕੋਲਮ_ਸਥਿਤੀ_ਬਦਲੋ)*3
                        빛삼원색[ਟੀਚਾ:ਟੀਚਾ+3]=bytes((ਸਮੱਗਰੀ[원본자료+2],ਸਮੱਗਰੀ[원본자료+1],ਸਮੱਗਰੀ[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        ਗਾਹਕ=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert 정확한값(ਗਾਹਕ,12)==b'RFB 003.008\n';ਗਾਹਕ.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(ਗਾਹਕ,정확한값(ਗਾਹਕ,1)[0]);ਗਾਹਕ.sendall(b'\x01');assert 정확한값(ਗਾਹਕ,4)==b'\0'*4
        ਗਾਹਕ.sendall(b'\x01');초기값=정확한값(ਗਾਹਕ,24);정확한값(ਗਾਹਕ,struct.unpack('>I',초기값[20:])[0])
        ਗਾਹਕ.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        ਗਾਹਕ.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in ਸ਼ੈਲ('ftpd start')
        ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ=ftplib.FTP();ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.encoding='utf-8';ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.connect('127.0.0.1',파일전송접속번호,timeout=20);ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.login()
        ਪੇਲੋਡ_ਸਮੱਗਰੀ=('GUI와 FTP 동시 사용 '+ਭਾਸ਼ਾ+' 😀\n').encode()
        ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.storbinary('STOR 함께.txt',io.BytesIO(ਪੇਲੋਡ_ਸਮੱਗਰੀ))
        assert ਪੇਲੋਡ_ਸਮੱਗਰੀ.decode().strip() in ਸ਼ੈਲ('cat /함께.txt')
        받은수=bytearray();ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==ਪੇਲੋਡ_ਸਮੱਗਰੀ;ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        ਈਮੇਲ_ਸੂਚੀ=ਸ਼ੈਲ('ls /example')
        assert all(ਨਾਂ in ਈਮੇਲ_ਸੂਚੀ for ਨਾਂ in ('java/','c/','python/','README.md')),ਈਮੇਲ_ਸੂਚੀ
        if ਭਾਸ਼ਾ=='java':
            꾸러미명세=json.loads((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/examples/manifest.json').read_text())
            for ਮਾਰਗ,ਦਾਖਲਾ_ਪੌਇੰਟ in 꾸러미명세.items():
                ਸ਼ੈਲ('cp '+ਮਾਰਗ+' /example-check.bin')
                ਤਤਕਰਾ_ਕੀਮਤ=bytearray();ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.retrbinary('RETR example-check.bin',ਤਤਕਰਾ_ਕੀਮਤ.extend)
                assert len(ਤਤਕਰਾ_ਕੀਮਤ)==ਦਾਖਲਾ_ਪੌਇੰਟ['bytes'] and hashlib.sha256(ਤਤਕਰਾ_ਕੀਮਤ).hexdigest()==ਦਾਖਲਾ_ਪੌਇੰਟ['sha256'],ਮਾਰਗ
            ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            ਜੋੜੇਦਾਰ=bytes(range(256))*64
            ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.storbinary('STOR boundary.bin',io.BytesIO(ਜੋੜੇਦਾਰ))
            ਤਤਕਰਾ_ਕੀਮਤ=bytearray();ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.retrbinary('RETR boundary.bin',ਤਤਕਰਾ_ਕੀਮਤ.extend)
            assert ਤਤਕਰਾ_ਕੀਮਤ==ਜੋੜੇਦਾਰ and 'boundary.bin' in ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.nlst()
            ਸ਼ੈਲ('cp /boundary.bin /boundary-copy.bin')
            ਤਤਕਰਾ_ਕੀਮਤ=bytearray();ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.retrbinary('RETR boundary-copy.bin',ਤਤਕਰਾ_ਕੀਮਤ.extend)
            assert ਤਤਕਰਾ_ਕੀਮਤ==ਜੋੜੇਦਾਰ
            ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.delete('boundary.bin');ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.delete('boundary-copy.bin')
        assert '출력예제' in ਸ਼ੈਲ('ls /example/'+ਭਾਸ਼ਾ)
        ਸ਼ੈਲ('cd /example/'+ਭਾਸ਼ਾ)
        ਨਾਮ_ਤਾਲਿਕਾ={'java':'JAVA','c':'C','python':'PYTHON'}[ਭਾਸ਼ਾ]
        예상파일=ਨਾਮ_ਤਾਲਿਕਾ+' ਫਾਇਲ: 한글 ਸਮੱਗਰੀ 😀\n'
        if ਭਾਸ਼ਾ=='java':
            ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼('javac 출력예제.java','Compiled:');ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼('java 출력예제','JAVA ਆਉਟਪੁੱਟ: 안녕하세요 😀')
            ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼('javac 파일예제.java','Compiled:');ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼('java 파일예제',예상파일)
            ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼('java 네트워크예제 {} {}'.format(되돌림서버항목.ਸੰਚਾਰ_ਰੋਕ_ਤਰੀਕਾ_ਪੋਰਟ,되돌림서버항목.전문접속번호),'JAVA 네트워크 ਤਸਦੀਕ: TCP UDP 한글')
            ਗਰਾਫਿਕਸ_ਆਦੇਸ਼='java 그래픽예제'
        elif ਭਾਸ਼ਾ=='c':
            for ਨਾਂ,전달값,예상결과 in [('ਆਉਟਪੁੱਟ','', 'C ਆਉਟਪੁੱਟ: 안녕하세요 😀'),('ਫਾਇਲ','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 ਤਸਦੀਕ: UDP 한글')]:
                ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼('cc '+ਨਾਂ+'예제.c -o ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼','Compiled native ARM64 ELF:')
                ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼('./ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼'+전달값,예상결과)
            ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼('cc 그래픽예제.c -o ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼','Compiled native ARM64 ELF:');ਗਰਾਫਿਕਸ_ਆਦੇਸ਼='./ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼'
        else:
            for ਨਾਂ,전달값,예상결과 in [('ਆਉਟਪੁੱਟ','','PYTHON ਆਉਟਪੁੱਟ: 안녕하세요 😀'),('ਫਾਇਲ','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 ਤਸਦੀਕ: UDP 한글')]:
                ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼('python '+ਨਾਂ+'예제.py'+전달값,예상결과)
            ਗਰਾਫਿਕਸ_ਆਦੇਸ਼='python 그래픽예제.py'
        ਸੁਰੂ_ਚਿੱਤਰ_ਬਨਾਉਣਾ=ਸੁਰੂ_ਔਫਸੈਟ(ਗਰਾਫਿਕਸ_ਆਦੇਸ਼)
        ਟੈਕਸਟ=수신하기('그림을 확인한 ਪਿਛਲਾ_ਕੀਮਤ Enter를 누르세요.\r\n'.encode(),ਸੁਰੂ_ਚਿੱਤਰ_ਬਨਾਉਣਾ)
        assert ਨਾਮ_ਤਾਲਿਕਾ+' 그래픽: 빨강 초록 파랑' in ਟੈਕਸਟ and 'exit 0' not in ਟੈਕਸਟ,ਟੈਕਸਟ
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            ਔਫਸੈਟ_ਕੀਮਤ=(세로좌표*640+610)*3;assert tuple(빛삼원색[ਔਫਸੈਟ_ਕੀਮਤ:ਔਫਸੈਟ_ਕੀਮਤ+3])==색상,(ਭਾਸ਼ਾ,세로좌표,tuple(빛삼원색[ਔਫਸੈਟ_ਕੀਮਤ:ਔਫਸੈਟ_ਕੀਮਤ+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(ਮਾਪ_ਸਮੱਗਰੀ/(ਭਾਸ਼ਾ+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',ਸੁਰੂ_ਚਿੱਤਰ_ਬਨਾਉਣਾ)
        if ਭਾਸ਼ਾ=='java':
            ਸੁਰੂ_ਵਿੰਡੋ=ਸੁਰੂ_ਔਫਸੈਟ('java 창예제')
            수신하기('GUI 예제 ਤਿਆਰ_ਕਰੋ: 창예제'.encode(),ਸੁਰੂ_ਵਿੰਡੋ)
            def ਕਲਿਕ_ਕਰੋ_ਕੀਮਤ(가로,ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ):
                for ਬਟਨ in (1,0):ਗਾਹਕ.sendall(struct.pack('>BBHH',5,ਬਟਨ,가로,ਲੰਬਵਤ_ਸਥਿਤੀ_ਬਦਲੋ))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            ਕਲਿਕ_ਕਰੋ_ਕੀਮਤ(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for ਵਰਣ_ਕੀਮਤ in '한글':누름값(0x1000000|ord(ਵਰਣ_ਕੀਮਤ));누름값(0x1000000|ord(ਵਰਣ_ਕੀਮਤ),False)
            for 횟수 in (1,2):
                ਚਲਾਓ_2=len(대화기록);ਕਲਿਕ_ਕਰੋ_ਕੀਮਤ(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),ਚਲਾਓ_2)
            time.sleep(.3)
            ਵਿੰਡੋ_ਚਿੱਤਰ_ਬਨਾਉਣਾ=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=ਵਿੰਡੋ_ਚਿੱਤਰ_ਬਨਾਉਣਾ.crop((110,272,530,300)).tobytes()
            ਵਿੰਡੋ_ਚਿੱਤਰ_ਬਨਾਉਣਾ.save(str(ਮਾਪ_ਸਮੱਗਰੀ/'java-swing.png'))
            ਚਲਾਓ_2=len(대화기록);ਕਲਿਕ_ਕਰੋ_ਕੀਮਤ(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',ਚਲਾਓ_2)
        # Download the guest-created bytes through FTP in the same GUI VM.
        ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ_ਨਾਮ={'java':'java.txt','c':'c.txt','python':'python.txt'}[ਭਾਸ਼ਾ]
        ਸ਼ੈਲ('cp '+ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ_ਨਾਮ+' /ਪ੍ਰਮਾਣਿਤ.txt')
        받은수=bytearray();ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.retrbinary('RETR ਪ੍ਰਮਾਣਿਤ.txt',받은수.extend);assert 받은수==예상파일.encode()
        ਸ਼ੈਲ('echo preserved > 출력예제.'+('py' if ਭਾਸ਼ਾ=='python' else ਭਾਸ਼ਾ))
        assert 'EXAMPLES READY' in ਸ਼ੈਲ('example '+ਭਾਸ਼ਾ)
        assert '\npreserved\n' in ਸ਼ੈਲ('cat 출력예제.'+('py' if ਭਾਸ਼ਾ=='python' else ਭਾਸ਼ਾ))
        assert '한/영 ਕੀ_ਕੀਮਤ, Shift+Space 또는 F9' in ਸ਼ੈਲ('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in ਸ਼ੈਲ('echo GUI NETWORK TOGETHER')
        ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.quit();ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ=None;assert 'FTP stopped' in ਸ਼ੈਲ('ftpd stop')
        print('PASS '+ਭਾਸ਼ਾ+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ:
            try:ਲਿਖਤ_ਪੱਤਰ_ਸਥਾਂਨਤਰ_ਸਬੰਧ.close()
            except OSError:pass
        if ਗਾਹਕ:ਗਾਹਕ.close()
        ਪਰੋਸੈੱਸ.terminate()
        try:ਪਰੋਸੈੱਸ.wait(timeout=8)
        except subprocess.TimeoutExpired:ਪਰੋਸੈੱਸ.kill();ਪਰੋਸੈੱਸ.wait()
        ਚੋਣਕਰਤਾ.close();ਪਰੋਸੈੱਸ.stdout.close();(ਮਾਪ_ਸਮੱਗਰੀ/(ਭਾਸ਼ਾ+'-serial.log')).write_bytes(대화기록)


def ਚਲਾਓ_2():
    ਮਾਪ_ਸਮੱਗਰੀ=ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/verification/examples';ਮਾਪ_ਸਮੱਗਰੀ.mkdir(parents=True,exist_ok=True)
    ਮਾਨਤਾ_ਵਿਵਰਨ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for ਭਾਸ਼ਾ in ('java','c','python'):
                test_언어(ਭਾਸ਼ਾ,되돌림서버항목,ਮਾਪ_ਸਮੱਗਰੀ);ਮਾਨਤਾ_ਵਿਵਰਨ['languages'].append(ਭਾਸ਼ਾ)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(ਸ਼੍ਰੇਣੀ_ਕੀਮਤ,ਸਮੱਗਰੀ.encode()) for ਸ਼੍ਰੇਣੀ_ਕੀਮਤ,ਸਮੱਗਰੀ in 예상결과],되돌림서버항목.수신됨
            ਮਾਨਤਾ_ਵਿਵਰਨ['host_network_payloads']=[{'protocol':ਸ਼੍ਰੇਣੀ_ਕੀਮਤ,'text':ਸਮੱਗਰੀ.decode()} for ਸ਼੍ਰੇਣੀ_ਕੀਮਤ,ਸਮੱਗਰੀ in 되돌림서버항목.수신됨]
        ਮਾਨਤਾ_ਵਿਵਰਨ.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(ਮਾਪ_ਸਮੱਗਰੀ/'report.json').write_text(json.dumps(ਮਾਨਤਾ_ਵਿਵਰਨ,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':ਚਲਾਓ_2()
