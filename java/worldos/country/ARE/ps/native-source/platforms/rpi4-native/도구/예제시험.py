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
from سرپاڼه_ليد import 정확한값
from 예제되돌림서버 import 되돌림서버
from 실행 import 기준


def test_언어(کمپیوټر_ژبه,되돌림서버항목,결과자료):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    بهير=subprocess.Popen(['python3',str(기준/'도구/실행.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비선택기=selectors.DefaultSelector();준비선택기.register(بهير.stdout,selectors.EVENT_READ)
    대화기록=bytearray();پېرن=None;دوتنه_لېږدول_پيوستون=None
    def 수신하기(확인표시,ځغلول=0):
        끝위치=time.monotonic()+60
        while 확인표시 not in 대화기록[ځغلول:]:
            if time.monotonic()>끝위치 or بهير.poll() is not None:raise AssertionError(대화기록[ځغلول:].decode('utf-8','replace'))
            for 누름값,_ in 준비선택기.select(.1):
                اومتوک=누름값.fileobj.read(65536)
                if اومتوک:대화기록.extend(اومتوک)
        return 대화기록[ځغلول:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(심볼,누르는중=True):پېرن.sendall(struct.pack('>BBHI',4,int(누르는중),0,심볼))
    def 시작위치(ليکه):
        ځغلول=len(대화기록)
        for 문자값 in ليکه+'\n':
            심볼=0xff0d if 문자값=='\n' else ord(문자값) if ord(문자값)<256 else 0x1000000|ord(문자값)
            누름값(심볼);누름값(심볼,False)
        return ځغلول
    def سیپۍ(ليکه):return 수신하기(b'jkoros-native> ',시작위치(ليکه))
    def 실행(ليکه,예상결과):
        ليکنه=سیپۍ(ليکه);assert 예상결과 in ليکنه and 'exit 0' in ليکنه,(ليکه,ليکنه)
        return ليکنه
    def 화소들():
        پېرن.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            ټولۍ_ارزښت=정확한값(پېرن,1)[0]
            if ټولۍ_ارزښت==2:continue
            if ټولۍ_ارزښت==3:
                개수=struct.unpack('>I',정확한값(پېرن,7)[3:])[0];정확한값(پېرن,개수);continue
            assert ټولۍ_ارزښت==0,ټولۍ_ارزښت
            항목수=struct.unpack('>H',정확한값(پېرن,3)[1:])[0]
            for _ in range(항목수):
                가로좌표,세로좌표,너비값,높이값,لوښه_غونډ=struct.unpack('>HHHHi',정확한값(پېرن,12));assert لوښه_غونډ==0,لوښه_غونډ
                اومتوک=정확한값(پېرن,너비값*높이값*4)
                for 행위치 in range(높이값):
                    for 열위치 in range(너비값):
                        원본자료=(행위치*너비값+열위치)*4;대상=((세로좌표+행위치)*640+가로좌표+열위치)*3
                        빛삼원색[대상:대상+3]=bytes((اومتوک[원본자료+2],اومتوک[원본자료+1],اومتوک[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        پېرن=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert 정확한값(پېرن,12)==b'RFB 003.008\n';پېرن.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(پېرن,정확한값(پېرن,1)[0]);پېرن.sendall(b'\x01');assert 정확한값(پېرن,4)==b'\0'*4
        پېرن.sendall(b'\x01');초기값=정확한값(پېرن,24);정확한값(پېرن,struct.unpack('>I',초기값[20:])[0])
        پېرن.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        پېرن.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in سیپۍ('ftpd start')
        دوتنه_لېږدول_پيوستون=ftplib.FTP();دوتنه_لېږدول_پيوستون.encoding='utf-8';دوتنه_لېږدول_پيوستون.connect('127.0.0.1',파일전송접속번호,timeout=20);دوتنه_لېږدول_پيوستون.login()
        내용자료=('GUI와 FTP 동시 사용 '+کمپیوټر_ژبه+' 😀\n').encode()
        دوتنه_لېږدول_پيوستون.storbinary('STOR 함께.txt',io.BytesIO(내용자료))
        assert 내용자료.decode().strip() in سیپۍ('cat /함께.txt')
        받은수=bytearray();دوتنه_لېږدول_پيوستون.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==내용자료;دوتنه_لېږدول_پيوستون.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        목록보내기=سیپۍ('ls /example')
        assert all(نوم in 목록보내기 for نوم in ('java/','c/','python/','README.md')),목록보내기
        if کمپیوټر_ژبه=='java':
            꾸러미명세=json.loads((기준/'build/examples/manifest.json').read_text())
            for يونلور,ننوت_ټکى in 꾸러미명세.items():
                سیپۍ('cp '+يونلور+' /example-check.bin')
                منځپانګه_ارزښت=bytearray();دوتنه_لېږدول_پيوستون.retrbinary('RETR example-check.bin',منځپانګه_ارزښت.extend)
                assert len(منځپانګه_ارزښت)==ننوت_ټکى['bytes'] and hashlib.sha256(منځپانګه_ارزښت).hexdigest()==ننوت_ټکى['sha256'],يونلور
            دوتنه_لېږدول_پيوستون.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            دويال=bytes(range(256))*64
            دوتنه_لېږدول_پيوستون.storbinary('STOR boundary.bin',io.BytesIO(دويال))
            منځپانګه_ارزښت=bytearray();دوتنه_لېږدول_پيوستون.retrbinary('RETR boundary.bin',منځپانګه_ارزښت.extend)
            assert منځپانګه_ارزښت==دويال and 'boundary.bin' in دوتنه_لېږدول_پيوستون.nlst()
            سیپۍ('cp /boundary.bin /boundary-copy.bin')
            منځپانګه_ارزښت=bytearray();دوتنه_لېږدول_پيوستون.retrbinary('RETR boundary-copy.bin',منځپانګه_ارزښت.extend)
            assert منځپانګه_ارزښت==دويال
            دوتنه_لېږدول_پيوستون.delete('boundary.bin');دوتنه_لېږدول_پيوستون.delete('boundary-copy.bin')
        assert '출력예제' in سیپۍ('ls /example/'+کمپیوټر_ژبه)
        سیپۍ('cd /example/'+کمپیوټر_ژبه)
        이름표={'java':'JAVA','c':'C','python':'PYTHON'}[کمپیوټر_ژبه]
        예상파일=이름표+' دوتنه: 한글 اومتوک 😀\n'
        if کمپیوټر_ژبه=='java':
            실행('javac 출력예제.java','Compiled:');실행('java 출력예제','JAVA 출력: 안녕하세요 😀')
            실행('javac 파일예제.java','Compiled:');실행('java 파일예제',예상파일)
            실행('java 네트워크예제 {} {}'.format(되돌림서버항목.لېږد_مهارې_باندره_درشل,되돌림서버항목.전문접속번호),'JAVA 네트워크 확인: TCP UDP 한글')
            그림명령='java 그래픽예제'
        elif کمپیوټر_ژبه=='c':
            for نوم,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('دوتنه','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 확인: UDP 한글')]:
                실행('cc '+نوم+'예제.c -o 실행','Compiled native ARM64 ELF:')
                실행('./실행'+전달값,예상결과)
            실행('cc 그래픽예제.c -o 실행','Compiled native ARM64 ELF:');그림명령='./실행'
        else:
            for نوم,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('دوتنه','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 확인: UDP 한글')]:
                실행('python '+نوم+'예제.py'+전달값,예상결과)
            그림명령='python 그래픽예제.py'
        그림시작=시작위치(그림명령)
        ليکنه=수신하기('그림을 확인한 뒤 Enter를 누르세요.\r\n'.encode(),그림시작)
        assert 이름표+' 그래픽: 빨강 초록 파랑' in ليکنه and 'exit 0' not in ليکنه,ليکنه
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        دوتنه_لېږدول_پيوستون.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();دوتنه_لېږدول_پيوستون.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';دوتنه_لېږدول_پيوستون.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            변위=(세로좌표*640+610)*3;assert tuple(빛삼원색[변위:변위+3])==색상,(کمپیوټر_ژبه,세로좌표,tuple(빛삼원색[변위:변위+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(결과자료/(کمپیوټر_ژبه+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',그림시작)
        if کمپیوټر_ژبه=='java':
            پيل_کړکۍ=시작위치('java 창예제')
            수신하기('GUI 예제 준비: 창예제'.encode(),پيل_کړکۍ)
            def ټک_ارزښت(가로,세로):
                for تڼۍ in (1,0):پېرن.sendall(struct.pack('>BBHH',5,تڼۍ,가로,세로))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            ټک_ارزښت(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for لوښه_ارزښت in '한글':누름값(0x1000000|ord(لوښه_ارزښت));누름값(0x1000000|ord(لوښه_ارزښت),False)
            for 횟수 in (1,2):
                ځغلول=len(대화기록);ټک_ارزښت(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),ځغلول)
            time.sleep(.3)
            창그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=창그림.crop((110,272,530,300)).tobytes()
            창그림.save(str(결과자료/'java-swing.png'))
            ځغلول=len(대화기록);ټک_ارزښت(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',ځغلول)
        # Download the guest-created bytes through FTP in the same GUI VM.
        파일이름={'java':'java.txt','c':'c.txt','python':'python.txt'}[کمپیوټر_ژبه]
        سیپۍ('cp '+파일이름+' /검증.txt')
        받은수=bytearray();دوتنه_لېږدول_پيوستون.retrbinary('RETR 검증.txt',받은수.extend);assert 받은수==예상파일.encode()
        سیپۍ('echo preserved > 출력예제.'+('py' if کمپیوټر_ژبه=='python' else کمپیوټر_ژبه))
        assert 'EXAMPLES READY' in سیپۍ('example '+کمپیوټر_ژبه)
        assert '\npreserved\n' in سیپۍ('cat 출력예제.'+('py' if کمپیوټر_ژبه=='python' else کمپیوټر_ژبه))
        assert '한/영 کيلي_ارزښت, Shift+Space 또는 F9' in سیپۍ('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in سیپۍ('echo GUI NETWORK TOGETHER')
        دوتنه_لېږدول_پيوستون.quit();دوتنه_لېږدول_پيوستون=None;assert 'FTP stopped' in سیپۍ('ftpd stop')
        print('PASS '+کمپیوټر_ژبه+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if دوتنه_لېږدول_پيوستون:
            try:دوتنه_لېږدول_پيوستون.close()
            except OSError:pass
        if پېرن:پېرن.close()
        بهير.terminate()
        try:بهير.wait(timeout=8)
        except subprocess.TimeoutExpired:بهير.kill();بهير.wait()
        준비선택기.close();بهير.stdout.close();(결과자료/(کمپیوټر_ژبه+'-serial.log')).write_bytes(대화기록)


def ځغلول():
    결과자료=기준/'build/verification/examples';결과자료.mkdir(parents=True,exist_ok=True)
    باورکړن_راپور={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for کمپیوټر_ژبه in ('java','c','python'):
                test_언어(کمپیوټر_ژبه,되돌림서버항목,결과자료);باورکړن_راپور['languages'].append(کمپیوټر_ژبه)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(ټولۍ_ارزښت,اومتوک.encode()) for ټولۍ_ارزښت,اومتوک in 예상결과],되돌림서버항목.수신됨
            باورکړن_راپور['host_network_payloads']=[{'protocol':ټولۍ_ارزښت,'text':اومتوک.decode()} for ټولۍ_ارزښت,اومتوک in 되돌림서버항목.수신됨]
        باورکړن_راپور.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(결과자료/'report.json').write_text(json.dumps(باورکړن_راپور,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':ځغلول()
