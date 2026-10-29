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
from ዴስክቶፕ_ትርኢት import 정확한값
from 예제되돌림서버 import 되돌림서버
from ተግብር_ትእዛዝ import 기준


def test_언어(ቋንቋ,되돌림서버항목,결과자료):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    መስርሕ=subprocess.Popen(['python3',str(기준/'መሳርሒታት/ተግብር_ትእዛዝ.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    መራፂ=selectors.DefaultSelector();መራፂ.register(መስርሕ.stdout,selectors.EVENT_READ)
    대화기록=bytearray();ዓሚል=None;ፋይል_ምስጋር_ርክብ=None
    def 수신하기(확인표시,ኣኺድ=0):
        ኣቑም_ሽፋን=time.monotonic()+60
        while 확인표시 not in 대화기록[ኣኺድ:]:
            if time.monotonic()>ኣቑም_ሽፋን or መስርሕ.poll() is not None:raise AssertionError(대화기록[ኣኺድ:].decode('utf-8','replace'))
            for 누름값,_ in መራፂ.select(.1):
                ሓበሬታ=누름값.fileobj.read(65536)
                if ሓበሬታ:대화기록.extend(ሓበሬታ)
        return 대화기록[ኣኺድ:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(ምልክት_ዋጋ,누르는중=True):ዓሚል.sendall(struct.pack('>BBHI',4,int(누르는중),0,ምልክት_ዋጋ))
    def ጀምር_ሽፋን(መስመር):
        ኣኺድ=len(대화기록)
        for ኮድ_ፊደል in መስመር+'\n':
            ምልክት_ዋጋ=0xff0d if ኮድ_ፊደል=='\n' else ord(ኮድ_ፊደል) if ord(ኮድ_ፊደል)<256 else 0x1000000|ord(ኮድ_ፊደል)
            누름값(ምልክት_ዋጋ);누름값(ምልክት_ዋጋ,False)
        return ኣኺድ
    def ሽፋን(መስመር):return 수신하기(b'jkoros-native> ',ጀምር_ሽፋን(መስመር))
    def ተግብር_ትእዛዝ(መስመር,예상결과):
        ጽሑፍ=ሽፋን(መስመር);assert 예상결과 in ጽሑፍ and 'exit 0' in ጽሑፍ,(መስመር,ጽሑፍ)
        return ጽሑፍ
    def 화소들():
        ዓሚል.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            መደብ_ዋጋ=정확한값(ዓሚል,1)[0]
            if መደብ_ዋጋ==2:continue
            if መደብ_ዋጋ==3:
                개수=struct.unpack('>I',정확한값(ዓሚል,7)[3:])[0];정확한값(ዓሚል,개수);continue
            assert መደብ_ዋጋ==0,መደብ_ዋጋ
            항목수=struct.unpack('>H',정확한값(ዓሚል,3)[1:])[0]
            for _ in range(항목수):
                가로좌표,세로좌표,너비값,높이값,እኩባት_ፊደላት=struct.unpack('>HHHHi',정확한값(ዓሚል,12));assert እኩባት_ፊደላት==0,እኩባት_ፊደላት
                ሓበሬታ=정확한값(ዓሚል,너비값*높이값*4)
                for 행위치 in range(높이값):
                    for 열위치 in range(너비값):
                        원본자료=(행위치*너비값+열위치)*4;ዕላማ=((세로좌표+행위치)*640+가로좌표+열위치)*3
                        빛삼원색[ዕላማ:ዕላማ+3]=bytes((ሓበሬታ[원본자료+2],ሓበሬታ[원본자료+1],ሓበሬታ[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        ዓሚል=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert 정확한값(ዓሚል,12)==b'RFB 003.008\n';ዓሚል.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(ዓሚል,정확한값(ዓሚል,1)[0]);ዓሚል.sendall(b'\x01');assert 정확한값(ዓሚል,4)==b'\0'*4
        ዓሚል.sendall(b'\x01');초기값=정확한값(ዓሚል,24);정확한값(ዓሚል,struct.unpack('>I',초기값[20:])[0])
        ዓሚል.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        ዓሚል.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in ሽፋን('ftpd start')
        ፋይል_ምስጋር_ርክብ=ftplib.FTP();ፋይል_ምስጋር_ርክብ.encoding='utf-8';ፋይል_ምስጋር_ርክብ.connect('127.0.0.1',파일전송접속번호,timeout=20);ፋይል_ምስጋር_ርክብ.login()
        ጽዕነት_ክፍሊት_ሓበሬታ=('GUI와 FTP 동시 사용 '+ቋንቋ+' 😀\n').encode()
        ፋይል_ምስጋር_ርክብ.storbinary('STOR 함께.txt',io.BytesIO(ጽዕነት_ክፍሊት_ሓበሬታ))
        assert ጽዕነት_ክፍሊት_ሓበሬታ.decode().strip() in ሽፋን('cat /함께.txt')
        받은수=bytearray();ፋይል_ምስጋር_ርክብ.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==ጽዕነት_ክፍሊት_ሓበሬታ;ፋይል_ምስጋር_ርክብ.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        ለኣኽ_ዝርዝር=ሽፋን('ls /example')
        assert all(ሽም in ለኣኽ_ዝርዝር for ሽም in ('java/','c/','python/','README.md')),ለኣኽ_ዝርዝር
        if ቋንቋ=='java':
            꾸러미명세=json.loads((기준/'build/examples/manifest.json').read_text())
            for መገዲ,ምእታው_ነጥቢ in 꾸러미명세.items():
                ሽፋን('cp '+መገዲ+' /example-check.bin')
                ትሕዝቶ_ዋጋ=bytearray();ፋይል_ምስጋር_ርክብ.retrbinary('RETR example-check.bin',ትሕዝቶ_ዋጋ.extend)
                assert len(ትሕዝቶ_ዋጋ)==ምእታው_ነጥቢ['bytes'] and hashlib.sha256(ትሕዝቶ_ዋጋ).hexdigest()==ምእታው_ነጥቢ['sha256'],መገዲ
            ፋይል_ምስጋር_ርክብ.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            ጽምዳዊ=bytes(range(256))*64
            ፋይል_ምስጋር_ርክብ.storbinary('STOR boundary.bin',io.BytesIO(ጽምዳዊ))
            ትሕዝቶ_ዋጋ=bytearray();ፋይል_ምስጋር_ርክብ.retrbinary('RETR boundary.bin',ትሕዝቶ_ዋጋ.extend)
            assert ትሕዝቶ_ዋጋ==ጽምዳዊ and 'boundary.bin' in ፋይል_ምስጋር_ርክብ.nlst()
            ሽፋን('cp /boundary.bin /boundary-copy.bin')
            ትሕዝቶ_ዋጋ=bytearray();ፋይል_ምስጋር_ርክብ.retrbinary('RETR boundary-copy.bin',ትሕዝቶ_ዋጋ.extend)
            assert ትሕዝቶ_ዋጋ==ጽምዳዊ
            ፋይል_ምስጋር_ርክብ.delete('boundary.bin');ፋይል_ምስጋር_ርክብ.delete('boundary-copy.bin')
        assert '출력예제' in ሽፋን('ls /example/'+ቋንቋ)
        ሽፋን('cd /example/'+ቋንቋ)
        ሽም_ሰሌዳ={'java':'JAVA','c':'C','python':'PYTHON'}[ቋንቋ]
        예상파일=ሽም_ሰሌዳ+' ፋይል: 한글 ሓበሬታ 😀\n'
        if ቋንቋ=='java':
            ተግብር_ትእዛዝ('javac 출력예제.java','Compiled:');ተግብር_ትእዛዝ('java 출력예제','JAVA 출력: 안녕하세요 😀')
            ተግብር_ትእዛዝ('javac 파일예제.java','Compiled:');ተግብር_ትእዛዝ('java 파일예제',예상파일)
            ተግብር_ትእዛዝ('java 네트워크예제 {} {}'.format(되돌림서버항목.ናይ_መተሓላላፊ_ተቖጻጻሪ_ፕሮቶኮል_ወደብ,되돌림서버항목.전문접속번호),'JAVA 네트워크 ኣረጋግጽ: TCP UDP 한글')
            그림명령='java 그래픽예제'
        elif ቋንቋ=='c':
            for ሽም,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('ፋይል','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 ኣረጋግጽ: UDP 한글')]:
                ተግብር_ትእዛዝ('cc '+ሽም+'예제.c -o ተግብር_ትእዛዝ','Compiled native ARM64 ELF:')
                ተግብር_ትእዛዝ('./ተግብር_ትእዛዝ'+전달값,예상결과)
            ተግብር_ትእዛዝ('cc 그래픽예제.c -o ተግብር_ትእዛዝ','Compiled native ARM64 ELF:');그림명령='./ተግብር_ትእዛዝ'
        else:
            for ሽም,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('ፋይል','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 ኣረጋግጽ: UDP 한글')]:
                ተግብር_ትእዛዝ('python '+ሽም+'예제.py'+전달값,예상결과)
            그림명령='python 그래픽예제.py'
        ጀምር_ስእሊ=ጀምር_ሽፋን(그림명령)
        ጽሑፍ=수신하기('그림을 확인한 ድሕሪት_ዋጋ Enter를 누르세요.\r\n'.encode(),ጀምር_ስእሊ)
        assert ሽም_ሰሌዳ+' 그래픽: 빨강 초록 파랑' in ጽሑፍ and 'exit 0' not in ጽሑፍ,ጽሑፍ
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        ፋይል_ምስጋር_ርክብ.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();ፋይል_ምስጋር_ርክብ.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';ፋይል_ምስጋር_ርክብ.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            ሽፋን_ዋጋ=(세로좌표*640+610)*3;assert tuple(빛삼원색[ሽፋን_ዋጋ:ሽፋን_ዋጋ+3])==색상,(ቋንቋ,세로좌표,tuple(빛삼원색[ሽፋን_ዋጋ:ሽፋን_ዋጋ+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(결과자료/(ቋንቋ+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',ጀምር_ስእሊ)
        if ቋንቋ=='java':
            ጀምር_መስኮት=ጀምር_ሽፋን('java 창예제')
            수신하기('GUI 예제 ኣዳልው: 창예제'.encode(),ጀምር_መስኮት)
            def ጠዉቕ_ዋጋ(가로,세로):
                for መጠወቒ in (1,0):ዓሚል.sendall(struct.pack('>BBHH',5,መጠወቒ,가로,세로))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            ጠዉቕ_ዋጋ(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for ፊደል_ዋጋ in '한글':누름값(0x1000000|ord(ፊደል_ዋጋ));누름값(0x1000000|ord(ፊደል_ዋጋ),False)
            for 횟수 in (1,2):
                ኣኺድ=len(대화기록);ጠዉቕ_ዋጋ(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),ኣኺድ)
            time.sleep(.3)
            መስኮት_ስእሊ=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=መስኮት_ስእሊ.crop((110,272,530,300)).tobytes()
            መስኮት_ስእሊ.save(str(결과자료/'java-swing.png'))
            ኣኺድ=len(대화기록);ጠዉቕ_ዋጋ(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',ኣኺድ)
        # Download the guest-created bytes through FTP in the same GUI VM.
        ፋይል_ምእታው_ሽም={'java':'java.txt','c':'c.txt','python':'python.txt'}[ቋንቋ]
        ሽፋን('cp '+ፋይል_ምእታው_ሽም+' /አረጋግፅ.txt')
        받은수=bytearray();ፋይል_ምስጋር_ርክብ.retrbinary('RETR አረጋግፅ.txt',받은수.extend);assert 받은수==예상파일.encode()
        ሽፋን('echo preserved > 출력예제.'+('py' if ቋንቋ=='python' else ቋንቋ))
        assert 'EXAMPLES READY' in ሽፋን('example '+ቋንቋ)
        assert '\npreserved\n' in ሽፋን('cat 출력예제.'+('py' if ቋንቋ=='python' else ቋንቋ))
        assert '한/영 መፍትሕ_ዋጋ, Shift+Space 또는 F9' in ሽፋን('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in ሽፋን('echo GUI NETWORK TOGETHER')
        ፋይል_ምስጋር_ርክብ.quit();ፋይል_ምስጋር_ርክብ=None;assert 'FTP stopped' in ሽፋን('ftpd stop')
        print('PASS '+ቋንቋ+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if ፋይል_ምስጋር_ርክብ:
            try:ፋይል_ምስጋር_ርክብ.close()
            except OSError:pass
        if ዓሚል:ዓሚል.close()
        መስርሕ.terminate()
        try:መስርሕ.wait(timeout=8)
        except subprocess.TimeoutExpired:መስርሕ.kill();መስርሕ.wait()
        መራፂ.close();መስርሕ.stdout.close();(결과자료/(ቋንቋ+'-serial.log')).write_bytes(대화기록)


def ኣኺድ():
    결과자료=기준/'build/verification/examples';결과자료.mkdir(parents=True,exist_ok=True)
    ምርግጋፅ_ጸብጻብ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for ቋንቋ in ('java','c','python'):
                test_언어(ቋንቋ,되돌림서버항목,결과자료);ምርግጋፅ_ጸብጻብ['languages'].append(ቋንቋ)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(መደብ_ዋጋ,ሓበሬታ.encode()) for መደብ_ዋጋ,ሓበሬታ in 예상결과],되돌림서버항목.수신됨
            ምርግጋፅ_ጸብጻብ['host_network_payloads']=[{'protocol':መደብ_ዋጋ,'text':ሓበሬታ.decode()} for መደብ_ዋጋ,ሓበሬታ in 되돌림서버항목.수신됨]
        ምርግጋፅ_ጸብጻብ.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(결과자료/'report.json').write_text(json.dumps(ምርግጋፅ_ጸብጻብ,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':ኣኺድ()
