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
from වැඩතලය_දසුන import 정확한값
from 예제되돌림서버 import 되돌림서버
from ක්_රියාත්මක_කරන්න_විධානය import 기준


def test_언어(භාෂාව,되돌림서버항목,결과자료):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    සැකසුම=subprocess.Popen(['python3',str(기준/'මෙවලම්/ක්_රියාත්මක_කරන්න_විධානය.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    වරකය=selectors.DefaultSelector();වරකය.register(සැකසුම.stdout,selectors.EVENT_READ)
    대화기록=bytearray();සේවාලාභීයා=None;ගොනුව_මාරුව_සබැඳුම=None
    def 수신하기(확인표시,ක්_රියාත්මක_කරන්න_2=0):
        නිමා_කරන්න_ඕෆ්සෙට්=time.monotonic()+60
        while 확인표시 not in 대화기록[ක්_රියාත්මක_කරන්න_2:]:
            if time.monotonic()>නිමා_කරන්න_ඕෆ්සෙට් or සැකසුම.poll() is not None:raise AssertionError(대화기록[ක්_රියාත්මක_කරන්න_2:].decode('utf-8','replace'))
            for 누름값,_ in වරකය.select(.1):
                දත්ත=누름값.fileobj.read(65536)
                if දත්ත:대화기록.extend(දත්ත)
        return 대화기록[ක්_රියාත්මක_කරන්න_2:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(සංකේතය_අගය,누르는중=True):සේවාලාභීයා.sendall(struct.pack('>BBHI',4,int(누르는중),0,සංකේතය_අගය))
    def ඇරඹුම_ඕෆ්සෙට්(පේළිය):
        ක්_රියාත්මක_කරන්න_2=len(대화기록)
        for අනුලකුණු_කේතය in පේළිය+'\n':
            සංකේතය_අගය=0xff0d if අනුලකුණු_කේතය=='\n' else ord(අනුලකුණු_කේතය) if ord(අනුලකුණු_කේතය)<256 else 0x1000000|ord(අනුලකුණු_කේතය)
            누름값(සංකේතය_අගය);누름값(සංකේතය_අගය,False)
        return ක්_රියාත්මක_කරන්න_2
    def කවචය(පේළිය):return 수신하기(b'jkoros-native> ',ඇරඹුම_ඕෆ්සෙට්(පේළිය))
    def ක්_රියාත්මක_කරන්න_විධානය(පේළිය,예상결과):
        පෙළ=කවචය(පේළිය);assert 예상결과 in පෙළ and 'exit 0' in පෙළ,(පේළිය,පෙළ)
        return පෙළ
    def 화소들():
        සේවාලාභීයා.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            ප්_රවර්ගය_අගය=정확한값(සේවාලාභීයා,1)[0]
            if ප්_රවර්ගය_අගය==2:continue
            if ප්_රවර්ගය_අගය==3:
                개수=struct.unpack('>I',정확한값(සේවාලාභීයා,7)[3:])[0];정확한값(සේවාලාභීයා,개수);continue
            assert ප්_රවර්ගය_අගය==0,ප්_රවර්ගය_අගය
            항목수=struct.unpack('>H',정확한값(සේවාලාභීයා,3)[1:])[0]
            for _ in range(항목수):
                x_ඛණ්ඩාංකය,세로좌표,너비값,높이값,අනුලකුණු_කුලකය=struct.unpack('>HHHHi',정확한값(සේවාලාභීයා,12));assert අනුලකුණු_කුලකය==0,අනුලකුණු_කුලකය
                දත්ත=정확한값(සේවාලාභීයා,너비값*높이값*4)
                for 행위치 in range(높이값):
                    for 열위치 in range(너비값):
                        원본자료=(행위치*너비값+열위치)*4;ඉලක්කය=((세로좌표+행위치)*640+x_ඛණ්ඩාංකය+열위치)*3
                        빛삼원색[ඉලක්කය:ඉලක්කය+3]=bytes((දත්ත[원본자료+2],දත්ත[원본자료+1],දත්ත[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        සේවාලාභීයා=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert 정확한값(සේවාලාභීයා,12)==b'RFB 003.008\n';සේවාලාභීයා.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(සේවාලාභීයා,정확한값(සේවාලාභීයා,1)[0]);සේවාලාභීයා.sendall(b'\x01');assert 정확한값(සේවාලාභීයා,4)==b'\0'*4
        සේවාලාභීයා.sendall(b'\x01');초기값=정확한값(සේවාලාභීයා,24);정확한값(සේවාලාභීයා,struct.unpack('>I',초기값[20:])[0])
        සේවාලාභීයා.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        සේවාලාභීයා.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in කවචය('ftpd start')
        ගොනුව_මාරුව_සබැඳුම=ftplib.FTP();ගොනුව_මාරුව_සබැඳුම.encoding='utf-8';ගොනුව_මාරුව_සබැඳුම.connect('127.0.0.1',파일전송접속번호,timeout=20);ගොනුව_මාරුව_සබැඳුම.login()
        ගෙවීම්_භාරය_දත්ත=('GUI와 FTP 동시 사용 '+භාෂාව+' 😀\n').encode()
        ගොනුව_මාරුව_සබැඳුම.storbinary('STOR 함께.txt',io.BytesIO(ගෙවීම්_භාරය_දත්ත))
        assert ගෙවීම්_භාරය_දත්ත.decode().strip() in කවචය('cat /함께.txt')
        받은수=bytearray();ගොනුව_මාරුව_සබැඳුම.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==ගෙවීම්_භාරය_දත්ත;ගොනුව_මාරුව_සබැඳුම.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        ඊමේල්_ලැයිස්තුව=කවචය('ls /example')
        assert all(නම in ඊමේල්_ලැයිස්තුව for නම in ('java/','c/','python/','README.md')),ඊමේල්_ලැයිස්තුව
        if භාෂාව=='java':
            꾸러미명세=json.loads((기준/'build/examples/manifest.json').read_text())
            for මාර්_ගය,පිවිසුම_ලකුණ in 꾸러미명세.items():
                කවචය('cp '+මාර්_ගය+' /example-check.bin')
                අන්තර්ගතය_අගය=bytearray();ගොනුව_මාරුව_සබැඳුම.retrbinary('RETR example-check.bin',අන්තර්ගතය_අගය.extend)
                assert len(අන්තර්ගතය_අගය)==පිවිසුම_ලකුණ['bytes'] and hashlib.sha256(අන්තර්ගතය_අගය).hexdigest()==පිවිසුම_ලකුණ['sha256'],මාර්_ගය
            ගොනුව_මාරුව_සබැඳුම.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            ද්විමය=bytes(range(256))*64
            ගොනුව_මාරුව_සබැඳුම.storbinary('STOR boundary.bin',io.BytesIO(ද්විමය))
            අන්තර්ගතය_අගය=bytearray();ගොනුව_මාරුව_සබැඳුම.retrbinary('RETR boundary.bin',අන්තර්ගතය_අගය.extend)
            assert අන්තර්ගතය_අගය==ද්විමය and 'boundary.bin' in ගොනුව_මාරුව_සබැඳුම.nlst()
            කවචය('cp /boundary.bin /boundary-copy.bin')
            අන්තර්ගතය_අගය=bytearray();ගොනුව_මාරුව_සබැඳුම.retrbinary('RETR boundary-copy.bin',අන්තර්ගතය_අගය.extend)
            assert අන්තර්ගතය_අගය==ද්විමය
            ගොනුව_මාරුව_සබැඳුම.delete('boundary.bin');ගොනුව_මාරුව_සබැඳුම.delete('boundary-copy.bin')
        assert '출력예제' in කවචය('ls /example/'+භාෂාව)
        කවචය('cd /example/'+භාෂාව)
        නම_වගුව={'java':'JAVA','c':'C','python':'PYTHON'}[භාෂාව]
        예상파일=නම_වගුව+' ගොනු: 한글 දත්ත 😀\n'
        if භාෂාව=='java':
            ක්_රියාත්මක_කරන්න_විධානය('javac 출력예제.java','Compiled:');ක්_රියාත්මක_කරන්න_විධානය('java 출력예제','JAVA 출력: 안녕하세요 😀')
            ක්_රියාත්මක_කරන්න_විධානය('javac 파일예제.java','Compiled:');ක්_රියාත්මක_කරන්න_විධානය('java 파일예제',예상파일)
            ක්_රියාත්මක_කරන්න_විධානය('java 네트워크예제 {} {}'.format(되돌림서버항목.සම්ප්_රේෂණ_පාලන_ප්_රොටොකෝලය_තොට,되돌림서버항목.전문접속번호),'JAVA 네트워크 තහවුරු_කරන්න: TCP UDP 한글')
            그림명령='java 그래픽예제'
        elif භාෂාව=='c':
            for නම,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('ගොනු','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 තහවුරු_කරන්න: UDP 한글')]:
                ක්_රියාත්මක_කරන්න_විධානය('cc '+නම+'예제.c -o ක්_රියාත්මක_කරන්න_විධානය','Compiled native ARM64 ELF:')
                ක්_රියාත්මක_කරන්න_විධානය('./ක්_රියාත්මක_කරන්න_විධානය'+전달값,예상결과)
            ක්_රියාත්මක_කරන්න_විධානය('cc 그래픽예제.c -o ක්_රියාත්මක_කරන්න_විධානය','Compiled native ARM64 ELF:');그림명령='./ක්_රියාත්මක_කරන්න_විධානය'
        else:
            for නම,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('ගොනු','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 තහවුරු_කරන්න: UDP 한글')]:
                ක්_රියාත්මක_කරන්න_විධානය('python '+නම+'예제.py'+전달값,예상결과)
            그림명령='python 그래픽예제.py'
        ඇරඹුම_චිත්_රය=ඇරඹුම_ඕෆ්සෙට්(그림명령)
        පෙළ=수신하기('그림을 확인한 ආපසු_අගය Enter를 누르세요.\r\n'.encode(),ඇරඹුම_චිත්_රය)
        assert නම_වගුව+' 그래픽: 빨강 초록 파랑' in පෙළ and 'exit 0' not in පෙළ,පෙළ
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        ගොනුව_මාරුව_සබැඳුම.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();ගොනුව_මාරුව_සබැඳුම.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';ගොනුව_මාරුව_සබැඳුම.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            ඕෆ්සෙට්_අගය=(세로좌표*640+610)*3;assert tuple(빛삼원색[ඕෆ්සෙට්_අගය:ඕෆ්සෙට්_අගය+3])==색상,(භාෂාව,세로좌표,tuple(빛삼원색[ඕෆ්සෙට්_අගය:ඕෆ්සෙට්_අගය+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(결과자료/(භාෂාව+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',ඇරඹුම_චිත්_රය)
        if භාෂාව=='java':
            ඇරඹුම_කවුළුව=ඇරඹුම_ඕෆ්සෙට්('java 창예제')
            수신하기('GUI 예제 පිළියෙල_කරන්න: 창예제'.encode(),ඇරඹුම_කවුළුව)
            def ක්ලික්_කරන්න_අගය(가로,세로):
                for බොත්තම in (1,0):සේවාලාභීයා.sendall(struct.pack('>BBHH',5,බොත්තම,가로,세로))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            ක්ලික්_කරන්න_අගය(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for අනුලකුණ_අගය in '한글':누름값(0x1000000|ord(අනුලකුණ_අගය));누름값(0x1000000|ord(අනුලකුණ_අගය),False)
            for 횟수 in (1,2):
                ක්_රියාත්මක_කරන්න_2=len(대화기록);ක්ලික්_කරන්න_අගය(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),ක්_රියාත්මක_කරන්න_2)
            time.sleep(.3)
            කවුළුව_චිත්_රය=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=කවුළුව_චිත්_රය.crop((110,272,530,300)).tobytes()
            කවුළුව_චිත්_රය.save(str(결과자료/'java-swing.png'))
            ක්_රියාත්මක_කරන්න_2=len(대화기록);ක්ලික්_කරන්න_අගය(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',ක්_රියාත්මක_කරන්න_2)
        # Download the guest-created bytes through FTP in the same GUI VM.
        ගොනුව_පිවිසුම_නම={'java':'java.txt','c':'c.txt','python':'python.txt'}[භාෂාව]
        කවචය('cp '+ගොනුව_පිවිසුම_නම+' /වලංගු_කරන්න.txt')
        받은수=bytearray();ගොනුව_මාරුව_සබැඳුම.retrbinary('RETR වලංගු_කරන්න.txt',받은수.extend);assert 받은수==예상파일.encode()
        කවචය('echo preserved > 출력예제.'+('py' if භාෂාව=='python' else භාෂාව))
        assert 'EXAMPLES READY' in කවචය('example '+භාෂාව)
        assert '\npreserved\n' in කවචය('cat 출력예제.'+('py' if භාෂාව=='python' else භාෂාව))
        assert '한/영 යතුර_අගය, Shift+Space 또는 F9' in කවචය('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in කවචය('echo GUI NETWORK TOGETHER')
        ගොනුව_මාරුව_සබැඳුම.quit();ගොනුව_මාරුව_සබැඳුම=None;assert 'FTP stopped' in කවචය('ftpd stop')
        print('PASS '+භාෂාව+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if ගොනුව_මාරුව_සබැඳුම:
            try:ගොනුව_මාරුව_සබැඳුම.close()
            except OSError:pass
        if සේවාලාභීයා:සේවාලාභීයා.close()
        සැකසුම.terminate()
        try:සැකසුම.wait(timeout=8)
        except subprocess.TimeoutExpired:සැකසුම.kill();සැකසුම.wait()
        වරකය.close();සැකසුම.stdout.close();(결과자료/(භාෂාව+'-serial.log')).write_bytes(대화기록)


def ක්_රියාත්මක_කරන්න_2():
    결과자료=기준/'build/verification/examples';결과자료.mkdir(parents=True,exist_ok=True)
    වලංගුකරණය_වාර්තාව={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for භාෂාව in ('java','c','python'):
                test_언어(භාෂාව,되돌림서버항목,결과자료);වලංගුකරණය_වාර්තාව['languages'].append(භාෂාව)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(ප්_රවර්ගය_අගය,දත්ත.encode()) for ප්_රවර්ගය_අගය,දත්ත in 예상결과],되돌림서버항목.수신됨
            වලංගුකරණය_වාර්තාව['host_network_payloads']=[{'protocol':ප්_රවර්ගය_අගය,'text':දත්ත.decode()} for ප්_රවර්ගය_අගය,දත්ත in 되돌림서버항목.수신됨]
        වලංගුකරණය_වාර්තාව.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(결과자료/'report.json').write_text(json.dumps(වලංගුකරණය_වාර්තාව,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':ක්_රියාත්මක_කරන්න_2()
