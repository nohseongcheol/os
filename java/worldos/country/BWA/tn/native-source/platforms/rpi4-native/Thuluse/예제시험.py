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
from desekethopo_Tebego import 정확한값
from 예제되돌림서버 import 되돌림서버
from diragatsa_Taelo import 기준


def test_언어(Puo,되돌림서버항목,결과자료):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    Thulaganyo=subprocess.Popen(['python3',str(기준/'Thuluse/diragatsa_Taelo.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    setlhophi=selectors.DefaultSelector();setlhophi.register(Thulaganyo.stdout,selectors.EVENT_READ)
    대화기록=bytearray();sedirelwa=None;faele_fudusa_Kgolagano=None
    def 수신하기(확인표시,dirisa=0):
        kgaola_Baya_ka_Tekatekanyo=time.monotonic()+60
        while 확인표시 not in 대화기록[dirisa:]:
            if time.monotonic()>kgaola_Baya_ka_Tekatekanyo or Thulaganyo.poll() is not None:raise AssertionError(대화기록[dirisa:].decode('utf-8','replace'))
            for 누름값,_ in setlhophi.select(.1):
                tshedimosetso=누름값.fileobj.read(65536)
                if tshedimosetso:대화기록.extend(tshedimosetso)
        return 대화기록[dirisa:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(letshwao_Boleng,누르는중=True):sedirelwa.sendall(struct.pack('>BBHI',4,int(누르는중),0,letshwao_Boleng))
    def simolola_Baya_ka_Tekatekanyo(Mola):
        dirisa=len(대화기록)
        for khoutuletshwao in Mola+'\n':
            letshwao_Boleng=0xff0d if khoutuletshwao=='\n' else ord(khoutuletshwao) if ord(khoutuletshwao)<256 else 0x1000000|ord(khoutuletshwao)
            누름값(letshwao_Boleng);누름값(letshwao_Boleng,False)
        return dirisa
    def setlhalosataelo(Mola):return 수신하기(b'jkoros-native> ',simolola_Baya_ka_Tekatekanyo(Mola))
    def diragatsa_Taelo(Mola,예상결과):
        SMS=setlhalosataelo(Mola);assert 예상결과 in SMS and 'exit 0' in SMS,(Mola,SMS)
        return SMS
    def 화소들():
        sedirelwa.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            setlhopha_Boleng_4b6d6445=정확한값(sedirelwa,1)[0]
            if setlhopha_Boleng_4b6d6445==2:continue
            if setlhopha_Boleng_4b6d6445==3:
                개수=struct.unpack('>I',정확한값(sedirelwa,7)[3:])[0];정확한값(sedirelwa,개수);continue
            assert setlhopha_Boleng_4b6d6445==0,setlhopha_Boleng_4b6d6445
            항목수=struct.unpack('>H',정확한값(sedirelwa,3)[1:])[0]
            for _ in range(항목수):
                kgokagano_ya_x,세로좌표,너비값,높이값,Setlhophatshwao=struct.unpack('>HHHHi',정확한값(sedirelwa,12));assert Setlhophatshwao==0,Setlhophatshwao
                tshedimosetso=정확한값(sedirelwa,너비값*높이값*4)
                for 행위치 in range(높이값):
                    for 열위치 in range(너비값):
                        원본자료=(행위치*너비값+열위치)*4;setotwa=((세로좌표+행위치)*640+kgokagano_ya_x+열위치)*3
                        빛삼원색[setotwa:setotwa+3]=bytes((tshedimosetso[원본자료+2],tshedimosetso[원본자료+1],tshedimosetso[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        sedirelwa=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert 정확한값(sedirelwa,12)==b'RFB 003.008\n';sedirelwa.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(sedirelwa,정확한값(sedirelwa,1)[0]);sedirelwa.sendall(b'\x01');assert 정확한값(sedirelwa,4)==b'\0'*4
        sedirelwa.sendall(b'\x01');초기값=정확한값(sedirelwa,24);정확한값(sedirelwa,struct.unpack('>I',초기값[20:])[0])
        sedirelwa.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        sedirelwa.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in setlhalosataelo('ftpd start')
        faele_fudusa_Kgolagano=ftplib.FTP();faele_fudusa_Kgolagano.encoding='utf-8';faele_fudusa_Kgolagano.connect('127.0.0.1',파일전송접속번호,timeout=20);faele_fudusa_Kgolagano.login()
        selekanyo_sa_tshedimosetso_tshedimosetso=('GUI와 FTP 동시 사용 '+Puo+' 😀\n').encode()
        faele_fudusa_Kgolagano.storbinary('STOR 함께.txt',io.BytesIO(selekanyo_sa_tshedimosetso_tshedimosetso))
        assert selekanyo_sa_tshedimosetso_tshedimosetso.decode().strip() in setlhalosataelo('cat /함께.txt')
        받은수=bytearray();faele_fudusa_Kgolagano.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==selekanyo_sa_tshedimosetso_tshedimosetso;faele_fudusa_Kgolagano.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        romela_lenaane=setlhalosataelo('ls /example')
        assert all(leina in romela_lenaane for leina in ('java/','c/','python/','README.md')),romela_lenaane
        if Puo=='java':
            꾸러미명세=json.loads((기준/'build/examples/manifest.json').read_text())
            for tsela,tsenyo_ntlha in 꾸러미명세.items():
                setlhalosataelo('cp '+tsela+' /example-check.bin')
                Diteng_Boleng=bytearray();faele_fudusa_Kgolagano.retrbinary('RETR example-check.bin',Diteng_Boleng.extend)
                assert len(Diteng_Boleng)==tsenyo_ntlha['bytes'] and hashlib.sha256(Diteng_Boleng).hexdigest()==tsenyo_ntlha['sha256'],tsela
            faele_fudusa_Kgolagano.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            baenari=bytes(range(256))*64
            faele_fudusa_Kgolagano.storbinary('STOR boundary.bin',io.BytesIO(baenari))
            Diteng_Boleng=bytearray();faele_fudusa_Kgolagano.retrbinary('RETR boundary.bin',Diteng_Boleng.extend)
            assert Diteng_Boleng==baenari and 'boundary.bin' in faele_fudusa_Kgolagano.nlst()
            setlhalosataelo('cp /boundary.bin /boundary-copy.bin')
            Diteng_Boleng=bytearray();faele_fudusa_Kgolagano.retrbinary('RETR boundary-copy.bin',Diteng_Boleng.extend)
            assert Diteng_Boleng==baenari
            faele_fudusa_Kgolagano.delete('boundary.bin');faele_fudusa_Kgolagano.delete('boundary-copy.bin')
        assert '출력예제' in setlhalosataelo('ls /example/'+Puo)
        setlhalosataelo('cd /example/'+Puo)
        leina_lenaneothalo={'java':'JAVA','c':'C','python':'PYTHON'}[Puo]
        예상파일=leina_lenaneothalo+' faele: 한글 tshedimosetso 😀\n'
        if Puo=='java':
            diragatsa_Taelo('javac 출력예제.java','Compiled:');diragatsa_Taelo('java 출력예제','JAVA 출력: 안녕하세요 😀')
            diragatsa_Taelo('javac 파일예제.java','Compiled:');diragatsa_Taelo('java 파일예제',예상파일)
            diragatsa_Taelo('java 네트워크예제 {} {}'.format(되돌림서버항목.TCP_gorogisetsa,되돌림서버항목.전문접속번호),'JAVA 네트워크 netefatsa: TCP UDP 한글')
            그림명령='java 그래픽예제'
        elif Puo=='c':
            for leina,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('faele','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 netefatsa: UDP 한글')]:
                diragatsa_Taelo('cc '+leina+'예제.c -o diragatsa_Taelo','Compiled native ARM64 ELF:')
                diragatsa_Taelo('./diragatsa_Taelo'+전달값,예상결과)
            diragatsa_Taelo('cc 그래픽예제.c -o diragatsa_Taelo','Compiled native ARM64 ELF:');그림명령='./diragatsa_Taelo'
        else:
            for leina,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('faele','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 netefatsa: UDP 한글')]:
                diragatsa_Taelo('python '+leina+'예제.py'+전달값,예상결과)
            그림명령='python 그래픽예제.py'
        simolola_sethalo=simolola_Baya_ka_Tekatekanyo(그림명령)
        SMS=수신하기('그림을 확인한 Morago_Boleng Enter를 누르세요.\r\n'.encode(),simolola_sethalo)
        assert leina_lenaneothalo+' 그래픽: 빨강 초록 파랑' in SMS and 'exit 0' not in SMS,SMS
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        faele_fudusa_Kgolagano.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();faele_fudusa_Kgolagano.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';faele_fudusa_Kgolagano.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            Baya_ka_Tekatekanyo_Boleng=(세로좌표*640+610)*3;assert tuple(빛삼원색[Baya_ka_Tekatekanyo_Boleng:Baya_ka_Tekatekanyo_Boleng+3])==색상,(Puo,세로좌표,tuple(빛삼원색[Baya_ka_Tekatekanyo_Boleng:Baya_ka_Tekatekanyo_Boleng+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(결과자료/(Puo+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',simolola_sethalo)
        if Puo=='java':
            simolola_fensetere=simolola_Baya_ka_Tekatekanyo('java 창예제')
            수신하기('GUI 예제 Baakanya: 창예제'.encode(),simolola_fensetere)
            def tobetsa_Boleng(가로,세로):
                for konopo in (1,0):sedirelwa.sendall(struct.pack('>BBHH',5,konopo,가로,세로))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            tobetsa_Boleng(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for Letshwao_Boleng in '한글':누름값(0x1000000|ord(Letshwao_Boleng));누름값(0x1000000|ord(Letshwao_Boleng),False)
            for 횟수 in (1,2):
                dirisa=len(대화기록);tobetsa_Boleng(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),dirisa)
            time.sleep(.3)
            fensetere_sethalo=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=fensetere_sethalo.crop((110,272,530,300)).tobytes()
            fensetere_sethalo.save(str(결과자료/'java-swing.png'))
            dirisa=len(대화기록);tobetsa_Boleng(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',dirisa)
        # Download the guest-created bytes through FTP in the same GUI VM.
        faele_tsenyo_leina={'java':'java.txt','c':'c.txt','python':'python.txt'}[Puo]
        setlhalosataelo('cp '+faele_tsenyo_leina+' /netefatsa_5fb2b747.txt')
        받은수=bytearray();faele_fudusa_Kgolagano.retrbinary('RETR netefatsa_5fb2b747.txt',받은수.extend);assert 받은수==예상파일.encode()
        setlhalosataelo('echo preserved > 출력예제.'+('py' if Puo=='python' else Puo))
        assert 'EXAMPLES READY' in setlhalosataelo('example '+Puo)
        assert '\npreserved\n' in setlhalosataelo('cat 출력예제.'+('py' if Puo=='python' else Puo))
        assert '한/영 taetsi_Boleng, Shift+Space 또는 F9' in setlhalosataelo('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in setlhalosataelo('echo GUI NETWORK TOGETHER')
        faele_fudusa_Kgolagano.quit();faele_fudusa_Kgolagano=None;assert 'FTP stopped' in setlhalosataelo('ftpd stop')
        print('PASS '+Puo+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if faele_fudusa_Kgolagano:
            try:faele_fudusa_Kgolagano.close()
            except OSError:pass
        if sedirelwa:sedirelwa.close()
        Thulaganyo.terminate()
        try:Thulaganyo.wait(timeout=8)
        except subprocess.TimeoutExpired:Thulaganyo.kill();Thulaganyo.wait()
        setlhophi.close();Thulaganyo.stdout.close();(결과자료/(Puo+'-serial.log')).write_bytes(대화기록)


def dirisa():
    결과자료=기준/'build/verification/examples';결과자료.mkdir(parents=True,exist_ok=True)
    netefatso_pego={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for Puo in ('java','c','python'):
                test_언어(Puo,되돌림서버항목,결과자료);netefatso_pego['languages'].append(Puo)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(setlhopha_Boleng_4b6d6445,tshedimosetso.encode()) for setlhopha_Boleng_4b6d6445,tshedimosetso in 예상결과],되돌림서버항목.수신됨
            netefatso_pego['host_network_payloads']=[{'protocol':setlhopha_Boleng_4b6d6445,'text':tshedimosetso.decode()} for setlhopha_Boleng_4b6d6445,tshedimosetso in 되돌림서버항목.수신됨]
        netefatso_pego.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(결과자료/'report.json').write_text(json.dumps(netefatso_pego,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':dirisa()
