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
from иш_такта_көрүү import 정확한값
from 예제되돌림서버 import 되돌림서버
from аткаруу_буйрук import 기준


def test_언어(Тил,되돌림서버항목,결과자료):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    Процесси=subprocess.Popen(['python3',str(기준/'Куралдар/аткаруу_буйрук.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    селектор=selectors.DefaultSelector();селектор.register(Процесси.stdout,selectors.EVENT_READ)
    대화기록=bytearray();керектөөчү=None;файл_ташүү_туташуу=None
    def 수신하기(확인표시,Жүргүзүү=0):
        аяктоо_Жылбышуу=time.monotonic()+60
        while 확인표시 not in 대화기록[Жүргүзүү:]:
            if time.monotonic()>аяктоо_Жылбышуу or Процесси.poll() is not None:raise AssertionError(대화기록[Жүргүзүү:].decode('utf-8','replace'))
            for 누름값,_ in селектор.select(.1):
                берилмелер=누름값.fileobj.read(65536)
                if берилмелер:대화기록.extend(берилмелер)
        return 대화기록[Жүргүзүү:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(символ_маани,누르는중=True):керектөөчү.sendall(struct.pack('>BBHI',4,int(누르는중),0,символ_маани))
    def Баштоо_Жылбышуу(сап):
        Жүргүзүү=len(대화기록)
        for символ_коду in сап+'\n':
            символ_маани=0xff0d if символ_коду=='\n' else ord(символ_коду) if ord(символ_коду)<256 else 0x1000000|ord(символ_коду)
            누름값(символ_маани);누름값(символ_маани,False)
        return Жүргүзүү
    def сырты(сап):return 수신하기(b'jkoros-native> ',Баштоо_Жылбышуу(сап))
    def аткаруу_буйрук(сап,예상결과):
        Текст=сырты(сап);assert 예상결과 in Текст and 'exit 0' in Текст,(сап,Текст)
        return Текст
    def 화소들():
        керектөөчү.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            категория_маани=정확한값(керектөөчү,1)[0]
            if категория_маани==2:continue
            if категория_маани==3:
                개수=struct.unpack('>I',정확한값(керектөөчү,7)[3:])[0];정확한값(керектөөчү,개수);continue
            assert категория_маани==0,категория_маани
            항목수=struct.unpack('>H',정확한값(керектөөчү,3)[1:])[0]
            for _ in range(항목수):
                x_координата,세로좌표,너비값,높이값,символдор_тобу=struct.unpack('>HHHHi',정확한값(керектөөчү,12));assert символдор_тобу==0,символдор_тобу
                берилмелер=정확한값(керектөөчү,너비값*높이값*4)
                for 행위치 in range(높이값):
                    for 열위치 in range(너비값):
                        원본자료=(행위치*너비값+열위치)*4;максат=((세로좌표+행위치)*640+x_координата+열위치)*3
                        빛삼원색[максат:максат+3]=bytes((берилмелер[원본자료+2],берилмелер[원본자료+1],берилмелер[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        керектөөчү=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert 정확한값(керектөөчү,12)==b'RFB 003.008\n';керектөөчү.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(керектөөчү,정확한값(керектөөчү,1)[0]);керектөөчү.sendall(b'\x01');assert 정확한값(керектөөчү,4)==b'\0'*4
        керектөөчү.sendall(b'\x01');초기값=정확한값(керектөөчү,24);정확한값(керектөөчү,struct.unpack('>I',초기값[20:])[0])
        керектөөчү.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        керектөөчү.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in сырты('ftpd start')
        файл_ташүү_туташуу=ftplib.FTP();файл_ташүү_туташуу.encoding='utf-8';файл_ташүү_туташуу.connect('127.0.0.1',파일전송접속번호,timeout=20);файл_ташүү_туташуу.login()
        керектүү_жүктөө_ченеми_берилмелер=('GUI와 FTP 동시 사용 '+Тил+' 😀\n').encode()
        файл_ташүү_туташуу.storbinary('STOR 함께.txt',io.BytesIO(керектүү_жүктөө_ченеми_берилмелер))
        assert керектүү_жүктөө_ченеми_берилмелер.decode().strip() in сырты('cat /함께.txt')
        받은수=bytearray();файл_ташүү_туташуу.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==керектүү_жүктөө_ченеми_берилмелер;файл_ташүү_туташуу.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        жөнөтүү_Тизме=сырты('ls /example')
        assert all(Аты in жөнөтүү_Тизме for Аты in ('java/','c/','python/','README.md')),жөнөтүү_Тизме
        if Тил=='java':
            꾸러미명세=json.loads((기준/'build/examples/manifest.json').read_text())
            for ЖОЛ,киргизме_жазуу_упай in 꾸러미명세.items():
                сырты('cp '+ЖОЛ+' /example-check.bin')
                Мазмун_маани=bytearray();файл_ташүү_туташуу.retrbinary('RETR example-check.bin',Мазмун_маани.extend)
                assert len(Мазмун_маани)==киргизме_жазуу_упай['bytes'] and hashlib.sha256(Мазмун_маани).hexdigest()==киргизме_жазуу_упай['sha256'],ЖОЛ
            файл_ташүү_туташуу.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            экилик=bytes(range(256))*64
            файл_ташүү_туташуу.storbinary('STOR boundary.bin',io.BytesIO(экилик))
            Мазмун_маани=bytearray();файл_ташүү_туташуу.retrbinary('RETR boundary.bin',Мазмун_маани.extend)
            assert Мазмун_маани==экилик and 'boundary.bin' in файл_ташүү_туташуу.nlst()
            сырты('cp /boundary.bin /boundary-copy.bin')
            Мазмун_маани=bytearray();файл_ташүү_туташуу.retrbinary('RETR boundary-copy.bin',Мазмун_маани.extend)
            assert Мазмун_маани==экилик
            файл_ташүү_туташуу.delete('boundary.bin');файл_ташүү_туташуу.delete('boundary-copy.bin')
        assert '출력예제' in сырты('ls /example/'+Тил)
        сырты('cd /example/'+Тил)
        аты_жадыбал={'java':'JAVA','c':'C','python':'PYTHON'}[Тил]
        예상파일=аты_жадыбал+' Файл: 한글 берилмелер 😀\n'
        if Тил=='java':
            аткаруу_буйрук('javac 출력예제.java','Compiled:');аткаруу_буйрук('java 출력예제','JAVA Чыгыш: 안녕하세요 😀')
            аткаруу_буйрук('javac 파일예제.java','Compiled:');аткаруу_буйрук('java 파일예제',예상파일)
            аткаруу_буйрук('java 네트워크예제 {} {}'.format(되돌림서버항목.TCP_протоколу_порт,되돌림서버항목.전문접속번호),'JAVA 네트워크 тууралыгын_аныктоо: TCP UDP 한글')
            그림명령='java 그래픽예제'
        elif Тил=='c':
            for Аты,전달값,예상결과 in [('Чыгыш','', 'C Чыгыш: 안녕하세요 😀'),('Файл','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 тууралыгын_аныктоо: UDP 한글')]:
                аткаруу_буйрук('cc '+Аты+'예제.c -o аткаруу_буйрук','Compiled native ARM64 ELF:')
                аткаруу_буйрук('./аткаруу_буйрук'+전달값,예상결과)
            аткаруу_буйрук('cc 그래픽예제.c -o аткаруу_буйрук','Compiled native ARM64 ELF:');그림명령='./аткаруу_буйрук'
        else:
            for Аты,전달값,예상결과 in [('Чыгыш','','PYTHON Чыгыш: 안녕하세요 😀'),('Файл','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 тууралыгын_аныктоо: UDP 한글')]:
                аткаруу_буйрук('python '+Аты+'예제.py'+전달값,예상결과)
            그림명령='python 그래픽예제.py'
        Баштоо_чийүү=Баштоо_Жылбышуу(그림명령)
        Текст=수신하기('그림을 확인한 Артка_маани Enter를 누르세요.\r\n'.encode(),Баштоо_чийүү)
        assert аты_жадыбал+' 그래픽: 빨강 초록 파랑' in Текст and 'exit 0' not in Текст,Текст
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        файл_ташүү_туташуу.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();файл_ташүү_туташуу.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';файл_ташүү_туташуу.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            Жылбышуу_маани=(세로좌표*640+610)*3;assert tuple(빛삼원색[Жылбышуу_маани:Жылбышуу_маани+3])==색상,(Тил,세로좌표,tuple(빛삼원색[Жылбышуу_маани:Жылбышуу_маани+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(결과자료/(Тил+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',Баштоо_чийүү)
        if Тил=='java':
            Баштоо_терезе=Баштоо_Жылбышуу('java 창예제')
            수신하기('GUI 예제 Даярдоо: 창예제'.encode(),Баштоо_терезе)
            def баскылоо_маани(가로,세로):
                for баскыч in (1,0):керектөөчү.sendall(struct.pack('>BBHH',5,баскыч,가로,세로))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            баскылоо_маани(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for символ_маани_068c2631 in '한글':누름값(0x1000000|ord(символ_маани_068c2631));누름값(0x1000000|ord(символ_маани_068c2631),False)
            for 횟수 in (1,2):
                Жүргүзүү=len(대화기록);баскылоо_маани(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Жүргүзүү)
            time.sleep(.3)
            терезе_чийүү=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=терезе_чийүү.crop((110,272,530,300)).tobytes()
            терезе_чийүү.save(str(결과자료/'java-swing.png'))
            Жүргүзүү=len(대화기록);баскылоо_маани(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',Жүргүзүү)
        # Download the guest-created bytes through FTP in the same GUI VM.
        файл_киргизме_жазуу_аты={'java':'java.txt','c':'c.txt','python':'python.txt'}[Тил]
        сырты('cp '+файл_киргизме_жазуу_аты+' /жарактуулугун_текшерүү.txt')
        받은수=bytearray();файл_ташүү_туташуу.retrbinary('RETR жарактуулугун_текшерүү.txt',받은수.extend);assert 받은수==예상파일.encode()
        сырты('echo preserved > 출력예제.'+('py' if Тил=='python' else Тил))
        assert 'EXAMPLES READY' in сырты('example '+Тил)
        assert '\npreserved\n' in сырты('cat 출력예제.'+('py' if Тил=='python' else Тил))
        assert '한/영 ачкыч_маани, Shift+Space 또는 F9' in сырты('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in сырты('echo GUI NETWORK TOGETHER')
        файл_ташүү_туташуу.quit();файл_ташүү_туташуу=None;assert 'FTP stopped' in сырты('ftpd stop')
        print('PASS '+Тил+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if файл_ташүү_туташуу:
            try:файл_ташүү_туташуу.close()
            except OSError:pass
        if керектөөчү:керектөөчү.close()
        Процесси.terminate()
        try:Процесси.wait(timeout=8)
        except subprocess.TimeoutExpired:Процесси.kill();Процесси.wait()
        селектор.close();Процесси.stdout.close();(결과자료/(Тил+'-serial.log')).write_bytes(대화기록)


def Жүргүзүү():
    결과자료=기준/'build/verification/examples';결과자료.mkdir(parents=True,exist_ok=True)
    ырастоо_отчет={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for Тил in ('java','c','python'):
                test_언어(Тил,되돌림서버항목,결과자료);ырастоо_отчет['languages'].append(Тил)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(категория_маани,берилмелер.encode()) for категория_маани,берилмелер in 예상결과],되돌림서버항목.수신됨
            ырастоо_отчет['host_network_payloads']=[{'protocol':категория_маани,'text':берилмелер.decode()} for категория_маани,берилмелер in 되돌림서버항목.수신됨]
        ырастоо_отчет.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(결과자료/'report.json').write_text(json.dumps(ырастоо_отчет,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Жүргүзүү()
