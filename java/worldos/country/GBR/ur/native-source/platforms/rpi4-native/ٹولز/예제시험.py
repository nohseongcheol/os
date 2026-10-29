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
from نفاذ_کریں_حکم import عکس_ڈالنا_روٹ


def test_언어(زبان,되돌림서버항목,پیمائش_کوائف):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));فائل_منتقلی_دہانہ_نمبر=임시자원.getsockname()[1]
    عمل_کاری=subprocess.Popen(['python3',str(عکس_ڈالنا_روٹ/'ٹولز/نفاذ_کریں_حکم.py'),'--desktop','--network','--port','0','--ftp-port',str(فائل_منتقلی_دہانہ_نمبر)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    منتخب_کنندہ=selectors.DefaultSelector();منتخب_کنندہ.register(عمل_کاری.stdout,selectors.EVENT_READ)
    대화기록=bytearray();کلائنٹ=None;فائل_منتقلی_رابطہ=None
    def 수신하기(확인표시,چلائیں=0):
        اختتام_آفسٹ=time.monotonic()+60
        while 확인표시 not in 대화기록[چلائیں:]:
            if time.monotonic()>اختتام_آفسٹ or عمل_کاری.poll() is not None:raise AssertionError(대화기록[چلائیں:].decode('utf-8','replace'))
            for 누름값,_ in منتخب_کنندہ.select(.1):
                کوائف=누름값.fileobj.read(65536)
                if کوائف:대화기록.extend(کوائف)
        return 대화기록[چلائیں:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(علامت_قدر,누르는중=True):کلائنٹ.sendall(struct.pack('>BBHI',4,int(누르는중),0,علامت_قدر))
    def ابتدا_آفسٹ(اندراج_کی_سطر):
        چلائیں=len(대화기록)
        for کریکٹر_ضابطہ in اندراج_کی_سطر+'\n':
            علامت_قدر=0xff0d if کریکٹر_ضابطہ=='\n' else ord(کریکٹر_ضابطہ) if ord(کریکٹر_ضابطہ)<256 else 0x1000000|ord(کریکٹر_ضابطہ)
            누름값(علامت_قدر);누름값(علامت_قدر,False)
        return چلائیں
    def شیل(اندراج_کی_سطر):return 수신하기(b'jkoros-native> ',ابتدا_آفسٹ(اندراج_کی_سطر))
    def نفاذ_کریں_حکم(اندراج_کی_سطر,예상결과):
        متن=شیل(اندراج_کی_سطر);assert 예상결과 in متن and 'exit 0' in متن,(اندراج_کی_سطر,متن)
        return متن
    def 화소들():
        کلائنٹ.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            زمرہ_قدر=정확한값(کلائنٹ,1)[0]
            if زمرہ_قدر==2:continue
            if زمرہ_قدر==3:
                개수=struct.unpack('>I',정확한값(کلائنٹ,7)[3:])[0];정확한값(کلائنٹ,개수);continue
            assert زمرہ_قدر==0,زمرہ_قدر
            항목수=struct.unpack('>H',정확한값(کلائنٹ,3)[1:])[0]
            for _ in range(항목수):
                ایکس_مربوط,세로좌표,너비값,높이값,کریکٹر_سیٹ=struct.unpack('>HHHHi',정확한값(کلائنٹ,12));assert کریکٹر_سیٹ==0,کریکٹر_سیٹ
                کوائف=정확한값(کلائنٹ,너비값*높이값*4)
                for صف_پوزیشن_ٹھیک_کریں in range(높이값):
                    for کالم_پوزیشن_ٹھیک_کریں in range(너비값):
                        원본자료=(صف_پوزیشن_ٹھیک_کریں*너비값+کالم_پوزیشن_ٹھیک_کریں)*4;ہدف=((세로좌표+صف_پوزیشن_ٹھیک_کریں)*640+ایکس_مربوط+کالم_پوزیشن_ٹھیک_کریں)*3
                        빛삼원색[ہدف:ہدف+3]=bytes((کوائف[원본자료+2],کوائف[원본자료+1],کوائف[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        دہانہ_نمبر=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        کلائنٹ=socket.create_connection(('127.0.0.1',دہانہ_نمبر),timeout=10)
        assert 정확한값(کلائنٹ,12)==b'RFB 003.008\n';کلائنٹ.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(کلائنٹ,정확한값(کلائنٹ,1)[0]);کلائنٹ.sendall(b'\x01');assert 정확한값(کلائنٹ,4)==b'\0'*4
        کلائنٹ.sendall(b'\x01');초기값=정확한값(کلائنٹ,24);정확한값(کلائنٹ,struct.unpack('>I',초기값[20:])[0])
        کلائنٹ.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        کلائنٹ.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in شیل('ftpd start')
        فائل_منتقلی_رابطہ=ftplib.FTP();فائل_منتقلی_رابطہ.encoding='utf-8';فائل_منتقلی_رابطہ.connect('127.0.0.1',فائل_منتقلی_دہانہ_نمبر,timeout=20);فائل_منتقلی_رابطہ.login()
        پے_لوڈ_کوائف=('GUI와 FTP 동시 사용 '+زبان+' 😀\n').encode()
        فائل_منتقلی_رابطہ.storbinary('STOR 함께.txt',io.BytesIO(پے_لوڈ_کوائف))
        assert پے_لوڈ_کوائف.decode().strip() in شیل('cat /함께.txt')
        받은수=bytearray();فائل_منتقلی_رابطہ.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==پے_لوڈ_کوائف;فائل_منتقلی_رابطہ.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        بھیجیں_فہرست=شیل('ls /example')
        assert all(نام in بھیجیں_فہرست for نام in ('java/','c/','python/','README.md')),بھیجیں_فہرست
        if زبان=='java':
            꾸러미명세=json.loads((عکس_ڈالنا_روٹ/'build/examples/manifest.json').read_text())
            for راستہ_2,اندراج_نقطہ in 꾸러미명세.items():
                شیل('cp '+راستہ_2+' /example-check.bin')
                مشمول_قدر=bytearray();فائل_منتقلی_رابطہ.retrbinary('RETR example-check.bin',مشمول_قدر.extend)
                assert len(مشمول_قدر)==اندراج_نقطہ['bytes'] and hashlib.sha256(مشمول_قدر).hexdigest()==اندراج_نقطہ['sha256'],راستہ_2
            فائل_منتقلی_رابطہ.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            ثنائی=bytes(range(256))*64
            فائل_منتقلی_رابطہ.storbinary('STOR boundary.bin',io.BytesIO(ثنائی))
            مشمول_قدر=bytearray();فائل_منتقلی_رابطہ.retrbinary('RETR boundary.bin',مشمول_قدر.extend)
            assert مشمول_قدر==ثنائی and 'boundary.bin' in فائل_منتقلی_رابطہ.nlst()
            شیل('cp /boundary.bin /boundary-copy.bin')
            مشمول_قدر=bytearray();فائل_منتقلی_رابطہ.retrbinary('RETR boundary-copy.bin',مشمول_قدر.extend)
            assert مشمول_قدر==ثنائی
            فائل_منتقلی_رابطہ.delete('boundary.bin');فائل_منتقلی_رابطہ.delete('boundary-copy.bin')
        assert 'چھپائیمثال' in شیل('ls /example/'+زبان)
        شیل('cd /example/'+زبان)
        نام_جدول={'java':'JAVA','c':'C','python':'PYTHON'}[زبان]
        예상파일=نام_جدول+' فائل_کا_نام: 한글 کوائف 😀\n'
        if زبان=='java':
            نفاذ_کریں_حکم('javac چھپائیمثال.java','Compiled:');نفاذ_کریں_حکم('java چھپائیمثال','JAVA اخراج_کا_مقام: 안녕하세요 😀')
            نفاذ_کریں_حکم('javac فائلمثال.java','Compiled:');نفاذ_کریں_حکم('java فائلمثال',예상파일)
            نفاذ_کریں_حکم('java نیٹورکمثال {} {}'.format(되돌림서버항목.ٹرانسمشن_کنٹرول_پروٹوکول_پورٹ,되돌림서버항목.전문접속번호),'JAVA 네트워크 تصدیق_کریں: TCP UDP 한글')
            گرافکس_حکم='java تصویرمثال'
        elif زبان=='c':
            for نام,전달값,예상결과 in [('اخراج_کا_مقام','', 'C اخراج_کا_مقام: 안녕하세요 😀'),('فائل_کا_نام','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 تصدیق_کریں: UDP 한글')]:
                نفاذ_کریں_حکم('cc '+نام+'예제.c -o نفاذ_کریں_حکم','Compiled native ARM64 ELF:')
                نفاذ_کریں_حکم('./نفاذ_کریں_حکم'+전달값,예상결과)
            نفاذ_کریں_حکم('cc تصویرمثال.c -o نفاذ_کریں_حکم','Compiled native ARM64 ELF:');گرافکس_حکم='./نفاذ_کریں_حکم'
        else:
            for نام,전달값,예상결과 in [('اخراج_کا_مقام','','PYTHON اخراج_کا_مقام: 안녕하세요 😀'),('فائل_کا_نام','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 تصدیق_کریں: UDP 한글')]:
                نفاذ_کریں_حکم('python '+نام+'예제.py'+전달값,예상결과)
            گرافکس_حکم='python تصویرمثال.py'
        ابتدا_ڈرائنگ=ابتدا_آفسٹ(گرافکس_حکم)
        متن=수신하기('그림을 확인한 واپس_قدر Enter를 누르세요.\r\n'.encode(),ابتدا_ڈرائنگ)
        assert نام_جدول+' 그래픽: 빨강 초록 파랑' in متن and 'exit 0' not in متن,متن
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        فائل_منتقلی_رابطہ.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();فائل_منتقلی_رابطہ.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';فائل_منتقلی_رابطہ.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            آفسٹ_قدر=(세로좌표*640+610)*3;assert tuple(빛삼원색[آفسٹ_قدر:آفسٹ_قدر+3])==색상,(زبان,세로좌표,tuple(빛삼원색[آفسٹ_قدر:آفسٹ_قدر+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(پیمائش_کوائف/(زبان+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',ابتدا_ڈرائنگ)
        if زبان=='java':
            ابتدا_دریچہ=ابتدا_آفسٹ('java کھڑکیمثال')
            수신하기('GUI 예제 تیار_کریں: کھڑکیمثال'.encode(),ابتدا_دریچہ)
            def کلک_قدر(가로,عمودی_پوزیشن_ٹھیک_کریں):
                for بٹن in (1,0):کلائنٹ.sendall(struct.pack('>BBHH',5,بٹن,가로,عمودی_پوزیشن_ٹھیک_کریں))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            کلک_قدر(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for کریکٹر_قدر in '한글':누름값(0x1000000|ord(کریکٹر_قدر));누름값(0x1000000|ord(کریکٹر_قدر),False)
            for 횟수 in (1,2):
                چلائیں=len(대화기록);کلک_قدر(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),چلائیں)
            time.sleep(.3)
            دریچہ_ڈرائنگ=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=دریچہ_ڈرائنگ.crop((110,272,530,300)).tobytes()
            دریچہ_ڈرائنگ.save(str(پیمائش_کوائف/'java-swing.png'))
            چلائیں=len(대화기록);کلک_قدر(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',چلائیں)
        # Download the guest-created bytes through FTP in the same GUI VM.
        فائل_اندراج_نام={'java':'java.txt','c':'c.txt','python':'python.txt'}[زبان]
        شیل('cp '+فائل_اندراج_نام+' /جواز_دہی_کریں.txt')
        받은수=bytearray();فائل_منتقلی_رابطہ.retrbinary('RETR جواز_دہی_کریں.txt',받은수.extend);assert 받은수==예상파일.encode()
        شیل('echo preserved > چھپائیمثال.'+('py' if زبان=='python' else زبان))
        assert 'EXAMPLES READY' in شیل('example '+زبان)
        assert '\npreserved\n' in شیل('cat چھپائیمثال.'+('py' if زبان=='python' else زبان))
        assert '한/영 کلید_قدر, Shift+Space 또는 F9' in شیل('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in شیل('echo GUI NETWORK TOGETHER')
        فائل_منتقلی_رابطہ.quit();فائل_منتقلی_رابطہ=None;assert 'FTP stopped' in شیل('ftpd stop')
        print('PASS '+زبان+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if فائل_منتقلی_رابطہ:
            try:فائل_منتقلی_رابطہ.close()
            except OSError:pass
        if کلائنٹ:کلائنٹ.close()
        عمل_کاری.terminate()
        try:عمل_کاری.wait(timeout=8)
        except subprocess.TimeoutExpired:عمل_کاری.kill();عمل_کاری.wait()
        منتخب_کنندہ.close();عمل_کاری.stdout.close();(پیمائش_کوائف/(زبان+'-serial.log')).write_bytes(대화기록)


def چلائیں():
    پیمائش_کوائف=عکس_ڈالنا_روٹ/'build/verification/examples';پیمائش_کوائف.mkdir(parents=True,exist_ok=True)
    توثیق_رپورٹ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((عکس_ڈالنا_روٹ/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for زبان in ('java','c','python'):
                test_언어(زبان,되돌림서버항목,پیمائش_کوائف);توثیق_رپورٹ['languages'].append(زبان)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(زمرہ_قدر,کوائف.encode()) for زمرہ_قدر,کوائف in 예상결과],되돌림서버항목.수신됨
            توثیق_رپورٹ['host_network_payloads']=[{'protocol':زمرہ_قدر,'text':کوائف.decode()} for زمرہ_قدر,کوائف in 되돌림서버항목.수신됨]
        توثیق_رپورٹ.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(پیمائش_کوائف/'report.json').write_text(json.dumps(توثیق_رپورٹ,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':چلائیں()
