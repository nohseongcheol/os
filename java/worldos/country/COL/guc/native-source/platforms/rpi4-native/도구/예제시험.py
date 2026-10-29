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
from a_yataainpalaa_e_rajaa import 정확한값
from 예제되돌림서버 import 되돌림서버
from 실행 import 기준


def test_언어(anüikii_komputatooralujatü,되돌림서버항목,결과자료):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    실행과정=subprocess.Popen(['python3',str(기준/'도구/실행.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비선택기=selectors.DefaultSelector();준비선택기.register(실행과정.stdout,selectors.EVENT_READ)
    대화기록=bytearray();matchanta=None;anaajaalaa_alate_eraa_epe_ipajia=None
    def 수신하기(확인표시,시작=0):
        끝위치=time.monotonic()+60
        while 확인표시 not in 대화기록[시작:]:
            if time.monotonic()>끝위치 or 실행과정.poll() is not None:raise AssertionError(대화기록[시작:].decode('utf-8','replace'))
            for 누름값,_ in 준비선택기.select(.1):
                atijaaya=누름값.fileobj.read(65536)
                if atijaaya:대화기록.extend(atijaaya)
        return 대화기록[시작:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(심볼,누르는중=True):matchanta.sendall(struct.pack('>BBHI',4,int(누르는중),0,심볼))
    def 시작위치(liinia):
        시작=len(대화기록)
        for 문자값 in liinia+'\n':
            심볼=0xff0d if 문자값=='\n' else ord(문자값) if ord(문자값)<256 else 0x1000000|ord(문자값)
            누름값(심볼);누름값(심볼,False)
        return 시작
    def aluwataalapu_u(liinia):return 수신하기(b'jkoros-native> ',시작위치(liinia))
    def 실행(liinia,예상결과):
        글=aluwataalapu_u(liinia);assert 예상결과 in 글 and 'exit 0' in 글,(liinia,글)
        return 글
    def 화소들():
        matchanta.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            akotchiraayanüliee_ajutuu=정확한값(matchanta,1)[0]
            if akotchiraayanüliee_ajutuu==2:continue
            if akotchiraayanüliee_ajutuu==3:
                개수=struct.unpack('>I',정확한값(matchanta,7)[3:])[0];정확한값(matchanta,개수);continue
            assert akotchiraayanüliee_ajutuu==0,akotchiraayanüliee_ajutuu
            항목수=struct.unpack('>H',정확한값(matchanta,3)[1:])[0]
            for _ in range(항목수):
                가로좌표,세로좌표,너비값,높이값,jeetkotchiraaya=struct.unpack('>HHHHi',정확한값(matchanta,12));assert jeetkotchiraaya==0,jeetkotchiraaya
                atijaaya=정확한값(matchanta,너비값*높이값*4)
                for 행위치 in range(높이값):
                    for 열위치 in range(너비값):
                        원본자료=(행위치*너비값+열위치)*4;대상=((세로좌표+행위치)*640+가로좌표+열위치)*3
                        빛삼원색[대상:대상+3]=bytes((atijaaya[원본자료+2],atijaaya[원본자료+1],atijaaya[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        matchanta=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert 정확한값(matchanta,12)==b'RFB 003.008\n';matchanta.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(matchanta,정확한값(matchanta,1)[0]);matchanta.sendall(b'\x01');assert 정확한값(matchanta,4)==b'\0'*4
        matchanta.sendall(b'\x01');초기값=정확한값(matchanta,24);정확한값(matchanta,struct.unpack('>I',초기값[20:])[0])
        matchanta.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        matchanta.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in aluwataalapu_u('ftpd start')
        anaajaalaa_alate_eraa_epe_ipajia=ftplib.FTP();anaajaalaa_alate_eraa_epe_ipajia.encoding='utf-8';anaajaalaa_alate_eraa_epe_ipajia.connect('127.0.0.1',파일전송접속번호,timeout=20);anaajaalaa_alate_eraa_epe_ipajia.login()
        내용자료=('GUI와 FTP 동시 사용 '+anüikii_komputatooralujatü+' 😀\n').encode()
        anaajaalaa_alate_eraa_epe_ipajia.storbinary('STOR 함께.txt',io.BytesIO(내용자료))
        assert 내용자료.decode().strip() in aluwataalapu_u('cat /함께.txt')
        받은수=bytearray();anaajaalaa_alate_eraa_epe_ipajia.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==내용자료;anaajaalaa_alate_eraa_epe_ipajia.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        목록보내기=aluwataalapu_u('ls /example')
        assert all(이름 in 목록보내기 for 이름 in ('java/','c/','python/','README.md')),목록보내기
        if anüikii_komputatooralujatü=='java':
            꾸러미명세=json.loads((기준/'build/examples/manifest.json').read_text())
            for wopu_a_ttaaleemüin,ekeroliaa_o_uchikanain in 꾸러미명세.items():
                aluwataalapu_u('cp '+wopu_a_ttaaleemüin+' /example-check.bin')
                alu_ujatüü_ajutuu=bytearray();anaajaalaa_alate_eraa_epe_ipajia.retrbinary('RETR example-check.bin',alu_ujatüü_ajutuu.extend)
                assert len(alu_ujatüü_ajutuu)==ekeroliaa_o_uchikanain['bytes'] and hashlib.sha256(alu_ujatüü_ajutuu).hexdigest()==ekeroliaa_o_uchikanain['sha256'],wopu_a_ttaaleemüin
            anaajaalaa_alate_eraa_epe_ipajia.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            tijitaalü=bytes(range(256))*64
            anaajaalaa_alate_eraa_epe_ipajia.storbinary('STOR boundary.bin',io.BytesIO(tijitaalü))
            alu_ujatüü_ajutuu=bytearray();anaajaalaa_alate_eraa_epe_ipajia.retrbinary('RETR boundary.bin',alu_ujatüü_ajutuu.extend)
            assert alu_ujatüü_ajutuu==tijitaalü and 'boundary.bin' in anaajaalaa_alate_eraa_epe_ipajia.nlst()
            aluwataalapu_u('cp /boundary.bin /boundary-copy.bin')
            alu_ujatüü_ajutuu=bytearray();anaajaalaa_alate_eraa_epe_ipajia.retrbinary('RETR boundary-copy.bin',alu_ujatüü_ajutuu.extend)
            assert alu_ujatüü_ajutuu==tijitaalü
            anaajaalaa_alate_eraa_epe_ipajia.delete('boundary.bin');anaajaalaa_alate_eraa_epe_ipajia.delete('boundary-copy.bin')
        assert '출력예제' in aluwataalapu_u('ls /example/'+anüikii_komputatooralujatü)
        aluwataalapu_u('cd /example/'+anüikii_komputatooralujatü)
        이름표={'java':'JAVA','c':'C','python':'PYTHON'}[anüikii_komputatooralujatü]
        예상파일=이름표+' anaajaalaa: 한글 atijaaya 😀\n'
        if anüikii_komputatooralujatü=='java':
            실행('javac 출력예제.java','Compiled:');실행('java 출력예제','JAVA 출력: 안녕하세요 😀')
            실행('javac 파일예제.java','Compiled:');실행('java 파일예제',예상파일)
            실행('java 네트워크예제 {} {}'.format(되돌림서버항목.Pürotokoola_Aa_inmajia_Alatiriaa_outtülee,되돌림서버항목.전문접속번호),'JAVA 네트워크 확인: TCP UDP 한글')
            그림명령='java 그래픽예제'
        elif anüikii_komputatooralujatü=='c':
            for 이름,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('anaajaalaa','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 확인: UDP 한글')]:
                실행('cc '+이름+'예제.c -o 실행','Compiled native ARM64 ELF:')
                실행('./실행'+전달값,예상결과)
            실행('cc 그래픽예제.c -o 실행','Compiled native ARM64 ELF:');그림명령='./실행'
        else:
            for 이름,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('anaajaalaa','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 확인: UDP 한글')]:
                실행('python '+이름+'예제.py'+전달값,예상결과)
            그림명령='python 그래픽예제.py'
        그림시작=시작위치(그림명령)
        글=수신하기('그림을 확인한 뒤 Enter를 누르세요.\r\n'.encode(),그림시작)
        assert 이름표+' 그래픽: 빨강 초록 파랑' in 글 and 'exit 0' not in 글,글
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        anaajaalaa_alate_eraa_epe_ipajia.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();anaajaalaa_alate_eraa_epe_ipajia.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';anaajaalaa_alate_eraa_epe_ipajia.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            변위=(세로좌표*640+610)*3;assert tuple(빛삼원색[변위:변위+3])==색상,(anüikii_komputatooralujatü,세로좌표,tuple(빛삼원색[변위:변위+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(결과자료/(anüikii_komputatooralujatü+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',그림시작)
        if anüikii_komputatooralujatü=='java':
            achuwalaa_analaaya=시작위치('java 창예제')
            수신하기('GUI 예제 준비: 창예제'.encode(),achuwalaa_analaaya)
            def aküliküjaa_ajutuu(가로,세로):
                for ajüttülee in (1,0):matchanta.sendall(struct.pack('>BBHH',5,ajüttülee,가로,세로))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            aküliküjaa_ajutuu(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for jeerü_ajutuu in '한글':누름값(0x1000000|ord(jeerü_ajutuu));누름값(0x1000000|ord(jeerü_ajutuu),False)
            for 횟수 in (1,2):
                시작=len(대화기록);aküliküjaa_ajutuu(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),시작)
            time.sleep(.3)
            창그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=창그림.crop((110,272,530,300)).tobytes()
            창그림.save(str(결과자료/'java-swing.png'))
            시작=len(대화기록);aküliküjaa_ajutuu(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',시작)
        # Download the guest-created bytes through FTP in the same GUI VM.
        파일이름={'java':'java.txt','c':'c.txt','python':'python.txt'}[anüikii_komputatooralujatü]
        aluwataalapu_u('cp '+파일이름+' /검증.txt')
        받은수=bytearray();anaajaalaa_alate_eraa_epe_ipajia.retrbinary('RETR 검증.txt',받은수.extend);assert 받은수==예상파일.encode()
        aluwataalapu_u('echo preserved > 출력예제.'+('py' if anüikii_komputatooralujatü=='python' else anüikii_komputatooralujatü))
        assert 'EXAMPLES READY' in aluwataalapu_u('example '+anüikii_komputatooralujatü)
        assert '\npreserved\n' in aluwataalapu_u('cat 출력예제.'+('py' if anüikii_komputatooralujatü=='python' else anüikii_komputatooralujatü))
        assert '한/영 ajüttia_ajutuu, Shift+Space 또는 F9' in aluwataalapu_u('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in aluwataalapu_u('echo GUI NETWORK TOGETHER')
        anaajaalaa_alate_eraa_epe_ipajia.quit();anaajaalaa_alate_eraa_epe_ipajia=None;assert 'FTP stopped' in aluwataalapu_u('ftpd stop')
        print('PASS '+anüikii_komputatooralujatü+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if anaajaalaa_alate_eraa_epe_ipajia:
            try:anaajaalaa_alate_eraa_epe_ipajia.close()
            except OSError:pass
        if matchanta:matchanta.close()
        실행과정.terminate()
        try:실행과정.wait(timeout=8)
        except subprocess.TimeoutExpired:실행과정.kill();실행과정.wait()
        준비선택기.close();실행과정.stdout.close();(결과자료/(anüikii_komputatooralujatü+'-serial.log')).write_bytes(대화기록)


def 시작():
    결과자료=기준/'build/verification/examples';결과자료.mkdir(parents=True,exist_ok=True)
    anaajiaakua_ipa_achikiimaajatü={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for anüikii_komputatooralujatü in ('java','c','python'):
                test_언어(anüikii_komputatooralujatü,되돌림서버항목,결과자료);anaajiaakua_ipa_achikiimaajatü['languages'].append(anüikii_komputatooralujatü)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(akotchiraayanüliee_ajutuu,atijaaya.encode()) for akotchiraayanüliee_ajutuu,atijaaya in 예상결과],되돌림서버항목.수신됨
            anaajiaakua_ipa_achikiimaajatü['host_network_payloads']=[{'protocol':akotchiraayanüliee_ajutuu,'text':atijaaya.decode()} for akotchiraayanüliee_ajutuu,atijaaya in 되돌림서버항목.수신됨]
        anaajiaakua_ipa_achikiimaajatü.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(결과자료/'report.json').write_text(json.dumps(anaajiaakua_ipa_achikiimaajatü,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':시작()
