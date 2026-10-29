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
from ডেস্কটপ_দর্শন import 정확한값
from 예제되돌림서버 import 되돌림서버
from নিষ্পাদন_আদেশ import 기준


def test_언어(ভাষা,되돌림서버항목,পৰিমাপ_ডাটা):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    প্ৰসেস=subprocess.Popen(['python3',str(기준/'সঁজুলিসমূহ/নিষ্পাদন_আদেশ.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    চয়নকাৰী=selectors.DefaultSelector();চয়নকাৰী.register(প্ৰসেস.stdout,selectors.EVENT_READ)
    대화기록=bytearray();ক্লায়েণ্ট=None;ফাইল_স্থানান্তৰণ_সংযোগ=None
    def 수신하기(확인표시,সঞ্চালন=0):
        অন্ত_কৰক_অফছেট=time.monotonic()+60
        while 확인표시 not in 대화기록[সঞ্চালন:]:
            if time.monotonic()>অন্ত_কৰক_অফছেট or প্ৰসেস.poll() is not None:raise AssertionError(대화기록[সঞ্চালন:].decode('utf-8','replace'))
            for 누름값,_ in চয়নকাৰী.select(.1):
                ডাটা=누름값.fileobj.read(65536)
                if ডাটা:대화기록.extend(ডাটা)
        return 대화기록[সঞ্চালন:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(প্ৰতীক_মান,누르는중=True):ক্লায়েণ্ট.sendall(struct.pack('>BBHI',4,int(누르는중),0,প্ৰতীক_মান))
    def আৰম্ভ_অফছেট(লাইন):
        সঞ্চালন=len(대화기록)
        for বৰ্ণ_ক_ড in লাইন+'\n':
            প্ৰতীক_মান=0xff0d if বৰ্ণ_ক_ড=='\n' else ord(বৰ্ণ_ক_ড) if ord(বৰ্ণ_ক_ড)<256 else 0x1000000|ord(বৰ্ণ_ক_ড)
            누름값(প্ৰতীক_মান);누름값(প্ৰতীক_মান,False)
        return সঞ্চালন
    def শ্বেল(লাইন):return 수신하기(b'jkoros-native> ',আৰম্ভ_অফছেট(লাইন))
    def নিষ্পাদন_আদেশ(লাইন,예상결과):
        টেক্সট=শ্বেল(লাইন);assert 예상결과 in টেক্সট and 'exit 0' in টেক্সট,(লাইন,টেক্সট)
        return টেক্সট
    def 화소들():
        ক্লায়েণ্ট.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            বর্গ_মান=정확한값(ক্লায়েণ্ট,1)[0]
            if বর্গ_মান==2:continue
            if বর্গ_মান==3:
                개수=struct.unpack('>I',정확한값(ক্লায়েণ্ট,7)[3:])[0];정확한값(ক্লায়েণ্ট,개수);continue
            assert বর্গ_মান==0,বর্গ_মান
            항목수=struct.unpack('>H',정확한값(ক্লায়েণ্ট,3)[1:])[0]
            for _ in range(항목수):
                x_ক_ৰ্ডিনেট,세로좌표,너비값,높이값,বৰ্ণ_ছেট=struct.unpack('>HHHHi',정확한값(ক্লায়েণ্ট,12));assert বৰ্ণ_ছেট==0,বৰ্ণ_ছেট
                ডাটা=정확한값(ক্লায়েণ্ট,너비값*높이값*4)
                for শাৰী_স্থান_সলনি_কৰক in range(높이값):
                    for স্তম্ভ_স্থান_সলনি_কৰক in range(너비값):
                        원본자료=(শাৰী_স্থান_সলনি_কৰক*너비값+স্তম্ভ_স্থান_সলনি_কৰক)*4;লক্ষ্য=((세로좌표+শাৰী_স্থান_সলনি_কৰক)*640+x_ক_ৰ্ডিনেট+স্তম্ভ_স্থান_সলনি_কৰক)*3
                        빛삼원색[লক্ষ্য:লক্ষ্য+3]=bytes((ডাটা[원본자료+2],ডাটা[원본자료+1],ডাটা[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        ক্লায়েণ্ট=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert 정확한값(ক্লায়েণ্ট,12)==b'RFB 003.008\n';ক্লায়েণ্ট.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(ক্লায়েণ্ট,정확한값(ক্লায়েণ্ট,1)[0]);ক্লায়েণ্ট.sendall(b'\x01');assert 정확한값(ক্লায়েণ্ট,4)==b'\0'*4
        ক্লায়েণ্ট.sendall(b'\x01');초기값=정확한값(ক্লায়েণ্ট,24);정확한값(ক্লায়েণ্ট,struct.unpack('>I',초기값[20:])[0])
        ক্লায়েণ্ট.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        ক্লায়েণ্ট.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in শ্বেল('ftpd start')
        ফাইল_স্থানান্তৰণ_সংযোগ=ftplib.FTP();ফাইল_স্থানান্তৰণ_সংযোগ.encoding='utf-8';ফাইল_স্থানান্তৰণ_সংযোগ.connect('127.0.0.1',파일전송접속번호,timeout=20);ফাইল_স্থানান্তৰণ_সংযোগ.login()
        প্লেল_ড_ডাটা=('GUI와 FTP 동시 사용 '+ভাষা+' 😀\n').encode()
        ফাইল_স্থানান্তৰণ_সংযোগ.storbinary('STOR 함께.txt',io.BytesIO(প্লেল_ড_ডাটা))
        assert প্লেল_ড_ডাটা.decode().strip() in শ্বেল('cat /함께.txt')
        받은수=bytearray();ফাইল_স্থানান্তৰণ_সংযোগ.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==প্লেল_ড_ডাটা;ফাইল_স্থানান্তৰণ_সংযোগ.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        ই_মেইল_কৰক_সূচী=শ্বেল('ls /example')
        assert all(নাম in ই_মেইল_কৰক_সূচী for নাম in ('java/','c/','python/','README.md')),ই_মেইল_কৰক_সূচী
        if ভাষা=='java':
            꾸러미명세=json.loads((기준/'build/examples/manifest.json').read_text())
            for পথ,প্রবিষ্ট_পইণ্ট in 꾸러미명세.items():
                শ্বেল('cp '+পথ+' /example-check.bin')
                সামগ্ৰী_মান=bytearray();ফাইল_স্থানান্তৰণ_সংযোগ.retrbinary('RETR example-check.bin',সামগ্ৰী_মান.extend)
                assert len(সামগ্ৰী_মান)==প্রবিষ্ট_পইণ্ট['bytes'] and hashlib.sha256(সামগ্ৰী_মান).hexdigest()==প্রবিষ্ট_পইণ্ট['sha256'],পথ
            ফাইল_স্থানান্তৰণ_সংযোগ.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            বাইনেৰি=bytes(range(256))*64
            ফাইল_স্থানান্তৰণ_সংযোগ.storbinary('STOR boundary.bin',io.BytesIO(বাইনেৰি))
            সামগ্ৰী_মান=bytearray();ফাইল_স্থানান্তৰণ_সংযোগ.retrbinary('RETR boundary.bin',সামগ্ৰী_মান.extend)
            assert সামগ্ৰী_মান==বাইনেৰি and 'boundary.bin' in ফাইল_স্থানান্তৰণ_সংযোগ.nlst()
            শ্বেল('cp /boundary.bin /boundary-copy.bin')
            সামগ্ৰী_মান=bytearray();ফাইল_স্থানান্তৰণ_সংযোগ.retrbinary('RETR boundary-copy.bin',সামগ্ৰী_মান.extend)
            assert সামগ্ৰী_মান==বাইনেৰি
            ফাইল_স্থানান্তৰণ_সংযোগ.delete('boundary.bin');ফাইল_স্থানান্তৰণ_সংযোগ.delete('boundary-copy.bin')
        assert '출력예제' in শ্বেল('ls /example/'+ভাষা)
        শ্বেল('cd /example/'+ভাষা)
        নাম_তালিকা={'java':'JAVA','c':'C','python':'PYTHON'}[ভাষা]
        예상파일=নাম_তালিকা+' নথিপত্ৰ: 한글 ডাটা 😀\n'
        if ভাষা=='java':
            নিষ্পাদন_আদেশ('javac 출력예제.java','Compiled:');নিষ্পাদন_আদেশ('java 출력예제','JAVA নিৰ্গম: 안녕하세요 😀')
            নিষ্পাদন_আদেশ('javac 파일예제.java','Compiled:');নিষ্পাদন_আদেশ('java 파일예제',예상파일)
            নিষ্পাদন_আদেশ('java 네트워크예제 {} {}'.format(되돌림서버항목.প্রচাৰণ_নিয়ন্ত্রণ_প্ৰ_ট_ক_ল_পৰ্ট,되돌림서버항목.전문접속번호),'JAVA 네트워크 প্ৰমাণিত_কৰক: TCP UDP 한글')
            গ্ৰাফিক্স_আদেশ='java 그래픽예제'
        elif ভাষা=='c':
            for নাম,전달값,예상결과 in [('নিৰ্গম','', 'C নিৰ্গম: 안녕하세요 😀'),('নথিপত্ৰ','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 প্ৰমাণিত_কৰক: UDP 한글')]:
                নিষ্পাদন_আদেশ('cc '+নাম+'예제.c -o নিষ্পাদন_আদেশ','Compiled native ARM64 ELF:')
                নিষ্পাদন_আদেশ('./নিষ্পাদন_আদেশ'+전달값,예상결과)
            নিষ্পাদন_আদেশ('cc 그래픽예제.c -o নিষ্পাদন_আদেশ','Compiled native ARM64 ELF:');গ্ৰাফিক্স_আদেশ='./নিষ্পাদন_আদেশ'
        else:
            for নাম,전달값,예상결과 in [('নিৰ্গম','','PYTHON নিৰ্গম: 안녕하세요 😀'),('নথিপত্ৰ','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 প্ৰমাণিত_কৰক: UDP 한글')]:
                নিষ্পাদন_আদেশ('python '+নাম+'예제.py'+전달값,예상결과)
            গ্ৰাফিক্স_আদেশ='python 그래픽예제.py'
        আৰম্ভ_অংকন=আৰম্ভ_অফছেট(গ্ৰাফিক্স_আদেশ)
        টেক্সট=수신하기('그림을 확인한 পাছলৈ_মান Enter를 누르세요.\r\n'.encode(),আৰম্ভ_অংকন)
        assert নাম_তালিকা+' 그래픽: 빨강 초록 파랑' in টেক্সট and 'exit 0' not in টেক্সট,টেক্সট
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        ফাইল_স্থানান্তৰণ_সংযোগ.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();ফাইল_স্থানান্তৰণ_সংযোগ.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';ফাইল_স্থানান্তৰণ_সংযোগ.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            অফছেট_মান=(세로좌표*640+610)*3;assert tuple(빛삼원색[অফছেট_মান:অফছেট_মান+3])==색상,(ভাষা,세로좌표,tuple(빛삼원색[অফছেট_মান:অফছেট_মান+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(পৰিমাপ_ডাটা/(ভাষা+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',আৰম্ভ_অংকন)
        if ভাষা=='java':
            আৰম্ভ_উইণ্ড=আৰম্ভ_অফছেট('java 창예제')
            수신하기('GUI 예제 প্ৰস্তুত_কৰক: 창예제'.encode(),আৰম্ভ_উইণ্ড)
            def ক্লিক_কৰক_মান(가로,উলম্ব_স্থান_সলনি_কৰক):
                for বুটাম in (1,0):ক্লায়েণ্ট.sendall(struct.pack('>BBHH',5,বুটাম,가로,উলম্ব_স্থান_সলনি_কৰক))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            ক্লিক_কৰক_মান(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for বৰ্ণ_মান in '한글':누름값(0x1000000|ord(বৰ্ণ_মান));누름값(0x1000000|ord(বৰ্ণ_মান),False)
            for 횟수 in (1,2):
                সঞ্চালন=len(대화기록);ক্লিক_কৰক_মান(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),সঞ্চালন)
            time.sleep(.3)
            উইণ্ড_অংকন=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=উইণ্ড_অংকন.crop((110,272,530,300)).tobytes()
            উইণ্ড_অংকন.save(str(পৰিমাপ_ডাটা/'java-swing.png'))
            সঞ্চালন=len(대화기록);ক্লিক_কৰক_মান(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',সঞ্চালন)
        # Download the guest-created bytes through FTP in the same GUI VM.
        ফাইল_প্রবিষ্ট_নাম={'java':'java.txt','c':'c.txt','python':'python.txt'}[ভাষা]
        শ্বেল('cp '+ফাইল_প্রবিষ্ট_নাম+' /বৈধকৰণ_কৰক.txt')
        받은수=bytearray();ফাইল_স্থানান্তৰণ_সংযোগ.retrbinary('RETR বৈধকৰণ_কৰক.txt',받은수.extend);assert 받은수==예상파일.encode()
        শ্বেল('echo preserved > 출력예제.'+('py' if ভাষা=='python' else ভাষা))
        assert 'EXAMPLES READY' in শ্বেল('example '+ভাষা)
        assert '\npreserved\n' in শ্বেল('cat 출력예제.'+('py' if ভাষা=='python' else ভাষা))
        assert '한/영 কী_মান, Shift+Space 또는 F9' in শ্বেল('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in শ্বেল('echo GUI NETWORK TOGETHER')
        ফাইল_স্থানান্তৰণ_সংযোগ.quit();ফাইল_স্থানান্তৰণ_সংযোগ=None;assert 'FTP stopped' in শ্বেল('ftpd stop')
        print('PASS '+ভাষা+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if ফাইল_স্থানান্তৰণ_সংযোগ:
            try:ফাইল_স্থানান্তৰণ_সংযোগ.close()
            except OSError:pass
        if ক্লায়েণ্ট:ক্লায়েণ্ট.close()
        প্ৰসেস.terminate()
        try:প্ৰসেস.wait(timeout=8)
        except subprocess.TimeoutExpired:প্ৰসেস.kill();প্ৰসেস.wait()
        চয়নকাৰী.close();প্ৰসেস.stdout.close();(পৰিমাপ_ডাটা/(ভাষা+'-serial.log')).write_bytes(대화기록)


def সঞ্চালন():
    পৰিমাপ_ডাটা=기준/'build/verification/examples';পৰিমাপ_ডাটা.mkdir(parents=True,exist_ok=True)
    বৈধতা_ৰিপ_ৰ্ট={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for ভাষা in ('java','c','python'):
                test_언어(ভাষা,되돌림서버항목,পৰিমাপ_ডাটা);বৈধতা_ৰিপ_ৰ্ট['languages'].append(ভাষা)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(বর্গ_মান,ডাটা.encode()) for বর্গ_মান,ডাটা in 예상결과],되돌림서버항목.수신됨
            বৈধতা_ৰিপ_ৰ্ট['host_network_payloads']=[{'protocol':বর্গ_মান,'text':ডাটা.decode()} for বর্গ_মান,ডাটা in 되돌림서버항목.수신됨]
        বৈধতা_ৰিপ_ৰ্ট.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(পৰিমাপ_ডাটা/'report.json').write_text(json.dumps(বৈধতা_ৰিপ_ৰ্ট,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':সঞ্চালন()
