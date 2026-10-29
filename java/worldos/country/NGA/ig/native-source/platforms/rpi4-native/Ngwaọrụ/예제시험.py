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
from desktọpụ_lèe import 정확한값
from 예제되돌림서버 import 되돌림서버
from mee_nnyemiwu import 기준


def test_언어(Asụsụ,되돌림서버항목,결과자료):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    ùsòrò=subprocess.Popen(['python3',str(기준/'Ngwaọrụ/mee_nnyemiwu.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    ihe_nhọpụta=selectors.DefaultSelector();ihe_nhọpụta.register(ùsòrò.stdout,selectors.EVENT_READ)
    대화기록=bytearray();klayènt=None;ọbọakwụkwọ_dògharịa_njikọ=None
    def 수신하기(확인표시,Bido=0):
        mèdebe_Nnokwata=time.monotonic()+60
        while 확인표시 not in 대화기록[Bido:]:
            if time.monotonic()>mèdebe_Nnokwata or ùsòrò.poll() is not None:raise AssertionError(대화기록[Bido:].decode('utf-8','replace'))
            for 누름값,_ in ihe_nhọpụta.select(.1):
                datà=누름값.fileobj.read(65536)
                if datà:대화기록.extend(datà)
        return 대화기록[Bido:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(adimara_valuu,누르는중=True):klayènt.sendall(struct.pack('>BBHI',4,int(누르는중),0,adimara_valuu))
    def Mbido_Nnokwata(ahịrī):
        Bido=len(대화기록)
        for koòdù_nkeakàrà in ahịrī+'\n':
            adimara_valuu=0xff0d if koòdù_nkeakàrà=='\n' else ord(koòdù_nkeakàrà) if ord(koòdù_nkeakàrà)<256 else 0x1000000|ord(koòdù_nkeakàrà)
            누름값(adimara_valuu);누름값(adimara_valuu,False)
        return Bido
    def nkọwannyemiwu(ahịrī):return 수신하기(b'jkoros-native> ',Mbido_Nnokwata(ahịrī))
    def mee_nnyemiwu(ahịrī,예상결과):
        SMS=nkọwannyemiwu(ahịrī);assert 예상결과 in SMS and 'exit 0' in SMS,(ahịrī,SMS)
        return SMS
    def 화소들():
        klayènt.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            otu_valuu_4b6d6445=정확한값(klayènt,1)[0]
            if otu_valuu_4b6d6445==2:continue
            if otu_valuu_4b6d6445==3:
                개수=struct.unpack('>I',정확한값(klayènt,7)[3:])[0];정확한값(klayènt,개수);continue
            assert otu_valuu_4b6d6445==0,otu_valuu_4b6d6445
            항목수=struct.unpack('>H',정확한값(klayènt,3)[1:])[0]
            for _ in range(항목수):
                ngakọrịta_x,세로좌표,너비값,높이값,òtù_mkpụrụedemede=struct.unpack('>HHHHi',정확한값(klayènt,12));assert òtù_mkpụrụedemede==0,òtù_mkpụrụedemede
                datà=정확한값(klayènt,너비값*높이값*4)
                for 행위치 in range(높이값):
                    for 열위치 in range(너비값):
                        원본자료=(행위치*너비값+열위치)*4;ebenlereanya=((세로좌표+행위치)*640+ngakọrịta_x+열위치)*3
                        빛삼원색[ebenlereanya:ebenlereanya+3]=bytes((datà[원본자료+2],datà[원본자료+1],datà[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        klayènt=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert 정확한값(klayènt,12)==b'RFB 003.008\n';klayènt.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(klayènt,정확한값(klayènt,1)[0]);klayènt.sendall(b'\x01');assert 정확한값(klayènt,4)==b'\0'*4
        klayènt.sendall(b'\x01');초기값=정확한값(klayènt,24);정확한값(klayènt,struct.unpack('>I',초기값[20:])[0])
        klayènt.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        klayènt.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in nkọwannyemiwu('ftpd start')
        ọbọakwụkwọ_dògharịa_njikọ=ftplib.FTP();ọbọakwụkwọ_dògharịa_njikọ.encoding='utf-8';ọbọakwụkwọ_dògharịa_njikọ.connect('127.0.0.1',파일전송접속번호,timeout=20);ọbọakwụkwọ_dògharịa_njikọ.login()
        ebe_mbulingwa_datà=('GUI와 FTP 동시 사용 '+Asụsụ+' 😀\n').encode()
        ọbọakwụkwọ_dògharịa_njikọ.storbinary('STOR 함께.txt',io.BytesIO(ebe_mbulingwa_datà))
        assert ebe_mbulingwa_datà.decode().strip() in nkọwannyemiwu('cat /함께.txt')
        받은수=bytearray();ọbọakwụkwọ_dògharịa_njikọ.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==ebe_mbulingwa_datà;ọbọakwụkwọ_dògharịa_njikọ.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        zìga_ndepụta=nkọwannyemiwu('ls /example')
        assert all(Aha in zìga_ndepụta for Aha in ('java/','c/','python/','README.md')),zìga_ndepụta
        if Asụsụ=='java':
            꾸러미명세=json.loads((기준/'build/examples/manifest.json').read_text())
            for ụzọ_ozi,ndebà_akara in 꾸러미명세.items():
                nkọwannyemiwu('cp '+ụzọ_ozi+' /example-check.bin')
                ndịnà_valuu=bytearray();ọbọakwụkwọ_dògharịa_njikọ.retrbinary('RETR example-check.bin',ndịnà_valuu.extend)
                assert len(ndịnà_valuu)==ndebà_akara['bytes'] and hashlib.sha256(ndịnà_valuu).hexdigest()==ndebà_akara['sha256'],ụzọ_ozi
            ọbọakwụkwọ_dògharịa_njikọ.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            ndìnààbụọ=bytes(range(256))*64
            ọbọakwụkwọ_dògharịa_njikọ.storbinary('STOR boundary.bin',io.BytesIO(ndìnààbụọ))
            ndịnà_valuu=bytearray();ọbọakwụkwọ_dògharịa_njikọ.retrbinary('RETR boundary.bin',ndịnà_valuu.extend)
            assert ndịnà_valuu==ndìnààbụọ and 'boundary.bin' in ọbọakwụkwọ_dògharịa_njikọ.nlst()
            nkọwannyemiwu('cp /boundary.bin /boundary-copy.bin')
            ndịnà_valuu=bytearray();ọbọakwụkwọ_dògharịa_njikọ.retrbinary('RETR boundary-copy.bin',ndịnà_valuu.extend)
            assert ndịnà_valuu==ndìnààbụọ
            ọbọakwụkwọ_dògharịa_njikọ.delete('boundary.bin');ọbọakwụkwọ_dògharịa_njikọ.delete('boundary-copy.bin')
        assert '출력예제' in nkọwannyemiwu('ls /example/'+Asụsụ)
        nkọwannyemiwu('cd /example/'+Asụsụ)
        akara_ahà_tebùl={'java':'JAVA','c':'C','python':'PYTHON'}[Asụsụ]
        예상파일=akara_ahà_tebùl+' Faịlụ: 한글 datà 😀\n'
        if Asụsụ=='java':
            mee_nnyemiwu('javac 출력예제.java','Compiled:');mee_nnyemiwu('java 출력예제','JAVA 출력: 안녕하세요 😀')
            mee_nnyemiwu('javac 파일예제.java','Compiled:');mee_nnyemiwu('java 파일예제',예상파일)
            mee_nnyemiwu('java 네트워크예제 {} {}'.format(되돌림서버항목.TCP_pọọt,되돌림서버항목.전문접속번호),'JAVA 네트워크 nkwàdo_eziokwū: TCP UDP 한글')
            그림명령='java 그래픽예제'
        elif Asụsụ=='c':
            for Aha,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('Faịlụ','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 nkwàdo_eziokwū: UDP 한글')]:
                mee_nnyemiwu('cc '+Aha+'예제.c -o mee_nnyemiwu','Compiled native ARM64 ELF:')
                mee_nnyemiwu('./mee_nnyemiwu'+전달값,예상결과)
            mee_nnyemiwu('cc 그래픽예제.c -o mee_nnyemiwu','Compiled native ARM64 ELF:');그림명령='./mee_nnyemiwu'
        else:
            for Aha,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('Faịlụ','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 nkwàdo_eziokwū: UDP 한글')]:
                mee_nnyemiwu('python '+Aha+'예제.py'+전달값,예상결과)
            그림명령='python 그래픽예제.py'
        Mbido_osise=Mbido_Nnokwata(그림명령)
        SMS=수신하기('그림을 확인한 Àzụ_valuu Enter를 누르세요.\r\n'.encode(),Mbido_osise)
        assert akara_ahà_tebùl+' 그래픽: 빨강 초록 파랑' in SMS and 'exit 0' not in SMS,SMS
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        ọbọakwụkwọ_dògharịa_njikọ.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();ọbọakwụkwọ_dògharịa_njikọ.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';ọbọakwụkwọ_dògharịa_njikọ.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            Nnokwata_valuu=(세로좌표*640+610)*3;assert tuple(빛삼원색[Nnokwata_valuu:Nnokwata_valuu+3])==색상,(Asụsụ,세로좌표,tuple(빛삼원색[Nnokwata_valuu:Nnokwata_valuu+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(결과자료/(Asụsụ+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',Mbido_osise)
        if Asụsụ=='java':
            Mbido_windò=Mbido_Nnokwata('java 창예제')
            수신하기('GUI 예제 Kwado: 창예제'.encode(),Mbido_windò)
            def pịkịnye_valuu(가로,세로):
                for ọdụmbi in (1,0):klayènt.sendall(struct.pack('>BBHH',5,ọdụmbi,가로,세로))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            pịkịnye_valuu(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for mkpụrụedemede_valuu in '한글':누름값(0x1000000|ord(mkpụrụedemede_valuu));누름값(0x1000000|ord(mkpụrụedemede_valuu),False)
            for 횟수 in (1,2):
                Bido=len(대화기록);pịkịnye_valuu(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Bido)
            time.sleep(.3)
            windò_osise=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=windò_osise.crop((110,272,530,300)).tobytes()
            windò_osise.save(str(결과자료/'java-swing.png'))
            Bido=len(대화기록);pịkịnye_valuu(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',Bido)
        # Download the guest-created bytes through FTP in the same GUI VM.
        ọbọakwụkwọ_ndebà_akara_ahà={'java':'java.txt','c':'c.txt','python':'python.txt'}[Asụsụ]
        nkọwannyemiwu('cp '+ọbọakwụkwọ_ndebà_akara_ahà+' /mee_ịbanihe.txt')
        받은수=bytearray();ọbọakwụkwọ_dògharịa_njikọ.retrbinary('RETR mee_ịbanihe.txt',받은수.extend);assert 받은수==예상파일.encode()
        nkọwannyemiwu('echo preserved > 출력예제.'+('py' if Asụsụ=='python' else Asụsụ))
        assert 'EXAMPLES READY' in nkọwannyemiwu('example '+Asụsụ)
        assert '\npreserved\n' in nkọwannyemiwu('cat 출력예제.'+('py' if Asụsụ=='python' else Asụsụ))
        assert '한/영 ọtụgwo_valuu, Shift+Space 또는 F9' in nkọwannyemiwu('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in nkọwannyemiwu('echo GUI NETWORK TOGETHER')
        ọbọakwụkwọ_dògharịa_njikọ.quit();ọbọakwụkwọ_dògharịa_njikọ=None;assert 'FTP stopped' in nkọwannyemiwu('ftpd stop')
        print('PASS '+Asụsụ+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if ọbọakwụkwọ_dògharịa_njikọ:
            try:ọbọakwụkwọ_dògharịa_njikọ.close()
            except OSError:pass
        if klayènt:klayènt.close()
        ùsòrò.terminate()
        try:ùsòrò.wait(timeout=8)
        except subprocess.TimeoutExpired:ùsòrò.kill();ùsòrò.wait()
        ihe_nhọpụta.close();ùsòrò.stdout.close();(결과자료/(Asụsụ+'-serial.log')).write_bytes(대화기록)


def Bido():
    결과자료=기준/'build/verification/examples';결과자료.mkdir(parents=True,exist_ok=True)
    nkwèputaonòdù_akụkọ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for Asụsụ in ('java','c','python'):
                test_언어(Asụsụ,되돌림서버항목,결과자료);nkwèputaonòdù_akụkọ['languages'].append(Asụsụ)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(otu_valuu_4b6d6445,datà.encode()) for otu_valuu_4b6d6445,datà in 예상결과],되돌림서버항목.수신됨
            nkwèputaonòdù_akụkọ['host_network_payloads']=[{'protocol':otu_valuu_4b6d6445,'text':datà.decode()} for otu_valuu_4b6d6445,datà in 되돌림서버항목.수신됨]
        nkwèputaonòdù_akụkọ.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(결과자료/'report.json').write_text(json.dumps(nkwèputaonòdù_akụkọ,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Bido()
