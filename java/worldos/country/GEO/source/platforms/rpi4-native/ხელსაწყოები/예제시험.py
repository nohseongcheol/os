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
from სამუშაო_დაფა_ხედი import 정확한값
from 예제되돌림서버 import 되돌림서버
from შესრულება_ბრძანება import პროეცირება_ფესვი


def test_언어(ენა,되돌림서버항목,გაზომვა_მონაცემები):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    პროცესი=subprocess.Popen(['python3',str(პროეცირება_ფესვი/'ხელსაწყოები/შესრულება_ბრძანება.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    სელექტორი=selectors.DefaultSelector();სელექტორი.register(პროცესი.stdout,selectors.EVENT_READ)
    대화기록=bytearray();კლიენტი=None;ფაილი_გადატანა_კავშირი=None
    def 수신하기(확인표시,გაშვება=0):
        დასასრული_ოფსეტი=time.monotonic()+60
        while 확인표시 not in 대화기록[გაშვება:]:
            if time.monotonic()>დასასრული_ოფსეტი or პროცესი.poll() is not None:raise AssertionError(대화기록[გაშვება:].decode('utf-8','replace'))
            for 누름값,_ in სელექტორი.select(.1):
                მონაცემები=누름값.fileobj.read(65536)
                if მონაცემები:대화기록.extend(მონაცემები)
        return 대화기록[გაშვება:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(სიმბოლო_მნიშვნელობა,누르는중=True):კლიენტი.sendall(struct.pack('>BBHI',4,int(누르는중),0,სიმბოლო_მნიშვნელობა))
    def დაწყება_ოფსეტი(ხაზი):
        გაშვება=len(대화기록)
        for სიმბოლოს_კოდი in ხაზი+'\n':
            სიმბოლო_მნიშვნელობა=0xff0d if სიმბოლოს_კოდი=='\n' else ord(სიმბოლოს_კოდი) if ord(სიმბოლოს_კოდი)<256 else 0x1000000|ord(სიმბოლოს_კოდი)
            누름값(სიმბოლო_მნიშვნელობა);누름값(სიმბოლო_მნიშვნელობა,False)
        return გაშვება
    def გარემო(ხაზი):return 수신하기(b'jkoros-native> ',დაწყება_ოფსეტი(ხაზი))
    def შესრულება_ბრძანება(ხაზი,예상결과):
        ტექსტი=გარემო(ხაზი);assert 예상결과 in ტექსტი and 'exit 0' in ტექსტი,(ხაზი,ტექსტი)
        return ტექსტი
    def 화소들():
        კლიენტი.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            კატეგორია_მნიშვნელობა=정확한값(კლიენტი,1)[0]
            if კატეგორია_მნიშვნელობა==2:continue
            if კატეგორია_მნიშვნელობა==3:
                개수=struct.unpack('>I',정확한값(კლიენტი,7)[3:])[0];정확한값(კლიენტი,개수);continue
            assert კატეგორია_მნიშვნელობა==0,კატეგორია_მნიშვნელობა
            항목수=struct.unpack('>H',정확한값(კლიენტი,3)[1:])[0]
            for _ in range(항목수):
                x_კოორდინატა,Y_ღილაკი_კოორდინატი,너비값,높이값,კოდირება=struct.unpack('>HHHHi',정확한값(კლიენტი,12));assert კოდირება==0,კოდირება
                მონაცემები=정확한값(კლიენტი,너비값*높이값*4)
                for ჩაწერა_პოზიცია in range(높이값):
                    for სვეტი_პოზიცია in range(너비값):
                        원본자료=(ჩაწერა_პოზიცია*너비값+სვეტი_პოზიცია)*4;მიზანი=((Y_ღილაკი_კოორდინატი+ჩაწერა_პოზიცია)*640+x_კოორდინატა+სვეტი_პოზიცია)*3
                        빛삼원색[მიზანი:მიზანი+3]=bytes((მონაცემები[원본자료+2],მონაცემები[원본자료+1],მონაცემები[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        კლიენტი=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert 정확한값(კლიენტი,12)==b'RFB 003.008\n';კლიენტი.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(კლიენტი,정확한값(კლიენტი,1)[0]);კლიენტი.sendall(b'\x01');assert 정확한값(კლიენტი,4)==b'\0'*4
        კლიენტი.sendall(b'\x01');초기값=정확한값(კლიენტი,24);정확한값(კლიენტი,struct.unpack('>I',초기값[20:])[0])
        კლიენტი.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        კლიენტი.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in გარემო('ftpd start')
        ფაილი_გადატანა_კავშირი=ftplib.FTP();ფაილი_გადატანა_კავშირი.encoding='utf-8';ფაილი_გადატანა_კავშირი.connect('127.0.0.1',파일전송접속번호,timeout=20);ფაილი_გადატანა_კავშირი.login()
        დატვირთვა_მონაცემები=('GUI와 FTP 동시 사용 '+ენა+' 😀\n').encode()
        ფაილი_გადატანა_კავშირი.storbinary('STOR 함께.txt',io.BytesIO(დატვირთვა_მონაცემები))
        assert დატვირთვა_მონაცემები.decode().strip() in გარემო('cat /함께.txt')
        받은수=bytearray();ფაილი_გადატანა_კავშირი.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==დატვირთვა_მონაცემები;ფაილი_გადატანა_კავშირი.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        გაგზავნა_სია=გარემო('ls /example')
        assert all(სახელი in გაგზავნა_სია for სახელი in ('java/','c/','python/','README.md')),გაგზავნა_სია
        if ენა=='java':
            꾸러미명세=json.loads((პროეცირება_ფესვი/'build/examples/manifest.json').read_text())
            for გეზი,შენატანი_პტ in 꾸러미명세.items():
                გარემო('cp '+გეზი+' /example-check.bin')
                შიგთავსი_მნიშვნელობა=bytearray();ფაილი_გადატანა_კავშირი.retrbinary('RETR example-check.bin',შიგთავსი_მნიშვნელობა.extend)
                assert len(შიგთავსი_მნიშვნელობა)==შენატანი_პტ['bytes'] and hashlib.sha256(შიგთავსი_მნიშვნელობა).hexdigest()==შენატანი_პტ['sha256'],გეზი
            ფაილი_გადატანა_კავშირი.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            ორობითი=bytes(range(256))*64
            ფაილი_გადატანა_კავშირი.storbinary('STOR boundary.bin',io.BytesIO(ორობითი))
            შიგთავსი_მნიშვნელობა=bytearray();ფაილი_გადატანა_კავშირი.retrbinary('RETR boundary.bin',შიგთავსი_მნიშვნელობა.extend)
            assert შიგთავსი_მნიშვნელობა==ორობითი and 'boundary.bin' in ფაილი_გადატანა_კავშირი.nlst()
            გარემო('cp /boundary.bin /boundary-copy.bin')
            შიგთავსი_მნიშვნელობა=bytearray();ფაილი_გადატანა_კავშირი.retrbinary('RETR boundary-copy.bin',შიგთავსი_მნიშვნელობა.extend)
            assert შიგთავსი_მნიშვნელობა==ორობითი
            ფაილი_გადატანა_კავშირი.delete('boundary.bin');ფაილი_გადატანა_კავშირი.delete('boundary-copy.bin')
        assert '출력예제' in გარემო('ls /example/'+ენა)
        გარემო('cd /example/'+ენა)
        სახელი_ცხრილი={'java':'JAVA','c':'C','python':'PYTHON'}[ენა]
        예상파일=სახელი_ცხრილი+' ფაილი: 한글 მონაცემები 😀\n'
        if ენა=='java':
            შესრულება_ბრძანება('javac 출력예제.java','Compiled:');შესრულება_ბრძანება('java 출력예제','JAVA 출력: 안녕하세요 😀')
            შესრულება_ბრძანება('javac 파일예제.java','Compiled:');შესრულება_ბრძანება('java 파일예제',예상파일)
            შესრულება_ბრძანება('java 네트워크예제 {} {}'.format(되돌림서버항목.გადაცემის_მართვის_პროტოკოლი_პორტი,되돌림서버항목.전문접속번호),'JAVA 네트워크 გადამოწმება: TCP UDP 한글')
            გრაფიკა_ბრძანება='java 그래픽예제'
        elif ენა=='c':
            for სახელი,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('ფაილი','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 გადამოწმება: UDP 한글')]:
                შესრულება_ბრძანება('cc '+სახელი+'예제.c -o შესრულება_ბრძანება','Compiled native ARM64 ELF:')
                შესრულება_ბრძანება('./შესრულება_ბრძანება'+전달값,예상결과)
            შესრულება_ბრძანება('cc 그래픽예제.c -o შესრულება_ბრძანება','Compiled native ARM64 ELF:');გრაფიკა_ბრძანება='./შესრულება_ბრძანება'
        else:
            for სახელი,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('ფაილი','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 გადამოწმება: UDP 한글')]:
                შესრულება_ბრძანება('python '+სახელი+'예제.py'+전달값,예상결과)
            გრაფიკა_ბრძანება='python 그래픽예제.py'
        დაწყება_ნახატი=დაწყება_ოფსეტი(გრაფიკა_ბრძანება)
        ტექსტი=수신하기('그림을 확인한 უკან_მნიშვნელობა Enter를 누르세요.\r\n'.encode(),დაწყება_ნახატი)
        assert სახელი_ცხრილი+' 그래픽: 빨강 초록 파랑' in ტექსტი and 'exit 0' not in ტექსტი,ტექსტი
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        ფაილი_გადატანა_კავშირი.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();ფაილი_გადატანა_კავშირი.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';ფაილი_გადატანა_კავშირი.delete('도중.txt')
        빛삼원색=화소들()
        for Y_ღილაკი_კოორდინატი,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            ოფსეტი_მნიშვნელობა=(Y_ღილაკი_კოორდინატი*640+610)*3;assert tuple(빛삼원색[ოფსეტი_მნიშვნელობა:ოფსეტი_მნიშვნელობა+3])==색상,(ენა,Y_ღილაკი_კოორდინატი,tuple(빛삼원색[ოფსეტი_მნიშვნელობა:ოფსეტი_მნიშვნელობა+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(გაზომვა_მონაცემები/(ენა+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',დაწყება_ნახატი)
        if ენა=='java':
            დაწყება_ფანჯარა=დაწყება_ოფსეტი('java 창예제')
            수신하기('GUI 예제 მომზადება: 창예제'.encode(),დაწყება_ფანჯარა)
            def დაწკაპუნება_მნიშვნელობა(가로,ვერტიკალური_პოზიცია):
                for ღილაკი in (1,0):კლიენტი.sendall(struct.pack('>BBHH',5,ღილაკი,가로,ვერტიკალური_პოზიცია))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            დაწკაპუნება_მნიშვნელობა(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for სიმბოლო_მნიშვნელობა_068c2631 in '한글':누름값(0x1000000|ord(სიმბოლო_მნიშვნელობა_068c2631));누름값(0x1000000|ord(სიმბოლო_მნიშვნელობა_068c2631),False)
            for 횟수 in (1,2):
                გაშვება=len(대화기록);დაწკაპუნება_მნიშვნელობა(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),გაშვება)
            time.sleep(.3)
            ფანჯარა_ნახატი=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=ფანჯარა_ნახატი.crop((110,272,530,300)).tobytes()
            ფანჯარა_ნახატი.save(str(გაზომვა_მონაცემები/'java-swing.png'))
            გაშვება=len(대화기록);დაწკაპუნება_მნიშვნელობა(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',გაშვება)
        # Download the guest-created bytes through FTP in the same GUI VM.
        ფაილი_შენატანი_სახელი={'java':'java.txt','c':'c.txt','python':'python.txt'}[ენა]
        გარემო('cp '+ფაილი_შენატანი_სახელი+' /შემოწმება.txt')
        받은수=bytearray();ფაილი_გადატანა_კავშირი.retrbinary('RETR შემოწმება.txt',받은수.extend);assert 받은수==예상파일.encode()
        გარემო('echo preserved > 출력예제.'+('py' if ენა=='python' else ენა))
        assert 'EXAMPLES READY' in გარემო('example '+ენა)
        assert '\npreserved\n' in გარემო('cat 출력예제.'+('py' if ენა=='python' else ენა))
        assert '한/영 კლავიში_მნიშვნელობა, Shift+Space 또는 F9' in გარემო('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in გარემო('echo GUI NETWORK TOGETHER')
        ფაილი_გადატანა_კავშირი.quit();ფაილი_გადატანა_კავშირი=None;assert 'FTP stopped' in გარემო('ftpd stop')
        print('PASS '+ენა+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if ფაილი_გადატანა_კავშირი:
            try:ფაილი_გადატანა_კავშირი.close()
            except OSError:pass
        if კლიენტი:კლიენტი.close()
        პროცესი.terminate()
        try:პროცესი.wait(timeout=8)
        except subprocess.TimeoutExpired:პროცესი.kill();პროცესი.wait()
        სელექტორი.close();პროცესი.stdout.close();(გაზომვა_მონაცემები/(ენა+'-serial.log')).write_bytes(대화기록)


def გაშვება():
    გაზომვა_მონაცემები=პროეცირება_ფესვი/'build/verification/examples';გაზომვა_მონაცემები.mkdir(parents=True,exist_ok=True)
    გადამოწმება_ანგარიში={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((პროეცირება_ფესვი/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for ენა in ('java','c','python'):
                test_언어(ენა,되돌림서버항목,გაზომვა_მონაცემები);გადამოწმება_ანგარიში['languages'].append(ენა)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(კატეგორია_მნიშვნელობა,მონაცემები.encode()) for კატეგორია_მნიშვნელობა,მონაცემები in 예상결과],되돌림서버항목.수신됨
            გადამოწმება_ანგარიში['host_network_payloads']=[{'protocol':კატეგორია_მნიშვნელობა,'text':მონაცემები.decode()} for კატეგორია_მნიშვნელობა,მონაცემები in 되돌림서버항목.수신됨]
        გადამოწმება_ანგარიში.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(გაზომვა_მონაცემები/'report.json').write_text(json.dumps(გადამოწმება_ანგარიში,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':გაშვება()
