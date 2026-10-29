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
from ዴስክቶፕ_እየው import 정확한값
from 예제되돌림서버 import 되돌림서버
from ፈጽም_ትእዛዝ import አሳይ_ስር


def test_언어(ቋንቋ,되돌림서버항목,ልኬት_ውሂብ):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));ፋይል_ትልልፍ_የወደብ_ቁጥር=임시자원.getsockname()[1]
    ሂደቶች=subprocess.Popen(['python3',str(አሳይ_ስር/'መሳሪያዎች/ፈጽም_ትእዛዝ.py'),'--desktop','--network','--port','0','--ftp-port',str(ፋይል_ትልልፍ_የወደብ_ቁጥር)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    መራጭ=selectors.DefaultSelector();መራጭ.register(ሂደቶች.stdout,selectors.EVENT_READ)
    대화기록=bytearray();ተገልጋይ=None;ፋይል_ትልልፍ_ግንኙነት=None
    def 수신하기(확인표시,ማስኬጃ=0):
        ጨርስ_ዝንፍ=time.monotonic()+60
        while 확인표시 not in 대화기록[ማስኬጃ:]:
            if time.monotonic()>ጨርስ_ዝንፍ or ሂደቶች.poll() is not None:raise AssertionError(대화기록[ማስኬጃ:].decode('utf-8','replace'))
            for 누름값,_ in መራጭ.select(.1):
                ውሂብ=누름값.fileobj.read(65536)
                if ውሂብ:대화기록.extend(ውሂብ)
        return 대화기록[ማስኬጃ:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(ምልክት_እሴት,누르는중=True):ተገልጋይ.sendall(struct.pack('>BBHI',4,int(누르는중),0,ምልክት_እሴት))
    def ጀምር_ዝንፍ(መስመር):
        ማስኬጃ=len(대화기록)
        for የቁምፊ_ኮድ in መስመር+'\n':
            ምልክት_እሴት=0xff0d if የቁምፊ_ኮድ=='\n' else ord(የቁምፊ_ኮድ) if ord(የቁምፊ_ኮድ)<256 else 0x1000000|ord(የቁምፊ_ኮድ)
            누름값(ምልክት_እሴት);누름값(ምልክት_እሴት,False)
        return ማስኬጃ
    def ሼል(መስመር):return 수신하기(b'jkoros-native> ',ጀምር_ዝንፍ(መስመር))
    def ፈጽም_ትእዛዝ(መስመር,예상결과):
        ጽሁፍ=ሼል(መስመር);assert 예상결과 in ጽሁፍ and 'exit 0' in ጽሁፍ,(መስመር,ጽሁፍ)
        return ጽሁፍ
    def 화소들():
        ተገልጋይ.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            ምድብ_እሴት=정확한값(ተገልጋይ,1)[0]
            if ምድብ_እሴት==2:continue
            if ምድብ_እሴት==3:
                개수=struct.unpack('>I',정확한값(ተገልጋይ,7)[3:])[0];정확한값(ተገልጋይ,개수);continue
            assert ምድብ_እሴት==0,ምድብ_እሴት
            항목수=struct.unpack('>H',정확한값(ተገልጋይ,3)[1:])[0]
            for _ in range(항목수):
                ኤክስ_አስተባባሪ,세로좌표,너비값,높이값,የቁምፊ_ጥምር=struct.unpack('>HHHHi',정확한값(ተገልጋይ,12));assert የቁምፊ_ጥምር==0,የቁምፊ_ጥምር
                ውሂብ=정확한값(ተገልጋይ,너비값*높이값*4)
                for ረድፍ_በቦታ_አስቀመጠ in range(높이값):
                    for አምድ_በቦታ_አስቀመጠ in range(너비값):
                        원본자료=(ረድፍ_በቦታ_አስቀመጠ*너비값+አምድ_በቦታ_አስቀመጠ)*4;ዓላማ=((세로좌표+ረድፍ_በቦታ_አስቀመጠ)*640+ኤክስ_አስተባባሪ+አምድ_በቦታ_አስቀመጠ)*3
                        빛삼원색[ዓላማ:ዓላማ+3]=bytes((ውሂብ[원본자료+2],ውሂብ[원본자료+1],ውሂብ[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        የወደብ_ቁጥር=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        ተገልጋይ=socket.create_connection(('127.0.0.1',የወደብ_ቁጥር),timeout=10)
        assert 정확한값(ተገልጋይ,12)==b'RFB 003.008\n';ተገልጋይ.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(ተገልጋይ,정확한값(ተገልጋይ,1)[0]);ተገልጋይ.sendall(b'\x01');assert 정확한값(ተገልጋይ,4)==b'\0'*4
        ተገልጋይ.sendall(b'\x01');초기값=정확한값(ተገልጋይ,24);정확한값(ተገልጋይ,struct.unpack('>I',초기값[20:])[0])
        ተገልጋይ.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        ተገልጋይ.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in ሼል('ftpd start')
        ፋይል_ትልልፍ_ግንኙነት=ftplib.FTP();ፋይል_ትልልፍ_ግንኙነት.encoding='utf-8';ፋይል_ትልልፍ_ግንኙነት.connect('127.0.0.1',ፋይል_ትልልፍ_የወደብ_ቁጥር,timeout=20);ፋይል_ትልልፍ_ግንኙነት.login()
        የክፍያ_ጫና_ውሂብ=('GUI와 FTP 동시 사용 '+ቋንቋ+' 😀\n').encode()
        ፋይል_ትልልፍ_ግንኙነት.storbinary('STOR 함께.txt',io.BytesIO(የክፍያ_ጫና_ውሂብ))
        assert የክፍያ_ጫና_ውሂብ.decode().strip() in ሼል('cat /함께.txt')
        받은수=bytearray();ፋይል_ትልልፍ_ግንኙነት.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==የክፍያ_ጫና_ውሂብ;ፋይል_ትልልፍ_ግንኙነት.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        ላክ_ዝርዝር=ሼል('ls /example')
        assert all(ስም in ላክ_ዝርዝር for ስም in ('java/','c/','python/','README.md')),ላክ_ዝርዝር
        if ቋንቋ=='java':
            꾸러미명세=json.loads((አሳይ_ስር/'build/examples/manifest.json').read_text())
            for መተላለፊያ,ምዝግብ_ቦታ in 꾸러미명세.items():
                ሼል('cp '+መተላለፊያ+' /example-check.bin')
                ይዘት_እሴት=bytearray();ፋይል_ትልልፍ_ግንኙነት.retrbinary('RETR example-check.bin',ይዘት_እሴት.extend)
                assert len(ይዘት_እሴት)==ምዝግብ_ቦታ['bytes'] and hashlib.sha256(ይዘት_እሴት).hexdigest()==ምዝግብ_ቦታ['sha256'],መተላለፊያ
            ፋይል_ትልልፍ_ግንኙነት.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            ባይነሪ=bytes(range(256))*64
            ፋይል_ትልልፍ_ግንኙነት.storbinary('STOR boundary.bin',io.BytesIO(ባይነሪ))
            ይዘት_እሴት=bytearray();ፋይል_ትልልፍ_ግንኙነት.retrbinary('RETR boundary.bin',ይዘት_እሴት.extend)
            assert ይዘት_እሴት==ባይነሪ and 'boundary.bin' in ፋይል_ትልልፍ_ግንኙነት.nlst()
            ሼል('cp /boundary.bin /boundary-copy.bin')
            ይዘት_እሴት=bytearray();ፋይል_ትልልፍ_ግንኙነት.retrbinary('RETR boundary-copy.bin',ይዘት_እሴት.extend)
            assert ይዘት_እሴት==ባይነሪ
            ፋይል_ትልልፍ_ግንኙነት.delete('boundary.bin');ፋይል_ትልልፍ_ግንኙነት.delete('boundary-copy.bin')
        assert '출력예제' in ሼል('ls /example/'+ቋንቋ)
        ሼል('cd /example/'+ቋንቋ)
        ስም_ሰንጠረዥ={'java':'JAVA','c':'C','python':'PYTHON'}[ቋንቋ]
        예상파일=ስም_ሰንጠረዥ+' ፋይል: 한글 ውሂብ 😀\n'
        if ቋንቋ=='java':
            ፈጽም_ትእዛዝ('javac 출력예제.java','Compiled:');ፈጽም_ትእዛዝ('java 출력예제','JAVA ውጤት: 안녕하세요 😀')
            ፈጽም_ትእዛዝ('javac 파일예제.java','Compiled:');ፈጽም_ትእዛዝ('java 파일예제',예상파일)
            ፈጽም_ትእዛዝ('java 네트워크예제 {} {}'.format(되돌림서버항목.የትልልፍ_ቁጥጥር_ፕሮቶኮል_ወደብ,되돌림서버항목.전문접속번호),'JAVA 네트워크 አረጋግጥ: TCP UDP 한글')
            ግራፊክስ_ትእዛዝ='java 그래픽예제'
        elif ቋንቋ=='c':
            for ስም,전달값,예상결과 in [('ውጤት','', 'C ውጤት: 안녕하세요 😀'),('ፋይል','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 አረጋግጥ: UDP 한글')]:
                ፈጽም_ትእዛዝ('cc '+ስም+'예제.c -o ፈጽም_ትእዛዝ','Compiled native ARM64 ELF:')
                ፈጽም_ትእዛዝ('./ፈጽም_ትእዛዝ'+전달값,예상결과)
            ፈጽም_ትእዛዝ('cc 그래픽예제.c -o ፈጽም_ትእዛዝ','Compiled native ARM64 ELF:');ግራፊክስ_ትእዛዝ='./ፈጽም_ትእዛዝ'
        else:
            for ስም,전달값,예상결과 in [('ውጤት','','PYTHON ውጤት: 안녕하세요 😀'),('ፋይል','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 አረጋግጥ: UDP 한글')]:
                ፈጽም_ትእዛዝ('python '+ስም+'예제.py'+전달값,예상결과)
            ግራፊክስ_ትእዛዝ='python 그래픽예제.py'
        ጀምር_ስዕል=ጀምር_ዝንፍ(ግራፊክስ_ትእዛዝ)
        ጽሁፍ=수신하기('그림을 확인한 ተመለስ_እሴት Enter를 누르세요.\r\n'.encode(),ጀምር_ስዕል)
        assert ስም_ሰንጠረዥ+' 그래픽: 빨강 초록 파랑' in ጽሁፍ and 'exit 0' not in ጽሁፍ,ጽሁፍ
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        ፋይል_ትልልፍ_ግንኙነት.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();ፋይል_ትልልፍ_ግንኙነት.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';ፋይል_ትልልፍ_ግንኙነት.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            ዝንፍ_እሴት=(세로좌표*640+610)*3;assert tuple(빛삼원색[ዝንፍ_እሴት:ዝንፍ_እሴት+3])==색상,(ቋንቋ,세로좌표,tuple(빛삼원색[ዝንፍ_እሴት:ዝንፍ_እሴት+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(ልኬት_ውሂብ/(ቋንቋ+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',ጀምር_ስዕል)
        if ቋንቋ=='java':
            ጀምር_መስኮት=ጀምር_ዝንፍ('java 창예제')
            수신하기('GUI 예제 አዘጋጅ_9ce364fc: 창예제'.encode(),ጀምር_መስኮት)
            def ጠቅ_አድርግ_እሴት(가로,ቋሚ_በቦታ_አስቀመጠ):
                for አዝራር in (1,0):ተገልጋይ.sendall(struct.pack('>BBHH',5,አዝራር,가로,ቋሚ_በቦታ_አስቀመጠ))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            ጠቅ_አድርግ_እሴት(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for ቁምፊ_እሴት in '한글':누름값(0x1000000|ord(ቁምፊ_እሴት));누름값(0x1000000|ord(ቁምፊ_እሴት),False)
            for 횟수 in (1,2):
                ማስኬጃ=len(대화기록);ጠቅ_አድርግ_እሴት(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),ማስኬጃ)
            time.sleep(.3)
            መስኮት_ስዕል=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=መስኮት_ስዕል.crop((110,272,530,300)).tobytes()
            መስኮት_ስዕል.save(str(ልኬት_ውሂብ/'java-swing.png'))
            ማስኬጃ=len(대화기록);ጠቅ_አድርግ_እሴት(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',ማስኬጃ)
        # Download the guest-created bytes through FTP in the same GUI VM.
        ፋይል_ምዝግብ_ስም={'java':'java.txt','c':'c.txt','python':'python.txt'}[ቋንቋ]
        ሼል('cp '+ፋይል_ምዝግብ_ስም+' /ትክክለኛነት_አረጋግጥ.txt')
        받은수=bytearray();ፋይል_ትልልፍ_ግንኙነት.retrbinary('RETR ትክክለኛነት_አረጋግጥ.txt',받은수.extend);assert 받은수==예상파일.encode()
        ሼል('echo preserved > 출력예제.'+('py' if ቋንቋ=='python' else ቋንቋ))
        assert 'EXAMPLES READY' in ሼል('example '+ቋንቋ)
        assert '\npreserved\n' in ሼል('cat 출력예제.'+('py' if ቋንቋ=='python' else ቋንቋ))
        assert '한/영 ቁልፍ_እሴት, Shift+Space 또는 F9' in ሼል('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in ሼል('echo GUI NETWORK TOGETHER')
        ፋይል_ትልልፍ_ግንኙነት.quit();ፋይል_ትልልፍ_ግንኙነት=None;assert 'FTP stopped' in ሼል('ftpd stop')
        print('PASS '+ቋንቋ+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if ፋይል_ትልልፍ_ግንኙነት:
            try:ፋይል_ትልልፍ_ግንኙነት.close()
            except OSError:pass
        if ተገልጋይ:ተገልጋይ.close()
        ሂደቶች.terminate()
        try:ሂደቶች.wait(timeout=8)
        except subprocess.TimeoutExpired:ሂደቶች.kill();ሂደቶች.wait()
        መራጭ.close();ሂደቶች.stdout.close();(ልኬት_ውሂብ/(ቋንቋ+'-serial.log')).write_bytes(대화기록)


def ማስኬጃ():
    ልኬት_ውሂብ=አሳይ_ስር/'build/verification/examples';ልኬት_ውሂብ.mkdir(parents=True,exist_ok=True)
    ማረጋገጥ_ዘገባ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((አሳይ_ስር/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for ቋንቋ in ('java','c','python'):
                test_언어(ቋንቋ,되돌림서버항목,ልኬት_ውሂብ);ማረጋገጥ_ዘገባ['languages'].append(ቋንቋ)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(ምድብ_እሴት,ውሂብ.encode()) for ምድብ_እሴት,ውሂብ in 예상결과],되돌림서버항목.수신됨
            ማረጋገጥ_ዘገባ['host_network_payloads']=[{'protocol':ምድብ_እሴት,'text':ውሂብ.decode()} for ምድብ_እሴት,ውሂብ in 되돌림서버항목.수신됨]
        ማረጋገጥ_ዘገባ.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(ልኬት_ውሂብ/'report.json').write_text(json.dumps(ማረጋገጥ_ዘገባ,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':ማስኬጃ()
