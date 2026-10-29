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
from радна_површина_поглед import 정확한값
from 예제되돌림서버 import 되돌림서버
from 실행 import 기준


def test_언어(Језик,되돌림서버항목,결과자료):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    процес=subprocess.Popen(['python3',str(기준/'도구/실행.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비선택기=selectors.DefaultSelector();준비선택기.register(процес.stdout,selectors.EVENT_READ)
    대화기록=bytearray();клијент=None;фајл_пријенос_веза=None
    def 수신하기(확인표시,시작=0):
        끝위치=time.monotonic()+60
        while 확인표시 not in 대화기록[시작:]:
            if time.monotonic()>끝위치 or процес.poll() is not None:raise AssertionError(대화기록[시작:].decode('utf-8','replace'))
            for 누름값,_ in 준비선택기.select(.1):
                подаци=누름값.fileobj.read(65536)
                if подаци:대화기록.extend(подаци)
        return 대화기록[시작:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(심볼,누르는중=True):клијент.sendall(struct.pack('>BBHI',4,int(누르는중),0,심볼))
    def 시작위치(редак):
        시작=len(대화기록)
        for кôд_знака in редак+'\n':
            심볼=0xff0d if кôд_знака=='\n' else ord(кôд_знака) if ord(кôд_знака)<256 else 0x1000000|ord(кôд_знака)
            누름값(심볼);누름값(심볼,False)
        return 시작
    def љуска(редак):return 수신하기(b'jkoros-native> ',시작위치(редак))
    def 실행(редак,예상결과):
        текст=љуска(редак);assert 예상결과 in текст and 'exit 0' in текст,(редак,текст)
        return текст
    def 화소들():
        клијент.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            категорија_вриједност=정확한값(клијент,1)[0]
            if категорија_вриједност==2:continue
            if категорија_вриједност==3:
                개수=struct.unpack('>I',정확한값(клијент,7)[3:])[0];정확한값(клијент,개수);continue
            assert категорија_вриједност==0,категорија_вриједност
            항목수=struct.unpack('>H',정확한값(клијент,3)[1:])[0]
            for _ in range(항목수):
                가로좌표,세로좌표,너비값,높이값,скуп_знакова=struct.unpack('>HHHHi',정확한값(клијент,12));assert скуп_знакова==0,скуп_знакова
                подаци=정확한값(клијент,너비값*높이값*4)
                for 행위치 in range(높이값):
                    for 열위치 in range(너비값):
                        원본자료=(행위치*너비값+열위치)*4;циљ=((세로좌표+행위치)*640+가로좌표+열위치)*3
                        빛삼원색[циљ:циљ+3]=bytes((подаци[원본자료+2],подаци[원본자료+1],подаци[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        клијент=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert 정확한값(клијент,12)==b'RFB 003.008\n';клијент.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(клијент,정확한값(клијент,1)[0]);клијент.sendall(b'\x01');assert 정확한값(клијент,4)==b'\0'*4
        клијент.sendall(b'\x01');초기값=정확한값(клијент,24);정확한값(клијент,struct.unpack('>I',초기값[20:])[0])
        клијент.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        клијент.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in љуска('ftpd start')
        фајл_пријенос_веза=ftplib.FTP();фајл_пријенос_веза.encoding='utf-8';фајл_пријенос_веза.connect('127.0.0.1',파일전송접속번호,timeout=20);фајл_пријенос_веза.login()
        корисни_садржај_подаци=('GUI와 FTP 동시 사용 '+Језик+' 😀\n').encode()
        фајл_пријенос_веза.storbinary('STOR 함께.txt',io.BytesIO(корисни_садржај_подаци))
        assert корисни_садржај_подаци.decode().strip() in љуска('cat /함께.txt')
        받은수=bytearray();фајл_пријенос_веза.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==корисни_садржај_подаци;фајл_пријенос_веза.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        послати_списак=љуска('ls /example')
        assert all(назив in послати_списак for назив in ('java/','c/','python/','README.md')),послати_списак
        if Језик=='java':
            꾸러미명세=json.loads((기준/'build/examples/manifest.json').read_text())
            for пут,унос_тачка in 꾸러미명세.items():
                љуска('cp '+пут+' /example-check.bin')
                Садржај_вриједност=bytearray();фајл_пријенос_веза.retrbinary('RETR example-check.bin',Садржај_вриједност.extend)
                assert len(Садржај_вриједност)==унос_тачка['bytes'] and hashlib.sha256(Садржај_вриједност).hexdigest()==унос_тачка['sha256'],пут
            фајл_пријенос_веза.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            бинарно=bytes(range(256))*64
            фајл_пријенос_веза.storbinary('STOR boundary.bin',io.BytesIO(бинарно))
            Садржај_вриједност=bytearray();фајл_пријенос_веза.retrbinary('RETR boundary.bin',Садржај_вриједност.extend)
            assert Садржај_вриједност==бинарно and 'boundary.bin' in фајл_пријенос_веза.nlst()
            љуска('cp /boundary.bin /boundary-copy.bin')
            Садржај_вриједност=bytearray();фајл_пријенос_веза.retrbinary('RETR boundary-copy.bin',Садржај_вриједност.extend)
            assert Садржај_вриједност==бинарно
            фајл_пријенос_веза.delete('boundary.bin');фајл_пријенос_веза.delete('boundary-copy.bin')
        assert '출력예제' in љуска('ls /example/'+Језик)
        љуска('cd /example/'+Језик)
        назив_табела={'java':'JAVA','c':'C','python':'PYTHON'}[Језик]
        예상파일=назив_табела+' фајл: 한글 подаци 😀\n'
        if Језик=='java':
            실행('javac 출력예제.java','Compiled:');실행('java 출력예제','JAVA 출력: 안녕하세요 😀')
            실행('javac 파일예제.java','Compiled:');실행('java 파일예제',예상파일)
            실행('java 네트워크예제 {} {}'.format(되돌림서버항목.TCP_порт,되돌림서버항목.전문접속번호),'JAVA 네트워크 потврдити: TCP UDP 한글')
            그림명령='java 그래픽예제'
        elif Језик=='c':
            for назив,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('фајл','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 потврдити: UDP 한글')]:
                실행('cc '+назив+'예제.c -o 실행','Compiled native ARM64 ELF:')
                실행('./실행'+전달값,예상결과)
            실행('cc 그래픽예제.c -o 실행','Compiled native ARM64 ELF:');그림명령='./실행'
        else:
            for назив,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('фајл','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 потврдити: UDP 한글')]:
                실행('python '+назив+'예제.py'+전달값,예상결과)
            그림명령='python 그래픽예제.py'
        почети_уцртавање=시작위치(그림명령)
        текст=수신하기('그림을 확인한 Назад_вриједност Enter를 누르세요.\r\n'.encode(),почети_уцртавање)
        assert назив_табела+' 그래픽: 빨강 초록 파랑' in текст and 'exit 0' not in текст,текст
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        фајл_пријенос_веза.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();фајл_пријенос_веза.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';фајл_пријенос_веза.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            변위=(세로좌표*640+610)*3;assert tuple(빛삼원색[변위:변위+3])==색상,(Језик,세로좌표,tuple(빛삼원색[변위:변위+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(결과자료/(Језик+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',почети_уцртавање)
        if Језик=='java':
            почети_прозор=시작위치('java 창예제')
            수신하기('GUI 예제 Припремити: 창예제'.encode(),почети_прозор)
            def кликнути_вриједност(가로,세로):
                for дугме in (1,0):клијент.sendall(struct.pack('>BBHH',5,дугме,가로,세로))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            кликнути_вриједност(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for знак_вриједност in '한글':누름값(0x1000000|ord(знак_вриједност));누름값(0x1000000|ord(знак_вриједност),False)
            for 횟수 in (1,2):
                시작=len(대화기록);кликнути_вриједност(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),시작)
            time.sleep(.3)
            прозор_уцртавање=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=прозор_уцртавање.crop((110,272,530,300)).tobytes()
            прозор_уцртавање.save(str(결과자료/'java-swing.png'))
            시작=len(대화기록);кликнути_вриједност(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',시작)
        # Download the guest-created bytes through FTP in the same GUI VM.
        фајл_унос_назив={'java':'java.txt','c':'c.txt','python':'python.txt'}[Језик]
        љуска('cp '+фајл_унос_назив+' /овјерити.txt')
        받은수=bytearray();фајл_пријенос_веза.retrbinary('RETR овјерити.txt',받은수.extend);assert 받은수==예상파일.encode()
        љуска('echo preserved > 출력예제.'+('py' if Језик=='python' else Језик))
        assert 'EXAMPLES READY' in љуска('example '+Језик)
        assert '\npreserved\n' in љуска('cat 출력예제.'+('py' if Језик=='python' else Језик))
        assert '한/영 кључ_вриједност, Shift+Space 또는 F9' in љуска('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in љуска('echo GUI NETWORK TOGETHER')
        фајл_пријенос_веза.quit();фајл_пријенос_веза=None;assert 'FTP stopped' in љуска('ftpd stop')
        print('PASS '+Језик+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if фајл_пријенос_веза:
            try:фајл_пријенос_веза.close()
            except OSError:pass
        if клијент:клијент.close()
        процес.terminate()
        try:процес.wait(timeout=8)
        except subprocess.TimeoutExpired:процес.kill();процес.wait()
        준비선택기.close();процес.stdout.close();(결과자료/(Језик+'-serial.log')).write_bytes(대화기록)


def 시작():
    결과자료=기준/'build/verification/examples';결과자료.mkdir(parents=True,exist_ok=True)
    провјера_извјештај={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for Језик in ('java','c','python'):
                test_언어(Језик,되돌림서버항목,결과자료);провјера_извјештај['languages'].append(Језик)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(категорија_вриједност,подаци.encode()) for категорија_вриједност,подаци in 예상결과],되돌림서버항목.수신됨
            провјера_извјештај['host_network_payloads']=[{'protocol':категорија_вриједност,'text':подаци.decode()} for категорија_вриједност,подаци in 되돌림서버항목.수신됨]
        провјера_извјештај.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(결과자료/'report.json').write_text(json.dumps(провјера_извјештај,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':시작()
