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
from Biro_wonin import 정확한값
from 예제되돌림서버 import 되돌림서버
from def_ndigel import 기준


def test_언어(Làkk,되돌림서버항목,결과자료):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    yokkute=subprocess.Popen(['python3',str(기준/'Jumtukaay_yi/def_ndigel.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    tànnkat=selectors.DefaultSelector();tànnkat.register(yokkute.stdout,selectors.EVENT_READ)
    대화기록=bytearray();lëkkalekat=None;bara_denc_toxal_jokkalóo=None
    def 수신하기(확인표시,daw=0):
        jeexal_Randal=time.monotonic()+60
        while 확인표시 not in 대화기록[daw:]:
            if time.monotonic()>jeexal_Randal or yokkute.poll() is not None:raise AssertionError(대화기록[daw:].decode('utf-8','replace'))
            for 누름값,_ in tànnkat.select(.1):
                mbir=누름값.fileobj.read(65536)
                if mbir:대화기록.extend(mbir)
        return 대화기록[daw:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(sembóol_xëyma,누르는중=True):lëkkalekat.sendall(struct.pack('>BBHI',4,int(누르는중),0,sembóol_xëyma))
    def Door_Randal(buum):
        daw=len(대화기록)
        for kotu_araf in buum+'\n':
            sembóol_xëyma=0xff0d if kotu_araf=='\n' else ord(kotu_araf) if ord(kotu_araf)<256 else 0x1000000|ord(kotu_araf)
            누름값(sembóol_xëyma);누름값(sembóol_xëyma,False)
        return daw
    def Wëreef(buum):return 수신하기(b'jkoros-native> ',Door_Randal(buum))
    def def_ndigel(buum,예상결과):
        Tekst=Wëreef(buum);assert 예상결과 in Tekst and 'exit 0' in Tekst,(buum,Tekst)
        return Tekst
    def 화소들():
        lëkkalekat.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            ngiir_xëyma=정확한값(lëkkalekat,1)[0]
            if ngiir_xëyma==2:continue
            if ngiir_xëyma==3:
                개수=struct.unpack('>I',정확한값(lëkkalekat,7)[3:])[0];정확한값(lëkkalekat,개수);continue
            assert ngiir_xëyma==0,ngiir_xëyma
            항목수=struct.unpack('>H',정확한값(lëkkalekat,3)[1:])[0]
            for _ in range(항목수):
                rëddu_iks_yi,세로좌표,너비값,높이값,Mbindin=struct.unpack('>HHHHi',정확한값(lëkkalekat,12));assert Mbindin==0,Mbindin
                mbir=정확한값(lëkkalekat,너비값*높이값*4)
                for 행위치 in range(높이값):
                    for 열위치 in range(너비값):
                        원본자료=(행위치*너비값+열위치)*4;luñu_name=((세로좌표+행위치)*640+rëddu_iks_yi+열위치)*3
                        빛삼원색[luñu_name:luñu_name+3]=bytes((mbir[원본자료+2],mbir[원본자료+1],mbir[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        lëkkalekat=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert 정확한값(lëkkalekat,12)==b'RFB 003.008\n';lëkkalekat.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(lëkkalekat,정확한값(lëkkalekat,1)[0]);lëkkalekat.sendall(b'\x01');assert 정확한값(lëkkalekat,4)==b'\0'*4
        lëkkalekat.sendall(b'\x01');초기값=정확한값(lëkkalekat,24);정확한값(lëkkalekat,struct.unpack('>I',초기값[20:])[0])
        lëkkalekat.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        lëkkalekat.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in Wëreef('ftpd start')
        bara_denc_toxal_jokkalóo=ftplib.FTP();bara_denc_toxal_jokkalóo.encoding='utf-8';bara_denc_toxal_jokkalóo.connect('127.0.0.1',파일전송접속번호,timeout=20);bara_denc_toxal_jokkalóo.login()
        njoxe_yu_solowu_mbir=('GUI와 FTP 동시 사용 '+Làkk+' 😀\n').encode()
        bara_denc_toxal_jokkalóo.storbinary('STOR 함께.txt',io.BytesIO(njoxe_yu_solowu_mbir))
        assert njoxe_yu_solowu_mbir.decode().strip() in Wëreef('cat /함께.txt')
        받은수=bytearray();bara_denc_toxal_jokkalóo.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==njoxe_yu_solowu_mbir;bara_denc_toxal_jokkalóo.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        Yónnee_lim=Wëreef('ls /example')
        assert all(tur_253d1510 in Yónnee_lim for tur_253d1510 in ('java/','c/','python/','README.md')),Yónnee_lim
        if Làkk=='java':
            꾸러미명세=json.loads((기준/'build/examples/manifest.json').read_text())
            for Yoonu_jëmale,dugal_xabaar_Tomb in 꾸러미명세.items():
                Wëreef('cp '+Yoonu_jëmale+' /example-check.bin')
                Këmb_xëyma=bytearray();bara_denc_toxal_jokkalóo.retrbinary('RETR example-check.bin',Këmb_xëyma.extend)
                assert len(Këmb_xëyma)==dugal_xabaar_Tomb['bytes'] and hashlib.sha256(Këmb_xëyma).hexdigest()==dugal_xabaar_Tomb['sha256'],Yoonu_jëmale
            bara_denc_toxal_jokkalóo.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            Seexalin_ci_kaw_0_et1=bytes(range(256))*64
            bara_denc_toxal_jokkalóo.storbinary('STOR boundary.bin',io.BytesIO(Seexalin_ci_kaw_0_et1))
            Këmb_xëyma=bytearray();bara_denc_toxal_jokkalóo.retrbinary('RETR boundary.bin',Këmb_xëyma.extend)
            assert Këmb_xëyma==Seexalin_ci_kaw_0_et1 and 'boundary.bin' in bara_denc_toxal_jokkalóo.nlst()
            Wëreef('cp /boundary.bin /boundary-copy.bin')
            Këmb_xëyma=bytearray();bara_denc_toxal_jokkalóo.retrbinary('RETR boundary-copy.bin',Këmb_xëyma.extend)
            assert Këmb_xëyma==Seexalin_ci_kaw_0_et1
            bara_denc_toxal_jokkalóo.delete('boundary.bin');bara_denc_toxal_jokkalóo.delete('boundary-copy.bin')
        assert '출력예제' in Wëreef('ls /example/'+Làkk)
        Wëreef('cd /example/'+Làkk)
        tur_àlluwa={'java':'JAVA','c':'C','python':'PYTHON'}[Làkk]
        예상파일=tur_àlluwa+' bara_denc: 한글 mbir 😀\n'
        if Làkk=='java':
            def_ndigel('javac 출력예제.java','Compiled:');def_ndigel('java 출력예제','JAVA 출력: 안녕하세요 😀')
            def_ndigel('javac 파일예제.java','Compiled:');def_ndigel('java 파일예제',예상파일)
            def_ndigel('java 네트워크예제 {} {}'.format(되돌림서버항목.TCP_jël,되돌림서버항목.전문접속번호),'JAVA 네트워크 luñutu: TCP UDP 한글')
            그림명령='java 그래픽예제'
        elif Làkk=='c':
            for tur_253d1510,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('bara_denc','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 luñutu: UDP 한글')]:
                def_ndigel('cc '+tur_253d1510+'예제.c -o def_ndigel','Compiled native ARM64 ELF:')
                def_ndigel('./def_ndigel'+전달값,예상결과)
            def_ndigel('cc 그래픽예제.c -o def_ndigel','Compiled native ARM64 ELF:');그림명령='./def_ndigel'
        else:
            for tur_253d1510,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('bara_denc','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 luñutu: UDP 한글')]:
                def_ndigel('python '+tur_253d1510+'예제.py'+전달값,예상결과)
            그림명령='python 그래픽예제.py'
        Door_deseñ=Door_Randal(그림명령)
        Tekst=수신하기('그림을 확인한 woñeeku_xëyma Enter를 누르세요.\r\n'.encode(),Door_deseñ)
        assert tur_àlluwa+' 그래픽: 빨강 초록 파랑' in Tekst and 'exit 0' not in Tekst,Tekst
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        bara_denc_toxal_jokkalóo.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();bara_denc_toxal_jokkalóo.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';bara_denc_toxal_jokkalóo.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            Randal_xëyma=(세로좌표*640+610)*3;assert tuple(빛삼원색[Randal_xëyma:Randal_xëyma+3])==색상,(Làkk,세로좌표,tuple(빛삼원색[Randal_xëyma:Randal_xëyma+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(결과자료/(Làkk+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',Door_deseñ)
        if Làkk=='java':
            Door_palanteer=Door_Randal('java 창예제')
            수신하기('GUI 예제 jël_matuwaay: 창예제'.encode(),Door_palanteer)
            def bës_xëyma(가로,세로):
                for butoñ in (1,0):lëkkalekat.sendall(struct.pack('>BBHH',5,butoñ,가로,세로))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            bës_xëyma(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for Araf_xëyma in '한글':누름값(0x1000000|ord(Araf_xëyma));누름값(0x1000000|ord(Araf_xëyma),False)
            for 횟수 in (1,2):
                daw=len(대화기록);bës_xëyma(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),daw)
            time.sleep(.3)
            palanteer_deseñ=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=palanteer_deseñ.crop((110,272,530,300)).tobytes()
            palanteer_deseñ.save(str(결과자료/'java-swing.png'))
            daw=len(대화기록);bës_xëyma(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',daw)
        # Download the guest-created bytes through FTP in the same GUI VM.
        bara_denc_dugal_xabaar_tur={'java':'java.txt','c':'c.txt','python':'python.txt'}[Làkk]
        Wëreef('cp '+bara_denc_dugal_xabaar_tur+' /wéral.txt')
        받은수=bytearray();bara_denc_toxal_jokkalóo.retrbinary('RETR wéral.txt',받은수.extend);assert 받은수==예상파일.encode()
        Wëreef('echo preserved > 출력예제.'+('py' if Làkk=='python' else Làkk))
        assert 'EXAMPLES READY' in Wëreef('example '+Làkk)
        assert '\npreserved\n' in Wëreef('cat 출력예제.'+('py' if Làkk=='python' else Làkk))
        assert '한/영 kër_xëyma, Shift+Space 또는 F9' in Wëreef('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in Wëreef('echo GUI NETWORK TOGETHER')
        bara_denc_toxal_jokkalóo.quit();bara_denc_toxal_jokkalóo=None;assert 'FTP stopped' in Wëreef('ftpd stop')
        print('PASS '+Làkk+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if bara_denc_toxal_jokkalóo:
            try:bara_denc_toxal_jokkalóo.close()
            except OSError:pass
        if lëkkalekat:lëkkalekat.close()
        yokkute.terminate()
        try:yokkute.wait(timeout=8)
        except subprocess.TimeoutExpired:yokkute.kill();yokkute.wait()
        tànnkat.close();yokkute.stdout.close();(결과자료/(Làkk+'-serial.log')).write_bytes(대화기록)


def daw():
    결과자료=기준/'build/verification/examples';결과자료.mkdir(parents=True,exist_ok=True)
    wéral_tënk={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for Làkk in ('java','c','python'):
                test_언어(Làkk,되돌림서버항목,결과자료);wéral_tënk['languages'].append(Làkk)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(ngiir_xëyma,mbir.encode()) for ngiir_xëyma,mbir in 예상결과],되돌림서버항목.수신됨
            wéral_tënk['host_network_payloads']=[{'protocol':ngiir_xëyma,'text':mbir.decode()} for ngiir_xëyma,mbir in 되돌림서버항목.수신됨]
        wéral_tënk.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(결과자료/'report.json').write_text(json.dumps(wéral_tënk,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':daw()
