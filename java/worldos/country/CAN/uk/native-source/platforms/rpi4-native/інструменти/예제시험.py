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
from настільний_Вигляд import 정확한값
from 예제되돌림서버 import відлуння_Сервери
from Виконати_команда import Дії_корінь


def test_언어(Мови,відлуння_сервер_запис,КР_дані):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));передавання_файлу_номер_порту=임시자원.getsockname()[1]
    Процеси=subprocess.Popen(['python3',str(Дії_корінь/'інструменти/Виконати_команда.py'),'--desktop','--network','--port','0','--ftp-port',str(передавання_файлу_номер_порту)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    селектор=selectors.DefaultSelector();селектор.register(Процеси.stdout,selectors.EVENT_READ)
    транскрипт=bytearray();клієнт=None;передавання_файлу_зв_язок=None
    def отримувати_повідомлення(маркер,запустити=0):
        завершити_виклик_Зміщена_копія=time.monotonic()+60
        while маркер not in транскрипт[запустити:]:
            if time.monotonic()>завершити_виклик_Зміщена_копія or Процеси.poll() is not None:raise AssertionError(транскрипт[запустити:].decode('utf-8','replace'))
            for 누름값,_ in селектор.select(.1):
                дані=누름값.fileobj.read(65536)
                if дані:транскрипт.extend(дані)
        return транскрипт[запустити:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(символ_значення,누르는중=True):клієнт.sendall(struct.pack('>BBHI',4,int(누르는중),0,символ_значення))
    def ПУСК_Зміщена_копія(рядок_введення):
        запустити=len(транскрипт)
        for код_символу in рядок_введення+'\n':
            символ_значення=0xff0d if код_символу=='\n' else ord(код_символу) if ord(код_символу)<256 else 0x1000000|ord(код_символу)
            누름값(символ_значення);누름값(символ_значення,False)
        return запустити
    def оболонка(рядок_введення):return отримувати_повідомлення(b'jkoros-native> ',ПУСК_Зміщена_копія(рядок_введення))
    def Виконати_команда(рядок_введення,예상결과):
        текст=оболонка(рядок_введення);assert 예상결과 in текст and 'exit 0' in текст,(рядок_введення,текст)
        return текст
    def 화소들():
        клієнт.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            область_значення=정확한값(клієнт,1)[0]
            if область_значення==2:continue
            if область_значення==3:
                개수=struct.unpack('>I',정확한값(клієнт,7)[3:])[0];정확한값(клієнт,개수);continue
            assert область_значення==0,область_значення
            항목수=struct.unpack('>H',정확한값(клієнт,3)[1:])[0]
            for _ in range(항목수):
                координата_X,세로좌표,너비값,높이값,набір_символів=struct.unpack('>HHHHi',정확한값(клієнт,12));assert набір_символів==0,набір_символів
                дані=정확한값(клієнт,너비값*높이값*4)
                for запис_посада in range(높이값):
                    for стовпець_посада in range(너비값):
                        원본자료=(запис_посада*너비값+стовпець_посада)*4;мета=((세로좌표+запис_посада)*640+координата_X+стовпець_посада)*3
                        빛삼원색[мета:мета+3]=bytes((дані[원본자료+2],дані[원본자료+1],дані[원본자료]))
            if 항목수:return 빛삼원색
    try:
        отримувати_повідомлення(b'TERMINAL READY');отримувати_повідомлення(b'jkoros-native> ',транскрипт.rfind(b'TERMINAL READY'))
        номер_порту=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',транскрипт).group(1))
        клієнт=socket.create_connection(('127.0.0.1',номер_порту),timeout=10)
        assert 정확한값(клієнт,12)==b'RFB 003.008\n';клієнт.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(клієнт,정확한값(клієнт,1)[0]);клієнт.sendall(b'\x01');assert 정확한값(клієнт,4)==b'\0'*4
        клієнт.sendall(b'\x01');초기값=정확한값(клієнт,24);정확한값(клієнт,struct.unpack('>I',초기값[20:])[0])
        клієнт.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        клієнт.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in оболонка('ftpd start')
        передавання_файлу_зв_язок=ftplib.FTP();передавання_файлу_зв_язок.encoding='utf-8';передавання_файлу_зв_язок.connect('127.0.0.1',передавання_файлу_номер_порту,timeout=20);передавання_файлу_зв_язок.login()
        вміст_пакета_дані=('GUI와 FTP 동시 використання_значення '+Мови+' 😀\n').encode()
        передавання_файлу_зв_язок.storbinary('STOR 함께.txt',io.BytesIO(вміст_пакета_дані))
        assert вміст_пакета_дані.decode().strip() in оболонка('cat /함께.txt')
        받은수=bytearray();передавання_файлу_зв_язок.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==вміст_пакета_дані;передавання_файлу_зв_язок.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        надсилати_список=оболонка('ls /example')
        assert all(Назва in надсилати_список for Назва in ('java/','c/','python/','README.md')),надсилати_список
        if Мови=='java':
            꾸러미명세=json.loads((Дії_корінь/'build/examples/manifest.json').read_text())
            for шлях,запис_бал in 꾸러미명세.items():
                оболонка('cp '+шлях+' /example-check.bin')
                Вміст_значення=bytearray();передавання_файлу_зв_язок.retrbinary('RETR example-check.bin',Вміст_значення.extend)
                assert len(Вміст_значення)==запис_бал['bytes'] and hashlib.sha256(Вміст_значення).hexdigest()==запис_бал['sha256'],шлях
            передавання_файлу_зв_язок.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            бінарний=bytes(range(256))*64
            передавання_файлу_зв_язок.storbinary('STOR boundary.bin',io.BytesIO(бінарний))
            Вміст_значення=bytearray();передавання_файлу_зв_язок.retrbinary('RETR boundary.bin',Вміст_значення.extend)
            assert Вміст_значення==бінарний and 'boundary.bin' in передавання_файлу_зв_язок.nlst()
            оболонка('cp /boundary.bin /boundary-copy.bin')
            Вміст_значення=bytearray();передавання_файлу_зв_язок.retrbinary('RETR boundary-copy.bin',Вміст_значення.extend)
            assert Вміст_значення==бінарний
            передавання_файлу_зв_язок.delete('boundary.bin');передавання_файлу_зв_язок.delete('boundary-copy.bin')
        assert 'ПрикладВиводу' in оболонка('ls /example/'+Мови)
        оболонка('cd /example/'+Мови)
        ім_я_таблиця={'java':'JAVA','c':'C','python':'PYTHON'}[Мови]
        예상파일=ім_я_таблиця+' файл: 한글 дані 😀\n'
        if Мови=='java':
            Виконати_команда('javac ПрикладВиводу.java','Compiled:');Виконати_команда('java ПрикладВиводу','JAVA Вивід: 안녕하세요 😀')
            Виконати_команда('javac ПрикладФайлу.java','Compiled:');Виконати_команда('java ПрикладФайлу',예상파일)
            Виконати_команда('java ПрикладМережі {} {}'.format(відлуння_сервер_запис.протокол_керування_передаванням_порт,відлуння_сервер_запис.протокол_користувацьких_дейтаграм_порт),'JAVA 네트워크 перевіряти: TCP UDP 한글')
            графіка_команда='java ПрикладМалювання'
        elif Мови=='c':
            for Назва,전달값,예상결과 in [('Вивід','', 'C Вивід: 안녕하세요 😀'),('файл','',예상파일),
                    ('네트워크',' '+str(відлуння_сервер_запис.протокол_користувацьких_дейтаграм_порт),'C 네트워크 перевіряти: UDP 한글')]:
                Виконати_команда('cc '+Назва+'예제.c -o Виконати_команда','Compiled native ARM64 ELF:')
                Виконати_команда('./Виконати_команда'+전달값,예상결과)
            Виконати_команда('cc ПрикладМалювання.c -o Виконати_команда','Compiled native ARM64 ELF:');графіка_команда='./Виконати_команда'
        else:
            for Назва,전달값,예상결과 in [('Вивід','','PYTHON Вивід: 안녕하세요 😀'),('файл','',예상파일),
                    ('네트워크',' '+str(відлуння_сервер_запис.протокол_користувацьких_дейтаграм_порт),'PYTHON 네트워크 перевіряти: UDP 한글')]:
                Виконати_команда('python '+Назва+'예제.py'+전달값,예상결과)
            графіка_команда='python ПрикладМалювання.py'
        ПУСК_малювання=ПУСК_Зміщена_копія(графіка_команда)
        текст=отримувати_повідомлення('그림을 확인한 НАЗАД_значення Enter를 누르세요.\r\n'.encode(),ПУСК_малювання)
        assert ім_я_таблиця+' 그래픽: 빨강 초록 파랑' in текст and 'exit 0' not in текст,текст
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        передавання_файлу_зв_язок.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();передавання_файлу_зв_язок.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';передавання_файлу_зв_язок.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            Зміщена_копія_значення=(세로좌표*640+610)*3;assert tuple(빛삼원색[Зміщена_копія_значення:Зміщена_копія_значення+3])==색상,(Мови,세로좌표,tuple(빛삼원색[Зміщена_копія_значення:Зміщена_копія_значення+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(КР_дані/(Мови+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in отримувати_повідомлення(b'jkoros-native> ',ПУСК_малювання)
        if Мови=='java':
            ПУСК_вікно=ПУСК_Зміщена_копія('java ПрикладВікна')
            отримувати_повідомлення('GUI 예제 Готувати: ПрикладВікна'.encode(),ПУСК_вікно)
            def клік_значення(가로,Вертикаль_посада):
                for кнопка in (1,0):клієнт.sendall(struct.pack('>BBHH',5,кнопка,가로,Вертикаль_посада))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            клік_значення(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for символ_значення_068c2631 in '한글':누름값(0x1000000|ord(символ_значення_068c2631));누름값(0x1000000|ord(символ_значення_068c2631),False)
            for 횟수 in (1,2):
                запустити=len(транскрипт);клік_значення(180,242)
                отримувати_повідомлення(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),запустити)
            time.sleep(.3)
            вікно_малювання=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=вікно_малювання.crop((110,272,530,300)).tobytes()
            вікно_малювання.save(str(КР_дані/'java-swing.png'))
            запустити=len(транскрипт);клік_значення(535,105)
            assert 'exit 0' in отримувати_повідомлення(b'jkoros-native> ',запустити)
        # Download the guest-created bytes through FTP in the same GUI VM.
        Файл_запис_ім_я={'java':'java.txt','c':'c.txt','python':'python.txt'}[Мови]
        оболонка('cp '+Файл_запис_ім_я+' /затвердити.txt')
        받은수=bytearray();передавання_файлу_зв_язок.retrbinary('RETR затвердити.txt',받은수.extend);assert 받은수==예상파일.encode()
        оболонка('echo preserved > ПрикладВиводу.'+('py' if Мови=='python' else Мови))
        assert 'EXAMPLES READY' in оболонка('example '+Мови)
        assert '\npreserved\n' in оболонка('cat ПрикладВиводу.'+('py' if Мови=='python' else Мови))
        assert '한/нуль_операнд Ключ_значення, Shift+Space 또는 F9' in оболонка('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in оболонка('echo GUI NETWORK TOGETHER')
        передавання_файлу_зв_язок.quit();передавання_файлу_зв_язок=None;assert 'FTP stopped' in оболонка('ftpd stop')
        print('PASS '+Мови+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if передавання_файлу_зв_язок:
            try:передавання_файлу_зв_язок.close()
            except OSError:pass
        if клієнт:клієнт.close()
        Процеси.terminate()
        try:Процеси.wait(timeout=8)
        except subprocess.TimeoutExpired:Процеси.kill();Процеси.wait()
        селектор.close();Процеси.stdout.close();(КР_дані/(Мови+'-serial.log')).write_bytes(транскрипт)


def запустити():
    КР_дані=Дії_корінь/'build/verification/examples';КР_дані.mkdir(parents=True,exist_ok=True)
    перевірка_звіт={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Дії_корінь/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with відлуння_Сервери() as відлуння_сервер_запис:
            for Мови in ('java','c','python'):
                test_언어(Мови,відлуння_сервер_запис,КР_дані);перевірка_звіт['languages'].append(Мови)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert відлуння_сервер_запис.수신됨==[(область_значення,дані.encode()) for область_значення,дані in 예상결과],відлуння_сервер_запис.수신됨
            перевірка_звіт['host_network_payloads']=[{'protocol':область_значення,'text':дані.decode()} for область_значення,дані in відлуння_сервер_запис.수신됨]
        перевірка_звіт.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(КР_дані/'report.json').write_text(json.dumps(перевірка_звіт,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':запустити()
