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
from дэлгэц_харах import 정확한값
from 예제되돌림서버 import 되돌림서버
from Гүйцэтгэх_команд import 기준


def test_언어(Хэл,되돌림서버항목,결과자료):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    үйл_явц=subprocess.Popen(['python3',str(기준/'Хэрэгслүүд/Гүйцэтгэх_команд.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    сонгогч=selectors.DefaultSelector();сонгогч.register(үйл_явц.stdout,selectors.EVENT_READ)
    대화기록=bytearray();клиент=None;файл_дамжуулах_холболт=None
    def 수신하기(확인표시,Ажиллуулах=0):
        дуусгах_Оффсет=time.monotonic()+60
        while 확인표시 not in 대화기록[Ажиллуулах:]:
            if time.monotonic()>дуусгах_Оффсет or үйл_явц.poll() is not None:raise AssertionError(대화기록[Ажиллуулах:].decode('utf-8','replace'))
            for 누름값,_ in сонгогч.select(.1):
                өгөгдөл=누름값.fileobj.read(65536)
                if өгөгдөл:대화기록.extend(өгөгдөл)
        return 대화기록[Ажиллуулах:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(тэмдэг_утга,누르는중=True):клиент.sendall(struct.pack('>BBHI',4,int(누르는중),0,тэмдэг_утга))
    def Эхлэл_Оффсет(Шугам):
        Ажиллуулах=len(대화기록)
        for тэмдэгтийн_код in Шугам+'\n':
            тэмдэг_утга=0xff0d if тэмдэгтийн_код=='\n' else ord(тэмдэгтийн_код) if ord(тэмдэгтийн_код)<256 else 0x1000000|ord(тэмдэгтийн_код)
            누름값(тэмдэг_утга);누름값(тэмдэг_утга,False)
        return Ажиллуулах
    def бүрхүүл(Шугам):return 수신하기(b'jkoros-native> ',Эхлэл_Оффсет(Шугам))
    def Гүйцэтгэх_команд(Шугам,예상결과):
        Бичвэр=бүрхүүл(Шугам);assert 예상결과 in Бичвэр and 'exit 0' in Бичвэр,(Шугам,Бичвэр)
        return Бичвэр
    def 화소들():
        клиент.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            ангилал_утга=정확한값(клиент,1)[0]
            if ангилал_утга==2:continue
            if ангилал_утга==3:
                개수=struct.unpack('>I',정확한값(клиент,7)[3:])[0];정확한값(клиент,개수);continue
            assert ангилал_утга==0,ангилал_утга
            항목수=struct.unpack('>H',정확한값(клиент,3)[1:])[0]
            for _ in range(항목수):
                х_координат,세로좌표,너비값,높이값,тэмдэгтийн_олонлог=struct.unpack('>HHHHi',정확한값(клиент,12));assert тэмдэгтийн_олонлог==0,тэмдэгтийн_олонлог
                өгөгдөл=정확한값(клиент,너비값*높이값*4)
                for 행위치 in range(높이값):
                    for 열위치 in range(너비값):
                        원본자료=(행위치*너비값+열위치)*4;зорилго=((세로좌표+행위치)*640+х_координат+열위치)*3
                        빛삼원색[зорилго:зорилго+3]=bytes((өгөгдөл[원본자료+2],өгөгдөл[원본자료+1],өгөгдөл[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        клиент=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert 정확한값(клиент,12)==b'RFB 003.008\n';клиент.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(клиент,정확한값(клиент,1)[0]);клиент.sendall(b'\x01');assert 정확한값(клиент,4)==b'\0'*4
        клиент.sendall(b'\x01');초기값=정확한값(клиент,24);정확한값(клиент,struct.unpack('>I',초기값[20:])[0])
        клиент.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        клиент.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in бүрхүүл('ftpd start')
        файл_дамжуулах_холболт=ftplib.FTP();файл_дамжуулах_холболт.encoding='utf-8';файл_дамжуулах_холболт.connect('127.0.0.1',파일전송접속번호,timeout=20);файл_дамжуулах_холболт.login()
        ашигтай_ачаалал_өгөгдөл=('GUI와 FTP 동시 사용 '+Хэл+' 😀\n').encode()
        файл_дамжуулах_холболт.storbinary('STOR 함께.txt',io.BytesIO(ашигтай_ачаалал_өгөгдөл))
        assert ашигтай_ачаалал_өгөгдөл.decode().strip() in бүрхүүл('cat /함께.txt')
        받은수=bytearray();файл_дамжуулах_холболт.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==ашигтай_ачаалал_өгөгдөл;файл_дамжуулах_холболт.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        илгээх_Жагсаалт=бүрхүүл('ls /example')
        assert all(Нэр in илгээх_Жагсаалт for Нэр in ('java/','c/','python/','README.md')),илгээх_Жагсаалт
        if Хэл=='java':
            꾸러미명세=json.loads((기준/'build/examples/manifest.json').read_text())
            for ЗАМ,оролт_цэг in 꾸러미명세.items():
                бүрхүүл('cp '+ЗАМ+' /example-check.bin')
                Агуулга_утга=bytearray();файл_дамжуулах_холболт.retrbinary('RETR example-check.bin',Агуулга_утга.extend)
                assert len(Агуулга_утга)==оролт_цэг['bytes'] and hashlib.sha256(Агуулга_утга).hexdigest()==оролт_цэг['sha256'],ЗАМ
            файл_дамжуулах_холболт.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            хоёрт=bytes(range(256))*64
            файл_дамжуулах_холболт.storbinary('STOR boundary.bin',io.BytesIO(хоёрт))
            Агуулга_утга=bytearray();файл_дамжуулах_холболт.retrbinary('RETR boundary.bin',Агуулга_утга.extend)
            assert Агуулга_утга==хоёрт and 'boundary.bin' in файл_дамжуулах_холболт.nlst()
            бүрхүүл('cp /boundary.bin /boundary-copy.bin')
            Агуулга_утга=bytearray();файл_дамжуулах_холболт.retrbinary('RETR boundary-copy.bin',Агуулга_утга.extend)
            assert Агуулга_утга==хоёрт
            файл_дамжуулах_холболт.delete('boundary.bin');файл_дамжуулах_холболт.delete('boundary-copy.bin')
        assert '출력예제' in бүрхүүл('ls /example/'+Хэл)
        бүрхүүл('cd /example/'+Хэл)
        нэр_хүснэгт={'java':'JAVA','c':'C','python':'PYTHON'}[Хэл]
        예상파일=нэр_хүснэгт+' Файл: 한글 өгөгдөл 😀\n'
        if Хэл=='java':
            Гүйцэтгэх_команд('javac 출력예제.java','Compiled:');Гүйцэтгэх_команд('java 출력예제','JAVA 출력: 안녕하세요 😀')
            Гүйцэтгэх_команд('javac 파일예제.java','Compiled:');Гүйцэтгэх_команд('java 파일예제',예상파일)
            Гүйцэтгэх_команд('java 네트워크예제 {} {}'.format(되돌림서버항목.Дамжууллын_хяналтын_протокол_порт,되돌림서버항목.전문접속번호),'JAVA 네트워크 шалгах: TCP UDP 한글')
            그림명령='java 그래픽예제'
        elif Хэл=='c':
            for Нэр,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('Файл','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 шалгах: UDP 한글')]:
                Гүйцэтгэх_команд('cc '+Нэр+'예제.c -o Гүйцэтгэх_команд','Compiled native ARM64 ELF:')
                Гүйцэтгэх_команд('./Гүйцэтгэх_команд'+전달값,예상결과)
            Гүйцэтгэх_команд('cc 그래픽예제.c -o Гүйцэтгэх_команд','Compiled native ARM64 ELF:');그림명령='./Гүйцэтгэх_команд'
        else:
            for Нэр,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('Файл','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 шалгах: UDP 한글')]:
                Гүйцэтгэх_команд('python '+Нэр+'예제.py'+전달값,예상결과)
            그림명령='python 그래픽예제.py'
        Эхлэл_зураг=Эхлэл_Оффсет(그림명령)
        Бичвэр=수신하기('그림을 확인한 Буцах_утга Enter를 누르세요.\r\n'.encode(),Эхлэл_зураг)
        assert нэр_хүснэгт+' 그래픽: 빨강 초록 파랑' in Бичвэр and 'exit 0' not in Бичвэр,Бичвэр
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        файл_дамжуулах_холболт.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();файл_дамжуулах_холболт.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';файл_дамжуулах_холболт.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            Оффсет_утга=(세로좌표*640+610)*3;assert tuple(빛삼원색[Оффсет_утга:Оффсет_утга+3])==색상,(Хэл,세로좌표,tuple(빛삼원색[Оффсет_утга:Оффсет_утга+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(결과자료/(Хэл+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',Эхлэл_зураг)
        if Хэл=='java':
            Эхлэл_цонх=Эхлэл_Оффсет('java 창예제')
            수신하기('GUI 예제 Бэлтгэх: 창예제'.encode(),Эхлэл_цонх)
            def товших_утга(가로,세로):
                for товч in (1,0):клиент.sendall(struct.pack('>BBHH',5,товч,가로,세로))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            товших_утга(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for тэмдэгт_утга in '한글':누름값(0x1000000|ord(тэмдэгт_утга));누름값(0x1000000|ord(тэмдэгт_утга),False)
            for 횟수 in (1,2):
                Ажиллуулах=len(대화기록);товших_утга(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Ажиллуулах)
            time.sleep(.3)
            цонх_зураг=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=цонх_зураг.crop((110,272,530,300)).tobytes()
            цонх_зураг.save(str(결과자료/'java-swing.png'))
            Ажиллуулах=len(대화기록);товших_утга(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',Ажиллуулах)
        # Download the guest-created bytes through FTP in the same GUI VM.
        файл_оролт_нэр={'java':'java.txt','c':'c.txt','python':'python.txt'}[Хэл]
        бүрхүүл('cp '+файл_оролт_нэр+' /баталгаажуулах.txt')
        받은수=bytearray();файл_дамжуулах_холболт.retrbinary('RETR баталгаажуулах.txt',받은수.extend);assert 받은수==예상파일.encode()
        бүрхүүл('echo preserved > 출력예제.'+('py' if Хэл=='python' else Хэл))
        assert 'EXAMPLES READY' in бүрхүүл('example '+Хэл)
        assert '\npreserved\n' in бүрхүүл('cat 출력예제.'+('py' if Хэл=='python' else Хэл))
        assert '한/영 түлхүүр_утга, Shift+Space 또는 F9' in бүрхүүл('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in бүрхүүл('echo GUI NETWORK TOGETHER')
        файл_дамжуулах_холболт.quit();файл_дамжуулах_холболт=None;assert 'FTP stopped' in бүрхүүл('ftpd stop')
        print('PASS '+Хэл+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if файл_дамжуулах_холболт:
            try:файл_дамжуулах_холболт.close()
            except OSError:pass
        if клиент:клиент.close()
        үйл_явц.terminate()
        try:үйл_явц.wait(timeout=8)
        except subprocess.TimeoutExpired:үйл_явц.kill();үйл_явц.wait()
        сонгогч.close();үйл_явц.stdout.close();(결과자료/(Хэл+'-serial.log')).write_bytes(대화기록)


def Ажиллуулах():
    결과자료=기준/'build/verification/examples';결과자료.mkdir(parents=True,exist_ok=True)
    баталгаажуулалт_тайлан={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for Хэл in ('java','c','python'):
                test_언어(Хэл,되돌림서버항목,결과자료);баталгаажуулалт_тайлан['languages'].append(Хэл)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(ангилал_утга,өгөгдөл.encode()) for ангилал_утга,өгөгдөл in 예상결과],되돌림서버항목.수신됨
            баталгаажуулалт_тайлан['host_network_payloads']=[{'protocol':ангилал_утга,'text':өгөгдөл.decode()} for ангилал_утга,өгөгдөл in 되돌림서버항목.수신됨]
        баталгаажуулалт_тайлан.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(결과자료/'report.json').write_text(json.dumps(баталгаажуулалт_тайлан,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Ажиллуулах()
