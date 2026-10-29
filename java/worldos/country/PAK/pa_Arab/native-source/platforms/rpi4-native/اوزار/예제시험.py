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
from ڈیسک_ٹاپ_منظر import 정확한값
from 예제되돌림서버 import 되돌림서버
from نفاذ_کرو_حکم import 기준


def test_언어(زبان,되돌림서버항목,결과자료):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    عمل=subprocess.Popen(['python3',str(기준/'اوزار/نفاذ_کرو_حکم.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    منتخب_کرنڑ_آلا=selectors.DefaultSelector();منتخب_کرنڑ_آلا.register(عمل.stdout,selectors.EVENT_READ)
    대화기록=bytearray();گاہک=None;فائل_منتقلی_کنکشن=None
    def 수신하기(확인표시,چلاؤ=0):
        ختم_کرو_آف_سیٹ=time.monotonic()+60
        while 확인표시 not in 대화기록[چلاؤ:]:
            if time.monotonic()>ختم_کرو_آف_سیٹ or عمل.poll() is not None:raise AssertionError(대화기록[چلاؤ:].decode('utf-8','replace'))
            for 누름값,_ in منتخب_کرنڑ_آلا.select(.1):
                کوائف=누름값.fileobj.read(65536)
                if کوائف:대화기록.extend(کوائف)
        return 대화기록[چلاؤ:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(علامت_قدر,누르는중=True):گاہک.sendall(struct.pack('>BBHI',4,int(누르는중),0,علامت_قدر))
    def مکھ_آف_سیٹ(لائن):
        چلاؤ=len(대화기록)
        for کیریکٹر_کوڈ in لائن+'\n':
            علامت_قدر=0xff0d if کیریکٹر_کوڈ=='\n' else ord(کیریکٹر_کوڈ) if ord(کیریکٹر_کوڈ)<256 else 0x1000000|ord(کیریکٹر_کوڈ)
            누름값(علامت_قدر);누름값(علامت_قدر,False)
        return چلاؤ
    def شیل(لائن):return 수신하기(b'jkoros-native> ',مکھ_آف_سیٹ(لائن))
    def نفاذ_کرو_حکم(لائن,예상결과):
        متن=شیل(لائن);assert 예상결과 in متن and 'exit 0' in متن,(لائن,متن)
        return متن
    def 화소들():
        گاہک.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            زمرہ_قدر=정확한값(گاہک,1)[0]
            if زمرہ_قدر==2:continue
            if زمرہ_قدر==3:
                개수=struct.unpack('>I',정확한값(گاہک,7)[3:])[0];정확한값(گاہک,개수);continue
            assert زمرہ_قدر==0,زمرہ_قدر
            항목수=struct.unpack('>H',정확한값(گاہک,3)[1:])[0]
            for _ in range(항목수):
                x_محدد,세로좌표,너비값,높이값,کریکٹر_سیٹ=struct.unpack('>HHHHi',정확한값(گاہک,12));assert کریکٹر_سیٹ==0,کریکٹر_سیٹ
                کوائف=정확한값(گاہک,너비값*높이값*4)
                for 행위치 in range(높이값):
                    for 열위치 in range(너비값):
                        원본자료=(행위치*너비값+열위치)*4;ہدف=((세로좌표+행위치)*640+x_محدد+열위치)*3
                        빛삼원색[ہدف:ہدف+3]=bytes((کوائف[원본자료+2],کوائف[원본자료+1],کوائف[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        گاہک=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert 정확한값(گاہک,12)==b'RFB 003.008\n';گاہک.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(گاہک,정확한값(گاہک,1)[0]);گاہک.sendall(b'\x01');assert 정확한값(گاہک,4)==b'\0'*4
        گاہک.sendall(b'\x01');초기값=정확한값(گاہک,24);정확한값(گاہک,struct.unpack('>I',초기값[20:])[0])
        گاہک.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        گاہک.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in شیل('ftpd start')
        فائل_منتقلی_کنکشن=ftplib.FTP();فائل_منتقلی_کنکشن.encoding='utf-8';فائل_منتقلی_کنکشن.connect('127.0.0.1',파일전송접속번호,timeout=20);فائل_منتقلی_کنکشن.login()
        پے_لوڈ_کوائف=('GUI와 FTP 동시 사용 '+زبان+' 😀\n').encode()
        فائل_منتقلی_کنکشن.storbinary('STOR 함께.txt',io.BytesIO(پے_لوڈ_کوائف))
        assert پے_لوڈ_کوائف.decode().strip() in شیل('cat /함께.txt')
        받은수=bytearray();فائل_منتقلی_کنکشن.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==پے_لوڈ_کوائف;فائل_منتقلی_کنکشن.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        بھیجو_فرست=شیل('ls /example')
        assert all(ناں in بھیجو_فرست for ناں in ('java/','c/','python/','README.md')),بھیجو_فرست
        if زبان=='java':
            꾸러미명세=json.loads((기준/'build/examples/manifest.json').read_text())
            for راہ,داخلہ_مقام in 꾸러미명세.items():
                شیل('cp '+راہ+' /example-check.bin')
                اجزاء_قدر=bytearray();فائل_منتقلی_کنکشن.retrbinary('RETR example-check.bin',اجزاء_قدر.extend)
                assert len(اجزاء_قدر)==داخلہ_مقام['bytes'] and hashlib.sha256(اجزاء_قدر).hexdigest()==داخلہ_مقام['sha256'],راہ
            فائل_منتقلی_کنکشن.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            مثنی=bytes(range(256))*64
            فائل_منتقلی_کنکشن.storbinary('STOR boundary.bin',io.BytesIO(مثنی))
            اجزاء_قدر=bytearray();فائل_منتقلی_کنکشن.retrbinary('RETR boundary.bin',اجزاء_قدر.extend)
            assert اجزاء_قدر==مثنی and 'boundary.bin' in فائل_منتقلی_کنکشن.nlst()
            شیل('cp /boundary.bin /boundary-copy.bin')
            اجزاء_قدر=bytearray();فائل_منتقلی_کنکشن.retrbinary('RETR boundary-copy.bin',اجزاء_قدر.extend)
            assert اجزاء_قدر==مثنی
            فائل_منتقلی_کنکشن.delete('boundary.bin');فائل_منتقلی_کنکشن.delete('boundary-copy.bin')
        assert '출력예제' in شیل('ls /example/'+زبان)
        شیل('cd /example/'+زبان)
        ناں_جدول={'java':'JAVA','c':'C','python':'PYTHON'}[زبان]
        예상파일=ناں_جدول+' فائل: 한글 کوائف 😀\n'
        if زبان=='java':
            نفاذ_کرو_حکم('javac 출력예제.java','Compiled:');نفاذ_کرو_حکم('java 출력예제','JAVA 출력: 안녕하세요 😀')
            نفاذ_کرو_حکم('javac 파일예제.java','Compiled:');نفاذ_کرو_حکم('java 파일예제',예상파일)
            نفاذ_کرو_حکم('java 네트워크예제 {} {}'.format(되돌림서버항목.ٹرانسمشن_کنٹرول_پروٹوکول_دہانہ,되돌림서버항목.전문접속번호),'JAVA 네트워크 تصدیق_کرو: TCP UDP 한글')
            그림명령='java 그래픽예제'
        elif زبان=='c':
            for ناں,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('فائل','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 تصدیق_کرو: UDP 한글')]:
                نفاذ_کرو_حکم('cc '+ناں+'예제.c -o نفاذ_کرو_حکم','Compiled native ARM64 ELF:')
                نفاذ_کرو_حکم('./نفاذ_کرو_حکم'+전달값,예상결과)
            نفاذ_کرو_حکم('cc 그래픽예제.c -o نفاذ_کرو_حکم','Compiled native ARM64 ELF:');그림명령='./نفاذ_کرو_حکم'
        else:
            for ناں,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('فائل','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 تصدیق_کرو: UDP 한글')]:
                نفاذ_کرو_حکم('python '+ناں+'예제.py'+전달값,예상결과)
            그림명령='python 그래픽예제.py'
        مکھ_ڈرائنگ=مکھ_آف_سیٹ(그림명령)
        متن=수신하기('그림을 확인한 پیچھے_قدر Enter를 누르세요.\r\n'.encode(),مکھ_ڈرائنگ)
        assert ناں_جدول+' 그래픽: 빨강 초록 파랑' in متن and 'exit 0' not in متن,متن
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        فائل_منتقلی_کنکشن.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();فائل_منتقلی_کنکشن.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';فائل_منتقلی_کنکشن.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            آف_سیٹ_قدر=(세로좌표*640+610)*3;assert tuple(빛삼원색[آف_سیٹ_قدر:آف_سیٹ_قدر+3])==색상,(زبان,세로좌표,tuple(빛삼원색[آف_سیٹ_قدر:آف_سیٹ_قدر+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(결과자료/(زبان+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',مکھ_ڈرائنگ)
        if زبان=='java':
            مکھ_کھڑکی=مکھ_آف_سیٹ('java 창예제')
            수신하기('GUI 예제 تیاری_کرو: 창예제'.encode(),مکھ_کھڑکی)
            def کلک_کرو_قدر(가로,세로):
                for بٹن in (1,0):گاہک.sendall(struct.pack('>BBHH',5,بٹن,가로,세로))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            کلک_کرو_قدر(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for کریکٹر_قدر in '한글':누름값(0x1000000|ord(کریکٹر_قدر));누름값(0x1000000|ord(کریکٹر_قدر),False)
            for 횟수 in (1,2):
                چلاؤ=len(대화기록);کلک_کرو_قدر(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),چلاؤ)
            time.sleep(.3)
            کھڑکی_ڈرائنگ=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=کھڑکی_ڈرائنگ.crop((110,272,530,300)).tobytes()
            کھڑکی_ڈرائنگ.save(str(결과자료/'java-swing.png'))
            چلاؤ=len(대화기록);کلک_کرو_قدر(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',چلاؤ)
        # Download the guest-created bytes through FTP in the same GUI VM.
        فائل_داخلہ_ناں={'java':'java.txt','c':'c.txt','python':'python.txt'}[زبان]
        شیل('cp '+فائل_داخلہ_ناں+' /تریخ_دے_مطابق_کرو.txt')
        받은수=bytearray();فائل_منتقلی_کنکشن.retrbinary('RETR تریخ_دے_مطابق_کرو.txt',받은수.extend);assert 받은수==예상파일.encode()
        شیل('echo preserved > 출력예제.'+('py' if زبان=='python' else زبان))
        assert 'EXAMPLES READY' in شیل('example '+زبان)
        assert '\npreserved\n' in شیل('cat 출력예제.'+('py' if زبان=='python' else زبان))
        assert '한/영 کلید_قدر, Shift+Space 또는 F9' in شیل('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in شیل('echo GUI NETWORK TOGETHER')
        فائل_منتقلی_کنکشن.quit();فائل_منتقلی_کنکشن=None;assert 'FTP stopped' in شیل('ftpd stop')
        print('PASS '+زبان+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if فائل_منتقلی_کنکشن:
            try:فائل_منتقلی_کنکشن.close()
            except OSError:pass
        if گاہک:گاہک.close()
        عمل.terminate()
        try:عمل.wait(timeout=8)
        except subprocess.TimeoutExpired:عمل.kill();عمل.wait()
        منتخب_کرنڑ_آلا.close();عمل.stdout.close();(결과자료/(زبان+'-serial.log')).write_bytes(대화기록)


def چلاؤ():
    결과자료=기준/'build/verification/examples';결과자료.mkdir(parents=True,exist_ok=True)
    جواز_دہی_رپورٹ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for زبان in ('java','c','python'):
                test_언어(زبان,되돌림서버항목,결과자료);جواز_دہی_رپورٹ['languages'].append(زبان)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(زمرہ_قدر,کوائف.encode()) for زمرہ_قدر,کوائف in 예상결과],되돌림서버항목.수신됨
            جواز_دہی_رپورٹ['host_network_payloads']=[{'protocol':زمرہ_قدر,'text':کوائف.decode()} for زمرہ_قدر,کوائف in 되돌림서버항목.수신됨]
        جواز_دہی_رپورٹ.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(결과자료/'report.json').write_text(json.dumps(جواز_دہی_رپورٹ,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':چلاؤ()
