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
from ڊيسڪٽاپ_منظر import 정확한값
from 예제되돌림서버 import 되돌림서버
from تعميل_ڪرڻ_حڪم import 기준


def test_언어(ٻولي,되돌림서버항목,결과자료):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    عمل_a7054519=subprocess.Popen(['python3',str(기준/'اوزار/تعميل_ڪرڻ_حڪم.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    چونڊيندڙ=selectors.DefaultSelector();چونڊيندڙ.register(عمل_a7054519.stdout,selectors.EVENT_READ)
    대화기록=bytearray();گراهڪ=None;فائل_منتقلي_ڪنيڪشن=None
    def 수신하기(확인표시,هلائڻ=0):
        ختم_ڪريو_آف_سيٽ=time.monotonic()+60
        while 확인표시 not in 대화기록[هلائڻ:]:
            if time.monotonic()>ختم_ڪريو_آف_سيٽ or عمل_a7054519.poll() is not None:raise AssertionError(대화기록[هلائڻ:].decode('utf-8','replace'))
            for 누름값,_ in چونڊيندڙ.select(.1):
                ڪوائف=누름값.fileobj.read(65536)
                if ڪوائف:대화기록.extend(ڪوائف)
        return 대화기록[هلائڻ:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(نشاني_قدر,누르는중=True):گراهڪ.sendall(struct.pack('>BBHI',4,int(누르는중),0,نشاني_قدر))
    def شروع_آف_سيٽ(لڪير):
        هلائڻ=len(대화기록)
        for ڪئريڪٽر_ڪوڊ in لڪير+'\n':
            نشاني_قدر=0xff0d if ڪئريڪٽر_ڪوڊ=='\n' else ord(ڪئريڪٽر_ڪوڊ) if ord(ڪئريڪٽر_ڪوڊ)<256 else 0x1000000|ord(ڪئريڪٽر_ڪوڊ)
            누름값(نشاني_قدر);누름값(نشاني_قدر,False)
        return هلائڻ
    def شيل(لڪير):return 수신하기(b'jkoros-native> ',شروع_آف_سيٽ(لڪير))
    def تعميل_ڪرڻ_حڪم(لڪير,예상결과):
        متن=شيل(لڪير);assert 예상결과 in متن and 'exit 0' in متن,(لڪير,متن)
        return متن
    def 화소들():
        گراهڪ.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            قسم_قدر_4b6d6445=정확한값(گراهڪ,1)[0]
            if قسم_قدر_4b6d6445==2:continue
            if قسم_قدر_4b6d6445==3:
                개수=struct.unpack('>I',정확한값(گراهڪ,7)[3:])[0];정확한값(گراهڪ,개수);continue
            assert قسم_قدر_4b6d6445==0,قسم_قدر_4b6d6445
            항목수=struct.unpack('>H',정확한값(گراهڪ,3)[1:])[0]
            for _ in range(항목수):
                x_رطبو,세로좌표,너비값,높이값,ڪيريڪٽرن_جو_سيٽ=struct.unpack('>HHHHi',정확한값(گراهڪ,12));assert ڪيريڪٽرن_جو_سيٽ==0,ڪيريڪٽرن_جو_سيٽ
                ڪوائف=정확한값(گراهڪ,너비값*높이값*4)
                for 행위치 in range(높이값):
                    for 열위치 in range(너비값):
                        원본자료=(행위치*너비값+열위치)*4;هدف=((세로좌표+행위치)*640+x_رطبو+열위치)*3
                        빛삼원색[هدف:هدف+3]=bytes((ڪوائف[원본자료+2],ڪوائف[원본자료+1],ڪوائف[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        گراهڪ=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert 정확한값(گراهڪ,12)==b'RFB 003.008\n';گراهڪ.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(گراهڪ,정확한값(گراهڪ,1)[0]);گراهڪ.sendall(b'\x01');assert 정확한값(گراهڪ,4)==b'\0'*4
        گراهڪ.sendall(b'\x01');초기값=정확한값(گراهڪ,24);정확한값(گراهڪ,struct.unpack('>I',초기값[20:])[0])
        گراهڪ.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        گراهڪ.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in شيل('ftpd start')
        فائل_منتقلي_ڪنيڪشن=ftplib.FTP();فائل_منتقلي_ڪنيڪشن.encoding='utf-8';فائل_منتقلي_ڪنيڪشن.connect('127.0.0.1',파일전송접속번호,timeout=20);فائل_منتقلي_ڪنيڪشن.login()
        بنيادي_بار_ڪوائف=('GUI와 FTP 동시 사용 '+ٻولي+' 😀\n').encode()
        فائل_منتقلي_ڪنيڪشن.storbinary('STOR 함께.txt',io.BytesIO(بنيادي_بار_ڪوائف))
        assert بنيادي_بار_ڪوائف.decode().strip() in شيل('cat /함께.txt')
        받은수=bytearray();فائل_منتقلي_ڪنيڪشن.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==بنيادي_بار_ڪوائف;فائل_منتقلي_ڪنيڪشن.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        اي_ميل_فهرست=شيل('ls /example')
        assert all(نالو in اي_ميل_فهرست for نالو in ('java/','c/','python/','README.md')),اي_ميل_فهرست
        if ٻولي=='java':
            꾸러미명세=json.loads((기준/'build/examples/manifest.json').read_text())
            for راههه,داخلا_هنڌ in 꾸러미명세.items():
                شيل('cp '+راههه+' /example-check.bin')
                مواد_قدر=bytearray();فائل_منتقلي_ڪنيڪشن.retrbinary('RETR example-check.bin',مواد_قدر.extend)
                assert len(مواد_قدر)==داخلا_هنڌ['bytes'] and hashlib.sha256(مواد_قدر).hexdigest()==داخلا_هنڌ['sha256'],راههه
            فائل_منتقلي_ڪنيڪشن.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            ٻٽو=bytes(range(256))*64
            فائل_منتقلي_ڪنيڪشن.storbinary('STOR boundary.bin',io.BytesIO(ٻٽو))
            مواد_قدر=bytearray();فائل_منتقلي_ڪنيڪشن.retrbinary('RETR boundary.bin',مواد_قدر.extend)
            assert مواد_قدر==ٻٽو and 'boundary.bin' in فائل_منتقلي_ڪنيڪشن.nlst()
            شيل('cp /boundary.bin /boundary-copy.bin')
            مواد_قدر=bytearray();فائل_منتقلي_ڪنيڪشن.retrbinary('RETR boundary-copy.bin',مواد_قدر.extend)
            assert مواد_قدر==ٻٽو
            فائل_منتقلي_ڪنيڪشن.delete('boundary.bin');فائل_منتقلي_ڪنيڪشن.delete('boundary-copy.bin')
        assert '출력예제' in شيل('ls /example/'+ٻولي)
        شيل('cd /example/'+ٻولي)
        نالو_جدول={'java':'JAVA','c':'C','python':'PYTHON'}[ٻولي]
        예상파일=نالو_جدول+' فائل: 한글 ڪوائف 😀\n'
        if ٻولي=='java':
            تعميل_ڪرڻ_حڪم('javac 출력예제.java','Compiled:');تعميل_ڪرڻ_حڪم('java 출력예제','JAVA 출력: 안녕하세요 😀')
            تعميل_ڪرڻ_حڪم('javac 파일예제.java','Compiled:');تعميل_ڪرڻ_حڪم('java 파일예제',예상파일)
            تعميل_ڪرڻ_حڪم('java 네트워크예제 {} {}'.format(되돌림서버항목.ٽرانسمشن_ڪنٽرول_پروٽوڪول_پورٽ,되돌림서버항목.전문접속번호),'JAVA 네트워크 تصديق_ڪريو: TCP UDP 한글')
            그림명령='java 그래픽예제'
        elif ٻولي=='c':
            for نالو,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('فائل','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 تصديق_ڪريو: UDP 한글')]:
                تعميل_ڪرڻ_حڪم('cc '+نالو+'예제.c -o تعميل_ڪرڻ_حڪم','Compiled native ARM64 ELF:')
                تعميل_ڪرڻ_حڪم('./تعميل_ڪرڻ_حڪم'+전달값,예상결과)
            تعميل_ڪرڻ_حڪم('cc 그래픽예제.c -o تعميل_ڪرڻ_حڪم','Compiled native ARM64 ELF:');그림명령='./تعميل_ڪرڻ_حڪم'
        else:
            for نالو,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('فائل','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 تصديق_ڪريو: UDP 한글')]:
                تعميل_ڪرڻ_حڪم('python '+نالو+'예제.py'+전달값,예상결과)
            그림명령='python 그래픽예제.py'
        شروع_ڊرائنگ=شروع_آف_سيٽ(그림명령)
        متن=수신하기('그림을 확인한 واپس_قدر Enter를 누르세요.\r\n'.encode(),شروع_ڊرائنگ)
        assert نالو_جدول+' 그래픽: 빨강 초록 파랑' in متن and 'exit 0' not in متن,متن
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        فائل_منتقلي_ڪنيڪشن.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();فائل_منتقلي_ڪنيڪشن.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';فائل_منتقلي_ڪنيڪشن.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            آف_سيٽ_قدر=(세로좌표*640+610)*3;assert tuple(빛삼원색[آف_سيٽ_قدر:آف_سيٽ_قدر+3])==색상,(ٻولي,세로좌표,tuple(빛삼원색[آف_سيٽ_قدر:آف_سيٽ_قدر+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(결과자료/(ٻولي+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',شروع_ڊرائنگ)
        if ٻولي=='java':
            شروع_دري=شروع_آف_سيٽ('java 창예제')
            수신하기('GUI 예제 تياري_ڪريو: 창예제'.encode(),شروع_دري)
            def ڪلڪ_ڪريو_قدر(가로,세로):
                for بٽن in (1,0):گراهڪ.sendall(struct.pack('>BBHH',5,بٽن,가로,세로))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            ڪلڪ_ڪريو_قدر(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for ڪريڪٽر_قدر in '한글':누름값(0x1000000|ord(ڪريڪٽر_قدر));누름값(0x1000000|ord(ڪريڪٽر_قدر),False)
            for 횟수 in (1,2):
                هلائڻ=len(대화기록);ڪلڪ_ڪريو_قدر(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),هلائڻ)
            time.sleep(.3)
            دري_ڊرائنگ=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=دري_ڊرائنگ.crop((110,272,530,300)).tobytes()
            دري_ڊرائنگ.save(str(결과자료/'java-swing.png'))
            هلائڻ=len(대화기록);ڪلڪ_ڪريو_قدر(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',هلائڻ)
        # Download the guest-created bytes through FTP in the same GUI VM.
        فائل_داخلا_نالو={'java':'java.txt','c':'c.txt','python':'python.txt'}[ٻولي]
        شيل('cp '+فائل_داخلا_نالو+' /ڪارگر_ڪريو.txt')
        받은수=bytearray();فائل_منتقلي_ڪنيڪشن.retrbinary('RETR ڪارگر_ڪريو.txt',받은수.extend);assert 받은수==예상파일.encode()
        شيل('echo preserved > 출력예제.'+('py' if ٻولي=='python' else ٻولي))
        assert 'EXAMPLES READY' in شيل('example '+ٻولي)
        assert '\npreserved\n' in شيل('cat 출력예제.'+('py' if ٻولي=='python' else ٻولي))
        assert '한/영 ڪليد_قدر, Shift+Space 또는 F9' in شيل('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in شيل('echo GUI NETWORK TOGETHER')
        فائل_منتقلي_ڪنيڪشن.quit();فائل_منتقلي_ڪنيڪشن=None;assert 'FTP stopped' in شيل('ftpd stop')
        print('PASS '+ٻولي+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if فائل_منتقلي_ڪنيڪشن:
            try:فائل_منتقلي_ڪنيڪشن.close()
            except OSError:pass
        if گراهڪ:گراهڪ.close()
        عمل_a7054519.terminate()
        try:عمل_a7054519.wait(timeout=8)
        except subprocess.TimeoutExpired:عمل_a7054519.kill();عمل_a7054519.wait()
        چونڊيندڙ.close();عمل_a7054519.stdout.close();(결과자료/(ٻولي+'-serial.log')).write_bytes(대화기록)


def هلائڻ():
    결과자료=기준/'build/verification/examples';결과자료.mkdir(parents=True,exist_ok=True)
    ڪارگر_رپورٽ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for ٻولي in ('java','c','python'):
                test_언어(ٻولي,되돌림서버항목,결과자료);ڪارگر_رپورٽ['languages'].append(ٻولي)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(قسم_قدر_4b6d6445,ڪوائف.encode()) for قسم_قدر_4b6d6445,ڪوائف in 예상결과],되돌림서버항목.수신됨
            ڪارگر_رپورٽ['host_network_payloads']=[{'protocol':قسم_قدر_4b6d6445,'text':ڪوائف.decode()} for قسم_قدر_4b6d6445,ڪوائف in 되돌림서버항목.수신됨]
        ڪارگر_رپورٽ.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(결과자료/'report.json').write_text(json.dumps(ڪارگر_رپورٽ,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':هلائڻ()
