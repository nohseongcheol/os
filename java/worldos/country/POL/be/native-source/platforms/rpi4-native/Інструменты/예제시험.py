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
from працоўны_стол_выгляд import 정확한값
from 예제되돌림서버 import 되돌림서버
from выканаць_каманда import 기준


def test_언어(Мова,되돌림서버항목,결과자료):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));файл_перанос_нумар_порта=임시자원.getsockname()[1]
    Працэс=subprocess.Popen(['python3',str(기준/'Інструменты/выканаць_каманда.py'),'--desktop','--network','--port','0','--ftp-port',str(файл_перанос_нумар_порта)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    селектар=selectors.DefaultSelector();селектар.register(Працэс.stdout,selectors.EVENT_READ)
    대화기록=bytearray();кліент=None;файл_перанос_кантакт=None
    def 수신하기(확인표시,Выканаць=0):
        скончыць_Зрух=time.monotonic()+60
        while 확인표시 not in 대화기록[Выканаць:]:
            if time.monotonic()>скончыць_Зрух or Працэс.poll() is not None:raise AssertionError(대화기록[Выканаць:].decode('utf-8','replace'))
            for 누름값,_ in селектар.select(.1):
                дадзеныя=누름값.fileobj.read(65536)
                if дадзеныя:대화기록.extend(дадзеныя)
        return 대화기록[Выканаць:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(сімвал_значэнне,누르는중=True):кліент.sendall(struct.pack('>BBHI',4,int(누르는중),0,сімвал_значэнне))
    def Пуск_Зрух(лінія):
        Выканаць=len(대화기록)
        for код_сімвала in лінія+'\n':
            сімвал_значэнне=0xff0d if код_сімвала=='\n' else ord(код_сімвала) if ord(код_сімвала)<256 else 0x1000000|ord(код_сімвала)
            누름값(сімвал_значэнне);누름값(сімвал_значэнне,False)
        return Выканаць
    def абалонка(лінія):return 수신하기(b'jkoros-native> ',Пуск_Зрух(лінія))
    def выканаць_каманда(лінія,예상결과):
        Тэкст=абалонка(лінія);assert 예상결과 in Тэкст and 'exit 0' in Тэкст,(лінія,Тэкст)
        return Тэкст
    def 화소들():
        кліент.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            катэгорыя_значэнне=정확한값(кліент,1)[0]
            if катэгорыя_значэнне==2:continue
            if катэгорыя_значэнне==3:
                개수=struct.unpack('>I',정확한값(кліент,7)[3:])[0];정확한값(кліент,개수);continue
            assert катэгорыя_значэнне==0,катэгорыя_значэнне
            항목수=struct.unpack('>H',정확한값(кліент,3)[1:])[0]
            for _ in range(항목수):
                каардыната_x,세로좌표,너비값,높이값,набор_сімвалаў=struct.unpack('>HHHHi',정확한값(кліент,12));assert набор_сімвалаў==0,набор_сімвалаў
                дадзеныя=정확한값(кліент,너비값*높이값*4)
                for 행위치 in range(높이값):
                    for 열위치 in range(너비값):
                        원본자료=(행위치*너비값+열위치)*4;мэтавы_паказчык=((세로좌표+행위치)*640+каардыната_x+열위치)*3
                        빛삼원색[мэтавы_паказчык:мэтавы_паказчык+3]=bytes((дадзеныя[원본자료+2],дадзеныя[원본자료+1],дадзеныя[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        нумар_порта=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        кліент=socket.create_connection(('127.0.0.1',нумар_порта),timeout=10)
        assert 정확한값(кліент,12)==b'RFB 003.008\n';кліент.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(кліент,정확한값(кліент,1)[0]);кліент.sendall(b'\x01');assert 정확한값(кліент,4)==b'\0'*4
        кліент.sendall(b'\x01');초기값=정확한값(кліент,24);정확한값(кліент,struct.unpack('>I',초기값[20:])[0])
        кліент.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        кліент.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in абалонка('ftpd start')
        файл_перанос_кантакт=ftplib.FTP();файл_перанос_кантакт.encoding='utf-8';файл_перанос_кантакт.connect('127.0.0.1',файл_перанос_нумар_порта,timeout=20);файл_перанос_кантакт.login()
        карыснае_змесціва_дадзеныя=('GUI와 FTP 동시 사용 '+Мова+' 😀\n').encode()
        файл_перанос_кантакт.storbinary('STOR 함께.txt',io.BytesIO(карыснае_змесціва_дадзеныя))
        assert карыснае_змесціва_дадзеныя.decode().strip() in абалонка('cat /함께.txt')
        받은수=bytearray();файл_перанос_кантакт.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==карыснае_змесціва_дадзеныя;файл_перанос_кантакт.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        адправіць_Спіс=абалонка('ls /example')
        assert all(Назва in адправіць_Спіс for Назва in ('java/','c/','python/','README.md')),адправіць_Спіс
        if Мова=='java':
            꾸러미명세=json.loads((기준/'build/examples/manifest.json').read_text())
            for ШЛЯХ,увядзенне_бал in 꾸러미명세.items():
                абалонка('cp '+ШЛЯХ+' /example-check.bin')
                кантэнт_значэнне=bytearray();файл_перанос_кантакт.retrbinary('RETR example-check.bin',кантэнт_значэнне.extend)
                assert len(кантэнт_значэнне)==увядзенне_бал['bytes'] and hashlib.sha256(кантэнт_значэнне).hexdigest()==увядзенне_бал['sha256'],ШЛЯХ
            файл_перанос_кантакт.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            дваічны=bytes(range(256))*64
            файл_перанос_кантакт.storbinary('STOR boundary.bin',io.BytesIO(дваічны))
            кантэнт_значэнне=bytearray();файл_перанос_кантакт.retrbinary('RETR boundary.bin',кантэнт_значэнне.extend)
            assert кантэнт_значэнне==дваічны and 'boundary.bin' in файл_перанос_кантакт.nlst()
            абалонка('cp /boundary.bin /boundary-copy.bin')
            кантэнт_значэнне=bytearray();файл_перанос_кантакт.retrbinary('RETR boundary-copy.bin',кантэнт_значэнне.extend)
            assert кантэнт_значэнне==дваічны
            файл_перанос_кантакт.delete('boundary.bin');файл_перанос_кантакт.delete('boundary-copy.bin')
        assert '출력예제' in абалонка('ls /example/'+Мова)
        абалонка('cd /example/'+Мова)
        імя_табліца={'java':'JAVA','c':'C','python':'PYTHON'}[Мова]
        예상파일=імя_табліца+' Файл: 한글 дадзеныя 😀\n'
        if Мова=='java':
            выканаць_каманда('javac 출력예제.java','Compiled:');выканаць_каманда('java 출력예제','JAVA Выхад: 안녕하세요 😀')
            выканаць_каманда('javac 파일예제.java','Compiled:');выканаць_каманда('java 파일예제',예상파일)
            выканаць_каманда('java 네트워크예제 {} {}'.format(되돌림서버항목.пратакол_кіравання_перадачай_TCP_порт,되돌림서버항목.전문접속번호),'JAVA 네트워크 праверыць: TCP UDP 한글')
            그림명령='java 그래픽예제'
        elif Мова=='c':
            for Назва,전달값,예상결과 in [('Выхад','', 'C Выхад: 안녕하세요 😀'),('Файл','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 праверыць: UDP 한글')]:
                выканаць_каманда('cc '+Назва+'예제.c -o выканаць_каманда','Compiled native ARM64 ELF:')
                выканаць_каманда('./выканаць_каманда'+전달값,예상결과)
            выканаць_каманда('cc 그래픽예제.c -o выканаць_каманда','Compiled native ARM64 ELF:');그림명령='./выканаць_каманда'
        else:
            for Назва,전달값,예상결과 in [('Выхад','','PYTHON Выхад: 안녕하세요 😀'),('Файл','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 праверыць: UDP 한글')]:
                выканаць_каманда('python '+Назва+'예제.py'+전달값,예상결과)
            그림명령='python 그래픽예제.py'
        Пуск_рукапісная_графіка=Пуск_Зрух(그림명령)
        Тэкст=수신하기('그림을 확인한 Назад_значэнне Enter를 누르세요.\r\n'.encode(),Пуск_рукапісная_графіка)
        assert імя_табліца+' 그래픽: 빨강 초록 파랑' in Тэкст and 'exit 0' not in Тэкст,Тэкст
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        файл_перанос_кантакт.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();файл_перанос_кантакт.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';файл_перанос_кантакт.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            Зрух_значэнне=(세로좌표*640+610)*3;assert tuple(빛삼원색[Зрух_значэнне:Зрух_значэнне+3])==색상,(Мова,세로좌표,tuple(빛삼원색[Зрух_значэнне:Зрух_значэнне+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(결과자료/(Мова+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',Пуск_рукапісная_графіка)
        if Мова=='java':
            Пуск_акно=Пуск_Зрух('java 창예제')
            수신하기('GUI 예제 Падрыхтаваць: 창예제'.encode(),Пуск_акно)
            def націснуць_значэнне(가로,세로):
                for кнопка in (1,0):кліент.sendall(struct.pack('>BBHH',5,кнопка,가로,세로))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            націснуць_значэнне(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for сімвал_значэнне_068c2631 in '한글':누름값(0x1000000|ord(сімвал_значэнне_068c2631));누름값(0x1000000|ord(сімвал_значэнне_068c2631),False)
            for 횟수 in (1,2):
                Выканаць=len(대화기록);націснуць_значэнне(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Выканаць)
            time.sleep(.3)
            акно_рукапісная_графіка=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=акно_рукапісная_графіка.crop((110,272,530,300)).tobytes()
            акно_рукапісная_графіка.save(str(결과자료/'java-swing.png'))
            Выканаць=len(대화기록);націснуць_значэнне(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',Выканаць)
        # Download the guest-created bytes through FTP in the same GUI VM.
        файл_увядзенне_імя={'java':'java.txt','c':'c.txt','python':'python.txt'}[Мова]
        абалонка('cp '+файл_увядзенне_імя+' /праверыць_5fb2b747.txt')
        받은수=bytearray();файл_перанос_кантакт.retrbinary('RETR праверыць_5fb2b747.txt',받은수.extend);assert 받은수==예상파일.encode()
        абалонка('echo preserved > 출력예제.'+('py' if Мова=='python' else Мова))
        assert 'EXAMPLES READY' in абалонка('example '+Мова)
        assert '\npreserved\n' in абалонка('cat 출력예제.'+('py' if Мова=='python' else Мова))
        assert '한/영 клавіша_значэнне, Shift+Space 또는 F9' in абалонка('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in абалонка('echo GUI NETWORK TOGETHER')
        файл_перанос_кантакт.quit();файл_перанос_кантакт=None;assert 'FTP stopped' in абалонка('ftpd stop')
        print('PASS '+Мова+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if файл_перанос_кантакт:
            try:файл_перанос_кантакт.close()
            except OSError:pass
        if кліент:кліент.close()
        Працэс.terminate()
        try:Працэс.wait(timeout=8)
        except subprocess.TimeoutExpired:Працэс.kill();Працэс.wait()
        селектар.close();Працэс.stdout.close();(결과자료/(Мова+'-serial.log')).write_bytes(대화기록)


def Выканаць():
    결과자료=기준/'build/verification/examples';결과자료.mkdir(parents=True,exist_ok=True)
    праверка_справаздача={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for Мова in ('java','c','python'):
                test_언어(Мова,되돌림서버항목,결과자료);праверка_справаздача['languages'].append(Мова)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(катэгорыя_значэнне,дадзеныя.encode()) for катэгорыя_значэнне,дадзеныя in 예상결과],되돌림서버항목.수신됨
            праверка_справаздача['host_network_payloads']=[{'protocol':катэгорыя_значэнне,'text':дадзеныя.decode()} for катэгорыя_значэнне,дадзеныя in 되돌림서버항목.수신됨]
        праверка_справаздача.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(결과자료/'report.json').write_text(json.dumps(праверка_справаздача,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Выканаць()
