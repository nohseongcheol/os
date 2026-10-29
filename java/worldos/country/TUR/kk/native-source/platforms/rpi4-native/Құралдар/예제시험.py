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
from үстелдік_Көрініс import 정확한값
from 예제되돌림서버 import экранға_шығару_Серверлер
from орындау_пәрмен import жоба_түбір


def test_언어(Тіл,экранға_шығару_сервер_енгізу,өлшем_деректер):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));файл_тасымалдау_порт_нөмірі=임시자원.getsockname()[1]
    Үрдіс=subprocess.Popen(['python3',str(жоба_түбір/'Құралдар/орындау_пәрмен.py'),'--desktop','--network','--port','0','--ftp-port',str(файл_тасымалдау_порт_нөмірі)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    селектор=selectors.DefaultSelector();селектор.register(Үрдіс.stdout,selectors.EVENT_READ)
    대화기록=bytearray();клиент=None;файл_тасымалдау_қосылым=None
    def 수신하기(확인표시,Орындау_2=0):
        тоқтату_жылжыту=time.monotonic()+60
        while 확인표시 not in 대화기록[Орындау_2:]:
            if time.monotonic()>тоқтату_жылжыту or Үрдіс.poll() is not None:raise AssertionError(대화기록[Орындау_2:].decode('utf-8','replace'))
            for 누름값,_ in селектор.select(.1):
                деректер=누름값.fileobj.read(65536)
                if деректер:대화기록.extend(деректер)
        return 대화기록[Орындау_2:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(символ_мән,누르는중=True):клиент.sendall(struct.pack('>BBHI',4,int(누르는중),0,символ_мән))
    def басы_жылжыту(Жол):
        Орындау_2=len(대화기록)
        for таңба_коды in Жол+'\n':
            символ_мән=0xff0d if таңба_коды=='\n' else ord(таңба_коды) if ord(таңба_коды)<256 else 0x1000000|ord(таңба_коды)
            누름값(символ_мән);누름값(символ_мән,False)
        return Орындау_2
    def қоршам(Жол):return 수신하기(b'jkoros-native> ',басы_жылжыту(Жол))
    def орындау_пәрмен(Жол,예상결과):
        Мәтін=қоршам(Жол);assert 예상결과 in Мәтін and 'exit 0' in Мәтін,(Жол,Мәтін)
        return Мәтін
    def 화소들():
        клиент.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            Санат_мән=정확한값(клиент,1)[0]
            if Санат_мән==2:continue
            if Санат_мән==3:
                개수=struct.unpack('>I',정확한값(клиент,7)[3:])[0];정확한값(клиент,개수);continue
            assert Санат_мән==0,Санат_мән
            항목수=struct.unpack('>H',정확한값(клиент,3)[1:])[0]
            for _ in range(항목수):
                x_координатасы,Y_түймешігі_координата,너비값,높이값,таңбалар_жиыны=struct.unpack('>HHHHi',정확한값(клиент,12));assert таңбалар_жиыны==0,таңбалар_жиыны
                деректер=정확한값(клиент,너비값*높이값*4)
                for жол_лауазым in range(높이값):
                    for баған_лауазым in range(너비값):
                        원본자료=(жол_лауазым*너비값+баған_лауазым)*4;мақсатты_мән=((Y_түймешігі_координата+жол_лауазым)*640+x_координатасы+баған_лауазым)*3
                        빛삼원색[мақсатты_мән:мақсатты_мән+3]=bytes((деректер[원본자료+2],деректер[원본자료+1],деректер[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        порт_нөмірі=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        клиент=socket.create_connection(('127.0.0.1',порт_нөмірі),timeout=10)
        assert 정확한값(клиент,12)==b'RFB 003.008\n';клиент.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(клиент,정확한값(клиент,1)[0]);клиент.sendall(b'\x01');assert 정확한값(клиент,4)==b'\0'*4
        клиент.sendall(b'\x01');초기값=정확한값(клиент,24);정확한값(клиент,struct.unpack('>I',초기값[20:])[0])
        клиент.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        клиент.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in қоршам('ftpd start')
        файл_тасымалдау_қосылым=ftplib.FTP();файл_тасымалдау_қосылым.encoding='utf-8';файл_тасымалдау_қосылым.connect('127.0.0.1',файл_тасымалдау_порт_нөмірі,timeout=20);файл_тасымалдау_қосылым.login()
        жүктеме_деректер=('GUI와 FTP 동시 사용 '+Тіл+' 😀\n').encode()
        файл_тасымалдау_қосылым.storbinary('STOR 함께.txt',io.BytesIO(жүктеме_деректер))
        assert жүктеме_деректер.decode().strip() in қоршам('cat /함께.txt')
        받은수=bytearray();файл_тасымалдау_қосылым.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==жүктеме_деректер;файл_тасымалдау_қосылым.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        жіберу_Тізім=қоршам('ls /example')
        assert all(Аты in жіберу_Тізім for Аты in ('java/','c/','python/','README.md')),жіберу_Тізім
        if Тіл=='java':
            꾸러미명세=json.loads((жоба_түбір/'build/examples/manifest.json').read_text())
            for Жол_2,енгізу_ұпай in 꾸러미명세.items():
                қоршам('cp '+Жол_2+' /example-check.bin')
                мазмұн_мән=bytearray();файл_тасымалдау_қосылым.retrbinary('RETR example-check.bin',мазмұн_мән.extend)
                assert len(мазмұн_мән)==енгізу_ұпай['bytes'] and hashlib.sha256(мазмұн_мән).hexdigest()==енгізу_ұпай['sha256'],Жол_2
            файл_тасымалдау_қосылым.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            екілік=bytes(range(256))*64
            файл_тасымалдау_қосылым.storbinary('STOR boundary.bin',io.BytesIO(екілік))
            мазмұн_мән=bytearray();файл_тасымалдау_қосылым.retrbinary('RETR boundary.bin',мазмұн_мән.extend)
            assert мазмұн_мән==екілік and 'boundary.bin' in файл_тасымалдау_қосылым.nlst()
            қоршам('cp /boundary.bin /boundary-copy.bin')
            мазмұн_мән=bytearray();файл_тасымалдау_қосылым.retrbinary('RETR boundary-copy.bin',мазмұн_мән.extend)
            assert мазмұн_мән==екілік
            файл_тасымалдау_қосылым.delete('boundary.bin');файл_тасымалдау_қосылым.delete('boundary-copy.bin')
        assert '출력예제' in қоршам('ls /example/'+Тіл)
        қоршам('cd /example/'+Тіл)
        аты_кесте={'java':'JAVA','c':'C','python':'PYTHON'}[Тіл]
        예상파일=аты_кесте+' Файл: 한글 деректер 😀\n'
        if Тіл=='java':
            орындау_пәрмен('javac 출력예제.java','Compiled:');орындау_пәрмен('java 출력예제','JAVA Шығысы: 안녕하세요 😀')
            орындау_пәрмен('javac 파일예제.java','Compiled:');орындау_пәрмен('java 파일예제',예상파일)
            орындау_пәрмен('java 네트워크예제 {} {}'.format(экранға_шығару_сервер_енгізу.TCP_протоколы_порт,экранға_шығару_сервер_енгізу.пайдаланушы_датаграммасының_протоколы_порт),'JAVA 네트워크 тексеру: TCP UDP 한글')
            графика_пәрмен='java 그래픽예제'
        elif Тіл=='c':
            for Аты,전달값,예상결과 in [('Шығысы','', 'C Шығысы: 안녕하세요 😀'),('Файл','',예상파일),
                    ('네트워크',' '+str(экранға_шығару_сервер_енгізу.пайдаланушы_датаграммасының_протоколы_порт),'C 네트워크 тексеру: UDP 한글')]:
                орындау_пәрмен('cc '+Аты+'예제.c -o орындау_пәрмен','Compiled native ARM64 ELF:')
                орындау_пәрмен('./орындау_пәрмен'+전달값,예상결과)
            орындау_пәрмен('cc 그래픽예제.c -o орындау_пәрмен','Compiled native ARM64 ELF:');графика_пәрмен='./орындау_пәрмен'
        else:
            for Аты,전달값,예상결과 in [('Шығысы','','PYTHON Шығысы: 안녕하세요 😀'),('Файл','',예상파일),
                    ('네트워크',' '+str(экранға_шығару_сервер_енгізу.пайдаланушы_датаграммасының_протоколы_порт),'PYTHON 네트워크 тексеру: UDP 한글')]:
                орындау_пәрмен('python '+Аты+'예제.py'+전달값,예상결과)
            графика_пәрмен='python 그래픽예제.py'
        басы_сызба=басы_жылжыту(графика_пәрмен)
        Мәтін=수신하기('그림을 확인한 АРТҚА_мән Enter를 누르세요.\r\n'.encode(),басы_сызба)
        assert аты_кесте+' 그래픽: 빨강 초록 파랑' in Мәтін and 'exit 0' not in Мәтін,Мәтін
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        файл_тасымалдау_қосылым.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();файл_тасымалдау_қосылым.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';файл_тасымалдау_қосылым.delete('도중.txt')
        빛삼원색=화소들()
        for Y_түймешігі_координата,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            жылжыту_мән_450fc799=(Y_түймешігі_координата*640+610)*3;assert tuple(빛삼원색[жылжыту_мән_450fc799:жылжыту_мән_450fc799+3])==색상,(Тіл,Y_түймешігі_координата,tuple(빛삼원색[жылжыту_мән_450fc799:жылжыту_мән_450fc799+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(өлшем_деректер/(Тіл+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',басы_сызба)
        if Тіл=='java':
            басы_терезе=басы_жылжыту('java 창예제')
            수신하기('GUI 예제 Дайындау: 창예제'.encode(),басы_терезе)
            def басу_мән(가로,Тік_лауазым):
                for батырма in (1,0):клиент.sendall(struct.pack('>BBHH',5,батырма,가로,Тік_лауазым))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            басу_мән(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for таңба_мән in '한글':누름값(0x1000000|ord(таңба_мән));누름값(0x1000000|ord(таңба_мән),False)
            for 횟수 in (1,2):
                Орындау_2=len(대화기록);басу_мән(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Орындау_2)
            time.sleep(.3)
            терезе_сызба=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=терезе_сызба.crop((110,272,530,300)).tobytes()
            терезе_сызба.save(str(өлшем_деректер/'java-swing.png'))
            Орындау_2=len(대화기록);басу_мән(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',Орындау_2)
        # Download the guest-created bytes through FTP in the same GUI VM.
        файл_енгізу_аты={'java':'java.txt','c':'c.txt','python':'python.txt'}[Тіл]
        қоршам('cp '+файл_енгізу_аты+' /тексеру_5fb2b747.txt')
        받은수=bytearray();файл_тасымалдау_қосылым.retrbinary('RETR тексеру_5fb2b747.txt',받은수.extend);assert 받은수==예상파일.encode()
        қоршам('echo preserved > 출력예제.'+('py' if Тіл=='python' else Тіл))
        assert 'EXAMPLES READY' in қоршам('example '+Тіл)
        assert '\npreserved\n' in қоршам('cat 출력예제.'+('py' if Тіл=='python' else Тіл))
        assert '한/영 Кілт_мән, Shift+Space 또는 F9' in қоршам('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in қоршам('echo GUI NETWORK TOGETHER')
        файл_тасымалдау_қосылым.quit();файл_тасымалдау_қосылым=None;assert 'FTP stopped' in қоршам('ftpd stop')
        print('PASS '+Тіл+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if файл_тасымалдау_қосылым:
            try:файл_тасымалдау_қосылым.close()
            except OSError:pass
        if клиент:клиент.close()
        Үрдіс.terminate()
        try:Үрдіс.wait(timeout=8)
        except subprocess.TimeoutExpired:Үрдіс.kill();Үрдіс.wait()
        селектор.close();Үрдіс.stdout.close();(өлшем_деректер/(Тіл+'-serial.log')).write_bytes(대화기록)


def Орындау_2():
    өлшем_деректер=жоба_түбір/'build/verification/examples';өлшем_деректер.mkdir(parents=True,exist_ok=True)
    тексерім_есеп={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((жоба_түбір/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with экранға_шығару_Серверлер() as экранға_шығару_сервер_енгізу:
            for Тіл in ('java','c','python'):
                test_언어(Тіл,экранға_шығару_сервер_енгізу,өлшем_деректер);тексерім_есеп['languages'].append(Тіл)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert экранға_шығару_сервер_енгізу.수신됨==[(Санат_мән,деректер.encode()) for Санат_мән,деректер in 예상결과],экранға_шығару_сервер_енгізу.수신됨
            тексерім_есеп['host_network_payloads']=[{'protocol':Санат_мән,'text':деректер.decode()} for Санат_мән,деректер in экранға_шығару_сервер_енгізу.수신됨]
        тексерім_есеп.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(өлшем_деректер/'report.json').write_text(json.dumps(тексерім_есеп,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Орындау_2()
