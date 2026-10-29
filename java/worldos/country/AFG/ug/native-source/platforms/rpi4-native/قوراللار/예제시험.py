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
from ئۈستەليۈزى_كۆرۈنمە import 정확한값
from 예제되돌림서버 import 되돌림서버
from ئىجرا_قىلىش_بۇيرۇق import كۆرسىتىش_يىلتىز


def test_언어(تىل,되돌림서버항목,ئۆلچەم_مەلۇمات):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    جەريان=subprocess.Popen(['python3',str(كۆرسىتىش_يىلتىز/'قوراللار/ئىجرا_قىلىش_بۇيرۇق.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    تاللىغۇچ=selectors.DefaultSelector();تاللىغۇچ.register(جەريان.stdout,selectors.EVENT_READ)
    대화기록=bytearray();ئابۇنىتېر=None;ھۆججەت_يوللاش_ئۇلىنىش=None
    def 수신하기(확인표시,ئىجرا_قىل_2=0):
        تاماملىماق_ئاغما=time.monotonic()+60
        while 확인표시 not in 대화기록[ئىجرا_قىل_2:]:
            if time.monotonic()>تاماملىماق_ئاغما or جەريان.poll() is not None:raise AssertionError(대화기록[ئىجرا_قىل_2:].decode('utf-8','replace'))
            for 누름값,_ in تاللىغۇچ.select(.1):
                مەلۇمات=누름값.fileobj.read(65536)
                if مەلۇمات:대화기록.extend(مەلۇمات)
        return 대화기록[ئىجرا_قىل_2:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(بەلگە_قىممىتى,누르는중=True):ئابۇنىتېر.sendall(struct.pack('>BBHI',4,int(누르는중),0,بەلگە_قىممىتى))
    def باشلاش_ئاغما(قۇر):
        ئىجرا_قىل_2=len(대화기록)
        for ھەرپ_كودى in قۇر+'\n':
            بەلگە_قىممىتى=0xff0d if ھەرپ_كودى=='\n' else ord(ھەرپ_كودى) if ord(ھەرپ_كودى)<256 else 0x1000000|ord(ھەرپ_كودى)
            누름값(بەلگە_قىممىتى);누름값(بەلگە_قىممىتى,False)
        return ئىجرا_قىل_2
    def قاپ(قۇر):return 수신하기(b'jkoros-native> ',باشلاش_ئاغما(قۇر))
    def ئىجرا_قىلىش_بۇيرۇق(قۇر,예상결과):
        تېكىست=قاپ(قۇر);assert 예상결과 in تېكىست and 'exit 0' in تېكىست,(قۇر,تېكىست)
        return تېكىست
    def 화소들():
        ئابۇنىتېر.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            تۈر_قىممىتى=정확한값(ئابۇنىتېر,1)[0]
            if تۈر_قىممىتى==2:continue
            if تۈر_قىممىتى==3:
                개수=struct.unpack('>I',정확한값(ئابۇنىتېر,7)[3:])[0];정확한값(ئابۇنىتېر,개수);continue
            assert تۈر_قىممىتى==0,تۈر_قىممىتى
            항목수=struct.unpack('>H',정확한값(ئابۇنىتېر,3)[1:])[0]
            for _ in range(항목수):
                x_كوردىنات,세로좌표,너비값,높이값,ھەرپ_بەلگە_توپلىمى=struct.unpack('>HHHHi',정확한값(ئابۇنىتېر,12));assert ھەرپ_بەلگە_توپلىمى==0,ھەرپ_بەلگە_توپلىمى
                مەلۇمات=정확한값(ئابۇنىتېر,너비값*높이값*4)
                for قۇر_ئورۇنلاشتۇرۇش in range(높이값):
                    for ئىستون_ئورۇنلاشتۇرۇش in range(너비값):
                        원본자료=(قۇر_ئورۇنلاشتۇرۇش*너비값+ئىستون_ئورۇنلاشتۇرۇش)*4;نىشان=((세로좌표+قۇر_ئورۇنلاشتۇرۇش)*640+x_كوردىنات+ئىستون_ئورۇنلاشتۇرۇش)*3
                        빛삼원색[نىشان:نىشان+3]=bytes((مەلۇمات[원본자료+2],مەلۇمات[원본자료+1],مەلۇمات[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        ئابۇنىتېر=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert 정확한값(ئابۇنىتېر,12)==b'RFB 003.008\n';ئابۇنىتېر.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(ئابۇنىتېر,정확한값(ئابۇنىتېر,1)[0]);ئابۇنىتېر.sendall(b'\x01');assert 정확한값(ئابۇنىتېر,4)==b'\0'*4
        ئابۇنىتېر.sendall(b'\x01');초기값=정확한값(ئابۇنىتېر,24);정확한값(ئابۇنىتېر,struct.unpack('>I',초기값[20:])[0])
        ئابۇنىتېر.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        ئابۇنىتېر.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in قاپ('ftpd start')
        ھۆججەت_يوللاش_ئۇلىنىش=ftplib.FTP();ھۆججەت_يوللاش_ئۇلىنىش.encoding='utf-8';ھۆججەت_يوللاش_ئۇلىنىش.connect('127.0.0.1',파일전송접속번호,timeout=20);ھۆججەت_يوللاش_ئۇلىنىش.login()
        يۈك_مەلۇمات=('GUI와 FTP 동시 사용 '+تىل+' 😀\n').encode()
        ھۆججەت_يوللاش_ئۇلىنىش.storbinary('STOR 함께.txt',io.BytesIO(يۈك_مەلۇمات))
        assert يۈك_مەلۇمات.decode().strip() in قاپ('cat /함께.txt')
        받은수=bytearray();ھۆججەت_يوللاش_ئۇلىنىش.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==يۈك_مەلۇمات;ھۆججەت_يوللاش_ئۇلىنىش.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        ئەۋەتمەك_تىزىم=قاپ('ls /example')
        assert all(ئاتى in ئەۋەتمەك_تىزىم for ئاتى in ('java/','c/','python/','README.md')),ئەۋەتمەك_تىزىم
        if تىل=='java':
            꾸러미명세=json.loads((كۆرسىتىش_يىلتىز/'build/examples/manifest.json').read_text())
            for يول,كىرگۈزۈش_نوقتا in 꾸러미명세.items():
                قاپ('cp '+يول+' /example-check.bin')
                مەزمۇن_قىممىتى=bytearray();ھۆججەت_يوللاش_ئۇلىنىش.retrbinary('RETR example-check.bin',مەزمۇن_قىممىتى.extend)
                assert len(مەزمۇن_قىممىتى)==كىرگۈزۈش_نوقتا['bytes'] and hashlib.sha256(مەزمۇن_قىممىتى).hexdigest()==كىرگۈزۈش_نوقتا['sha256'],يول
            ھۆججەت_يوللاش_ئۇلىنىش.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            ئىككىلىك=bytes(range(256))*64
            ھۆججەت_يوللاش_ئۇلىنىش.storbinary('STOR boundary.bin',io.BytesIO(ئىككىلىك))
            مەزمۇن_قىممىتى=bytearray();ھۆججەت_يوللاش_ئۇلىنىش.retrbinary('RETR boundary.bin',مەزمۇن_قىممىتى.extend)
            assert مەزمۇن_قىممىتى==ئىككىلىك and 'boundary.bin' in ھۆججەت_يوللاش_ئۇلىنىش.nlst()
            قاپ('cp /boundary.bin /boundary-copy.bin')
            مەزمۇن_قىممىتى=bytearray();ھۆججەت_يوللاش_ئۇلىنىش.retrbinary('RETR boundary-copy.bin',مەزمۇن_قىممىتى.extend)
            assert مەزمۇن_قىممىتى==ئىككىلىك
            ھۆججەت_يوللاش_ئۇلىنىش.delete('boundary.bin');ھۆججەت_يوللاش_ئۇلىنىش.delete('boundary-copy.bin')
        assert '출력예제' in قاپ('ls /example/'+تىل)
        قاپ('cd /example/'+تىل)
        نامى_جەدۋەل={'java':'JAVA','c':'C','python':'PYTHON'}[تىل]
        예상파일=نامى_جەدۋەل+' ھۆججەت: 한글 مەلۇمات 😀\n'
        if تىل=='java':
            ئىجرا_قىلىش_بۇيرۇق('javac 출력예제.java','Compiled:');ئىجرا_قىلىش_بۇيرۇق('java 출력예제','JAVA چىقار: 안녕하세요 😀')
            ئىجرا_قىلىش_بۇيرۇق('javac 파일예제.java','Compiled:');ئىجرا_قىلىش_بۇيرۇق('java 파일예제',예상파일)
            ئىجرا_قىلىش_بۇيرۇق('java 네트워크예제 {} {}'.format(되돌림서버항목.يەتكۈزۈش_كونترول_كېلىشىمى_ئېغىز,되돌림서버항목.전문접속번호),'JAVA 네트워크 دەلىللىمەك: TCP UDP 한글')
            گرافىكلار_بۇيرۇق='java 그래픽예제'
        elif تىل=='c':
            for ئاتى,전달값,예상결과 in [('چىقار','', 'C چىقار: 안녕하세요 😀'),('ھۆججەت','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 دەلىللىمەك: UDP 한글')]:
                ئىجرا_قىلىش_بۇيرۇق('cc '+ئاتى+'예제.c -o ئىجرا_قىلىش_بۇيرۇق','Compiled native ARM64 ELF:')
                ئىجرا_قىلىش_بۇيرۇق('./ئىجرا_قىلىش_بۇيرۇق'+전달값,예상결과)
            ئىجرا_قىلىش_بۇيرۇق('cc 그래픽예제.c -o ئىجرا_قىلىش_بۇيرۇق','Compiled native ARM64 ELF:');گرافىكلار_بۇيرۇق='./ئىجرا_قىلىش_بۇيرۇق'
        else:
            for ئاتى,전달값,예상결과 in [('چىقار','','PYTHON چىقار: 안녕하세요 😀'),('ھۆججەت','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 دەلىللىمەك: UDP 한글')]:
                ئىجرا_قىلىش_بۇيرۇق('python '+ئاتى+'예제.py'+전달값,예상결과)
            گرافىكلار_بۇيرۇق='python 그래픽예제.py'
        باشلاش_سىزىش=باشلاش_ئاغما(گرافىكلار_بۇيرۇق)
        تېكىست=수신하기('그림을 확인한 ئارقىغا_قىممىتى Enter를 누르세요.\r\n'.encode(),باشلاش_سىزىش)
        assert نامى_جەدۋەل+' 그래픽: 빨강 초록 파랑' in تېكىست and 'exit 0' not in تېكىست,تېكىست
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        ھۆججەت_يوللاش_ئۇلىنىش.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();ھۆججەت_يوللاش_ئۇلىنىش.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';ھۆججەت_يوللاش_ئۇلىنىش.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            ئاغما_قىممىتى=(세로좌표*640+610)*3;assert tuple(빛삼원색[ئاغما_قىممىتى:ئاغما_قىممىتى+3])==색상,(تىل,세로좌표,tuple(빛삼원색[ئاغما_قىممىتى:ئاغما_قىممىتى+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(ئۆلچەم_مەلۇمات/(تىل+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',باشلاش_سىزىش)
        if تىل=='java':
            باشلاش_كۆزنەك=باشلاش_ئاغما('java 창예제')
            수신하기('GUI 예제 تەييارلىماق: 창예제'.encode(),باشلاش_كۆزنەك)
            def چەكمەك_قىممىتى(가로,تىك_ئورۇنلاشتۇرۇش):
                for كۇنۇپكا in (1,0):ئابۇنىتېر.sendall(struct.pack('>BBHH',5,كۇنۇپكا,가로,تىك_ئورۇنلاشتۇرۇش))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            چەكمەك_قىممىتى(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for ھەرپ_بەلگە_قىممىتى in '한글':누름값(0x1000000|ord(ھەرپ_بەلگە_قىممىتى));누름값(0x1000000|ord(ھەرپ_بەلگە_قىممىتى),False)
            for 횟수 in (1,2):
                ئىجرا_قىل_2=len(대화기록);چەكمەك_قىممىتى(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),ئىجرا_قىل_2)
            time.sleep(.3)
            كۆزنەك_سىزىش=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=كۆزنەك_سىزىش.crop((110,272,530,300)).tobytes()
            كۆزنەك_سىزىش.save(str(ئۆلچەم_مەلۇمات/'java-swing.png'))
            ئىجرا_قىل_2=len(대화기록);چەكمەك_قىممىتى(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',ئىجرا_قىل_2)
        # Download the guest-created bytes through FTP in the same GUI VM.
        ھۆججەت_كىرگۈزۈش_نامى={'java':'java.txt','c':'c.txt','python':'python.txt'}[تىل]
        قاپ('cp '+ھۆججەت_كىرگۈزۈش_نامى+' /دەلىللەش.txt')
        받은수=bytearray();ھۆججەت_يوللاش_ئۇلىنىش.retrbinary('RETR دەلىللەش.txt',받은수.extend);assert 받은수==예상파일.encode()
        قاپ('echo preserved > 출력예제.'+('py' if تىل=='python' else تىل))
        assert 'EXAMPLES READY' in قاپ('example '+تىل)
        assert '\npreserved\n' in قاپ('cat 출력예제.'+('py' if تىل=='python' else تىل))
        assert '한/영 ئاچقۇچ_قىممىتى, Shift+Space 또는 F9' in قاپ('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in قاپ('echo GUI NETWORK TOGETHER')
        ھۆججەت_يوللاش_ئۇلىنىش.quit();ھۆججەت_يوللاش_ئۇلىنىش=None;assert 'FTP stopped' in قاپ('ftpd stop')
        print('PASS '+تىل+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if ھۆججەت_يوللاش_ئۇلىنىش:
            try:ھۆججەت_يوللاش_ئۇلىنىش.close()
            except OSError:pass
        if ئابۇنىتېر:ئابۇنىتېر.close()
        جەريان.terminate()
        try:جەريان.wait(timeout=8)
        except subprocess.TimeoutExpired:جەريان.kill();جەريان.wait()
        تاللىغۇچ.close();جەريان.stdout.close();(ئۆلچەم_مەلۇمات/(تىل+'-serial.log')).write_bytes(대화기록)


def ئىجرا_قىل_2():
    ئۆلچەم_مەلۇمات=كۆرسىتىش_يىلتىز/'build/verification/examples';ئۆلچەم_مەلۇمات.mkdir(parents=True,exist_ok=True)
    دەلىللەش_خەۋەر={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((كۆرسىتىش_يىلتىز/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for تىل in ('java','c','python'):
                test_언어(تىل,되돌림서버항목,ئۆلچەم_مەلۇمات);دەلىللەش_خەۋەر['languages'].append(تىل)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(تۈر_قىممىتى,مەلۇمات.encode()) for تۈر_قىممىتى,مەلۇمات in 예상결과],되돌림서버항목.수신됨
            دەلىللەش_خەۋەر['host_network_payloads']=[{'protocol':تۈر_قىممىتى,'text':مەلۇمات.decode()} for تۈر_قىممىتى,مەلۇمات in 되돌림서버항목.수신됨]
        دەلىللەش_خەۋەر.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(ئۆلچەم_مەلۇمات/'report.json').write_text(json.dumps(دەلىللەش_خەۋەر,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':ئىجرا_قىل_2()
