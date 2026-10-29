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
from классик_карау import EXACT_VALUE
from 예제되돌림서버 import 되돌림서버
from үтәргә_команда import экранга_җибәрү_тамыр


def test_언어(тел,되돌림서버항목,үлчәм_мәгълүмат):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    Процесс=subprocess.Popen(['python3',str(экранга_җибәрү_тамыр/'Кораллар/үтәргә_команда.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    сайлагыч=selectors.DefaultSelector();сайлагыч.register(Процесс.stdout,selectors.EVENT_READ)
    대화기록=bytearray();клиент=None;файл_күчерү_тоташу=None
    def 수신하기(확인표시,эшләтү=0):
        тәмамлау_OFFSET=time.monotonic()+60
        while 확인표시 not in 대화기록[эшләтү:]:
            if time.monotonic()>тәмамлау_OFFSET or Процесс.poll() is not None:raise AssertionError(대화기록[эшләтү:].decode('utf-8','replace'))
            for 누름값,_ in сайлагыч.select(.1):
                мәгълүмат=누름값.fileobj.read(65536)
                if мәгълүмат:대화기록.extend(мәгълүмат)
        return 대화기록[эшләтү:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(символ_VALUE,누르는중=True):клиент.sendall(struct.pack('>BBHI',4,int(누르는중),0,символ_VALUE))
    def Start_OFFSET(юл):
        эшләтү=len(대화기록)
        for символ_коды in юл+'\n':
            символ_VALUE=0xff0d if символ_коды=='\n' else ord(символ_коды) if ord(символ_коды)<256 else 0x1000000|ord(символ_коды)
            누름값(символ_VALUE);누름값(символ_VALUE,False)
        return эшләтү
    def тышча(юл):return 수신하기(b'jkoros-native> ',Start_OFFSET(юл))
    def үтәргә_команда(юл,예상결과):
        Mäten=тышча(юл);assert 예상결과 in Mäten and 'exit 0' in Mäten,(юл,Mäten)
        return Mäten
    def 화소들():
        клиент.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            категория_VALUE=EXACT_VALUE(клиент,1)[0]
            if категория_VALUE==2:continue
            if категория_VALUE==3:
                элемент_COUNT=struct.unpack('>I',EXACT_VALUE(клиент,7)[3:])[0];EXACT_VALUE(клиент,элемент_COUNT);continue
            assert категория_VALUE==0,категория_VALUE
            кертү_COUNT=struct.unpack('>H',EXACT_VALUE(клиент,3)[1:])[0]
            for _ in range(кертү_COUNT):
                X_координатасы,세로좌표,너비값,높이값,символлар_җыелмасы=struct.unpack('>HHHHi',EXACT_VALUE(клиент,12));assert символлар_җыелмасы==0,символлар_җыелмасы
                мәгълүмат=EXACT_VALUE(клиент,너비값*높이값*4)
                for юл_урнаштыру in range(높이값):
                    for COLUMN_урнаштыру in range(너비값):
                        원본자료=(юл_урнаштыру*너비값+COLUMN_урнаштыру)*4;максат_кыйммәт=((세로좌표+юл_урнаштыру)*640+X_координатасы+COLUMN_урнаштыру)*3
                        빛삼원색[максат_кыйммәт:максат_кыйммәт+3]=bytes((мәгълүмат[원본자료+2],мәгълүмат[원본자료+1],мәгълүмат[원본자료]))
            if кертү_COUNT:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        клиент=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert EXACT_VALUE(клиент,12)==b'RFB 003.008\n';клиент.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(клиент,EXACT_VALUE(клиент,1)[0]);клиент.sendall(b'\x01');assert EXACT_VALUE(клиент,4)==b'\0'*4
        клиент.sendall(b'\x01');초기값=EXACT_VALUE(клиент,24);EXACT_VALUE(клиент,struct.unpack('>I',초기값[20:])[0])
        клиент.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        клиент.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in тышча('ftpd start')
        файл_күчерү_тоташу=ftplib.FTP();файл_күчерү_тоташу.encoding='utf-8';файл_күчерү_тоташу.connect('127.0.0.1',파일전송접속번호,timeout=20);файл_күчерү_тоташу.login()
        төп_өлеш_мәгълүмат=('GUI와 FTP 동시 사용 '+тел+' 😀\n').encode()
        файл_күчерү_тоташу.storbinary('STOR 함께.txt',io.BytesIO(төп_өлеш_мәгълүмат))
        assert төп_өлеш_мәгълүмат.decode().strip() in тышча('cat /함께.txt')
        RECEIVED_COUNT=bytearray();файл_күчерү_тоташу.retrbinary('RETR 함께.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==төп_өлеш_мәгълүмат;файл_күчерү_тоташу.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        җибәрү_Исемлек=тышча('ls /example')
        assert all(исем in җибәрү_Исемлек for исем in ('java/','c/','python/','README.md')),җибәрү_Исемлек
        if тел=='java':
            꾸러미명세=json.loads((экранга_җибәрү_тамыр/'build/examples/manifest.json').read_text())
            for Yul,кертү_балл in 꾸러미명세.items():
                тышча('cp '+Yul+' /example-check.bin')
                Эчтәлек_VALUE=bytearray();файл_күчерү_тоташу.retrbinary('RETR example-check.bin',Эчтәлек_VALUE.extend)
                assert len(Эчтәлек_VALUE)==кертү_балл['bytes'] and hashlib.sha256(Эчтәлек_VALUE).hexdigest()==кертү_балл['sha256'],Yul
            файл_күчерү_тоташу.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            бинар=bytes(range(256))*64
            файл_күчерү_тоташу.storbinary('STOR boundary.bin',io.BytesIO(бинар))
            Эчтәлек_VALUE=bytearray();файл_күчерү_тоташу.retrbinary('RETR boundary.bin',Эчтәлек_VALUE.extend)
            assert Эчтәлек_VALUE==бинар and 'boundary.bin' in файл_күчерү_тоташу.nlst()
            тышча('cp /boundary.bin /boundary-copy.bin')
            Эчтәлек_VALUE=bytearray();файл_күчерү_тоташу.retrbinary('RETR boundary-copy.bin',Эчтәлек_VALUE.extend)
            assert Эчтәлек_VALUE==бинар
            файл_күчерү_тоташу.delete('boundary.bin');файл_күчерү_тоташу.delete('boundary-copy.bin')
        assert '출력예제' in тышча('ls /example/'+тел)
        тышча('cd /example/'+тел)
        исем_таблица={'java':'JAVA','c':'C','python':'PYTHON'}[тел]
        예상파일=исем_таблица+' Birem: 한글 мәгълүмат 😀\n'
        if тел=='java':
            үтәргә_команда('javac 출력예제.java','Compiled:');үтәргә_команда('java 출력예제','JAVA 출력: 안녕하세요 😀')
            үтәргә_команда('javac 파일예제.java','Compiled:');үтәргә_команда('java 파일예제',예상파일)
            үтәргә_команда('java 네트워크예제 {} {}'.format(되돌림서버항목.TCP_протоколы_порт,되돌림서버항목.UDP_порт),'JAVA 네트워크 раслау: TCP UDP 한글')
            графика_команда='java 그래픽예제'
        elif тел=='c':
            for исем,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('Birem','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.UDP_порт),'C 네트워크 раслау: UDP 한글')]:
                үтәргә_команда('cc '+исем+'예제.c -o үтәргә_команда','Compiled native ARM64 ELF:')
                үтәргә_команда('./үтәргә_команда'+전달값,예상결과)
            үтәргә_команда('cc 그래픽예제.c -o үтәргә_команда','Compiled native ARM64 ELF:');графика_команда='./үтәргә_команда'
        else:
            for исем,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('Birem','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.UDP_порт),'PYTHON 네트워크 раслау: UDP 한글')]:
                үтәргә_команда('python '+исем+'예제.py'+전달값,예상결과)
            графика_команда='python 그래픽예제.py'
        Start_сызым=Start_OFFSET(графика_команда)
        Mäten=수신하기('그림을 확인한 Артка_VALUE Enter를 누르세요.\r\n'.encode(),Start_сызым)
        assert исем_таблица+' 그래픽: 빨강 초록 파랑' in Mäten and 'exit 0' not in Mäten,Mäten
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        файл_күчерү_тоташу.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        RECEIVED_COUNT=bytearray();файл_күчерү_тоташу.retrbinary('RETR 도중.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==b'FTP DURING GRAPHICS';файл_күчерү_тоташу.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            OFFSET_VALUE=(세로좌표*640+610)*3;assert tuple(빛삼원색[OFFSET_VALUE:OFFSET_VALUE+3])==색상,(тел,세로좌표,tuple(빛삼원색[OFFSET_VALUE:OFFSET_VALUE+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(үлчәм_мәгълүмат/(тел+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',Start_сызым)
        if тел=='java':
            Start_тәрәз=Start_OFFSET('java 창예제')
            수신하기('GUI 예제 Әзерләү: 창예제'.encode(),Start_тәрәз)
            def чирттерү_VALUE(가로,Вертикаль_урнаштыру):
                for төймә in (1,0):клиент.sendall(struct.pack('>BBHH',5,төймә,가로,Вертикаль_урнаштыру))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            чирттерү_VALUE(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for символ_VALUE_068c2631 in '한글':누름값(0x1000000|ord(символ_VALUE_068c2631));누름값(0x1000000|ord(символ_VALUE_068c2631),False)
            for 횟수 in (1,2):
                эшләтү=len(대화기록);чирттерү_VALUE(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),эшләтү)
            time.sleep(.3)
            тәрәз_сызым=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=тәрәз_сызым.crop((110,272,530,300)).tobytes()
            тәрәз_сызым.save(str(үлчәм_мәгълүмат/'java-swing.png'))
            эшләтү=len(대화기록);чирттерү_VALUE(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',эшләтү)
        # Download the guest-created bytes through FTP in the same GUI VM.
        файл_кертү_исем={'java':'java.txt','c':'c.txt','python':'python.txt'}[тел]
        тышча('cp '+файл_кертү_исем+' /тикшерү.txt')
        RECEIVED_COUNT=bytearray();файл_күчерү_тоташу.retrbinary('RETR тикшерү.txt',RECEIVED_COUNT.extend);assert RECEIVED_COUNT==예상파일.encode()
        тышча('echo preserved > 출력예제.'+('py' if тел=='python' else тел))
        assert 'EXAMPLES READY' in тышча('example '+тел)
        assert '\npreserved\n' in тышча('cat 출력예제.'+('py' if тел=='python' else тел))
        assert '한/영 ачкыч_VALUE, Shift+Space 또는 F9' in тышча('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in тышча('echo GUI NETWORK TOGETHER')
        файл_күчерү_тоташу.quit();файл_күчерү_тоташу=None;assert 'FTP stopped' in тышча('ftpd stop')
        print('PASS '+тел+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if файл_күчерү_тоташу:
            try:файл_күчерү_тоташу.close()
            except OSError:pass
        if клиент:клиент.close()
        Процесс.terminate()
        try:Процесс.wait(timeout=8)
        except subprocess.TimeoutExpired:Процесс.kill();Процесс.wait()
        сайлагыч.close();Процесс.stdout.close();(үлчәм_мәгълүмат/(тел+'-serial.log')).write_bytes(대화기록)


def эшләтү():
    үлчәм_мәгълүмат=экранга_җибәрү_тамыр/'build/verification/examples';үлчәм_мәгълүмат.mkdir(parents=True,exist_ok=True)
    раслау_отчет={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((экранга_җибәрү_тамыр/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for тел in ('java','c','python'):
                test_언어(тел,되돌림서버항목,үлчәм_мәгълүмат);раслау_отчет['languages'].append(тел)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(категория_VALUE,мәгълүмат.encode()) for категория_VALUE,мәгълүмат in 예상결과],되돌림서버항목.수신됨
            раслау_отчет['host_network_payloads']=[{'protocol':категория_VALUE,'text':мәгълүмат.decode()} for категория_VALUE,мәгълүмат in 되돌림서버항목.수신됨]
        раслау_отчет.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(үлчәм_мәгълүмат/'report.json').write_text(json.dumps(раслау_отчет,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':эшләтү()
