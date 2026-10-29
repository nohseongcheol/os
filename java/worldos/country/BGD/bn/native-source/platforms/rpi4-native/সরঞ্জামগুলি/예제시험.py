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
from ডেস্কটপ_ভিউ import 정확한값
from 예제되돌림서버 import 되돌림서버
from কার্যকর_করুন_আদেশ import প্রকল্প_মূল


def test_언어(ভাষা,되돌림서버항목,পরিমাপ_ডাটা):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));ফাইল_স্থানান্তর_পোর্ট_নম্বর=임시자원.getsockname()[1]
    প্রসেস=subprocess.Popen(['python3',str(প্রকল্প_মূল/'সরঞ্জামগুলি/কার্যকর_করুন_আদেশ.py'),'--desktop','--network','--port','0','--ftp-port',str(ফাইল_স্থানান্তর_পোর্ট_নম্বর)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    নির্বাচক=selectors.DefaultSelector();নির্বাচক.register(প্রসেস.stdout,selectors.EVENT_READ)
    대화기록=bytearray();গ্রাহক=None;ফাইল_স্থানান্তর_সংযোগ=None
    def 수신하기(확인표시,চালনা=0):
        শেষ_করা_অফসেট=time.monotonic()+60
        while 확인표시 not in 대화기록[চালনা:]:
            if time.monotonic()>শেষ_করা_অফসেট or প্রসেস.poll() is not None:raise AssertionError(대화기록[চালনা:].decode('utf-8','replace'))
            for 누름값,_ in নির্বাচক.select(.1):
                ডাটা=누름값.fileobj.read(65536)
                if ডাটা:대화기록.extend(ডাটা)
        return 대화기록[চালনা:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(প্রতীক_মান,누르는중=True):গ্রাহক.sendall(struct.pack('>BBHI',4,int(누르는중),0,প্রতীক_মান))
    def শুরু_অফসেট(নিবেশের_পঙ্_ক্তি):
        চালনা=len(대화기록)
        for অক্ষর_কোড in নিবেশের_পঙ্_ক্তি+'\n':
            প্রতীক_মান=0xff0d if অক্ষর_কোড=='\n' else ord(অক্ষর_কোড) if ord(অক্ষর_কোড)<256 else 0x1000000|ord(অক্ষর_কোড)
            누름값(প্রতীক_মান);누름값(প্রতীক_মান,False)
        return চালনা
    def শেল(নিবেশের_পঙ্_ক্তি):return 수신하기(b'jkoros-native> ',শুরু_অফসেট(নিবেশের_পঙ্_ক্তি))
    def কার্যকর_করুন_আদেশ(নিবেশের_পঙ্_ক্তি,예상결과):
        পাঠ=শেল(নিবেশের_পঙ্_ক্তি);assert 예상결과 in পাঠ and 'exit 0' in পাঠ,(নিবেশের_পঙ্_ক্তি,পাঠ)
        return পাঠ
    def 화소들():
        গ্রাহক.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            বিভাগ_মান=정확한값(গ্রাহক,1)[0]
            if বিভাগ_মান==2:continue
            if বিভাগ_মান==3:
                개수=struct.unpack('>I',정확한값(গ্রাহক,7)[3:])[0];정확한값(গ্রাহক,개수);continue
            assert বিভাগ_মান==0,বিভাগ_মান
            항목수=struct.unpack('>H',정확한값(গ্রাহক,3)[1:])[0]
            for _ in range(항목수):
                X_বোতাম_অক্ষবিন্দু,Y_বোতাম_অক্ষবিন্দু,너비값,높이값,অক্ষর_সেট=struct.unpack('>HHHHi',정확한값(গ্রাহক,12));assert অক্ষর_সেট==0,অক্ষর_সেট
                ডাটা=정확한값(গ্রাহক,너비값*높이값*4)
                for সারি_পদ in range(높이값):
                    for কলাম_পদ in range(너비값):
                        원본자료=(সারি_পদ*너비값+কলাম_পদ)*4;লক্ষ্য=((Y_বোতাম_অক্ষবিন্দু+সারি_পদ)*640+X_বোতাম_অক্ষবিন্দু+কলাম_পদ)*3
                        빛삼원색[লক্ষ্য:লক্ষ্য+3]=bytes((ডাটা[원본자료+2],ডাটা[원본자료+1],ডাটা[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        পোর্ট_নম্বর=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        গ্রাহক=socket.create_connection(('127.0.0.1',পোর্ট_নম্বর),timeout=10)
        assert 정확한값(গ্রাহক,12)==b'RFB 003.008\n';গ্রাহক.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(গ্রাহক,정확한값(গ্রাহক,1)[0]);গ্রাহক.sendall(b'\x01');assert 정확한값(গ্রাহক,4)==b'\0'*4
        গ্রাহক.sendall(b'\x01');초기값=정확한값(গ্রাহক,24);정확한값(গ্রাহক,struct.unpack('>I',초기값[20:])[0])
        গ্রাহক.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        গ্রাহক.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in শেল('ftpd start')
        ফাইল_স্থানান্তর_সংযোগ=ftplib.FTP();ফাইল_স্থানান্তর_সংযোগ.encoding='utf-8';ফাইল_স্থানান্তর_সংযোগ.connect('127.0.0.1',ফাইল_স্থানান্তর_পোর্ট_নম্বর,timeout=20);ফাইল_স্থানান্তর_সংযোগ.login()
        পেলোড_ডাটা=('GUI와 FTP 동시 사용 '+ভাষা+' 😀\n').encode()
        ফাইল_স্থানান্তর_সংযোগ.storbinary('STOR 함께.txt',io.BytesIO(পেলোড_ডাটা))
        assert পেলোড_ডাটা.decode().strip() in শেল('cat /함께.txt')
        받은수=bytearray();ফাইল_স্থানান্তর_সংযোগ.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==পেলোড_ডাটা;ফাইল_স্থানান্তর_সংযোগ.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        পাঠান_তালিকা=শেল('ls /example')
        assert all(নাম in পাঠান_তালিকা for নাম in ('java/','c/','python/','README.md')),পাঠান_তালিকা
        if ভাষা=='java':
            꾸러미명세=json.loads((প্রকল্প_মূল/'build/examples/manifest.json').read_text())
            for পথ_2,ভুক্তি_বিন্দু in 꾸러미명세.items():
                শেল('cp '+পথ_2+' /example-check.bin')
                সামগ্রি_মান=bytearray();ফাইল_স্থানান্তর_সংযোগ.retrbinary('RETR example-check.bin',সামগ্রি_মান.extend)
                assert len(সামগ্রি_মান)==ভুক্তি_বিন্দু['bytes'] and hashlib.sha256(সামগ্রি_মান).hexdigest()==ভুক্তি_বিন্দু['sha256'],পথ_2
            ফাইল_স্থানান্তর_সংযোগ.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            বাইনারি=bytes(range(256))*64
            ফাইল_স্থানান্তর_সংযোগ.storbinary('STOR boundary.bin',io.BytesIO(বাইনারি))
            সামগ্রি_মান=bytearray();ফাইল_স্থানান্তর_সংযোগ.retrbinary('RETR boundary.bin',সামগ্রি_মান.extend)
            assert সামগ্রি_মান==বাইনারি and 'boundary.bin' in ফাইল_স্থানান্তর_সংযোগ.nlst()
            শেল('cp /boundary.bin /boundary-copy.bin')
            সামগ্রি_মান=bytearray();ফাইল_স্থানান্তর_সংযোগ.retrbinary('RETR boundary-copy.bin',সামগ্রি_মান.extend)
            assert সামগ্রি_মান==বাইনারি
            ফাইল_স্থানান্তর_সংযোগ.delete('boundary.bin');ফাইল_স্থানান্তর_সংযোগ.delete('boundary-copy.bin')
        assert 'মুদ্রণনমুনা' in শেল('ls /example/'+ভাষা)
        শেল('cd /example/'+ভাষা)
        নাম_সারণি={'java':'JAVA','c':'C','python':'PYTHON'}[ভাষা]
        예상파일=নাম_সারণি+' নথির_নাম: 한글 ডাটা 😀\n'
        if ভাষা=='java':
            কার্যকর_করুন_আদেশ('javac মুদ্রণনমুনা.java','Compiled:');কার্যকর_করুন_আদেশ('java মুদ্রণনমুনা','JAVA নির্গম: 안녕하세요 😀')
            কার্যকর_করুন_আদেশ('javac ফাইলনমুনা.java','Compiled:');কার্যকর_করুন_আদেশ('java ফাইলনমুনা',예상파일)
            কার্যকর_করুন_আদেশ('java নেটওয়ার্ক {} {}'.format(되돌림서버항목.ট্রান্সমিশন_কন্ট্রোল_প্রটোকল_পোর্ট,되돌림서버항목.전문접속번호),'JAVA 네트워크 যাচাই_করা: TCP UDP 한글')
            গ্রাফিক্স_আদেশ='java অঙ্কননমুনা'
        elif ভাষা=='c':
            for নাম,전달값,예상결과 in [('নির্গম','', 'C নির্গম: 안녕하세요 😀'),('নথির_নাম','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 যাচাই_করা: UDP 한글')]:
                কার্যকর_করুন_আদেশ('cc '+নাম+'예제.c -o কার্যকর_করুন_আদেশ','Compiled native ARM64 ELF:')
                কার্যকর_করুন_আদেশ('./কার্যকর_করুন_আদেশ'+전달값,예상결과)
            কার্যকর_করুন_আদেশ('cc অঙ্কননমুনা.c -o কার্যকর_করুন_আদেশ','Compiled native ARM64 ELF:');গ্রাফিক্স_আদেশ='./কার্যকর_করুন_আদেশ'
        else:
            for নাম,전달값,예상결과 in [('নির্গম','','PYTHON নির্গম: 안녕하세요 😀'),('নথির_নাম','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 যাচাই_করা: UDP 한글')]:
                কার্যকর_করুন_আদেশ('python '+নাম+'예제.py'+전달값,예상결과)
            গ্রাফিক্স_আদেশ='python অঙ্কননমুনা.py'
        শুরু_অঙ্কন=শুরু_অফসেট(গ্রাফিক্স_আদেশ)
        পাঠ=수신하기('그림을 확인한 ফিরে_যান_মান Enter를 누르세요.\r\n'.encode(),শুরু_অঙ্কন)
        assert নাম_সারণি+' 그래픽: 빨강 초록 파랑' in পাঠ and 'exit 0' not in পাঠ,পাঠ
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        ফাইল_স্থানান্তর_সংযোগ.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();ফাইল_স্থানান্তর_সংযোগ.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';ফাইল_স্থানান্তর_সংযোগ.delete('도중.txt')
        빛삼원색=화소들()
        for Y_বোতাম_অক্ষবিন্দু,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            অফসেট_মান=(Y_বোতাম_অক্ষবিন্দু*640+610)*3;assert tuple(빛삼원색[অফসেট_মান:অফসেট_মান+3])==색상,(ভাষা,Y_বোতাম_অক্ষবিন্দু,tuple(빛삼원색[অফসেট_মান:অফসেট_মান+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(পরিমাপ_ডাটা/(ভাষা+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',শুরু_অঙ্কন)
        if ভাষা=='java':
            শুরু_উইন্ডো=শুরু_অফসেট('java জানালানমুনা')
            수신하기('GUI 예제 প্রস্তুত_করুন: জানালানমুনা'.encode(),শুরু_উইন্ডো)
            def ক্লিক_করা_মান(가로,উল্লম্ব_পদ):
                for বোতাম in (1,0):গ্রাহক.sendall(struct.pack('>BBHH',5,বোতাম,가로,উল্লম্ব_পদ))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            ক্লিক_করা_মান(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for অক্ষর_মান in '한글':누름값(0x1000000|ord(অক্ষর_মান));누름값(0x1000000|ord(অক্ষর_মান),False)
            for 횟수 in (1,2):
                চালনা=len(대화기록);ক্লিক_করা_মান(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),চালনা)
            time.sleep(.3)
            উইন্ডো_অঙ্কন=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=উইন্ডো_অঙ্কন.crop((110,272,530,300)).tobytes()
            উইন্ডো_অঙ্কন.save(str(পরিমাপ_ডাটা/'java-swing.png'))
            চালনা=len(대화기록);ক্লিক_করা_মান(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',চালনা)
        # Download the guest-created bytes through FTP in the same GUI VM.
        ফাইল_ভুক্তি_নাম={'java':'java.txt','c':'c.txt','python':'python.txt'}[ভাষা]
        শেল('cp '+ফাইল_ভুক্তি_নাম+' /বৈধ_করুন.txt')
        받은수=bytearray();ফাইল_স্থানান্তর_সংযোগ.retrbinary('RETR বৈধ_করুন.txt',받은수.extend);assert 받은수==예상파일.encode()
        শেল('echo preserved > মুদ্রণনমুনা.'+('py' if ভাষা=='python' else ভাষা))
        assert 'EXAMPLES READY' in শেল('example '+ভাষা)
        assert '\npreserved\n' in শেল('cat মুদ্রণনমুনা.'+('py' if ভাষা=='python' else ভাষা))
        assert '한/영 কী_মান, Shift+Space 또는 F9' in শেল('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in শেল('echo GUI NETWORK TOGETHER')
        ফাইল_স্থানান্তর_সংযোগ.quit();ফাইল_স্থানান্তর_সংযোগ=None;assert 'FTP stopped' in শেল('ftpd stop')
        print('PASS '+ভাষা+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if ফাইল_স্থানান্তর_সংযোগ:
            try:ফাইল_স্থানান্তর_সংযোগ.close()
            except OSError:pass
        if গ্রাহক:গ্রাহক.close()
        প্রসেস.terminate()
        try:প্রসেস.wait(timeout=8)
        except subprocess.TimeoutExpired:প্রসেস.kill();প্রসেস.wait()
        নির্বাচক.close();প্রসেস.stdout.close();(পরিমাপ_ডাটা/(ভাষা+'-serial.log')).write_bytes(대화기록)


def চালনা():
    পরিমাপ_ডাটা=প্রকল্প_মূল/'build/verification/examples';পরিমাপ_ডাটা.mkdir(parents=True,exist_ok=True)
    বৈধকরণ_রিপোর্ট={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((প্রকল্প_মূল/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for ভাষা in ('java','c','python'):
                test_언어(ভাষা,되돌림서버항목,পরিমাপ_ডাটা);বৈধকরণ_রিপোর্ট['languages'].append(ভাষা)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(বিভাগ_মান,ডাটা.encode()) for বিভাগ_মান,ডাটা in 예상결과],되돌림서버항목.수신됨
            বৈধকরণ_রিপোর্ট['host_network_payloads']=[{'protocol':বিভাগ_মান,'text':ডাটা.decode()} for বিভাগ_মান,ডাটা in 되돌림서버항목.수신됨]
        বৈধকরণ_রিপোর্ট.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(পরিমাপ_ডাটা/'report.json').write_text(json.dumps(বৈধকরণ_রিপোর্ট,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':চালনা()
