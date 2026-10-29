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
from ເດັສທັອບ_ເບິ່ງ import 정확한값
from 예제되돌림서버 import 되돌림서버
from ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ import ໂຄງ_ການ_ເລກຮາກ


def test_언어(ພາ_ສາ,되돌림서버항목,ມາດຕະການ_ຂໍ້ມູນ):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));ຟາຍ_ໂອນ_ຫມາຍເລກພອດ=임시자원.getsockname()[1]
    ຂະ_ບວນ_ການ=subprocess.Popen(['python3',str(ໂຄງ_ການ_ເລກຮາກ/'ເຄື່ອງມື/ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.py'),'--desktop','--network','--port','0','--ftp-port',str(ຟາຍ_ໂອນ_ຫມາຍເລກພອດ)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    ຕົວ_ໃຊ້_ເລືອກ=selectors.DefaultSelector();ຕົວ_ໃຊ້_ເລືອກ.register(ຂະ_ບວນ_ການ.stdout,selectors.EVENT_READ)
    대화기록=bytearray();ລູກຂ່າຍ=None;ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່=None
    def 수신하기(확인표시,ແລ່ນ=0):
        ຈົບ_ອອບເຊັດ=time.monotonic()+60
        while 확인표시 not in 대화기록[ແລ່ນ:]:
            if time.monotonic()>ຈົບ_ອອບເຊັດ or ຂະ_ບວນ_ການ.poll() is not None:raise AssertionError(대화기록[ແລ່ນ:].decode('utf-8','replace'))
            for 누름값,_ in ຕົວ_ໃຊ້_ເລືອກ.select(.1):
                ຂໍ້ມູນ=누름값.fileobj.read(65536)
                if ຂໍ້ມູນ:대화기록.extend(ຂໍ້ມູນ)
        return 대화기록[ແລ່ນ:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(ສັນຍາລັກ_ຄ່າ,누르는중=True):ລູກຂ່າຍ.sendall(struct.pack('>BBHI',4,int(누르는중),0,ສັນຍາລັກ_ຄ່າ))
    def ເລີ່ມ_ອອບເຊັດ(ສາຍ):
        ແລ່ນ=len(대화기록)
        for ຈຸດ_ລະ_ຫັດ in ສາຍ+'\n':
            ສັນຍາລັກ_ຄ່າ=0xff0d if ຈຸດ_ລະ_ຫັດ=='\n' else ord(ຈຸດ_ລະ_ຫັດ) if ord(ຈຸດ_ລະ_ຫັດ)<256 else 0x1000000|ord(ຈຸດ_ລະ_ຫັດ)
            누름값(ສັນຍາລັກ_ຄ່າ);누름값(ສັນຍາລັກ_ຄ່າ,False)
        return ແລ່ນ
    def ເຊລ(ສາຍ):return 수신하기(b'jkoros-native> ',ເລີ່ມ_ອອບເຊັດ(ສາຍ))
    def ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ(ສາຍ,예상결과):
        ຂໍ້ຄວາມ=ເຊລ(ສາຍ);assert 예상결과 in ຂໍ້ຄວາມ and 'exit 0' in ຂໍ້ຄວາມ,(ສາຍ,ຂໍ້ຄວາມ)
        return ຂໍ້ຄວາມ
    def 화소들():
        ລູກຂ່າຍ.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            ຫມວດ_ຄ່າ=정확한값(ລູກຂ່າຍ,1)[0]
            if ຫມວດ_ຄ່າ==2:continue
            if ຫມວດ_ຄ່າ==3:
                개수=struct.unpack('>I',정확한값(ລູກຂ່າຍ,7)[3:])[0];정확한값(ລູກຂ່າຍ,개수);continue
            assert ຫມວດ_ຄ່າ==0,ຫມວດ_ຄ່າ
            항목수=struct.unpack('>H',정확한값(ລູກຂ່າຍ,3)[1:])[0]
            for _ in range(항목수):
                ຈຸດ_ພິ_ກັດ_x,ປຸ່ມ_Y_ຈຸດປະສານ,너비값,높이값,ຊຸດ_ຕົວ_ອັກ_ສອນ=struct.unpack('>HHHHi',정확한값(ລູກຂ່າຍ,12));assert ຊຸດ_ຕົວ_ອັກ_ສອນ==0,ຊຸດ_ຕົວ_ອັກ_ສອນ
                ຂໍ້ມູນ=정확한값(ລູກຂ່າຍ,너비값*높이값*4)
                for ແຖວ_ຈັດຕໍາແຫນ່ງ in range(높이값):
                    for ຖັນ_ຈັດຕໍາແຫນ່ງ in range(너비값):
                        원본자료=(ແຖວ_ຈັດຕໍາແຫນ່ງ*너비값+ຖັນ_ຈັດຕໍາແຫນ່ງ)*4;ເປົ້າ_ຫມາຍ=((ປຸ່ມ_Y_ຈຸດປະສານ+ແຖວ_ຈັດຕໍາແຫນ່ງ)*640+ຈຸດ_ພິ_ກັດ_x+ຖັນ_ຈັດຕໍາແຫນ່ງ)*3
                        빛삼원색[ເປົ້າ_ຫມາຍ:ເປົ້າ_ຫມາຍ+3]=bytes((ຂໍ້ມູນ[원본자료+2],ຂໍ້ມູນ[원본자료+1],ຂໍ້ມູນ[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        ຫມາຍເລກພອດ=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        ລູກຂ່າຍ=socket.create_connection(('127.0.0.1',ຫມາຍເລກພອດ),timeout=10)
        assert 정확한값(ລູກຂ່າຍ,12)==b'RFB 003.008\n';ລູກຂ່າຍ.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(ລູກຂ່າຍ,정확한값(ລູກຂ່າຍ,1)[0]);ລູກຂ່າຍ.sendall(b'\x01');assert 정확한값(ລູກຂ່າຍ,4)==b'\0'*4
        ລູກຂ່າຍ.sendall(b'\x01');초기값=정확한값(ລູກຂ່າຍ,24);정확한값(ລູກຂ່າຍ,struct.unpack('>I',초기값[20:])[0])
        ລູກຂ່າຍ.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        ລູກຂ່າຍ.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in ເຊລ('ftpd start')
        ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່=ftplib.FTP();ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.encoding='utf-8';ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.connect('127.0.0.1',ຟາຍ_ໂອນ_ຫມາຍເລກພອດ,timeout=20);ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.login()
        ນ້ໍາຫນັກບັນທຸກ_ຂໍ້ມູນ=('GUI와 FTP 동시 사용 '+ພາ_ສາ+' 😀\n').encode()
        ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.storbinary('STOR 함께.txt',io.BytesIO(ນ້ໍາຫນັກບັນທຸກ_ຂໍ້ມູນ))
        assert ນ້ໍາຫນັກບັນທຸກ_ຂໍ້ມູນ.decode().strip() in ເຊລ('cat /함께.txt')
        받은수=bytearray();ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==ນ້ໍາຫນັກບັນທຸກ_ຂໍ້ມູນ;ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        ສົ່ງ_ລາຍຊື່=ເຊລ('ls /example')
        assert all(ຊື່ in ສົ່ງ_ລາຍຊື່ for ຊື່ in ('java/','c/','python/','README.md')),ສົ່ງ_ລາຍຊື່
        if ພາ_ສາ=='java':
            꾸러미명세=json.loads((ໂຄງ_ການ_ເລກຮາກ/'build/examples/manifest.json').read_text())
            for ທາງໂຄຈອນ,ເຂົ້າໃນ_ຈຸດ in 꾸러미명세.items():
                ເຊລ('cp '+ທາງໂຄຈອນ+' /example-check.bin')
                ເນື້ອໃນ_ຄ່າ_cb0f2404=bytearray();ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.retrbinary('RETR example-check.bin',ເນື້ອໃນ_ຄ່າ_cb0f2404.extend)
                assert len(ເນື້ອໃນ_ຄ່າ_cb0f2404)==ເຂົ້າໃນ_ຈຸດ['bytes'] and hashlib.sha256(ເນື້ອໃນ_ຄ່າ_cb0f2404).hexdigest()==ເຂົ້າໃນ_ຈຸດ['sha256'],ທາງໂຄຈອນ
            ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            ຖານ_ສອງ=bytes(range(256))*64
            ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.storbinary('STOR boundary.bin',io.BytesIO(ຖານ_ສອງ))
            ເນື້ອໃນ_ຄ່າ_cb0f2404=bytearray();ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.retrbinary('RETR boundary.bin',ເນື້ອໃນ_ຄ່າ_cb0f2404.extend)
            assert ເນື້ອໃນ_ຄ່າ_cb0f2404==ຖານ_ສອງ and 'boundary.bin' in ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.nlst()
            ເຊລ('cp /boundary.bin /boundary-copy.bin')
            ເນື້ອໃນ_ຄ່າ_cb0f2404=bytearray();ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.retrbinary('RETR boundary-copy.bin',ເນື້ອໃນ_ຄ່າ_cb0f2404.extend)
            assert ເນື້ອໃນ_ຄ່າ_cb0f2404==ຖານ_ສອງ
            ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.delete('boundary.bin');ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.delete('boundary-copy.bin')
        assert '출력예제' in ເຊລ('ls /example/'+ພາ_ສາ)
        ເຊລ('cd /example/'+ພາ_ສາ)
        ຊື່_ຕາຕະລາງ={'java':'JAVA','c':'C','python':'PYTHON'}[ພາ_ສາ]
        예상파일=ຊື່_ຕາຕະລາງ+' ຟາຍ: 한글 ຂໍ້ມູນ 😀\n'
        if ພາ_ສາ=='java':
            ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ('javac 출력예제.java','Compiled:');ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ('java 출력예제','JAVA 출력: 안녕하세요 😀')
            ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ('javac 파일예제.java','Compiled:');ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ('java 파일예제',예상파일)
            ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ('java 네트워크예제 {} {}'.format(되돌림서버항목.ທີຊີພີ_ຜອດ,되돌림서버항목.ຢູດີພີ_ຜອດ),'JAVA 네트워크 확인: TCP UDP 한글')
            ກຣາບຟິກ_ຄໍາສັ່ງ='java 그래픽예제'
        elif ພາ_ສາ=='c':
            for ຊື່,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('ຟາຍ','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.ຢູດີພີ_ຜອດ),'C 네트워크 확인: UDP 한글')]:
                ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ('cc '+ຊື່+'예제.c -o ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ','Compiled native ARM64 ELF:')
                ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ('./ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ'+전달값,예상결과)
            ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ('cc 그래픽예제.c -o ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ','Compiled native ARM64 ELF:');ກຣາບຟິກ_ຄໍາສັ່ງ='./ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ'
        else:
            for ຊື່,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('ຟາຍ','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.ຢູດີພີ_ຜອດ),'PYTHON 네트워크 확인: UDP 한글')]:
                ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ('python '+ຊື່+'예제.py'+전달값,예상결과)
            ກຣາບຟິກ_ຄໍາສັ່ງ='python 그래픽예제.py'
        ເລີ່ມ_ການ_ແຕ້ມ=ເລີ່ມ_ອອບເຊັດ(ກຣາບຟິກ_ຄໍາສັ່ງ)
        ຂໍ້ຄວາມ=수신하기('그림을 확인한 ກັບ_ຄືນ_ຄ່າ Enter를 누르세요.\r\n'.encode(),ເລີ່ມ_ການ_ແຕ້ມ)
        assert ຊື່_ຕາຕະລາງ+' 그래픽: 빨강 초록 파랑' in ຂໍ້ຄວາມ and 'exit 0' not in ຂໍ້ຄວາມ,ຂໍ້ຄວາມ
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.delete('도중.txt')
        빛삼원색=화소들()
        for ປຸ່ມ_Y_ຈຸດປະສານ,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            ອອບເຊັດ_ຄ່າ=(ປຸ່ມ_Y_ຈຸດປະສານ*640+610)*3;assert tuple(빛삼원색[ອອບເຊັດ_ຄ່າ:ອອບເຊັດ_ຄ່າ+3])==색상,(ພາ_ສາ,ປຸ່ມ_Y_ຈຸດປະສານ,tuple(빛삼원색[ອອບເຊັດ_ຄ່າ:ອອບເຊັດ_ຄ່າ+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(ມາດຕະການ_ຂໍ້ມູນ/(ພາ_ສາ+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',ເລີ່ມ_ການ_ແຕ້ມ)
        if ພາ_ສາ=='java':
            ເລີ່ມ_ວິນໂດ=ເລີ່ມ_ອອບເຊັດ('java 창예제')
            수신하기('GUI 예제 ກະ_ກຽມ: 창예제'.encode(),ເລີ່ມ_ວິນໂດ)
            def ກົດ_ຄ່າ(가로,ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ):
                for ປຸ່ມ in (1,0):ລູກຂ່າຍ.sendall(struct.pack('>BBHH',5,ປຸ່ມ,가로,ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            ກົດ_ຄ່າ(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for ຕົວອັກສອນ_ຄ່າ in '한글':누름값(0x1000000|ord(ຕົວອັກສອນ_ຄ່າ));누름값(0x1000000|ord(ຕົວອັກສອນ_ຄ່າ),False)
            for 횟수 in (1,2):
                ແລ່ນ=len(대화기록);ກົດ_ຄ່າ(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),ແລ່ນ)
            time.sleep(.3)
            ວິນໂດ_ການ_ແຕ້ມ=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=ວິນໂດ_ການ_ແຕ້ມ.crop((110,272,530,300)).tobytes()
            ວິນໂດ_ການ_ແຕ້ມ.save(str(ມາດຕະການ_ຂໍ້ມູນ/'java-swing.png'))
            ແລ່ນ=len(대화기록);ກົດ_ຄ່າ(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',ແລ່ນ)
        # Download the guest-created bytes through FTP in the same GUI VM.
        ຟາຍ_ເຂົ້າໃນ_ຊື່={'java':'java.txt','c':'c.txt','python':'python.txt'}[ພາ_ສາ]
        ເຊລ('cp '+ຟາຍ_ເຂົ້າໃນ_ຊື່+' /ຮັບ_ຮອງ.txt')
        받은수=bytearray();ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.retrbinary('RETR ຮັບ_ຮອງ.txt',받은수.extend);assert 받은수==예상파일.encode()
        ເຊລ('echo preserved > 출력예제.'+('py' if ພາ_ສາ=='python' else ພາ_ສາ))
        assert 'EXAMPLES READY' in ເຊລ('example '+ພາ_ສາ)
        assert '\npreserved\n' in ເຊລ('cat 출력예제.'+('py' if ພາ_ສາ=='python' else ພາ_ສາ))
        assert '한/영 ກະແຈ_ຄ່າ, Shift+Space 또는 F9' in ເຊລ('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in ເຊລ('echo GUI NETWORK TOGETHER')
        ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.quit();ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່=None;assert 'FTP stopped' in ເຊລ('ftpd stop')
        print('PASS '+ພາ_ສາ+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່:
            try:ຟາຍ_ໂອນ_ການເຊື່ອມຕໍ່.close()
            except OSError:pass
        if ລູກຂ່າຍ:ລູກຂ່າຍ.close()
        ຂະ_ບວນ_ການ.terminate()
        try:ຂະ_ບວນ_ການ.wait(timeout=8)
        except subprocess.TimeoutExpired:ຂະ_ບວນ_ການ.kill();ຂະ_ບວນ_ການ.wait()
        ຕົວ_ໃຊ້_ເລືອກ.close();ຂະ_ບວນ_ການ.stdout.close();(ມາດຕະການ_ຂໍ້ມູນ/(ພາ_ສາ+'-serial.log')).write_bytes(대화기록)


def ແລ່ນ():
    ມາດຕະການ_ຂໍ້ມູນ=ໂຄງ_ການ_ເລກຮາກ/'build/verification/examples';ມາດຕະການ_ຂໍ້ມູນ.mkdir(parents=True,exist_ok=True)
    ໃຊ້ໄດ້_ລາຍງານ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ໂຄງ_ການ_ເລກຮາກ/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for ພາ_ສາ in ('java','c','python'):
                test_언어(ພາ_ສາ,되돌림서버항목,ມາດຕະການ_ຂໍ້ມູນ);ໃຊ້ໄດ້_ລາຍງານ['languages'].append(ພາ_ສາ)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(ຫມວດ_ຄ່າ,ຂໍ້ມູນ.encode()) for ຫມວດ_ຄ່າ,ຂໍ້ມູນ in 예상결과],되돌림서버항목.수신됨
            ໃຊ້ໄດ້_ລາຍງານ['host_network_payloads']=[{'protocol':ຫມວດ_ຄ່າ,'text':ຂໍ້ມູນ.decode()} for ຫມວດ_ຄ່າ,ຂໍ້ມູນ in 되돌림서버항목.수신됨]
        ໃຊ້ໄດ້_ລາຍງານ.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(ມາດຕະການ_ຂໍ້ມູນ/'report.json').write_text(json.dumps(ໃຊ້ໄດ້_ລາຍງານ,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':ແລ່ນ()
