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
from رایانه_نما import 정확한값
from 예제되돌림서버 import 되돌림서버
from اجرا_فرمان import نمایش_دادن_جذر


def test_언어(زبان,되돌림서버항목,سنجش_داده_ها):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));فایل_انتقال_شماره_درگاه=임시자원.getsockname()[1]
    فرآیند=subprocess.Popen(['python3',str(نمایش_دادن_جذر/'ابزارها/اجرا_فرمان.py'),'--desktop','--network','--port','0','--ftp-port',str(فایل_انتقال_شماره_درگاه)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    انتخاب_کننده=selectors.DefaultSelector();انتخاب_کننده.register(فرآیند.stdout,selectors.EVENT_READ)
    대화기록=bytearray();سرویس_گیرنده=None;فایل_انتقال_اتصال=None
    def 수신하기(확인표시,اجرا_2=0):
        پایان_دادن_جابجایی_لایه_ای=time.monotonic()+60
        while 확인표시 not in 대화기록[اجرا_2:]:
            if time.monotonic()>پایان_دادن_جابجایی_لایه_ای or فرآیند.poll() is not None:raise AssertionError(대화기록[اجرا_2:].decode('utf-8','replace'))
            for 누름값,_ in انتخاب_کننده.select(.1):
                داده_ها=누름값.fileobj.read(65536)
                if داده_ها:대화기록.extend(داده_ها)
        return 대화기록[اجرا_2:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(نماد_مقدار,누르는중=True):سرویس_گیرنده.sendall(struct.pack('>BBHI',4,int(누르는중),0,نماد_مقدار))
    def شروع_جابجایی_لایه_ای(خط):
        اجرا_2=len(대화기록)
        for کد_نویسه in خط+'\n':
            نماد_مقدار=0xff0d if کد_نویسه=='\n' else ord(کد_نویسه) if ord(کد_نویسه)<256 else 0x1000000|ord(کد_نویسه)
            누름값(نماد_مقدار);누름값(نماد_مقدار,False)
        return اجرا_2
    def واسط(خط):return 수신하기(b'jkoros-native> ',شروع_جابجایی_لایه_ای(خط))
    def اجرا_فرمان(خط,예상결과):
        متن=واسط(خط);assert 예상결과 in متن and 'exit 0' in متن,(خط,متن)
        return متن
    def 화소들():
        سرویس_گیرنده.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            دسته_مقدار=정확한값(سرویس_گیرنده,1)[0]
            if دسته_مقدار==2:continue
            if دسته_مقدار==3:
                개수=struct.unpack('>I',정확한값(سرویس_گیرنده,7)[3:])[0];정확한값(سرویس_گیرنده,개수);continue
            assert دسته_مقدار==0,دسته_مقدار
            항목수=struct.unpack('>H',정확한값(سرویس_گیرنده,3)[1:])[0]
            for _ in range(항목수):
                مختصات_x,دکمه_Y_مختصات,너비값,높이값,مجموعه_نویسه_ها=struct.unpack('>HHHHi',정확한값(سرویس_گیرنده,12));assert مجموعه_نویسه_ها==0,مجموعه_نویسه_ها
                داده_ها=정확한값(سرویس_گیرنده,너비값*높이값*4)
                for ردیف_مرتب_کردن in range(높이값):
                    for ستون_مرتب_کردن in range(너비값):
                        원본자료=(ردیف_مرتب_کردن*너비값+ستون_مرتب_کردن)*4;هدف=((دکمه_Y_مختصات+ردیف_مرتب_کردن)*640+مختصات_x+ستون_مرتب_کردن)*3
                        빛삼원색[هدف:هدف+3]=bytes((داده_ها[원본자료+2],داده_ها[원본자료+1],داده_ها[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        شماره_درگاه=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        سرویس_گیرنده=socket.create_connection(('127.0.0.1',شماره_درگاه),timeout=10)
        assert 정확한값(سرویس_گیرنده,12)==b'RFB 003.008\n';سرویس_گیرنده.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(سرویس_گیرنده,정확한값(سرویس_گیرنده,1)[0]);سرویس_گیرنده.sendall(b'\x01');assert 정확한값(سرویس_گیرنده,4)==b'\0'*4
        سرویس_گیرنده.sendall(b'\x01');초기값=정확한값(سرویس_گیرنده,24);정확한값(سرویس_گیرنده,struct.unpack('>I',초기값[20:])[0])
        سرویس_گیرنده.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        سرویس_گیرنده.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in واسط('ftpd start')
        فایل_انتقال_اتصال=ftplib.FTP();فایل_انتقال_اتصال.encoding='utf-8';فایل_انتقال_اتصال.connect('127.0.0.1',فایل_انتقال_شماره_درگاه,timeout=20);فایل_انتقال_اتصال.login()
        داده_های_ضروری_داده_ها=('GUI와 FTP 동시 사용 '+زبان+' 😀\n').encode()
        فایل_انتقال_اتصال.storbinary('STOR 함께.txt',io.BytesIO(داده_های_ضروری_داده_ها))
        assert داده_های_ضروری_داده_ها.decode().strip() in واسط('cat /함께.txt')
        받은수=bytearray();فایل_انتقال_اتصال.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==داده_های_ضروری_داده_ها;فایل_انتقال_اتصال.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        ارسال_لیست=واسط('ls /example')
        assert all(نام in ارسال_لیست for نام in ('java/','c/','python/','README.md')),ارسال_لیست
        if زبان=='java':
            꾸러미명세=json.loads((نمایش_دادن_جذر/'build/examples/manifest.json').read_text())
            for مسیر,ورودی_نقطه in 꾸러미명세.items():
                واسط('cp '+مسیر+' /example-check.bin')
                محتوا_مقدار=bytearray();فایل_انتقال_اتصال.retrbinary('RETR example-check.bin',محتوا_مقدار.extend)
                assert len(محتوا_مقدار)==ورودی_نقطه['bytes'] and hashlib.sha256(محتوا_مقدار).hexdigest()==ورودی_نقطه['sha256'],مسیر
            فایل_انتقال_اتصال.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            دودویی=bytes(range(256))*64
            فایل_انتقال_اتصال.storbinary('STOR boundary.bin',io.BytesIO(دودویی))
            محتوا_مقدار=bytearray();فایل_انتقال_اتصال.retrbinary('RETR boundary.bin',محتوا_مقدار.extend)
            assert محتوا_مقدار==دودویی and 'boundary.bin' in فایل_انتقال_اتصال.nlst()
            واسط('cp /boundary.bin /boundary-copy.bin')
            محتوا_مقدار=bytearray();فایل_انتقال_اتصال.retrbinary('RETR boundary-copy.bin',محتوا_مقدار.extend)
            assert محتوا_مقدار==دودویی
            فایل_انتقال_اتصال.delete('boundary.bin');فایل_انتقال_اتصال.delete('boundary-copy.bin')
        assert 'نمونهچاپ' in واسط('ls /example/'+زبان)
        واسط('cd /example/'+زبان)
        نام_جدول={'java':'JAVA','c':'C','python':'PYTHON'}[زبان]
        예상파일=نام_جدول+' پرونده: 한글 داده_ها 😀\n'
        if زبان=='java':
            اجرا_فرمان('javac نمونهچاپ.java','Compiled:');اجرا_فرمان('java نمونهچاپ','JAVA خروجی: 안녕하세요 😀')
            اجرا_فرمان('javac نمونهپرونده.java','Compiled:');اجرا_فرمان('java نمونهپرونده',예상파일)
            اجرا_فرمان('java نمونهشبکه {} {}'.format(되돌림서버항목.پروتکل_کنترل_مخابره_تبدیل,되돌림서버항목.پروتکل_داده_نگار_کاربر_تبدیل),'JAVA 네트워크 تأیید_صحت: TCP UDP 한글')
            گرافیک_ها_فرمان='java نمونهنقاشی'
        elif زبان=='c':
            for نام,전달값,예상결과 in [('خروجی','', 'C خروجی: 안녕하세요 😀'),('پرونده','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.پروتکل_داده_نگار_کاربر_تبدیل),'C 네트워크 تأیید_صحت: UDP 한글')]:
                اجرا_فرمان('cc '+نام+'예제.c -o اجرا_فرمان','Compiled native ARM64 ELF:')
                اجرا_فرمان('./اجرا_فرمان'+전달값,예상결과)
            اجرا_فرمان('cc نمونهنقاشی.c -o اجرا_فرمان','Compiled native ARM64 ELF:');گرافیک_ها_فرمان='./اجرا_فرمان'
        else:
            for نام,전달값,예상결과 in [('خروجی','','PYTHON خروجی: 안녕하세요 😀'),('پرونده','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.پروتکل_داده_نگار_کاربر_تبدیل),'PYTHON 네트워크 تأیید_صحت: UDP 한글')]:
                اجرا_فرمان('python '+نام+'예제.py'+전달값,예상결과)
            گرافیک_ها_فرمان='python نمونهنقاشی.py'
        شروع_نقاشی=شروع_جابجایی_لایه_ای(گرافیک_ها_فرمان)
        متن=수신하기('그림을 확인한 برگشت_مقدار Enter를 누르세요.\r\n'.encode(),شروع_نقاشی)
        assert نام_جدول+' 그래픽: 빨강 초록 파랑' in متن and 'exit 0' not in متن,متن
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        فایل_انتقال_اتصال.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();فایل_انتقال_اتصال.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';فایل_انتقال_اتصال.delete('도중.txt')
        빛삼원색=화소들()
        for دکمه_Y_مختصات,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            جابجایی_لایه_ای_مقدار=(دکمه_Y_مختصات*640+610)*3;assert tuple(빛삼원색[جابجایی_لایه_ای_مقدار:جابجایی_لایه_ای_مقدار+3])==색상,(زبان,دکمه_Y_مختصات,tuple(빛삼원색[جابجایی_لایه_ای_مقدار:جابجایی_لایه_ای_مقدار+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(سنجش_داده_ها/(زبان+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',شروع_نقاشی)
        if زبان=='java':
            شروع_پنجره=شروع_جابجایی_لایه_ای('java نمونهپنجره')
            수신하기('GUI 예제 آماده_کردن: نمونهپنجره'.encode(),شروع_پنجره)
            def کلیک_مقدار(가로,عمودی_مرتب_کردن):
                for دکمه in (1,0):سرویس_گیرنده.sendall(struct.pack('>BBHH',5,دکمه,가로,عمودی_مرتب_کردن))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            کلیک_مقدار(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for نویسه_مقدار in '한글':누름값(0x1000000|ord(نویسه_مقدار));누름값(0x1000000|ord(نویسه_مقدار),False)
            for 횟수 in (1,2):
                اجرا_2=len(대화기록);کلیک_مقدار(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),اجرا_2)
            time.sleep(.3)
            پنجره_نقاشی=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=پنجره_نقاشی.crop((110,272,530,300)).tobytes()
            پنجره_نقاشی.save(str(سنجش_داده_ها/'java-swing.png'))
            اجرا_2=len(대화기록);کلیک_مقدار(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',اجرا_2)
        # Download the guest-created bytes through FTP in the same GUI VM.
        فایل_ورودی_نام={'java':'java.txt','c':'c.txt','python':'python.txt'}[زبان]
        واسط('cp '+فایل_ورودی_نام+' /ارزیابی_کردن.txt')
        받은수=bytearray();فایل_انتقال_اتصال.retrbinary('RETR ارزیابی_کردن.txt',받은수.extend);assert 받은수==예상파일.encode()
        واسط('echo preserved > نمونهچاپ.'+('py' if زبان=='python' else زبان))
        assert 'EXAMPLES READY' in واسط('example '+زبان)
        assert '\npreserved\n' in واسط('cat نمونهچاپ.'+('py' if زبان=='python' else زبان))
        assert '한/영 کلید_مقدار, Shift+Space 또는 F9' in واسط('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in واسط('echo GUI NETWORK TOGETHER')
        فایل_انتقال_اتصال.quit();فایل_انتقال_اتصال=None;assert 'FTP stopped' in واسط('ftpd stop')
        print('PASS '+زبان+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if فایل_انتقال_اتصال:
            try:فایل_انتقال_اتصال.close()
            except OSError:pass
        if سرویس_گیرنده:سرویس_گیرنده.close()
        فرآیند.terminate()
        try:فرآیند.wait(timeout=8)
        except subprocess.TimeoutExpired:فرآیند.kill();فرآیند.wait()
        انتخاب_کننده.close();فرآیند.stdout.close();(سنجش_داده_ها/(زبان+'-serial.log')).write_bytes(대화기록)


def اجرا_2():
    سنجش_داده_ها=نمایش_دادن_جذر/'build/verification/examples';سنجش_داده_ها.mkdir(parents=True,exist_ok=True)
    اعتبارسنجی_گزارش={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((نمایش_دادن_جذر/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for زبان in ('java','c','python'):
                test_언어(زبان,되돌림서버항목,سنجش_داده_ها);اعتبارسنجی_گزارش['languages'].append(زبان)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(دسته_مقدار,داده_ها.encode()) for دسته_مقدار,داده_ها in 예상결과],되돌림서버항목.수신됨
            اعتبارسنجی_گزارش['host_network_payloads']=[{'protocol':دسته_مقدار,'text':داده_ها.decode()} for دسته_مقدار,داده_ها in 되돌림서버항목.수신됨]
        اعتبارسنجی_گزارش.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(سنجش_داده_ها/'report.json').write_text(json.dumps(اعتبارسنجی_گزارش,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':اجرا_2()
