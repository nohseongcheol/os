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
from 바탕화면 import 정확한값
from 예제되돌림서버 import 되돌림서버
from 실행 import 기준


def test_언어(언어,되돌림서버항목,결과자료):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    실행과정=subprocess.Popen(['python3',str(기준/'도구/실행.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비선택기=selectors.DefaultSelector();준비선택기.register(실행과정.stdout,selectors.EVENT_READ)
    대화기록=bytearray();접속자=None;파일전송접속=None
    def 수신하기(확인표시,Exeque=0):
        끝위치=time.monotonic()+60
        while 확인표시 not in 대화기록[Exeque:]:
            if time.monotonic()>끝위치 or 실행과정.poll() is not None:raise AssertionError(대화기록[Exeque:].decode('utf-8','replace'))
            for 누름값,_ in 준비선택기.select(.1):
                자료=누름값.fileobj.read(65536)
                if 자료:대화기록.extend(자료)
        return 대화기록[Exeque:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(심볼,누르는중=True):접속자.sendall(struct.pack('>BBHI',4,int(누르는중),0,심볼))
    def 시작위치(rango):
        Exeque=len(대화기록)
        for 문자값 in rango+'\n':
            심볼=0xff0d if 문자값=='\n' else ord(문자값) if ord(문자값)<256 else 0x1000000|ord(문자값)
            누름값(심볼);누름값(심볼,False)
        return Exeque
    def 셸(rango):return 수신하기(b'jkoros-native> ',시작위치(rango))
    def 실행(rango,예상결과):
        texto=셸(rango);assert 예상결과 in texto and 'exit 0' in texto,(rango,texto)
        return texto
    def 화소들():
        접속자.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            분류=정확한값(접속자,1)[0]
            if 분류==2:continue
            if 분류==3:
                개수=struct.unpack('>I',정확한값(접속자,7)[3:])[0];정확한값(접속자,개수);continue
            assert 분류==0,분류
            항목수=struct.unpack('>H',정확한값(접속자,3)[1:])[0]
            for _ in range(항목수):
                가로좌표,세로좌표,너비값,높이값,문자부호=struct.unpack('>HHHHi',정확한값(접속자,12));assert 문자부호==0,문자부호
                자료=정확한값(접속자,너비값*높이값*4)
                for 행위치 in range(높이값):
                    for 열위치 in range(너비값):
                        원본자료=(행위치*너비값+열위치)*4;대상=((세로좌표+행위치)*640+가로좌표+열위치)*3
                        빛삼원색[대상:대상+3]=bytes((자료[원본자료+2],자료[원본자료+1],자료[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        접속자=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert 정확한값(접속자,12)==b'RFB 003.008\n';접속자.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(접속자,정확한값(접속자,1)[0]);접속자.sendall(b'\x01');assert 정확한값(접속자,4)==b'\0'*4
        접속자.sendall(b'\x01');초기값=정확한값(접속자,24);정확한값(접속자,struct.unpack('>I',초기값[20:])[0])
        접속자.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        접속자.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in 셸('ftpd start')
        파일전송접속=ftplib.FTP();파일전송접속.encoding='utf-8';파일전송접속.connect('127.0.0.1',파일전송접속번호,timeout=20);파일전송접속.login()
        내용자료=('GUI와 FTP 동시 사용 '+언어+' 😀\n').encode()
        파일전송접속.storbinary('STOR 함께.txt',io.BytesIO(내용자료))
        assert 내용자료.decode().strip() in 셸('cat /함께.txt')
        받은수=bytearray();파일전송접속.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==내용자료;파일전송접속.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        목록보내기=셸('ls /example')
        assert all(Nomine in 목록보내기 for Nomine in ('java/','c/','python/','README.md')),목록보내기
        if 언어=='java':
            꾸러미명세=json.loads((기준/'build/examples/manifest.json').read_text())
            for Percurso,진입점 in 꾸러미명세.items():
                셸('cp '+Percurso+' /example-check.bin')
                내용=bytearray();파일전송접속.retrbinary('RETR example-check.bin',내용.extend)
                assert len(내용)==진입점['bytes'] and hashlib.sha256(내용).hexdigest()==진입점['sha256'],Percurso
            파일전송접속.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            실행바이너리=bytes(range(256))*64
            파일전송접속.storbinary('STOR boundary.bin',io.BytesIO(실행바이너리))
            내용=bytearray();파일전송접속.retrbinary('RETR boundary.bin',내용.extend)
            assert 내용==실행바이너리 and 'boundary.bin' in 파일전송접속.nlst()
            셸('cp /boundary.bin /boundary-copy.bin')
            내용=bytearray();파일전송접속.retrbinary('RETR boundary-copy.bin',내용.extend)
            assert 내용==실행바이너리
            파일전송접속.delete('boundary.bin');파일전송접속.delete('boundary-copy.bin')
        assert '출력예제' in 셸('ls /example/'+언어)
        셸('cd /example/'+언어)
        이름표={'java':'JAVA','c':'C','python':'PYTHON'}[언어]
        예상파일=이름표+' 파일: 한글 자료 😀\n'
        if 언어=='java':
            실행('javac 출력예제.java','Compiled:');실행('java 출력예제','JAVA Exito: 안녕하세요 😀')
            실행('javac 파일예제.java','Compiled:');실행('java 파일예제',예상파일)
            실행('java 네트워크예제 {} {}'.format(되돌림서버항목.연결접속번호,되돌림서버항목.전문접속번호),'JAVA 네트워크 확인: TCP UDP 한글')
            그림명령='java 그래픽예제'
        elif 언어=='c':
            for Nomine,전달값,예상결과 in [('Exito','', 'C Exito: 안녕하세요 😀'),('파일','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 확인: UDP 한글')]:
                실행('cc '+Nomine+'예제.c -o 실행','Compiled native ARM64 ELF:')
                실행('./실행'+전달값,예상결과)
            실행('cc 그래픽예제.c -o 실행','Compiled native ARM64 ELF:');그림명령='./실행'
        else:
            for Nomine,전달값,예상결과 in [('Exito','','PYTHON Exito: 안녕하세요 😀'),('파일','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 확인: UDP 한글')]:
                실행('python '+Nomine+'예제.py'+전달값,예상결과)
            그림명령='python 그래픽예제.py'
        그림시작=시작위치(그림명령)
        texto=수신하기('그림을 확인한 뒤 Enter를 누르세요.\r\n'.encode(),그림시작)
        assert 이름표+' 그래픽: 빨강 초록 파랑' in texto and 'exit 0' not in texto,texto
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        파일전송접속.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();파일전송접속.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';파일전송접속.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            변위=(세로좌표*640+610)*3;assert tuple(빛삼원색[변위:변위+3])==색상,(언어,세로좌표,tuple(빛삼원색[변위:변위+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(결과자료/(언어+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',그림시작)
        if 언어=='java':
            창시작=시작위치('java 창예제')
            수신하기('GUI 예제 준비: 창예제'.encode(),창시작)
            def 클릭(가로,세로):
                for 단추 in (1,0):접속자.sendall(struct.pack('>BBHH',5,단추,가로,세로))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            클릭(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for 글자 in '한글':누름값(0x1000000|ord(글자));누름값(0x1000000|ord(글자),False)
            for 횟수 in (1,2):
                Exeque=len(대화기록);클릭(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Exeque)
            time.sleep(.3)
            창그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=창그림.crop((110,272,530,300)).tobytes()
            창그림.save(str(결과자료/'java-swing.png'))
            Exeque=len(대화기록);클릭(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',Exeque)
        # Download the guest-created bytes through FTP in the same GUI VM.
        파일이름={'java':'java.txt','c':'c.txt','python':'python.txt'}[언어]
        셸('cp '+파일이름+' /검증.txt')
        받은수=bytearray();파일전송접속.retrbinary('RETR 검증.txt',받은수.extend);assert 받은수==예상파일.encode()
        셸('echo preserved > 출력예제.'+('py' if 언어=='python' else 언어))
        assert 'EXAMPLES READY' in 셸('example '+언어)
        assert '\npreserved\n' in 셸('cat 출력예제.'+('py' if 언어=='python' else 언어))
        assert '한/영 키, Shift+Space 또는 F9' in 셸('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in 셸('echo GUI NETWORK TOGETHER')
        파일전송접속.quit();파일전송접속=None;assert 'FTP stopped' in 셸('ftpd stop')
        print('PASS '+언어+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if 파일전송접속:
            try:파일전송접속.close()
            except OSError:pass
        if 접속자:접속자.close()
        실행과정.terminate()
        try:실행과정.wait(timeout=8)
        except subprocess.TimeoutExpired:실행과정.kill();실행과정.wait()
        준비선택기.close();실행과정.stdout.close();(결과자료/(언어+'-serial.log')).write_bytes(대화기록)


def Exeque():
    결과자료=기준/'build/verification/examples';결과자료.mkdir(parents=True,exist_ok=True)
    검증기록={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for 언어 in ('java','c','python'):
                test_언어(언어,되돌림서버항목,결과자료);검증기록['languages'].append(언어)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(분류,자료.encode()) for 분류,자료 in 예상결과],되돌림서버항목.수신됨
            검증기록['host_network_payloads']=[{'protocol':분류,'text':자료.decode()} for 분류,자료 in 되돌림서버항목.수신됨]
        검증기록.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(결과자료/'report.json').write_text(json.dumps(검증기록,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Exeque()
