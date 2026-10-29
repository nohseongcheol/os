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
from سطح_مكتب_عرض import 정확한값
from 예제되돌림서버 import ارتداد_خوادم
from ينفذ_أمر import يعرض_جذر


def يختبر_لغة(لغة,ارتداد_خادم_إدخال,مقياس_بيانات):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));نقل_الملفات_رقم_المنفذ=임시자원.getsockname()[1]
    عملية=subprocess.Popen(['python3',str(يعرض_جذر/'أدوات/ينفذ_أمر.py'),'--desktop','--network','--port','0','--ftp-port',str(نقل_الملفات_رقم_المنفذ)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    محدد=selectors.DefaultSelector();محدد.register(عملية.stdout,selectors.EVENT_READ)
    نسخة_مكتوبة=bytearray();عميل=None;نقل_الملفات_صديق=None
    def يستلم_رسالة(علامة,تشغيل=0):
        إنهاء_مكالمة_إزاحة=time.monotonic()+60
        while علامة not in نسخة_مكتوبة[تشغيل:]:
            if time.monotonic()>إنهاء_مكالمة_إزاحة or عملية.poll() is not None:raise AssertionError(نسخة_مكتوبة[تشغيل:].decode('utf-8','replace'))
            for 누름값,_ in محدد.select(.1):
                بيانات=누름값.fileobj.read(65536)
                if بيانات:نسخة_مكتوبة.extend(بيانات)
        return نسخة_مكتوبة[تشغيل:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(رمز_قيمة,누르는중=True):عميل.sendall(struct.pack('>BBHI',4,int(누르는중),0,رمز_قيمة))
    def بدء_إزاحة(سطر):
        تشغيل=len(نسخة_مكتوبة)
        for رمز_الحرف in سطر+'\n':
            رمز_قيمة=0xff0d if رمز_الحرف=='\n' else ord(رمز_الحرف) if ord(رمز_الحرف)<256 else 0x1000000|ord(رمز_الحرف)
            누름값(رمز_قيمة);누름값(رمز_قيمة,False)
        return تشغيل
    def 셸(سطر):return يستلم_رسالة(b'jkoros-native> ',بدء_إزاحة(سطر))
    def ينفذ_أمر(سطر,예상결과):
        نص=셸(سطر);assert 예상결과 in نص and 'exit 0' in نص,(سطر,نص)
        return نص
    def 화소들():
        عميل.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            فئة_قيمة=정확한값(عميل,1)[0]
            if فئة_قيمة==2:continue
            if فئة_قيمة==3:
                개수=struct.unpack('>I',정확한값(عميل,7)[3:])[0];정확한값(عميل,개수);continue
            assert فئة_قيمة==0,فئة_قيمة
            항목수=struct.unpack('>H',정확한값(عميل,3)[1:])[0]
            for _ in range(항목수):
                الإحداثي_س,الزر_Y_إحداثيات,너비값,مطلوب_ارتفاع_قيمة,مجموعة_أحرف=struct.unpack('>HHHHi',정확한값(عميل,12));assert مجموعة_أحرف==0,مجموعة_أحرف
                بيانات=정확한값(عميل,너비값*مطلوب_ارتفاع_قيمة*4)
                for صف_منصب in range(مطلوب_ارتفاع_قيمة):
                    for عمود_منصب in range(너비값):
                        원본자료=(صف_منصب*너비값+عمود_منصب)*4;الهدف=((الزر_Y_إحداثيات+صف_منصب)*640+الإحداثي_س+عمود_منصب)*3
                        빛삼원색[الهدف:الهدف+3]=bytes((بيانات[원본자료+2],بيانات[원본자료+1],بيانات[원본자료]))
            if 항목수:return 빛삼원색
    try:
        يستلم_رسالة(b'TERMINAL READY');يستلم_رسالة(b'jkoros-native> ',نسخة_مكتوبة.rfind(b'TERMINAL READY'))
        رقم_المنفذ=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',نسخة_مكتوبة).group(1))
        عميل=socket.create_connection(('127.0.0.1',رقم_المنفذ),timeout=10)
        assert 정확한값(عميل,12)==b'RFB 003.008\n';عميل.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(عميل,정확한값(عميل,1)[0]);عميل.sendall(b'\x01');assert 정확한값(عميل,4)==b'\0'*4
        عميل.sendall(b'\x01');초기값=정확한값(عميل,24);정확한값(عميل,struct.unpack('>I',초기값[20:])[0])
        عميل.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        عميل.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in 셸('ftpd start')
        نقل_الملفات_صديق=ftplib.FTP();نقل_الملفات_صديق.encoding='utf-8';نقل_الملفات_صديق.connect('127.0.0.1',نقل_الملفات_رقم_المنفذ,timeout=20);نقل_الملفات_صديق.login()
        حمولة_بيانات=('GUI와 FTP 동시 يستخدم_قيمة '+لغة+' 😀\n').encode()
        نقل_الملفات_صديق.storbinary('STOR 함께.txt',io.BytesIO(حمولة_بيانات))
        assert حمولة_بيانات.decode().strip() in 셸('cat /함께.txt')
        받은수=bytearray();نقل_الملفات_صديق.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==حمولة_بيانات;نقل_الملفات_صديق.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        يرسل_قائمة=셸('ls /example')
        assert all(اسم in يرسل_قائمة for اسم in ('java/','c/','python/','README.md')),يرسل_قائمة
        if لغة=='java':
            يُجمع_بيان=json.loads((يعرض_جذر/'build/examples/manifest.json').read_text())
            for مسار,نقطة_الإدخال in يُجمع_بيان.items():
                셸('cp '+مسار+' /example-check.bin')
                محتوى_قيمة=bytearray();نقل_الملفات_صديق.retrbinary('RETR example-check.bin',محتوى_قيمة.extend)
                assert len(محتوى_قيمة)==نقطة_الإدخال['bytes'] and hashlib.sha256(محتوى_قيمة).hexdigest()==نقطة_الإدخال['sha256'],مسار
            نقل_الملفات_صديق.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            ثنائي=bytes(range(256))*64
            نقل_الملفات_صديق.storbinary('STOR boundary.bin',io.BytesIO(ثنائي))
            محتوى_قيمة=bytearray();نقل_الملفات_صديق.retrbinary('RETR boundary.bin',محتوى_قيمة.extend)
            assert محتوى_قيمة==ثنائي and 'boundary.bin' in نقل_الملفات_صديق.nlst()
            셸('cp /boundary.bin /boundary-copy.bin')
            محتوى_قيمة=bytearray();نقل_الملفات_صديق.retrbinary('RETR boundary-copy.bin',محتوى_قيمة.extend)
            assert محتوى_قيمة==ثنائي
            نقل_الملفات_صديق.delete('boundary.bin');نقل_الملفات_صديق.delete('boundary-copy.bin')
        assert 'مثالطباعة' in 셸('ls /example/'+لغة)
        셸('cd /example/'+لغة)
        اسم_جدول={'java':'JAVA','c':'C','python':'PYTHON'}[لغة]
        예상파일=اسم_جدول+' ملف: 한글 بيانات 😀\n'
        if لغة=='java':
            ينفذ_أمر('javac مثالطباعة.java','Compiled:');ينفذ_أمر('java مثالطباعة','JAVA مخرجات: 안녕하세요 😀')
            ينفذ_أمر('javac مثالملف.java','Compiled:');ينفذ_أمر('java مثالملف',예상파일)
            ينفذ_أمر('java مثالشبكة {} {}'.format(ارتداد_خادم_إدخال.TCP_منفذ,ارتداد_خادم_إدخال.بروتوكول_مخطط_بيانات_المستخدم_منفذ),'JAVA 네트워크 يتحقق: TCP UDP 한글')
            رسومات_أمر='java مثالرسم'
        elif لغة=='c':
            for اسم,전달값,예상결과 in [('مخرجات','', 'C مخرجات: 안녕하세요 😀'),('ملف','',예상파일),
                    ('네트워크',' '+str(ارتداد_خادم_إدخال.بروتوكول_مخطط_بيانات_المستخدم_منفذ),'C 네트워크 يتحقق: UDP 한글')]:
                ينفذ_أمر('cc '+اسم+'예제.c -o ينفذ_أمر','Compiled native ARM64 ELF:')
                ينفذ_أمر('./ينفذ_أمر'+전달값,예상결과)
            ينفذ_أمر('cc مثالرسم.c -o ينفذ_أمر','Compiled native ARM64 ELF:');رسومات_أمر='./ينفذ_أمر'
        else:
            for اسم,전달값,예상결과 in [('مخرجات','','PYTHON مخرجات: 안녕하세요 😀'),('ملف','',예상파일),
                    ('네트워크',' '+str(ارتداد_خادم_إدخال.بروتوكول_مخطط_بيانات_المستخدم_منفذ),'PYTHON 네트워크 يتحقق: UDP 한글')]:
                ينفذ_أمر('python '+اسم+'예제.py'+전달값,예상결과)
            رسومات_أمر='python مثالرسم.py'
        بدء_رسم=بدء_إزاحة(رسومات_أمر)
        نص=يستلم_رسالة('그림을 확인한 عودة_قيمة Enter를 누르세요.\r\n'.encode(),بدء_رسم)
        assert اسم_جدول+' 그래픽: 빨강 초록 파랑' in نص and 'exit 0' not in نص,نص
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        نقل_الملفات_صديق.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();نقل_الملفات_صديق.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';نقل_الملفات_صديق.delete('도중.txt')
        빛삼원색=화소들()
        for الزر_Y_إحداثيات,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            إزاحة_قيمة=(الزر_Y_إحداثيات*640+610)*3;assert tuple(빛삼원색[إزاحة_قيمة:إزاحة_قيمة+3])==색상,(لغة,الزر_Y_إحداثيات,tuple(빛삼원색[إزاحة_قيمة:إزاحة_قيمة+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(مقياس_بيانات/(لغة+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in يستلم_رسالة(b'jkoros-native> ',بدء_رسم)
        if لغة=='java':
            بدء_نافذة=بدء_إزاحة('java مثالنافذة')
            يستلم_رسالة('GUI 예제 إعداد: مثالنافذة'.encode(),بدء_نافذة)
            def نقرة_قيمة(가로,عمودي_منصب):
                for زر in (1,0):عميل.sendall(struct.pack('>BBHH',5,زر,가로,عمودي_منصب))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            نقرة_قيمة(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for حرف_قيمة in '한글':누름값(0x1000000|ord(حرف_قيمة));누름값(0x1000000|ord(حرف_قيمة),False)
            for 횟수 in (1,2):
                تشغيل=len(نسخة_مكتوبة);نقرة_قيمة(180,242)
                يستلم_رسالة(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),تشغيل)
            time.sleep(.3)
            نافذة_رسم=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=نافذة_رسم.crop((110,272,530,300)).tobytes()
            نافذة_رسم.save(str(مقياس_بيانات/'java-swing.png'))
            تشغيل=len(نسخة_مكتوبة);نقرة_قيمة(535,105)
            assert 'exit 0' in يستلم_رسالة(b'jkoros-native> ',تشغيل)
        # Download the guest-created bytes through FTP in the same GUI VM.
        ملف_إدخال_اسم={'java':'java.txt','c':'c.txt','python':'python.txt'}[لغة]
        셸('cp '+ملف_إدخال_اسم+' /التحقق_من_صحة.txt')
        받은수=bytearray();نقل_الملفات_صديق.retrbinary('RETR التحقق_من_صحة.txt',받은수.extend);assert 받은수==예상파일.encode()
        셸('echo preserved > مثالطباعة.'+('py' if لغة=='python' else لغة))
        assert 'EXAMPLES READY' in 셸('example '+لغة)
        assert '\npreserved\n' in 셸('cat مثالطباعة.'+('py' if لغة=='python' else لغة))
        assert '한/صفر_مُعامل مفتاح_قيمة, Shift+Space 또는 F9' in 셸('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in 셸('echo GUI NETWORK TOGETHER')
        نقل_الملفات_صديق.quit();نقل_الملفات_صديق=None;assert 'FTP stopped' in 셸('ftpd stop')
        print('PASS '+لغة+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if نقل_الملفات_صديق:
            try:نقل_الملفات_صديق.close()
            except OSError:pass
        if عميل:عميل.close()
        عملية.terminate()
        try:عملية.wait(timeout=8)
        except subprocess.TimeoutExpired:عملية.kill();عملية.wait()
        محدد.close();عملية.stdout.close();(مقياس_بيانات/(لغة+'-serial.log')).write_bytes(نسخة_مكتوبة)


def تشغيل():
    مقياس_بيانات=يعرض_جذر/'build/verification/examples';مقياس_بيانات.mkdir(parents=True,exist_ok=True)
    التحقق_من_صحة_إبلاغ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((يعرض_جذر/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with ارتداد_خوادم() as ارتداد_خادم_إدخال:
            for لغة in ('java','c','python'):
                يختبر_لغة(لغة,ارتداد_خادم_إدخال,مقياس_بيانات);التحقق_من_صحة_إبلاغ['languages'].append(لغة)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert ارتداد_خادم_إدخال.수신됨==[(فئة_قيمة,بيانات.encode()) for فئة_قيمة,بيانات in 예상결과],ارتداد_خادم_إدخال.수신됨
            التحقق_من_صحة_إبلاغ['host_network_payloads']=[{'protocol':فئة_قيمة,'text':بيانات.decode()} for فئة_قيمة,بيانات in ارتداد_خادم_إدخال.수신됨]
        التحقق_من_صحة_إبلاغ.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(مقياس_بيانات/'report.json').write_text(json.dumps(التحقق_من_صحة_إبلاغ,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':تشغيل()
