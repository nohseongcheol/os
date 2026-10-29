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
from ដែសថប_ការមើល import 정확한값
from 예제되돌림서버 import 되돌림서버
from អនុវត្ត_ពាក្យបញ្ជា import បញ្ចាំង_ឬស


def test_언어(ភាសា,되돌림서버항목,ការវាស់វែង_ទិន្នន័យ):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));ឯកសារ_ផ្ទេរ_លេខរន្ធ=임시자원.getsockname()[1]
    ដំណើរការ=subprocess.Popen(['python3',str(បញ្ចាំង_ឬស/'ឧបករណ៍/អនុវត្ត_ពាក្យបញ្ជា.py'),'--desktop','--network','--port','0','--ftp-port',str(ឯកសារ_ផ្ទេរ_លេខរន្ធ)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    អ្នកជ្រើសរើស=selectors.DefaultSelector();អ្នកជ្រើសរើស.register(ដំណើរការ.stdout,selectors.EVENT_READ)
    대화기록=bytearray();អតិថិជន=None;ឯកសារ_ផ្ទេរ_ការភ្ជាប់=None
    def 수신하기(확인표시,រត់=0):
        បញ្ចប់_ការបែង_ភាគ=time.monotonic()+60
        while 확인표시 not in 대화기록[រត់:]:
            if time.monotonic()>បញ្ចប់_ការបែង_ភាគ or ដំណើរការ.poll() is not None:raise AssertionError(대화기록[រត់:].decode('utf-8','replace'))
            for 누름값,_ in អ្នកជ្រើសរើស.select(.1):
                ទិន្នន័យ=누름값.fileobj.read(65536)
                if ទិន្នន័យ:대화기록.extend(ទិន្នន័យ)
        return 대화기록[រត់:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(និមិត្ត_សញ្ញា_តំលៃ,누르는중=True):អតិថិជន.sendall(struct.pack('>BBHI',4,int(누르는중),0,និមិត្ត_សញ្ញា_តំលៃ))
    def ផ្តើម_ការបែង_ភាគ(បន្ទាត់):
        រត់=len(대화기록)
        for កូដនៃតួអក្សរ in បន្ទាត់+'\n':
            និមិត្ត_សញ្ញា_តំលៃ=0xff0d if កូដនៃតួអក្សរ=='\n' else ord(កូដនៃតួអក្សរ) if ord(កូដនៃតួអក្សរ)<256 else 0x1000000|ord(កូដនៃតួអក្សរ)
            누름값(និមិត្ត_សញ្ញា_តំលៃ);누름값(និមិត្ត_សញ្ញា_តំលៃ,False)
        return រត់
    def 셸(បន្ទាត់):return 수신하기(b'jkoros-native> ',ផ្តើម_ការបែង_ភាគ(បន្ទាត់))
    def អនុវត្ត_ពាក្យបញ្ជា(បន្ទាត់,예상결과):
        អត្ថបទ=셸(បន្ទាត់);assert 예상결과 in អត្ថបទ and 'exit 0' in អត្ថបទ,(បន្ទាត់,អត្ថបទ)
        return អត្ថបទ
    def 화소들():
        អតិថិជន.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            ប្រភេទ_តំលៃ=정확한값(អតិថិជន,1)[0]
            if ប្រភេទ_តំលៃ==2:continue
            if ប្រភេទ_តំលៃ==3:
                개수=struct.unpack('>I',정확한값(អតិថិជន,7)[3:])[0];정확한값(អតិថិជន,개수);continue
            assert ប្រភេទ_តំលៃ==0,ប្រភេទ_តំលៃ
            항목수=struct.unpack('>H',정확한값(អតិថិជន,3)[1:])[0]
            for _ in range(항목수):
                កូអរដោណេ_x,ប៊ូតុង_Y_កូអរដោនេ,너비값,높이값,សំណុំតួអក្សរ=struct.unpack('>HHHHi',정확한값(អតិថិជន,12));assert សំណុំតួអក្សរ==0,សំណុំតួអក្សរ
                ទិន្នន័យ=정확한값(អតិថិជន,너비값*높이값*4)
                for ជួរដេក_កំណត់ទីតាំង in range(높이값):
                    for ជួរឈរ_កំណត់ទីតាំង in range(너비값):
                        원본자료=(ជួរដេក_កំណត់ទីតាំង*너비값+ជួរឈរ_កំណត់ទីតាំង)*4;គោលដៅ=((ប៊ូតុង_Y_កូអរដោនេ+ជួរដេក_កំណត់ទីតាំង)*640+កូអរដោណេ_x+ជួរឈរ_កំណត់ទីតាំង)*3
                        빛삼원색[គោលដៅ:គោលដៅ+3]=bytes((ទិន្នន័យ[원본자료+2],ទិន្នន័យ[원본자료+1],ទិន្នន័យ[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        លេខរន្ធ=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        អតិថិជន=socket.create_connection(('127.0.0.1',លេខរន្ធ),timeout=10)
        assert 정확한값(អតិថិជន,12)==b'RFB 003.008\n';អតិថិជន.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(អតិថិជន,정확한값(អតិថិជន,1)[0]);អតិថិជន.sendall(b'\x01');assert 정확한값(អតិថិជន,4)==b'\0'*4
        អតិថិជន.sendall(b'\x01');초기값=정확한값(អតិថិជន,24);정확한값(អតិថិជន,struct.unpack('>I',초기값[20:])[0])
        អតិថិជន.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        អតិថិជន.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in 셸('ftpd start')
        ឯកសារ_ផ្ទេរ_ការភ្ជាប់=ftplib.FTP();ឯកសារ_ផ្ទេរ_ការភ្ជាប់.encoding='utf-8';ឯកសារ_ផ្ទេរ_ការភ្ជាប់.connect('127.0.0.1',ឯកសារ_ផ្ទេរ_លេខរន្ធ,timeout=20);ឯកសារ_ផ្ទេរ_ការភ្ជាប់.login()
        ទិន្នន័យដែលផ្ទុក_ទិន្នន័យ=('GUI와 FTP 동시 사용 '+ភាសា+' 😀\n').encode()
        ឯកសារ_ផ្ទេរ_ការភ្ជាប់.storbinary('STOR 함께.txt',io.BytesIO(ទិន្នន័យដែលផ្ទុក_ទិន្នន័យ))
        assert ទិន្នន័យដែលផ្ទុក_ទិន្នន័យ.decode().strip() in 셸('cat /함께.txt')
        받은수=bytearray();ឯកសារ_ផ្ទេរ_ការភ្ជាប់.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==ទិន្នន័យដែលផ្ទុក_ទិន្នន័យ;ឯកសារ_ផ្ទេរ_ការភ្ជាប់.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        ផ្ញើ_បញ្ជី=셸('ls /example')
        assert all(ឈ្មោះ in ផ្ញើ_បញ្ជី for ឈ្មោះ in ('java/','c/','python/','README.md')),ផ្ញើ_បញ្ជី
        if ភាសា=='java':
            꾸러미명세=json.loads((បញ្ចាំង_ឬស/'build/examples/manifest.json').read_text())
            for ផ្លូវ,ការបញ្ចូល_ចំនុច in 꾸러미명세.items():
                셸('cp '+ផ្លូវ+' /example-check.bin')
                មាតិកា_តំលៃ=bytearray();ឯកសារ_ផ្ទេរ_ការភ្ជាប់.retrbinary('RETR example-check.bin',មាតិកា_តំលៃ.extend)
                assert len(មាតិកា_តំលៃ)==ការបញ្ចូល_ចំនុច['bytes'] and hashlib.sha256(មាតិកា_តំលៃ).hexdigest()==ការបញ្ចូល_ចំនុច['sha256'],ផ្លូវ
            ឯកសារ_ផ្ទេរ_ការភ្ជាប់.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            គោលពីរ=bytes(range(256))*64
            ឯកសារ_ផ្ទេរ_ការភ្ជាប់.storbinary('STOR boundary.bin',io.BytesIO(គោលពីរ))
            មាតិកា_តំលៃ=bytearray();ឯកសារ_ផ្ទេរ_ការភ្ជាប់.retrbinary('RETR boundary.bin',មាតិកា_តំលៃ.extend)
            assert មាតិកា_តំលៃ==គោលពីរ and 'boundary.bin' in ឯកសារ_ផ្ទេរ_ការភ្ជាប់.nlst()
            셸('cp /boundary.bin /boundary-copy.bin')
            មាតិកា_តំលៃ=bytearray();ឯកសារ_ផ្ទេរ_ការភ្ជាប់.retrbinary('RETR boundary-copy.bin',មាតិកា_តំលៃ.extend)
            assert មាតិកា_តំលៃ==គោលពីរ
            ឯកសារ_ផ្ទេរ_ការភ្ជាប់.delete('boundary.bin');ឯកសារ_ផ្ទេរ_ការភ្ជាប់.delete('boundary-copy.bin')
        assert '출력예제' in 셸('ls /example/'+ភាសា)
        셸('cd /example/'+ភាសា)
        ឈ្មោះ_តារាង={'java':'JAVA','c':'C','python':'PYTHON'}[ភាសា]
        예상파일=ឈ្មោះ_តារាង+' ឯកសារ: 한글 ទិន្នន័យ 😀\n'
        if ភាសា=='java':
            អនុវត្ត_ពាក្យបញ្ជា('javac 출력예제.java','Compiled:');អនុវត្ត_ពាក្យបញ្ជា('java 출력예제','JAVA លទ្ធផល: 안녕하세요 😀')
            អនុវត្ត_ពាក្យបញ្ជា('javac 파일예제.java','Compiled:');អនុវត្ត_ពាក្យបញ្ជា('java 파일예제',예상파일)
            អនុវត្ត_ពាក្យបញ្ជា('java 네트워크예제 {} {}'.format(되돌림서버항목.ប្រូតូកូលត្រូតពិនិត្យការបញ្ជូន_ច្រក,되돌림서버항목.전문접속번호),'JAVA 네트워크 ផ្ទៀងផ្ទាត់: TCP UDP 한글')
            ក្រាហ្វិក_ពាក្យបញ្ជា='java 그래픽예제'
        elif ភាសា=='c':
            for ឈ្មោះ,전달값,예상결과 in [('លទ្ធផល','', 'C លទ្ធផល: 안녕하세요 😀'),('ឯកសារ','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 ផ្ទៀងផ្ទាត់: UDP 한글')]:
                អនុវត្ត_ពាក្យបញ្ជា('cc '+ឈ្មោះ+'예제.c -o អនុវត្ត_ពាក្យបញ្ជា','Compiled native ARM64 ELF:')
                អនុវត្ត_ពាក្យបញ្ជា('./អនុវត្ត_ពាក្យបញ្ជា'+전달값,예상결과)
            អនុវត្ត_ពាក្យបញ្ជា('cc 그래픽예제.c -o អនុវត្ត_ពាក្យបញ្ជា','Compiled native ARM64 ELF:');ក្រាហ្វិក_ពាក្យបញ្ជា='./អនុវត្ត_ពាក្យបញ្ជា'
        else:
            for ឈ្មោះ,전달값,예상결과 in [('លទ្ធផល','','PYTHON លទ្ធផល: 안녕하세요 😀'),('ឯកសារ','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 ផ្ទៀងផ្ទាត់: UDP 한글')]:
                អនុវត្ត_ពាក្យបញ្ជា('python '+ឈ្មោះ+'예제.py'+전달값,예상결과)
            ក្រាហ្វិក_ពាក្យបញ្ជា='python 그래픽예제.py'
        ផ្តើម_ការគូរ=ផ្តើម_ការបែង_ភាគ(ក្រាហ្វិក_ពាក្យបញ្ជា)
        អត្ថបទ=수신하기('그림을 확인한 ការថយ_តំលៃ Enter를 누르세요.\r\n'.encode(),ផ្តើម_ការគូរ)
        assert ឈ្មោះ_តារាង+' 그래픽: 빨강 초록 파랑' in អត្ថបទ and 'exit 0' not in អត្ថបទ,អត្ថបទ
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        ឯកសារ_ផ្ទេរ_ការភ្ជាប់.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();ឯកសារ_ផ្ទេរ_ការភ្ជាប់.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';ឯកសារ_ផ្ទេរ_ការភ្ជាប់.delete('도중.txt')
        빛삼원색=화소들()
        for ប៊ូតុង_Y_កូអរដោនេ,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            ការបែង_ភាគ_តំលៃ=(ប៊ូតុង_Y_កូអរដោនេ*640+610)*3;assert tuple(빛삼원색[ការបែង_ភាគ_តំលៃ:ការបែង_ភាគ_តំលៃ+3])==색상,(ភាសា,ប៊ូតុង_Y_កូអរដោនេ,tuple(빛삼원색[ការបែង_ភាគ_តំលៃ:ការបែង_ភាគ_តំលៃ+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(ការវាស់វែង_ទិន្នន័យ/(ភាសា+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',ផ្តើម_ការគូរ)
        if ភាសា=='java':
            ផ្តើម_វីនដូ=ផ្តើម_ការបែង_ភាគ('java 창예제')
            수신하기('GUI 예제 រៀបចំ: 창예제'.encode(),ផ្តើម_វីនដូ)
            def ចុច_តំលៃ(가로,បញ្ឈរ_កំណត់ទីតាំង):
                for ប៊ូតុង in (1,0):អតិថិជន.sendall(struct.pack('>BBHH',5,ប៊ូតុង,가로,បញ្ឈរ_កំណត់ទីតាំង))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            ចុច_តំលៃ(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for តួអក្សរ_តំលៃ in '한글':누름값(0x1000000|ord(តួអក្សរ_តំលៃ));누름값(0x1000000|ord(តួអក្សរ_តំលៃ),False)
            for 횟수 in (1,2):
                រត់=len(대화기록);ចុច_តំលៃ(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),រត់)
            time.sleep(.3)
            វីនដូ_ការគូរ=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=វីនដូ_ការគូរ.crop((110,272,530,300)).tobytes()
            វីនដូ_ការគូរ.save(str(ការវាស់វែង_ទិន្នន័យ/'java-swing.png'))
            រត់=len(대화기록);ចុច_តំលៃ(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',រត់)
        # Download the guest-created bytes through FTP in the same GUI VM.
        ឯកសារ_ការបញ្ចូល_ឈ្មោះ={'java':'java.txt','c':'c.txt','python':'python.txt'}[ភាសា]
        셸('cp '+ឯកសារ_ការបញ្ចូល_ឈ្មោះ+' /ធ្វើអោយមានសុពលភាព.txt')
        받은수=bytearray();ឯកសារ_ផ្ទេរ_ការភ្ជាប់.retrbinary('RETR ធ្វើអោយមានសុពលភាព.txt',받은수.extend);assert 받은수==예상파일.encode()
        셸('echo preserved > 출력예제.'+('py' if ភាសា=='python' else ភាសា))
        assert 'EXAMPLES READY' in 셸('example '+ភាសា)
        assert '\npreserved\n' in 셸('cat 출력예제.'+('py' if ភាសា=='python' else ភាសា))
        assert '한/영 ឃី_តំលៃ, Shift+Space 또는 F9' in 셸('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in 셸('echo GUI NETWORK TOGETHER')
        ឯកសារ_ផ្ទេរ_ការភ្ជាប់.quit();ឯកសារ_ផ្ទេរ_ការភ្ជាប់=None;assert 'FTP stopped' in 셸('ftpd stop')
        print('PASS '+ភាសា+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if ឯកសារ_ផ្ទេរ_ការភ្ជាប់:
            try:ឯកសារ_ផ្ទេរ_ការភ្ជាប់.close()
            except OSError:pass
        if អតិថិជន:អតិថិជន.close()
        ដំណើរការ.terminate()
        try:ដំណើរការ.wait(timeout=8)
        except subprocess.TimeoutExpired:ដំណើរការ.kill();ដំណើរការ.wait()
        អ្នកជ្រើសរើស.close();ដំណើរការ.stdout.close();(ការវាស់វែង_ទិន្នន័យ/(ភាសា+'-serial.log')).write_bytes(대화기록)


def រត់():
    ការវាស់វែង_ទិន្នន័យ=បញ្ចាំង_ឬស/'build/verification/examples';ការវាស់វែង_ទិន្នន័យ.mkdir(parents=True,exist_ok=True)
    សុពលភាព_រាយការណ៍={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((បញ្ចាំង_ឬស/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for ភាសា in ('java','c','python'):
                test_언어(ភាសា,되돌림서버항목,ការវាស់វែង_ទិន្នន័យ);សុពលភាព_រាយការណ៍['languages'].append(ភាសា)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(ប្រភេទ_តំលៃ,ទិន្នន័យ.encode()) for ប្រភេទ_តំលៃ,ទិន្នន័យ in 예상결과],되돌림서버항목.수신됨
            សុពលភាព_រាយការណ៍['host_network_payloads']=[{'protocol':ប្រភេទ_តំលៃ,'text':ទិន្នន័យ.decode()} for ប្រភេទ_តំលៃ,ទិន្នន័យ in 되돌림서버항목.수신됨]
        សុពលភាព_រាយការណ៍.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(ការវាស់វែង_ទិន្នន័យ/'report.json').write_text(json.dumps(សុពលភាព_រាយការណ៍,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':រត់()
