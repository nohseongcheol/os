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
from десктоп_Приказ import 정확한값
from 예제되돌림서버 import 되돌림서버
from Изврши_команда import пројектовати_корен


def test_언어(Језик,되돌림서버항목,мера_подаци):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));фајл_пренос_број_порта=임시자원.getsockname()[1]
    Процес=subprocess.Popen(['python3',str(пројектовати_корен/'Алатке/Изврши_команда.py'),'--desktop','--network','--port','0','--ftp-port',str(фајл_пренос_број_порта)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    бирач=selectors.DefaultSelector();бирач.register(Процес.stdout,selectors.EVENT_READ)
    транскрипт=bytearray();клијент=None;фајл_пренос_веза=None
    def 수신하기(확인표시,Покрени=0):
        завршити_Помак=time.monotonic()+60
        while 확인표시 not in транскрипт[Покрени:]:
            if time.monotonic()>завршити_Помак or Процес.poll() is not None:raise AssertionError(транскрипт[Покрени:].decode('utf-8','replace'))
            for 누름값,_ in бирач.select(.1):
                подаци=누름값.fileobj.read(65536)
                if подаци:транскрипт.extend(подаци)
        return транскрипт[Покрени:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(симбол_вриједност,누르는중=True):клијент.sendall(struct.pack('>BBHI',4,int(누르는중),0,симбол_вриједност))
    def Старт_Помак(Ред):
        Покрени=len(транскрипт)
        for кôд_знака in Ред+'\n':
            симбол_вриједност=0xff0d if кôд_знака=='\n' else ord(кôд_знака) if ord(кôд_знака)<256 else 0x1000000|ord(кôд_знака)
            누름값(симбол_вриједност);누름값(симбол_вриједност,False)
        return Покрени
    def љуска(Ред):return 수신하기(b'jkoros-native> ',Старт_Помак(Ред))
    def Изврши_команда(Ред,예상결과):
        Текст=љуска(Ред);assert 예상결과 in Текст and 'exit 0' in Текст,(Ред,Текст)
        return Текст
    def 화소들():
        клијент.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            област_вриједност=정확한값(клијент,1)[0]
            if област_вриједност==2:continue
            if област_вриједност==3:
                개수=struct.unpack('>I',정확한값(клијент,7)[3:])[0];정확한값(клијент,개수);continue
            assert област_вриједност==0,област_вриједност
            항목수=struct.unpack('>H',정확한값(клијент,3)[1:])[0]
            for _ in range(항목수):
                x_координата,дугме_Y_координата,너비값,높이값,скуп_знакова=struct.unpack('>HHHHi',정확한값(клијент,12));assert скуп_знакова==0,скуп_знакова
                подаци=정확한값(клијент,너비값*높이값*4)
                for ред_позиција in range(높이값):
                    for колона_позиција in range(너비값):
                        원본자료=(ред_позиција*너비값+колона_позиција)*4;циљ=((дугме_Y_координата+ред_позиција)*640+x_координата+колона_позиција)*3
                        빛삼원색[циљ:циљ+3]=bytes((подаци[원본자료+2],подаци[원본자료+1],подаци[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',транскрипт.rfind(b'TERMINAL READY'))
        број_порта=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',транскрипт).group(1))
        клијент=socket.create_connection(('127.0.0.1',број_порта),timeout=10)
        assert 정확한값(клијент,12)==b'RFB 003.008\n';клијент.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(клијент,정확한값(клијент,1)[0]);клијент.sendall(b'\x01');assert 정확한값(клијент,4)==b'\0'*4
        клијент.sendall(b'\x01');초기값=정확한값(клијент,24);정확한값(клијент,struct.unpack('>I',초기값[20:])[0])
        клијент.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        клијент.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in љуска('ftpd start')
        фајл_пренос_веза=ftplib.FTP();фајл_пренос_веза.encoding='utf-8';фајл_пренос_веза.connect('127.0.0.1',фајл_пренос_број_порта,timeout=20);фајл_пренос_веза.login()
        корисни_подаци_подаци=('GUI와 FTP 동시 사용 '+Језик+' 😀\n').encode()
        фајл_пренос_веза.storbinary('STOR 함께.txt',io.BytesIO(корисни_подаци_подаци))
        assert корисни_подаци_подаци.decode().strip() in љуска('cat /함께.txt')
        받은수=bytearray();фајл_пренос_веза.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==корисни_подаци_подаци;фајл_пренос_веза.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        послати_Листа=љуска('ls /example')
        assert all(Назив in послати_Листа for Назив in ('java/','c/','python/','README.md')),послати_Листа
        if Језик=='java':
            꾸러미명세=json.loads((пројектовати_корен/'build/examples/manifest.json').read_text())
            for ПУТАЊА,унос_поен in 꾸러미명세.items():
                љуска('cp '+ПУТАЊА+' /example-check.bin')
                Садржај_вриједност=bytearray();фајл_пренос_веза.retrbinary('RETR example-check.bin',Садржај_вриједност.extend)
                assert len(Садржај_вриједност)==унос_поен['bytes'] and hashlib.sha256(Садржај_вриједност).hexdigest()==унос_поен['sha256'],ПУТАЊА
            фајл_пренос_веза.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            бинарно=bytes(range(256))*64
            фајл_пренос_веза.storbinary('STOR boundary.bin',io.BytesIO(бинарно))
            Садржај_вриједност=bytearray();фајл_пренос_веза.retrbinary('RETR boundary.bin',Садржај_вриједност.extend)
            assert Садржај_вриједност==бинарно and 'boundary.bin' in фајл_пренос_веза.nlst()
            љуска('cp /boundary.bin /boundary-copy.bin')
            Садржај_вриједност=bytearray();фајл_пренос_веза.retrbinary('RETR boundary-copy.bin',Садржај_вриједност.extend)
            assert Садржај_вриједност==бинарно
            фајл_пренос_веза.delete('boundary.bin');фајл_пренос_веза.delete('boundary-copy.bin')
        assert '출력예제' in љуска('ls /example/'+Језик)
        љуска('cd /example/'+Језик)
        име_табела={'java':'JAVA','c':'C','python':'PYTHON'}[Језик]
        예상파일=име_табела+' Датотека: 한글 подаци 😀\n'
        if Језик=='java':
            Изврши_команда('javac 출력예제.java','Compiled:');Изврши_команда('java 출력예제','JAVA Излаз: 안녕하세요 😀')
            Изврши_команда('javac 파일예제.java','Compiled:');Изврши_команда('java 파일예제',예상파일)
            Изврши_команда('java 네트워크예제 {} {}'.format(되돌림서버항목.연결접속번호,되돌림서버항목.전문접속번호),'JAVA 네트워크 потврдити: TCP UDP 한글')
            графика_команда='java 그래픽예제'
        elif Језик=='c':
            for Назив,전달값,예상결과 in [('Излаз','', 'C Излаз: 안녕하세요 😀'),('Датотека','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 потврдити: UDP 한글')]:
                Изврши_команда('cc '+Назив+'예제.c -o Изврши_команда','Compiled native ARM64 ELF:')
                Изврши_команда('./Изврши_команда'+전달값,예상결과)
            Изврши_команда('cc 그래픽예제.c -o Изврши_команда','Compiled native ARM64 ELF:');графика_команда='./Изврши_команда'
        else:
            for Назив,전달값,예상결과 in [('Излаз','','PYTHON Излаз: 안녕하세요 😀'),('Датотека','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 потврдити: UDP 한글')]:
                Изврши_команда('python '+Назив+'예제.py'+전달값,예상결과)
            графика_команда='python 그래픽예제.py'
        Старт_цртеж=Старт_Помак(графика_команда)
        Текст=수신하기('그림을 확인한 НАЗАД_вриједност Enter를 누르세요.\r\n'.encode(),Старт_цртеж)
        assert име_табела+' 그래픽: 빨강 초록 파랑' in Текст and 'exit 0' not in Текст,Текст
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        фајл_пренос_веза.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();фајл_пренос_веза.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';фајл_пренос_веза.delete('도중.txt')
        빛삼원색=화소들()
        for дугме_Y_координата,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            Помак_вриједност=(дугме_Y_координата*640+610)*3;assert tuple(빛삼원색[Помак_вриједност:Помак_вриједност+3])==색상,(Језик,дугме_Y_координата,tuple(빛삼원색[Помак_вриједност:Помак_вриједност+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(мера_подаци/(Језик+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',Старт_цртеж)
        if Језик=='java':
            Старт_прозор=Старт_Помак('java 창예제')
            수신하기('GUI 예제 Припремити: 창예제'.encode(),Старт_прозор)
            def клик_вриједност(가로,вертикала_позиција):
                for дугме in (1,0):клијент.sendall(struct.pack('>BBHH',5,дугме,가로,вертикала_позиција))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            клик_вриједност(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for знак_вриједност in '한글':누름값(0x1000000|ord(знак_вриједност));누름값(0x1000000|ord(знак_вриједност),False)
            for 횟수 in (1,2):
                Покрени=len(транскрипт);клик_вриједност(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Покрени)
            time.sleep(.3)
            прозор_цртеж=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=прозор_цртеж.crop((110,272,530,300)).tobytes()
            прозор_цртеж.save(str(мера_подаци/'java-swing.png'))
            Покрени=len(транскрипт);клик_вриједност(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',Покрени)
        # Download the guest-created bytes through FTP in the same GUI VM.
        фајл_унос_име={'java':'java.txt','c':'c.txt','python':'python.txt'}[Језик]
        љуска('cp '+фајл_унос_име+' /потврдити_5fb2b747.txt')
        받은수=bytearray();фајл_пренос_веза.retrbinary('RETR потврдити_5fb2b747.txt',받은수.extend);assert 받은수==예상파일.encode()
        љуска('echo preserved > 출력예제.'+('py' if Језик=='python' else Језик))
        assert 'EXAMPLES READY' in љуска('example '+Језик)
        assert '\npreserved\n' in љуска('cat 출력예제.'+('py' if Језик=='python' else Језик))
        assert '한/영 Кључ_вриједност, Shift+Space 또는 F9' in љуска('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in љуска('echo GUI NETWORK TOGETHER')
        фајл_пренос_веза.quit();фајл_пренос_веза=None;assert 'FTP stopped' in љуска('ftpd stop')
        print('PASS '+Језик+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if фајл_пренос_веза:
            try:фајл_пренос_веза.close()
            except OSError:pass
        if клијент:клијент.close()
        Процес.terminate()
        try:Процес.wait(timeout=8)
        except subprocess.TimeoutExpired:Процес.kill();Процес.wait()
        бирач.close();Процес.stdout.close();(мера_подаци/(Језик+'-serial.log')).write_bytes(транскрипт)


def Покрени():
    мера_подаци=пројектовати_корен/'build/verification/examples';мера_подаци.mkdir(parents=True,exist_ok=True)
    провјера_извештај={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((пројектовати_корен/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for Језик in ('java','c','python'):
                test_언어(Језик,되돌림서버항목,мера_подаци);провјера_извештај['languages'].append(Језик)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(област_вриједност,подаци.encode()) for област_вриједност,подаци in 예상결과],되돌림서버항목.수신됨
            провјера_извештај['host_network_payloads']=[{'protocol':област_вриједност,'text':подаци.decode()} for област_вриједност,подаци in 되돌림서버항목.수신됨]
        провјера_извештај.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(мера_подаци/'report.json').write_text(json.dumps(провјера_извештај,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Покрени()
