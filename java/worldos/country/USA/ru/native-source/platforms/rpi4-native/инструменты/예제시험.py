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
from компьютер_Вид import СОВПАД_ЗНАЧЕН
from 예제되돌림서버 import вывод_на_экран_Серверы
from 실행 import задача_корень


def тест_Язык(Язык,вывод_на_экран_сервер_ввод,KR_данные):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));передача_файла_номер_порта=임시자원.getsockname()[1]
    Процесс=subprocess.Popen(['python3',str(задача_корень/'инструменты/실행.py'),'--desktop','--network','--port','0','--ftp-port',str(передача_файла_номер_порта)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    селектор=selectors.DefaultSelector();селектор.register(Процесс.stdout,selectors.EVENT_READ)
    расшифровка=bytearray();клиент=None;передача_файла_контакт=None
    def получить_письмо(метка,запустить=0):
        элемент_СМЕЩ=time.monotonic()+60
        while метка not in расшифровка[запустить:]:
            if time.monotonic()>элемент_СМЕЩ or Процесс.poll() is not None:raise AssertionError(расшифровка[запустить:].decode('utf-8','replace'))
            for 누름값,_ in селектор.select(.1):
                данные=누름값.fileobj.read(65536)
                if данные:расшифровка.extend(данные)
        return расшифровка[запустить:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(символ_ЗНАЧЕН,누르는중=True):клиент.sendall(struct.pack('>BBHI',4,int(누르는중),0,символ_ЗНАЧЕН))
    def Пуск_СМЕЩ(строка_ввода):
        запустить=len(расшифровка)
        for код_знака in строка_ввода+'\n':
            символ_ЗНАЧЕН=0xff0d if код_знака=='\n' else ord(код_знака) if ord(код_знака)<256 else 0x1000000|ord(код_знака)
            누름값(символ_ЗНАЧЕН);누름값(символ_ЗНАЧЕН,False)
        return запустить
    def оболочка(строка_ввода):return получить_письмо(b'jkoros-native> ',Пуск_СМЕЩ(строка_ввода))
    def 실행(строка_ввода,예상결과):
        текст=оболочка(строка_ввода);assert 예상결과 in текст and 'exit 0' in текст,(строка_ввода,текст)
        return текст
    def 화소들():
        клиент.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            область_ЗНАЧЕН=СОВПАД_ЗНАЧЕН(клиент,1)[0]
            if область_ЗНАЧЕН==2:continue
            if область_ЗНАЧЕН==3:
                товар_СЧЁТ=struct.unpack('>I',СОВПАД_ЗНАЧЕН(клиент,7)[3:])[0];СОВПАД_ЗНАЧЕН(клиент,товар_СЧЁТ);continue
            assert область_ЗНАЧЕН==0,область_ЗНАЧЕН
            ввод_СЧЁТ=struct.unpack('>H',СОВПАД_ЗНАЧЕН(клиент,3)[1:])[0]
            for _ in range(ввод_СЧЁТ):
                координата_X,Y_координата,너비값,높이값,кодировка=struct.unpack('>HHHHi',СОВПАД_ЗНАЧЕН(клиент,12));assert кодировка==0,кодировка
                данные=СОВПАД_ЗНАЧЕН(клиент,너비값*높이값*4)
                for СТРОКА_позиция in range(높이값):
                    for СТОЛБЕЦ_позиция in range(너비값):
                        원본자료=(СТРОКА_позиция*너비값+СТОЛБЕЦ_позиция)*4;целевое_значение=((Y_координата+СТРОКА_позиция)*640+координата_X+СТОЛБЕЦ_позиция)*3
                        빛삼원색[целевое_значение:целевое_значение+3]=bytes((данные[원본자료+2],данные[원본자료+1],данные[원본자료]))
            if ввод_СЧЁТ:return 빛삼원색
    try:
        получить_письмо(b'TERMINAL READY');получить_письмо(b'jkoros-native> ',расшифровка.rfind(b'TERMINAL READY'))
        номер_порта=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',расшифровка).group(1))
        клиент=socket.create_connection(('127.0.0.1',номер_порта),timeout=10)
        assert СОВПАД_ЗНАЧЕН(клиент,12)==b'RFB 003.008\n';клиент.sendall(b'RFB 003.008\n')
        assert 1 in СОВПАД_ЗНАЧЕН(клиент,СОВПАД_ЗНАЧЕН(клиент,1)[0]);клиент.sendall(b'\x01');assert СОВПАД_ЗНАЧЕН(клиент,4)==b'\0'*4
        клиент.sendall(b'\x01');초기값=СОВПАД_ЗНАЧЕН(клиент,24);СОВПАД_ЗНАЧЕН(клиент,struct.unpack('>I',초기값[20:])[0])
        клиент.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        клиент.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in оболочка('ftpd start')
        передача_файла_контакт=ftplib.FTP();передача_файла_контакт.encoding='utf-8';передача_файла_контакт.connect('127.0.0.1',передача_файла_номер_порта,timeout=20);передача_файла_контакт.login()
        полезные_данные_данные=('GUI와 FTP 동시 использовать_ЗНАЧЕН '+Язык+' 😀\n').encode()
        передача_файла_контакт.storbinary('STOR 함께.txt',io.BytesIO(полезные_данные_данные))
        assert полезные_данные_данные.decode().strip() in оболочка('cat /함께.txt')
        ПОЛУЧЕНО_СЧЁТ=bytearray();передача_файла_контакт.retrbinary('RETR 함께.txt',ПОЛУЧЕНО_СЧЁТ.extend);assert ПОЛУЧЕНО_СЧЁТ==полезные_данные_данные;передача_файла_контакт.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        написать_Список=оболочка('ls /example')
        assert all(Название in написать_Список for Название in ('java/','c/','python/','README.md')),написать_Список
        if Язык=='java':
            пакет_манифест=json.loads((задача_корень/'build/examples/manifest.json').read_text())
            for путь,точка_входа in пакет_манифест.items():
                оболочка('cp '+путь+' /example-check.bin')
                контент_ЗНАЧЕН=bytearray();передача_файла_контакт.retrbinary('RETR example-check.bin',контент_ЗНАЧЕН.extend)
                assert len(контент_ЗНАЧЕН)==точка_входа['bytes'] and hashlib.sha256(контент_ЗНАЧЕН).hexdigest()==точка_входа['sha256'],путь
            передача_файла_контакт.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            binary=bytes(range(256))*64
            передача_файла_контакт.storbinary('STOR boundary.bin',io.BytesIO(binary))
            контент_ЗНАЧЕН=bytearray();передача_файла_контакт.retrbinary('RETR boundary.bin',контент_ЗНАЧЕН.extend)
            assert контент_ЗНАЧЕН==binary and 'boundary.bin' in передача_файла_контакт.nlst()
            оболочка('cp /boundary.bin /boundary-copy.bin')
            контент_ЗНАЧЕН=bytearray();передача_файла_контакт.retrbinary('RETR boundary-copy.bin',контент_ЗНАЧЕН.extend)
            assert контент_ЗНАЧЕН==binary
            передача_файла_контакт.delete('boundary.bin');передача_файла_контакт.delete('boundary-copy.bin')
        assert 'ПримерВывода' in оболочка('ls /example/'+Язык)
        оболочка('cd /example/'+Язык)
        имя_таблица={'java':'JAVA','c':'C','python':'PYTHON'}[Язык]
        예상파일=имя_таблица+' файл: 한글 данные 😀\n'
        if Язык=='java':
            실행('javac ПримерВывода.java','Compiled:');실행('java ПримерВывода','JAVA текстовыйВывод: 안녕하세요 😀')
            실행('javac ПримерФайла.java','Compiled:');실행('java ПримерФайла',예상파일)
            실행('java ПримерСети {} {}'.format(вывод_на_экран_сервер_ввод.TCP_порт,вывод_на_экран_сервер_ввод.UDP_порт),'JAVA 네트워크 проверять: TCP UDP 한글')
            그림명령='java ПримерРисования'
        elif Язык=='c':
            for Название,전달값,예상결과 in [('текстовыйВывод','', 'C текстовыйВывод: 안녕하세요 😀'),('файл','',예상파일),
                    ('네트워크',' '+str(вывод_на_экран_сервер_ввод.UDP_порт),'C 네트워크 проверять: UDP 한글')]:
                실행('cc '+Название+'예제.c -o 실행','Compiled native ARM64 ELF:')
                실행('./실행'+전달값,예상결과)
            실행('cc ПримерРисования.c -o 실행','Compiled native ARM64 ELF:');그림명령='./실행'
        else:
            for Название,전달값,예상결과 in [('текстовыйВывод','','PYTHON текстовыйВывод: 안녕하세요 😀'),('файл','',예상파일),
                    ('네트워크',' '+str(вывод_на_экран_сервер_ввод.UDP_порт),'PYTHON 네트워크 проверять: UDP 한글')]:
                실행('python '+Название+'예제.py'+전달값,예상결과)
            그림명령='python ПримерРисования.py'
        Пуск_рисунок=Пуск_СМЕЩ(그림명령)
        текст=получить_письмо('그림을 확인한 BACK_ЗНАЧЕН Enter를 누르세요.\r\n'.encode(),Пуск_рисунок)
        assert имя_таблица+' 그래픽: 빨강 초록 파랑' in текст and 'exit 0' not in текст,текст
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        передача_файла_контакт.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        ПОЛУЧЕНО_СЧЁТ=bytearray();передача_файла_контакт.retrbinary('RETR 도중.txt',ПОЛУЧЕНО_СЧЁТ.extend);assert ПОЛУЧЕНО_СЧЁТ==b'FTP DURING GRAPHICS';передача_файла_контакт.delete('도중.txt')
        빛삼원색=화소들()
        for Y_координата,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            СМЕЩ_ЗНАЧЕН=(Y_координата*640+610)*3;assert tuple(빛삼원색[СМЕЩ_ЗНАЧЕН:СМЕЩ_ЗНАЧЕН+3])==색상,(Язык,Y_координата,tuple(빛삼원색[СМЕЩ_ЗНАЧЕН:СМЕЩ_ЗНАЧЕН+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(KR_данные/(Язык+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in получить_письмо(b'jkoros-native> ',Пуск_рисунок)
        if Язык=='java':
            Пуск_окно=Пуск_СМЕЩ('java ПримерОкна')
            получить_письмо('GUI 예제 Подготовить: ПримерОкна'.encode(),Пуск_окно)
            def клик_ЗНАЧЕН(가로,Вертикаль_позиция):
                for кнопка in (1,0):клиент.sendall(struct.pack('>BBHH',5,кнопка,가로,Вертикаль_позиция))
            time.sleep(.3)
            Назад_фото=Image.frombytes('RGB',(640,480),bytes(화소들()))
            клик_ЗНАЧЕН(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for знак_ЗНАЧЕН in '한글':누름값(0x1000000|ord(знак_ЗНАЧЕН));누름값(0x1000000|ord(знак_ЗНАЧЕН),False)
            for повторение_СЧЁТ in (1,2):
                запустить=len(расшифровка);клик_ЗНАЧЕН(180,242)
                получить_письмо(('GUI приветствие_ae353e94: 안녕하세요, 한글님! ('+str(повторение_СЧЁТ)+')').encode(),запустить)
            time.sleep(.3)
            окно_рисунок=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert Назад_фото.crop((110,272,530,300)).tobytes()!=окно_рисунок.crop((110,272,530,300)).tobytes()
            окно_рисунок.save(str(KR_данные/'java-swing.png'))
            запустить=len(расшифровка);клик_ЗНАЧЕН(535,105)
            assert 'exit 0' in получить_письмо(b'jkoros-native> ',запустить)
        # Download the guest-created bytes through FTP in the same GUI VM.
        файл_ввод_имя={'java':'java.txt','c':'c.txt','python':'python.txt'}[Язык]
        оболочка('cp '+файл_ввод_имя+' /проверить.txt')
        ПОЛУЧЕНО_СЧЁТ=bytearray();передача_файла_контакт.retrbinary('RETR проверить.txt',ПОЛУЧЕНО_СЧЁТ.extend);assert ПОЛУЧЕНО_СЧЁТ==예상파일.encode()
        оболочка('echo preserved > ПримерВывода.'+('py' if Язык=='python' else Язык))
        assert 'EXAMPLES READY' in оболочка('example '+Язык)
        assert '\npreserved\n' in оболочка('cat ПримерВывода.'+('py' if Язык=='python' else Язык))
        assert '한/нуль_операнд Ключ_ЗНАЧЕН, Shift+Space 또는 F9' in оболочка('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in оболочка('echo GUI NETWORK TOGETHER')
        передача_файла_контакт.quit();передача_файла_контакт=None;assert 'FTP stopped' in оболочка('ftpd stop')
        print('PASS '+Язык+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if передача_файла_контакт:
            try:передача_файла_контакт.close()
            except OSError:pass
        if клиент:клиент.close()
        Процесс.terminate()
        try:Процесс.wait(timeout=8)
        except subprocess.TimeoutExpired:Процесс.kill();Процесс.wait()
        селектор.close();Процесс.stdout.close();(KR_данные/(Язык+'-serial.log')).write_bytes(расшифровка)


def запустить():
    KR_данные=задача_корень/'build/verification/examples';KR_данные.mkdir(parents=True,exist_ok=True)
    проверка_Отчет={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((задача_корень/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with вывод_на_экран_Серверы() as вывод_на_экран_сервер_ввод:
            for Язык in ('java','c','python'):
                тест_Язык(Язык,вывод_на_экран_сервер_ввод,KR_данные);проверка_Отчет['languages'].append(Язык)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert вывод_на_экран_сервер_ввод.수신됨==[(область_ЗНАЧЕН,данные.encode()) for область_ЗНАЧЕН,данные in 예상결과],вывод_на_экран_сервер_ввод.수신됨
            проверка_Отчет['host_network_payloads']=[{'protocol':область_ЗНАЧЕН,'text':данные.decode()} for область_ЗНАЧЕН,данные in вывод_на_экран_сервер_ввод.수신됨]
        проверка_Отчет.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(KR_данные/'report.json').write_text(json.dumps(проверка_Отчет,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':запустить()
