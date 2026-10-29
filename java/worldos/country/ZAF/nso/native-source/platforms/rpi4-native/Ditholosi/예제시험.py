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
from teskethopo_pogelo import 정확한값
from 예제되돌림서버 import 되돌림서버
from phethagatša_taelo import 기준


def test_언어(Polelo,되돌림서버항목,결과자료):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));파일전송접속번호=임시자원.getsockname()[1]
    tiragalo_a7054519=subprocess.Popen(['python3',str(기준/'Ditholosi/phethagatša_taelo.py'),'--desktop','--network','--port','0','--ftp-port',str(파일전송접속번호)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    sekgethi=selectors.DefaultSelector();sekgethi.register(tiragalo_a7054519.stdout,selectors.EVENT_READ)
    대화기록=bytearray();klaente=None;faele_fetišetša_kgokaganya=None
    def 수신하기(확인표시,Diriša=0):
        fetša_E_Šetšego=time.monotonic()+60
        while 확인표시 not in 대화기록[Diriša:]:
            if time.monotonic()>fetša_E_Šetšego or tiragalo_a7054519.poll() is not None:raise AssertionError(대화기록[Diriša:].decode('utf-8','replace'))
            for 누름값,_ in sekgethi.select(.1):
                data=누름값.fileobj.read(65536)
                if data:대화기록.extend(data)
        return 대화기록[Diriša:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(leswao_boleng,누르는중=True):klaente.sendall(struct.pack('>BBHI',4,int(누르는중),0,leswao_boleng))
    def Thomišo_E_Šetšego(mothaladi):
        Diriša=len(대화기록)
        for khouto_ya_tlhaka in mothaladi+'\n':
            leswao_boleng=0xff0d if khouto_ya_tlhaka=='\n' else ord(khouto_ya_tlhaka) if ord(khouto_ya_tlhaka)<256 else 0x1000000|ord(khouto_ya_tlhaka)
            누름값(leswao_boleng);누름값(leswao_boleng,False)
        return Diriša
    def šele(mothaladi):return 수신하기(b'jkoros-native> ',Thomišo_E_Šetšego(mothaladi))
    def phethagatša_taelo(mothaladi,예상결과):
        Sengwalwa=šele(mothaladi);assert 예상결과 in Sengwalwa and 'exit 0' in Sengwalwa,(mothaladi,Sengwalwa)
        return Sengwalwa
    def 화소들():
        klaente.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            legoro_boleng=정확한값(klaente,1)[0]
            if legoro_boleng==2:continue
            if legoro_boleng==3:
                개수=struct.unpack('>I',정확한값(klaente,7)[3:])[0];정확한값(klaente,개수);continue
            assert legoro_boleng==0,legoro_boleng
            항목수=struct.unpack('>H',정확한값(klaente,3)[1:])[0]
            for _ in range(항목수):
                kamano_ya_x,세로좌표,너비값,높이값,sete_ya_ditlhaka=struct.unpack('>HHHHi',정확한값(klaente,12));assert sete_ya_ditlhaka==0,sete_ya_ditlhaka
                data=정확한값(klaente,너비값*높이값*4)
                for 행위치 in range(높이값):
                    for 열위치 in range(너비값):
                        원본자료=(행위치*너비값+열위치)*4;nepo=((세로좌표+행위치)*640+kamano_ya_x+열위치)*3
                        빛삼원색[nepo:nepo+3]=bytes((data[원본자료+2],data[원본자료+1],data[원본자료]))
            if 항목수:return 빛삼원색
    try:
        수신하기(b'TERMINAL READY');수신하기(b'jkoros-native> ',대화기록.rfind(b'TERMINAL READY'))
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        klaente=socket.create_connection(('127.0.0.1',접속번호),timeout=10)
        assert 정확한값(klaente,12)==b'RFB 003.008\n';klaente.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(klaente,정확한값(klaente,1)[0]);klaente.sendall(b'\x01');assert 정확한값(klaente,4)==b'\0'*4
        klaente.sendall(b'\x01');초기값=정확한값(klaente,24);정확한값(klaente,struct.unpack('>I',초기값[20:])[0])
        klaente.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        klaente.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in šele('ftpd start')
        faele_fetišetša_kgokaganya=ftplib.FTP();faele_fetišetša_kgokaganya.encoding='utf-8';faele_fetišetša_kgokaganya.connect('127.0.0.1',파일전송접속번호,timeout=20);faele_fetišetša_kgokaganya.login()
        morwalotefelwa_data=('GUI와 FTP 동시 사용 '+Polelo+' 😀\n').encode()
        faele_fetišetša_kgokaganya.storbinary('STOR 함께.txt',io.BytesIO(morwalotefelwa_data))
        assert morwalotefelwa_data.decode().strip() in šele('cat /함께.txt')
        받은수=bytearray();faele_fetišetša_kgokaganya.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==morwalotefelwa_data;faele_fetišetša_kgokaganya.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        Romela_Lenaneo=šele('ls /example')
        assert all(Leina in Romela_Lenaneo for Leina in ('java/','c/','python/','README.md')),Romela_Lenaneo
        if Polelo=='java':
            꾸러미명세=json.loads((기준/'build/examples/manifest.json').read_text())
            for Tsejana,go_tsenya_tshedimošo_ntlha in 꾸러미명세.items():
                šele('cp '+Tsejana+' /example-check.bin')
                Diteng_boleng=bytearray();faele_fetišetša_kgokaganya.retrbinary('RETR example-check.bin',Diteng_boleng.extend)
                assert len(Diteng_boleng)==go_tsenya_tshedimošo_ntlha['bytes'] and hashlib.sha256(Diteng_boleng).hexdigest()==go_tsenya_tshedimošo_ntlha['sha256'],Tsejana
            faele_fetišetša_kgokaganya.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            paenari=bytes(range(256))*64
            faele_fetišetša_kgokaganya.storbinary('STOR boundary.bin',io.BytesIO(paenari))
            Diteng_boleng=bytearray();faele_fetišetša_kgokaganya.retrbinary('RETR boundary.bin',Diteng_boleng.extend)
            assert Diteng_boleng==paenari and 'boundary.bin' in faele_fetišetša_kgokaganya.nlst()
            šele('cp /boundary.bin /boundary-copy.bin')
            Diteng_boleng=bytearray();faele_fetišetša_kgokaganya.retrbinary('RETR boundary-copy.bin',Diteng_boleng.extend)
            assert Diteng_boleng==paenari
            faele_fetišetša_kgokaganya.delete('boundary.bin');faele_fetišetša_kgokaganya.delete('boundary-copy.bin')
        assert '출력예제' in šele('ls /example/'+Polelo)
        šele('cd /example/'+Polelo)
        leina_tafola={'java':'JAVA','c':'C','python':'PYTHON'}[Polelo]
        예상파일=leina_tafola+' Faele: 한글 data 😀\n'
        if Polelo=='java':
            phethagatša_taelo('javac 출력예제.java','Compiled:');phethagatša_taelo('java 출력예제','JAVA 출력: 안녕하세요 😀')
            phethagatša_taelo('javac 파일예제.java','Compiled:');phethagatša_taelo('java 파일예제',예상파일)
            phethagatša_taelo('java 네트워크예제 {} {}'.format(되돌림서버항목.TCP_phote,되돌림서버항목.전문접속번호),'JAVA 네트워크 kgonthiša: TCP UDP 한글')
            그림명령='java 그래픽예제'
        elif Polelo=='c':
            for Leina,전달값,예상결과 in [('출력','', 'C 출력: 안녕하세요 😀'),('Faele','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 kgonthiša: UDP 한글')]:
                phethagatša_taelo('cc '+Leina+'예제.c -o phethagatša_taelo','Compiled native ARM64 ELF:')
                phethagatša_taelo('./phethagatša_taelo'+전달값,예상결과)
            phethagatša_taelo('cc 그래픽예제.c -o phethagatša_taelo','Compiled native ARM64 ELF:');그림명령='./phethagatša_taelo'
        else:
            for Leina,전달값,예상결과 in [('출력','','PYTHON 출력: 안녕하세요 😀'),('Faele','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 kgonthiša: UDP 한글')]:
                phethagatša_taelo('python '+Leina+'예제.py'+전달값,예상결과)
            그림명령='python 그래픽예제.py'
        Thomišo_sethalwa=Thomišo_E_Šetšego(그림명령)
        Sengwalwa=수신하기('그림을 확인한 Morago_boleng Enter를 누르세요.\r\n'.encode(),Thomišo_sethalwa)
        assert leina_tafola+' 그래픽: 빨강 초록 파랑' in Sengwalwa and 'exit 0' not in Sengwalwa,Sengwalwa
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        faele_fetišetša_kgokaganya.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();faele_fetišetša_kgokaganya.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';faele_fetišetša_kgokaganya.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            E_Šetšego_boleng=(세로좌표*640+610)*3;assert tuple(빛삼원색[E_Šetšego_boleng:E_Šetšego_boleng+3])==색상,(Polelo,세로좌표,tuple(빛삼원색[E_Šetšego_boleng:E_Šetšego_boleng+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(결과자료/(Polelo+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in 수신하기(b'jkoros-native> ',Thomišo_sethalwa)
        if Polelo=='java':
            Thomišo_lefastere=Thomišo_E_Šetšego('java 창예제')
            수신하기('GUI 예제 Lokišetša: 창예제'.encode(),Thomišo_lefastere)
            def klika_boleng(가로,세로):
                for konope in (1,0):klaente.sendall(struct.pack('>BBHH',5,konope,가로,세로))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            klika_boleng(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for tlhaka_boleng in '한글':누름값(0x1000000|ord(tlhaka_boleng));누름값(0x1000000|ord(tlhaka_boleng),False)
            for 횟수 in (1,2):
                Diriša=len(대화기록);klika_boleng(180,242)
                수신하기(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Diriša)
            time.sleep(.3)
            lefastere_sethalwa=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=lefastere_sethalwa.crop((110,272,530,300)).tobytes()
            lefastere_sethalwa.save(str(결과자료/'java-swing.png'))
            Diriša=len(대화기록);klika_boleng(535,105)
            assert 'exit 0' in 수신하기(b'jkoros-native> ',Diriša)
        # Download the guest-created bytes through FTP in the same GUI VM.
        faele_go_tsenya_tshedimošo_leina={'java':'java.txt','c':'c.txt','python':'python.txt'}[Polelo]
        šele('cp '+faele_go_tsenya_tshedimošo_leina+' /kgonthiša_5fb2b747.txt')
        받은수=bytearray();faele_fetišetša_kgokaganya.retrbinary('RETR kgonthiša_5fb2b747.txt',받은수.extend);assert 받은수==예상파일.encode()
        šele('echo preserved > 출력예제.'+('py' if Polelo=='python' else Polelo))
        assert 'EXAMPLES READY' in šele('example '+Polelo)
        assert '\npreserved\n' in šele('cat 출력예제.'+('py' if Polelo=='python' else Polelo))
        assert '한/영 khii_boleng, Shift+Space 또는 F9' in šele('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in šele('echo GUI NETWORK TOGETHER')
        faele_fetišetša_kgokaganya.quit();faele_fetišetša_kgokaganya=None;assert 'FTP stopped' in šele('ftpd stop')
        print('PASS '+Polelo+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if faele_fetišetša_kgokaganya:
            try:faele_fetišetša_kgokaganya.close()
            except OSError:pass
        if klaente:klaente.close()
        tiragalo_a7054519.terminate()
        try:tiragalo_a7054519.wait(timeout=8)
        except subprocess.TimeoutExpired:tiragalo_a7054519.kill();tiragalo_a7054519.wait()
        sekgethi.close();tiragalo_a7054519.stdout.close();(결과자료/(Polelo+'-serial.log')).write_bytes(대화기록)


def Diriša():
    결과자료=기준/'build/verification/examples';결과자료.mkdir(parents=True,exist_ok=True)
    tiišetšo_pego={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for Polelo in ('java','c','python'):
                test_언어(Polelo,되돌림서버항목,결과자료);tiišetšo_pego['languages'].append(Polelo)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(legoro_boleng,data.encode()) for legoro_boleng,data in 예상결과],되돌림서버항목.수신됨
            tiišetšo_pego['host_network_payloads']=[{'protocol':legoro_boleng,'text':data.decode()} for legoro_boleng,data in 되돌림서버항목.수신됨]
        tiišetšo_pego.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(결과자료/'report.json').write_text(json.dumps(tiišetšo_pego,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Diriša()
