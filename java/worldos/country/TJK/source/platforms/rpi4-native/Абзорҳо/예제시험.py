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
from мизи_корӣ_намуд import 정확한값
from 예제되돌림서버 import 되돌림서버
from иҷро_кардан_фармон import 기준


def test_언어(Забон,되돌림서버항목,결과자료):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    Раванд=subprocess.Popen(['python3',str(기준/'Абзорҳо/иҷро_кардан_фармон.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    интихобкунанда=selectors.DefaultSelector();интихобкунанда.register(Раванд.stdout,selectors.EVENT_READ)
    대화기록=bytearray();муштарӣ=None;файл_интиқол_пайваст=None
    def 수신하기(확인표시,порча=0):
        анҷом_додан_Интиқолшавӣ=time.monotonic()+60
        while 확인표시 not in 대화기록[порча:]:
            if time.monotonic()>анҷом_додан_Интиқолшавӣ or Раванд.poll() is not None:raise AssertionError(대화기록[порча:].decode('utf-8','replace'))
            for 누름값,_ in интихобкунанда.select(.1):
                иттилоот=누름값.fileobj.read(65536)
                if иттилоот:대화기록.extend(иттилоот)
        return 대화기록[порча:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(аломат_қимат,누르는중=True):муштарӣ.sendall(struct.pack('>BBHI',4,int(누르는중),0,аломат_қимат))
    def Оғоз_Интиқолшавӣ(хат):
        порча=len(대화기록)
        for рамзи_аломат in хат+'\n':
            аломат_қимат=0xff0d if рамзи_аломат=='\n' else ord(рамзи_аломат) if ord(рамзи_аломат)<256 else 0x1000000|ord(рамзи_аломат)
            누름값(аломат_қимат);누름값(аломат_қимат,False)
        return порча
    def восит(хат):return 수신하기(b'jkoros-native> ',Оғоз_Интиқолшавӣ(хат))
    def иҷро_кардан_фармон(хат,예상결과):
        Матн=восит(хат);assert 예상결과 in Матн and 'exit 0' in Матн,(хат,Матн)
        return Матн
    def 화소들():
        муштарӣ.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            категория_қимат=정확한값(муштарӣ,1)[0]
            if категория_қимат==2:continue
            if категория_қимат==3:
                개수=struct.unpack('>I',정확한값(муштарӣ,7)[3:])[0];정확한값(муштарӣ,개수);continue
            assert категория_қимат==0,категория_қимат
            항목수=struct.unpack('>H',정확한값(муштарӣ,3)[1:])[0]
            for _ in range(항목수):
                координатаи_х,세로좌표,너비값,높이값,маҷмӯи_аломатҳо=struct.unpack('>HHHHi',정확한값(муштарӣ,12));assert маҷмӯи_аломатҳо==0,маҷмӯи_аломатҳо
                иттилоот=정확한값(муштарӣ,너비값*높이값*4)
                for 행위치 in range(높이값):
                    for 열위치 in range(너비값):
                        원본자료=(행위치*너비값+열위치)*4;ҳадаф=((세로좌표+행위치)*640+координатаи_х+열위치)*3
                        빛삼원색[ҳадаф:ҳадаф+3]=bytes((иттилоот[원본자료+2],иттилоот[원본자료+1],иттилоот[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        муштарӣ=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert 정확한값(муштарӣ,12)==b'RFB 003.008\n';муштарӣ.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(муштарӣ,정확한값(муштарӣ,1)[0]);муштарӣ.sendall(b'\x01');assert 정확한값(муштарӣ,4)==b'\0'*4
        муштарӣ.sendall(b'\x01');초기값=정확한값(муштарӣ,24);정확한값(муштарӣ,struct.unpack('>I',초기값[20:])[0])
        муштарӣ.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        муштарӣ.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in восит('ftpd start')
        файл_интиқол_пайваст=ftplib.FTP();файл_интиқол_пайваст.encoding='utf-8';файл_интиқол_пайваст.connect('127.0.0.1',파일전송접속번호,timeout=20);файл_интиқол_пайваст.login()
        қобилият_иттилоот=('GUI와 FTP 동시 사용 '+Забон+' 😀\n').encode()
        файл_интиқол_пайваст.storbinary('STOR 함께.txt',io.BytesIO(қобилият_иттилоот))
        assert қобилият_иттилоот.decode().strip() in восит('cat /함께.txt')
        받은수=bytearray();файл_интиқол_пайваст.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==қобилият_иттилоот;файл_интиқол_пайваст.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        фиристодан_Рӯйхат=восит('ls /example')
        assert all(Ном in фиристодан_Рӯйхат for Ном in ('java/','c/','python/','README.md')),фиристодан_Рӯйхат
        if Забон=='java':
            꾸러미명세=json.loads((기준/'build/examples/manifest.json').read_text())
            for масир,ворида_нуқта in 꾸러미명세.items():
                восит('cp '+масир+' /example-check.bin')
                Мӯҳтаво_қимат=bytearray();файл_интиқол_пайваст.retrbinary('RETR example-check.bin',Мӯҳтаво_қимат.extend)
                assert len(Мӯҳтаво_қимат)==ворида_нуқта['bytes'] and hashlib.sha256(Мӯҳтаво_қимат).hexdigest()==ворида_нуқта['sha256'],масир
            файл_интиқол_пайваст.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            дуӣ=bytes(range(256))*64
            файл_интиқол_пайваст.storbinary('STOR boundary.bin',io.BytesIO(дуӣ))
            Мӯҳтаво_қимат=bytearray();файл_интиқол_пайваст.retrbinary('RETR boundary.bin',Мӯҳтаво_қимат.extend)
            assert Мӯҳтаво_қимат==дуӣ and 'boundary.bin' in файл_интиқол_пайваст.nlst()
            восит('cp /boundary.bin /boundary-copy.bin')
            Мӯҳтаво_қимат=bytearray();файл_интиқол_пайваст.retrbinary('RETR boundary-copy.bin',Мӯҳтаво_қимат.extend)
            assert Мӯҳтаво_қимат==дуӣ
            файл_интиқол_пайваст.delete('boundary.bin');файл_интиқол_пайваст.delete('boundary-copy.bin')
        assert '출력예제' in восит('ls /example/'+Забон)
        восит('cd /example/'+Забон)
        ном_ҷадвал={'java':'JAVA','c':'C','python':'PYTHON'}[Забон]
        예상파일=ном_ҷадвал+' Файл: 한글 иттилоот 😀\n'
        if Забон=='java':
            иҷро_кардан_фармон('javac 출력예제.java','Compiled:');иҷро_кардан_фармон('java 출력예제','JAVA 출력: 안녕하세요 😀')
            иҷро_кардан_фармон('javac 파일예제.java','Compiled:');иҷро_кардан_фармон('java 파일예제',예상파일)
            иҷро_кардан_фармон('java 네트워크예제 {} {}'.format(되돌림서버항목.Протоколи_TCP_порт,되돌림서버항목.전문접속번호),'JAVA 네트워크 тасдиқ_кардан: TCP UDP 한글')
            그림명령='java 그래픽예제'
        elif Забон=='c':
            for Ном,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('Файл','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 тасдиқ_кардан: UDP 한글')]:
                иҷро_кардан_фармон('cc '+Ном+'예제.c -o иҷро_кардан_фармон','Compiled native ARM64 ELF:')
                иҷро_кардан_фармон('./иҷро_кардан_фармон'+전달값,예상결과)
            иҷро_кардан_фармон('cc 그래픽예제.c -o иҷро_кардан_фармон','Compiled native ARM64 ELF:');그림명령='./иҷро_кардан_фармон'
        else:
            for Ном,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('Файл','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 тасдиқ_кардан: UDP 한글')]:
                иҷро_кардан_фармон('python '+Ном+'예제.py'+전달값,예상결과)
            그림명령='python 그래픽예제.py'
        Оғоз_нақша=Оғоз_Интиқолшавӣ(그림명령)
        Матн=수신하기('그림을 확인한 Бозгашт_қимат Enter를 누르세요.\r\n'.encode(),Оғоз_нақша)
        assert ном_ҷадвал+' 그래픽: 빨강 초록 파랑' in Матн and 'exit 0' not in Матн,Матн
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        файл_интиқол_пайваст.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();файл_интиқол_пайваст.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';файл_интиқол_пайваст.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            Интиқолшавӣ_қимат=(세로좌표*640+610)*3;assert tuple(빛삼원색[Интиқолшавӣ_қимат:Интиқолшавӣ_қимат+3])==색상,(Забон,세로좌표,tuple(빛삼원색[Интиқолшавӣ_қимат:Интиқолшавӣ_қимат+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(결과자료/(Забон+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',Оғоз_нақша)
        if Забон=='java':
            Оғоз_равзана=Оғоз_Интиқолшавӣ('java 창예제')
            수신하기('GUI 예제 Омода_кардан: 창예제'.encode(),Оғоз_равзана)
            def зер_кардан_қимат(가로,세로):
                for тугма in (1,0):муштарӣ.sendall(struct.pack('>BBHH',5,тугма,가로,세로))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            зер_кардан_қимат(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for аломат_қимат_068c2631 in '한글':누름값(0x1000000|ord(аломат_қимат_068c2631));누름값(0x1000000|ord(аломат_қимат_068c2631),False)
            for 횟수 in (1,2):
                порча=len(대화기록);зер_кардан_қимат(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),порча)
            time.sleep(.3)
            равзана_нақша=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=равзана_нақша.crop((110,272,530,300)).tobytes()
            равзана_нақша.save(str(결과자료/'java-swing.png'))
            порча=len(대화기록);зер_кардан_қимат(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',порча)
        # Download the guest-created bytes through FTP in the same GUI VM.
        файл_ворида_ном={'java':'java.txt','c':'c.txt','python':'python.txt'}[Забон]
        восит('cp '+файл_ворида_ном+' /санҷидани_эътибор.txt')
        받은수=bytearray();файл_интиқол_пайваст.retrbinary('RETR санҷидани_эътибор.txt',받은수.extend);assert 받은수==예상파일.encode()
        восит('echo preserved > 출력예제.'+('py' if Забон=='python' else Забон))
        assert 'EXAMPLES READY' in восит('example '+Забон)
        assert '\npreserved\n' in восит('cat 출력예제.'+('py' if Забон=='python' else Забон))
        assert '한/영 калид_қимат, Shift+Space 또는 F9' in восит('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in восит('echo GUI NETWORK TOGETHER')
        файл_интиқол_пайваст.quit();файл_интиқол_пайваст=None;assert 'FTP stopped' in восит('ftpd stop')
        print('PASS '+Забон+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if файл_интиқол_пайваст:
            try:файл_интиқол_пайваст.close()
            except OSError:pass
        if муштарӣ:муштарӣ.close()
        Раванд.terminate()
        try:Раванд.wait(timeout=8)
        except subprocess.TimeoutExpired:Раванд.kill();Раванд.wait()
        интихобкунанда.close();Раванд.stdout.close();(결과자료/(Забон+'-serial.log')).write_bytes(대화기록)


def порча():
    결과자료=기준/'build/verification/examples';결과자료.mkdir(parents=True,exist_ok=True)
    санҷиши_эътибор_гузориш={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for Забон in ('java','c','python'):
                test_언어(Забон,되돌림서버항목,결과자료);санҷиши_эътибор_гузориш['languages'].append(Забон)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(категория_қимат,иттилоот.encode()) for категория_қимат,иттилоот in 예상결과],되돌림서버항목.수신됨
            санҷиши_эътибор_гузориш['host_network_payloads']=[{'protocol':категория_қимат,'text':иттилоот.decode()} for категория_қимат,иттилоот in 되돌림서버항목.수신됨]
        санҷиши_эътибор_гузориш.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(결과자료/'report.json').write_text(json.dumps(санҷиши_эътибор_гузориш,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':порча()
