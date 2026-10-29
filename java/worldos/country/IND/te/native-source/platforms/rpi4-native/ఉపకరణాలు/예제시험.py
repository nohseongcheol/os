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
from డెస్క్_టాప్_వీక్షణ import 정확한값
from 예제되돌림서버 import 되돌림서버
from అమలు_చేయి_ఆదేశం import ప్రొజెక్ట్_మూలం


def test_언어(భాష,되돌림서버항목,ప్రమాణం_డేటా):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));ఫైలు_బదిలీ_పోర్ట్_సంఖ్య=임시자원.getsockname()[1]
    క్రమణం=subprocess.Popen(['python3',str(ప్రొజెక్ట్_మూలం/'ఉపకరణాలు/అమలు_చేయి_ఆదేశం.py'),'--desktop','--network','--port','0','--ftp-port',str(ఫైలు_బదిలీ_పోర్ట్_సంఖ్య)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    సెలక్టర్=selectors.DefaultSelector();సెలక్టర్.register(క్రమణం.stdout,selectors.EVENT_READ)
    대화기록=bytearray();క్లయింట్=None;ఫైలు_బదిలీ_కనెక్షన్=None
    def 수신하기(확인표시,నడుపుము=0):
        ముగించు_ఆఫ్_సెట్=time.monotonic()+60
        while 확인표시 not in 대화기록[నడుపుము:]:
            if time.monotonic()>ముగించు_ఆఫ్_సెట్ or క్రమణం.poll() is not None:raise AssertionError(대화기록[నడుపుము:].decode('utf-8','replace'))
            for 누름값,_ in సెలక్టర్.select(.1):
                డేటా=누름값.fileobj.read(65536)
                if డేటా:대화기록.extend(డేటా)
        return 대화기록[నడుపుము:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(చిహ్నం_మూల్యం,누르는중=True):క్లయింట్.sendall(struct.pack('>BBHI',4,int(누르는중),0,చిహ్నం_మూల్యం))
    def ప్రారంభం_ఆఫ్_సెట్(పంక్తి):
        నడుపుము=len(대화기록)
        for అక్షర_కోడ్ in పంక్తి+'\n':
            చిహ్నం_మూల్యం=0xff0d if అక్షర_కోడ్=='\n' else ord(అక్షర_కోడ్) if ord(అక్షర_కోడ్)<256 else 0x1000000|ord(అక్షర_కోడ్)
            누름값(చిహ్నం_మూల్యం);누름값(చిహ్నం_మూల్యం,False)
        return నడుపుము
    def షెల్(పంక్తి):return 수신하기(b'jkoros-native> ',ప్రారంభం_ఆఫ్_సెట్(పంక్తి))
    def అమలు_చేయి_ఆదేశం(పంక్తి,예상결과):
        పాఠ్యము=షెల్(పంక్తి);assert 예상결과 in పాఠ్యము and 'exit 0' in పాఠ్యము,(పంక్తి,పాఠ్యము)
        return పాఠ్యము
    def 화소들():
        క్లయింట్.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            వర్గం_మూల్యం=정확한값(క్లయింట్,1)[0]
            if వర్గం_మూల్యం==2:continue
            if వర్గం_మూల్యం==3:
                개수=struct.unpack('>I',정확한값(క్లయింట్,7)[3:])[0];정확한값(క్లయింట్,개수);continue
            assert వర్గం_మూల్యం==0,వర్గం_మూల్యం
            항목수=struct.unpack('>H',정확한값(క్లయింట్,3)[1:])[0]
            for _ in range(항목수):
                x_నిర్దేశాంకం,Y_బటన్_సమన్వయపరుచు,너비값,높이값,అక్షర_సమితి=struct.unpack('>HHHHi',정확한값(క్లయింట్,12));assert అక్షర_సమితి==0,అక్షర_సమితి
                డేటా=정확한값(క్లయింట్,너비값*높이값*4)
                for వరుస_స్థాయి in range(높이값):
                    for కాలమ్_స్థాయి in range(너비값):
                        원본자료=(వరుస_స్థాయి*너비값+కాలమ్_స్థాయి)*4;లక్ష్యం=((Y_బటన్_సమన్వయపరుచు+వరుస_స్థాయి)*640+x_నిర్దేశాంకం+కాలమ్_స్థాయి)*3
                        빛삼원색[లక్ష్యం:లక్ష్యం+3]=bytes((డేటా[원본자료+2],డేటా[원본자료+1],డేటా[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        పోర్ట్_సంఖ్య=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        క్లయింట్=socket.create_connection(('127.0.0.1',పోర్ట్_సంఖ్య),timeout=10)
        assert 정확한값(క్లయింట్,12)==b'RFB 003.008\n';క్లయింట్.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(క్లయింట్,정확한값(క్లయింట్,1)[0]);క్లయింట్.sendall(b'\x01');assert 정확한값(క్లయింట్,4)==b'\0'*4
        క్లయింట్.sendall(b'\x01');초기값=정확한값(క్లయింట్,24);정확한값(క్లయింట్,struct.unpack('>I',초기값[20:])[0])
        క్లయింట్.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        క్లయింట్.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in షెల్('ftpd start')
        ఫైలు_బదిలీ_కనెక్షన్=ftplib.FTP();ఫైలు_బదిలీ_కనెక్షన్.encoding='utf-8';ఫైలు_బదిలీ_కనెక్షన్.connect('127.0.0.1',ఫైలు_బదిలీ_పోర్ట్_సంఖ్య,timeout=20);ఫైలు_బదిలీ_కనెక్షన్.login()
        చెల్లింపుభారం_డేటా=('GUI와 FTP 동시 사용 '+భాష+' 😀\n').encode()
        ఫైలు_బదిలీ_కనెక్షన్.storbinary('STOR 함께.txt',io.BytesIO(చెల్లింపుభారం_డేటా))
        assert చెల్లింపుభారం_డేటా.decode().strip() in షెల్('cat /함께.txt')
        받은수=bytearray();ఫైలు_బదిలీ_కనెక్షన్.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==చెల్లింపుభారం_డేటా;ఫైలు_బదిలీ_కనెక్షన్.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        పంపు_జాబితా=షెల్('ls /example')
        assert all(పేరు in పంపు_జాబితా for పేరు in ('java/','c/','python/','README.md')),పంపు_జాబితా
        if భాష=='java':
            꾸러미명세=json.loads((ప్రొజెక్ట్_మూలం/'build/examples/manifest.json').read_text())
            for పాత్,ప్రవేశం_పాయింట్ in 꾸러미명세.items():
                షెల్('cp '+పాత్+' /example-check.bin')
                విషయం_మూల్యం=bytearray();ఫైలు_బదిలీ_కనెక్షన్.retrbinary('RETR example-check.bin',విషయం_మూల్యం.extend)
                assert len(విషయం_మూల్యం)==ప్రవేశం_పాయింట్['bytes'] and hashlib.sha256(విషయం_మూల్యం).hexdigest()==ప్రవేశం_పాయింట్['sha256'],పాత్
            ఫైలు_బదిలీ_కనెక్షన్.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            బైనరీ=bytes(range(256))*64
            ఫైలు_బదిలీ_కనెక్షన్.storbinary('STOR boundary.bin',io.BytesIO(బైనరీ))
            విషయం_మూల్యం=bytearray();ఫైలు_బదిలీ_కనెక్షన్.retrbinary('RETR boundary.bin',విషయం_మూల్యం.extend)
            assert విషయం_మూల్యం==బైనరీ and 'boundary.bin' in ఫైలు_బదిలీ_కనెక్షన్.nlst()
            షెల్('cp /boundary.bin /boundary-copy.bin')
            విషయం_మూల్యం=bytearray();ఫైలు_బదిలీ_కనెక్షన్.retrbinary('RETR boundary-copy.bin',విషయం_మూల్యం.extend)
            assert విషయం_మూల్యం==బైనరీ
            ఫైలు_బదిలీ_కనెక్షన్.delete('boundary.bin');ఫైలు_బదిలీ_కనెక్షన్.delete('boundary-copy.bin')
        assert '출력예제' in షెల్('ls /example/'+భాష)
        షెల్('cd /example/'+భాష)
        పేరు_పట్టిక={'java':'JAVA','c':'C','python':'PYTHON'}[భాష]
        예상파일=పేరు_పట్టిక+' దస్త్రం: 한글 డేటా 😀\n'
        if భాష=='java':
            అమలు_చేయి_ఆదేశం('javac 출력예제.java','Compiled:');అమలు_చేయి_ఆదేశం('java 출력예제','JAVA అవుట్పుట్: 안녕하세요 😀')
            అమలు_చేయి_ఆదేశం('javac 파일예제.java','Compiled:');అమలు_చేయి_ఆదేశం('java 파일예제',예상파일)
            అమలు_చేయి_ఆదేశం('java 네트워크예제 {} {}'.format(되돌림서버항목.ట్రాన్స్_మిషన్_కంట్రోల్_ప్రోటోకాల్_పోర్టు,되돌림서버항목.전문접속번호),'JAVA 네트워크 సరిచూడు: TCP UDP 한글')
            గ్రాఫిక్స్_ఆదేశం='java 그래픽예제'
        elif భాష=='c':
            for పేరు,전달값,예상결과 in [('అవుట్పుట్','', 'C అవుట్పుట్: 안녕하세요 😀'),('దస్త్రం','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 సరిచూడు: UDP 한글')]:
                అమలు_చేయి_ఆదేశం('cc '+పేరు+'예제.c -o అమలు_చేయి_ఆదేశం','Compiled native ARM64 ELF:')
                అమలు_చేయి_ఆదేశం('./అమలు_చేయి_ఆదేశం'+전달값,예상결과)
            అమలు_చేయి_ఆదేశం('cc 그래픽예제.c -o అమలు_చేయి_ఆదేశం','Compiled native ARM64 ELF:');గ్రాఫిక్స్_ఆదేశం='./అమలు_చేయి_ఆదేశం'
        else:
            for పేరు,전달값,예상결과 in [('అవుట్పుట్','','PYTHON అవుట్పుట్: 안녕하세요 😀'),('దస్త్రం','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 సరిచూడు: UDP 한글')]:
                అమలు_చేయి_ఆదేశం('python '+పేరు+'예제.py'+전달값,예상결과)
            గ్రాఫిక్స్_ఆదేశం='python 그래픽예제.py'
        ప్రారంభం_రేఖాచిత్రణ=ప్రారంభం_ఆఫ్_సెట్(గ్రాఫిక్స్_ఆదేశం)
        పాఠ్యము=수신하기('그림을 확인한 వెనుకకు_మూల్యం Enter를 누르세요.\r\n'.encode(),ప్రారంభం_రేఖాచిత్రణ)
        assert పేరు_పట్టిక+' 그래픽: 빨강 초록 파랑' in పాఠ్యము and 'exit 0' not in పాఠ్యము,పాఠ్యము
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        ఫైలు_బదిలీ_కనెక్షన్.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();ఫైలు_బదిలీ_కనెక్షన్.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';ఫైలు_బదిలీ_కనెక్షన్.delete('도중.txt')
        빛삼원색=화소들()
        for Y_బటన్_సమన్వయపరుచు,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            ఆఫ్_సెట్_మూల్యం=(Y_బటన్_సమన్వయపరుచు*640+610)*3;assert tuple(빛삼원색[ఆఫ్_సెట్_మూల్యం:ఆఫ్_సెట్_మూల్యం+3])==색상,(భాష,Y_బటన్_సమన్వయపరుచు,tuple(빛삼원색[ఆఫ్_సెట్_మూల్యం:ఆఫ్_సెట్_మూల్యం+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(ప్రమాణం_డేటా/(భాష+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',ప్రారంభం_రేఖాచిత్రణ)
        if భాష=='java':
            ప్రారంభం_గవాక్షం=ప్రారంభం_ఆఫ్_సెట్('java 창예제')
            수신하기('GUI 예제 సిద్ధం_చేయు: 창예제'.encode(),ప్రారంభం_గవాక్షం)
            def క్లిక్_చెయండి_మూల్యం(가로,నిలువు_స్థాయి):
                for బటన్ in (1,0):క్లయింట్.sendall(struct.pack('>BBHH',5,బటన్,가로,నిలువు_స్థాయి))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            క్లిక్_చెయండి_మూల్యం(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for అక్షరం_మూల్యం in '한글':누름값(0x1000000|ord(అక్షరం_మూల్యం));누름값(0x1000000|ord(అక్షరం_మూల్యం),False)
            for 횟수 in (1,2):
                నడుపుము=len(대화기록);క్లిక్_చెయండి_మూల్యం(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),నడుపుము)
            time.sleep(.3)
            గవాక్షం_రేఖాచిత్రణ=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=గవాక్షం_రేఖాచిత్రణ.crop((110,272,530,300)).tobytes()
            గవాక్షం_రేఖాచిత్రణ.save(str(ప్రమాణం_డేటా/'java-swing.png'))
            నడుపుము=len(대화기록);క్లిక్_చెయండి_మూల్యం(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',నడుపుము)
        # Download the guest-created bytes through FTP in the same GUI VM.
        ఫైలు_ప్రవేశం_పేరు={'java':'java.txt','c':'c.txt','python':'python.txt'}[భాష]
        షెల్('cp '+ఫైలు_ప్రవేశం_పేరు+' /నిర్థారీకరించు.txt')
        받은수=bytearray();ఫైలు_బదిలీ_కనెక్షన్.retrbinary('RETR నిర్థారీకరించు.txt',받은수.extend);assert 받은수==예상파일.encode()
        షెల్('echo preserved > 출력예제.'+('py' if భాష=='python' else భాష))
        assert 'EXAMPLES READY' in షెల్('example '+భాష)
        assert '\npreserved\n' in షెల్('cat 출력예제.'+('py' if భాష=='python' else భాష))
        assert '한/영 కీ_మూల్యం, Shift+Space 또는 F9' in షెల్('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in షెల్('echo GUI NETWORK TOGETHER')
        ఫైలు_బదిలీ_కనెక్షన్.quit();ఫైలు_బదిలీ_కనెక్షన్=None;assert 'FTP stopped' in షెల్('ftpd stop')
        print('PASS '+భాష+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if ఫైలు_బదిలీ_కనెక్షన్:
            try:ఫైలు_బదిలీ_కనెక్షన్.close()
            except OSError:pass
        if క్లయింట్:క్లయింట్.close()
        క్రమణం.terminate()
        try:క్రమణం.wait(timeout=8)
        except subprocess.TimeoutExpired:క్రమణం.kill();క్రమణం.wait()
        సెలక్టర్.close();క్రమణం.stdout.close();(ప్రమాణం_డేటా/(భాష+'-serial.log')).write_bytes(대화기록)


def నడుపుము():
    ప్రమాణం_డేటా=ప్రొజెక్ట్_మూలం/'build/verification/examples';ప్రమాణం_డేటా.mkdir(parents=True,exist_ok=True)
    నిర్ధారణ_నివేదిక={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ప్రొజెక్ట్_మూలం/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for భాష in ('java','c','python'):
                test_언어(భాష,되돌림서버항목,ప్రమాణం_డేటా);నిర్ధారణ_నివేదిక['languages'].append(భాష)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(వర్గం_మూల్యం,డేటా.encode()) for వర్గం_మూల్యం,డేటా in 예상결과],되돌림서버항목.수신됨
            నిర్ధారణ_నివేదిక['host_network_payloads']=[{'protocol':వర్గం_మూల్యం,'text':డేటా.decode()} for వర్గం_మూల్యం,డేటా in 되돌림서버항목.수신됨]
        నిర్ధారణ_నివేదిక.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(ప్రమాణం_డేటా/'report.json').write_text(json.dumps(నిర్ధారణ_నివేదిక,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':నడుపుము()
