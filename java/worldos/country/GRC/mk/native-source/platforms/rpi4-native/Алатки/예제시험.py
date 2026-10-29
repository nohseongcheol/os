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
from десктоп_Приказ import EXACT_VALUE
from 예제되돌림서버 import 되돌림서버
from Изврши_наредба import Project_корен


def test_언어(јазик,되돌림서버항목,мерка_податоци):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));датотека_пренос_број_на_порта=임시자원.getsockname()[1]
    Процес=subprocess.Popen(['python3',str(Project_корен/'Алатки/Изврши_наредба.py'),'--desktop','--network','--port','0','--ftp-port',str(датотека_пренос_број_на_порта)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    избирач=selectors.DefaultSelector();избирач.register(Процес.stdout,selectors.EVENT_READ)
    대화기록=bytearray();клиент=None;датотека_пренос_врска=None
    def 수신하기(확인표시,Изврши_2=0):
        крај_OFFSET=time.monotonic()+60
        while 확인표시 not in 대화기록[Изврши_2:]:
            if time.monotonic()>крај_OFFSET or Процес.poll() is not None:raise AssertionError(대화기록[Изврши_2:].decode('utf-8','replace'))
            for 누름값,_ in избирач.select(.1):
                податоци=누름값.fileobj.read(65536)
                if податоци:대화기록.extend(податоци)
        return 대화기록[Изврши_2:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(симбол_VALUE,누르는중=True):клиент.sendall(struct.pack('>BBHI',4,int(누르는중),0,симбол_VALUE))
    def Start_OFFSET(ред):
        Изврши_2=len(대화기록)
        for кодна_точка in ред+'\n':
            симбол_VALUE=0xff0d if кодна_точка=='\n' else ord(кодна_точка) if ord(кодна_точка)<256 else 0x1000000|ord(кодна_точка)
            누름값(симбол_VALUE);누름값(симбол_VALUE,False)
        return Изврши_2
    def обвивка(ред):return 수신하기(b'jkoros-native> ',Start_OFFSET(ред))
    def Изврши_наредба(ред,예상결과):
        Текст=обвивка(ред);assert 예상결과 in Текст and 'exit 0' in Текст,(ред,Текст)
        return Текст
    def 화소들():
        клиент.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            област_VALUE=EXACT_VALUE(клиент,1)[0]
            if област_VALUE==2:continue
            if област_VALUE==3:
                ставка_COUNT=struct.unpack('>I',EXACT_VALUE(клиент,7)[3:])[0];EXACT_VALUE(клиент,ставка_COUNT);continue
            assert област_VALUE==0,област_VALUE
            внес_COUNT=struct.unpack('>H',EXACT_VALUE(клиент,3)[1:])[0]
            for _ in range(внес_COUNT):
                координата_х,세로좌표,너비값,높이값,збир_знаци=struct.unpack('>HHHHi',EXACT_VALUE(клиент,12));assert збир_знаци==0,збир_знаци
                податоци=EXACT_VALUE(клиент,너비값*높이값*4)
                for ROW_позиционирање in range(높이값):
                    for COLUMN_позиционирање in range(너비값):
                        원본자료=(ROW_позиционирање*너비값+COLUMN_позиционирање)*4;цел=((세로좌표+ROW_позиционирање)*640+координата_х+COLUMN_позиционирање)*3
                        빛삼원색[цел:цел+3]=bytes((податоци[원본자료+2],податоци[원본자료+1],податоци[원본자료]))
            if внес_COUNT:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        број_на_порта=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        клиент=socket.create_connection(('127.0.0.1',број_на_порта),timeout=10)
        assert EXACT_VALUE(клиент,12)==b'RFB 003.008\n';клиент.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(клиент,EXACT_VALUE(клиент,1)[0]);клиент.sendall(b'\x01');assert EXACT_VALUE(клиент,4)==b'\0'*4
        клиент.sendall(b'\x01');초기값=EXACT_VALUE(клиент,24);EXACT_VALUE(клиент,struct.unpack('>I',초기값[20:])[0])
        клиент.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        клиент.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in обвивка('ftpd start')
        датотека_пренос_врска=ftplib.FTP();датотека_пренос_врска.encoding='utf-8';датотека_пренос_врска.connect('127.0.0.1',датотека_пренос_број_на_порта,timeout=20);датотека_пренос_врска.login()
        капацитет_податоци=('GUI와 FTP 동시 사용 '+јазик+' 😀\n').encode()
        датотека_пренос_врска.storbinary('STOR 함께.txt',io.BytesIO(капацитет_податоци))
        assert капацитет_податоци.decode().strip() in обвивка('cat /함께.txt')
        RECEIVED_COUNT=bytearray();датотека_пренос_врска.retrbinary('RETR 함께.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==капацитет_податоци;датотека_пренос_врска.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        испрати_Список=обвивка('ls /example')
        assert all(Име in испрати_Список for Име in ('java/','c/','python/','README.md')),испрати_Список
        if јазик=='java':
            꾸러미명세=json.loads((Project_корен/'build/examples/manifest.json').read_text())
            for ПАТЕКА,внес_поен in 꾸러미명세.items():
                обвивка('cp '+ПАТЕКА+' /example-check.bin')
                Содржина_VALUE=bytearray();датотека_пренос_врска.retrbinary('RETR example-check.bin',Содржина_VALUE.extend)
                assert len(Содржина_VALUE)==внес_поен['bytes'] and hashlib.sha256(Содржина_VALUE).hexdigest()==внес_поен['sha256'],ПАТЕКА
            датотека_пренос_врска.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            бинарен=bytes(range(256))*64
            датотека_пренос_врска.storbinary('STOR boundary.bin',io.BytesIO(бинарен))
            Содржина_VALUE=bytearray();датотека_пренос_врска.retrbinary('RETR boundary.bin',Содржина_VALUE.extend)
            assert Содржина_VALUE==бинарен and 'boundary.bin' in датотека_пренос_врска.nlst()
            обвивка('cp /boundary.bin /boundary-copy.bin')
            Содржина_VALUE=bytearray();датотека_пренос_врска.retrbinary('RETR boundary-copy.bin',Содржина_VALUE.extend)
            assert Содржина_VALUE==бинарен
            датотека_пренос_врска.delete('boundary.bin');датотека_пренос_врска.delete('boundary-copy.bin')
        assert '출력예제' in обвивка('ls /example/'+јазик)
        обвивка('cd /example/'+јазик)
        име_табела={'java':'JAVA','c':'C','python':'PYTHON'}[јазик]
        예상파일=име_табела+' Датотека: 한글 податоци 😀\n'
        if јазик=='java':
            Изврши_наредба('javac 출력예제.java','Compiled:');Изврши_наредба('java 출력예제','JAVA 출력: 안녕하세요 😀')
            Изврши_наредба('javac 파일예제.java','Compiled:');Изврши_наредба('java 파일예제',예상파일)
            Изврши_наредба('java 네트워크예제 {} {}'.format(되돌림서버항목.ТЦП_порта,되돌림서버항목.УДП_порта),'JAVA 네트워크 провери: TCP UDP 한글')
            графика_наредба='java 그래픽예제'
        elif јазик=='c':
            for Име,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('Датотека','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.УДП_порта),'C 네트워크 провери: UDP 한글')]:
                Изврши_наредба('cc '+Име+'예제.c -o Изврши_наредба','Compiled native ARM64 ELF:')
                Изврши_наредба('./Изврши_наредба'+전달값,예상결과)
            Изврши_наредба('cc 그래픽예제.c -o Изврши_наредба','Compiled native ARM64 ELF:');графика_наредба='./Изврши_наредба'
        else:
            for Име,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('Датотека','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.УДП_порта),'PYTHON 네트워크 провери: UDP 한글')]:
                Изврши_наредба('python '+Име+'예제.py'+전달값,예상결과)
            графика_наредба='python 그래픽예제.py'
        Start_цртеж=Start_OFFSET(графика_наредба)
        Текст=수신하기('그림을 확인한 Назад_VALUE Enter를 누르세요.\r\n'.encode(),Start_цртеж)
        assert име_табела+' 그래픽: 빨강 초록 파랑' in Текст and 'exit 0' not in Текст,Текст
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        датотека_пренос_врска.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        RECEIVED_COUNT=bytearray();датотека_пренос_врска.retrbinary('RETR 도중.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==b'FTP DURING GRAPHICS';датотека_пренос_врска.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            OFFSET_VALUE=(세로좌표*640+610)*3;assert tuple(빛삼원색[OFFSET_VALUE:OFFSET_VALUE+3])==색상,(јазик,세로좌표,tuple(빛삼원색[OFFSET_VALUE:OFFSET_VALUE+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(мерка_податоци/(јазик+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',Start_цртеж)
        if јазик=='java':
            Start_прозорец=Start_OFFSET('java 창예제')
            수신하기('GUI 예제 Подготви: 창예제'.encode(),Start_прозорец)
            def кликни_VALUE(가로,вертикала_позиционирање):
                for копче in (1,0):клиент.sendall(struct.pack('>BBHH',5,копче,가로,вертикала_позиционирање))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            кликни_VALUE(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for знак_VALUE in '한글':누름값(0x1000000|ord(знак_VALUE));누름값(0x1000000|ord(знак_VALUE),False)
            for 횟수 in (1,2):
                Изврши_2=len(대화기록);кликни_VALUE(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Изврши_2)
            time.sleep(.3)
            прозорец_цртеж=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=прозорец_цртеж.crop((110,272,530,300)).tobytes()
            прозорец_цртеж.save(str(мерка_податоци/'java-swing.png'))
            Изврши_2=len(대화기록);кликни_VALUE(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',Изврши_2)
        # Download the guest-created bytes through FTP in the same GUI VM.
        датотека_внес_име={'java':'java.txt','c':'c.txt','python':'python.txt'}[јазик]
        обвивка('cp '+датотека_внес_име+' /потврди.txt')
        RECEIVED_COUNT=bytearray();датотека_пренос_врска.retrbinary('RETR потврди.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==예상파일.encode()
        обвивка('echo preserved > 출력예제.'+('py' if јазик=='python' else јазик))
        assert 'EXAMPLES READY' in обвивка('example '+јазик)
        assert '\npreserved\n' in обвивка('cat 출력예제.'+('py' if јазик=='python' else јазик))
        assert '한/영 Клуч_VALUE, Shift+Space 또는 F9' in обвивка('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in обвивка('echo GUI NETWORK TOGETHER')
        датотека_пренос_врска.quit();датотека_пренос_врска=None;assert 'FTP stopped' in обвивка('ftpd stop')
        print('PASS '+јазик+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if датотека_пренос_врска:
            try:датотека_пренос_врска.close()
            except OSError:pass
        if клиент:клиент.close()
        Процес.terminate()
        try:Процес.wait(timeout=8)
        except subprocess.TimeoutExpired:Процес.kill();Процес.wait()
        избирач.close();Процес.stdout.close();(мерка_податоци/(јазик+'-serial.log')).write_bytes(대화기록)


def Изврши_2():
    мерка_податоци=Project_корен/'build/verification/examples';мерка_податоци.mkdir(parents=True,exist_ok=True)
    проверка_извештај={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_корен/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for јазик in ('java','c','python'):
                test_언어(јазик,되돌림서버항목,мерка_податоци);проверка_извештај['languages'].append(јазик)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(област_VALUE,податоци.encode()) for област_VALUE,податоци in 예상결과],되돌림서버항목.수신됨
            проверка_извештај['host_network_payloads']=[{'protocol':област_VALUE,'text':податоци.decode()} for област_VALUE,податоци in 되돌림서버항목.수신됨]
        проверка_извештај.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(мерка_податоци/'report.json').write_text(json.dumps(проверка_извештај,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Изврши_2()
