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
from iş_stoly_görkez import 정확한값
from 예제되돌림서버 import 되돌림서버
from ýerine_ýetir_buýruk import 기준


def test_언어(Dil,되돌림서버항목,결과자료):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    Proses=subprocess.Popen(['python3',str(기준/'Gurallar/ýerine_ýetir_buýruk.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    saýlaýjy=selectors.DefaultSelector();saýlaýjy.register(Proses.stdout,selectors.EVENT_READ)
    대화기록=bytearray();müşderi=None;faýl_geçir_birikme=None
    def 수신하기(확인표시,Bitir=0):
        tamamla_Süýşüriş=time.monotonic()+60
        while 확인표시 not in 대화기록[Bitir:]:
            if time.monotonic()>tamamla_Süýşüriş or Proses.poll() is not None:raise AssertionError(대화기록[Bitir:].decode('utf-8','replace'))
            for 누름값,_ in saýlaýjy.select(.1):
                maglumat=누름값.fileobj.read(65536)
                if maglumat:대화기록.extend(maglumat)
        return 대화기록[Bitir:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(nyşan_baha,누르는중=True):müşderi.sendall(struct.pack('>BBHI',4,int(누르는중),0,nyşan_baha))
    def başlat_Süýşüriş(setir):
        Bitir=len(대화기록)
        for nyşanyň_kody in setir+'\n':
            nyşan_baha=0xff0d if nyşanyň_kody=='\n' else ord(nyşanyň_kody) if ord(nyşanyň_kody)<256 else 0x1000000|ord(nyşanyň_kody)
            누름값(nyşan_baha);누름값(nyşan_baha,False)
        return Bitir
    def gabyjak(setir):return 수신하기(b'jkoros-native> ',başlat_Süýşüriş(setir))
    def ýerine_ýetir_buýruk(setir,예상결과):
        Metin=gabyjak(setir);assert 예상결과 in Metin and 'exit 0' in Metin,(setir,Metin)
        return Metin
    def 화소들():
        müşderi.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            kategoriýa_baha=정확한값(müşderi,1)[0]
            if kategoriýa_baha==2:continue
            if kategoriýa_baha==3:
                개수=struct.unpack('>I',정확한값(müşderi,7)[3:])[0];정확한값(müşderi,개수);continue
            assert kategoriýa_baha==0,kategoriýa_baha
            항목수=struct.unpack('>H',정확한값(müşderi,3)[1:])[0]
            for _ in range(항목수):
                x_koordinatasy,세로좌표,너비값,높이값,nyşanlaryň_toplumy=struct.unpack('>HHHHi',정확한값(müşderi,12));assert nyşanlaryň_toplumy==0,nyşanlaryň_toplumy
                maglumat=정확한값(müşderi,너비값*높이값*4)
                for 행위치 in range(높이값):
                    for 열위치 in range(너비값):
                        원본자료=(행위치*너비값+열위치)*4;niýet=((세로좌표+행위치)*640+x_koordinatasy+열위치)*3
                        빛삼원색[niýet:niýet+3]=bytes((maglumat[원본자료+2],maglumat[원본자료+1],maglumat[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        müşderi=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert 정확한값(müşderi,12)==b'RFB 003.008\n';müşderi.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(müşderi,정확한값(müşderi,1)[0]);müşderi.sendall(b'\x01');assert 정확한값(müşderi,4)==b'\0'*4
        müşderi.sendall(b'\x01');초기값=정확한값(müşderi,24);정확한값(müşderi,struct.unpack('>I',초기값[20:])[0])
        müşderi.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        müşderi.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in gabyjak('ftpd start')
        faýl_geçir_birikme=ftplib.FTP();faýl_geçir_birikme.encoding='utf-8';faýl_geçir_birikme.connect('127.0.0.1',파일전송접속번호,timeout=20);faýl_geçir_birikme.login()
        ýük_gutujygy_maglumat=('GUI와 FTP 동시 사용 '+Dil+' 😀\n').encode()
        faýl_geçir_birikme.storbinary('STOR 함께.txt',io.BytesIO(ýük_gutujygy_maglumat))
        assert ýük_gutujygy_maglumat.decode().strip() in gabyjak('cat /함께.txt')
        받은수=bytearray();faýl_geçir_birikme.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==ýük_gutujygy_maglumat;faýl_geçir_birikme.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        iber_Sanaw=gabyjak('ls /example')
        assert all(Ad in iber_Sanaw for Ad in ('java/','c/','python/','README.md')),iber_Sanaw
        if Dil=='java':
            꾸러미명세=json.loads((기준/'build/examples/manifest.json').read_text())
            for Ýol,girizmeklik_utuk in 꾸러미명세.items():
                gabyjak('cp '+Ýol+' /example-check.bin')
                Mazmun_baha=bytearray();faýl_geçir_birikme.retrbinary('RETR example-check.bin',Mazmun_baha.extend)
                assert len(Mazmun_baha)==girizmeklik_utuk['bytes'] and hashlib.sha256(Mazmun_baha).hexdigest()==girizmeklik_utuk['sha256'],Ýol
            faýl_geçir_birikme.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            ikilik=bytes(range(256))*64
            faýl_geçir_birikme.storbinary('STOR boundary.bin',io.BytesIO(ikilik))
            Mazmun_baha=bytearray();faýl_geçir_birikme.retrbinary('RETR boundary.bin',Mazmun_baha.extend)
            assert Mazmun_baha==ikilik and 'boundary.bin' in faýl_geçir_birikme.nlst()
            gabyjak('cp /boundary.bin /boundary-copy.bin')
            Mazmun_baha=bytearray();faýl_geçir_birikme.retrbinary('RETR boundary-copy.bin',Mazmun_baha.extend)
            assert Mazmun_baha==ikilik
            faýl_geçir_birikme.delete('boundary.bin');faýl_geçir_birikme.delete('boundary-copy.bin')
        assert '출력예제' in gabyjak('ls /example/'+Dil)
        gabyjak('cd /example/'+Dil)
        at_tablisa={'java':'JAVA','c':'C','python':'PYTHON'}[Dil]
        예상파일=at_tablisa+' Faýl: 한글 maglumat 😀\n'
        if Dil=='java':
            ýerine_ýetir_buýruk('javac 출력예제.java','Compiled:');ýerine_ýetir_buýruk('java 출력예제','JAVA 출력: 안녕하세요 😀')
            ýerine_ýetir_buýruk('javac 파일예제.java','Compiled:');ýerine_ýetir_buýruk('java 파일예제',예상파일)
            ýerine_ýetir_buýruk('java 네트워크예제 {} {}'.format(되돌림서버항목.TCP_port,되돌림서버항목.전문접속번호),'JAVA 네트워크 barla: TCP UDP 한글')
            그림명령='java 그래픽예제'
        elif Dil=='c':
            for Ad,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('Faýl','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 barla: UDP 한글')]:
                ýerine_ýetir_buýruk('cc '+Ad+'예제.c -o ýerine_ýetir_buýruk','Compiled native ARM64 ELF:')
                ýerine_ýetir_buýruk('./ýerine_ýetir_buýruk'+전달값,예상결과)
            ýerine_ýetir_buýruk('cc 그래픽예제.c -o ýerine_ýetir_buýruk','Compiled native ARM64 ELF:');그림명령='./ýerine_ýetir_buýruk'
        else:
            for Ad,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('Faýl','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 barla: UDP 한글')]:
                ýerine_ýetir_buýruk('python '+Ad+'예제.py'+전달값,예상결과)
            그림명령='python 그래픽예제.py'
        başlat_çyzgy=başlat_Süýşüriş(그림명령)
        Metin=수신하기('그림을 확인한 Yza_baha Enter를 누르세요.\r\n'.encode(),başlat_çyzgy)
        assert at_tablisa+' 그래픽: 빨강 초록 파랑' in Metin and 'exit 0' not in Metin,Metin
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        faýl_geçir_birikme.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();faýl_geçir_birikme.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';faýl_geçir_birikme.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            Süýşüriş_baha=(세로좌표*640+610)*3;assert tuple(빛삼원색[Süýşüriş_baha:Süýşüriş_baha+3])==색상,(Dil,세로좌표,tuple(빛삼원색[Süýşüriş_baha:Süýşüriş_baha+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(결과자료/(Dil+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',başlat_çyzgy)
        if Dil=='java':
            başlat_penjire=başlat_Süýşüriş('java 창예제')
            수신하기('GUI 예제 Taýýarla: 창예제'.encode(),başlat_penjire)
            def bas_baha(가로,세로):
                for düwme in (1,0):müşderi.sendall(struct.pack('>BBHH',5,düwme,가로,세로))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            bas_baha(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for nyşan_baha_068c2631 in '한글':누름값(0x1000000|ord(nyşan_baha_068c2631));누름값(0x1000000|ord(nyşan_baha_068c2631),False)
            for 횟수 in (1,2):
                Bitir=len(대화기록);bas_baha(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Bitir)
            time.sleep(.3)
            penjire_çyzgy=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=penjire_çyzgy.crop((110,272,530,300)).tobytes()
            penjire_çyzgy.save(str(결과자료/'java-swing.png'))
            Bitir=len(대화기록);bas_baha(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',Bitir)
        # Download the guest-created bytes through FTP in the same GUI VM.
        faýl_girizmeklik_at={'java':'java.txt','c':'c.txt','python':'python.txt'}[Dil]
        gabyjak('cp '+faýl_girizmeklik_at+' /tassykla.txt')
        받은수=bytearray();faýl_geçir_birikme.retrbinary('RETR tassykla.txt',받은수.extend);assert 받은수==예상파일.encode()
        gabyjak('echo preserved > 출력예제.'+('py' if Dil=='python' else Dil))
        assert 'EXAMPLES READY' in gabyjak('example '+Dil)
        assert '\npreserved\n' in gabyjak('cat 출력예제.'+('py' if Dil=='python' else Dil))
        assert '한/영 açar_baha, Shift+Space 또는 F9' in gabyjak('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in gabyjak('echo GUI NETWORK TOGETHER')
        faýl_geçir_birikme.quit();faýl_geçir_birikme=None;assert 'FTP stopped' in gabyjak('ftpd stop')
        print('PASS '+Dil+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if faýl_geçir_birikme:
            try:faýl_geçir_birikme.close()
            except OSError:pass
        if müşderi:müşderi.close()
        Proses.terminate()
        try:Proses.wait(timeout=8)
        except subprocess.TimeoutExpired:Proses.kill();Proses.wait()
        saýlaýjy.close();Proses.stdout.close();(결과자료/(Dil+'-serial.log')).write_bytes(대화기록)


def Bitir():
    결과자료=기준/'build/verification/examples';결과자료.mkdir(parents=True,exist_ok=True)
    barlag_hasabat={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for Dil in ('java','c','python'):
                test_언어(Dil,되돌림서버항목,결과자료);barlag_hasabat['languages'].append(Dil)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(kategoriýa_baha,maglumat.encode()) for kategoriýa_baha,maglumat in 예상결과],되돌림서버항목.수신됨
            barlag_hasabat['host_network_payloads']=[{'protocol':kategoriýa_baha,'text':maglumat.decode()} for kategoriýa_baha,maglumat in 되돌림서버항목.수신됨]
        barlag_hasabat.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(결과자료/'report.json').write_text(json.dumps(barlag_hasabat,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Bitir()
