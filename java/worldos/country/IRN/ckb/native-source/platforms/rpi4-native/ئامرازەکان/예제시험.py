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
from دێسکتۆپ_دیمەن import 정확한값
from 예제되돌림서버 import 되돌림서버
from جێبەجێکردن_فەرمان import 기준


def test_언어(زمان,되돌림서버항목,결과자료):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    پرۆسە=subprocess.Popen(['python3',str(기준/'ئامرازەکان/جێبەجێکردن_فەرمان.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    هەڵبژێرەر=selectors.DefaultSelector();هەڵبژێرەر.register(پرۆسە.stdout,selectors.EVENT_READ)
    대화기록=bytearray();کلایەنت=None;فایل_گواستنەوە_گرێدان=None
    def 수신하기(확인표시,ڕادان=0):
        دوایی_کردن_ئۆفسێت=time.monotonic()+60
        while 확인표시 not in 대화기록[ڕادان:]:
            if time.monotonic()>دوایی_کردن_ئۆفسێت or پرۆسە.poll() is not None:raise AssertionError(대화기록[ڕادان:].decode('utf-8','replace'))
            for 누름값,_ in هەڵبژێرەر.select(.1):
                دەیتا=누름값.fileobj.read(65536)
                if دەیتا:대화기록.extend(دەیتا)
        return 대화기록[ڕادان:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(سیمبۆل_نرخ,누르는중=True):کلایەنت.sendall(struct.pack('>BBHI',4,int(누르는중),0,سیمبۆل_نرخ))
    def دەستپێك_ئۆفسێت(دێڕ):
        ڕادان=len(대화기록)
        for کۆدی_نووسە in دێڕ+'\n':
            سیمبۆل_نرخ=0xff0d if کۆدی_نووسە=='\n' else ord(کۆدی_نووسە) if ord(کۆدی_نووسە)<256 else 0x1000000|ord(کۆدی_نووسە)
            누름값(سیمبۆل_نرخ);누름값(سیمبۆل_نرخ,False)
        return ڕادان
    def توێکڵ(دێڕ):return 수신하기(b'jkoros-native> ',دەستپێك_ئۆفسێت(دێڕ))
    def جێبەجێکردن_فەرمان(دێڕ,예상결과):
        دەق=توێکڵ(دێڕ);assert 예상결과 in دەق and 'exit 0' in دەق,(دێڕ,دەق)
        return دەق
    def 화소들():
        کلایەنت.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            پۆل_نرخ=정확한값(کلایەنت,1)[0]
            if پۆل_نرخ==2:continue
            if پۆل_نرخ==3:
                개수=struct.unpack('>I',정확한값(کلایەنت,7)[3:])[0];정확한값(کلایەنت,개수);continue
            assert پۆل_نرخ==0,پۆل_نرخ
            항목수=struct.unpack('>H',정확한값(کلایەنت,3)[1:])[0]
            for _ in range(항목수):
                پۆوتانی_x,세로좌표,너비값,높이값,کۆمەڵە_نووسە=struct.unpack('>HHHHi',정확한값(کلایەنت,12));assert کۆمەڵە_نووسە==0,کۆمەڵە_نووسە
                دەیتا=정확한값(کلایەنت,너비값*높이값*4)
                for 행위치 in range(높이값):
                    for 열위치 in range(너비값):
                        원본자료=(행위치*너비값+열위치)*4;مەبەست=((세로좌표+행위치)*640+پۆوتانی_x+열위치)*3
                        빛삼원색[مەبەست:مەبەست+3]=bytes((دەیتا[원본자료+2],دەیتا[원본자료+1],دەیتا[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        کلایەنت=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert 정확한값(کلایەنت,12)==b'RFB 003.008\n';کلایەنت.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(کلایەنت,정확한값(کلایەنت,1)[0]);کلایەنت.sendall(b'\x01');assert 정확한값(کلایەنت,4)==b'\0'*4
        کلایەنت.sendall(b'\x01');초기값=정확한값(کلایەنت,24);정확한값(کلایەنت,struct.unpack('>I',초기값[20:])[0])
        کلایەنت.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        کلایەنت.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in توێکڵ('ftpd start')
        فایل_گواستنەوە_گرێدان=ftplib.FTP();فایل_گواستنەوە_گرێدان.encoding='utf-8';فایل_گواستنەوە_گرێدان.connect('127.0.0.1',파일전송접속번호,timeout=20);فایل_گواستنەوە_گرێدان.login()
        بارگەى_كرێ_دەیتا=('GUI와 FTP 동시 사용 '+زمان+' 😀\n').encode()
        فایل_گواستنەوە_گرێدان.storbinary('STOR 함께.txt',io.BytesIO(بارگەى_كرێ_دەیتا))
        assert بارگەى_كرێ_دەیتا.decode().strip() in توێکڵ('cat /함께.txt')
        받은수=bytearray();فایل_گواستنەوە_گرێدان.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==بارگەى_كرێ_دەیتا;فایل_گواستنەوە_گرێدان.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        ناردن_لیست=توێکڵ('ls /example')
        assert all(ناو in ناردن_لیست for ناو in ('java/','c/','python/','README.md')),ناردن_لیست
        if زمان=='java':
            꾸러미명세=json.loads((기준/'build/examples/manifest.json').read_text())
            for گوزەر,تێنووسین_خاڵ in 꾸러미명세.items():
                توێکڵ('cp '+گوزەر+' /example-check.bin')
                ناوەرۆک_نرخ=bytearray();فایل_گواستنەوە_گرێدان.retrbinary('RETR example-check.bin',ناوەرۆک_نرخ.extend)
                assert len(ناوەرۆک_نرخ)==تێنووسین_خاڵ['bytes'] and hashlib.sha256(ناوەرۆک_نرخ).hexdigest()==تێنووسین_خاڵ['sha256'],گوزەر
            فایل_گواستنەوە_گرێدان.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            دوانەیی=bytes(range(256))*64
            فایل_گواستنەوە_گرێدان.storbinary('STOR boundary.bin',io.BytesIO(دوانەیی))
            ناوەرۆک_نرخ=bytearray();فایل_گواستنەوە_گرێدان.retrbinary('RETR boundary.bin',ناوەرۆک_نرخ.extend)
            assert ناوەرۆک_نرخ==دوانەیی and 'boundary.bin' in فایل_گواستنەوە_گرێدان.nlst()
            توێکڵ('cp /boundary.bin /boundary-copy.bin')
            ناوەرۆک_نرخ=bytearray();فایل_گواستنەوە_گرێدان.retrbinary('RETR boundary-copy.bin',ناوەرۆک_نرخ.extend)
            assert ناوەرۆک_نرخ==دوانەیی
            فایل_گواستنەوە_گرێدان.delete('boundary.bin');فایل_گواستنەوە_گرێدان.delete('boundary-copy.bin')
        assert '출력예제' in توێکڵ('ls /example/'+زمان)
        توێکڵ('cd /example/'+زمان)
        ناو_خشتە={'java':'JAVA','c':'C','python':'PYTHON'}[زمان]
        예상파일=ناو_خشتە+' فایل: 한글 دەیتا 😀\n'
        if زمان=='java':
            جێبەجێکردن_فەرمان('javac 출력예제.java','Compiled:');جێبەجێکردن_فەرمان('java 출력예제','JAVA 출력: 안녕하세요 😀')
            جێبەجێکردن_فەرمان('javac 파일예제.java','Compiled:');جێبەجێکردن_فەرمان('java 파일예제',예상파일)
            جێبەجێکردن_فەرمان('java 네트워크예제 {} {}'.format(되돌림서버항목.TCP_دەرگا,되돌림서버항목.전문접속번호),'JAVA 네트워크 سەلماندن: TCP UDP 한글')
            그림명령='java 그래픽예제'
        elif زمان=='c':
            for ناو,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('فایل','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 سەلماندن: UDP 한글')]:
                جێبەجێکردن_فەرمان('cc '+ناو+'예제.c -o جێبەجێکردن_فەرمان','Compiled native ARM64 ELF:')
                جێبەجێکردن_فەرمان('./جێبەجێکردن_فەرمان'+전달값,예상결과)
            جێبەجێکردن_فەرمان('cc 그래픽예제.c -o جێبەجێکردن_فەرمان','Compiled native ARM64 ELF:');그림명령='./جێبەجێکردن_فەرمان'
        else:
            for ناو,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('فایل','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 سەلماندن: UDP 한글')]:
                جێبەجێکردن_فەرمان('python '+ناو+'예제.py'+전달값,예상결과)
            그림명령='python 그래픽예제.py'
        دەستپێك_نگار=دەستپێك_ئۆفسێت(그림명령)
        دەق=수신하기('그림을 확인한 دواوە_نرخ Enter를 누르세요.\r\n'.encode(),دەستپێك_نگار)
        assert ناو_خشتە+' 그래픽: 빨강 초록 파랑' in دەق and 'exit 0' not in دەق,دەق
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        فایل_گواستنەوە_گرێدان.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();فایل_گواستنەوە_گرێدان.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';فایل_گواستنەوە_گرێدان.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            ئۆفسێت_نرخ=(세로좌표*640+610)*3;assert tuple(빛삼원색[ئۆفسێت_نرخ:ئۆفسێت_نرخ+3])==색상,(زمان,세로좌표,tuple(빛삼원색[ئۆفسێت_نرخ:ئۆفسێت_نرخ+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(결과자료/(زمان+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',دەستپێك_نگار)
        if زمان=='java':
            دەستپێك_پەنجەرە=دەستپێك_ئۆفسێت('java 창예제')
            수신하기('GUI 예제 ئامادە_کردن_9ce364fc: 창예제'.encode(),دەستپێك_پەنجەرە)
            def کرته_کردن_نرخ(가로,세로):
                for دوگمه in (1,0):کلایەنت.sendall(struct.pack('>BBHH',5,دوگمه,가로,세로))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            کرته_کردن_نرخ(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for نووسە_نرخ in '한글':누름값(0x1000000|ord(نووسە_نرخ));누름값(0x1000000|ord(نووسە_نرخ),False)
            for 횟수 in (1,2):
                ڕادان=len(대화기록);کرته_کردن_نرخ(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),ڕادان)
            time.sleep(.3)
            پەنجەرە_نگار=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=پەنجەرە_نگار.crop((110,272,530,300)).tobytes()
            پەنجەرە_نگار.save(str(결과자료/'java-swing.png'))
            ڕادان=len(대화기록);کرته_کردن_نرخ(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',ڕادان)
        # Download the guest-created bytes through FTP in the same GUI VM.
        فایل_تێنووسین_ناو={'java':'java.txt','c':'c.txt','python':'python.txt'}[زمان]
        توێکڵ('cp '+فایل_تێنووسین_ناو+' /ڕەوایی.txt')
        받은수=bytearray();فایل_گواستنەوە_گرێدان.retrbinary('RETR ڕەوایی.txt',받은수.extend);assert 받은수==예상파일.encode()
        توێکڵ('echo preserved > 출력예제.'+('py' if زمان=='python' else زمان))
        assert 'EXAMPLES READY' in توێکڵ('example '+زمان)
        assert '\npreserved\n' in توێکڵ('cat 출력예제.'+('py' if زمان=='python' else زمان))
        assert '한/영 کلیل_نرخ, Shift+Space 또는 F9' in توێکڵ('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in توێکڵ('echo GUI NETWORK TOGETHER')
        فایل_گواستنەوە_گرێدان.quit();فایل_گواستنەوە_گرێدان=None;assert 'FTP stopped' in توێکڵ('ftpd stop')
        print('PASS '+زمان+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if فایل_گواستنەوە_گرێدان:
            try:فایل_گواستنەوە_گرێدان.close()
            except OSError:pass
        if کلایەنت:کلایەنت.close()
        پرۆسە.terminate()
        try:پرۆسە.wait(timeout=8)
        except subprocess.TimeoutExpired:پرۆسە.kill();پرۆسە.wait()
        هەڵبژێرەر.close();پرۆسە.stdout.close();(결과자료/(زمان+'-serial.log')).write_bytes(대화기록)


def ڕادان():
    결과자료=기준/'build/verification/examples';결과자료.mkdir(parents=True,exist_ok=True)
    ڕەواکردن_ڕاپۆرت={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for زمان in ('java','c','python'):
                test_언어(زمان,되돌림서버항목,결과자료);ڕەواکردن_ڕاپۆرت['languages'].append(زمان)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(پۆل_نرخ,دەیتا.encode()) for پۆل_نرخ,دەیتا in 예상결과],되돌림서버항목.수신됨
            ڕەواکردن_ڕاپۆرت['host_network_payloads']=[{'protocol':پۆل_نرخ,'text':دەیتا.decode()} for پۆل_نرخ,دەیتا in 되돌림서버항목.수신됨]
        ڕەواکردن_ڕاپۆرت.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(결과자료/'report.json').write_text(json.dumps(ڕەواکردن_ڕاپۆرت,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':ڕادان()
