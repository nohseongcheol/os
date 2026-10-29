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
from десктоп_Изглед import 정확한값
from 예제되돌림서버 import Ехо_Сървъри
from изпълнявам_команда import проект_корен


def test_언어(език,Ехо_сървър_запис,мярка_данни):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));прехвърляне_на_файл_номер_на_порт=임시자원.getsockname()[1]
    Процес=subprocess.Popen(['python3',str(проект_корен/'Инструменти/изпълнявам_команда.py'),'--desktop','--network','--port','0','--ftp-port',str(прехвърляне_на_файл_номер_на_порт)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    свързан_елемент_за_избор=selectors.DefaultSelector();свързан_елемент_за_избор.register(Процес.stdout,selectors.EVENT_READ)
    препис=bytearray();клиент=None;прехвърляне_на_файл_връзка=None
    def получавам_имейл(маркер,Стартиране=0):
        прекратяване_на_повикването_Изместване=time.monotonic()+60
        while маркер not in препис[Стартиране:]:
            if time.monotonic()>прекратяване_на_повикването_Изместване or Процес.poll() is not None:raise AssertionError(препис[Стартиране:].decode('utf-8','replace'))
            for 누름값,_ in свързан_елемент_за_избор.select(.1):
                данни=누름값.fileobj.read(65536)
                if данни:препис.extend(данни)
        return препис[Стартиране:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(символ_стойност,누르는중=True):клиент.sendall(struct.pack('>BBHI',4,int(누르는중),0,символ_стойност))
    def Старт_Изместване(ред):
        Стартиране=len(препис)
        for знаков_код in ред+'\n':
            символ_стойност=0xff0d if знаков_код=='\n' else ord(знаков_код) if ord(знаков_код)<256 else 0x1000000|ord(знаков_код)
            누름값(символ_стойност);누름값(символ_стойност,False)
        return Стартиране
    def обвивка(ред):return получавам_имейл(b'jkoros-native> ',Старт_Изместване(ред))
    def изпълнявам_команда(ред,예상결과):
        Текст=обвивка(ред);assert 예상결과 in Текст and 'exit 0' in Текст,(ред,Текст)
        return Текст
    def 화소들():
        клиент.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            област_стойност=정확한값(клиент,1)[0]
            if област_стойност==2:continue
            if област_стойност==3:
                개수=struct.unpack('>I',정확한값(клиент,7)[3:])[0];정확한값(клиент,개수);continue
            assert област_стойност==0,област_стойност
            항목수=struct.unpack('>H',정확한값(клиент,3)[1:])[0]
            for _ in range(항목수):
                x_координата,세로좌표,너비값,높이값,набор_символи=struct.unpack('>HHHHi',정확한값(клиент,12));assert набор_символи==0,набор_символи
                данни=정확한값(клиент,너비값*높이값*4)
                for ред_позиция in range(높이값):
                    for колона_позиция in range(너비값):
                        원본자료=(ред_позиция*너비값+колона_позиция)*4;цел=((세로좌표+ред_позиция)*640+x_координата+колона_позиция)*3
                        빛삼원색[цел:цел+3]=bytes((данни[원본자료+2],данни[원본자료+1],данни[원본자료]))
            if 항목수:return 빛삼원색
    try:
        получавам_имейл(b'TERMINAL READY');получавам_имейл(b'jkoros-native> ',препис.rfind(b'TERMINAL READY'))
        номер_на_порт=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',препис).group(1))
        клиент=socket.create_connection(('127.0.0.1',номер_на_порт),timeout=10)
        assert 정확한값(клиент,12)==b'RFB 003.008\n';клиент.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(клиент,정확한값(клиент,1)[0]);клиент.sendall(b'\x01');assert 정확한값(клиент,4)==b'\0'*4
        клиент.sendall(b'\x01');초기값=정확한값(клиент,24);정확한값(клиент,struct.unpack('>I',초기값[20:])[0])
        клиент.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        клиент.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in обвивка('ftpd start')
        прехвърляне_на_файл_връзка=ftplib.FTP();прехвърляне_на_файл_връзка.encoding='utf-8';прехвърляне_на_файл_връзка.connect('127.0.0.1',прехвърляне_на_файл_номер_на_порт,timeout=20);прехвърляне_на_файл_връзка.login()
        полезен_обем_данни=('GUI와 FTP 동시 използвам_стойност '+език+' 😀\n').encode()
        прехвърляне_на_файл_връзка.storbinary('STOR 함께.txt',io.BytesIO(полезен_обем_данни))
        assert полезен_обем_данни.decode().strip() in обвивка('cat /함께.txt')
        받은수=bytearray();прехвърляне_на_файл_връзка.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==полезен_обем_данни;прехвърляне_на_файл_връзка.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        изпращам_Списък=обвивка('ls /example')
        assert all(Име in изпращам_Списък for Име in ('java/','c/','python/','README.md')),изпращам_Списък
        if език=='java':
            пакет_манифест=json.loads((проект_корен/'build/examples/manifest.json').read_text())
            for ПЪТ,запис_пункт in пакет_манифест.items():
                обвивка('cp '+ПЪТ+' /example-check.bin')
                Съдържание_стойност=bytearray();прехвърляне_на_файл_връзка.retrbinary('RETR example-check.bin',Съдържание_стойност.extend)
                assert len(Съдържание_стойност)==запис_пункт['bytes'] and hashlib.sha256(Съдържание_стойност).hexdigest()==запис_пункт['sha256'],ПЪТ
            прехвърляне_на_файл_връзка.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            двоичен=bytes(range(256))*64
            прехвърляне_на_файл_връзка.storbinary('STOR boundary.bin',io.BytesIO(двоичен))
            Съдържание_стойност=bytearray();прехвърляне_на_файл_връзка.retrbinary('RETR boundary.bin',Съдържание_стойност.extend)
            assert Съдържание_стойност==двоичен and 'boundary.bin' in прехвърляне_на_файл_връзка.nlst()
            обвивка('cp /boundary.bin /boundary-copy.bin')
            Съдържание_стойност=bytearray();прехвърляне_на_файл_връзка.retrbinary('RETR boundary-copy.bin',Съдържание_стойност.extend)
            assert Съдържание_стойност==двоичен
            прехвърляне_на_файл_връзка.delete('boundary.bin');прехвърляне_на_файл_връзка.delete('boundary-copy.bin')
        assert '출력예제' in обвивка('ls /example/'+език)
        обвивка('cd /example/'+език)
        препратка_към_клетка_таблица={'java':'JAVA','c':'C','python':'PYTHON'}[език]
        예상파일=препратка_към_клетка_таблица+' Файл: 한글 данни 😀\n'
        if език=='java':
            изпълнявам_команда('javac 출력예제.java','Compiled:');изпълнявам_команда('java 출력예제','JAVA Изход: 안녕하세요 😀')
            изпълнявам_команда('javac 파일예제.java','Compiled:');изпълнявам_команда('java 파일예제',예상파일)
            изпълнявам_команда('java 네트워크예제 {} {}'.format(Ехо_сървър_запис.연결접속번호,Ехо_сървър_запис.전문접속번호),'JAVA 네트워크 проверявам: TCP UDP 한글')
            графични_елементи_команда='java 그래픽예제'
        elif език=='c':
            for Име,전달값,예상결과 in [('Изход','', 'C Изход: 안녕하세요 😀'),('Файл','',예상파일),
                    ('네트워크',' '+str(Ехо_сървър_запис.전문접속번호),'C 네트워크 проверявам: UDP 한글')]:
                изпълнявам_команда('cc '+Име+'예제.c -o изпълнявам_команда','Compiled native ARM64 ELF:')
                изпълнявам_команда('./изпълнявам_команда'+전달값,예상결과)
            изпълнявам_команда('cc 그래픽예제.c -o изпълнявам_команда','Compiled native ARM64 ELF:');графични_елементи_команда='./изпълнявам_команда'
        else:
            for Име,전달값,예상결과 in [('Изход','','PYTHON Изход: 안녕하세요 😀'),('Файл','',예상파일),
                    ('네트워크',' '+str(Ехо_сървър_запис.전문접속번호),'PYTHON 네트워크 проверявам: UDP 한글')]:
                изпълнявам_команда('python '+Име+'예제.py'+전달값,예상결과)
            графични_елементи_команда='python 그래픽예제.py'
        Старт_чертеж=Старт_Изместване(графични_елементи_команда)
        Текст=получавам_имейл('그림을 확인한 НАЗАД_стойност Enter를 누르세요.\r\n'.encode(),Старт_чертеж)
        assert препратка_към_клетка_таблица+' 그래픽: 빨강 초록 파랑' in Текст and 'exit 0' not in Текст,Текст
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        прехвърляне_на_файл_връзка.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();прехвърляне_на_файл_връзка.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';прехвърляне_на_файл_връзка.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            Изместване_стойност=(세로좌표*640+610)*3;assert tuple(빛삼원색[Изместване_стойност:Изместване_стойност+3])==색상,(език,세로좌표,tuple(빛삼원색[Изместване_стойност:Изместване_стойност+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(мярка_данни/(език+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in получавам_имейл(b'jkoros-native> ',Старт_чертеж)
        if език=='java':
            Старт_прозорец=Старт_Изместване('java 창예제')
            получавам_имейл('GUI 예제 Подготвяне: 창예제'.encode(),Старт_прозорец)
            def кликвам_стойност(가로,вертикал_позиция):
                for бутон in (1,0):клиент.sendall(struct.pack('>BBHH',5,бутон,가로,вертикал_позиция))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            кликвам_стойност(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for знак_стойност in '한글':누름값(0x1000000|ord(знак_стойност));누름값(0x1000000|ord(знак_стойност),False)
            for 횟수 in (1,2):
                Стартиране=len(препис);кликвам_стойност(180,242)
                получавам_имейл(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Стартиране)
            time.sleep(.3)
            прозорец_чертеж=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=прозорец_чертеж.crop((110,272,530,300)).tobytes()
            прозорец_чертеж.save(str(мярка_данни/'java-swing.png'))
            Стартиране=len(препис);кликвам_стойност(535,105)
            assert 'exit 0' in получавам_имейл(b'jkoros-native> ',Стартиране)
        # Download the guest-created bytes through FTP in the same GUI VM.
        Файл_запис_препратка_към_клетка={'java':'java.txt','c':'c.txt','python':'python.txt'}[език]
        обвивка('cp '+Файл_запис_препратка_към_клетка+' /проверка.txt')
        받은수=bytearray();прехвърляне_на_файл_връзка.retrbinary('RETR проверка.txt',받은수.extend);assert 받은수==예상파일.encode()
        обвивка('echo preserved > 출력예제.'+('py' if език=='python' else език))
        assert 'EXAMPLES READY' in обвивка('example '+език)
        assert '\npreserved\n' in обвивка('cat 출력예제.'+('py' if език=='python' else език))
        assert '한/нула_операнд Ключ_стойност, Shift+Space 또는 F9' in обвивка('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in обвивка('echo GUI NETWORK TOGETHER')
        прехвърляне_на_файл_връзка.quit();прехвърляне_на_файл_връзка=None;assert 'FTP stopped' in обвивка('ftpd stop')
        print('PASS '+език+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if прехвърляне_на_файл_връзка:
            try:прехвърляне_на_файл_връзка.close()
            except OSError:pass
        if клиент:клиент.close()
        Процес.terminate()
        try:Процес.wait(timeout=8)
        except subprocess.TimeoutExpired:Процес.kill();Процес.wait()
        свързан_елемент_за_избор.close();Процес.stdout.close();(мярка_данни/(език+'-serial.log')).write_bytes(препис)


def Стартиране():
    мярка_данни=проект_корен/'build/verification/examples';мярка_данни.mkdir(parents=True,exist_ok=True)
    проверка_отчет={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((проект_корен/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with Ехо_Сървъри() as Ехо_сървър_запис:
            for език in ('java','c','python'):
                test_언어(език,Ехо_сървър_запис,мярка_данни);проверка_отчет['languages'].append(език)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert Ехо_сървър_запис.수신됨==[(област_стойност,данни.encode()) for област_стойност,данни in 예상결과],Ехо_сървър_запис.수신됨
            проверка_отчет['host_network_payloads']=[{'protocol':област_стойност,'text':данни.decode()} for област_стойност,данни in Ехо_сървър_запис.수신됨]
        проверка_отчет.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(мярка_данни/'report.json').write_text(json.dumps(проверка_отчет,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Стартиране()
