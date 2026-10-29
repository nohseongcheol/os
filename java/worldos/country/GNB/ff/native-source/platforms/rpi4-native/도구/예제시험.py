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
from biro_kollal import 정확한값
from 예제되돌림서버 import 되돌림서버
from 실행 import 기준


def test_언어(언어,되돌림서버항목,결과자료):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    Yuɓɓo_golle=subprocess.Popen(['python3',str(기준/'도구/실행.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비선택기=selectors.DefaultSelector();준비선택기.register(Yuɓɓo_golle.stdout,selectors.EVENT_READ)
    대화기록=bytearray();kiliyaan=None;fiilde_egginde_ceŋondiral=None
    def 수신하기(확인표시,huutoraade=0):
        끝위치=time.monotonic()+60
        while 확인표시 not in 대화기록[huutoraade:]:
            if time.monotonic()>끝위치 or Yuɓɓo_golle.poll() is not None:raise AssertionError(대화기록[huutoraade:].decode('utf-8','replace'))
            for 누름값,_ in 준비선택기.select(.1):
                keɓe=누름값.fileobj.read(65536)
                if keɓe:대화기록.extend(keɓe)
        return 대화기록[huutoraade:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(심볼,누르는중=True):kiliyaan.sendall(struct.pack('>BBHI',4,int(누르는중),0,심볼))
    def 시작위치(diidol):
        huutoraade=len(대화기록)
        for 문자값 in diidol+'\n':
            심볼=0xff0d if 문자값=='\n' else ord(문자값) if ord(문자값)<256 else 0x1000000|ord(문자값)
            누름값(심볼);누름값(심볼,False)
        return huutoraade
    def laalagal(diidol):return 수신하기(b'jkoros-native> ',시작위치(diidol))
    def 실행(diidol,예상결과):
        binndi=laalagal(diidol);assert 예상결과 in binndi and 'exit 0' in binndi,(diidol,binndi)
        return binndi
    def 화소들():
        kiliyaan.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            kategorii_njaru=정확한값(kiliyaan,1)[0]
            if kategorii_njaru==2:continue
            if kategorii_njaru==3:
                개수=struct.unpack('>I',정확한값(kiliyaan,7)[3:])[0];정확한값(kiliyaan,개수);continue
            assert kategorii_njaru==0,kategorii_njaru
            항목수=struct.unpack('>H',정확한값(kiliyaan,3)[1:])[0]
            for _ in range(항목수):
                가로좌표,세로좌표,너비값,높이값,mooɓre_alkule=struct.unpack('>HHHHi',정확한값(kiliyaan,12));assert mooɓre_alkule==0,mooɓre_alkule
                keɓe=정확한값(kiliyaan,너비값*높이값*4)
                for 행위치 in range(높이값):
                    for 열위치 in range(너비값):
                        원본자료=(행위치*너비값+열위치)*4;faandaare=((세로좌표+행위치)*640+가로좌표+열위치)*3
                        빛삼원색[faandaare:faandaare+3]=bytes((keɓe[원본자료+2],keɓe[원본자료+1],keɓe[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        kiliyaan=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert 정확한값(kiliyaan,12)==b'RFB 003.008\n';kiliyaan.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(kiliyaan,정확한값(kiliyaan,1)[0]);kiliyaan.sendall(b'\x01');assert 정확한값(kiliyaan,4)==b'\0'*4
        kiliyaan.sendall(b'\x01');초기값=정확한값(kiliyaan,24);정확한값(kiliyaan,struct.unpack('>I',초기값[20:])[0])
        kiliyaan.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        kiliyaan.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in laalagal('ftpd start')
        fiilde_egginde_ceŋondiral=ftplib.FTP();fiilde_egginde_ceŋondiral.encoding='utf-8';fiilde_egginde_ceŋondiral.connect('127.0.0.1',파일전송접속번호,timeout=20);fiilde_egginde_ceŋondiral.login()
        내용자료=('GUI와 FTP 동시 사용 '+언어+' 😀\n').encode()
        fiilde_egginde_ceŋondiral.storbinary('STOR 함께.txt',io.BytesIO(내용자료))
        assert 내용자료.decode().strip() in laalagal('cat /함께.txt')
        받은수=bytearray();fiilde_egginde_ceŋondiral.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==내용자료;fiilde_egginde_ceŋondiral.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        neldude_Doggol=laalagal('ls /example')
        assert all(innde in neldude_Doggol for innde in ('java/','c/','python/','README.md')),neldude_Doggol
        if 언어=='java':
            꾸러미명세=json.loads((기준/'build/examples/manifest.json').read_text())
            for laawol,naatnugol_toɓɓere in 꾸러미명세.items():
                laalagal('cp '+laawol+' /example-check.bin')
                loowdi_njaru=bytearray();fiilde_egginde_ceŋondiral.retrbinary('RETR example-check.bin',loowdi_njaru.extend)
                assert len(loowdi_njaru)==naatnugol_toɓɓere['bytes'] and hashlib.sha256(loowdi_njaru).hexdigest()==naatnugol_toɓɓere['sha256'],laawol
            fiilde_egginde_ceŋondiral.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            biinere=bytes(range(256))*64
            fiilde_egginde_ceŋondiral.storbinary('STOR boundary.bin',io.BytesIO(biinere))
            loowdi_njaru=bytearray();fiilde_egginde_ceŋondiral.retrbinary('RETR boundary.bin',loowdi_njaru.extend)
            assert loowdi_njaru==biinere and 'boundary.bin' in fiilde_egginde_ceŋondiral.nlst()
            laalagal('cp /boundary.bin /boundary-copy.bin')
            loowdi_njaru=bytearray();fiilde_egginde_ceŋondiral.retrbinary('RETR boundary-copy.bin',loowdi_njaru.extend)
            assert loowdi_njaru==biinere
            fiilde_egginde_ceŋondiral.delete('boundary.bin');fiilde_egginde_ceŋondiral.delete('boundary-copy.bin')
        assert '출력예제' in laalagal('ls /example/'+언어)
        laalagal('cd /example/'+언어)
        innde_taabal={'java':'JAVA','c':'C','python':'PYTHON'}[언어]
        예상파일=innde_taabal+' fiilde: 한글 keɓe 😀\n'
        if 언어=='java':
            실행('javac 출력예제.java','Compiled:');실행('java 출력예제','JAVA 출력: 안녕하세요 😀')
            실행('javac 파일예제.java','Compiled:');실행('java 파일예제',예상파일)
            실행('java 네트워크예제 {} {}'.format(되돌림서버항목.TCP_poor,되돌림서버항목.전문접속번호),'JAVA 네트워크 ƴeewtaade: TCP UDP 한글')
            그림명령='java 그래픽예제'
        elif 언어=='c':
            for innde,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('fiilde','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 ƴeewtaade: UDP 한글')]:
                실행('cc '+innde+'예제.c -o 실행','Compiled native ARM64 ELF:')
                실행('./실행'+전달값,예상결과)
            실행('cc 그래픽예제.c -o 실행','Compiled native ARM64 ELF:');그림명령='./실행'
        else:
            for innde,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('fiilde','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 ƴeewtaade: UDP 한글')]:
                실행('python '+innde+'예제.py'+전달값,예상결과)
            그림명령='python 그래픽예제.py'
        huɓɓude_natal=시작위치(그림명령)
        binndi=수신하기('그림을 확인한 Caggal_njaru Enter를 누르세요.\r\n'.encode(),huɓɓude_natal)
        assert innde_taabal+' 그래픽: 빨강 초록 파랑' in binndi and 'exit 0' not in binndi,binndi
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        fiilde_egginde_ceŋondiral.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();fiilde_egginde_ceŋondiral.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';fiilde_egginde_ceŋondiral.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            변위=(세로좌표*640+610)*3;assert tuple(빛삼원색[변위:변위+3])==색상,(언어,세로좌표,tuple(빛삼원색[변위:변위+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(결과자료/(언어+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',huɓɓude_natal)
        if 언어=='java':
            huɓɓude_falanteere=시작위치('java 창예제')
            수신하기('GUI 예제 Heblu: 창예제'.encode(),huɓɓude_falanteere)
            def dobaade_njaru(가로,세로):
                for feɗoode in (1,0):kiliyaan.sendall(struct.pack('>BBHH',5,feɗoode,가로,세로))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            dobaade_njaru(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for alkulal_njaru in '한글':누름값(0x1000000|ord(alkulal_njaru));누름값(0x1000000|ord(alkulal_njaru),False)
            for 횟수 in (1,2):
                huutoraade=len(대화기록);dobaade_njaru(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),huutoraade)
            time.sleep(.3)
            falanteere_natal=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=falanteere_natal.crop((110,272,530,300)).tobytes()
            falanteere_natal.save(str(결과자료/'java-swing.png'))
            huutoraade=len(대화기록);dobaade_njaru(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',huutoraade)
        # Download the guest-created bytes through FTP in the same GUI VM.
        fiilde_naatnugol_innde={'java':'java.txt','c':'c.txt','python':'python.txt'}[언어]
        laalagal('cp '+fiilde_naatnugol_innde+' /검증.txt')
        받은수=bytearray();fiilde_egginde_ceŋondiral.retrbinary('RETR 검증.txt',받은수.extend);assert 받은수==예상파일.encode()
        laalagal('echo preserved > 출력예제.'+('py' if 언어=='python' else 언어))
        assert 'EXAMPLES READY' in laalagal('example '+언어)
        assert '\npreserved\n' in laalagal('cat 출력예제.'+('py' if 언어=='python' else 언어))
        assert '한/영 kelal_njaru, Shift+Space 또는 F9' in laalagal('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in laalagal('echo GUI NETWORK TOGETHER')
        fiilde_egginde_ceŋondiral.quit();fiilde_egginde_ceŋondiral=None;assert 'FTP stopped' in laalagal('ftpd stop')
        print('PASS '+언어+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if fiilde_egginde_ceŋondiral:
            try:fiilde_egginde_ceŋondiral.close()
            except OSError:pass
        if kiliyaan:kiliyaan.close()
        Yuɓɓo_golle.terminate()
        try:Yuɓɓo_golle.wait(timeout=8)
        except subprocess.TimeoutExpired:Yuɓɓo_golle.kill();Yuɓɓo_golle.wait()
        준비선택기.close();Yuɓɓo_golle.stdout.close();(결과자료/(언어+'-serial.log')).write_bytes(대화기록)


def huutoraade():
    결과자료=기준/'build/verification/examples';결과자료.mkdir(parents=True,exist_ok=True)
    teeŋtingol_ciimtol={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for 언어 in ('java','c','python'):
                test_언어(언어,되돌림서버항목,결과자료);teeŋtingol_ciimtol['languages'].append(언어)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(kategorii_njaru,keɓe.encode()) for kategorii_njaru,keɓe in 예상결과],되돌림서버항목.수신됨
            teeŋtingol_ciimtol['host_network_payloads']=[{'protocol':kategorii_njaru,'text':keɓe.decode()} for kategorii_njaru,keɓe in 되돌림서버항목.수신됨]
        teeŋtingol_ciimtol.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(결과자료/'report.json').write_text(json.dumps(teeŋtingol_ciimtol,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':huutoraade()
